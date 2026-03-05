"""Comprehensive test suite for aau_toolkit.py — ai-agent-utilities installer core."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

# Ensure repo root is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from aau_toolkit import (
    _BLOCK_BEGIN,
    _BLOCK_END,
    _has_toolkit_skills,
    ensure_symlink,
    install_skills,
    manage_gitignore,
    remove_symlink,
    scan_for_repos,
    uninstall_skills,
)

# ── Helpers ──────────────────────────────────────────────────────────────────

TOOLKIT_DIR = Path(__file__).resolve().parent.parent  # repo root with skills/


def _git_init(path: Path) -> None:
    """Initialize a bare git repo at path (creates .git/)."""
    subprocess.run(
        ["git", "init", str(path)],
        capture_output=True,
        check=True,
    )


# ── Symlink engine tests ────────────────────────────────────────────────────


def test_ensure_symlink_creates_new(tmp_path):
    """Fresh install creates symlink, returns 'created'."""
    src = tmp_path / "source"
    src.mkdir()
    dst = tmp_path / "target" / "link"

    result = ensure_symlink(src, dst)

    assert result == "created"
    assert dst.is_symlink()
    assert dst.resolve() == src.resolve()


def test_ensure_symlink_idempotent(tmp_path):
    """Existing correct symlink returns 'exists'."""
    src = tmp_path / "source"
    src.mkdir()
    dst = tmp_path / "link"

    ensure_symlink(src, dst)
    result = ensure_symlink(src, dst)

    assert result == "exists"
    assert dst.is_symlink()


def test_ensure_symlink_replaces_broken(tmp_path):
    """Broken symlink replaced, returns 'replaced'."""
    src = tmp_path / "source"
    src.mkdir()
    # Create a broken symlink pointing to nonexistent target
    dst = tmp_path / "link"
    dst.symlink_to(tmp_path / "nonexistent")
    assert dst.is_symlink()
    assert not dst.exists()  # broken

    result = ensure_symlink(src, dst)

    assert result == "replaced"
    assert dst.is_symlink()
    assert dst.resolve() == src.resolve()


def test_ensure_symlink_replaces_wrong_target(tmp_path):
    """Symlink to wrong target replaced, returns 'replaced'."""
    src_a = tmp_path / "a"
    src_a.mkdir()
    src_b = tmp_path / "b"
    src_b.mkdir()
    dst = tmp_path / "link"

    ensure_symlink(src_a, dst)
    assert dst.resolve() == src_a.resolve()

    result = ensure_symlink(src_b, dst)

    assert result == "replaced"
    assert dst.resolve() == src_b.resolve()


def test_ensure_symlink_conflict_real_file(tmp_path):
    """Real file at destination raises FileExistsError."""
    src = tmp_path / "source"
    src.mkdir()
    dst = tmp_path / "blocker"
    dst.write_text("I am a real file")

    with pytest.raises(FileExistsError):
        ensure_symlink(src, dst)


def test_ensure_symlink_conflict_real_dir(tmp_path):
    """Real directory at destination raises FileExistsError."""
    src = tmp_path / "source"
    src.mkdir()
    dst = tmp_path / "blocker_dir"
    dst.mkdir()

    with pytest.raises(FileExistsError):
        ensure_symlink(src, dst)


def test_ensure_symlink_creates_parents(tmp_path):
    """Parent directories created automatically."""
    src = tmp_path / "source"
    src.mkdir()
    dst = tmp_path / "deep" / "nested" / "path" / "link"

    result = ensure_symlink(src, dst)

    assert result == "created"
    assert dst.is_symlink()
    assert (tmp_path / "deep" / "nested" / "path").is_dir()


# ── Gitignore manager tests ─────────────────────────────────────────────────


def test_gitignore_add_block(tmp_path):
    """Adds managed block with entries."""
    manage_gitignore(
        tmp_path, [".claude/skills/code-review", ".claude/skills/test"], "add"
    )

    content = (tmp_path / ".gitignore").read_text()
    assert _BLOCK_BEGIN in content
    assert _BLOCK_END in content
    assert ".claude/skills/code-review" in content
    assert ".claude/skills/test" in content


def test_gitignore_add_idempotent(tmp_path):
    """Re-adding same entries doesn't duplicate block."""
    entries = [".claude/skills/code-review"]
    manage_gitignore(tmp_path, entries, "add")
    manage_gitignore(tmp_path, entries, "add")

    content = (tmp_path / ".gitignore").read_text()
    assert content.count(_BLOCK_BEGIN) == 1
    assert content.count(_BLOCK_END) == 1


