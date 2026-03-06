---
name: documentation
description: |
  Knowledge skill providing documentation methodology — style matching, structure, and best practices for README,
  API docs, architecture docs, and inline comments. Loaded as background context. Paired with the 'docs' action skill.
  Trigger phrases: "write docs", "generate documentation", "update README", "API docs", "document this".
type: knowledge
metadata:
  version: "1.0"
  author: ai-agent-utilities
---

# Documentation

## Overview

This skill guides the creation and maintenance of comprehensive documentation for software projects. It covers analyzing existing documentation, matching project style, and generating documentation for APIs, architecture, configuration, and user guides.

## When to Use This Skill

Trigger this skill when:
- Writing or updating README files
- Generating API documentation
- Creating architecture documentation
- Writing inline code comments and docstrings
- Documenting configuration options
- Creating quick start guides
- Updating CHANGELOG or release notes
- Documenting known limitations or gotchas

## Process

### 1. Analyze Existing Documentation

Before writing new documentation:
- Locate existing README.md, CONTRIBUTING.md, docs/ directory
- Review existing documentation style: tone, structure, formatting conventions
- Check for inline comments, docstrings, JSDoc/docstring patterns
- Identify documentation gaps and outdated sections
- Note any existing diagrams, code examples, or visual aids

### 2. Match Project Style

Maintain consistency with existing documentation:
- Use the same heading hierarchy (# for main, ## for sections, ### for subsections)
- Match code block formatting and language tags
- Follow existing tone: formal, casual, technical, beginner-friendly
- Use consistent terminology and abbreviations
- Maintain the same list formatting (bullets vs. numbered)
- Keep similar line length and paragraph structure

### 3. What to Document

**Always document:**
- **Public APIs**: Functions, classes, methods, endpoints with parameters and return values
- **Architecture and Design**: System design, component relationships, data flow diagrams (described in text)
- **Installation and Setup**: Prerequisites, installation steps, configuration
- **Quick Start Guide**: Minimal example to get users started
- **Configuration Options**: All configurable parameters with defaults and effects
- **Known Limitations**: Constraints, edge cases, platform-specific issues
- **Gotchas and Pitfalls**: Common mistakes and how to avoid them
- **Examples**: Real-world usage examples for key features

### 4. What NOT to Document

**Skip documenting:**
- Implementation details that change frequently (internal algorithms, refactoring notes)
- Self-explanatory code (obvious variable names, simple logic)
- Temporary workarounds or debugging notes
- Internal-only functions or private APIs
- Redundant information (don't repeat what's in code comments)

### 5. Output Formats

Choose appropriate documentation formats:
- **README.md**: Project overview, quick start, installation, basic usage
- **API Documentation**: JSDoc (JavaScript), docstrings (Python), Javadoc (Java), etc.
- **Architecture Docs**: Design decisions, component diagrams (as text descriptions or ASCII art)
- **CHANGELOG.md**: Version history, breaking changes, new features
- **CONTRIBUTING.md**: Development setup, code style, PR process
- **docs/ directory**: Detailed guides, tutorials, troubleshooting

### 6. Cross-References

Link documentation together:
- Reference related documentation sections
- Link from README to detailed guides
- Cross-reference API docs with examples
- Include "See also" sections for related topics
- Maintain a table of contents for longer documents

## Best Practices

- **Keep it current**: Update documentation when code changes
- **Use examples**: Include code snippets and real-world usage
- **Be specific**: Avoid vague language; use concrete details
- **Structure clearly**: Use headings, lists, and white space
- **Test examples**: Verify code examples actually work
- **Write for users**: Explain the "why" not just the "what"
- **Use consistent formatting**: Follow project conventions
- **Include warnings**: Highlight breaking changes and gotchas

## Common Pitfalls

- Documenting implementation instead of interface
- Letting documentation drift from code
- Writing for experts instead of new users
- Inconsistent formatting and style
- Missing examples or use cases
- Outdated or incorrect information
- Overly technical language for user guides
