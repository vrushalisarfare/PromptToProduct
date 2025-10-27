#!/usr/bin/env python3
"""
Configuration Validation Tool for PromptToProduct

Run this script to validate your configuration setup and get recommendations.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Main configuration validation."""
    print("🔧 PromptToProduct Configuration Validator")
    print("=" * 50)
    
    try:
        from src.config import get_config
        config = get_config()
        
        # Validate configuration
        validation_result = config.validate_configuration()
        
        # Display summary
        summary = validation_result["summary"]
        print(f"\n📋 Configuration Summary:")
        print(f"   GitHub Configured: {'✅' if summary['github_configured'] else '❌'}")
        print(f"   Repository: {summary['repo']}")
        print(f"   Banking Products: {summary['banking_products']}")
        print(f"   Compliance Areas: {summary['compliance_areas']}")
        print(f"   Specs Directory: {summary['specs_root']}")
        print(f"   Debug Mode: {'✅' if summary['debug_mode'] else '❌'}")
        print(f"   Auto GitHub Sync: {'✅' if summary['auto_sync'] else '❌'}")
        
        # Display issues
        if validation_result["issues"]:
            print(f"\n❌ Configuration Issues:")
            for issue in validation_result["issues"]:
                print(f"   • {issue}")
        
        # Display warnings
        if validation_result["warnings"]:
            print(f"\n⚠️ Configuration Warnings:")
            for warning in validation_result["warnings"]:
                print(f"   • {warning}")
        
        # Display recommendations
        print(f"\n💡 Recommendations:")
        if not config.github.token:
            print(f"   1. Set GITHUB_PERSONAL_ACCESS_TOKEN environment variable")
            print(f"   2. Or create .env file with your GitHub token")
        
        if not (project_root / ".env").exists():
            print(f"   3. Copy .env.example to .env and configure your settings")
        
        print(f"   4. Run: pip install python-dotenv (for .env file support)")
        
        # Overall status
        if validation_result["valid"]:
            print(f"\n✅ Configuration is valid!")
        else:
            print(f"\n❌ Configuration has issues that need to be resolved.")
            
    except ImportError as e:
        print(f"❌ Failed to load configuration system: {e}")
        print(f"\n💡 Quick Setup:")
        print(f"   1. Install dependencies: pip install python-dotenv")
        print(f"   2. Copy .env.example to .env")
        print(f"   3. Set your GITHUB_PERSONAL_ACCESS_TOKEN")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())