def test_gitignore_remove_block(tmp_path):
    """Removes managed block, preserves other content."""
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text("*.pyc\n__pycache__/\n")

    manage_gitignore(tmp_path, [".claude/skills/test"], "add")
    assert _BLOCK_BEGIN in gitignore.read_text()

    manage_gitignore(tmp_path, [], "remove")
    content = gitignore.read_text()
    assert _BLOCK_BEGIN not in content
    assert _BLOCK_END not in content
    assert "*.pyc" in content
    assert "__pycache__/" in content


def test_gitignore_add_creates_file(tmp_path):
    """Creates .gitignore if missing."""
    gitignore = tmp_path / ".gitignore"
    assert not gitignore.exists()

    manage_gitignore(tmp_path, [".claude/skills/test"], "add")

    assert gitignore.exists()
    assert _BLOCK_BEGIN in gitignore.read_text()


def test_gitignore_preserves_existing(tmp_path):
    """Existing entries outside block are untouched."""
    gitignore = tmp_path / ".gitignore"
    original = "# Custom ignores\n*.log\n.env\n"
    gitignore.write_text(original)

    manage_gitignore(tmp_path, [".claude/skills/test"], "add")

    content = gitignore.read_text()
    assert "# Custom ignores" in content
    assert "*.log" in content
    assert ".env" in content
    assert _BLOCK_BEGIN in content


# ── Remove symlink tests ────────────────────────────────────────────────────


def test_remove_symlink_removes_valid(tmp_path):
    """remove_symlink removes symlink pointing under expected prefix."""
    src = tmp_path / "toolkit" / "skills" / "test"
    src.mkdir(parents=True)
    dst = tmp_path / "repo" / ".claude" / "skills" / "test"
    dst.parent.mkdir(parents=True)
    dst.symlink_to(src)

    result = remove_symlink(dst, tmp_path / "toolkit")

    assert result is True
    assert not dst.exists()


def test_remove_symlink_skips_wrong_prefix(tmp_path):
    """remove_symlink skips symlink pointing outside expected prefix."""
    other = tmp_path / "other"
    other.mkdir()
    dst = tmp_path / "link"
    dst.symlink_to(other)

    result = remove_symlink(dst, tmp_path / "toolkit")

    assert result is False
    assert dst.is_symlink()  # still there


def test_remove_symlink_skips_non_symlink(tmp_path):
    """remove_symlink returns False for non-symlink."""
    regular_file = tmp_path / "file.txt"
    regular_file.write_text("hello")

    result = remove_symlink(regular_file, tmp_path)

    assert result is False


# ── Install/uninstall integration tests ─────────────────────────────────────


def test_install_all_skills(tmp_path):
    """Installs all 10 skills, verifies symlinks + .gitignore."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git_init(repo)

    result = install_skills(TOOLKIT_DIR, repo)

    assert len(result["created"]) == 10
    assert len(result["conflicts"]) == 0
    assert len(result["exists"]) == 0
    assert len(result["replaced"]) == 0

    # Verify symlinks exist
    skills_dir = repo / ".claude" / "skills"
    assert skills_dir.is_dir()
    assert (skills_dir / "code-review").is_symlink()
    assert (skills_dir / "test").is_symlink()

    # Verify .gitignore updated
    gitignore = repo / ".gitignore"
    assert gitignore.exists()
    content = gitignore.read_text()
    assert _BLOCK_BEGIN in content
    assert ".claude/skills/code-review" in content


def test_install_selective(tmp_path):
    """skill_names=['code-review'] installs only that one."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git_init(repo)

    result = install_skills(TOOLKIT_DIR, repo, skill_names=["code-review"])

    assert result["created"] == ["code-review"]
    assert len(result["conflicts"]) == 0
    assert (repo / ".claude" / "skills" / "code-review").is_symlink()
    # Other skills NOT installed
    assert not (repo / ".claude" / "skills" / "test").exists()


def test_install_two_phase_conflict(tmp_path):
    """Real file in target → zero installs (all-or-nothing)."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git_init(repo)

    # Place a real directory at one skill's target path
    conflict_dir = repo / ".claude" / "skills" / "code-review"
    conflict_dir.mkdir(parents=True)
    (conflict_dir / "readme.txt").write_text("custom content")

    result = install_skills(TOOLKIT_DIR, repo)

    # Conflict detected
    assert "code-review" in result["conflicts"]
    # Nothing was installed (all-or-nothing)
    assert len(result["created"]) == 0
    assert len(result["replaced"]) == 0
    assert len(result["exists"]) == 0


def test_install_idempotent(tmp_path):
    """Double install → no errors, all 'exists'."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git_init(repo)

    result1 = install_skills(TOOLKIT_DIR, repo)
    assert len(result1["created"]) == 10

    result2 = install_skills(TOOLKIT_DIR, repo)
    assert len(result2["exists"]) == 10
    assert len(result2["created"]) == 0
    assert len(result2["conflicts"]) == 0


