class TestGenerator {
  generate(spec) {
    let output = '';
    
    // Add header
    output += '// Auto-generated tests from specification\n';
    output += '// DO NOT EDIT: This file was generated from the specification\n\n';
    
    // Add describe block for the project
    output += `describe('${spec.name || 'Application'}', () => {\n`;
    
    // Generate tests for functional requirements
    if (spec.requirements && spec.requirements.functional) {
      output += '  describe(\'Functional Requirements\', () => {\n';
      
      spec.requirements.functional.forEach(req => {
        output += `    test('${req.id}: ${req.description}', () => {\n`;
        output += `      // TODO: Implement test for ${req.id}\n`;
        output += '      expect(true).toBe(true);\n';
        output += '    });\n\n';
      });
      
      output += '  });\n\n';
    }
    
    // Generate tests for user stories
    if (spec.user_stories && spec.user_stories.length > 0) {
      output += '  describe(\'User Stories\', () => {\n';
      
      spec.user_stories.forEach(story => {
        const testName = `${story.id || 'User Story'}: As a ${story.as_a}, I want ${story.i_want}`;
        output += `    test('${testName}', () => {\n`;
        
        if (story.acceptance_criteria && story.acceptance_criteria.length > 0) {
          story.acceptance_criteria.forEach(criterion => {
            output += `      // Acceptance: ${criterion}\n`;
          });
        }
        
        output += '      // TODO: Implement test for this user story\n';
        output += '      expect(true).toBe(true);\n';
        output += '    });\n\n';
      });
      
      output += '  });\n\n';
    }
    
    // Generate tests for test cases
    if (spec.test_cases && spec.test_cases.length > 0) {
      output += '  describe(\'Test Cases\', () => {\n';
      
      spec.test_cases.forEach(tc => {
        output += `    test('${tc.id}: ${tc.description}', () => {\n`;
        
        if (tc.preconditions) {
          output += `      // Preconditions: ${tc.preconditions}\n`;
        }
        
        if (tc.steps && tc.steps.length > 0) {
          output += '      // Steps:\n';
          tc.steps.forEach((step, index) => {
            output += `      // ${index + 1}. ${step}\n`;
          });
        }
        
        if (tc.expected_result) {
          output += `      // Expected: ${tc.expected_result}\n`;
        }
        
        output += '      // TODO: Implement test steps\n';
        output += '      expect(true).toBe(true);\n';
        output += '    });\n\n';
      });
      
      output += '  });\n';
    }
    
    output += '});\n';
    
    return output;
  }
}

module.exports = { TestGenerator };
