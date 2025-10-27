class Calculator {
  constructor() {
    this.history = [];
  }
  
  add(a, b) {
    const result = a + b;
    this._addToHistory('add', a, b, result);
    return result;
  }
  
  subtract(a, b) {
    const result = a - b;
    this._addToHistory('subtract', a, b, result);
    return result;
  }
  
  multiply(a, b) {
    const result = a * b;
    this._addToHistory('multiply', a, b, result);
    return result;
  }
  
  divide(a, b) {
    if (b === 0) {
      throw new Error('Cannot divide by zero');
    }
    const result = a / b;
    this._addToHistory('divide', a, b, result);
    return result;
  }
  
  getHistory() {
    return this.history.slice(-10); // Last 10 calculations
  }
  
  clearHistory() {
    this.history = [];
  }
  
  _addToHistory(operation, operand1, operand2, result) {
    this.history.push({
      operation,
      operand1,
      operand2,
      result,
      timestamp: new Date().toISOString()
    });
  }
}

module.exports = Calculator;
