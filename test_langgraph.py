#!/usr/bin/env python3
"""
Test script for LangGraph integration
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Test the LangGraph system
try:
    from prompttoproduct import PromptToProduct
    
    print("🚀 Testing LangGraph PromptToProduct System...")
    
    # Initialize system
    system = PromptToProduct()
    
    # Test status
    print("\n📊 System Status:")
    status = system.get_status()
    print(f"System: {status['system']}")
    print(f"Version: {status['version']}")
    print(f"Orchestration: {status['orchestration']}")
    print(f"Agents: {len(status['agents'])} available")
    
    # Test simple prompt
    print("\n🧪 Testing with simple prompt...")
    result = system.process_prompt("Create a basic user authentication system")
    
    print(f"\n✅ Test completed!")
    print(f"Status: {result.get('status', 'unknown')}")
    print(f"Workflow ID: {result.get('workflow_id', 'unknown')}")
    
    if result.get('status') == 'completed':
        print("🎉 LangGraph workflow executed successfully!")
        results = result.get('results', {})
        
        if results.get('orchestrator'):
            print(f"  Orchestrator: ✅ Intent = {result.get('intent', 'unknown')}")
        if results.get('spec_agent'):
            print(f"  Spec Agent: ✅ Type = {results['spec_agent'].get('spec_type', 'unknown')}")
        if results.get('validation'):
            print(f"  Validation: ✅ Score = {results['validation'].get('overall_score', 0.0):.2f}")
        if results.get('project'):
            print(f"  Project: ✅ Issues = {len(results['project'].get('created_issues', []))}")
    else:
        print(f"❌ Workflow failed: {result.get('last_error', 'Unknown error')}")
    
    print("\n🎯 LangGraph integration test completed!")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()