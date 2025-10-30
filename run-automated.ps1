#!/usr/bin/env powershell
<#
.SYNOPSIS
    Automated PromptToProduct execution script
    
.DESCRIPTION
    Demonstrates automated execution of PromptToProduct system without user interaction
    
.PARAMETER Prompt
    The prompt to execute
    
.PARAMETER Silent
    Run in silent mode with minimal output
    
.EXAMPLE
    .\run-automated.ps1 -Prompt "Create loan API"
    .\run-automated.ps1 -Prompt "Build fraud detection" -Silent
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$Prompt,
    
    [switch]$Silent
)

# Set environment variable for automated execution
$env:PROMPTTOPRODUCT_PROMPT = $Prompt

Write-Host "🤖 Running PromptToProduct in automated mode..." -ForegroundColor Cyan
Write-Host "📝 Prompt: $Prompt" -ForegroundColor Yellow

if ($Silent) {
    # Run in silent mode (redirect output)
    python prompttoproduct.py --auto --json | Out-Null
    Write-Host "✅ Execution completed silently" -ForegroundColor Green
} else {
    # Run with full output
    python prompttoproduct.py --auto
}

# Clean up environment variable
Remove-Item env:PROMPTTOPRODUCT_PROMPT -ErrorAction SilentlyContinue

Write-Host "🎉 Automated execution finished!" -ForegroundColor Green