# Prompt to Product - Spec-Driven Development Framework

A comprehensive framework for Spec-Driven Development (SDD) that helps transform product specifications into working code through a structured, test-first approach.

## What is Spec-Driven Development?

Spec-Driven Development (SDD) is a software development methodology that follows this workflow:

1. **Write Specifications**: Start with clear, detailed product specifications
2. **Generate Tests**: Create test cases based on the specifications
3. **Implement Code**: Write code to pass the tests
4. **Verify**: Ensure all requirements are met

This approach ensures that development stays aligned with requirements and that all features are properly tested.

## Features

- 📝 Structured specification templates (Markdown and YAML)
- ✅ Specification validation
- 🧪 Automatic test generation from specs
- 🎯 Requirement tracking
- 🚀 CLI tool for easy workflow management

## Installation

```bash
npm install
```

Make the CLI executable:
```bash
chmod +x src/cli.js
```

Or install globally:
```bash
npm install -g .
```

## Quick Start

### 1. Initialize a New Project

```bash
node src/cli.js init --name my-awesome-project
cd my-awesome-project
```

This creates a new project with the following structure:
```
my-awesome-project/
├── specs/
│   └── specification.md
├── src/
├── tests/
└── README.md
```

### 2. Write Your Specification

Edit `specs/specification.md` or create a YAML spec. See the `specs/` directory for examples.

**Markdown Example:**
```markdown
## Functional Requirements
1. **FR-001**: User can login with email and password
   - **Priority**: High
   - **Status**: Planned
```

**YAML Example:**
```yaml
name: my-app
description: "My awesome application"
requirements:
  functional:
    - id: FR-001
      description: "User can login"
      priority: high
```

### 3. Validate Your Specification

```bash
node src/cli.js validate specs/specification.md
```

This checks:
- Required fields are present
- Requirement IDs are unique
- Test cases are well-formed
- Specification completeness

### 4. Generate Tests

```bash
node src/cli.js generate specs/specification.md --output tests
```

This creates test scaffolding based on your specification:
- Tests for each functional requirement
- Tests for each user story
- Tests for each test case

### 5. Implement Your Code

Write code in the `src/` directory to make the tests pass. Follow TDD principles:
- Run tests frequently
- Write minimal code to pass tests
- Refactor as needed

### 6. Verify

Run your tests to ensure all requirements are met:
```bash
npm test
```

## CLI Commands

### `init`
Initialize a new spec-driven project.

```bash
node src/cli.js init --name <project-name>
```

### `validate`
Validate a specification file.

```bash
node src/cli.js validate [spec-file]
```

Options:
- `spec-file`: Path to specification file (default: `specs/specification.md`)

### `parse`
Parse and display specification in structured format.

```bash
node src/cli.js parse <spec-file>
```

### `generate`
Generate test scaffolding from specification.

```bash
node src/cli.js generate <spec-file> [options]
```

Options:
- `-o, --output <dir>`: Output directory for tests (default: `tests`)

### `status`
Show development progress vs specifications.

```bash
node src/cli.js status
```

## Specification Formats

### Markdown Format

Use the provided template at `specs/TEMPLATE.md`. Key sections:

- **Overview**: Project description
- **Requirements**: Functional and non-functional requirements
- **User Stories**: User-centric feature descriptions
- **Test Cases**: Detailed test scenarios
- **Technical Specifications**: Architecture and design details

### YAML Format

More structured format, ideal for automation. See `specs/example-calculator.yaml` for a complete example.

```yaml
name: project-name
version: "1.0.0"
description: "Project description"

requirements:
  functional:
    - id: FR-001
      description: "Requirement description"
      priority: high
      status: planned

test_cases:
  - id: TC-001
    description: "Test description"
    steps:
      - "Step 1"
      - "Step 2"
    expected_result: "Expected outcome"
```

## Example: Calculator Project

An example calculator project specification is included in `specs/example-calculator.yaml`.

To see it in action:

```bash
# Validate the spec
node src/cli.js validate specs/example-calculator.yaml

# Parse the spec
node src/cli.js parse specs/example-calculator.yaml

# Generate tests
node src/cli.js generate specs/example-calculator.yaml --output examples/tests
```

## Best Practices

### Writing Specifications

1. **Be Specific**: Clear, unambiguous requirements
2. **Use IDs**: Assign unique IDs to all requirements and test cases
3. **Prioritize**: Mark requirements as high/medium/low priority
4. **Measurable**: Include acceptance criteria for each requirement
5. **Testable**: Ensure each requirement can be tested

### Requirement IDs

Use consistent naming:
- `FR-XXX`: Functional Requirements
- `NFR-XXX`: Non-Functional Requirements
- `US-XXX`: User Stories
- `TC-XXX`: Test Cases

### Test Cases

Include:
- Clear description
- Preconditions
- Step-by-step instructions
- Expected results

### User Stories

Follow the format:
> As a [user type], I want [goal] so that [benefit]

Include acceptance criteria as checkboxes.

## Workflow Example

Here's a complete workflow example:

```bash
# 1. Create project
node src/cli.js init --name todo-app
cd todo-app

# 2. Write specification
# Edit specs/specification.md with your requirements

# 3. Validate
node src/cli.js validate specs/specification.md

# 4. Generate tests
node src/cli.js generate specs/specification.md

# 5. Run tests (they will fail initially)
npm test

# 6. Implement features
# Write code in src/ to pass tests

# 7. Run tests again
npm test

# 8. Repeat steps 6-7 until all tests pass
```

## Project Structure

```
PromptToProduct/
├── src/                    # Framework source code
│   ├── cli.js             # CLI interface
│   ├── spec-parser.js     # Specification parser
│   ├── spec-validator.js  # Specification validator
│   ├── test-generator.js  # Test generator
│   └── index.js           # Main exports
├── specs/                 # Specification templates and examples
│   ├── TEMPLATE.md        # Markdown template
│   └── example-calculator.yaml  # Example spec
├── examples/              # Example projects
├── tests/                 # Framework tests
├── docs/                  # Additional documentation
├── package.json           # NPM configuration
└── README.md             # This file
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Write clear specifications for new features
2. Generate and implement tests
3. Ensure all tests pass
4. Update documentation

## Benefits of Spec-Driven Development

1. **Clear Requirements**: Specifications provide a single source of truth
2. **Better Planning**: Think through requirements before coding
3. **Automated Testing**: Generate tests directly from specs
4. **Traceability**: Link code back to requirements
5. **Documentation**: Specs serve as living documentation
6. **Quality Assurance**: Test-first approach catches issues early
7. **Team Alignment**: Everyone understands what's being built

## License

MIT

## Support

For issues, questions, or contributions, please visit the GitHub repository.
