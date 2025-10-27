class SpecValidator {
  validate(content, filename) {
    const result = {
      valid: true,
      errors: [],
      warnings: []
    };
    
    const ext = filename.split('.').pop().toLowerCase();
    
    if (ext === 'yaml' || ext === 'yml') {
      this.validateYAML(content, result);
    } else if (ext === 'md') {
      this.validateMarkdown(content, result);
    } else {
      result.valid = false;
      result.errors.push(`Unsupported file format: ${ext}`);
    }
    
    return result;
  }
  
  validateYAML(content, result) {
    const YAML = require('yaml');
    
    try {
      const spec = YAML.parse(content);
      
      // Check required fields
      if (!spec.name) {
        result.errors.push('Missing required field: name');
        result.valid = false;
      }
      
      if (!spec.description) {
        result.warnings.push('Missing description field');
      }
      
      if (!spec.requirements) {
        result.warnings.push('No requirements defined');
      } else {
        if (!spec.requirements.functional || spec.requirements.functional.length === 0) {
          result.warnings.push('No functional requirements defined');
        }
      }
      
      // Validate requirement IDs are unique
      if (spec.requirements) {
        const ids = new Set();
        const allRequirements = [
          ...(spec.requirements.functional || []),
          ...(spec.requirements.non_functional || [])
        ];
        
        allRequirements.forEach(req => {
          if (!req.id) {
            result.errors.push('Requirement missing ID');
            result.valid = false;
          } else if (ids.has(req.id)) {
            result.errors.push(`Duplicate requirement ID: ${req.id}`);
            result.valid = false;
          } else {
            ids.add(req.id);
          }
        });
      }
      
      // Validate test cases
      if (spec.test_cases) {
        spec.test_cases.forEach((tc, index) => {
          if (!tc.id) {
            result.errors.push(`Test case at index ${index} missing ID`);
            result.valid = false;
          }
          if (!tc.description) {
            result.warnings.push(`Test case ${tc.id || index} missing description`);
          }
          if (!tc.expected_result) {
            result.warnings.push(`Test case ${tc.id || index} missing expected result`);
          }
        });
      } else {
        result.warnings.push('No test cases defined');
      }
      
    } catch (error) {
      result.valid = false;
      result.errors.push(`Invalid YAML: ${error.message}`);
    }
  }
  
  validateMarkdown(content, result) {
    // Check for basic structure
    const requiredSections = ['## Overview', '## Requirements', '## Test Cases'];
    const missingSections = requiredSections.filter(section => 
      !content.includes(section)
    );
    
    if (missingSections.length > 0) {
      missingSections.forEach(section => {
        result.warnings.push(`Missing recommended section: ${section}`);
      });
    }
    
    // Check if file is too short
    if (content.length < 100) {
      result.warnings.push('Specification seems incomplete (very short)');
    }
    
    // Check for at least one requirement
    if (!content.match(/\*\*FR-\d+\*\*/)) {
      result.warnings.push('No functional requirements found');
    }
    
    // Check for at least one test case
    if (!content.match(/\*\*ID\*\*:\s*TC-\d+/)) {
      result.warnings.push('No test cases found');
    }
  }
}

module.exports = { SpecValidator };
