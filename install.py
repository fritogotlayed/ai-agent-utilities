"""ai-agent-utilities installer core module.

Functions:
    ensure_symlink: Create/verify/replace symlinks
    remove_symlink: Safely remove toolkit symlinks
    manage_gitignore: Manage .gitignore managed block
    install_skills: Two-phase skill installation
    uninstall_skills: Skill uninstallation
"""

import os
import re
import sys
import argparse
from pathlib import Path

if sys.platform == "win32":
    raise RuntimeError(
        "ai-agent-utilities does not support Windows in v1. Use Linux or macOS."
    )

_BLOCK_BEGIN = "# BEGIN MANAGED BY ai-agent-utilities"
_BLOCK_END = "# END MANAGED BY ai-agent-utilities"


def ensure_symlink(src: Path, dst: Path) -> str:
    """Create symlink dst -> src.

    Returns:
        'created' if new symlink created
        'exists' if correct symlink already present (idempotent)
        'replaced' if stale/broken/wrong-target symlink replaced

    Raises:
        FileExistsError: if dst is a real file or real directory
    """
    if dst.is_symlink():
        if dst.resolve() == src.resolve():
            return "exists"
        dst.unlink()
        dst.symlink_to(src)
        return "replaced"
    elif dst.exists():
        raise FileExistsError(
            f"Conflict: {dst} exists and is not a symlink. "
            "Remove it manually or use a different target."
        )
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.symlink_to(src)
        return "created"


def remove_symlink(dst: Path, expected_src_prefix: Path) -> bool:
    """Remove dst symlink only if it points under expected_src_prefix.

    Returns:
        True if symlink was removed
        False if skipped (not a symlink, wrong target, or safety check failed)
    """
    if not dst.is_symlink():
        return False
    try:
        target = dst.resolve()
        if str(target).startswith(str(expected_src_prefix.resolve())):
            dst.unlink()
            return True
    except (OSError, ValueError):
        pass
    return False


def manage_gitignore(repo_dir: Path, entries: list[str], action: str) -> None:
    """Manage the MANAGED BY ai-agent-utilities block in .gitignore.

    Args:
        repo_dir: Repository root directory
        entries: List of paths to add to .gitignore (for action='add')
        action: 'add' to add/replace block, 'remove' to remove block
    """
    gitignore_path = repo_dir / ".gitignore"

    if action == "add":
        existing = gitignore_path.read_text() if gitignore_path.exists() else ""
        block_lines = [_BLOCK_BEGIN] + entries + [_BLOCK_END]
        block_str = "\n".join(block_lines)

        pattern = re.compile(
            rf"{re.escape(_BLOCK_BEGIN)}.*?{re.escape(_BLOCK_END)}",
            re.DOTALL,
        )
        if pattern.search(existing):
            new_content = pattern.sub(block_str, existing)
        else:
            sep = "\n" if existing and not existing.endswith("\n") else ""
            new_content = existing + sep + block_str + "\n"

        gitignore_path.write_text(new_content)

    elif action == "remove":
        if not gitignore_path.exists():
            return
        existing = gitignore_path.read_text()
        pattern = re.compile(
            rf"\n?{re.escape(_BLOCK_BEGIN)}.*?{re.escape(_BLOCK_END)}\n?",
            re.DOTALL,
        )
        new_content = pattern.sub("", existing)
        gitignore_path.write_text(new_content)


