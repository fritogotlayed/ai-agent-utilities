---
name: new-skill
description: |
  Action skill that scaffolds a new Agent Skills standard skill in the current project.
  Uses the 'skill-builder' knowledge skill for spec reference and templates.
  Trigger phrases: "/new-skill", "scaffold a new skill", "create new skill file", "create a skill".
type: action
metadata:
  version: "1.0"
  author: ai-agent-utilities
---

# New Skill Action

When invoked, create a new Agent Skills standard skill in the current project.

## Steps

### 1. Gather Information
Ask the user:
- What should the skill be named? (lowercase, hyphens only, max 64 chars)
- What does the skill do? (used for the description)
- What phrases should trigger this skill? (for the description field)

### 2. Validate Skill Name
The name must match: lowercase alphanumeric characters and hyphens only, 1-64 characters.
Valid: `code-review`, `my-tool`, `api3`
Invalid: `MyTool`, `my_tool`, `tool!`

### 3. Load Skill Builder Reference
Load the `skill-builder` skill for the full Agent Skills open standard specification.
Key rules from the spec:
- Only 6 allowed top-level frontmatter fields: `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`
- `version` must be under `metadata.version`, NOT at the top level
- `name` field must match the parent directory name exactly

### 4. Determine Target Directory
Prefer `.claude/skills/` as it works with OpenCode, Claude Code, and Cursor.
Alternative: `.opencode/skills/` if the project uses OpenCode-specific paths.

### 5. Create the Skill
Create `<target-dir>/<skill-name>/SKILL.md` with:
```yaml
---
name: <skill-name>
description: |
  Trigger phrases: <phrases from user>.
  <description from user>
metadata:
  version: "1.0"
---

# <Skill Title>

[Add skill body here based on what the user wants the skill to do]
```

### 6. Verify
Parse the YAML frontmatter to confirm:
- `name` field matches the directory name
- No top-level `version` field exists

### 7. Report
Tell the user:
- Path of the created skill
- How to install it (reference `install.py` from ai-agent-utilities if available)
- Next steps (customize the body)

## Reference
- Agent Skills specification: https://agentskills.io/specification
