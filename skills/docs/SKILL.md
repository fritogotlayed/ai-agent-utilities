---
name: docs
description: |
  Trigger phrases: "/docs", "generate docs", "update documentation", "document this module", "write documentation".
  Action skill: generates or updates documentation for specified target (file, module, or entire project).
metadata:
  version: "1.0"
  author: ai-agent-utilities
---

# Docs Action

## Overview

This action skill generates or updates documentation for specified targets — individual files, modules, or entire projects. It analyzes existing documentation to match style and conventions, then creates or refreshes README files, API documentation, module documentation, and architecture overviews.

## When to Use This Skill

Trigger this skill when:
- Generating documentation for a new module or file
- Updating stale or incomplete documentation
- Creating API documentation for functions or classes
- Writing module-level documentation with usage examples
- Generating architecture overview documentation
- Updating project-level README with current information

## Process

### 1. Determine Target

Identify what needs documentation:
- **Specific file**: Document a single source file with its purpose, functions, and usage
- **Module**: Document a directory/package with overview, components, and examples
- **Project**: Document entire project with README, architecture, and guides

### 2. Load Documentation Skill for Methodology

Reference the `documentation` skill to understand:
- Documentation style and conventions for the project
- What to document (public APIs, architecture, setup, examples)
- What NOT to document (implementation details, temporary notes)
- Best practices for structure, formatting, and cross-references

### 3. Analyze Existing Documentation

Before generating new documentation:
- Locate existing README.md, docs/ directory, inline comments
- Review existing documentation style: tone, structure, formatting conventions
- Check for inline comments, docstrings, JSDoc/docstring patterns
- Identify documentation gaps and outdated sections
- Note any existing diagrams, code examples, or visual aids

### 4. Generate or Update Documentation

Create or refresh documentation files:
- **README** (if project level): Overview, quick start, installation, basic usage
- **API documentation**: Function/class docs with parameters, return values, examples
- **Module documentation**: Purpose, components, usage examples, configuration
- **Architecture overview**: System design, component relationships, data flow (if applicable)

### 5. Preserve Existing Content

Maintain continuity:
- Keep existing content where appropriate
- Update only stale or missing sections
- Preserve custom examples and project-specific notes
- Maintain consistent formatting with existing documentation

### 6. Output Results

List all files created or updated:
- File paths relative to project root
- Brief description of changes (new, updated, refreshed)
- Any warnings about incomplete or placeholder sections

## Best Practices

- **Match project style**: Use same heading hierarchy, tone, formatting as existing docs
- **Include examples**: Provide code snippets and real-world usage patterns
- **Be specific**: Avoid vague language; use concrete details and parameters
- **Structure clearly**: Use headings, lists, and white space for readability
- **Document the "why"**: Explain purpose and design decisions, not just implementation
- **Keep it current**: Update documentation when code changes
- **Cross-reference**: Link related documentation sections together

## Common Pitfalls

- Documenting implementation instead of interface
- Letting documentation drift from code
- Writing for experts instead of new users
- Inconsistent formatting and style
- Missing examples or use cases
- Outdated or incorrect information
