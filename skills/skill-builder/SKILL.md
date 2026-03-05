---
name: skill-builder
description: |
  Meta-skill for creating Agent Skills standard skills. Explains the SKILL.md format, allowed frontmatter fields, naming conventions, and provides complete templates.
  
  Trigger phrases: "create a skill", "new skill", "build a skill", "scaffold skill", "SKILL.md template", "Agent Skills specification"
license: MIT
metadata:
  version: "1.0"
  author: ai-agent-utilities
---

# Skill Builder

A meta-skill for creating new Agent Skills that conform to the open standard specification. This skill teaches the SKILL.md format, frontmatter requirements, and best practices for skill development.

## What is Agent Skills?

Agent Skills is an open standard for creating reusable, cross-tool compatible skills that extend AI agent capabilities. Skills are self-contained modules with:

- **Standardized format** (SKILL.md) for consistency across tools
- **Portable metadata** enabling skills to work across different AI platforms
- **Clear interface** defining what tools, triggers, and capabilities a skill provides
- **Composability** allowing skills to be combined and extended

The Agent Skills specification ensures that a skill created for one tool can be understood and used by another, breaking down silos in the AI agent ecosystem.

## SKILL.md Format

Every Agent Skill is a single markdown file named `SKILL.md` located in a directory matching the skill name. The file has two parts:

### 1. YAML Frontmatter (Required)

Enclosed in `---` delimiters at the top of the file. Contains metadata about the skill.

### 2. Markdown Body (Required)

The skill documentation and implementation details below the frontmatter.

## Allowed Top-Level Frontmatter Fields

Only **6 fields** are allowed at the top level of the YAML frontmatter:

### `name` (Required)
- **Type**: string
- **Rules**: lowercase alphanumeric + hyphens only, 1-64 characters
- **Critical**: MUST match the parent directory name exactly
- **Example**: `name: skill-builder`

### `description` (Required)
- **Type**: string (can be multi-line with `|`)
- **Content**: Brief purpose statement + trigger phrases/conditions
- **Purpose**: Helps AI agents understand when to invoke this skill
- **Example**: Include phrases like "create a skill", "new skill", "build a skill"

### `license` (Optional)
- **Type**: string
- **Purpose**: Specify the license under which the skill is distributed
- **Example**: `license: MIT`

### `compatibility` (Optional)
- **Type**: list of strings
- **Purpose**: Declare which tools/platforms this skill is compatible with
- **Example**: `compatibility: [claude-code, anthropic-cli]`

### `metadata` (Optional)
- **Type**: object/mapping
- **Purpose**: Store additional structured data about the skill
- **Common fields**:
  - `version`: Semantic version (e.g., "1.0", "1.2.3")
  - `author`: Creator/maintainer name
  - `created`: ISO 8601 date
  - `tags`: List of category tags
- **Example**:
  ```yaml
  metadata:
    version: "1.0"
    author: ai-agent-utilities
    tags: [meta, skill-creation]
  ```

### `allowed-tools` (Optional)
- **Type**: list of strings
- **Purpose**: Restrict which tools this skill can use (security/capability control)
- **Example**: `allowed-tools: [mcp_bash, mcp_read, mcp_write]`

## Critical Mistake to Avoid

❌ **WRONG**: Adding `version:` at the top level
```yaml
---
name: my-skill
version: "1.0"  # ← INCORRECT
---
```

✅ **CORRECT**: Nesting `version` under `metadata`
```yaml
---
name: my-skill
metadata:
  version: "1.0"  # ← CORRECT
---
```

This is a common mistake because many YAML-based formats use top-level `version`. Agent Skills reserves the top level for the 6 defined fields only.

## Naming Conventions

- **Directory name**: lowercase, alphanumeric + hyphens (e.g., `skill-builder`)
- **File name**: Always `SKILL.md` (uppercase, exact spelling)
- **Skill name field**: Must match directory name exactly
- **Avoid collisions**: Check existing skills before naming (e.g., `skill-builder` not `skill-creator`)

## Complete SKILL.md Template

Copy and customize this template for new skills:

```markdown
---
name: my-skill
description: |
  Brief description of what this skill does.
  
  Trigger phrases: "phrase one", "phrase two", "phrase three"
license: MIT
metadata:
  version: "1.0"
  author: your-name-or-org
  tags: [category, subcategory]
---

# My Skill

## Overview

Explain what this skill does and why it's useful.

## How to Use

Describe the trigger conditions and expected behavior.

## Implementation Details

Provide any technical details, examples, or guidance for using this skill.

## References

- Link to relevant documentation
- Link to examples or related skills
```

## Body Guidelines

- **Length**: Keep under 5000 tokens for optimal performance
- **Format**: Plain markdown, no special syntax
- **Structure**: Use clear headings (H2, H3) to organize content
- **Examples**: Include concrete examples of skill usage
- **Clarity**: Write for both AI agents and human readers

## Reference

For the complete Agent Skills specification, see: https://agentskills.io/specification

## Related Skills

- `skill-creator` (Anthropic official skill for creating skills)
- Other meta-skills in the ai-agent-utilities collection
