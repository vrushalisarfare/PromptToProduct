# Spec-Driven Development Workflow Guide

This guide walks you through the complete Spec-Driven Development workflow using the PromptToProduct framework.

## Overview

Spec-Driven Development follows these steps:
1. **Specify** - Write clear requirements
2. **Validate** - Ensure specs are complete
3. **Generate** - Create test scaffolding
4. **Implement** - Write code to pass tests
5. **Verify** - Run tests and validate
6. **Iterate** - Refine and improve

## Step-by-Step Workflow

### Step 1: Initialize Your Project

Start by creating a new project:

```bash
node src/cli.js init --name my-awesome-app
cd my-awesome-app
```

This creates:
- `specs/` - For your specifications
- `src/` - For your implementation code
- `tests/` - For your tests
- `README.md` - Project documentation

### Step 2: Write Your Specification

Edit `specs/specification.md` or create a YAML file. Choose the format that works best for you:

#### Option A: Markdown (Human-Readable)

```markdown
## Functional Requirements

1. **FR-001**: User can login with email and password
   - **Priority**: High
   - **Status**: Planned

## Test Cases

### Test Case 1
- **ID**: TC-001
- **Description**: Successful login
- **Expected Result**: User is authenticated
```

#### Option B: YAML (Machine-Readable)

```yaml
name: my-app
version: "1.0.0"
description: "My application"

requirements:
  functional:
    - id: FR-001
      description: "User can login"
      priority: high
      status: planned

test_cases:
  - id: TC-001
    description: "Successful login"
    expected_result: "User is authenticated"
```

### Step 3: Validate Your Specification

Before generating tests, validate your spec:

```bash
node src/cli.js validate specs/specification.md
```

Or for YAML:

```bash
node src/cli.js validate specs/specification.yaml
```

The validator checks:
- Required fields are present
- Requirement IDs are unique
- Test cases are well-formed
- No duplicate IDs
- Completeness of the spec

**Fix any errors before proceeding!**

### Step 4: Parse Your Specification (Optional)

To see how your spec is interpreted:

```bash
node src/cli.js parse specs/specification.yaml
```

This outputs the structured data that will be used for test generation.

### Step 5: Generate Test Scaffolding

Generate test files from your spec:

```bash
node src/cli.js generate specs/specification.yaml --output tests
```

This creates `tests/generated.test.js` with:
- Test suites for each requirement
- Test cases for user stories
- Placeholders for test implementation

**Review the generated tests** to ensure they match your expectations.

### Step 6: Implement Your Tests

Edit the generated tests to add actual test logic:

```javascript
// Before
test('FR-001: User can login', () => {
  // TODO: Implement test for FR-001
  expect(true).toBe(true);
});

// After
test('FR-001: User can login', () => {
  const user = { email: 'test@example.com', password: 'password' };
  const result = authService.login(user);
  expect(result.authenticated).toBe(true);
});
```

### Step 7: Run Tests (They Should Fail)

Run your test suite:

```bash
npm test
```

**Tests should fail** because you haven't implemented the code yet. This is expected!

### Step 8: Implement Your Code

Write code in `src/` to make the tests pass:

```javascript
// src/auth-service.js
class AuthService {
  login(user) {
    // Implementation here
    return { authenticated: true };
  }
}
```

### Step 9: Run Tests Again

```bash
npm test
```

Keep implementing until all tests pass!

### Step 10: Iterate

As requirements change:

1. Update your specification
2. Re-validate
3. Re-generate tests (or update manually)
4. Update implementation
5. Verify tests still pass

## Best Practices

### Writing Good Specifications

1. **Be Specific**: Avoid ambiguous requirements
   - ❌ "The app should be fast"
   - ✅ "Response time should be under 100ms"

2. **Use Unique IDs**: Assign IDs to all requirements
   - FR-XXX for functional requirements
   - NFR-XXX for non-functional requirements
   - TC-XXX for test cases

