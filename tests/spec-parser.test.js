const { SpecParser } = require('../src/spec-parser');

describe('SpecParser', () => {
  let parser;
  
  beforeEach(() => {
    parser = new SpecParser();
  });
  
  describe('YAML parsing', () => {
    test('parses valid YAML spec', () => {
      const content = `
name: calculator
version: "1.0.0"
description: "Calculator app"
requirements:
  functional:
    - id: FR-001
      description: "Add numbers"
      priority: high
`;
      
      const spec = parser.parse(content, 'test.yaml');
      
      expect(spec.name).toBe('calculator');
      expect(spec.version).toBe('1.0.0');
      expect(spec.requirements.functional).toHaveLength(1);
      expect(spec.requirements.functional[0].id).toBe('FR-001');
    });
    
    test('throws error on invalid YAML', () => {
      const content = `
name: test
  invalid: yaml: structure
`;
      
      expect(() => {
        parser.parse(content, 'test.yaml');
      }).toThrow();
    });
  });
  
  describe('Markdown parsing', () => {
    test('parses markdown spec', () => {
      const content = `
## Functional Requirements
1. **FR-001**: Add two numbers
   - **Priority**: High
   - **Status**: Planned

## Test Cases
### Test Case 1
- **ID**: TC-001
- **Description**: Test addition
- **Expected Result**: Sum is correct
`;
      
      const spec = parser.parse(content, 'test.md');
      
      expect(spec.requirements.functional).toHaveLength(1);
      expect(spec.requirements.functional[0].id).toBe('FR-001');
      expect(spec.requirements.functional[0].priority).toBe('high');
      expect(spec.test_cases).toHaveLength(1);
      expect(spec.test_cases[0].id).toBe('TC-001');
    });
  });
  
  describe('unsupported formats', () => {
    test('throws error for unsupported format', () => {
      expect(() => {
        parser.parse('content', 'test.txt');
      }).toThrow('Unsupported file format');
    });
  });
});