def test_uninstall_removes_toolkit_only(tmp_path):
    """Custom skill dirs are preserved during uninstall."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git_init(repo)

    # Install toolkit skills
    install_skills(TOOLKIT_DIR, repo)

    # Add a custom (non-toolkit) skill directory
    custom_skill = repo / ".claude" / "skills" / "my-custom-skill"
    custom_skill.mkdir(parents=True)
    (custom_skill / "SKILL.md").write_text("# Custom Skill")

    result = uninstall_skills(TOOLKIT_DIR, repo)

    assert len(result["removed"]) == 11  # 10 skills + README.md
    assert "my-custom-skill" in result["skipped"]
    # Custom skill preserved
    assert custom_skill.is_dir()
    assert (custom_skill / "SKILL.md").exists()


def test_uninstall_removes_gitignore_block(tmp_path):
    """Managed block cleaned up after uninstall."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git_init(repo)

    install_skills(TOOLKIT_DIR, repo)
    gitignore = repo / ".gitignore"
    assert _BLOCK_BEGIN in gitignore.read_text()

    uninstall_skills(TOOLKIT_DIR, repo)

    content = gitignore.read_text()
    assert _BLOCK_BEGIN not in content
    assert _BLOCK_END not in content


def test_uninstall_preserves_claude_dir(tmp_path):
    """.claude/ directory not deleted after uninstall."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git_init(repo)

    install_skills(TOOLKIT_DIR, repo)
    assert (repo / ".claude" / "skills").is_dir()

    uninstall_skills(TOOLKIT_DIR, repo)

    # .claude/ and .claude/skills/ still exist
    assert (repo / ".claude").is_dir()
    assert (repo / ".claude" / "skills").is_dir()


# ── Repo discovery (scan) tests ─────────────────────────────────────────────


def test_scan_finds_repos(tmp_path):
    """Discovers git repos in temp dir tree."""
    # Create three repos at different depths
    repo_a = tmp_path / "projects" / "alpha"
    repo_a.mkdir(parents=True)
    _git_init(repo_a)

    repo_b = tmp_path / "projects" / "beta"
    repo_b.mkdir(parents=True)
    _git_init(repo_b)

    repo_c = tmp_path / "other" / "gamma"
    repo_c.mkdir(parents=True)
    _git_init(repo_c)

    repos = scan_for_repos(tmp_path)

    assert len(repos) == 3
    assert repo_a in repos
    assert repo_b in repos
    assert repo_c in repos


def test_scan_prunes_node_modules(tmp_path):
    """Skips pruned directories (node_modules, .cache, etc.)."""
    # Repo inside node_modules should NOT be found
    nm_repo = tmp_path / "node_modules" / "some-package"
    nm_repo.mkdir(parents=True)
    _git_init(nm_repo)

    # Repo inside .cache should NOT be found
    cache_repo = tmp_path / ".cache" / "cached-repo"
    cache_repo.mkdir(parents=True)
    _git_init(cache_repo)

    # Regular repo SHOULD be found
    real_repo = tmp_path / "my-project"
    real_repo.mkdir()
    _git_init(real_repo)

    repos = scan_for_repos(tmp_path)

    assert real_repo in repos
    assert nm_repo not in repos
    assert cache_repo not in repos


def test_scan_respects_max_depth(tmp_path):
    """Depth-limited traversal works."""
    # Repo at depth 1 — should be found
    shallow = tmp_path / "shallow"
    shallow.mkdir()
    _git_init(shallow)

    # Repo at depth 3 — should NOT be found with max_depth=2
    deep = tmp_path / "a" / "b" / "deep"
    deep.mkdir(parents=True)
    _git_init(deep)

    repos = scan_for_repos(tmp_path, max_depth=2)

    assert shallow in repos
    assert deep not in repos


def test_scan_handles_permission_error(tmp_path):
    """PermissionError → skip, not crash."""
    # Create a directory with no read permission
    forbidden = tmp_path / "forbidden"
    forbidden.mkdir()
    forbidden.chmod(0o000)

    # Create a regular repo that should still be found
    repo = tmp_path / "accessible"
    repo.mkdir()
    _git_init(repo)

    try:
        repos = scan_for_repos(tmp_path)
        assert repo in repos
        # Should not crash — the forbidden dir is simply skipped
    finally:
        # Restore permissions for cleanup
        forbidden.chmod(0o755)


def test_scan_returns_sorted(tmp_path):
    """scan_for_repos returns repos in sorted order."""
    for name in ["zeta", "alpha", "mu"]:
        r = tmp_path / name
        r.mkdir()
        _git_init(r)

    repos = scan_for_repos(tmp_path)

    assert repos == sorted(repos)


def test_scan_empty_directory(tmp_path):
    """Empty directory returns empty list."""
    repos = scan_for_repos(tmp_path)
    assert repos == []


def test_scan_does_not_descend_into_repos(tmp_path):
    """Once a .git dir is found, scanner does not descend further."""
    # Create parent repo
    parent = tmp_path / "parent"
    parent.mkdir()
    _git_init(parent)

    # Create nested repo inside parent (should NOT be found)
    nested = parent / "sub" / "nested"
    nested.mkdir(parents=True)
    _git_init(nested)

    repos = scan_for_repos(tmp_path)

    assert parent in repos
    assert nested not in repos


# ── _has_toolkit_skills tests ─────────────────────────────────────────────────


def test_has_toolkit_skills_with_installed(tmp_path):
    """Repo with at least one toolkit symlink in .claude/skills/ returns True."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git_init(repo)
    skills_dir = repo / ".claude" / "skills"
    skills_dir.mkdir(parents=True)
    # Create a symlink pointing into TOOLKIT_DIR/skills/
    (skills_dir / "code-review").symlink_to(TOOLKIT_DIR / "skills" / "code-review")
    assert _has_toolkit_skills(TOOLKIT_DIR, repo) is True


