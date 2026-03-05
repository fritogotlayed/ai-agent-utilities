---
name: security-audit
description: |
  Performs OWASP-aware security analysis and vulnerability assessment.
  
  Trigger phrases: "security audit", "check for vulnerabilities", "security review", "OWASP", "find security issues", "vulnerability scan", "security assessment", "penetration test", "threat analysis".
  
  Analyzes code and configurations for injection attacks, authentication/authorization flaws, secrets exposure, dependency vulnerabilities, data exposure risks, and insecure configurations. Returns severity-ranked findings (critical/high/medium/low) with CWE references.
metadata:
  version: "1.0"
  author: ai-agent-utilities
---

# Security Audit Skill

Comprehensive OWASP-aware security review and vulnerability assessment for applications and infrastructure.

## Overview

This skill performs systematic security analysis across the OWASP Top 10 and related vulnerability categories. It identifies and ranks security issues by severity, providing actionable remediation guidance with CWE/CVE references.

## Coverage Areas

### 1. Injection Vulnerabilities (CWE-89, CWE-79, CWE-94)

**SQL Injection**
- Detects unsanitized user input in database queries
- Identifies missing parameterized queries/prepared statements
- Flags string concatenation in SQL construction
- Checks for ORM misuse (raw queries, unsafe methods)

**Command Injection**
- Identifies shell command execution with user input
- Detects unsafe functions: `exec()`, `system()`, `shell=True`, backticks
- Flags missing input validation before OS commands
- Checks for command chaining vulnerabilities

**Cross-Site Scripting (XSS)**
- Detects unescaped user input in HTML/JavaScript context
- Identifies missing Content Security Policy (CSP) headers
- Flags DOM-based XSS vulnerabilities
- Checks for unsafe template rendering

**Template Injection**
- Identifies unsafe template rendering with user input
- Detects SSTI (Server-Side Template Injection) patterns
- Flags template auto-escaping disabled
- Checks for expression language injection

### 2. Authentication & Authorization (CWE-287, CWE-639, CWE-613)

**Missing Authentication**
- Identifies unprotected endpoints requiring authentication
- Detects missing login checks on sensitive operations
- Flags public access to admin/privileged functions
- Checks for authentication bypass vulnerabilities

