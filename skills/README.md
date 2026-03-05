# Installed Skills

This directory contains AI agent skills from [ai-agent-utilities](https://github.com/your-org/ai-agent-utilities). Each subdirectory holds a `SKILL.md` file following the [Agent Skills](https://agentskills.io) standard.

## Two Types of Skills

**Knowledge skills** load as background context. They provide methodology, frameworks, and criteria that shape how the agent thinks — but they don't execute anything on their own.

**Action skills** are invoked directly via `/command` or trigger phrase. They follow step-by-step procedures to produce a result. Most action skills reference a knowledge skill for their underlying methodology.

## Skill Pairs

Four knowledge skills are paired with a corresponding action skill:

| Knowledge (methodology) | Action (execution) | What they do |
|---|---|---|
| `code-review` | `review` | Code review — methodology + reviewer |
| `documentation` | `docs` | Documentation — style guide + generator |
| `security-audit` | `security` | Security — OWASP framework + scanner |
| `skill-builder` | `new-skill` | Skill creation — spec reference + scaffolder |

**How pairing works:** When you invoke `/review`, the action skill loads the `code-review` knowledge skill's methodology, then applies it to your target (staged changes, files, PR). The knowledge skill provides the *what to check*, the action skill provides the *how to do it*.

## Standalone Skills

| Skill | Type | What it does |
|---|---|---|
| `refactoring` | Knowledge | Safe, behavior-preserving refactoring methodology |
| `test` | Action | Writes tests following project conventions |

## Quick Reference

| Trigger | Skill | Type |
|---|---|---|
| `/review`, "review my code" | review | Action |
| `/docs`, "generate docs" | docs | Action |
| `/security`, "security scan" | security | Action |
| `/new-skill`, "create a skill" | new-skill | Action |
| `/test`, "write tests" | test | Action |
| "refactor", "clean up code" | refactoring | Knowledge |