def test_has_toolkit_skills_no_claude_dir(tmp_path):
    """Repo without .claude/ directory returns False."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git_init(repo)
    assert _has_toolkit_skills(TOOLKIT_DIR, repo) is False


def test_has_toolkit_skills_empty_skills_dir(tmp_path):
    """Repo with empty .claude/skills/ directory returns False."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git_init(repo)
    (repo / ".claude" / "skills").mkdir(parents=True)
    assert _has_toolkit_skills(TOOLKIT_DIR, repo) is False


def test_has_toolkit_skills_custom_only(tmp_path):
    """Repo with only non-toolkit real directories in .claude/skills/ returns False."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git_init(repo)
    skills_dir = repo / ".claude" / "skills"
    skills_dir.mkdir(parents=True)
    # Real directory (not a symlink), not from toolkit
    (skills_dir / "my-custom-skill").mkdir()
    assert _has_toolkit_skills(TOOLKIT_DIR, repo) is False


def test_has_toolkit_skills_mixed(tmp_path):
    """Repo with both toolkit symlinks and custom dirs returns True."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git_init(repo)
    skills_dir = repo / ".claude" / "skills"
    skills_dir.mkdir(parents=True)
    # Custom real directory
    (skills_dir / "my-custom-skill").mkdir()
    # Toolkit symlink
    (skills_dir / "code-review").symlink_to(TOOLKIT_DIR / "skills" / "code-review")
    assert _has_toolkit_skills(TOOLKIT_DIR, repo) is True


# ── uninstall --scan integration tests ────────────────────────────────────────────


def test_uninstall_scan_filters_repos(tmp_path):
    """scan + filter shows only repos with toolkit skills installed."""
    # Create 3 git repos
    repo_a = tmp_path / "repo_a"
    repo_b = tmp_path / "repo_b"
    repo_c = tmp_path / "repo_c"
    for repo in (repo_a, repo_b, repo_c):
        repo.mkdir()
        _git_init(repo)

    # Install toolkit skills in repo_a and repo_b only
    for repo in (repo_a, repo_b):
        skills_dir = repo / ".claude" / "skills"
        skills_dir.mkdir(parents=True)
        (skills_dir / "code-review").symlink_to(TOOLKIT_DIR / "skills" / "code-review")

    # Scan and filter
    repos = scan_for_repos(tmp_path, max_depth=2)
    filtered = [r for r in repos if _has_toolkit_skills(TOOLKIT_DIR, r)]

    assert len(filtered) == 2
    assert repo_a in filtered
    assert repo_b in filtered
    assert repo_c not in filtered


def test_uninstall_scan_no_git_repos(tmp_path):
    """Scanning directory with no git repos returns empty list."""
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    repos = scan_for_repos(empty_dir, max_depth=3)
    assert repos == []


def test_uninstall_scan_no_toolkit_repos(tmp_path):
    """Scanning directory where repos have no toolkit skills returns empty after filter."""
    # Create 2 git repos without toolkit skills
    for name in ("repo_x", "repo_y"):
        r = tmp_path / name
        r.mkdir()
        _git_init(r)

    repos = scan_for_repos(tmp_path, max_depth=2)
    assert len(repos) == 2  # both repos found

    filtered = [r for r in repos if _has_toolkit_skills(TOOLKIT_DIR, r)]
    assert filtered == []  # none have toolkit skills
