# GitHub MCP Server Setup Script
# Run this script to configure GitHub PAT and validate MCP setup

param(
    [Parameter(Mandatory=$false)]
    [string]$GitHubToken,
    
    [Parameter(Mandatory=$false)]
    [switch]$ValidateOnly
)

Write-Host "🚀 GitHub MCP Server Configuration Script" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Function to test GitHub API access
function Test-GitHubAccess {
    param([string]$Token)
    
    try {
        $headers = @{
            "Authorization" = "Bearer $Token"
            "Accept" = "application/vnd.github.v3+json"
        }
        
        $response = Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $headers
        Write-Host "✅ GitHub API access successful!" -ForegroundColor Green
        Write-Host "   User: $($response.login)" -ForegroundColor Gray
        Write-Host "   Name: $($response.name)" -ForegroundColor Gray
        return $true
    }
    catch {
        Write-Host "❌ GitHub API access failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to test repository access
function Test-RepositoryAccess {
    param([string]$Token)
    
    try {
        $headers = @{
            "Authorization" = "Bearer $Token"
            "Accept" = "application/vnd.github.v3+json"
        }
        
        $response = Invoke-RestMethod -Uri "https://api.github.com/repos/vrushalisarfare/PromptToProduct" -Headers $headers
        Write-Host "✅ Repository access successful!" -ForegroundColor Green
        Write-Host "   Repository: $($response.full_name)" -ForegroundColor Gray
        Write-Host "   Description: $($response.description)" -ForegroundColor Gray
        return $true
    }
    catch {
        Write-Host "❌ Repository access failed: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "   Make sure your token has 'repo' scope permissions" -ForegroundColor Yellow
        return $false
    }
}

# Check if validation only mode
if ($ValidateOnly) {
    Write-Host "🔍 Validation Mode - Checking existing configuration..." -ForegroundColor Yellow
    
    $existingToken = $env:GITHUB_PERSONAL_ACCESS_TOKEN
    if (-not $existingToken) {
        Write-Host "❌ GITHUB_PERSONAL_ACCESS_TOKEN environment variable not set" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✅ Environment variable found" -ForegroundColor Green
    
    if (Test-GitHubAccess -Token $existingToken) {
        if (Test-RepositoryAccess -Token $existingToken) {
            Write-Host "🎉 All validations passed! MCP server should work correctly." -ForegroundColor Green
            exit 0
        }
    }
    exit 1
}

# Setup mode
if (-not $GitHubToken) {
    Write-Host "📝 Please provide your GitHub Personal Access Token" -ForegroundColor Yellow
    Write-Host "   You can generate one at: https://github.com/settings/tokens" -ForegroundColor Gray
    Write-Host ""
    $GitHubToken = Read-Host "Enter your GitHub PAT"
}

if (-not $GitHubToken) {
    Write-Host "❌ No token provided. Exiting." -ForegroundColor Red
    exit 1
}

# Validate token format
if ($GitHubToken -notmatch "^(ghp_|github_pat_)[A-Za-z0-9_]+$") {
    Write-Host "⚠️  Warning: Token doesn't match expected GitHub PAT format" -ForegroundColor Yellow
    Write-Host "   Modern PATs should start with 'ghp_' or 'github_pat_'" -ForegroundColor Gray
}

Write-Host "🔐 Testing GitHub API access..." -ForegroundColor Blue

if (-not (Test-GitHubAccess -Token $GitHubToken)) {
    Write-Host "❌ Failed to access GitHub API. Please check your token." -ForegroundColor Red
    exit 1
}

Write-Host "🏛️ Testing repository access..." -ForegroundColor Blue

if (-not (Test-RepositoryAccess -Token $GitHubToken)) {
    Write-Host "❌ Failed to access repository. Please check token permissions." -ForegroundColor Red
    exit 1
}

# Set environment variable
Write-Host "💾 Setting environment variable..." -ForegroundColor Blue

try {
    # Set for current session
    $env:GITHUB_PERSONAL_ACCESS_TOKEN = $GitHubToken
    
    # Set permanently for user
    [Environment]::SetEnvironmentVariable("GITHUB_PERSONAL_ACCESS_TOKEN", $GitHubToken, "User")
    
    Write-Host "✅ Environment variable set successfully!" -ForegroundColor Green
    Write-Host "   Current session: Set" -ForegroundColor Gray
    Write-Host "   User profile: Set (requires restart for some applications)" -ForegroundColor Gray
}
catch {
    Write-Host "❌ Failed to set environment variable: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Check MCP configuration files
Write-Host "📁 Checking MCP configuration..." -ForegroundColor Blue

$mcpConfigPath = ".vscode\mcp.json"
if (Test-Path $mcpConfigPath) {
    Write-Host "✅ MCP configuration file found: $mcpConfigPath" -ForegroundColor Green
} else {
    Write-Host "❌ MCP configuration file not found: $mcpConfigPath" -ForegroundColor Red
}

$mcpServerPath = "mcp_server\mcp_main.py"
if (Test-Path $mcpServerPath) {
    Write-Host "✅ Local MCP server found: $mcpServerPath" -ForegroundColor Green
} else {
    Write-Host "⚠️  Local MCP server not found: $mcpServerPath" -ForegroundColor Yellow
    Write-Host "   The local server is optional but recommended for repository-specific operations" -ForegroundColor Gray
}

Write-Host ""
Write-Host "🎉 Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Restart VS Code to load the new environment variable" -ForegroundColor White
Write-Host "2. Install the MCP extension in VS Code if not already installed" -ForegroundColor White
Write-Host "3. Open the PromptToProduct workspace" -ForegroundColor White
Write-Host "4. Check MCP status in VS Code (Ctrl+Shift+P → 'MCP: Show Status')" -ForegroundColor White
Write-Host ""
Write-Host "To validate your setup later, run:" -ForegroundColor Gray
Write-Host "  .\setup-github-mcp.ps1 -ValidateOnly" -ForegroundColor Gray