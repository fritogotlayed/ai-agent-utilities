---
name: test
description: |
  Trigger phrases: "/test", "write tests", "add tests", "test this", "improve test coverage", "write unit tests".
  Action skill: writes tests for specified code, following the project's existing test patterns and conventions.
metadata:
  version: "1.0"
  author: ai-agent-utilities
---

# Test Action

An action skill that writes comprehensive tests for specified code, following the project's existing test patterns and conventions. Covers happy paths, edge cases, error conditions, and boundary values.

## Test Writing Methodology

### 1. Detect Test Framework

Identify the project's test framework by examining configuration files:

- **Python**: Look for `pytest.ini`, `pyproject.toml` with `[tool.pytest]`, or `setup.cfg` with `[tool:pytest]`
  - Default: pytest
  - Check for pytest plugins: pytest-cov, pytest-mock, pytest-asyncio
- **JavaScript/TypeScript**: Look for `package.json` with test scripts
  - Jest: `jest.config.js`, `jest.config.json`, or `"jest"` in package.json
  - Vitest: `vitest.config.ts`, `vitest.config.js`
  - Mocha: `mocha.opts`, `.mocharc.json`
- **Go**: Look for `go.mod` and `*_test.go` files
  - Default: go test (built-in)
- **Rust**: Look for `Cargo.toml`
  - Default: cargo test
- **Java**: Look for `pom.xml` (Maven) or `build.gradle` (Gradle)
  - Maven: JUnit, TestNG
  - Gradle: JUnit, TestNG

If no tests exist, suggest an appropriate framework based on the project language and recommend scaffolding a test structure.

### 2. Analyze Target Code

Understand the code to be tested:

- **Identify public API**: Functions, methods, classes, exported symbols
- **Understand inputs and outputs**: Parameter types, return types, side effects
- **Identify edge cases**: Null/undefined values, empty collections, zero values, negative numbers, boundary conditions
- **Identify error paths**: Exceptions, error codes, validation failures, resource exhaustion
- **Understand dependencies**: External services, databases, file systems, network calls
- **Review existing tests**: Study naming conventions, assertion patterns, test structure, mocking strategies

### 3. Write Tests Following Project Conventions

Create tests that match the project's existing patterns:

- **Test naming**: Follow project convention (e.g., `test_function_name`, `testFunctionName`, `function_name_test`)
- **Test structure**: Match existing test file organization and directory structure
- **Assertion style**: Use the same assertion library and patterns as existing tests
- **Mocking/stubbing**: Follow project's mocking patterns (unittest.mock, jest.mock, sinon, etc.)
- **Setup/teardown**: Use project's fixture/setup patterns (pytest fixtures, beforeEach/afterEach, setUp/tearDown)
- **Test organization**: Group related tests in classes or describe blocks as the project does

### 4. Cover Test Cases

Write tests for comprehensive coverage:

- **Happy path**: Normal operation with valid inputs, expected outputs
- **Edge cases**: Boundary values, empty inputs, maximum/minimum values, special characters
- **Error conditions**: Invalid inputs, missing required parameters, type mismatches, exceptions
- **State transitions**: Before/after state, side effects, state mutations
- **Concurrency**: Race conditions, async operations, parallel execution (if applicable)
- **Resource handling**: File cleanup, connection closure, memory leaks (if applicable)

### 5. Run Tests

Execute the test suite to verify tests pass:

- **Python**: `PYENV_VERSION=3.13.7 python3 -m pytest tests/ -v`
- **JavaScript**: `npm test` or `yarn test`
- **Go**: `go test ./...`
- **Rust**: `cargo test`
- **Java**: `mvn test` or `gradle test`

Verify:
- All tests pass
- No import errors or syntax errors
- Coverage is reasonable (aim for >80% for critical code)

### 6. Report Results

Provide a summary of test work:

```
Tests Written:
- [test_name]: [description]
- [test_name]: [description]

Coverage:
- Lines: X%
- Functions: X%
- Branches: X%

Status: ✓ All tests passing
```

## Test Quality Checklist

- [ ] Tests are independent and can run in any order
- [ ] Tests use descriptive names that explain what is being tested
- [ ] Tests follow the Arrange-Act-Assert pattern
- [ ] Tests verify behavior, not implementation details
- [ ] Tests use appropriate assertions for the expected outcome
- [ ] Tests handle async operations correctly (promises, callbacks, async/await)
- [ ] Tests clean up resources (files, connections, mocks)
- [ ] Tests are fast and don't have unnecessary delays
- [ ] Tests are deterministic and don't depend on external state
- [ ] Tests document expected behavior through examples

## Common Testing Patterns

### Python (pytest)

```python
def test_function_happy_path():
    """Test normal operation with valid inputs."""
    result = function(valid_input)
    assert result == expected_output

def test_function_edge_case():
    """Test boundary condition."""
    result = function(boundary_value)
    assert result == expected_output

def test_function_error_condition():
    """Test error handling."""
    with pytest.raises(ValueError):
        function(invalid_input)
```

### JavaScript (Jest)

```javascript
describe('function', () => {
  test('happy path', () => {
    const result = function(validInput);
    expect(result).toBe(expectedOutput);
  });

  test('edge case', () => {
    const result = function(boundaryValue);
    expect(result).toBe(expectedOutput);
  });

  test('error condition', () => {
    expect(() => function(invalidInput)).toThrow(Error);
  });
});
```

### Go

```go
func TestFunctionHappyPath(t *testing.T) {
    result := function(validInput)
    if result != expectedOutput {
        t.Errorf("expected %v, got %v", expectedOutput, result)
    }
}

func TestFunctionErrorCondition(t *testing.T) {
    _, err := function(invalidInput)
    if err == nil {
        t.Error("expected error, got nil")
    }
}
```

## Best Practices

- **Test one thing per test**: Each test should verify a single behavior
- **Use descriptive names**: Test names should explain what is being tested and the expected outcome
- **Avoid test interdependencies**: Tests should not depend on the order of execution or state from other tests
- **Mock external dependencies**: Use mocks for external services, databases, and file systems
- **Test behavior, not implementation**: Focus on what the code does, not how it does it
- **Keep tests simple**: Complex test logic is harder to maintain and debug
- **Use fixtures and factories**: Create reusable test data and objects
- **Test error paths**: Don't just test the happy path; test error conditions and edge cases
- **Maintain test code quality**: Refactor tests as you would production code
- **Run tests frequently**: Run tests during development, not just before commit
