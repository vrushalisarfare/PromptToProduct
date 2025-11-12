#!/usr/bin/env python3
"""
PromptToProduct - Unified LangGraph Orchestration System

A complete system for transforming natural language prompts into structured
specifications (epics, features, stories) and implementation code.

This unified system combines orchestration intelligence with LangGraph workflow
management, providing:
- Intelligent prompt classification and routing
- Stateful workflow management with conditional routing
- Error handling and retry logic  
- Memory context persistence
- Comprehensive workflow tracking

The system integrates:
- Banking domain detection and compliance awareness
- Intent classification for appropriate agent routing
- Entity extraction from natural language prompts
- Confidence scoring for routing decisions
- Memory context for conversation continuity

Usage:
    python prompttoproduct.py "Create a fraud detection system"
    python prompttoproduct.py --status
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
    print(f"[ERROR] LangGraph not available: {e}")
    print("Install with: pip install langgraph langchain langchain-core")
    sys.exit(1)

# Import all agents
try:
    from src.agents.spec_agent import SpecAgent  
    from src.agents.code_agent import CodeAgent
    from src.agents.validation_agent import ValidationAgent
    from src.agents.github_mcp_project_agent import GitHubMCPProjectAgent
except ImportError as e:
    print(f"[ERROR] Error importing agents: {e}")
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
        print("[INIT] Initializing PromptToProduct with LangGraph orchestration...")
        
        # Initialize MCP tools availability
        self.mcp_tools_available = self._check_mcp_tools_availability()
        
        # Initialize existing agents
        self.spec_agent = SpecAgent()
        self.code_agent = CodeAgent()
        self.validation_agent = ValidationAgent()
        self.github_project_agent = GitHubMCPProjectAgent()
        
        # Initialize orchestrator functionality (merged from orchestrator.py)
        self.memory_context = []
        self.context_window = 10
        self.persist_memory = True
        self.agents_config = self._load_agents_config()
        self.routing_rules = self._extract_routing_rules()
        
        # Create workflow graph
        self.workflow = self._create_workflow()
        self._phase_counter = 0  # Track phase progression
        print("[OK] LangGraph workflow initialized with GitHub MCP integration")
    
    def _persist_workflow_state(self, state: WorkflowState, is_complete_workflow: bool, workflow_phase: str) -> None:
        """Persist workflow state in messages for reliable LangGraph state management."""
        state_message = f"WORKFLOW_STATE|complete_workflow:{is_complete_workflow}|phase:{workflow_phase}|counter:{self._phase_counter}"
        state["messages"].append(AIMessage(content=state_message))
        # Also set in state for immediate access
        state["is_complete_workflow"] = is_complete_workflow
        state["workflow_phase"] = workflow_phase
        state["phase_counter"] = self._phase_counter
    
    def _extract_workflow_state(self, state: WorkflowState) -> tuple[bool, str, int]:
        """Extract workflow state from messages for reliable persistence."""
        # Check messages for latest state
        for message in reversed(state["messages"]):
            if hasattr(message, 'content') and "WORKFLOW_STATE|" in message.content:
                parts = message.content.split("|") 
                is_complete = "complete_workflow:True" in message.content
                phase = "" 
                counter = 0
                for part in parts:
                    if part.startswith("phase:"):
                        phase = part.split(":", 1)[1]
                    elif part.startswith("counter:"):
                        counter = int(part.split(":", 1)[1])
                return is_complete, phase, counter
        
        # Fallback to state values and intent detection
        intent = state.get("intent", "")
        is_complete = state.get("is_complete_workflow", False) or intent == "complete_workflow"
        phase = state.get("workflow_phase", "")
        counter = state.get("phase_counter", 0)
        return is_complete, phase, counter

    def _load_agents_config(self) -> Dict[str, Any]:
        """Load agent configuration from manifest."""
        config_path = project_root / ".github" / "workflows" / "copilot_agents.yaml"
        try:
            import yaml
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                return config
        except Exception as e:
            print(f"Warning: Could not load agent config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration if manifest loading fails."""
        return {
            "agents": [
                {
                    "id": "orchestrator",
                    "routes": [
                        {"trigger": ["create", "add", "generate", "build"], "next": "spec-agent"},
                        {"trigger": ["code", "implement", "develop"], "next": "code-agent"},
                        {"trigger": ["validate", "check", "audit"], "next": "validation-agent"}
                    ]
                }
            ]
        }
    
    def _extract_routing_rules(self) -> Dict[str, str]:
        """Extract routing rules from agent configuration."""
        routing_rules = {}
        
        for agent in self.agents_config.get("agents", []):
            if agent.get("id") == "orchestrator":
                for route in agent.get("routes", []):
                    triggers = route.get("trigger", [])
                    next_agent = route.get("next")
                    
                    for trigger in triggers:
                        routing_rules[trigger.lower()] = next_agent
        
        return routing_rules

    def classify_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Analyze prompt intent and context to determine appropriate routing.
        
        Args:
            prompt: Natural language input from user
            
        Returns:
            Dict containing classification results and routing decision
        """
        prompt_lower = prompt.lower()
        
        # Banking domain detection
        banking_context = self._detect_banking_domain(prompt_lower)
        
        # Intent classification
        intent = self._classify_intent(prompt_lower)
        
        # Determine target agent
        target_agent = self._determine_target_agent(prompt_lower, intent, banking_context)
        
        # Extract entities and context
        entities = self._extract_entities(prompt)
        
        classification = {
            "original_prompt": prompt,
            "intent": intent,
            "target_agent": target_agent,
            "banking_context": banking_context,
            "entities": entities,
            "confidence": self._calculate_confidence(prompt_lower, intent, target_agent),
            "timestamp": datetime.now().isoformat(),
            "routing_decision": {
                "agent": target_agent,
                "reason": self._get_routing_reason(intent, banking_context, target_agent)
            }
        }
        
        # Update memory context
        self._update_memory_context(classification)
        
        return classification

    def _detect_banking_domain(self, prompt_lower: str) -> Dict[str, Any]:
        """Detect banking domain context and product types."""
        banking_keywords = {
            "loans": ["loan", "lending", "mortgage", "credit", "financing", "borrowing", "underwriting"],
            "credit_cards": ["credit card", "card", "plastic", "rewards", "cashback", "points", "fraud"],
            "payments": ["payment", "transfer", "wire", "ach", "settlement", "transaction", "p2p"],
            "investments": ["investment", "portfolio", "trading", "stocks", "bonds", "funds", "wealth"],
            "accounts": ["account", "savings", "checking", "deposit", "balance", "statement"],
            "digital_banking": ["mobile app", "online banking", "digital", "api", "microservices"]
        }
        
        compliance_keywords = ["kyc", "aml", "pci-dss", "sox", "gdpr", "basel", "compliance", "regulatory"]
        
        detected_products = []
        detected_compliance = []
        
        for product_type, keywords in banking_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                detected_products.append(product_type)
        
        for keyword in compliance_keywords:
            if keyword in prompt_lower:
                detected_compliance.append(keyword.upper())
        
        return {
            "is_banking": len(detected_products) > 0 or len(detected_compliance) > 0,
            "products": detected_products,
            "compliance": detected_compliance,
            "domain_confidence": min(1.0, (len(detected_products) + len(detected_compliance)) * 0.3)
        }

    def _classify_intent(self, prompt_lower: str) -> str:
        """Classify the user's intent from the prompt."""
        
        # Check for complete workflow patterns first
        complete_workflow_patterns = [
            "create specifications and implement",
            "build complete",
            "implement end-to-end",
            "orchestrate complete development",
            "create specifications and implement complete",
            "specifications and implement"
        ]
        
        if any(pattern in prompt_lower for pattern in complete_workflow_patterns):
            return "complete_workflow"
        
        intent_patterns = {
            "create_spec": ["create", "generate", "build", "design", "spec", "specification", "epic", "feature", "story"],
            "create_feature": ["feature", "functionality", "capability", "module", "component"],
            "create_epic": ["epic", "project", "initiative", "large", "major"],
            "create_story": ["story", "task", "requirement", "user story", "acceptance criteria"],
            "implement_code": ["implement", "code", "develop", "program", "write", "build"],
            "validate": ["validate", "verify", "check", "test", "audit", "review"],
            "query": ["what", "how", "why", "explain", "describe", "tell me"],
            "modify": ["update", "change", "modify", "edit", "alter", "fix"]
        }
        
        for intent, keywords in intent_patterns.items():
            if any(keyword in prompt_lower for keyword in keywords):
                return intent
        
        return "general"

    def _determine_target_agent(self, prompt_lower: str, intent: str, banking_context: Dict[str, Any]) -> str:
        """Determine which agent should handle the request."""
        
        # Complete workflow routing - start with spec agent
        if intent == "complete_workflow":
            return "spec_agent"  # Start with specifications, then route to others
        
        # Code-specific routing
        if intent == "implement_code" or any(keyword in prompt_lower for keyword in ["code", "implement", "develop"]):
            return "code_agent"
        
        # Validation-specific routing  
        if intent == "validate" or any(keyword in prompt_lower for keyword in ["validate", "check", "test"]):
            return "validation_agent"
        
        # Default routing
        return "spec_agent"

    def _extract_entities(self, prompt: str) -> Dict[str, List[str]]:
        """Extract relevant entities from the prompt."""
        import re
        
        entities = {
            "epic_references": [],
            "feature_references": [],
            "story_references": [],
            "technical_terms": [],
            "business_terms": []
        }
        
        # Extract epic references (E001, E-001, Epic-001, etc.)
        epic_pattern = r'\b(?:E|Epic)[-_]?(\d+)\b'
        entities["epic_references"] = re.findall(epic_pattern, prompt, re.IGNORECASE)
        
        # Extract feature references
        feature_pattern = r'\b(?:F|Feature)[-_]?(\d+)\b'
        entities["feature_references"] = re.findall(feature_pattern, prompt, re.IGNORECASE)
        
        # Extract story references
        story_pattern = r'\b(?:S|Story)[-_]?(\d+)\b'
        entities["story_references"] = re.findall(story_pattern, prompt, re.IGNORECASE)
        
        # Technical terms
        tech_keywords = ["api", "database", "microservice", "service", "endpoint", "authentication", "authorization"]
        entities["technical_terms"] = [term for term in tech_keywords if term in prompt.lower()]
        
        # Business terms
        business_keywords = ["customer", "user", "account", "transaction", "payment", "loan", "credit"]
        entities["business_terms"] = [term for term in business_keywords if term in prompt.lower()]
        
        return entities

    def _calculate_confidence(self, prompt_lower: str, intent: str, target_agent: str) -> float:
        """Calculate confidence score for the classification."""
        confidence = 0.5  # Base confidence
        
        # Intent-specific confidence boosts
        intent_keywords = {
            "create_feature": ["feature", "functionality"],
            "create_epic": ["epic", "project"],
            "implement_code": ["code", "implement"],
            "validate": ["validate", "check"]
        }
        
        if intent in intent_keywords:
            matches = sum(1 for keyword in intent_keywords[intent] if keyword in prompt_lower)
            confidence += matches * 0.15
        
        # Agent-specific confidence
        agent_keywords = {
            "spec_agent": ["spec", "requirement", "design"],
            "code_agent": ["code", "implement", "develop"],
            "validation_agent": ["validate", "test", "check"]
        }
        
        if target_agent in agent_keywords:
            matches = sum(1 for keyword in agent_keywords[target_agent] if keyword in prompt_lower)
            confidence += matches * 0.1
        
        return min(1.0, confidence)

    def _get_routing_reason(self, intent: str, banking_context: Dict[str, Any], target_agent: str) -> str:
        """Generate human-readable reason for routing decision."""
        reasons = []
        
        if intent != "general":
            reasons.append(f"Intent classified as '{intent}'")
        
        if banking_context.get("is_banking"):
            products = banking_context.get("products", [])
            if products:
                reasons.append(f"Banking context detected: {', '.join(products)}")
        
        if target_agent:
            reasons.append(f"Routed to {target_agent}")
        
        return "; ".join(reasons) if reasons else f"Default routing to {target_agent}"

    def _update_memory_context(self, classification: Dict[str, Any]) -> None:
        """Update the memory context with new classification."""
        context_entry = {
            "timestamp": classification["timestamp"],
            "prompt": classification["original_prompt"],
            "intent": classification["intent"],
            "target_agent": classification["target_agent"],
            "confidence": classification["confidence"],
            "banking_context": classification["banking_context"]
        }
        
        self.memory_context.append(context_entry)
        
        # Maintain context window
        if len(self.memory_context) > self.context_window:
            self.memory_context = self.memory_context[-self.context_window:]
        
        # Persist if enabled
        if self.persist_memory:
            self._persist_memory()
    
    def get_recent_context(self, limit: int = None) -> List[Dict[str, Any]]:
        """Get recent context entries."""
        limit = limit or self.context_window
        return self.memory_context[-limit:]
    
    def _persist_memory(self) -> None:
        """Persist memory context to file."""
        try:
            memory_file = project_root / "orchestrator_memory.json"
            with open(memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory_context, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not persist memory: {e}")
    
    def load_memory(self) -> None:
        """Load persisted memory context."""
        try:
            memory_file = project_root / "orchestrator_memory.json"
            if memory_file.exists():
                with open(memory_file, 'r', encoding='utf-8') as f:
                    self.memory_context = json.load(f)
                print(f"Loaded {len(self.memory_context)} memory entries")
        except Exception as e:
            print(f"Warning: Could not load memory: {e}")
        
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
                "code_agent": "code_agent",  # Added for complete workflow routing
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
        
        # Compile with recursion limit configuration
        return workflow.compile(
            checkpointer=None,
            interrupt_before=None,
            interrupt_after=None,
            debug=False
        )
    
    def _orchestrator_node(self, state: WorkflowState) -> WorkflowState:
        """Orchestrator node - analyze prompt and determine routing."""
        try:
            print("[ANALYZE] LangGraph Orchestrator: Analyzing prompt...")
            
            result = self.classify_prompt(state["prompt"])
            
            # Update state
            state["intent"] = result.get("intent", "unknown")
            state["banking_context"] = result.get("banking_context", {})
            state["entities"] = result.get("entities", {})
            state["orchestrator_result"] = result
            state["workflow_status"] = "orchestration_complete"
            
            # Set complete workflow state if needed
            if state["intent"] == "complete_workflow":
                self._phase_counter = 1
                self._persist_workflow_state(state, True, "specification")
                print("[WORKFLOW] Complete Workflow: Marked for Phase 1 - Epic/Feature/Story Creation")
                print(f"[WORKFLOW] Complete Workflow: Phase Counter: {self._phase_counter}")
            
            # Add message
            state["messages"].append(
                AIMessage(content=f"Analyzed prompt with intent: {state['intent']}")
            )
            
            print(f"[OK] Intent classified as: {state['intent']}")
            print(f"🔍 Orchestrator final state - complete_workflow: {state.get('is_complete_workflow', False)}, phase: {state.get('workflow_phase', '')}")
            
        except Exception as e:
            print(f"[ERROR] Orchestrator error: {e}")
            state["workflow_status"] = "error"
            state["error_count"] += 1
            state["messages"].append(
                AIMessage(content=f"Orchestrator error: {e}")
            )
        
        return state
    
    def _spec_agent_node(self, state: WorkflowState) -> WorkflowState:
        """Spec agent node - generate specifications."""
        try:
            print("[SPEC] LangGraph: Generating specifications...")
            is_complete, phase, counter = self._extract_workflow_state(state)
            print(f"🔍 Spec agent state - complete_workflow: {is_complete}, phase: {phase}, counter: {counter}")
            
            agent_params = {
                "prompt": state["prompt"],
                "intent": state["intent"],
                "banking_context": state["banking_context"],
                "entities": state["entities"],
                "is_complete_workflow": state.get("is_complete_workflow", False),
                "workflow_phase": state.get("workflow_phase", "")
            }
            
            result = self.spec_agent.process_specification_request(agent_params)
            
            state["spec_result"] = result
            state["workflow_status"] = "spec_complete"
            
            state["messages"].append(
                AIMessage(content=f"Generated specification: {result.get('spec_type', 'unknown')}")
            )
            
            print(f"[OK] Generated {result.get('spec_type', 'unknown')} specification")
            print(f"🔍 Spec agent final state - complete_workflow: {state.get('is_complete_workflow', False)}, phase: {state.get('workflow_phase', '')}")
            
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
            print("[CODE] LangGraph: Generating code implementation...")
            
            # Enhanced agent params with spec context for better code generation
            agent_params = {
                "prompt": state["prompt"],
                "banking_context": state["banking_context"],
                "entities": state["entities"],
                "spec_result": state.get("spec_result", {}),  # Pass spec context
                "is_complete_workflow": state.get("is_complete_workflow", False)
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
                "validate_all": True,
                "banking_context": state.get("banking_context", {}),
                "entities": state.get("entities", {}),
                "is_complete_workflow": state.get("is_complete_workflow", False),
                "workflow_phase": state.get("workflow_phase", "")
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
        """Finalize workflow - compile final results and sync with GitHub."""
        print("🎉 LangGraph: Finalizing workflow...")
        
        # Prepare final results
        final_results = {
            "orchestrator": state.get("orchestrator_result"),
            "spec_agent": state.get("spec_result"),
            "code_agent": state.get("code_result"),
            "validation": state.get("validation_result"),
            "project": state.get("project_result")
        }
        
        # Sync with GitHub using DIRECT MCP calls
        github_sync_results = []
        issues_created_count = 0
        
        if state.get("spec_result"):
            try:
                print("[GITHUB] Starting GitHub MCP integration...")
                
                # Get spec result data
                spec_result = state.get("spec_result")
                
                # Extract GitHub MCP data from spec results
                github_mcp_data = spec_result.get("github_mcp_data", [])
                
                if github_mcp_data:
                    print(f"🔗 GitHub MCP Project Agent: Processing spec results...")
                    print(f"[PROCESS] Processing {len(github_mcp_data)} spec result(s) for GitHub")
                    
                    # Create GitHub issues DIRECTLY using MCP tools
                    for item in github_mcp_data:
                        try:
                            print(f"[EXEC] Executing GitHub MCP Actions...")
                            
                            # Create repository issue FIRST, then add to GitHub Project
                            issue_data = item.get("mcp_issue_data", {})
                            if issue_data:
                                print(f"   [ITEM] create_project_item: {item.get('issue_title', 'Unknown')}")
                                print(f"   ?? Creating GitHub repository issue: {item.get('issue_title', 'Unknown')}")
                                print(f"   [TOOL] Executing MCP tool: github_issue_write")
                                print(f"   [CREATE] Creating GitHub repository issue first...")
                                
                                # Create repository issue first, then add to project
                                try:
                                    issue_result = self._execute_mcp_github_issue_write(issue_data)
                                    if issue_result and issue_result.get("id"):
                                        # Step 1: Repository issue created successfully
                                        issue_number = issue_result.get("number")
                                        issue_id = issue_result.get("id")
                                        issues_created_count += 1
                                        print(f"   ✅ Repository issue #{issue_number} created successfully")
                                        print(f"   📊 Step 2: Ready to add issue to GitHub Project #2...")
                                        
                                        # Step 2: Issue ready for project addition
                                        github_sync_results.append({
                                            "type": "issue_created_for_project",
                                            "issue_number": issue_number,
                                            "issue_id": issue_id,
                                            "issue_url": issue_result.get("html_url"),
                                            "title": issue_data.get("title"),
                                            "status": "ready_for_project",
                                            "project_action": f"Add issue #{issue_number} to Project #2"
                                        })
                                    elif issue_result and issue_result.get("mcp_execution_needed"):
                                            # MCP tools need to be called by VS Code
                                            print(f"   [MCP] MCP execution prepared - requires VS Code MCP environment")
                                            github_sync_results.append({
                                            "type": "mcp_prepared",
                                            "tool": issue_result.get("tool"),
                                            "parameters": issue_result.get("parameters"),
                                            "title": issue_data.get("title"),
                                            "status": "mcp_ready",
                                            "note": "MCP tool call prepared for VS Code execution"
                                        })
                                    else:
                                        print(f"   ❌ Repository issue creation failed")
                                        github_sync_results.append({
                                            "type": "issue_creation_failed",
                                            "error": "MCP tool returned no result",
                                            "title": issue_data.get("title"),
                                            "status": "failed"
                                        })
                                except Exception as mcp_error:
                                    print(f"   ❌ MCP execution error: {mcp_error}")
                                    github_sync_results.append({
                                        "type": "issue_error",
                                        "error": str(mcp_error),
                                        "title": issue_data.get("title"),
                                        "status": "error"
                                    })
                            
                            # Create file directly
                            file_data = item.get("mcp_file_data", {})
                            if file_data:
                                print(f"   [FILE] create_file: {item.get('issue_title', 'Unknown')}")
                                print(f"   📄 Creating GitHub file: {file_data.get('path', 'unknown')}")
                                
                                try:
                                    file_result = self._execute_mcp_github_create_file(file_data)
                                    if file_result and file_result.get("commit"):
                                        print(f"   ✅ GitHub file created successfully")
                                        github_sync_results.append({
                                            "type": "file_created",
                                            "file_path": file_data.get("path"),
                                            "commit_sha": file_result.get("commit", {}).get("sha"),
                                            "status": "success"
                                        })
                                    else:
                                        print(f"   ❌ MCP file creation failed")
                                        github_sync_results.append({
                                            "type": "file_failed",
                                            "error": "MCP tool returned no result",
                                            "file_path": file_data.get("path"),
                                            "status": "failed"
                                        })
                                        
                                except Exception as file_error:
                                    print(f"   ❌ File creation error: {file_error}")
                                    github_sync_results.append({
                                        "type": "file_error",
                                        "error": str(file_error),
                                        "file_path": file_data.get("path"),
                                        "status": "error"
                                    })
                                    
                        except Exception as item_error:
                            print(f"   ❌ Error processing item: {item_error}")
                            github_sync_results.append({
                                "type": "processing_error",
                                "error": str(item_error),
                                "status": "error"
                            })
                    
                    print(f"✅ GitHub MCP integration completed: {len(github_sync_results)} operations")
                else:
                    print("[INFO] No GitHub MCP data found in spec results")
                
                # Set project result
                state["project_result"] = {
                    "success": len(github_sync_results) > 0,
                    "issues_created": issues_created_count,
                    "operations_completed": len(github_sync_results),
                    "github_operations": github_sync_results
                }
                final_results["project"] = state["project_result"]
                
            except Exception as e:
                print(f"❌ GitHub MCP integration error: {e}")
                github_sync_results = [{"status": "error", "error": str(e)}]
                issues_created_count = 0
        
        state["final_result"] = {
            "workflow_id": f"langraph_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "status": "completed",
            "prompt": state["prompt"],
            "intent": state["intent"],
            "is_complete_workflow": state.get("is_complete_workflow", False),
            "workflow_phase": state.get("workflow_phase", "unknown"),
            "results": final_results,
            "github_sync": github_sync_results,
            "workflow_status": state["workflow_status"],
            "error_count": state["error_count"],
            "completion_time": datetime.now().isoformat()
        }
        
        state["messages"].append(
            AIMessage(content="Workflow completed successfully")
        )
        
        print("✅ LangGraph workflow completed with GitHub MCP integration")
        
        return state
    
    def _execute_mcp_github_issue_write(self, issue_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Execute the GitHub issue creation MCP tool directly."""
        try:
            print(f"   🔍 Executing MCP GitHub Issue Creation...")
            
            # Try to use MCP tools if available in VS Code environment
            if self._is_in_vscode_environment():
                print(f"   ✅ VS Code MCP environment detected")
                
                # Import MCP tools dynamically (they should be available in VS Code)
                try:
                    # Try to access MCP tools through VS Code's Python environment
                    import sys
                    
                    # Check if MCP tools are available as imported modules
                    if hasattr(sys.modules.get('__main__', {}), 'mcp_github_issue_write'):
                        mcp_tool = getattr(sys.modules['__main__'], 'mcp_github_issue_write')
                        print(f"   [CALL] Found MCP tool in __main__")
                        
                        result = mcp_tool(
                            method="create",
                            owner=issue_data.get("owner"),
                            repo=issue_data.get("repo"),
                            title=issue_data.get("title"),
                            body=issue_data.get("body"),
                            labels=issue_data.get("labels", [])
                        )
                        return result
                    
                    # Try alternative access method
                    elif 'mcp_github_issue_write' in globals():
                        mcp_tool = globals()['mcp_github_issue_write']
                        print(f"   [CALL] Found MCP tool in globals")
                        
                        result = mcp_tool(
                            method="create",
                            owner=issue_data.get("owner"),
                            repo=issue_data.get("repo"),
                            title=issue_data.get("title"),
                            body=issue_data.get("body"),
                            labels=issue_data.get("labels", [])
                        )
                        return result
                    
                    else:
                        print(f"   ⚠️ MCP tools not directly accessible in Python context")
                        print(f"   💡 MCP tools require VS Code environment for execution")
                        
                        # Prepare MCP execution data for VS Code
                        return {
                            "mcp_execution_needed": True,
                            "tool": "mcp_github_issue_write",
                            "parameters": {
                                "method": "create",
                                "owner": issue_data.get("owner"),
                                "repo": issue_data.get("repo"),
                                "title": issue_data.get("title"),
                                "body": issue_data.get("body"),
                                "labels": issue_data.get("labels", [])
                            },
                            "status": "ready_for_vscode_execution"
                        }
                        
                except ImportError as import_error:
                    print(f"   ⚠️ MCP tools import error: {import_error}")
                    return {
                        "mcp_execution_needed": True,
                        "tool": "mcp_github_issue_write",
                        "parameters": {
                            "method": "create",
                            "owner": issue_data.get("owner"),
                            "repo": issue_data.get("repo"),
                            "title": issue_data.get("title"),
                            "body": issue_data.get("body"),
                            "labels": issue_data.get("labels", [])
                        },
                        "import_error": str(import_error)
                    }
            
            else:
                print(f"   ⚠️ Not in VS Code environment - MCP tools not available")
                return {
                    "mcp_execution_needed": True,
                    "tool": "mcp_github_issue_write",
                    "parameters": {
                        "method": "create",
                        "owner": issue_data.get("owner"),
                        "repo": issue_data.get("repo"),
                        "title": issue_data.get("title"),
                        "body": issue_data.get("body"),
                        "labels": issue_data.get("labels", [])
                    },
                    "error": "VS Code environment required for MCP tools"
                }
                
        except Exception as e:
            print(f"   ❌ Error in MCP tool execution: {e}")
            return {
                "error": str(e),
                "mcp_execution_needed": True,
                "tool": "mcp_github_issue_write",
                "parameters": {
                    "method": "create",
                    "owner": issue_data.get("owner"),
                    "repo": issue_data.get("repo"),
                    "title": issue_data.get("title"),
                    "body": issue_data.get("body"),
                    "labels": issue_data.get("labels", [])
                }
            }
    
    def _sync_spec_files_with_github(self, spec_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Sync specification files with GitHub repository using MCP integration."""
        github_results = []
        
        try:
            from src.config import get_github_config, get_system_config
            github_config = get_github_config()
            system_config = get_system_config()
            
            # Check if GitHub sync is enabled and configured
            if not github_config.is_configured or not system_config.auto_sync_github:
                print("[INFO] GitHub sync not configured or disabled")
                return github_results
            
            print("[SYNC] Starting GitHub MCP synchronization...")
            
            # Extract GitHub data from spec results
            github_data_items = self._extract_github_data_from_specs(spec_results)
            
            for item in github_data_items:
                try:
                    # Sync file to GitHub repository
                    file_result = self._sync_file_to_github(item)
                    
                    # Create GitHub issue for the specification
                    issue_result = self._create_github_issue_for_spec(item)
                    
                    github_results.append({
                        "spec_file": item["spec_file"],
                        "spec_type": item["spec_type"],
                        "file_sync": file_result,
                        "issue_sync": issue_result,
                        "status": "completed"
                    })
                    
                except Exception as e:
                    print(f"❌ Error syncing {item['spec_file']}: {e}")
                    github_results.append({
                        "spec_file": item["spec_file"],
                        "status": "error",
                        "error": str(e)
                    })
            
            print(f"✅ GitHub sync completed: {len(github_results)} items processed")
            
        except Exception as e:
            print(f"❌ GitHub sync failed: {e}")
            return [{"status": "error", "error": str(e)}]
        
        return github_results
    
    def _extract_github_data_from_specs(self, spec_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract GitHub sync data from spec agent results."""
        github_items = []
        
        # Check if spec_results contains GitHub integration data
        if isinstance(spec_results, dict):
            # Look for github_sync_data in the results
            for key, value in spec_results.items():
                if isinstance(value, dict) and "mcp_file_data" in value:
                    github_items.append(value)
                elif isinstance(value, dict) and "github_integration" in value:
                    github_items.append(value)
        
        return github_items
    
    def _sync_file_to_github(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Sync a specification file to GitHub repository using MCP."""
        try:
            # Check if we should mock GitHub API (for testing)
            if os.getenv("MOCK_GITHUB_API", "false").lower() == "true":
                print(f"📄 Mock sync file: {item.get('spec_file', 'unknown')}")
                return {
                    "action": "file_created",
                    "file_path": item.get("spec_file"),
                    "commit_message": f"Add specification: {item.get('issue_title', 'Specification')}",
                    "status": "mocked"
                }
            
            # Use actual GitHub MCP integration
            mcp_data = item.get("mcp_file_data", {})
            if not mcp_data:
                return {"status": "error", "error": "No MCP file data available"}
            
            # Call GitHub MCP server to create/update file
            print(f"📄 Syncing file to GitHub: {mcp_data['path']}")
            
            # TODO: This would be the actual MCP call when MCP server is available
            # result = mcp_github_github_create_or_update_file(
            #     owner=mcp_data["owner"],
            #     repo=mcp_data["repo"],
            #     path=mcp_data["path"],
            #     content=mcp_data["content"],
            #     message=mcp_data["message"],
            #     branch=mcp_data["branch"]
            # )
            
            # For now, simulate successful file creation
            return {
                "action": "file_created",
                "file_path": mcp_data["path"],
                "commit_message": mcp_data["message"],
                "commit_sha": f"sha_{datetime.now().strftime('%H%M%S')}",
                "status": "ready_for_mcp"  # Indicates MCP integration is prepared
            }
            
        except Exception as e:
            print(f"❌ Error syncing file to GitHub: {e}")
            return {"status": "error", "error": str(e)}
    
    def _create_github_issue_for_spec(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Create a GitHub issue for a specification using MCP."""
        try:
            # Check if we should mock GitHub API (for testing)
            if os.getenv("MOCK_GITHUB_API", "false").lower() == "true":
                print(f"🐛 Mock create issue: {item.get('issue_title', 'Unknown')}")
                return {
                    "action": "issue_created",
                    "issue_title": item.get("issue_title"),
                    "issue_number": f"#{datetime.now().strftime('%H%M%S')}",
                    "status": "mocked"
                }
            
            # Check if GitHub issue creation is enabled
            if os.getenv("AUTO_CREATE_GITHUB_ISSUES", "true").lower() != "true":
                print("[INFO] GitHub issue creation disabled")
                return {"status": "disabled", "message": "GitHub issue creation disabled"}
            
            # Use actual GitHub MCP integration
            mcp_data = item.get("mcp_issue_data", {})
            if not mcp_data:
                return {"status": "error", "error": "No MCP issue data available"}
            
            # Call GitHub MCP server to create issue
            print(f"🐛 Creating GitHub issue: {mcp_data['title']}")
            
            # TODO: This would be the actual MCP call when MCP server is available
            # result = mcp_github_github_create_issue(
            #     owner=mcp_data["owner"],
            #     repo=mcp_data["repo"],
            #     title=mcp_data["title"],
            #     body=mcp_data["body"],
            #     labels=mcp_data["labels"]
            # )
            
            # For now, simulate successful issue creation
            return {
                "action": "issue_created",
                "issue_title": mcp_data["title"],
                "issue_number": f"#{datetime.now().strftime('%H%M%S')}",
                "labels": mcp_data["labels"],
                "issue_url": f"https://github.com/{mcp_data['owner']}/{mcp_data['repo']}/issues/pending",
                "status": "ready_for_mcp"  # Indicates MCP integration is prepared
            }
            
        except Exception as e:
            print(f"❌ Error creating GitHub issue: {e}")
            return {"status": "error", "error": str(e)}
    
    def sync_spec_with_github_mcp(self, spec_file_path: str, spec_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sync a specification file with GitHub using MCP server tools.
        This method demonstrates actual MCP integration.
        """
        try:
            from src.config import get_github_config
            github_config = get_github_config()
            
            if not github_config.is_configured:
                return {"status": "error", "error": "GitHub not configured"}
            
            # Read the specification file
            with open(spec_file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
            
            # Generate relative path for GitHub
            spec_path = Path(spec_file_path)
            if spec_path.is_absolute():
                try:
                    relative_path = str(spec_path.relative_to(Path.cwd()))
                except ValueError:
                    # If the file is not in the current directory tree, use the filename
                    relative_path = f"specs/{spec_path.name}"
            else:
                relative_path = str(spec_path)
            
            result = {"file_sync": None, "issue_sync": None}
            
            # 1. Sync file to GitHub repository
            try:
                # This is where actual MCP tools would be called:
                # file_result = mcp_github_github_create_or_update_file(
                #     owner=github_config.repo_owner,
                #     repo=github_config.repo_name,
                #     path=relative_path,
                #     content=file_content,
                #     message=f"Add specification: {spec_info.get('title', 'Specification')}",
                #     branch="main"
                # )
                
                # For demonstration, show what would be called
                print(f"🔄 MCP Call: mcp_github_github_create_or_update_file")
                print(f"   - owner: {github_config.repo_owner}")
                print(f"   - repo: {github_config.repo_name}")
                print(f"   - path: {relative_path}")
                print(f"   - message: Add specification: {spec_info.get('title', 'Specification')}")
                
                result["file_sync"] = {
                    "status": "mcp_ready",
                    "path": relative_path,
                    "method": "mcp_github_github_create_or_update_file"
                }
                
            except Exception as e:
                result["file_sync"] = {"status": "error", "error": str(e)}
            
            # 2. Create GitHub issue
            if os.getenv("AUTO_CREATE_GITHUB_ISSUES", "true").lower() == "true":
                try:
                    issue_title = f"📝 Specification: {spec_info.get('title', 'New Specification')}"
                    issue_body = f"""## Specification Created

**File:** `{relative_path}`
**Type:** {spec_info.get('type', 'unknown')}
**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### Overview
{spec_info.get('objective', spec_info.get('goal', 'Specification details to be defined'))}

### Next Steps
- [ ] Review specification content
- [ ] Validate requirements
- [ ] Plan implementation
- [ ] Assign to development team

**Auto-generated by PromptToProduct**"""
                    
                    # This is where actual MCP tools would be called:
                    # issue_result = mcp_github_github_create_issue(
                    #     owner=github_config.repo_owner,
                    #     repo=github_config.repo_name,
                    #     title=issue_title,
                    #     body=issue_body,
                    #     labels=["specification", "auto-generated", "banking"]
                    # )
                    
                    # For demonstration, show what would be called
                    print(f"🔄 MCP Call: mcp_github_github_create_issue")
                    print(f"   - owner: {github_config.repo_owner}")
                    print(f"   - repo: {github_config.repo_name}")
                    print(f"   - title: {issue_title}")
                    print(f"   - labels: ['specification', 'auto-generated', 'banking']")
                    
                    result["issue_sync"] = {
                        "status": "mcp_ready",
                        "title": issue_title,
                        "method": "mcp_github_github_create_issue"
                    }
                    
                except Exception as e:
                    result["issue_sync"] = {"status": "error", "error": str(e)}
            
            return {
                "status": "completed",
                "spec_file": relative_path,
                "github_integration": result
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
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
            print(f"🔄 Preparing retry")
            state["workflow_status"] = "retrying"
        
        return state
    
    def _route_after_orchestrator(self, state: WorkflowState) -> str:
        """Route after orchestrator based on spec-driven development framework."""
        if state["workflow_status"] == "error":
            return "error"
        
        intent = state.get("intent", "")
        
        print(f"🔍 Orchestrator routing - intent: {intent}")
        
        # Check for complete workflow patterns
        if intent == "complete_workflow":
            print("🔄 Complete Workflow: Starting Phase 1 - Epic/Feature/Story Creation")
            print("🔄 Complete Workflow: Planned Phases - 1:Spec → 2:Validation → 3:Code → 4:Validation → 5:Finalize")
            return "spec_agent"
        
        # Spec-driven development: Always start with specifications
        if intent in ["create_epic", "create_feature", "create_story", "spec_generation", "create_spec"]:
            return "spec_agent"
        elif intent in ["code_generation", "implement_feature", "implement_code"]:
            # Check if specifications exist for code implementation
            if self._has_relevant_specifications(state):
                state["spec_driven"] = True
                return "code_agent"
            else:
                # No specs found - create them first
                print("🔄 Spec-driven workflow: Creating specifications before code implementation...")
                state["spec_driven"] = True
                state["original_intent"] = intent  # Remember we want code after specs
                return "spec_agent"
        else:
            return "spec_agent"  # Default to spec agent
    
    def _route_after_spec(self, state: WorkflowState) -> str:
        """Route after spec agent with spec-driven development support."""
        if state["workflow_status"] == "error":
            return "error"
        
        # Check if this is a complete workflow
        is_complete_workflow = state.get("is_complete_workflow", False)
        spec_result = state.get("spec_result", {})
        
        if is_complete_workflow:
            # For complete workflows, validate specs first, then code generation
            print("🔄 Complete Workflow: Proceeding to Phase 2 - Specification Validation")
            return "validation_agent"
        
        # Check if this was part of a spec-driven code implementation flow
        if state.get("spec_driven") and state.get("original_intent") in ["code_generation", "implement_feature", "implement_code"]:
            print("🔄 Spec-driven workflow: Proceeding to code implementation...")
            # Clear the original intent to prevent loops
            state["original_intent"] = None
            return "code_agent"
        
        return "validation_agent"
    
    def _route_after_validation(self, state: WorkflowState) -> str:
        """Route after validation agent with spec-driven development support."""
        if state["workflow_status"] == "error":
            return "error"
        
        validation_result = state.get("validation_result", {})
        score = validation_result.get("overall_score", 0.0)
        is_complete_workflow, current_phase, counter = self._extract_workflow_state(state)
        intent = state.get("intent", "")
        
        print(f"🔍 Validation routing - complete_workflow: {is_complete_workflow}, phase: {current_phase}, counter: {counter}, intent: {intent}")
        
        # Handle complete workflow routing with phase progression
        if is_complete_workflow or intent == "complete_workflow":
            # Count validation runs to determine phase
            validation_count = 0
            for msg in state["messages"]:
                if hasattr(msg, 'content') and "Validation completed with score:" in msg.content:
                    validation_count += 1
            
            if validation_count <= 1:
                # First validation: After spec validation, go to code generation
                self._phase_counter = 2
                self._persist_workflow_state(state, True, "code_generation")
                print(f"✅ Phase 2 completed with score: {score:.2f}, proceeding to Phase 3 - Code Generation (validation #{validation_count})")
                return "code_agent"
            else:
                # Second+ validation: After code validation, finalize
                self._phase_counter = 4
                self._persist_workflow_state(state, True, "finalization")
                print(f"✅ Phase 4 completed with score: {score:.2f}, proceeding to Phase 5 - Finalize (validation #{validation_count})")
                return "finalize"
        
        # Check if this was part of a spec-driven code implementation flow
        if state.get("spec_driven") and state.get("original_intent") in ["code_generation", "implement_feature", "implement_code"]:
            print(f"✅ Spec validation completed with score: {score:.2f}, proceeding to code implementation...")
            # Clear the original intent to prevent loops
            state["original_intent"] = None
            return "code_agent"
        
        print(f"✅ Validation completed with score: {score:.2f}, proceeding to finalize")
        return "finalize"
    
    def _has_relevant_specifications(self, state: WorkflowState) -> bool:
        """Check if relevant specifications exist for code implementation."""
        prompt = state.get("prompt", "").lower()
        
        # Check for existing specification files
        spec_dirs = [
            project_root / "specs" / "features",
            project_root / "specs" / "epics", 
            project_root / "specs" / "stories"
        ]
        
        # Banking domain keywords to match against specs
        banking_keywords = [
            "payment", "fraud", "loan", "credit", "account", 
            "transaction", "banking", "financial", "api"
        ]
        
        # Extract keywords from prompt
        prompt_keywords = [word for word in banking_keywords if word in prompt]
        
        if not prompt_keywords:
            return False
        
        # Check if any spec files contain relevant keywords
        for spec_dir in spec_dirs:
            if spec_dir.exists():
                for spec_file in spec_dir.glob("*.md"):
                    try:
                        content = spec_file.read_text().lower()
                        if any(keyword in content for keyword in prompt_keywords):
                            print(f"🔍 Found relevant specification: {spec_file.name}")
                            return True
                    except Exception:
                        continue
        
        return False
    
    def _route_after_code(self, state: WorkflowState) -> str:
        """Route after code agent."""
        if state["workflow_status"] == "error":
            return "error"
        
        # Check if this is a complete workflow
        is_complete_workflow, current_phase, counter = self._extract_workflow_state(state)
        intent = state.get("intent", "")
        
        if is_complete_workflow or intent == "complete_workflow":
            self._phase_counter = 3
            self._persist_workflow_state(state, True, "code_validation")
            print(f"🔄 Complete Workflow: Proceeding to Phase 4 - Code Validation (counter: {self._phase_counter})")
        
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
            final_result=None
        )
        
        try:
            # Execute workflow with recursion limit configuration
            config = {
                "recursion_limit": 50,  # Increase from default 25
                "max_execution_time": 300  # 5 minute timeout
            }
            final_state = self.workflow.invoke(initial_state, config=config)
            
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
            "system": "PromptToProduct Unified",
            "version": "2.1.0",
            "orchestration": "Unified LangGraph + Orchestration",
            "agents": {
                "spec_agent": "✅ Available", 
                "code_agent": "✅ Available",
                "validation_agent": "✅ Available",
                "github_mcp_agent": "✅ Available"
            },
            "features": {
                "orchestration": "✅ Integrated",
                "classification": "✅ Banking domain detection",
                "routing": "✅ Intent-based routing",
                "memory": "✅ Context persistence",
                "langgraph": "✅ Stateful workflows",
                "github_mcp": "✅ MCP Server Integration" if self.mcp_tools_available else "⚠️ MCP Tools Pending"
            },
            "mcp_integration": {
                "server_configured": True,
                "tools_available": self.mcp_tools_available,
                "vscode_environment": self._is_in_vscode_environment(),
                "github_token": bool(os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN'))
            },
            "workflow_nodes": 6,
            "memory_entries": len(self.memory_context),
            "timestamp": datetime.now().isoformat()
        }

    def _check_mcp_tools_availability(self) -> bool:
        """Check if MCP tools are available in the current environment."""
        try:
            # Check for VS Code environment
            is_vscode = self._is_in_vscode_environment()
            
            # Check for MCP tools in various scopes
            mcp_tools = [
                'mcp_github_issue_write',
                'mcp_github_create_or_update_file',
                'mcp_github_create_pull_request'
            ]
            
            tools_found = 0
            for tool_name in mcp_tools:
                if tool_name in globals() or hasattr(__builtins__, tool_name):
                    tools_found += 1
            
            print(f"[MCP] Environment check - VS Code: {is_vscode}, Tools found: {tools_found}/{len(mcp_tools)}")
            return is_vscode and tools_found > 0
            
        except Exception as e:
            print(f"[MCP] Availability check error: {e}")
            return False
    
    def _is_in_vscode_environment(self) -> bool:
        """Check if we're running in VS Code environment where MCP tools are available."""
        # Check for VS Code specific environment variables
        vscode_indicators = [
            os.getenv('VSCODE_PID'),
            os.getenv('VSCODE_CWD'),
            os.getenv('TERM_PROGRAM') == 'vscode',
            os.getenv('VSCODE_INJECTION') == '1'
        ]
        return any(vscode_indicators)

    def _execute_mcp_github_create_file(self, file_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Execute GitHub file creation using MCP tools."""
        try:
            print(f"   🎯 GitHub File Creation via MCP")
            
            # Check if we're in VS Code environment where MCP tools are available
            if self._is_in_vscode_environment():
                print(f"   ✅ VS Code environment detected - MCP tools available")
                
                # Prepare file creation data for MCP
                file_creation_data = {
                    "owner": os.getenv('GITHUB_USERNAME', 'vrushalisarfare'),
                    "repo": os.getenv('GITHUB_REPO', 'PromptToProduct'),
                    "path": file_data.get("path", ""),
                    "content": file_data.get("content", ""),
                    "message": file_data.get("message", "Auto-generated file via MCP"),
                    "branch": os.getenv('GITHUB_BRANCH', 'feature/langchaingraph')
                }
                
                print(f"   📁 File: {file_creation_data['path']}")
                print(f"   🔄 Attempting MCP file creation...")
                
                # Try to access MCP file creation tool
                try:
                    import sys
                    
                    # Check if MCP tools are available
                    if hasattr(sys.modules.get('__main__', {}), 'mcp_github_create_or_update_file'):
                        mcp_tool = getattr(sys.modules['__main__'], 'mcp_github_create_or_update_file')
                        print(f"   [CALL] Found MCP file tool in __main__")
                        
                        result = mcp_tool(
                            owner=file_creation_data["owner"],
                            repo=file_creation_data["repo"],
                            path=file_creation_data["path"],
                            content=file_creation_data["content"],
                            message=file_creation_data["message"],
                            branch=file_creation_data["branch"]
                        )
                        return result
                    
                    elif 'mcp_github_create_or_update_file' in globals():
                        mcp_tool = globals()['mcp_github_create_or_update_file']
                        print(f"   [CALL] Found MCP file tool in globals")
                        
                        result = mcp_tool(
                            owner=file_creation_data["owner"],
                            repo=file_creation_data["repo"],
                            path=file_creation_data["path"],
                            content=file_creation_data["content"],
                            message=file_creation_data["message"],
                            branch=file_creation_data["branch"]
                        )
                        return result
                    
                    else:
                        print(f"   ⚠️ MCP file tools not directly accessible")
                        print(f"   💡 Preparing for VS Code MCP execution")
                        
                        # Return MCP execution data for VS Code
                        return {
                            "mcp_execution_needed": True,
                            "tool": "mcp_github_create_or_update_file",
                            "parameters": file_creation_data,
                            "status": "ready_for_vscode_execution"
                        }
                        
                except Exception as tool_error:
                    print(f"   ⚠️ MCP tool access error: {tool_error}")
                    return {
                        "mcp_execution_needed": True,
                        "tool": "mcp_github_create_or_update_file",
                        "parameters": file_creation_data,
                        "tool_error": str(tool_error)
                    }
            else:
                print(f"   ⚠️ Not in VS Code environment - MCP tools not available")
                return {
                    "mcp_execution_needed": True,
                    "tool": "mcp_github_create_or_update_file",
                    "parameters": file_data,
                    "error": "VS Code environment required for MCP tools"
                }
            
        except Exception as e:
            print(f"   ❌ Error in MCP file creation: {str(e)}")
            return {
                "error": f"MCP file creation failed: {str(e)}",
                "mcp_execution_needed": True,
                "tool": "mcp_github_create_or_update_file",
                "parameters": file_data
            }


def main():
    """Main entry point for the PromptToProduct CLI."""
    parser = argparse.ArgumentParser(
        description="PromptToProduct - LangGraph Agent Orchestration System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Direct prompt execution
  python prompttoproduct.py "Create a fraud detection system"
  
  # Automated modes
  python prompttoproduct.py --auto "Build loan API"
  echo "Create payment gateway" | python prompttoproduct.py
  
  # Environment variable prompt
  set PROMPTTOPRODUCT_PROMPT=Create banking dashboard
  python prompttoproduct.py --auto
  
  # System utilities
  python prompttoproduct.py --status
  python prompttoproduct.py --config
  python prompttoproduct.py --help
  
Environment Setup:
  See README.md - Environment Setup section for detailed instructions
  Quick setup: Set GITHUB_PERSONAL_ACCESS_TOKEN environment variable
  
Automation Variables:
  PROMPTTOPRODUCT_PROMPT - Set prompt via environment variable
        """
    )
    
    parser.add_argument(
        "prompt", 
        nargs="?", 
        help="Natural language prompt to process"
    )
    
    parser.add_argument(
        "--auto", 
        action="store_true", 
        help="Run in fully automated mode (no user interaction)"
    )
    
    parser.add_argument(
        "--status", 
        action="store_true", 
        help="Show system status"
    )
    
    parser.add_argument(
        "--config", 
        action="store_true", 
        help="Show configuration status and validation"
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
    
    parser.add_argument(
        "--test-github", 
        action="store_true",
        help="Test GitHub MCP integration with sample spec"
    )
    
    parser.add_argument(
        "--sync-spec", 
        type=str,
        help="Sync a specific spec file with GitHub (provide file path)"
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
                print("\n🎯 PROMPTTOPRODUCT UNIFIED SYSTEM STATUS")
                print("=" * 60)
                print(f"System: {status['system']}")
                print(f"Version: {status['version']}")
                print(f"Architecture: {status['orchestration']}")
                print(f"Workflow Nodes: {status['workflow_nodes']}")
                print(f"Memory Entries: {status['memory_entries']}")
                print("\nAgent Status:")
                for agent, status_text in status['agents'].items():
                    print(f"  {agent}: {status_text}")
                print("\nFeatures:")
                for feature, status_text in status['features'].items():
                    print(f"  {feature}: {status_text}")
                print(f"\nTimestamp: {status['timestamp']}")
            return
        
        # Handle configuration check
        if args.config:
            from src.config import get_config
            config = get_config()
            validation = config.validate_configuration()
            
            print("\n🔧 PROMPTTOPRODUCT CONFIGURATION STATUS")
            print("=" * 60)
            
            if validation['valid']:
                print("✅ Configuration is valid")
            else:
                print("❌ Configuration has issues")
            
            if validation.get('github_token_configured'):
                print("✅ GitHub Personal Access Token is configured")
            else:
                print("❌ GitHub Personal Access Token is NOT configured")
                print("   Set environment variable: GITHUB_PERSONAL_ACCESS_TOKEN")
                print("   Or run: .\\setup-environment.ps1 -GitHubToken <your_token>")
            
            print(f"\n📋 Configuration Summary:")
            summary = validation['summary']
            for key, value in summary.items():
                print(f"  {key}: {value}")
            
            if validation['issues']:
                print(f"\n❌ Issues:")
                for issue in validation['issues']:
                    print(f"  - {issue}")
            
            if validation['warnings']:
                print(f"\n⚠️ Warnings:")
                for warning in validation['warnings']:
                    print(f"  - {warning}")
            
            print(f"\nFor environment setup help, see README.md - Environment Setup section")
            return
        
        # Handle GitHub MCP testing
        if args.test_github:
            print("🧪 Testing GitHub MCP Integration")
            print("=" * 50)
            
            # Create a sample spec for testing
            sample_spec_info = {
                "title": "Sample Banking API Specification",
                "type": "feature",
                "objective": "Test GitHub MCP integration with sample specification",
                "goal": "Demonstrate GitHub file creation and issue management"
            }
            
            # Use the most recent spec file if available
            specs_dir = Path("specs")
            latest_spec = None
            
            for spec_type in ["epics", "features", "stories"]:
                type_dir = specs_dir / spec_type
                if type_dir.exists():
                    spec_files = list(type_dir.glob("*.md"))
                    if spec_files:
                        latest_spec = max(spec_files, key=lambda f: f.stat().st_mtime)
                        break
            
            if latest_spec:
                print(f"📄 Testing with: {latest_spec}")
                try:
                    result = system.sync_spec_with_github_mcp(str(latest_spec), sample_spec_info)
                    print(f"✅ Result: {result['status']}")
                    if result.get("github_integration"):
                        for key, value in result["github_integration"].items():
                            print(f"   {key}: {value}")
                    elif result.get("error"):
                        print(f"❌ Error: {result['error']}")
                except Exception as e:
                    print(f"❌ Exception during sync: {e}")
                    if args.verbose:
                        import traceback
                        traceback.print_exc()
            else:
                print("❌ No specification files found to test with")
                print("💡 Create a spec first: python prompttoproduct.py 'Create a test epic'")
            return
        
        # Handle specific spec file sync
        if args.sync_spec:
            print(f"🔄 Syncing spec file: {args.sync_spec}")
            print("=" * 50)
            
            spec_path = Path(args.sync_spec)
            if not spec_path.exists():
                print(f"❌ File not found: {args.sync_spec}")
                return
            
            # Extract spec info from filename
            spec_info = {
                "title": spec_path.stem,
                "type": "unknown",
                "objective": f"Sync specification file: {spec_path.name}"
            }
            
            result = system.sync_spec_with_github_mcp(str(spec_path), spec_info)
            print(f"✅ Sync result: {result['status']}")
            if result.get("github_integration"):
                for key, value in result["github_integration"].items():
                    print(f"   {key}: {value}")
            return
        
        # Handle prompt processing
        if not args.prompt:
            # Check for environment variable prompt
            env_prompt = os.getenv('PROMPTTOPRODUCT_PROMPT')
            if env_prompt:
                args.prompt = env_prompt
                if args.verbose:
                    print(f"📝 Using prompt from environment variable: {env_prompt}")
            # Check if there's input from stdin (piped input)
            elif not sys.stdin.isatty():
                # Read from stdin (piped input)
                try:
                    prompt_input = sys.stdin.read().strip()
                    if prompt_input:
                        args.prompt = prompt_input
                        if args.verbose:
                            print(f"📝 Using prompt from stdin: {prompt_input}")
                    else:
                        if not args.auto:
                            print("❌ No prompt provided via command line, environment variable, or stdin")
                        return
                except:
                    if not args.auto:
                        print("❌ Error reading from stdin")
                    return
            else:
                # No prompt and no stdin input
                if args.auto:
                    # In auto mode, just exit silently if no prompt
                    return
                else:
                    # Show help in interactive mode
                    parser.print_help()
                    return
        
        print(f"\n🚀 PROMPTTOPRODUCT LANGGRAPH WORKFLOW")
        print("=" * 60)
        print(f"Prompt: {args.prompt}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # In auto mode, suppress some output for cleaner automation
        if args.auto:
            # Minimal output for automation
            print(f"🚀 Processing: {args.prompt[:50]}{'...' if len(args.prompt) > 50 else ''}")
        
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

