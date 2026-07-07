module.exports = {
  testEnvironment: "jsdom",

  collectCoverage: true,

  collectCoverageFrom: [
    "frontend/src/**/*.{js,jsx}"
  ],

  coverageThreshold: {
    global: {
      branches: 85,
      functions: 85,
      lines: 85,
      statements: 85
    }
  }
};