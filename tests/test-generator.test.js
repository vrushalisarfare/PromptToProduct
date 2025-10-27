const { TestGenerator } = require('../src/test-generator');

describe('TestGenerator', () => {
  let generator;
  
  beforeEach(() => {
    generator = new TestGenerator();
  });
  
  test('generates test structure for functional requirements', () => {
    const spec = {
      name: 'test-app',
      requirements: {
        functional: [
          {
            id: 'FR-001',
            description: 'User can login',
            priority: 'high'
          }
        ]
      }
    };
    
    const tests = generator.generate(spec);
    
    expect(tests).toContain("describe('test-app'");
    expect(tests).toContain("describe('Functional Requirements'");
    expect(tests).toContain("test('FR-001: User can login'");
    expect(tests).toContain('TODO: Implement test for FR-001');
  });
  
  test('generates tests for user stories', () => {
    const spec = {
      name: 'test-app',
      user_stories: [
        {
          id: 'US-001',
          as_a: 'user',
          i_want: 'to login',
          so_that: 'I can access my account',
          acceptance_criteria: [
            'Login form is displayed',
            'User can submit credentials'
          ]
        }
      ]
    };
    
    const tests = generator.generate(spec);
    
    expect(tests).toContain("describe('User Stories'");
    expect(tests).toContain('As a user');
    expect(tests).toContain('I want to login');
    expect(tests).toContain('Login form is displayed');
  });
  
  test('generates tests for test cases', () => {
    const spec = {
      name: 'test-app',
      test_cases: [
        {
          id: 'TC-001',
          description: 'Test login functionality',
          preconditions: 'User exists',
          steps: ['Open login page', 'Enter credentials', 'Click submit'],
          expected_result: 'User is logged in'
        }
      ]
    };
    
    const tests = generator.generate(spec);
    
    expect(tests).toContain("describe('Test Cases'");
    expect(tests).toContain("test('TC-001: Test login functionality'");
    expect(tests).toContain('Preconditions: User exists');
    expect(tests).toContain('1. Open login page');
    expect(tests).toContain('Expected: User is logged in');
  });
  
  test('generates valid JavaScript test file', () => {
    const spec = {
      name: 'simple-app',
      requirements: {
        functional: [
          { id: 'FR-001', description: 'Basic feature' }
        ]
      }
    };
    
    const tests = generator.generate(spec);
    
    // Should not throw syntax error
    expect(() => {
      new Function(tests);
    }).not.toThrow();
    
    expect(tests).toContain('describe(');
    expect(tests).toContain('test(');
    expect(tests).toContain('expect(');
  });
  
  test('handles empty spec gracefully', () => {
    const spec = {
      name: 'empty-app'
    };
    
    const tests = generator.generate(spec);
    
    expect(tests).toContain("describe('empty-app'");
    expect(tests).toBeTruthy();
  });
});