3. **Include Acceptance Criteria**: Define what "done" means
   ```yaml
   acceptance_criteria:
     - Login form is displayed
     - User can submit credentials
     - Error message shown for invalid login
   ```

4. **Prioritize**: Mark priority levels
   - High: Must have
   - Medium: Should have
   - Low: Nice to have

### Writing Good Tests

1. **Follow AAA Pattern**:
   - Arrange: Set up test data
   - Act: Execute the code
   - Assert: Verify the result

2. **One Assertion Per Test** (generally):
   ```javascript
   test('adds two numbers', () => {
     const result = calculator.add(2, 3);
     expect(result).toBe(5);
   });
   ```

3. **Use Descriptive Names**:
   - ❌ `test('test1', ...)`
   - ✅ `test('returns error when dividing by zero', ...)`

4. **Test Edge Cases**:
   - Empty inputs
   - Null/undefined values
   - Boundary conditions
   - Error scenarios

### Code Implementation

1. **Write Minimal Code**: Only write code to pass tests
2. **Refactor**: After tests pass, improve the code
3. **Keep Tests Green**: Don't break existing tests
4. **Document**: Add comments for complex logic

## Example Workflow in Action

Here's a real example from our calculator:

```bash
# 1. Validate spec
$ node src/cli.js validate specs/example-calculator.yaml
✓ Specification is valid

# 2. Generate tests
$ node src/cli.js generate specs/example-calculator.yaml --output tests
✓ Tests generated successfully: tests/generated.test.js

# 3. Run tests (will fail)
$ npm test
FAIL tests/generated.test.js
  ● FR-001: Perform basic arithmetic operations
    ReferenceError: calculator is not defined

# 4. Implement calculator
$ cat > src/calculator.js
class Calculator {
  add(a, b) { return a + b; }
  // ... more methods
}

# 5. Update tests to use calculator
$ vi tests/generated.test.js
# Add: const Calculator = require('../src/calculator');

# 6. Run tests (should pass)
$ npm test
PASS tests/generated.test.js
✓ All tests passed!
```

## Troubleshooting

### Validation Fails

**Problem**: Spec has errors

**Solution**: Read error messages and fix issues:
- Add missing required fields
- Remove duplicate IDs
- Fix YAML/Markdown syntax

### Tests Don't Generate

**Problem**: Parse error

**Solution**: 
- Check file format is correct
- Ensure file exists
- Try parsing first: `node src/cli.js parse spec-file`

### Tests Fail After Implementation

**Problem**: Code doesn't match requirements

**Solution**:
- Review the requirement
- Check test logic
- Verify implementation
- Consider if spec needs updating

### Too Many Tests Fail

**Problem**: Trying to do too much at once

**Solution**:
- Focus on one requirement at a time
- Comment out other tests
- Make incremental progress

## Tips

1. **Start Small**: Begin with a simple spec and grow it
2. **Iterate Quickly**: Write spec → validate → generate → implement
3. **Keep Specs Updated**: Treat specs as living documents
4. **Automate**: Use CI/CD to run validation and tests
5. **Collaborate**: Share specs with team for review

## Advanced Usage

### Custom Test Templates

You can extend the test generator to use custom templates:

```javascript
const generator = new TestGenerator();
const tests = generator.generate(spec);
// Customize tests here
```

### Integration with CI/CD

Add to your CI pipeline:

```yaml
# .github/workflows/ci.yml
- name: Validate Specs
  run: node src/cli.js validate specs/*.yaml

- name: Run Tests
  run: npm test
```

### Tracking Progress

Use the status command (coming soon):

```bash
node src/cli.js status
# Shows: Requirements complete: 5/10
#        Tests passing: 8/15
```

## Resources

- [Main Documentation](../docs/README.md)
- [Specification Template](../specs/TEMPLATE.md)
- [Example Project](../examples/calculator/)
- [API Reference](API.md) (if you create one)

## Next Steps

1. Try the calculator example: `examples/calculator/`
2. Create your own project
3. Share your specs with your team
4. Build something amazing!

Happy spec-driven developing! 🚀
