const Calculator = require('../src/calculator');

describe('Calculator Implementation', () => {
  let calculator;
  
  beforeEach(() => {
    calculator = new Calculator();
  });
  
  describe('Basic Operations', () => {
    test('adds two positive numbers', () => {
      expect(calculator.add(5, 3)).toBe(8);
    });
    
    test('subtracts two numbers', () => {
      expect(calculator.subtract(10, 4)).toBe(6);
    });
    
    test('multiplies two numbers', () => {
      expect(calculator.multiply(6, 7)).toBe(42);
    });
    
    test('divides two numbers', () => {
      expect(calculator.divide(20, 4)).toBe(5);
    });
    
    test('handles decimal numbers', () => {
      expect(calculator.add(1.5, 2.3)).toBeCloseTo(3.8);
      expect(calculator.multiply(2.5, 4)).toBe(10);
    });
    
    test('handles negative numbers', () => {
      expect(calculator.add(-5, 3)).toBe(-2);
      expect(calculator.subtract(-10, -4)).toBe(-6);
    });
  });
  
  describe('Error Handling', () => {
    test('throws error on division by zero', () => {
      expect(() => {
        calculator.divide(10, 0);
      }).toThrow('Cannot divide by zero');
    });
  });
  
  describe('History Feature', () => {
    test('stores calculation history', () => {
      calculator.add(5, 3);
      calculator.multiply(2, 4);
      
      const history = calculator.getHistory();
      
      expect(history).toHaveLength(2);
      expect(history[0].operation).toBe('add');
      expect(history[0].result).toBe(8);
      expect(history[1].operation).toBe('multiply');
      expect(history[1].result).toBe(8);
    });
    
    test('limits history to last 10 calculations', () => {
      for (let i = 0; i < 15; i++) {
        calculator.add(i, 1);
      }
      
      expect(calculator.getHistory()).toHaveLength(10);
    });
    
    test('clears history', () => {
      calculator.add(5, 3);
      calculator.clearHistory();
      
      expect(calculator.getHistory()).toHaveLength(0);
    });
  });
  
  describe('Performance', () => {
    test('completes operations under 100ms', () => {
      const start = Date.now();
      
      for (let i = 0; i < 1000; i++) {
        calculator.add(i, i + 1);
      }
      
      const duration = Date.now() - start;
      
      expect(duration).toBeLessThan(100);
    });
  });
});
