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
    from src.agents.project_agent import ProjectAgent
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
        self.project_agent = ProjectAgent()
        
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
        workflow.add_node("project_agent", self._project_agent_node)
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
                "project_agent": "project_agent",
                "spec_agent": "spec_agent",  # Retry if validation fails
                "error": "error_handler"
            }
        )
        
        workflow.add_conditional_edges(
            "code_agent",
            self._route_after_code,
            {
                "validation_agent": "validation_agent",
                "project_agent": "project_agent",
                "error": "error_handler"
            }
        )
        
        workflow.add_conditional_edges(
            "project_agent",
            self._route_after_project,
            {
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
            
            result = self.spec_agent.create_spec_from_prompt(agent_params)
            
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
            
            result = self.validation_agent.validate_specs(agent_params)
            
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
    
    def _project_agent_node(self, state: WorkflowState) -> WorkflowState:
        """Project agent node - sync with GitHub Projects."""
        try:
            print("🚀 LangGraph: Syncing with GitHub Projects...")
            
            agent_params = {
                "prompt": state["prompt"],
                "created_specs": state.get("spec_result", {}).get("created_files", [])
            }
            
            result = self.project_agent.sync_specs_to_project(agent_params)
            
            state["project_result"] = result
            state["workflow_status"] = "project_complete"
            
            created_issues = len(result.get("created_issues", []))
            state["messages"].append(
                AIMessage(content=f"Created {created_issues} GitHub issues")
            )
            
            print(f"✅ Created {created_issues} GitHub issues")
            
        except Exception as e:
            print(f"❌ Project agent error: {e}")
            state["workflow_status"] = "error"
            state["error_count"] += 1
            state["messages"].append(
                AIMessage(content=f"Project agent error: {e}")
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
        
        return "project_agent"
    
    def _route_after_code(self, state: WorkflowState) -> str:
        """Route after code agent."""
        if state["workflow_status"] == "error":
            return "error"
        
        # Check if we need validation
        code_result = state.get("code_result", {})
        if code_result.get("generated_files"):
            return "validation_agent"
        
        return "project_agent"
    
    def _route_after_project(self, state: WorkflowState) -> str:
        """Route after project agent."""
        if state["workflow_status"] == "error":
            return "error"
        
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
                "validation_agent": "✅ Available",
                "project_agent": "✅ Available"
            },
            "langgraph": "✅ Available",
            "workflow_nodes": 7,
            "timestamp": datetime.now().isoformat()

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
            "project_result": None,
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
            
            # Step 4: Validation Agent (always run for quality assessment)
            should_validate = (
                "validation-agent" in session_result["agents_involved"] or
                options.get("auto_validate", True) and session_result.get("spec_result")
            )
            
            if should_validate:
                print(f"\n✅ Step 4: Quality Validation")
                print("-" * 40)
                
                # Prepare validation parameters (focused on quality only)
                validation_params = orchestrator_result.copy()
                validation_params.update({
                    "spec_type": "validate_all",
                    "sync_github": False  # ProjectAgent handles GitHub integration
                })
                
                validation_result = self.validation_agent.validate_specifications(validation_params)
                session_result["validation_result"] = validation_result
                
                print(f"📊 Overall Score: {validation_result.get('overall_score', 0.0):.2f}/1.00")
                print(f"� Specs Validated: {len(validation_result.get('validation_results', []))}")
                
            # Step 5: Project Agent (for GitHub Projects integration)
            should_sync_github = options.get("sync_github", False)
            
            if should_sync_github and session_result.get("spec_result"):
                print(f"\n🔗 Step 5: GitHub Projects Integration")
                print("-" * 40)
                
                # Get spec results from spec agent
                spec_created_files = session_result["spec_result"].get("created_files", [])
                if spec_created_files:
                    # Transform spec results for ProjectAgent
                    spec_results_for_project = []
                    
                    # Handle the case where created_files contains file paths as strings
                    for file_info in spec_created_files:
                        if isinstance(file_info, str):
                            # Extract info from file path string
                            file_path = file_info
                            file_name = Path(file_path).name
                            
                            # Determine spec type from file path
                            if "/epics/" in file_path or "\\epics\\" in file_path:
                                spec_type = "epic"
                            elif "/features/" in file_path or "\\features\\" in file_path:
                                spec_type = "feature"
                            elif "/stories/" in file_path or "\\stories\\" in file_path:
                                spec_type = "story"
                            else:
                                spec_type = "epic"  # default
                            
                            # Extract title from filename
                            title_parts = file_name.replace(".md", "").split("-")[1:]
                            title = " ".join(title_parts).replace("-", " ").title() if title_parts else "Generated Spec"
                            
                            spec_results_for_project.append({
                                "file_path": file_path,
                                "spec_type": spec_type,
                                "title": title,
                                "objective": orchestrator_result.get("intent", ""),
                                "owner": "vrushalisarfare",  # From config
                                "assigned_to": "vrushalisarfare",
                                "priority": "Medium",
                                "status": "In Progress",
                                "banking_domain": orchestrator_result.get("banking_context", {}).get("product_types", ["general"])[0] if orchestrator_result.get("banking_context", {}).get("product_types") else "general",
                                "compliance_requirements": orchestrator_result.get("banking_context", {}).get("compliance_areas", [])
                            })
                        else:
                            # Handle dictionary format (if it exists)
                            spec_results_for_project.append({
                                "file_path": file_info.get("file_path", ""),
                                "spec_type": file_info.get("spec_type", "epic"),
                                "title": file_info.get("title", "Generated Spec"),
                                "objective": orchestrator_result.get("intent", ""),
                                "owner": "vrushalisarfare",
                                "assigned_to": "vrushalisarfare",
                                "priority": "Medium",
                                "status": "In Progress",
                                "banking_domain": orchestrator_result.get("banking_context", {}).get("product_types", ["general"])[0] if orchestrator_result.get("banking_context", {}).get("product_types") else "general",
                                "compliance_requirements": orchestrator_result.get("banking_context", {}).get("compliance_areas", [])
                            })
                    
                    project_result = self.project_agent.create_spec_project_items(spec_results_for_project)
                    session_result["project_result"] = project_result
                    
                    if project_result.get("success"):
                        print(f"✅ Project Items: {project_result.get('items_created', 0)} created")
                        print(f"📋 Project #{project_result.get('project_number')} in {project_result.get('organization')}")
                    else:
                        print(f"⚠️ GitHub Projects: {project_result.get('reason', 'Integration failed')}")
                        if project_result.get("errors"):
                            print(f"   📋 Errors: {'; '.join(project_result['errors'])}")
                else:
                    print("⚠️ No spec files to sync with GitHub Projects")
            
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
        if session_result.get("project_result", {}).get("success"):
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