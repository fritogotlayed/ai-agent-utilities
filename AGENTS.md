# PROJECT KNOWLEDGE BASE

## OVERVIEW

Python CLI toolkit that symlinks reusable AI agent skills (SKILL.md files following the [Agent Skills](https://agentskills.io) standard) into target repositories. Single-module design — all logic lives in `aau_toolkit.py`. No third-party runtime dependencies; stdlib only.

**Target:** Python 3.9+ on Linux/macOS. Windows is explicitly unsupported (hard error at import time).

## STRUCTURE

```
ai-agent-utilities/
├── aau_toolkit.py           # ALL source code — CLI + installer logic (single module)
├── pyproject.toml           # Project metadata + pytest config
├── tests/
│   ├── conftest.py          # Pytest fixtures (currently empty)
│   └── test_install.py      # 29 tests covering symlink engine, gitignore, install/uninstall, scan
├── skills/                  # 10 skill directories, each containing SKILL.md
│   ├── code-review/         # Knowledge skills (loaded as context)
│   ├── security-audit/
│   ├── documentation/
│   ├── refactoring/
│   ├── skill-builder/
│   ├── review/              # Action skills (invoked directly)
│   ├── test/
│   ├── security/
│   ├── docs/
│   └── new-skill/
├── README.md
├── LICENSE                  # MIT
└── .gitignore
```

## COMMANDS

```bash
# Run all tests
python -m pytest

# Run tests verbose
python -m pytest -v

# Run a single test by name
python -m pytest tests/test_install.py::test_ensure_symlink_creates_new

# Run tests matching a keyword
python -m pytest -k "gitignore"

# Run with short traceback (recommended for CI)
python -m pytest --tb=short

# CLI usage
python3 aau_toolkit.py install /path/to/repo
python3 aau_toolkit.py uninstall /path/to/repo
python3 aau_toolkit.py list
python3 aau_toolkit.py scan ~/projects --max-depth 3
```

**Test dependencies:** Install with `pip install -e ".[test]"` (pytest >= 7.0, pyyaml >= 6.0).

There is no linter or formatter configured in `pyproject.toml`. A `.ruff_cache/` directory exists, suggesting ruff has been used during development — follow the style conventions below.

## CODE STYLE

### Imports

- **Always** start source files with `from __future__ import annotations`
- Group imports: stdlib first, then third-party, then local — separated by blank lines
- Within stdlib group, one import per line, roughly alphabetical: `os`, `re`, `sys`, `argparse`, `pathlib`
- Import specific names from pathlib: `from pathlib import Path`
- Tests import directly from the module: `from aau_toolkit import ensure_symlink, install_skills`

### Types & Annotations

- Use modern union syntax: `str | None`, `list[str] | None` (safe because of `__future__.annotations`)
- Use lowercase generics: `list[str]`, `dict[str, list[str]]`, `tuple[Path, int]`
- Annotate all function signatures (parameters + return type)
- No `as any` / `# type: ignore` equivalents — keep type correctness

### Naming

- Functions and variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE` (e.g., `_BLOCK_BEGIN`, `_PRUNE_DIRS`)
- Private/internal functions: prefix with `_` (e.g., `_get_managed_entries`, `_parse_frontmatter`)
- CLI handlers: `cmd_<subcommand>` (e.g., `cmd_install`, `cmd_scan`)
- Test functions: `test_<unit>_<scenario>` (e.g., `test_ensure_symlink_creates_new`)

### Functions & Docstrings

- Pure functional style — no classes. Module-level functions only.
- Google-style docstrings with `Args:`, `Returns:`, `Raises:` sections
- Every public function gets a docstring describing behavior, return values, and exceptions
- Keep functions focused: one responsibility per function

```python
def ensure_symlink(src: Path, dst: Path) -> str:
    """Create symlink dst -> src.

    Returns:
        'created' if new symlink created
        'exists' if correct symlink already present (idempotent)
        'replaced' if stale/broken/wrong-target symlink replaced

    Raises:
        FileExistsError: if dst is a real file or real directory
    """
```

### Error Handling

- Raise specific exception types: `FileExistsError`, `RuntimeError` — never bare `Exception`
- Catch specific exceptions: `except (OSError, ValueError)` — never bare `except`
- CLI commands use `sys.exit(1)` for error exit codes
- Fail-safe patterns: check-then-act with graceful fallbacks (e.g., `PermissionError` → skip + warn)

### Formatting

- 4-space indentation
- Double quotes for strings
- Trailing commas in multi-line data structures and function args
- Black-compatible line length (88 chars)
- Blank line between top-level functions, two blank lines before function definitions
- ANSI color constants as module-level private vars (`_GREEN`, `_RED`, etc.)

### Path Operations

- Use `pathlib.Path` everywhere — never raw string path manipulation
- Resolve paths before comparison: `dst.resolve() == src.resolve()`
- Create parent dirs with `mkdir(parents=True, exist_ok=True)`
- Check existence with `.is_symlink()`, `.is_dir()`, `.exists()` — order matters for symlinks

## TESTING CONVENTIONS

- All tests in `tests/test_install.py`, flat function style (no test classes)
- Use `tmp_path` fixture for filesystem isolation — never touch the real filesystem
- Each test gets a one-line docstring explaining what it verifies
- Helper functions at top of test file (e.g., `_git_init`)
- Test naming: `test_<component>_<behavior>` (e.g., `test_install_two_phase_conflict`)
- Tests reference `TOOLKIT_DIR` constant pointing to repo root for real skill fixtures
- Integration tests use real skills directory for end-to-end verification

## ARCHITECTURE NOTES

- **Single-module design**: Everything in `aau_toolkit.py`. No packages, no src/ layout.
- **Two-phase install**: Phase 1 scans for conflicts, Phase 2 creates symlinks only if zero conflicts (all-or-nothing).
- **Managed gitignore block**: Entries wrapped in `BEGIN/END MANAGED BY` markers for clean add/remove.
- **Symlink-based distribution**: Skills live here, symlinks go into target repos. `git pull` updates propagate automatically.
- **Skills are SKILL.md files**: YAML frontmatter (name, description, metadata) + markdown body. Parsed with a custom stdlib-only YAML parser (`_parse_frontmatter`).
- **No runtime dependencies**: stdlib only. Test deps (pytest, pyyaml) are optional.
