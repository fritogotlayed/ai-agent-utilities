---
name: security
description: |
  Trigger phrases: "/security", "check security", "security scan", "is this secure", "security check".
  Action skill: performs security analysis on specified target (files, project, or staged changes).
  Identifies vulnerabilities, hardcoded secrets, injection risks, and unsafe patterns.
license: MIT
compatibility: all
metadata:
  version: "1.0"
  author: ai-agent-utilities
allowed-tools:
  - bash
  - grep
  - read
---

# Security Action

## Overview
This skill performs on-demand security scanning and vulnerability analysis. It identifies common security risks including hardcoded secrets, SQL injection patterns, unsafe code execution, and insecure DOM manipulation.

## Trigger Phrases
- `/security`
- `check security`
- `security scan`
- `is this secure`
- `security check`

## Action Steps

### 1. Determine Target
Identify what to scan:
- **Specific file(s)**: User provides explicit path(s)
- **Entire project**: Scan all source files in current directory
- **Staged changes**: Analyze only modified/staged files (if in git repo)

### 2. Load Security Audit Methodology
Reference the `security-audit` skill for comprehensive audit methodology and detailed vulnerability classification.

### 3. Run Automated Pattern Checks

#### Hardcoded Secrets Detection
Search for common secret patterns:
- API keys: `API_KEY`, `api_key`, `APIKEY`
- Passwords: `PASSWORD`, `password`, `passwd`
- Tokens: `TOKEN`, `token`, `SECRET`, `secret`
- AWS credentials: `AKIA`, `aws_secret_access_key`
- Private keys: `PRIVATE_KEY`, `private_key`, `-----BEGIN`

#### SQL Injection Risks
Identify string concatenation with user input in SQL queries:
- Pattern: `query = "SELECT ... " + user_input`
- Pattern: `f"SELECT ... {variable}"`
- Pattern: `query.format(user_input)`
- Missing parameterized queries

#### Code Execution Risks
Find unsafe code execution patterns:
- `eval()` on user-controlled input
- `exec()` on user-controlled input
- `subprocess.call()` with shell=True and user input
- `os.system()` with user input

#### Unsafe DOM Manipulation (JavaScript/React)
Identify insecure DOM operations:
- `innerHTML` assignment without sanitization
- `dangerouslySetInnerHTML` in React without sanitization
- `document.write()` with user input
- Missing Content Security Policy headers

### 4. Severity Classification

**CRITICAL**
- Hardcoded credentials in source code
- SQL injection vulnerabilities
- Remote code execution via eval/exec
- Unvalidated user input in system commands

**HIGH**
- Weak cryptography usage
- Missing authentication/authorization checks
- Insecure deserialization
- Unsafe DOM manipulation

**MEDIUM**
- Missing input validation
- Insufficient logging of security events
- Weak password policies
- Missing HTTPS enforcement

**LOW**
- Deprecated security libraries
- Missing security headers
- Verbose error messages
- Outdated dependencies

**CLEAN**
- No security issues detected
- All checks passed

### 5. Generate Report

Output format:
```
SECURITY SCAN REPORT
====================
Target: [file/directory/staged changes]
Scan Date: [timestamp]

OVERALL RISK LEVEL: [CRITICAL|HIGH|MEDIUM|LOW|CLEAN]

FINDINGS BY SEVERITY
====================

[CRITICAL] (count)
- [Finding 1]: [File:Line] - [Description]
- [Finding 2]: [File:Line] - [Description]

[HIGH] (count)
- [Finding 1]: [File:Line] - [Description]

[MEDIUM] (count)
- [Finding 1]: [File:Line] - [Description]

[LOW] (count)
- [Finding 1]: [File:Line] - [Description]

EXECUTIVE SUMMARY
=================
[1-2 sentence summary of overall security posture]

TOP RECOMMENDATIONS
===================
1. [Priority 1 action]
2. [Priority 2 action]
3. [Priority 3 action]

SCAN STATISTICS
===============
Files Scanned: [count]
Total Findings: [count]
Scan Duration: [time]
```

## Implementation Notes

- Use grep with regex patterns for efficient scanning
- Support multiple file types: Python, JavaScript, TypeScript, Java, C#, Go, Rust
- Exclude common non-source directories: node_modules, .git, venv, __pycache__, dist, build
- Provide file:line references for all findings
- Rank findings by severity for actionable prioritization
- Include context snippets (2-3 lines) for each finding

## Related Skills
- `security-audit`: Comprehensive security audit methodology and detailed vulnerability analysis
