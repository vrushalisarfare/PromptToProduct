#!/usr/bin/env python3
"""
Orchestrator Agent - Main Hub for Prompt Classification, Routing and GitHub Integration

This agent serves as the central orchestration point for the PromptToProduct system,
classifying user intents, delegating to appropriate domain agents, and managing GitHub integration.
"""
import json
import re
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import configuration system
try:
    from src.config import get_config, get_github_config
    config = get_config()
    github_config = get_github_config()
    CONFIG_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Configuration system not available: {e}")
    CONFIG_AVAILABLE = False

class PromptOrchestrator:
    """
    Central orchestration agent that classifies prompts and routes to appropriate agents.
    
    Capabilities:
    - classify_prompt: Analyze intent and context
    - route_to_agent: Delegate to appropriate specialist
    - memory_context: Maintain conversation context with persistence
    """
    
    def __init__(self, config_path: str = None):
        """Initialize the orchestrator with configuration."""
        self.config_path = config_path or str(project_root / ".github" / "workflows" / "copilot_agents.yaml")
        self.memory_context = []
        self.context_window = 10
        self.persist_memory = True
        self.agents_config = self._load_agents_config()
        self.routing_rules = self._extract_routing_rules()
        
    def _load_agents_config(self) -> Dict[str, Any]:
        """Load agent configuration from manifest."""
        try:
            import yaml
            with open(self.config_path, 'r', encoding='utf-8') as f:
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
            "is_banking": bool(detected_products),
            "product_types": detected_products,
            "compliance_areas": detected_compliance,
            "primary_product": detected_products[0] if detected_products else None
        }
    
    def _classify_intent(self, prompt_lower: str) -> str:
        """Classify the primary intent of the prompt."""
        intent_patterns = {
            "create_epic": r"create.*epic|add.*epic|new.*epic|epic.*for",
            "create_feature": r"create.*feature|add.*feature|new.*feature|feature.*for",
            "create_story": r"create.*story|add.*story|new.*story|story.*for",
            "generate_code": r"code|implement|develop|generate.*code|write.*code",
            "validate": r"validate|check|verify|audit|test",
            "update": r"update|modify|change|edit",
            "analyze": r"analyze|review|investigate|examine"
        }
        
        for intent, pattern in intent_patterns.items():
            if re.search(pattern, prompt_lower):
                return intent
        
        return "general_inquiry"
    
    def _determine_target_agent(self, prompt_lower: str, intent: str, banking_context: Dict[str, Any]) -> str:
        """Determine which agent should handle the prompt."""
        # Check routing rules based on trigger keywords
        for trigger, agent in self.routing_rules.items():
            if trigger in prompt_lower:
                return agent
        
        # Intent-based routing
        if intent in ["create_epic", "create_feature", "create_story"]:
            return "spec-agent"
        elif intent in ["generate_code"]:
            return "code-agent"
        elif intent in ["validate"]:
            return "validation-agent"
        
        # Banking context routing
        if banking_context.get("is_banking"):
            if banking_context.get("compliance_areas"):
                return "validation-agent"  # Compliance-related
            else:
                return "spec-agent"  # Banking feature creation
        
        # Default routing
        return "spec-agent"
    
    def _extract_entities(self, prompt: str) -> Dict[str, List[str]]:
        """Extract relevant entities from the prompt."""
        entities = {
            "epic_references": [],
            "feature_references": [],
            "story_references": [],
            "technologies": [],
            "stakeholders": []
        }
        
        # Extract ID references
        epic_matches = re.findall(r'\bE\d{3}\b', prompt, re.IGNORECASE)
        feature_matches = re.findall(r'\bF\d{3}\b', prompt, re.IGNORECASE)
        story_matches = re.findall(r'\bS\d{3}\b', prompt, re.IGNORECASE)
        
        entities["epic_references"] = [match.upper() for match in epic_matches]
        entities["feature_references"] = [match.upper() for match in feature_matches]
        entities["story_references"] = [match.upper() for match in story_matches]
        
        # Extract technologies
        tech_keywords = ["python", "java", "javascript", "react", "angular", "api", "microservices", "docker", "kubernetes"]
        entities["technologies"] = [tech for tech in tech_keywords if tech in prompt.lower()]
        
        # Extract stakeholders
        stakeholder_patterns = [
            r"as (?:a |an )?(\w+)",  # "as a developer"
            r"for (\w+)",  # "for customers"
        ]
        
        for pattern in stakeholder_patterns:
            matches = re.findall(pattern, prompt, re.IGNORECASE)
            entities["stakeholders"].extend(matches)
        
        return entities
    
    def _calculate_confidence(self, prompt_lower: str, intent: str, target_agent: str) -> float:
        """Calculate confidence score for the routing decision."""
        confidence = 0.5  # Base confidence
        
        # Boost confidence for clear trigger words
        trigger_found = any(trigger in prompt_lower for trigger in self.routing_rules.keys())
        if trigger_found:
            confidence += 0.3
        
        # Boost confidence for specific intent patterns
        if intent != "general_inquiry":
            confidence += 0.2
        
        # Boost confidence for banking domain context
        banking_keywords = ["loan", "credit", "payment", "account", "fraud", "compliance"]
        if any(keyword in prompt_lower for keyword in banking_keywords):
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _get_routing_reason(self, intent: str, banking_context: Dict[str, Any], target_agent: str) -> str:
        """Get human-readable reason for routing decision."""
        if target_agent == "spec-agent":
            if banking_context.get("is_banking"):
                return f"Banking domain {intent} - routing to spec agent for structured specification creation"
            else:
                return f"Specification creation intent detected - routing to spec agent"
        elif target_agent == "code-agent":
            return "Code generation or implementation request - routing to code agent"
        elif target_agent == "validation-agent":
            return "Validation, compliance, or audit request - routing to validation agent"
        else:
            return f"Default routing to {target_agent}"
    
    def route_to_agent(self, classification: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route the classified prompt to the appropriate agent.
        
        Args:
            classification: Result from classify_prompt
            
        Returns:
            Routing result with agent selection and parameters
        """
        target_agent = classification["routing_decision"]["agent"]
        
        # Prepare agent-specific parameters
        agent_params = {
            "prompt": classification["original_prompt"],
            "intent": classification["intent"],
            "entities": classification["entities"],
            "banking_context": classification["banking_context"],
            "confidence": classification["confidence"],
            "memory_context": self.get_recent_context()
        }
        
        routing_result = {
            "target_agent": target_agent,
            "agent_params": agent_params,
            "routing_timestamp": datetime.now().isoformat(),
            "orchestrator_decision": classification["routing_decision"],
            "next_action": self._get_next_action(target_agent),
            "expected_output": self._get_expected_output(target_agent, classification)
        }
        
        return routing_result
    
    def _get_next_action(self, target_agent: str) -> str:
        """Get the next action to be performed by the target agent."""
        actions = {
            "spec-agent": "process_specification_request",
            "code-agent": "generate_code_from_specs",
            "validation-agent": "validate_and_sync"
        }
        return actions.get(target_agent, "process_request")
    
    def _get_expected_output(self, target_agent: str, classification: Dict[str, Any]) -> Dict[str, str]:
        """Get expected output description for the target agent."""
        outputs = {
            "spec-agent": {
                "type": "markdown_specification",
                "location": "specs/",
                "format": "Epic (E###), Feature (F###), or Story (S###)"
            },
            "code-agent": {
                "type": "python_code",
                "location": "src/MyBank/",
                "format": "Python modules and classes"
            },
            "validation-agent": {
                "type": "validation_report",
                "location": "reports/",
                "format": "GitHub issues and workflow logs"
            }
        }
        return outputs.get(target_agent, {"type": "unknown", "location": "unknown", "format": "unknown"})
    
    def _update_memory_context(self, classification: Dict[str, Any]) -> None:
        """Update memory context with new classification."""
        context_entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt": classification["original_prompt"],
            "intent": classification["intent"],
            "target_agent": classification["target_agent"],
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
    
    def process_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Main entry point for processing a prompt through the orchestration system.
        
        Args:
            prompt: Natural language input
            
        Returns:
            Complete processing result with classification and routing
        """
        # Step 1: Classify the prompt
        classification = self.classify_prompt(prompt)
        
        # Step 2: Route to appropriate agent
        routing = self.route_to_agent(classification)
        
        # Step 3: Prepare final result
        result = {
            "orchestrator_version": "1.0",
            "processing_timestamp": datetime.now().isoformat(),
            "input_prompt": prompt,
            "classification": classification,
            "routing": routing,
            "status": "routed_successfully",
            "next_steps": [
                f"Execute {routing['target_agent']}.{routing['next_action']}",
                f"Generate {routing['expected_output']['type']} in {routing['expected_output']['location']}",
                "Return to orchestrator for validation routing"
            ]
        }
        
        return result
    
    def get_orchestrator_status(self) -> Dict[str, Any]:
        """Get current orchestrator status and statistics."""
        return {
            "orchestrator_id": "orchestrator",
            "version": "1.0",
            "status": "active",
            "memory_entries": len(self.memory_context),
            "context_window": self.context_window,
            "routing_rules": len(self.routing_rules),
            "available_agents": list(set(self.routing_rules.values())),
            "last_activity": self.memory_context[-1]["timestamp"] if self.memory_context else None,
            "configuration_loaded": bool(self.agents_config)
        }


def main():
    """CLI interface for the orchestrator agent."""
    import argparse
    
    parser = argparse.ArgumentParser(description="PromptToProduct Orchestrator Agent")
    parser.add_argument("prompt", nargs="?", help="Prompt to process")
    parser.add_argument("--status", action="store_true", help="Show orchestrator status")
    parser.add_argument("--memory", action="store_true", help="Show recent memory context")
    parser.add_argument("--config", help="Path to agent configuration file")
    args = parser.parse_args()
    
    # Initialize orchestrator
    orchestrator = PromptOrchestrator(config_path=args.config)
    orchestrator.load_memory()
    
    if args.status:
        status = orchestrator.get_orchestrator_status()
        print("🤖 Orchestrator Status")
        print("=" * 40)
        for key, value in status.items():
            print(f"{key}: {value}")
        return
    
    if args.memory:
        context = orchestrator.get_recent_context()
        print("🧠 Recent Memory Context")
        print("=" * 40)
        for entry in context:
            print(f"[{entry['timestamp']}] {entry['prompt']} -> {entry['target_agent']}")
        return
    
    if not args.prompt:
        print("Usage: python orchestrator.py '<prompt>' or --status or --memory")
        return
    
    # Process the prompt
    print(f"🔄 Processing: {args.prompt}")
    print("-" * 50)
    
    result = orchestrator.process_prompt(args.prompt)
    
    # Display results
    print(f"✅ Classification: {result['classification']['intent']}")
    print(f"🎯 Target Agent: {result['routing']['target_agent']}")
    print(f"🏦 Banking Context: {result['classification']['banking_context']['is_banking']}")
    print(f"📊 Confidence: {result['classification']['confidence']:.2f}")
    print(f"🔗 Next Action: {result['routing']['next_action']}")
    print(f"📁 Expected Output: {result['routing']['expected_output']['type']}")
    
    if result['classification']['entities']['epic_references']:
        print(f"📋 Epic References: {', '.join(result['classification']['entities']['epic_references'])}")
    
    print(f"\n💡 Routing Reason: {result['classification']['routing_decision']['reason']}")


if __name__ == "__main__":
    main()