def install_skills(
    toolkit_dir: Path,
    repo_dir: Path,
    skill_names: list[str] | None = None,
) -> dict:
    """Two-phase skill installation.

    Phase 1: Scan for conflicts (real non-symlink files at target paths).
    Phase 2: Create symlinks only if zero conflicts found.

    Returns:
        dict with keys 'created', 'exists', 'replaced', 'conflicts'
        Each value is a list of skill name strings.
    """
    skills_dir = toolkit_dir / "skills"
    result: dict[str, list[str]] = {
        "created": [],
        "exists": [],
        "replaced": [],
        "conflicts": [],
    }

    if not skills_dir.is_dir():
        return result

    skill_dirs = sorted(
        d
        for d in skills_dir.iterdir()
        if d.is_dir() and (skill_names is None or d.name in skill_names)
    )

    # Phase 1: scan for conflicts
    target_base = repo_dir / ".claude" / "skills"
    for skill_dir in skill_dirs:
        target = target_base / skill_dir.name
        if target.exists() and not target.is_symlink():
            result["conflicts"].append(skill_dir.name)

    if result["conflicts"]:
        return result

    # Phase 2: create symlinks (only if zero conflicts)
    gitignore_entries = []
    for skill_dir in skill_dirs:
        target = target_base / skill_dir.name
        status = ensure_symlink(skill_dir.resolve(), target)
        result[status].append(skill_dir.name)
        gitignore_entries.append(f".claude/skills/{skill_dir.name}")

    # Phase 3: update .gitignore
    if gitignore_entries:
        existing_entries = _get_managed_entries(repo_dir)
        all_entries = sorted(set(existing_entries + gitignore_entries))
        manage_gitignore(repo_dir, all_entries, "add")

    return result


def uninstall_skills(toolkit_dir: Path, repo_dir: Path) -> dict:
    """Remove toolkit symlinks from repo_dir/.claude/skills/.

    Only removes symlinks pointing to paths under toolkit_dir.
    Does NOT remove .claude/ or .claude/skills/ directories.

    Returns:
        dict with keys 'removed', 'skipped' (lists of skill name strings)
    """
    result: dict[str, list[str]] = {"removed": [], "skipped": []}
    skills_target = repo_dir / ".claude" / "skills"

    if not skills_target.is_dir():
        return result

    for item in sorted(skills_target.iterdir()):
        if remove_symlink(item, toolkit_dir):
            result["removed"].append(item.name)
        else:
            result["skipped"].append(item.name)

    manage_gitignore(repo_dir, [], "remove")

    return result


def _get_managed_entries(repo_dir: Path) -> list[str]:
    """Read current entries from the managed .gitignore block."""
    gitignore_path = repo_dir / ".gitignore"
    if not gitignore_path.exists():
        return []
    content = gitignore_path.read_text()
    pattern = re.compile(
        rf"{re.escape(_BLOCK_BEGIN)}\n(.*?){re.escape(_BLOCK_END)}",
        re.DOTALL,
    )
    m = pattern.search(content)
    if not m:
        return []
    return [line for line in m.group(1).splitlines() if line.strip()]

_PRUNE_DIRS = {
    "node_modules", ".git", ".cache", "vendor",
    ".venv", "venv", "__pycache__", "dist", "build",
}


def scan_for_repos(root_dir: Path, max_depth: int = 5) -> list[Path]:
    """Discover git repositories under root_dir using os.scandir with manual stack.

    Uses depth-limited traversal with pruning. A directory is a git repo
    if it contains a .git entry (file or directory). Once found, does not
    descend into the repo.
    """
    repos: list[Path] = []
    # Stack: list of (path, current_depth)
    stack: list[tuple[Path, int]] = [(root_dir, 0)]

    while stack:
        current, depth = stack.pop()
        if depth > max_depth:
            continue
        try:
            entries = list(os.scandir(current))
        except PermissionError:
            print(f"  Warning: skipping {current} (permission denied)", file=sys.stderr)
            continue
        except OSError:
            continue

        # Check if this directory is a git repo
        has_git = any(e.name == ".git" for e in entries)
        if has_git:
            repos.append(current)
            continue  # Don't descend into git repos

        # Descend into subdirectories (skip pruned dirs)
        for entry in sorted(entries, key=lambda e: e.name):
            if entry.name in _PRUNE_DIRS:
                continue
            try:
                if entry.is_dir(follow_symlinks=False):
                    stack.append((Path(entry.path), depth + 1))
            except OSError:
                continue

    return sorted(repos)

