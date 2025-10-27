# GitHub MCP Server Configuration Guide

## Step 1: Create GitHub Personal Access Token (PAT)

### 1.1 Generate PAT on GitHub
1. Go to GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Configure the token:
   - **Name**: `PromptToProduct MCP Server`
   - **Expiration**: 90 days (or as per your organization policy)
   - **Scopes** (select these permissions):
     - ✅ `repo` (Full control of private repositories)
     - ✅ `read:org` (Read organization membership)
     - ✅ `user:email` (Access user email addresses)
     - ✅ `read:project` (Read project boards)

### 1.2 Save Your Token
⚠️ **IMPORTANT**: Copy the token immediately after generation - you won't be able to see it again!

## Step 2: Configure Environment Variables

### Windows (PowerShell)
```powershell
# Set environment variable for current session
$env:GITHUB_PERSONAL_ACCESS_TOKEN = "your_github_token_here"

# Set permanently (requires restart)
[Environment]::SetEnvironmentVariable("GITHUB_PERSONAL_ACCESS_TOKEN", "your_github_token_here", "User")
```

### Windows (Command Prompt)
```cmd
setx GITHUB_PERSONAL_ACCESS_TOKEN "your_github_token_here"
```

### macOS/Linux
```bash
# Add to ~/.bashrc or ~/.zshrc
export GITHUB_PERSONAL_ACCESS_TOKEN="your_github_token_here"

# Reload shell or restart terminal
source ~/.bashrc
```

## Step 3: Verify Configuration

### 3.1 Check Environment Variable
```powershell
# Windows PowerShell
echo $env:GITHUB_PERSONAL_ACCESS_TOKEN

# Should display your token (first few characters will be visible)
```

### 3.2 Test GitHub API Access
```powershell
# Test API access
curl -H "Authorization: Bearer $env:GITHUB_PERSONAL_ACCESS_TOKEN" https://api.github.com/user
```

## Step 4: VS Code MCP Configuration

The MCP configuration file has been created at:
`.vscode/mcp.json`

### Configuration Details:
- **GitHub MCP Server**: Official server for GitHub integration
- **Local PromptToProduct Server**: Custom server for repository-specific operations
- **Environment Variables**: Secure token handling via environment variables
- **Base URL**: GitHub API endpoint (https://api.github.com)

## Step 5: VS Code Setup

### 5.1 Install MCP Extension
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "MCP" or "Model Context Protocol"
4. Install the official MCP extension

### 5.2 Reload VS Code
1. Close VS Code completely
2. Restart VS Code
3. Open the PromptToProduct workspace
4. The MCP servers should automatically connect

## Step 6: Verification

### 6.1 Check MCP Status
1. Open VS Code Command Palette (Ctrl+Shift+P)
2. Type "MCP: Show Status"
3. Verify both servers are connected:
   - ✅ `github` - Connected
   - ✅ `prompttoproduct-local` - Connected

### 6.2 Test GitHub Integration
1. Open Copilot Chat
2. Try a command like: "List recent commits in this repository"
3. Copilot should be able to access GitHub data via the MCP server

## Troubleshooting

### Common Issues:
1. **Token not recognized**: Ensure environment variable is set correctly
2. **Permission denied**: Verify token has required scopes
3. **Server not connecting**: Check VS Code MCP extension is installed
4. **Path issues**: Ensure `mcp_server/mcp_main.py` exists in workspace

### Debug Commands:
```powershell
# Check if token is set
echo $env:GITHUB_PERSONAL_ACCESS_TOKEN

# Test GitHub API directly
curl -H "Authorization: Bearer $env:GITHUB_PERSONAL_ACCESS_TOKEN" https://api.github.com/repos/vrushalisarfare/PromptToProduct

# Check MCP server files exist
ls mcp_server/mcp_main.py
```

## Security Notes
- Never commit your PAT to version control
- Use environment variables for token storage
- Regularly rotate your tokens (every 90 days recommended)
- Limit token scopes to minimum required permissions