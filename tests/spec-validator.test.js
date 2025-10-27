const { SpecValidator } = require('../src/spec-validator');

describe('SpecValidator', () => {
  let validator;
  
  beforeEach(() => {
    validator = new SpecValidator();
  });
  
  describe('YAML validation', () => {
    test('validates correct YAML spec', () => {
      const content = `
name: test-project
description: "Test project"
requirements:
  functional:
    - id: FR-001
      description: "Test requirement"
      priority: high
      status: planned
test_cases:
  - id: TC-001
    description: "Test case"
    expected_result: "Success"
`;
      
      const result = validator.validate(content, 'test.yaml');
      
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });
    
    test('detects missing name field', () => {
      const content = `
description: "Test project"
requirements:
  functional: []
`;
      
      const result = validator.validate(content, 'test.yaml');
      
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Missing required field: name');
    });
    
    test('detects duplicate requirement IDs', () => {
      const content = `
name: test-project
requirements:
  functional:
    - id: FR-001
      description: "First requirement"
    - id: FR-001
      description: "Duplicate ID"
`;
      
      const result = validator.validate(content, 'test.yaml');
      
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.includes('Duplicate requirement ID'))).toBe(true);
    });
    
    test('warns about missing description', () => {
      const content = `
name: test-project
requirements:
  functional: []
`;
      
      const result = validator.validate(content, 'test.yaml');
      
      expect(result.warnings).toContain('Missing description field');
    });
  });
  
  describe('Markdown validation', () => {
    test('validates markdown with basic structure', () => {
      const content = `
## Overview
Test project

## Requirements
### Functional Requirements
**FR-001**: Test requirement

## Test Cases
**ID**: TC-001
`;
      
      const result = validator.validate(content, 'test.md');
      
      expect(result.valid).toBe(true);
    });
    
    test('warns about missing sections', () => {
      const content = `# Simple spec`;
      
      const result = validator.validate(content, 'test.md');
      
      expect(result.warnings.length).toBeGreaterThan(0);
    });
  });
  
  describe('unsupported formats', () => {
    test('rejects unsupported file format', () => {
      const result = validator.validate('content', 'test.txt');
      
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Unsupported file format: txt');
    });
  });
});
