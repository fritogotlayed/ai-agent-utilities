---
name: review
description: |
  Action skill that performs code review on a specified target (files, staged changes, or diff).
  Uses the 'code-review' knowledge skill for review methodology.
  Trigger phrases: "/review", "review this file", "review these changes", "review my PR", "review my code".
type: action
license: MIT
compatibility: claude-3-5-sonnet, claude-3-opus
metadata:
  version: "1.0"
  author: ai-agent-utilities
allowed-tools:
  - mcp_bash
  - mcp_read
  - mcp_grep
  - mcp_lsp_diagnostics
---

# Review Action

When invoked with `/review` or code review trigger phrases, perform a structured code review on the specified target.

## Step 1: Determine Review Target

- **If specific file(s) mentioned**: Review those files directly
- **If "staged" or no target specified**: Review staged changes via `git diff --cached`
- **If "changes" or PR context**: Review `git diff` output or relevant commit range
- **If directory mentioned**: Review all modified files in that directory

## Step 2: Load Code Review Methodology

Load the `code-review` skill to understand the review framework:
- Code quality standards
- Security considerations
- Performance implications
- Maintainability assessment
- Testing coverage expectations

## Step 3: Apply Review Methodology

For each target file or change:

1. **Analyze code structure**: Check organization, naming, complexity
2. **Identify issues**: Security flaws, performance problems, maintainability concerns
3. **Assess quality**: Code style, documentation, test coverage
4. **Evaluate patterns**: Design patterns, anti-patterns, best practices
5. **Check dependencies**: Unused imports, circular dependencies, version conflicts

## Step 4: Organize Findings

Categorize findings by severity:

- **CRITICAL**: Security vulnerabilities, data loss risks, runtime errors
- **HIGH**: Performance issues, architectural problems, breaking changes
- **MEDIUM**: Code quality, maintainability, style violations
- **LOW**: Minor improvements, documentation gaps, refactoring suggestions

## Step 5: Generate Structured Output

Provide findings in this format:

```
## Code Review: [target]

### Summary
- **Verdict**: APPROVE / REQUEST CHANGES
- **Confidence**: [HIGH / MEDIUM / LOW]
- **Rationale**: [Brief explanation of verdict]

### Critical Issues
[List critical findings with line numbers and remediation]

### High Priority Issues
[List high-priority findings]

### Medium Priority Issues
[List medium-priority findings]

### Low Priority Issues
[List low-priority findings]

### Recommendations
[Actionable next steps, refactoring suggestions, testing recommendations]
```

## Step 6: Provide Actionable Feedback

For each issue:
- Specify exact location (file, line number)
- Explain the problem clearly
- Suggest concrete remediation
- Reference relevant standards or best practices

## Invocation Examples

- `/review` — Review staged changes
- `review this file` — Review specified file
- `review my PR` — Review pull request changes
- `review these changes` — Review diff output
- `review my code` — Review current working directory changes
