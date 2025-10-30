#!/usr/bin/env python3
"""
Demo: Meaningful Spec File Naming and GitHub Integration

This script demonstrates the new meaningful file naming feature and GitHub MCP integration.
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.agents.spec_agent import SpecAgent

def demo_meaningful_naming():
    """Demonstrate meaningful file naming with banking context."""
    print("🚀 PromptToProduct: Meaningful Naming & GitHub Integration Demo")
    print("=" * 60)
    
    # Initialize spec agent
    spec_agent = SpecAgent()
    
    # Demo prompts with banking context
    demo_prompts = [
        {
            "prompt": "Create an epic for loan fraud detection system",
            "expected_domain": "loans",
            "expected_type": "epic"
        },
        {
            "prompt": "Build a feature for real-time payment processing",
            "expected_domain": "payments", 
            "expected_type": "feature"
        },
        {
            "prompt": "Implement KYC verification user story",
            "expected_domain": "compliance",
            "expected_type": "story"
        },
        {
            "prompt": "Create a credit card rewards management epic",
            "expected_domain": "cards",
            "expected_type": "epic"
        }
    ]
    
    results = []
    
    for i, demo in enumerate(demo_prompts, 1):
        print(f"\n{i}. Processing: {demo['prompt']}")
        print("-" * 40)
        
        # Prepare agent parameters
        agent_params = {
            "prompt": demo["prompt"],
            "intent": f"create_{demo['expected_type']}",
            "banking_context": {
                "is_banking": True,
                "product_types": [demo["expected_domain"]],
                "compliance_areas": ["KYC", "AML"] if demo["expected_domain"] == "compliance" else []
            },
            "entities": {
                "epic_references": [],
                "feature_references": [],
                "story_references": [],
                "technologies": [],
                "stakeholders": ["user"]
            }
        }
        
        # Process the specification
        try:
            result = spec_agent.process_specification_request(agent_params)
            
            if result.get("status") == "completed":
                created_files = result.get("created_files", [])
                github_sync = result.get("github_sync_data", [])
                
                if created_files:
                    print(f"✅ Created: {created_files[0]}")
                    filename = Path(created_files[0]).name
                    print(f"📝 Filename: {filename}")
                    
                if github_sync:
                    print(f"🚀 GitHub Integration: {github_sync[0].get('github_integration', 'Ready')}")
                    print(f"📋 Issue Title: {github_sync[0].get('issue_title', 'N/A')}")
                
                results.append({
                    "prompt": demo["prompt"],
                    "filename": Path(created_files[0]).name if created_files else "Not created",
                    "domain": demo["expected_domain"],
                    "type": demo["expected_type"],
                    "github_ready": bool(github_sync)
                })
            else:
                print(f"❌ Failed: {result.get('errors', ['Unknown error'])}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Summary
    print(f"\n📊 DEMO SUMMARY")
    print("=" * 60)
    
    for result in results:
        print(f"Domain: {result['domain']:10} | Type: {result['type']:7} | GitHub: {'✅' if result['github_ready'] else '❌'}")
        print(f"File: {result['filename']}")
        print(f"Prompt: {result['prompt'][:50]}...")
        print("-" * 60)
    
    print(f"\n🎉 Demo completed! {len(results)} specifications processed")
    print("📁 Check the specs/ directory for generated files")
    
    # GitHub configuration status
    print(f"\n🔧 GitHub Integration Status:")
    try:
        from src.config import get_github_config, get_system_config
        github_config = get_github_config()
        system_config = get_system_config()
        
        print(f"   Configured: {'✅' if github_config.is_configured else '❌'}")
        print(f"   Auto Sync: {'✅' if system_config.auto_sync_github else '❌'}")
        print(f"   Repository: {github_config.repo_owner}/{github_config.repo_name}")
        
        if not github_config.is_configured:
            print(f"   💡 Configure GitHub by copying .env.example to .env and setting your token")
            
    except Exception as e:
        print(f"   Status: Configuration error - {e}")

if __name__ == "__main__":
    demo_meaningful_naming()