#!/usr/bin/env python3
"""
PromptToProduct - LangGraph Agent Orchestration System

A complete system for transforming natural language prompts into structured
specifications (epics, features, stories) and implementation code for MyBank.

Orchestrated using LangGraph for stateful workflow management with:
- Conditional routing based on results
- Error handling and retry logic  
- Parallel execution where possible
- Comprehensive workflow tracking

Usage:
    python prompttoproduct.py "Create a fraud detection system"
"""
import sys
import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, TypedDict, Annotated
from datetime import datetime
import argparse

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import LangGraph dependencies
try:
    from langgraph.graph import StateGraph, END
    from langgraph.graph.message import AnyMessage, add_messages
    from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
    LANGGRAPH_AVAILABLE = True
except ImportError as e:
    print(f"❌ LangGraph not available: {e}")
    print("Install with: pip install langgraph langchain langchain-core")
    sys.exit(1)

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


class WorkflowState(TypedDict):
    """State management for LangGraph workflow."""
    messages: Annotated[List[AnyMessage], add_messages]
    prompt: str
    intent: str
    banking_context: Dict[str, Any]
    entities: Dict[str, Any]
    orchestrator_result: Optional[Dict[str, Any]]
    spec_result: Optional[Dict[str, Any]]
    code_result: Optional[Dict[str, Any]]
    validation_result: Optional[Dict[str, Any]]
    project_result: Optional[Dict[str, Any]]
    workflow_status: str
    error_count: int
    retry_count: int
    final_result: Optional[Dict[str, Any]]