**Broken Authorization**
- Detects privilege escalation opportunities
- Identifies missing authorization checks on resources
- Flags horizontal privilege escalation (user A accessing user B's data)
- Checks for vertical privilege escalation (user accessing admin functions)

**Insecure Session Management**
- Identifies weak session token generation
- Detects missing session timeout
- Flags session fixation vulnerabilities
- Checks for insecure session storage (localStorage, cookies without HttpOnly)
- Identifies missing CSRF protection

**Weak Authentication Mechanisms**
- Detects hardcoded credentials
- Identifies weak password policies
- Flags missing multi-factor authentication (MFA)
- Checks for insecure password reset flows

### 3. Secrets Management (CWE-798, CWE-321)

**Hardcoded Secrets**
- Detects API keys, tokens, passwords in source code
- Identifies database credentials in configuration files
- Flags private keys, certificates in repositories
- Checks for OAuth tokens, JWT secrets in code

**Environment Variable Exposure**
- Identifies .env files committed to version control
- Detects environment variables logged or exposed in error messages
- Flags secrets in Docker images or build artifacts
- Checks for secrets in CI/CD pipeline logs

**Insecure Secret Storage**
- Detects plaintext secret storage
- Identifies missing encryption for sensitive data
- Flags secrets in version control history
- Checks for secrets in backup files

### 4. Dependency Security (CWE-1035, CWE-1104)

**Known Vulnerabilities (CVEs)**
- Identifies outdated packages with known CVEs
- Detects vulnerable dependency versions
- Flags unmaintained or abandoned dependencies
- Checks for transitive dependency vulnerabilities

**Supply Chain Risks**
- Detects typosquatting/package confusion attacks
- Identifies suspicious package sources
- Flags packages with unusual permissions
- Checks for compromised package versions

**Dependency Management**
- Identifies missing dependency pinning
- Detects overly permissive version constraints
- Flags missing lock files (package-lock.json, Pipfile.lock, etc.)
- Checks for unvetted third-party dependencies

### 5. Data Exposure (CWE-200, CWE-532)

**Verbose Error Messages**
- Detects stack traces exposed to users
- Identifies database error details in responses
- Flags sensitive information in error logs
- Checks for debug mode enabled in production

**PII in Logs**
- Identifies personally identifiable information (PII) in logs
- Detects credit card numbers, SSNs, email addresses logged
- Flags authentication tokens in logs
- Checks for sensitive data in debug output

**Insecure Data Transmission**
- Detects unencrypted HTTP for sensitive data
- Identifies missing HTTPS enforcement
- Flags mixed content (HTTP + HTTPS)
- Checks for insecure TLS/SSL configurations

**Insecure Data Storage**
- Identifies plaintext storage of sensitive data
- Detects missing encryption at rest
- Flags weak encryption algorithms
- Checks for missing data masking/tokenization

### 6. Configuration Issues (CWE-16, CWE-693)

**CORS Misconfiguration**
- Detects overly permissive CORS policies (`Access-Control-Allow-Origin: *`)
- Identifies missing CORS headers
- Flags wildcard origins with credentials
- Checks for CORS bypass vulnerabilities

**Security Headers**
- Identifies missing security headers:
  - `Strict-Transport-Security` (HSTS)
  - `X-Content-Type-Options`
  - `X-Frame-Options`
  - `Content-Security-Policy` (CSP)
  - `X-XSS-Protection`
  - `Referrer-Policy`
- Flags weak header configurations

**Cookie Security**
- Detects missing `HttpOnly` flag
- Identifies missing `Secure` flag on HTTPS
- Flags missing `SameSite` attribute
- Checks for overly broad cookie scope

**HTTPS & TLS**
- Identifies unencrypted HTTP endpoints
- Detects weak TLS versions (< 1.2)
- Flags weak cipher suites
- Checks for certificate validation issues

**Default Credentials**
- Detects unchanged default passwords
- Identifies default admin accounts
- Flags default API keys/tokens
- Checks for default service configurations

## Output Format

Security findings are ranked by severity:

- **CRITICAL**: Immediate exploitation risk, data breach potential, system compromise
- **HIGH**: Significant security impact, likely exploitation path
- **MEDIUM**: Moderate risk, requires specific conditions or user interaction
- **LOW**: Minor security concern, defense-in-depth issue

Each finding includes:
- Severity level
- CWE/CVE reference (if applicable)
- Affected component/file
- Vulnerability description
- Exploitation scenario
- Remediation steps
- Compliance impact (OWASP, PCI-DSS, HIPAA, etc.)

## Methodology

1. **Code Review**: Static analysis of source code for vulnerable patterns
2. **Configuration Audit**: Review of application and infrastructure settings
3. **Dependency Analysis**: Scan for known vulnerabilities in third-party libraries
4. **Data Flow Analysis**: Trace sensitive data handling and exposure risks
5. **Authentication/Authorization Review**: Verify access control mechanisms
6. **Secrets Scanning**: Detect hardcoded credentials and sensitive information
7. **Compliance Check**: Verify alignment with security standards

## Limitations

- Requires access to source code and configuration files
- Cannot detect runtime-only vulnerabilities without execution
- Depends on accurate code context and configuration details
- May produce false positives in complex or unusual code patterns
- Does not replace professional penetration testing

## Related Skills

- Code Review: General code quality and best practices
- Dependency Audit: Detailed package vulnerability analysis
- Infrastructure Security: Cloud and infrastructure-specific security
- Compliance Review: Regulatory and compliance requirements
