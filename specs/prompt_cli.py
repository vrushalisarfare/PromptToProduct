#!/usr/bin/env python3
"""
PromptToProduct Schema CLI
Simple command-line interface for processing prompts using the PromptToProduct schema.
"""
from schema_processor import PromptToProductSchema
import sys
import json


def print_help():
    """Print usage help."""
    help_text = """
PromptToProduct Schema CLI

Usage:
    python prompt_cli.py "<prompt>"
    python prompt_cli.py --validate
    python prompt_cli.py --status

Examples:
    python prompt_cli.py "Create an epic for user management system"
    python prompt_cli.py "Add a feature for authentication under epic E001"
    python prompt_cli.py "Create a story for login validation under feature F001"
    python prompt_cli.py --validate

Commands:
    --validate    Validate all spec links
    --status      Show current specs status
    --help        Show this help message
"""
    print(help_text)


def show_status():
    """Show current status of specs."""
    processor = PromptToProductSchema()
    validation = processor.validate_spec_links()
    
    print("📊 PromptToProduct Schema Status")
    print("=" * 40)
    print(f"Epics:    {len(validation['epics'])} ({', '.join(validation['epics']) if validation['epics'] else 'None'})")
    print(f"Features: {len(validation['features'])} ({', '.join(validation['features']) if validation['features'] else 'None'})")
    print(f"Stories:  {len(validation['stories'])} ({', '.join(validation['stories']) if validation['stories'] else 'None'})")
    
    if validation['orphaned_features']:
        print(f"\n⚠️  Orphaned Features:")
        for orphan in validation['orphaned_features']:
            print(f"   {orphan['feature']} → missing epic {orphan['missing_epic']}")
    
    if validation['orphaned_stories']:
        print(f"\n⚠️  Orphaned Stories:")
        for orphan in validation['orphaned_stories']:
            print(f"   {orphan['story']} → missing feature {orphan['missing_feature']}")
    
    if not validation['orphaned_features'] and not validation['orphaned_stories']:
        print("\n✅ All specs are properly linked!")


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1]
    
    if command in ["--help", "-h"]:
        print_help()
        return
    
    if command == "--status":
        show_status()
        return
    
    if command == "--validate":
        processor = PromptToProductSchema()
        result = processor.process_prompt("validate links")
        
        if result["success"]:
            validation = result["validation"]
            print("✅ Validation completed successfully!")
            print(f"Found {len(validation['epics'])} epics, {len(validation['features'])} features, {len(validation['stories'])} stories")
            
            if validation['orphaned_features'] or validation['orphaned_stories']:
                print("\n⚠️  Issues found:")
                for orphan in validation['orphaned_features']:
                    print(f"   Feature {orphan['feature']} references missing epic {orphan['missing_epic']}")
                for orphan in validation['orphaned_stories']:
                    print(f"   Story {orphan['story']} references missing feature {orphan['missing_feature']}")
            else:
                print("✅ All specs are properly linked!")
        else:
            print(f"❌ Validation failed: {result['error']}")
        return
    
    # Process as a prompt
    if command.startswith("--"):
        print(f"Unknown command: {command}")
        print_help()
        return
    
    prompt = " ".join(sys.argv[1:])
    processor = PromptToProductSchema()
    
    print(f"🔄 Processing: {prompt}")
    print("-" * 50)
    
    result = processor.process_prompt(prompt)
    
    if result["success"]:
        if result.get("file_created"):
            print(f"✅ Success! Created: {result['file_created']}")
            # Show file content preview
            try:
                with open(result['file_created'], 'r') as f:
                    lines = f.readlines()[:10]  # First 10 lines
                print("\n📄 File preview:")
                for line in lines:
                    print(f"   {line.rstrip()}")
                if len(lines) == 10:
                    print("   ...")
            except Exception:
                pass
        elif result.get("validation"):
            show_status()
    else:
        print(f"❌ Error: {result['error']}")


if __name__ == "__main__":
    main()