#!/usr/bin/env python3
"""
LangGraph Orchestrator - Advanced Agent Workflow Management

This module implements LangGraph-based orchestration for the PromptToProduct system,
providing stateful workflows, conditional routing, and enhanced agent coordination.
"""
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, TypedDict, Annotated
from datetime import datetime

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from langgraph.graph import StateGraph, END
    from langgraph.graph.message import AnyMessage, add_messages
    from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
    from langchain_core.runnables import RunnableLambda
    LANGGRAPH_AVAILABLE = True
except ImportError as e:
    print(f"Warning: LangGraph not available: {e}")
    print("Install with: pip install -r requirements.txt")
    LANGGRAPH_AVAILABLE = False

# Import existing agents
try:
    from src.agents.orchestrator import PromptOrchestrator
    from src.agents.spec_agent import SpecAgent
    from src.agents.code_agent import CodeAgent
    from src.agents.validation_agent import ValidationAgent
    from src.agents.project_agent import ProjectAgent
    from src.config import get_config, get_github_config
    config = get_config()
    github_config = get_github_config()
except ImportError as e:
    print(f"Warning: Could not import existing agents: {e}")


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


class LangGraphOrchestrator:
    """
    LangGraph-based orchestrator for PromptToProduct system.
    
    Provides:
    - Stateful workflow management
    - Conditional routing based on results
    - Error handling and retry logic
    - Parallel agent execution where possible
    - Comprehensive workflow tracking
    """
    
    def __init__(self):
        """Initialize LangGraph orchestrator."""
        if not LANGGRAPH_AVAILABLE:
            raise ImportError("LangGraph is required. Install with: pip install -r requirements.txt")
        
        self.config = config if 'config' in globals() else None
        self.github_config = github_config if 'github_config' in globals() else None
        
        # Initialize existing agents
        self.orchestrator = PromptOrchestrator() if 'PromptOrchestrator' in globals() else None
        self.spec_agent = SpecAgent() if 'SpecAgent' in globals() else None
        self.code_agent = CodeAgent() if 'CodeAgent' in globals() else None
        self.validation_agent = ValidationAgent() if 'ValidationAgent' in globals() else None
        self.project_agent = ProjectAgent() if 'ProjectAgent' in globals() else None
        
        # Create workflow graph
        self.workflow = self._create_workflow()
        
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
            if not self.orchestrator:
                raise ValueError("Orchestrator agent not available")
            
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
            if not self.spec_agent:
                raise ValueError("Spec agent not available")
            
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
            if not self.code_agent:
                raise ValueError("Code agent not available")
            
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
            if not self.validation_agent:
                raise ValueError("Validation agent not available")
            
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
            if not self.project_agent:
                raise ValueError("Project agent not available")
            
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
    
    def process_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Main entry point for processing prompts with LangGraph workflow.
        
        Args:
            prompt: User prompt to process
            
        Returns:
            Complete workflow result
        """
        if not LANGGRAPH_AVAILABLE:
            raise ImportError("LangGraph is required but not available")
        
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


def main():
    """Test the LangGraph orchestrator."""
    if len(sys.argv) < 2:
        print("Usage: python langgraph_orchestrator.py <prompt>")
        sys.exit(1)
    
    prompt = " ".join(sys.argv[1:])
    
    try:
        orchestrator = LangGraphOrchestrator()
        result = orchestrator.process_prompt(prompt)
        
        print("\n" + "="*80)
        print("🎉 LANGGRAPH WORKFLOW RESULTS")
        print("="*80)
        print(json.dumps(result, indent=2, default=str))
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()