# ── ANSI colour helpers (stdlib only) ──────────────────────────────────────
_GREEN = "\033[32m"
_YELLOW = "\033[33m"
_DIM = "\033[2m"
_RED = "\033[31m"
_BOLD = "\033[1m"
_RESET = "\033[0m"


def _parse_frontmatter(text: str) -> dict:
    """Parse simple YAML frontmatter from SKILL.md without yaml dependency."""
    parts = text.split("---")
    if len(parts) < 3:
        return {}
    fm_lines = parts[1].strip().splitlines()
    result: dict[str, str] = {}
    current_key: str | None = None
    for line in fm_lines:
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            value = value.strip()
            if value == "|":
                current_key = key.strip()
                result[current_key] = ""
            else:
                current_key = None
                result[key.strip()] = value
        elif current_key and line.startswith("  "):
            if result[current_key]:
                result[current_key] += " " + line.strip()
            else:
                result[current_key] = line.strip()
    return result


def cmd_install(args) -> None:
    """Handle the 'install' subcommand."""
    toolkit_dir = Path(__file__).resolve().parent
    has_error = False

    for repo in args.repos:
        repo = Path(repo).resolve()
        if not repo.is_dir():
            print(f"{_RED}\u2717 Repository not found: {repo}{_RESET}")
            has_error = True
            continue

        skill_names = None
        if args.skills:
            skill_names = [s.strip() for s in args.skills.split(",")]

        result = install_skills(toolkit_dir, repo, skill_names)

        print(f"\n{_BOLD}Installing to {repo}{_RESET}")
        for name in result["created"]:
            print(f"  {_GREEN}\u2713 {name} \u2014 created{_RESET}")
        for name in result["replaced"]:
            print(f"  {_YELLOW}\u21bb {name} \u2014 replaced{_RESET}")
        for name in result["exists"]:
            print(f"  {_DIM}\u2022 {name} \u2014 exists{_RESET}")
        for name in result["conflicts"]:
            print(f"  {_RED}\u2717 {name} \u2014 conflict{_RESET}")
            has_error = True

        if not result["conflicts"]:
            ok = len(result["created"]) + len(result["replaced"]) + len(result["exists"])
            print(f"  {ok} skill(s) ready")

    sys.exit(1 if has_error else 0)


def cmd_uninstall(args) -> None:
    """Handle the 'uninstall' subcommand."""
    toolkit_dir = Path(__file__).resolve().parent
    has_error = False

    for repo in args.repos:
        repo = Path(repo).resolve()
        if not repo.is_dir():
            print(f"{_RED}\u2717 Repository not found: {repo}{_RESET}")
            has_error = True
            continue

        result = uninstall_skills(toolkit_dir, repo)

        print(f"\n{_BOLD}Uninstalling from {repo}{_RESET}")
        for name in result["removed"]:
            print(f"  {_GREEN}\u2713 {name} \u2014 removed{_RESET}")
        for name in result["skipped"]:
            print(f"  {_DIM}\u2022 {name} \u2014 skipped{_RESET}")

        print(f"  {len(result['removed'])} skill(s) removed")

    sys.exit(1 if has_error else 0)


def cmd_list(args) -> None:
    """Handle the 'list' subcommand."""
    toolkit_dir = Path(__file__).resolve().parent
    skills_dir = toolkit_dir / "skills"

    if not skills_dir.is_dir():
        print("No skills directory found.")
        sys.exit(1)

    skills: list[tuple[str, str]] = []
    for skill_dir in sorted(skills_dir.iterdir()):
        skill_md = skill_dir / "SKILL.md"
        if skill_dir.is_dir() and skill_md.exists():
            fm = _parse_frontmatter(skill_md.read_text())
            name = fm.get("name", skill_dir.name)
            desc = fm.get("description", "")
            skills.append((name, desc))

    if not skills:
        print("No skills found.")
        sys.exit(0)

    name_width = max(len(s[0]) for s in skills)
    name_width = max(name_width, 4)  # minimum for "Name" header

    print(f"\n{_BOLD}Available Skills{_RESET}\n")
    print(f"  {'Name':<{name_width}}  Description")
    print(f"  {'\u2500' * name_width}  {'\u2500' * 60}")
    for name, desc in skills:
        if len(desc) > 80:
            desc = desc[:77] + "..."
        print(f"  {name:<{name_width}}  {desc}")
    print(f"\n  {len(skills)} skill(s) available")
    sys.exit(0)


