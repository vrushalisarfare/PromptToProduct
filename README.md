# PromptToProduct

A comprehensive Spec-Driven Development (SDD) framework that helps transform product specifications into working code through a structured, test-first approach.

## What is This?

PromptToProduct is a framework for **Spec-Driven Development** - a methodology where you:
1. Write clear product specifications
2. Generate tests from those specs
3. Implement code to pass the tests
4. Verify all requirements are met

This ensures development stays aligned with requirements and all features are properly tested.

## Quick Start

```bash
# Install dependencies
npm install

# Initialize a new project
node src/cli.js init --name my-project

# See available commands
node src/cli.js --help
```

## Key Features

- 📝 **Structured Specifications**: Use Markdown or YAML templates
- ✅ **Validation**: Ensure specs are complete and well-formed
- 🧪 **Test Generation**: Auto-generate test scaffolding from specs
- 🎯 **Requirement Tracking**: Link code to requirements
- 🚀 **CLI Tool**: Easy-to-use command-line interface

## Example Workflow

```bash
# 1. Initialize project
node src/cli.js init --name calculator-app

# 2. Write specifications in specs/specification.md

# 3. Validate your specification
node src/cli.js validate specs/specification.md

# 4. Generate tests
node src/cli.js generate specs/specification.md

# 5. Implement code to pass tests

# 6. Run tests
npm test
```

## Example Included

Check out `specs/example-calculator.yaml` for a complete example specification:

```bash
# Validate the example
node src/cli.js validate specs/example-calculator.yaml

# Generate tests from the example
node src/cli.js generate specs/example-calculator.yaml --output examples/tests
```

## Documentation

For detailed documentation, see:
- [Complete Documentation](docs/README.md)
- [Specification Template](specs/TEMPLATE.md)
- [Example Calculator Spec](specs/example-calculator.yaml)

## CLI Commands

- `init` - Initialize a new spec-driven project
- `validate` - Validate a specification file
- `parse` - Parse and display specification structure
- `generate` - Generate test scaffolding from spec
- `status` - Show development progress

## Why Spec-Driven Development?

1. **Clear Requirements** - Single source of truth
2. **Better Planning** - Think before coding
3. **Automated Testing** - Tests from specs
4. **Traceability** - Link code to requirements
5. **Quality Assurance** - Test-first approach
6. **Documentation** - Specs as living docs

## License

MIT
