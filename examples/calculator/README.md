# Calculator Example

This example demonstrates the Spec-Driven Development workflow using a simple calculator application.

## Steps Followed

### 1. Specification
The specification is defined in `../../specs/example-calculator.yaml`. It includes:
- Functional requirements (arithmetic operations)
- Non-functional requirements (performance, error handling)
- User stories
- Test cases
- API definition

### 2. Validation
```bash
node ../../src/cli.js validate ../../specs/example-calculator.yaml
```

### 3. Test Generation
```bash
node ../../src/cli.js generate ../../specs/example-calculator.yaml --output tests
```

This generates test scaffolding in `tests/generated.test.js`.

### 4. Implementation
The calculator is implemented in `src/calculator.js` to pass all tests.

### 5. Verification
```bash
npm test
```

## Project Structure

```
calculator/
├── src/
│   └── calculator.js      # Implementation
├── tests/
│   ├── generated.test.js  # Auto-generated tests
│   └── calculator.test.js # Additional tests
└── README.md
```

## Running This Example

From the root of the PromptToProduct project:

```bash
# Generate tests
node src/cli.js generate specs/example-calculator.yaml --output examples/calculator/tests

# View the generated tests
cat examples/calculator/tests/generated.test.js
```

## Key Takeaways

1. **Specification First**: We defined requirements before writing any code
2. **Test Generation**: Tests were automatically generated from the spec
3. **Implementation Driven by Tests**: Code was written to satisfy the test cases
4. **Traceability**: Each piece of code traces back to a requirement

This is the core of Spec-Driven Development!
