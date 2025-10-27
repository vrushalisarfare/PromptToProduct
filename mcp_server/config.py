"""
Configuration for the PromptToProduct MCP server.
"""
import os
from typing import Dict, Any

# Repository configuration
REPO_CONFIG = {
    "owner": "vrushalisarfare",
    "name": "PromptToProduct",
    "full_name": "vrushalisarfare/PromptToProduct",
    "clone_url": "https://github.com/vrushalisarfare/PromptToProduct.git"
}

def get_config() -> Dict[str, Any]:
    """Get server configuration from environment variables and defaults."""
    return {
        "host": os.environ.get("MCP_HOST", "0.0.0.0"),
        "port": int(os.environ.get("MCP_PORT", "8080")),
        "github_webhook_secret": os.environ.get("GITHUB_WEBHOOK_SECRET"),
        "repo": REPO_CONFIG,
        "debug": os.environ.get("DEBUG", "false").lower() == "true"
    }

def is_valid_repo(repo_full_name: str) -> bool:
    """Check if the repository is the expected PromptToProduct repo."""
    return repo_full_name == REPO_CONFIG["full_name"]