#!/usr/bin/env python3
"""
Configuration Management for PromptToProduct

Centralized configuration loading from .env files and environment variables
with proper defaults and validation.
"""
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    print("Warning: python-dotenv not installed. Install with: pip install python-dotenv")

@dataclass
class GitHubConfig:
    """GitHub configuration settings."""
    token: Optional[str]
    repo_owner: str
    repo_name: str
    base_url: str
    
    @property
    def is_configured(self) -> bool:
        """Check if GitHub is properly configured."""
        return bool(self.token and self.repo_owner and self.repo_name)

@dataclass
class BankingConfig:
    """Banking domain configuration."""
    default_context: bool
    compliance_areas: list
    products: list

@dataclass
class AgentConfig:
    """Agent-specific configuration."""
    orchestrator_memory_size: int
    spec_agent_auto_validate: bool
    code_agent_default_language: str
    validation_agent_min_score: float

@dataclass
class PathConfig:
    """File path configuration."""
    specs_root: Path
    mybank_root: Path
    prompts_library: Path
    project_root: Path

@dataclass
class SystemConfig:
    """System-wide configuration."""
    log_level: str
    debug_mode: bool
    auto_sync_github: bool
    session_timeout: int
    development_mode: bool

class ConfigManager:
    """
    Centralized configuration management for PromptToProduct.
    
    Loads configuration from:
    1. .env file (if present)
    2. Environment variables
    3. Default values
    """
    
    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize configuration manager."""
        self.project_root = config_dir or Path(__file__).parent.parent
        self.env_file = self.project_root / ".env"
        
        # Load environment variables
        self._load_env_file()
        
        # Initialize all configurations
        self.github = self._load_github_config()
        self.banking = self._load_banking_config()
        self.agents = self._load_agent_config()
        self.paths = self._load_path_config()
        self.system = self._load_system_config()
    
    def _load_env_file(self):
        """Load .env file if available."""
        if DOTENV_AVAILABLE and self.env_file.exists():
            load_dotenv(self.env_file)
            print(f"✅ Loaded configuration from {self.env_file}")
        elif self.env_file.exists():
            print(f"⚠️ .env file found but python-dotenv not installed")
        else:
            print(f"ℹ️ No .env file found, using environment variables and defaults")
    
    def _load_github_config(self) -> GitHubConfig:
        """Load GitHub configuration."""
        # Get token from environment variable first, then from .env file
        token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
        
        return GitHubConfig(
            token=token,  # This will be None if not set, which is correct for security
            repo_owner=os.getenv("GITHUB_REPO_OWNER", "vrushalisarfare"),
            repo_name=os.getenv("GITHUB_REPO_NAME", "PromptToProduct"),
            base_url=os.getenv("GITHUB_BASE_URL", "https://api.github.com")
        )
    
    def _load_banking_config(self) -> BankingConfig:
        """Load banking domain configuration."""
        compliance_str = os.getenv("DEFAULT_COMPLIANCE_AREAS", "KYC,AML,PCI-DSS")
        products_str = os.getenv("BANKING_PRODUCTS", "loans,credit_cards,payments,investments,accounts,digital_banking")
        
        return BankingConfig(
            default_context=os.getenv("DEFAULT_BANKING_CONTEXT", "true").lower() == "true",
            compliance_areas=[area.strip() for area in compliance_str.split(",")],
            products=[product.strip() for product in products_str.split(",")]
        )
    
    def _load_agent_config(self) -> AgentConfig:
        """Load agent configuration."""
        return AgentConfig(
            orchestrator_memory_size=int(os.getenv("ORCHESTRATOR_MEMORY_SIZE", "10")),
            spec_agent_auto_validate=os.getenv("SPEC_AGENT_AUTO_VALIDATE", "true").lower() == "true",
            code_agent_default_language=os.getenv("CODE_AGENT_DEFAULT_LANGUAGE", "python"),
            validation_agent_min_score=float(os.getenv("VALIDATION_AGENT_MIN_SCORE", "0.7"))
        )
    
    def _load_path_config(self) -> PathConfig:
        """Load path configuration."""
        return PathConfig(
            specs_root=self.project_root / os.getenv("SPECS_ROOT_PATH", "specs"),
            mybank_root=self.project_root / os.getenv("MYBANK_ROOT_PATH", "src/MyBank"),
            prompts_library=self.project_root / os.getenv("PROMPTS_LIBRARY_PATH", "prompts"),
            project_root=self.project_root
        )
    
    def _load_system_config(self) -> SystemConfig:
        """Load system configuration."""
        return SystemConfig(
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            debug_mode=os.getenv("DEBUG_MODE", "false").lower() == "true",
            auto_sync_github=os.getenv("AUTO_SYNC_GITHUB", "false").lower() == "true",
            session_timeout=int(os.getenv("SESSION_TIMEOUT", "3600")),
            development_mode=os.getenv("DEVELOPMENT_MODE", "true").lower() == "true"
        )
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of current configuration."""
        return {
            "github_configured": self.github.is_configured,
            "repo": f"{self.github.repo_owner}/{self.github.repo_name}",
            "banking_products": len(self.banking.products),
            "compliance_areas": len(self.banking.compliance_areas),
            "specs_root": str(self.paths.specs_root),
            "debug_mode": self.system.debug_mode,
            "auto_sync": self.system.auto_sync_github
        }
    
    def validate_configuration(self) -> Dict[str, Any]:
        """Validate current configuration and return status."""
        issues = []
        warnings = []
        
        # Check GitHub configuration
        if not self.github.token:
            issues.append("GITHUB_PERSONAL_ACCESS_TOKEN environment variable not set")
        elif len(self.github.token) < 10:
            warnings.append("GitHub token seems too short")
        
        # Check paths
        if not self.paths.specs_root.exists():
            warnings.append(f"Specs directory does not exist: {self.paths.specs_root}")
        
        # Check agent configuration
        if self.agents.validation_agent_min_score > 1.0 or self.agents.validation_agent_min_score < 0.0:
            issues.append("Validation agent min score must be between 0.0 and 1.0")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "github_token_configured": bool(self.github.token),
            "summary": self.get_config_summary()
        }

# Global configuration instance
_config_instance = None

def get_config() -> ConfigManager:
    """Get the global configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigManager()
    return _config_instance

def reload_config() -> ConfigManager:
    """Reload configuration from files."""
    global _config_instance
    _config_instance = ConfigManager()
    return _config_instance

# Convenience functions for common configuration access
def get_github_config() -> GitHubConfig:
    """Get GitHub configuration."""
    return get_config().github

def get_banking_config() -> BankingConfig:
    """Get banking configuration."""
    return get_config().banking

def get_agent_config() -> AgentConfig:
    """Get agent configuration."""
    return get_config().agents

def get_path_config() -> PathConfig:
    """Get path configuration."""
    return get_config().paths

def get_system_config() -> SystemConfig:
    """Get system configuration."""
    return get_config().system