def cmd_scan(args) -> None:
    """Handle the 'scan' subcommand — discover repos and install interactively."""
    root = Path(args.directory).resolve()
    if not root.is_dir():
        print(f"{_RED}\u2717 Directory not found: {args.directory}{_RESET}")
        sys.exit(1)

    repos = scan_for_repos(root, args.max_depth)
    if not repos:
        print("No git repositories found.")
        return

    print(f"\nFound {len(repos)} git repositories:")
    for i, repo in enumerate(repos, 1):
        print(f"  [{i}] {repo}")

    print(
        "\nSelect repos to install (comma-separated numbers, 'all', or 'q' to cancel): ",
        end="",
        flush=True,
    )
    try:
        choice = input().strip()
    except (EOFError, KeyboardInterrupt):
        print("\nCancelled.")
        return

    if not choice or choice.lower() == "q":
        print("Cancelled.")
        return

    if choice.lower() == "all":
        selected = repos
    else:
        try:
            indices = [int(x.strip()) for x in choice.split(",")]
            selected = [repos[i - 1] for i in indices if 1 <= i <= len(repos)]
        except (ValueError, IndexError):
            print(f"{_RED}\u2717 Invalid selection{_RESET}")
            sys.exit(1)

    if not selected:
        print("No valid repos selected.")
        return

    toolkit_dir = Path(__file__).resolve().parent
    skill_names = [s.strip() for s in args.skills.split(",")] if args.skills else None

    for repo in selected:
        result = install_skills(toolkit_dir, repo, skill_names)

        print(f"\n{_BOLD}Installing to {repo}{_RESET}")
        for name in result["created"]:
            print(f"  {_GREEN}\u2713 {name} \u2014 created{_RESET}")
        for name in result["replaced"]:
            print(f"  {_YELLOW}\u21bb {name} \u2014 replaced{_RESET}")
        for name in result["exists"]:
            print(f"  {_DIM}\u2022 {name} \u2014 exists{_RESET}")
        for name in result["conflicts"]:
            print(f"  {_RED}\u2717 {name} \u2014 conflict{_RESET}")

        if not result["conflicts"]:
            ok = len(result["created"]) + len(result["replaced"]) + len(result["exists"])
            print(f"  {ok} skill(s) ready")


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="install.py",
        description="AI Agent Utilities installer \u2014 symlink skills into repositories",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # install
    p_install = subparsers.add_parser("install", help="Install skills to repositories")
    p_install.add_argument("repos", nargs="+", type=Path, help="Repository paths")
    p_install.add_argument(
        "--skills", help="Comma-separated skill names (default: all)"
    )
    p_install.set_defaults(func=cmd_install)

    # uninstall
    p_uninstall = subparsers.add_parser(
        "uninstall", help="Uninstall skills from repositories"
    )
    p_uninstall.add_argument("repos", nargs="+", type=Path, help="Repository paths")
    p_uninstall.set_defaults(func=cmd_uninstall)

    # list
    p_list = subparsers.add_parser("list", help="List available skills")
    p_list.set_defaults(func=cmd_list)

    # scan
    p_scan = subparsers.add_parser(
        "scan", help="Scan directory for repos and install interactively"
    )
    p_scan.add_argument("directory", help="Root directory to scan")
    p_scan.add_argument(
        "--max-depth", type=int, default=5, help="Maximum scan depth (default: 5)"
    )
    p_scan.add_argument(
        "--skills", help="Comma-separated skill names (default: all)"
    )
    p_scan.set_defaults(func=cmd_scan)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
