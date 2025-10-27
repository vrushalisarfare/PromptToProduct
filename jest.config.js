module.exports = {
  testEnvironment: 'node',
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'src/**/*.js',
    '!src/cli.js'
  ],
  testMatch: [
    '**/tests/**/*.test.js'
  ],
  verbose: true
};
