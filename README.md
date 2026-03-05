# AI Agent Utilities

A collection of AI agent skills that can be bootstrapped into any repository, giving your AI coding assistant a consistent set of capabilities across all your projects.

## Quick Start

```bash
git clone https://github.com/your-org/ai-agent-utilities.git ~/ai-agent-utilities
cd ~/ai-agent-utilities
python3 aau_toolkit.py install /path/to/your/repo
```

## Prerequisites

- Python 3.9 or later
- Linux or macOS (Windows is not supported)
- Git

## Usage

### Install skills to a repository

```bash
# Install all skills
python3 aau_toolkit.py install /path/to/repo

# Install to multiple repositories at once
python3 aau_toolkit.py install /path/to/repo1 /path/to/repo2

# Install specific skills only
python3 aau_toolkit.py install /path/to/repo --skills code-review,security-audit
```

### Uninstall skills from a repository

```bash
python3 aau_toolkit.py uninstall /path/to/repo

# Scan for repos with skills and uninstall interactively
python3 aau_toolkit.py uninstall --scan ~/projects

# Limit scan depth
python3 aau_toolkit.py uninstall --scan ~/projects --max-depth 3
```

This removes all symlinks and cleans up the managed `.gitignore` block. Use `--scan` to discover repositories with skills installed and choose which to uninstall.

### Scan a directory for repositories

```bash
# Scan and install interactively
python3 aau_toolkit.py scan ~/projects

# Limit how deep to search
python3 aau_toolkit.py scan ~/projects --max-depth 3
```

The scan command finds git repositories under the given directory and prompts you to choose which ones to install into.

### List available skills

```bash
python3 aau_toolkit.py list
```

## Available Skills

### Knowledge Skills

Loaded as background context — shape how the agent approaches problems.

| Name | Description |
|------|-------------|
| code-review | Systematic code review covering correctness, security, performance, and maintainability |
| documentation | Documentation generation methodology |
| refactoring | Safe, behavior-preserving code refactoring process |
| security-audit | OWASP-aware security analysis and vulnerability assessment |
| skill-builder | Meta-skill for creating new Agent Skills standard skills |

### Action Skills

Invoked directly with a trigger phrase or `/command`. Action skills reference their knowledge counterpart for methodology.

| Name | Uses | Description |
|------|------|-------------|
| review | code-review | Performs code review on specified target (files, staged changes, or diff) |
| docs | documentation | Generates or updates documentation |
| security | security-audit | Performs security analysis on specified target |
| new-skill | skill-builder | Scaffolds new Agent Skills standard skills |
| test | — | Writes and runs tests following project conventions |

## How It Works

Skills are `SKILL.md` files following the [Agent Skills open standard](https://agentskills.io). Each skill lives in its own directory under `skills/`.

When you run `aau_toolkit.py install`, the installer creates symlinks from the target repository's `.claude/skills/` directory back to this toolkit's `skills/` directory. Because they're symlinks, any update you pull into this toolkit (`git pull`) automatically propagates to every repository you've installed into. No re-running the installer needed.

The installer also adds per-symlink entries to the target repository's `.gitignore` inside a managed block, so the symlinks don't accidentally get committed.

## Supported Tools

Any tool that implements the Agent Skills standard will pick up these skills automatically. Currently that includes:

- [OpenCode](https://opencode.ai) (reads `.claude/skills/`)
- [Claude Code](https://claude.ai/code) (reads `.claude/skills/`)
- [Cursor](https://cursor.sh) (reads `.claude/skills/` via Agent Skills standard)
- Any other tool implementing [agentskills.io](https://agentskills.io)

## Creating Custom Skills

Use the `skill-builder` knowledge skill. Once installed, ask your agent to "create a skill" or "scaffold a new skill" and it will walk you through the SKILL.md format, required frontmatter fields, naming conventions, and provide a complete template.

You can also run `aau_toolkit.py list` to see the `new-skill` action skill, which automates the scaffolding step.

## Known Limitations

- Windows is not supported. The installer will exit immediately on Windows.
- Windsurf and Aider do not yet support the Agent Skills standard and won't pick up these skills.

## License

MIT. See [LICENSE](LICENSE).
