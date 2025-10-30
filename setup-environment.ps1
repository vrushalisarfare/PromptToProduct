# PromptToProduct Environment Setup Script
# This script helps set up the required environment variables for the PromptToProduct system

param(
    [Parameter(Mandatory=$false)]
    [string]$GitHubToken,
    
    [Parameter(Mandatory=$false)]
    [switch]$Check,
    
    [Parameter(Mandatory=$false)]
    [switch]$Help
)

function Show-Help {
    Write-Host @"
PromptToProduct Environment Setup Script
========================================

Usage:
  .\setup-environment.ps1 -GitHubToken <your_token>   # Set GitHub token
  .\setup-environment.ps1 -Check                      # Check environment
  .\setup-environment.ps1 -Help                       # Show this help

Examples:
  .\setup-environment.ps1 -GitHubToken "ghp_xxxxxxxxxxxxxxxxxxxx"
  .\setup-environment.ps1 -Check

Environment Variables:
  GITHUB_PERSONAL_ACCESS_TOKEN - Your GitHub Personal Access Token (required)
  GITHUB_REPO_OWNER           - Repository owner (default: vrushalisarfare)
  GITHUB_REPO_NAME            - Repository name (default: PromptToProduct)

Security Note:
  The GitHub token is stored as a USER environment variable for security.
  It will be available in future PowerShell sessions but not visible in files.

"@
}

function Set-GitHubToken {
    param([string]$Token)
    
    if ([string]::IsNullOrEmpty($Token)) {
        Write-Host "❌ No token provided" -ForegroundColor Red
        return
    }
    
    if ($Token.Length -lt 10) {
        Write-Host "⚠️ Warning: Token seems too short" -ForegroundColor Yellow
    }
    
    try {
        # Set user environment variable (persists across sessions)
        [Environment]::SetEnvironmentVariable("GITHUB_PERSONAL_ACCESS_TOKEN", $Token, [EnvironmentVariableTarget]::User)
        
        # Set for current session
        $env:GITHUB_PERSONAL_ACCESS_TOKEN = $Token
        
        Write-Host "✅ GitHub Personal Access Token set successfully" -ForegroundColor Green
        Write-Host "   Token will be available in future PowerShell sessions" -ForegroundColor Gray
        
        # Test the token
        Test-GitHubToken $Token
        
    } catch {
        Write-Host "❌ Failed to set environment variable: $($_.Exception.Message)" -ForegroundColor Red
    }
}

function Test-GitHubToken {
    param([string]$Token)
    
    if ([string]::IsNullOrEmpty($Token)) {
        Write-Host "⚠️ No token to test" -ForegroundColor Yellow
        return
    }
    
    Write-Host "🔍 Testing GitHub token..." -ForegroundColor Cyan
    
    try {
        $headers = @{
            "Authorization" = "token $Token"
            "User-Agent" = "PromptToProduct"
        }
        
        $response = Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $headers -Method Get
        Write-Host "✅ Token is valid for user: $($response.login)" -ForegroundColor Green
        
        # Test repository access
        $repoResponse = Invoke-RestMethod -Uri "https://api.github.com/repos/vrushalisarfare/PromptToProduct" -Headers $headers -Method Get
        Write-Host "✅ Repository access confirmed: $($repoResponse.full_name)" -ForegroundColor Green
        
    } catch {
        if ($_.Exception.Response.StatusCode -eq 401) {
            Write-Host "❌ Token is invalid or expired" -ForegroundColor Red
        } elseif ($_.Exception.Response.StatusCode -eq 404) {
            Write-Host "❌ Repository not found or no access" -ForegroundColor Red
        } else {
            Write-Host "❌ Token test failed: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

function Check-Environment {
    Write-Host "🔍 Checking PromptToProduct Environment Configuration" -ForegroundColor Cyan
    Write-Host "=" * 60
    
    # Check GitHub token
    $token = [Environment]::GetEnvironmentVariable("GITHUB_PERSONAL_ACCESS_TOKEN", [EnvironmentVariableTarget]::User)
    if ([string]::IsNullOrEmpty($token)) {
        $token = $env:GITHUB_PERSONAL_ACCESS_TOKEN
    }
    
    if ([string]::IsNullOrEmpty($token)) {
        Write-Host "❌ GITHUB_PERSONAL_ACCESS_TOKEN not set" -ForegroundColor Red
        Write-Host "   Run: .\setup-environment.ps1 -GitHubToken <your_token>" -ForegroundColor Gray
    } else {
        Write-Host "✅ GITHUB_PERSONAL_ACCESS_TOKEN configured" -ForegroundColor Green
        Test-GitHubToken $token
    }
    
    # Check other environment variables
    $vars = @{
        "GITHUB_REPO_OWNER" = "vrushalisarfare"
        "GITHUB_REPO_NAME" = "PromptToProduct"
    }
    
    foreach ($var in $vars.GetEnumerator()) {
        $value = [Environment]::GetEnvironmentVariable($var.Key)
        if ([string]::IsNullOrEmpty($value)) {
            Write-Host "ℹ️ $($var.Key) not set (will use default: $($var.Value))" -ForegroundColor Yellow
        } else {
            Write-Host "✅ $($var.Key) = $value" -ForegroundColor Green
        }
    }
    
    # Check Python environment
    Write-Host "`n🐍 Python Environment:" -ForegroundColor Cyan
    $pythonPath = "C:\PrompttoProduct\PromptToProduct-1\.venv\Scripts\python.exe"
    if (Test-Path $pythonPath) {
        Write-Host "✅ Python virtual environment found" -ForegroundColor Green
        try {
            $pythonVersion = & $pythonPath --version 2>&1
            Write-Host "   Version: $pythonVersion" -ForegroundColor Gray
        } catch {
            Write-Host "⚠️ Could not get Python version" -ForegroundColor Yellow
        }
    } else {
        Write-Host "❌ Python virtual environment not found at $pythonPath" -ForegroundColor Red
    }
    
    # Check PromptToProduct system
    Write-Host "`n🎯 PromptToProduct System:" -ForegroundColor Cyan
    $mainScript = "C:\PrompttoProduct\PromptToProduct-1\prompttoproduct.py"
    if (Test-Path $mainScript) {
        Write-Host "✅ PromptToProduct script found" -ForegroundColor Green
        Write-Host "   Ready to run: python prompttoproduct.py --status" -ForegroundColor Gray
    } else {
        Write-Host "❌ PromptToProduct script not found" -ForegroundColor Red
    }
}

# Main script logic
if ($Help) {
    Show-Help
    exit 0
}

if ($Check) {
    Check-Environment
    exit 0
}

if (-not [string]::IsNullOrEmpty($GitHubToken)) {
    Set-GitHubToken $GitHubToken
    exit 0
}

# If no parameters provided, show help
Write-Host "PromptToProduct Environment Setup" -ForegroundColor Cyan
Write-Host "Use -Help for detailed instructions" -ForegroundColor Gray
Write-Host ""
Write-Host "Quick setup:"
Write-Host "  .\setup-environment.ps1 -GitHubToken <your_token>"
Write-Host "  .\setup-environment.ps1 -Check"