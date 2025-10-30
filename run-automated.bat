@echo off
REM Automated PromptToProduct execution script
REM Usage: run-automated.bat "Your prompt here"

if "%1"=="" (
    echo Error: Please provide a prompt
    echo Usage: run-automated.bat "Your prompt here"
    exit /b 1
)

echo 🤖 Running PromptToProduct in automated mode...
echo 📝 Prompt: %1

REM Set environment variable and run
set "PROMPTTOPRODUCT_PROMPT=%~1"
python prompttoproduct.py --auto

REM Clean up
set "PROMPTTOPRODUCT_PROMPT="

echo 🎉 Automated execution finished!