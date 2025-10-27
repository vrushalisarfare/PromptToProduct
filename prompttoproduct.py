#!/usr/bin/env python3
"""
PromptToProduct - Complete Agent Orchestration System

Main CLI interface for the 4-agent system that converts natural language 
prompts into complete banking software specifications and implementations.

Usage:
    python prompttoproduct.py "Create a credit card fraud detection system"
    python prompttoproduct.py --status
    python prompttoproduct.py --validate-all
    python prompttoproduct.py --agent orchestrator "Route banking loan requests"
"""
import sys
import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import argparse

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import all agents
try:
    from src.agents.orchestrator import PromptOrchestrator
    from src.agents.spec_agent import SpecAgent  
    from src.agents.code_agent import CodeAgent
    from src.agents.validation_agent import ValidationAgent
except ImportError as e:
    print(f"❌ Error importing agents: {e}")
    print("Ensure all agent files are present in src/agents/")
    sys.exit(1)

class PromptToProduct:
    """
    Main orchestration system for the PromptToProduct workflow.
    
    Coordinates all four agents to provide complete prompt-to-code workflow:
    1. Orchestrator - Routes prompts to appropriate agents
    2. Spec Agent - Generates markdown specifications  
    3. Code Agent - Creates Python implementations
    4. Validation Agent - Validates specs and syncs with GitHub
    """
    
    def __init__(self):
        """Initialize the complete system."""
        self.version = "1.0.0"
        self.system_name = "PromptToProduct"
        
        # Initialize all agents
        print("🚀 Initializing PromptToProduct System...")
        self.orchestrator = PromptOrchestrator()
        self.spec_agent = SpecAgent()
        self.code_agent = CodeAgent()
        self.validation_agent = ValidationAgent()
        
        # System state tracking
        self.session_history = []
        self.active_agents = {
            "orchestrator": True,
            "spec-agent": True, 
            "code-agent": True,
            "validation-agent": True
        }
        
        print("✅ All agents initialized successfully")
    
    def process_prompt(self, prompt: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Main entry point for processing natural language prompts.
        
        Args:
            prompt: Natural language prompt from user
            options: Additional processing options
            
        Returns:
            Complete processing result from all relevant agents
        """
        options = options or {}
        
        print(f"\n🎯 Processing Prompt: {prompt}")
        print("=" * 80)
        
        # Initialize session result
        session_result = {
            "session_id": f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "input_prompt": prompt,
            "processing_timestamp": datetime.now().isoformat(),
            "options": options,
            "agents_involved": [],
            "orchestrator_result": None,
            "spec_result": None,
            "code_result": None,
            "validation_result": None,
            "overall_status": "processing",
            "execution_summary": {},
            "errors": []
        }
        
        try:
            # Step 1: Orchestrator analysis and routing
            print("\n🎼 Step 1: Orchestrator Analysis")
            print("-" * 40)
            
            orchestrator_result = self.orchestrator.classify_prompt(prompt)
            
            # Transform to expected format for compatibility
            session_result["orchestrator_result"] = orchestrator_result
            session_result["agents_involved"] = [orchestrator_result.get("target_agent", "spec-agent")]
            
            print(f"🎯 Intent: {orchestrator_result.get('intent', 'unknown')}")
            print(f"🏦 Banking Context: {orchestrator_result.get('banking_context', {}).get('is_banking', False)}")
            print(f"📋 Target Agent: {orchestrator_result.get('target_agent', 'spec-agent')}")
            
            # Step 2: Spec Agent (if recommended)
            if "spec-agent" in session_result["agents_involved"]:
                print(f"\n📝 Step 2: Specification Generation")
                print("-" * 40)
                
                # Map orchestrator result to spec agent format
                spec_params = {
                    "prompt": orchestrator_result.get("original_prompt", prompt),
                    "intent": orchestrator_result.get("intent", ""),
                    "banking_context": orchestrator_result.get("banking_context", {}),
                    "entities": orchestrator_result.get("entities", {})
                }
                
                spec_result = self.spec_agent.process_specification_request(spec_params)
                session_result["spec_result"] = spec_result
                
                print(f"📄 Generated: {spec_result.get('generation_type', 'unknown')}")
                print(f"💾 Files: {len(spec_result.get('created_files', []))} created")
            
            # Step 3: Code Agent (if recommended)
            if "code-agent" in session_result["agents_involved"]:
                print(f"\n💻 Step 3: Code Generation")
                print("-" * 40)
                
                code_result = self.code_agent.generate_code_from_specs(orchestrator_result)
                session_result["code_result"] = code_result
                
                print(f"⚙️ Generated: {code_result.get('generation_type', 'unknown')}")
                print(f"📁 Files: {len(code_result.get('generated_files', []))} created")
            
            # Step 4: Validation Agent (if requested or specs were generated)
            should_validate = (
                "validation-agent" in session_result["agents_involved"] or
                options.get("auto_validate", True) and session_result.get("spec_result")
            )
            
            if should_validate:
                print(f"\n✅ Step 4: Validation & Sync")
                print("-" * 40)
                
                # Prepare validation parameters
                validation_params = orchestrator_result.copy()
                validation_params.update({
                    "spec_type": "validate_all",
                    "sync_github": options.get("sync_github", False)
                })
                
                validation_result = self.validation_agent.validate_specifications(validation_params)
                session_result["validation_result"] = validation_result
                
                print(f"📊 Overall Score: {validation_result.get('overall_score', 0.0):.2f}/1.00")
                print(f"🔄 GitHub Sync: {validation_result.get('github_sync_status', {}).get('status', 'not_performed')}")
            
            # Generate execution summary
            session_result["execution_summary"] = self._generate_execution_summary(session_result)
            session_result["overall_status"] = "completed"
            
        except Exception as e:
            session_result["overall_status"] = "error"
            session_result["errors"].append(str(e))
            session_result["execution_summary"] = {
                "agents_executed": 0,
                "total_files_created": 0,
                "banking_features_detected": 0,
                "validation_score": 0.0,
                "github_integration": False,
                "processing_time": "< 1 minute",
                "recommendations": [f"Error occurred: {str(e)}"]
            }
            print(f"❌ System Error: {e}")
        
        # Add to session history
        self.session_history.append(session_result)
        
        # Display final summary
        self._display_session_summary(session_result)
        
        return session_result
    
    def _generate_execution_summary(self, session_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive execution summary."""
        summary = {
            "agents_executed": len(session_result["agents_involved"]),
            "total_files_created": 0,
            "banking_features_detected": 0,
            "validation_score": 0.0,
            "github_integration": False,
            "processing_time": "< 1 minute",
            "recommendations": []
        }
        
        # Count files created
        if session_result.get("spec_result"):
            summary["total_files_created"] += len(session_result["spec_result"].get("created_files", []))
        
        if session_result.get("code_result"):
            summary["total_files_created"] += len(session_result["code_result"].get("generated_files", []))
        
        # Banking features
        orchestrator_result = session_result.get("orchestrator_result", {})
        banking_context = orchestrator_result.get("banking_context", {})
        if banking_context.get("is_banking"):
            summary["banking_features_detected"] = len(banking_context.get("product_types", []))
        
        # Validation score
        if session_result.get("validation_result"):
            summary["validation_score"] = session_result["validation_result"].get("overall_score", 0.0)
        
        # GitHub integration
        if session_result.get("validation_result", {}).get("github_sync_status"):
            summary["github_integration"] = True
        
        # Generate recommendations
        summary["recommendations"] = self._generate_system_recommendations(session_result)
        
        return summary
    
    def _generate_system_recommendations(self, session_result: Dict[str, Any]) -> List[str]:
        """Generate system-level recommendations."""
        recommendations = []
        
        # Based on agents involved
        agents_involved = session_result.get("agents_involved", [])
        
        if "spec-agent" in agents_involved and "code-agent" not in agents_involved:
            recommendations.append("Consider running code generation to implement the specifications")
        
        if "code-agent" in agents_involved and session_result.get("validation_result", {}).get("overall_score", 1.0) < 0.7:
            recommendations.append("Improve specification quality before generating more code")
        
        # Based on banking context
        orchestrator_result = session_result.get("orchestrator_result", {})
        if orchestrator_result.get("banking_context", {}).get("is_banking"):
            if not orchestrator_result.get("banking_context", {}).get("compliance_areas"):
                recommendations.append("Consider adding compliance requirements for banking features")
        
        # Based on validation results
        if session_result.get("validation_result"):
            val_recommendations = session_result["validation_result"].get("recommendations", [])
            recommendations.extend(val_recommendations[:2])  # Add top 2 validation recommendations
        
        return recommendations[:5]  # Limit to top 5
    
    def _display_session_summary(self, session_result: Dict[str, Any]):
        """Display comprehensive session summary."""
        print(f"\n🎯 PromptToProduct Session Summary")
        print("=" * 80)
        
        summary = session_result["execution_summary"]
        
        print(f"📋 Session ID: {session_result['session_id']}")
        print(f"📊 Status: {session_result['overall_status']}")
        print(f"⚙️ Agents Executed: {summary['agents_executed']}")
        print(f"📁 Files Created: {summary['total_files_created']}")
        
        if summary["banking_features_detected"]:
            print(f"🏦 Banking Features: {summary['banking_features_detected']} detected")
        
        if summary["validation_score"] > 0:
            print(f"✅ Validation Score: {summary['validation_score']:.2f}/1.00")
        
        if summary["github_integration"]:
            print(f"🔄 GitHub: Synchronized")
        
        # Show errors if any
        if session_result.get("errors"):
            print(f"\n❌ Errors ({len(session_result['errors'])}):")
            for error in session_result["errors"]:
                print(f"   • {error}")
        
        # Show recommendations
        if summary.get("recommendations"):
            print(f"\n💡 Recommendations:")
            for i, rec in enumerate(summary["recommendations"], 1):
                print(f"   {i}. {rec}")
        
        print(f"\n🕒 Processing Time: {summary['processing_time']}")
        print("=" * 80)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        return {
            "system_name": self.system_name,
            "version": self.version,
            "agents": {
                "orchestrator": self.orchestrator.get_orchestrator_status(),
                "spec_agent": self.spec_agent.get_spec_agent_status(),
                "code_agent": self.code_agent.get_code_agent_status(),
                "validation_agent": self.validation_agent.get_validation_agent_status()
            },
            "session_history": len(self.session_history),
            "active_agents": self.active_agents,
            "system_health": "operational"
        }
    
    def validate_all_specs(self) -> Dict[str, Any]:
        """Validate all specifications in the workspace."""
        print("🔍 Validating All Specifications...")
        
        validation_params = {
            "prompt": "validate all specifications",
            "spec_type": "validate_all",
            "banking_context": {"is_banking": True},
            "sync_github": False
        }
        
        return self.validation_agent.validate_specifications(validation_params)
    
    def run_specific_agent(self, agent_name: str, prompt: str) -> Dict[str, Any]:
        """Run a specific agent directly."""
        print(f"🔧 Running {agent_name} directly...")
        
        if agent_name == "orchestrator":
            return self.orchestrator.classify_prompt(prompt)
        elif agent_name == "spec-agent":
            # Need orchestrator context first
            context = self.orchestrator.classify_prompt(prompt)
            return self.spec_agent.process_specification_request(context)
        elif agent_name == "code-agent":
            context = self.orchestrator.classify_prompt(prompt)
            return self.code_agent.generate_code_from_specs(context)
        elif agent_name == "validation-agent":
            return self.validation_agent.validate_specifications({
                "prompt": prompt,
                "spec_type": "validate_all"
            })
        else:
            raise ValueError(f"Unknown agent: {agent_name}")


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="PromptToProduct - Complete Agent Orchestration System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python prompttoproduct.py "Create a credit card fraud detection system"
  python prompttoproduct.py "Build a loan application API" --sync-github
  python prompttoproduct.py --status
  python prompttoproduct.py --validate-all
  python prompttoproduct.py --agent orchestrator "Route banking requests"
        """
    )
    
    # Main arguments
    parser.add_argument("prompt", nargs="?", help="Natural language prompt to process")
    
    # System actions
    parser.add_argument("--status", action="store_true", help="Show system status")
    parser.add_argument("--validate-all", action="store_true", help="Validate all specifications")
    
    # Agent-specific actions
    parser.add_argument("--agent", choices=["orchestrator", "spec-agent", "code-agent", "validation-agent"],
                       help="Run specific agent directly")
    
    # Processing options
    parser.add_argument("--sync-github", action="store_true", help="Sync results with GitHub")
    parser.add_argument("--no-validate", action="store_true", help="Skip automatic validation")
    parser.add_argument("--banking-context", action="store_true", default=True, help="Force banking context")
    
    # Output options
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Initialize system
    try:
        system = PromptToProduct()
    except Exception as e:
        print(f"❌ Failed to initialize PromptToProduct system: {e}")
        sys.exit(1)
    
    # Handle status request
    if args.status:
        status = system.get_system_status()
        if args.json:
            print(json.dumps(status, indent=2, default=str))
        else:
            print("🚀 PromptToProduct System Status")
            print("=" * 50)
            print(f"Version: {status['version']}")
            print(f"System Health: {status['system_health']}")
            print(f"Sessions: {status['session_history']}")
            print(f"Active Agents: {', '.join([k for k, v in status['active_agents'].items() if v])}")
        return
    
    # Handle validate-all request  
    if args.validate_all:
        result = system.validate_all_specs()
        if args.json:
            print(json.dumps(result, indent=2, default=str))
        return
    
    # Handle specific agent request
    if args.agent:
        if not args.prompt:
            print("❌ Prompt required when using --agent")
            sys.exit(1)
        
        result = system.run_specific_agent(args.agent, args.prompt)
        if args.json:
            print(json.dumps(result, indent=2, default=str))
        return
    
    # Handle main prompt processing
    if not args.prompt:
        parser.print_help()
        return
    
    # Prepare processing options
    options = {
        "sync_github": args.sync_github,
        "auto_validate": not args.no_validate,
        "banking_context": args.banking_context,
        "verbose": args.verbose
    }
    
    # Process the prompt
    result = system.process_prompt(args.prompt, options)
    
    # Output result
    if args.json:
        print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()