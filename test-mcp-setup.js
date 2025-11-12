#!/usr/bin/env node

// Simple test to verify MCP GitHub server setup
const { spawn } = require('child_process');

// Set the GitHub token from environment
process.env.GITHUB_PERSONAL_ACCESS_TOKEN = process.env.GITHUB_PERSONAL_ACCESS_TOKEN || 
  require('child_process').execSync('powershell -Command "[System.Environment]::GetEnvironmentVariable(\'GITHUB_PERSONAL_ACCESS_TOKEN\', \'User\')"', {encoding: 'utf8'}).trim();

console.log('🧪 Testing GitHub MCP Server Setup...');
console.log(`Token available: ${!!process.env.GITHUB_PERSONAL_ACCESS_TOKEN}`);
console.log(`Token length: ${process.env.GITHUB_PERSONAL_ACCESS_TOKEN?.length || 0}`);

// Test MCP server initialization
const mcpServer = spawn('mcp-server-github', [], {
  stdio: ['pipe', 'pipe', 'pipe'],
  env: { ...process.env }
});

let output = '';
let errorOutput = '';

mcpServer.stdout.on('data', (data) => {
  output += data.toString();
});

mcpServer.stderr.on('data', (data) => {
  errorOutput += data.toString();
});

// Send initialization message
const initMessage = {
  jsonrpc: "2.0",
  id: 1,
  method: "initialize",
  params: {
    protocolVersion: "2024-11-05",
    capabilities: {},
    clientInfo: {
      name: "PromptToProduct",
      version: "1.0"
    }
  }
};

mcpServer.stdin.write(JSON.stringify(initMessage) + '\n');

setTimeout(() => {
  mcpServer.kill();
  
  console.log('\n📊 MCP Server Test Results:');
  console.log('Output:', output || 'No output');
  console.log('Errors:', errorOutput || 'No errors');
  
  if (output.includes('jsonrpc') || output.includes('result')) {
    console.log('✅ MCP Server appears to be working');
  } else {
    console.log('⚠️ MCP Server response unclear');
  }
  
  console.log('\n🔗 Next Steps:');
  console.log('1. Restart VS Code to load MCP configuration');
  console.log('2. Open this project in VS Code');
  console.log('3. MCP tools should be available to GitHub Copilot');
  console.log('4. Test with: python prompttoproduct.py "Create test feature"');
  
}, 2000);