class PromptToProduct:
    """
    LangGraph-based orchestrator for PromptToProduct system.
    
    Provides:
    - Stateful workflow management with LangGraph
    - Conditional routing based on results
    - Error handling and retry logic
    - Parallel agent execution where possible
    - Comprehensive workflow tracking
    """
    
    def __init__(self):
        """Initialize LangGraph orchestrator."""
        print("🚀 Initializing PromptToProduct with LangGraph orchestration...")
        
        # Initialize existing agents
        self.orchestrator = PromptOrchestrator()
        self.spec_agent = SpecAgent()
        self.code_agent = CodeAgent()
        self.validation_agent = ValidationAgent()
        
        # Create workflow graph
        self.workflow = self._create_workflow()
        print("✅ LangGraph workflow initialized")
        
    def _create_workflow(self) -> StateGraph:
        """Create the LangGraph workflow."""
        workflow = StateGraph(WorkflowState)
        
        # Add nodes
        workflow.add_node("orchestrator", self._orchestrator_node)
        workflow.add_node("spec_agent", self._spec_agent_node)
        workflow.add_node("code_agent", self._code_agent_node)
        workflow.add_node("validation_agent", self._validation_agent_node)
        workflow.add_node("finalize", self._finalize_node)
        workflow.add_node("error_handler", self._error_handler_node)
        
        # Set entry point
        workflow.set_entry_point("orchestrator")
        
        # Add edges with conditional routing
        workflow.add_conditional_edges(
            "orchestrator",
            self._route_after_orchestrator,
            {
                "spec_agent": "spec_agent",
                "code_agent": "code_agent",
                "error": "error_handler"
            }
        )
        
        workflow.add_conditional_edges(
            "spec_agent",
            self._route_after_spec,
            {
                "validation_agent": "validation_agent",
                "error": "error_handler",
                "retry": "spec_agent"
            }
        )
        
        workflow.add_conditional_edges(
            "validation_agent",
            self._route_after_validation,
            {
                "finalize": "finalize",
                "spec_agent": "spec_agent",  # Retry if validation fails
                "error": "error_handler"
            }
        )
        
        workflow.add_conditional_edges(
            "code_agent",
            self._route_after_code,
            {
                "validation_agent": "validation_agent",
                "finalize": "finalize",
                "error": "error_handler"
            }
        )
        
        workflow.add_edge("finalize", END)
        workflow.add_edge("error_handler", END)
        
        return workflow.compile()
    
    def _orchestrator_node(self, state: WorkflowState) -> WorkflowState:
        """Orchestrator node - analyze prompt and determine routing."""
        try:
            print("🎯 LangGraph Orchestrator: Analyzing prompt...")
            
            result = self.orchestrator.classify_prompt(state["prompt"])
            
            # Update state
            state["intent"] = result.get("intent", "unknown")
            state["banking_context"] = result.get("banking_context", {})
            state["entities"] = result.get("entities", {})
            state["orchestrator_result"] = result
            state["workflow_status"] = "orchestration_complete"
            
            # Add message
            state["messages"].append(
                AIMessage(content=f"Analyzed prompt with intent: {state['intent']}")
            )
            
            print(f"✅ Intent classified as: {state['intent']}")
            
        except Exception as e:
            print(f"❌ Orchestrator error: {e}")
            state["workflow_status"] = "error"
            state["error_count"] += 1
            state["messages"].append(
                AIMessage(content=f"Orchestrator error: {e}")
            )
        
        return state
    
    def _spec_agent_node(self, state: WorkflowState) -> WorkflowState:
        """Spec agent node - generate specifications."""
        try:
            print("📋 LangGraph: Generating specifications...")
            
            agent_params = {
                "prompt": state["prompt"],
                "intent": state["intent"],
                "banking_context": state["banking_context"],
                "entities": state["entities"]
            }
            
            result = self.spec_agent.process_specification_request(agent_params)
            
            state["spec_result"] = result
            state["workflow_status"] = "spec_complete"
            
            state["messages"].append(
                AIMessage(content=f"Generated specification: {result.get('spec_type', 'unknown')}")
            )
            
            print(f"✅ Generated {result.get('spec_type', 'unknown')} specification")
            
        except Exception as e:
            print(f"❌ Spec agent error: {e}")
            state["workflow_status"] = "error"
            state["error_count"] += 1
            state["messages"].append(
                AIMessage(content=f"Spec agent error: {e}")
            )
        
        return state
    
    def _code_agent_node(self, state: WorkflowState) -> WorkflowState:
        """Code agent node - generate implementation code."""
        try:
            print("🔧 LangGraph: Generating code implementation...")
            
            agent_params = {
                "prompt": state["prompt"],
                "banking_context": state["banking_context"],
                "entities": state["entities"]
            }
            
            result = self.code_agent.generate_code_from_specs(agent_params)
            
            state["code_result"] = result
            state["workflow_status"] = "code_complete"
            
            state["messages"].append(
                AIMessage(content=f"Generated code files: {len(result.get('generated_files', []))}")
            )
            
            print(f"✅ Generated {len(result.get('generated_files', []))} code files")
            
        except Exception as e:
            print(f"❌ Code agent error: {e}")
            state["workflow_status"] = "error"
            state["error_count"] += 1
            state["messages"].append(
                AIMessage(content=f"Code agent error: {e}")
            )
        
        return state
    
    def _validation_agent_node(self, state: WorkflowState) -> WorkflowState:
        """Validation agent node - validate specifications and code."""
        try:
            print("🔍 LangGraph: Validating specifications...")
            
            agent_params = {
                "prompt": state["prompt"],
                "validate_all": True
            }
            
            result = self.validation_agent.validate_specifications(agent_params)
            
            state["validation_result"] = result
            state["workflow_status"] = "validation_complete"
            
            validation_score = result.get("overall_score", 0.0)
            state["messages"].append(
                AIMessage(content=f"Validation completed with score: {validation_score:.2f}")
            )
            
            print(f"✅ Validation score: {validation_score:.2f}")
            
        except Exception as e:
            print(f"❌ Validation agent error: {e}")
            state["workflow_status"] = "error"
            state["error_count"] += 1
            state["messages"].append(
                AIMessage(content=f"Validation agent error: {e}")
            )
        
        return state
    
    def _finalize_node(self, state: WorkflowState) -> WorkflowState:
        """Finalize workflow - compile final results."""
        print("🎉 LangGraph: Finalizing workflow...")
        
        state["final_result"] = {
            "workflow_id": f"langraph_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "status": "completed",
            "prompt": state["prompt"],
            "intent": state["intent"],
            "results": {
                "orchestrator": state.get("orchestrator_result"),
                "spec_agent": state.get("spec_result"),
                "code_agent": state.get("code_result"),
                "validation": state.get("validation_result"),
                "project": state.get("project_result")
            },
            "workflow_status": state["workflow_status"],
            "error_count": state["error_count"],
            "retry_count": state["retry_count"],
            "completion_time": datetime.now().isoformat()
        }
        
        state["messages"].append(
            AIMessage(content="Workflow completed successfully")
        )
        
        print("✅ LangGraph workflow completed")
        
        return state
    
    def _error_handler_node(self, state: WorkflowState) -> WorkflowState:
        """Error handler node - manage errors and retries."""
        print(f"⚠️ LangGraph: Handling error (count: {state['error_count']})")
        
        if state["error_count"] >= 3:
            print("❌ Maximum errors reached, terminating workflow")
            state["workflow_status"] = "failed"
            state["final_result"] = {
                "status": "failed",
                "error_count": state["error_count"],
                "last_error": state.get("messages", [])[-1].content if state.get("messages") else "Unknown error"
            }
        else:
            print(f"🔄 Preparing retry (attempt {state['retry_count'] + 1})")
            state["retry_count"] += 1
            state["workflow_status"] = "retrying"
        
        return state
    
    def _route_after_orchestrator(self, state: WorkflowState) -> str:
        """Route after orchestrator based on intent."""
        if state["workflow_status"] == "error":
            return "error"
        
        intent = state.get("intent", "")
        
        if intent in ["create_epic", "create_feature", "create_story", "spec_generation"]:
            return "spec_agent"
        elif intent in ["code_generation", "implement_feature"]:
            return "code_agent"
        else:
            return "spec_agent"  # Default to spec agent
    
    def _route_after_spec(self, state: WorkflowState) -> str:
        """Route after spec agent."""
        if state["workflow_status"] == "error":
            if state["retry_count"] < 2:
                return "retry"
            return "error"
        
        return "validation_agent"
    
    def _route_after_validation(self, state: WorkflowState) -> str:
        """Route after validation agent."""
        if state["workflow_status"] == "error":
            return "error"
        
        validation_result = state.get("validation_result", {})
        score = validation_result.get("overall_score", 0.0)
        
        if score < 0.7 and state["retry_count"] < 2:
            print(f"🔄 Validation score {score:.2f} too low, retrying spec generation")
            state["retry_count"] += 1
            return "spec_agent"
        
        return "finalize"
    
    def _route_after_code(self, state: WorkflowState) -> str:
        """Route after code agent."""
        if state["workflow_status"] == "error":
            return "error"
        
        # Check if we need validation
        code_result = state.get("code_result", {})
        if code_result.get("generated_files"):
            return "validation_agent"
        
        return "finalize"
    
    def process_prompt(self, prompt: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Main entry point for processing prompts with LangGraph workflow.
        
        Args:
            prompt: User prompt to process
            options: Additional processing options
            
        Returns:
            Complete workflow result
        """
        print(f"🚀 Starting LangGraph workflow for: {prompt}")
        
        # Initialize state
        initial_state = WorkflowState(
            messages=[HumanMessage(content=prompt)],
            prompt=prompt,
            intent="",
            banking_context={},
            entities={},
            orchestrator_result=None,
            spec_result=None,
            code_result=None,
            validation_result=None,
            project_result=None,
            workflow_status="started",
            error_count=0,
            retry_count=0,
            final_result=None
        )
        
        try:
            # Execute workflow
            final_state = self.workflow.invoke(initial_state)
            
            # Return final result
            return final_state.get("final_result", {
                "status": "error",
                "message": "Workflow completed but no final result generated"
            })
            
        except Exception as e:
            print(f"❌ LangGraph workflow error: {e}")
            return {
                "status": "error",
                "error": str(e),
                "workflow_id": f"langraph_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get system status information."""
        return {
            "system": "PromptToProduct LangGraph",
            "version": "2.0.0",
            "orchestration": "LangGraph-based",
            "agents": {
                "orchestrator": "✅ Available",
                "spec_agent": "✅ Available", 
                "code_agent": "✅ Available",
                "validation_agent": "✅ Available"
            },
            "langgraph": "✅ Available",
            "workflow_nodes": 6,
            "timestamp": datetime.now().isoformat()
        }


def main():
    """Main entry point for the PromptToProduct CLI."""
    parser = argparse.ArgumentParser(
        description="PromptToProduct - LangGraph Agent Orchestration System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python prompttoproduct.py "Create a fraud detection system"
  python prompttoproduct.py --status
  python prompttoproduct.py --help
        """
    )
    
    parser.add_argument(
        "prompt", 
        nargs="?", 
        help="Natural language prompt to process"
    )
    
    parser.add_argument(
        "--status", 
        action="store_true", 
        help="Show system status"
    )
    
    parser.add_argument(
        "--json", 
        action="store_true", 
        help="Output results in JSON format"
    )
    
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize PromptToProduct system
        system = PromptToProduct()
        
        # Handle status request
        if args.status:
            status = system.get_status()
            if args.json:
                print(json.dumps(status, indent=2))
            else:
                print("\n🎯 PROMPTTOPRODUCT LANGGRAPH SYSTEM STATUS")
                print("=" * 60)
                print(f"System: {status['system']}")
                print(f"Version: {status['version']}")
                print(f"Orchestration: {status['orchestration']}")
                print(f"Workflow Nodes: {status['workflow_nodes']}")
                print("\nAgent Status:")
                for agent, status_text in status['agents'].items():
                    print(f"  {agent}: {status_text}")
                print(f"\nLangGraph: {status['langgraph']}")
                print(f"Timestamp: {status['timestamp']}")
            return
        
        # Handle prompt processing
        if not args.prompt:
            parser.print_help()
            return
        
        print(f"\n🚀 PROMPTTOPRODUCT LANGGRAPH WORKFLOW")
        print("=" * 60)
        print(f"Prompt: {args.prompt}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Process prompt with LangGraph workflow
        result = system.process_prompt(args.prompt)
        
        # Output results
        if args.json:
            print(json.dumps(result, indent=2, default=str))
        else:
            print("\n🎉 WORKFLOW RESULTS")
            print("=" * 60)
            print(f"Status: {result.get('status', 'unknown')}")
            print(f"Workflow ID: {result.get('workflow_id', 'unknown')}")
            
            if result.get('status') == 'completed':
                print(f"Intent: {result.get('intent', 'unknown')}")
                
                results = result.get('results', {})
                
                # Orchestrator results
                if results.get('orchestrator'):
                    print("\n📋 Orchestrator Results:")
                    print(f"  Banking Context: {results['orchestrator'].get('banking_context', {}).get('is_banking', False)}")
                
                # Spec agent results  
                if results.get('spec_agent'):
                    spec_result = results['spec_agent']
                    print(f"\n📄 Specification Results:")
                    print(f"  Type: {spec_result.get('spec_type', 'unknown')}")
                    print(f"  Files Created: {len(spec_result.get('created_files', []))}")
                
                # Code agent results
                if results.get('code_agent'):
                    code_result = results['code_agent']
                    print(f"\n🔧 Code Generation Results:")
                    print(f"  Files Generated: {len(code_result.get('generated_files', []))}")
                
                # Validation results
                if results.get('validation'):
                    validation_result = results['validation']
                    print(f"\n🔍 Validation Results:")
                    print(f"  Overall Score: {validation_result.get('overall_score', 0.0):.2f}")
                
                # Project results
                if results.get('project'):
                    project_result = results['project']
                    print(f"\n🚀 GitHub Project Results:")
                    print(f"  Issues Created: {len(project_result.get('created_issues', []))}")
                
                print(f"\nCompletion Time: {result.get('completion_time', 'unknown')}")
                print(f"Error Count: {result.get('error_count', 0)}")
                print(f"Retry Count: {result.get('retry_count', 0)}")
            
            elif result.get('status') == 'failed':
                print(f"Error Count: {result.get('error_count', 0)}")
                print(f"Last Error: {result.get('last_error', 'Unknown')}")
            
            print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n⚠️ Process interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()