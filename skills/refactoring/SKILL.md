---
name: refactoring
description: |
  Trigger phrases: "refactor", "restructure", "clean up code", "reduce complexity", "code smells", "improve structure".
  Guides safe, behavior-preserving code refactoring using incremental steps and LSP tools.
license: MIT
metadata:
  version: "1.0"
  author: ai-agent-utilities
---

# Refactoring

Safe code refactoring is about improving structure and readability while preserving behavior. This skill provides a systematic 6-step process to refactor code safely, using language server tools when available.

## 6-Step Refactoring Process

### 1. Identify Scope

Before touching any code, clearly define what you're refactoring and what you're leaving alone.

- **What to refactor**: Specify the exact functions, classes, modules, or files in scope
- **What to leave alone**: Identify dependencies and public APIs that must remain unchanged
- **Risk assessment**: Evaluate test coverage, complexity, and potential impact
- **Success criteria**: Define what "better" looks like (readability, performance, maintainability)

### 2. Assess Test Coverage

You cannot safely refactor without knowing if behavior is preserved. Check test coverage first.

- **Run existing tests**: Ensure all tests pass before making changes
- **Identify coverage gaps**: Use code coverage tools to find untested code paths
- **Add tests if needed**: If coverage is low (< 80%), add tests BEFORE refactoring
- **Document expected behavior**: Write tests that capture current behavior as the baseline

### 3. Identify Code Smells

Recognize patterns that indicate refactoring opportunities:

- **Long methods**: Functions > 20 lines often hide multiple responsibilities
- **Large classes**: Classes with many methods or fields often violate single responsibility
- **Feature envy**: Code that accesses another object's internals more than its own
- **Shotgun surgery**: Changes that require edits in many places (sign of poor cohesion)
- **Duplicate code**: Copy-pasted logic that should be extracted
- **Magic numbers/strings**: Unexplained constants that should be named
- **Deep nesting**: Conditional logic that's hard to follow

### 4. Plan Changes

Break refactoring into smallest safe steps. Never mix behavior changes with structural changes.

- **One refactoring at a time**: Extract method, then rename, then move. Not all at once.
- **Prioritize by risk**: Start with low-risk refactorings (rename, extract) before high-risk ones (restructure)
- **Use LSP tools**: Leverage language server tools for safe transformations:
  - `lsp_find_references`: Find all usages of a symbol before renaming
  - `lsp_rename`: Safely rename symbols across the entire codebase
  - `lsp_goto_definition`: Understand dependencies before moving code
- **Plan commits**: Each refactoring step should be a separate, atomic commit
- **Document rationale**: Note why each change improves the code

### 5. Execute

Apply refactorings incrementally, testing after each step.

- **Make one change**: Apply a single refactoring (e.g., extract method)
- **Run tests**: Execute the full test suite to verify behavior is unchanged
- **Commit atomically**: Create a commit with just this refactoring
- **Repeat**: Move to the next refactoring step
- **Avoid mixing concerns**: Never refactor AND add features in the same commit

### 6. Verify

Ensure the refactored code is correct and maintains the original behavior.

- **Run full test suite**: Execute all tests, not just affected ones
- **Check public API**: Verify that public interfaces are unchanged (unless intentional)
- **Code review**: Have another developer review the refactoring for clarity
- **Performance check**: If refactoring touched performance-critical code, benchmark before/after
- **Documentation**: Update comments and docstrings to reflect new structure

## Key Principles

### Never Change Behavior and Structure in the Same Commit

Mixing refactoring with feature changes makes it impossible to isolate bugs. Keep them separate:

- **Refactoring PR**: Only structural changes, no behavior changes, all tests pass
- **Feature PR**: Only new behavior, minimal refactoring, clear intent

### Use LSP Tools for Safe Transformations

When available, language server tools are safer than manual edits:

- **lsp_find_references**: Before renaming, find all usages to understand impact
- **lsp_rename**: Rename symbols across the entire codebase consistently
- **lsp_goto_definition**: Navigate to understand code structure before moving

### Each Step Must Be Independently Reversible

If a refactoring step breaks something, you should be able to revert just that step:

- Atomic commits enable easy rollback
- Small changes are easier to debug
- Tests catch problems immediately

### Keep Refactoring PRs Separate from Feature PRs

Mixing refactoring with features makes code review harder and debugging slower:

- Refactoring PRs should have zero behavior changes
- Feature PRs should have minimal refactoring
- This separation makes git blame and bisect more useful

## Common Refactorings

### Extract Method

When a method does multiple things, extract a helper method:

1. Identify the code to extract
2. Create a new method with a clear name
3. Move the code into the new method
4. Replace the original code with a call to the new method
5. Run tests
6. Commit

### Rename Symbol

When a name is unclear, rename it consistently:

1. Use `lsp_find_references` to find all usages
2. Use `lsp_rename` to rename across the codebase
3. Run tests
4. Commit

### Move Code

When code belongs in a different module:

1. Identify the code to move
2. Check for dependencies using `lsp_find_references`
3. Move the code to the new location
4. Update imports
5. Run tests
6. Commit

### Simplify Conditionals

When conditionals are complex, simplify them:

1. Extract conditions into named variables
2. Use guard clauses to reduce nesting
3. Replace complex logic with helper methods
4. Run tests after each step
5. Commit

## When NOT to Refactor

- **During a crisis**: Focus on fixing the bug, refactor later
- **Without tests**: Add tests first, then refactor
- **Before a release**: Refactor in the next sprint
- **In unfamiliar code**: Understand it first, then refactor
- **Without a clear goal**: "Make it better" is not a goal

## Tools and Resources

- **Language Server Protocol (LSP)**: Use `lsp_find_references`, `lsp_rename`, `lsp_goto_definition`
- **Code coverage tools**: Identify untested code before refactoring
- **Linters**: Identify code smells automatically
- **Version control**: Use git to track refactoring commits
- **Tests**: The safety net for all refactoring

## Summary

Safe refactoring follows a clear process: identify scope, assess coverage, identify smells, plan changes, execute incrementally, and verify thoroughly. Use LSP tools when available, keep refactoring separate from features, and always run tests after each step. This approach ensures that code improves without introducing bugs.
