---
name: code-review
description: |
  Trigger phrases: "review my code", "code review", "check code quality", "find bugs", "review these changes".
  Performs systematic code review covering security, performance, maintainability, and correctness.
metadata:
  version: "1.0"
  author: ai-agent-utilities
---

# Code Review

A systematic code review skill that examines code across five critical dimensions to identify issues, security vulnerabilities, performance problems, and maintainability concerns.

## Review Methodology

### 1. Understand Context
Before reviewing code, establish the context:
- Read related files and dependencies to understand the codebase structure
- Identify the purpose and scope of the code being reviewed
- Understand the project's architecture, patterns, and conventions
- Note any relevant documentation or specifications
- Consider the target environment and constraints

### 2. Check Correctness
Verify that the code logic is sound and handles all cases:
- Identify logic errors and flawed assumptions
- Check for off-by-one errors and boundary conditions
- Verify edge case handling (null values, empty collections, zero values)
- Ensure error handling is appropriate and complete
- Validate that the code matches its intended behavior
- Check for unreachable code or dead branches

### 3. Check Security
Examine the code for security vulnerabilities and unsafe patterns:
- Identify injection vulnerabilities (SQL, command, template injection)
- Check authentication and authorization logic
- Verify that secrets and credentials are not exposed in code
- Look for unsafe operations (eval, deserialization, unsafe reflection)
- Check input validation and sanitization
- Verify secure handling of sensitive data (encryption, hashing)
- Identify potential privilege escalation issues

### 4. Check Performance
Evaluate the code for efficiency and resource usage:
- Identify unnecessary allocations and memory leaks
- Look for N+1 query patterns and inefficient database access
- Check for blocking calls in async contexts
- Identify inefficient loops and algorithms
- Verify appropriate use of caching and memoization
- Check for unnecessary computations or redundant operations
- Evaluate time and space complexity

### 5. Check Maintainability
Assess code clarity, organization, and long-term sustainability:
- Verify naming clarity (variables, functions, classes)
- Identify excessive complexity and opportunities for simplification
- Check for DRY (Don't Repeat Yourself) violations
- Look for dead code and unused imports
- Verify appropriate abstraction levels
- Check for proper separation of concerns
- Identify technical debt and code smells
- Ensure consistent use of language idioms
- Check for proper documentation and comment quality

## Output Format

Present findings in a structured format:

```
[SEVERITY] file:line — Issue description
  Suggestion: How to fix this issue
```

**Severity Levels:**
- **critical** — Security vulnerability, data loss risk, or runtime crash
- **warning** — Logic error, performance issue, or maintainability concern
- **info** — Minor improvement or best practice suggestion

## Review Summary

After completing the review, provide a summary:
```
Review Summary:
- Critical issues: N
- Warnings: N
- Info items: N
- Total issues: N
```

## Best Practices

- Review code with fresh eyes; take breaks if reviewing large files
- Focus on the most critical issues first (security, correctness, performance)
- Provide constructive feedback with specific suggestions
- Consider the context and constraints of the project
- Acknowledge good code and patterns alongside issues
- Ask clarifying questions if intent is unclear
