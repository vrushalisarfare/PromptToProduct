#!/usr/bin/env python3
"""
Spec Agent - Converts Developer Prompts into Structured Markdown Specs

This agent specializes in converting natural language prompts into structured
specifications (epics, features, stories) with banking domain intelligence.
"""
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from specs.schema_processor import PromptToProductSchema
except ImportError:
    print("Warning: Could not import schema processor. Some functionality may be limited.")
    PromptToProductSchema = None

class SpecAgent:
    """
    Spec Agent for converting prompts to structured markdown specifications.
    
    Actions:
    - create_epic: Generate epic specifications
    - create_feature: Create feature specs with banking context
    - create_story: Develop user stories and compliance stories
    """
    
    def __init__(self):
        """Initialize the spec agent."""
        self.agent_id = "spec-agent"
        self.version = "1.0"
        self.schema_processor = None
        self._initialize_schema_processor()
        
    def _initialize_schema_processor(self):
        """Initialize the schema processor if available."""
        if PromptToProductSchema:
            try:
                self.schema_processor = PromptToProductSchema()
                print(f"✅ Schema processor initialized successfully")
            except Exception as e:
                print(f"Warning: Schema processor initialization failed: {e}")
    
    def process_specification_request(self, agent_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for processing specification requests.
        
        Args:
            agent_params: Parameters from orchestrator including prompt, intent, etc.
            
        Returns:
            Processing result with created specifications
        """
        prompt = agent_params.get("prompt", "")
        intent = agent_params.get("intent", "")
        banking_context = agent_params.get("banking_context", {})
        entities = agent_params.get("entities", {})
        
        print(f"🔧 Spec Agent Processing: {intent}")
        print(f"📝 Prompt: {prompt}")
        
        result = {
            "agent_id": self.agent_id,
            "processing_timestamp": datetime.now().isoformat(),
            "input_prompt": prompt,
            "intent": intent,
            "banking_context": banking_context,
            "status": "processing",
            "created_files": [],
            "errors": []
        }
        
        try:
            # Route to appropriate creation method
            if intent in ["create_epic"] or "epic" in prompt.lower():
                spec_result = self.create_epic(prompt, banking_context, entities)
            elif intent in ["create_feature"] or "feature" in prompt.lower():
                spec_result = self.create_feature(prompt, banking_context, entities)
            elif intent in ["create_story"] or "story" in prompt.lower():
                spec_result = self.create_story(prompt, banking_context, entities)
            else:
                # Auto-detect based on content and context
                spec_result = self._auto_detect_and_create(prompt, banking_context, entities)
            
            result.update(spec_result)
            result["status"] = "completed"
            
        except Exception as e:
            result["status"] = "error"
            result["errors"].append(str(e))
            print(f"❌ Error in spec processing: {e}")
        
        return result
    
    def create_epic(self, prompt: str, banking_context: Dict[str, Any], entities: Dict[str, Any]) -> Dict[str, Any]:
        """Create an epic specification from prompt."""
        print("📋 Creating Epic Specification...")
        
        # Extract epic information
        epic_info = self._extract_epic_info(prompt, banking_context)
        
        if self.schema_processor:
            try:
                # Use schema processor for creation
                schema_result = self.schema_processor.process_prompt(prompt)
                if schema_result.get("success") and schema_result.get("file_created"):
                    return {
                        "action": "create_epic",
                        "method": "schema_processor",
                        "created_files": [schema_result["file_created"]],
                        "epic_info": epic_info,
                        "schema_result": schema_result
                    }
            except Exception as e:
                print(f"Schema processor failed, using manual creation: {e}")
        
        # Manual epic creation
        epic_file = self._create_epic_manually(epic_info)
        
        return {
            "action": "create_epic",
            "method": "manual_creation",
            "created_files": [epic_file] if epic_file else [],
            "epic_info": epic_info
        }
    
    def create_feature(self, prompt: str, banking_context: Dict[str, Any], entities: Dict[str, Any]) -> Dict[str, Any]:
        """Create a feature specification from prompt."""
        print("🎯 Creating Feature Specification...")
        
        # Extract feature information
        feature_info = self._extract_feature_info(prompt, banking_context, entities)
        
        if self.schema_processor:
            try:
                # Use schema processor for banking features
                if banking_context.get("is_banking"):
                    schema_result = self.schema_processor.process_prompt(prompt)
                    if schema_result.get("success") and schema_result.get("file_created"):
                        return {
                            "action": "create_banking_feature",
                            "method": "schema_processor",
                            "created_files": [schema_result["file_created"]],
                            "feature_info": feature_info,
                            "banking_context": banking_context,
                            "schema_result": schema_result
                        }
            except Exception as e:
                print(f"Schema processor failed, using manual creation: {e}")
        
        # Manual feature creation
        feature_file = self._create_feature_manually(feature_info, banking_context)
        
        return {
            "action": "create_feature",
            "method": "manual_creation",
            "created_files": [feature_file] if feature_file else [],
            "feature_info": feature_info,
            "banking_context": banking_context
        }
    
    def create_story(self, prompt: str, banking_context: Dict[str, Any], entities: Dict[str, Any]) -> Dict[str, Any]:
        """Create a story specification from prompt."""
        print("📖 Creating Story Specification...")
        
        # Extract story information
        story_info = self._extract_story_info(prompt, banking_context, entities)
        
        if self.schema_processor:
            try:
                # Use schema processor, especially for compliance stories
                if banking_context.get("compliance_areas"):
                    schema_result = self.schema_processor.process_prompt(prompt)
                    if schema_result.get("success") and schema_result.get("file_created"):
                        return {
                            "action": "create_compliance_story",
                            "method": "schema_processor",
                            "created_files": [schema_result["file_created"]],
                            "story_info": story_info,
                            "compliance_context": banking_context.get("compliance_areas", []),
                            "schema_result": schema_result
                        }
                else:
                    schema_result = self.schema_processor.process_prompt(prompt)
                    if schema_result.get("success") and schema_result.get("file_created"):
                        return {
                            "action": "create_story",
                            "method": "schema_processor",
                            "created_files": [schema_result["file_created"]],
                            "story_info": story_info,
                            "schema_result": schema_result
                        }
            except Exception as e:
                print(f"Schema processor failed, using manual creation: {e}")
        
        # Manual story creation
        story_file = self._create_story_manually(story_info, banking_context)
        
        return {
            "action": "create_story",
            "method": "manual_creation",
            "created_files": [story_file] if story_file else [],
            "story_info": story_info,
            "banking_context": banking_context
        }
    
    def _auto_detect_and_create(self, prompt: str, banking_context: Dict[str, Any], entities: Dict[str, Any]) -> Dict[str, Any]:
        """Auto-detect specification type and create appropriately."""
        prompt_lower = prompt.lower()
        
        # Epic detection
        if any(keyword in prompt_lower for keyword in ["platform", "system", "transformation", "initiative"]):
            return self.create_epic(prompt, banking_context, entities)
        
        # Feature detection
        elif any(keyword in prompt_lower for keyword in ["feature", "capability", "functionality"]):
            return self.create_feature(prompt, banking_context, entities)
        
        # Story detection
        elif any(keyword in prompt_lower for keyword in ["story", "requirement", "task", "user"]):
            return self.create_story(prompt, banking_context, entities)
        
        # Default to feature if banking context
        elif banking_context.get("is_banking"):
            return self.create_feature(prompt, banking_context, entities)
        
        # Default to story
        else:
            return self.create_story(prompt, banking_context, entities)
    
    def _extract_epic_info(self, prompt: str, banking_context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract epic information from prompt."""
        import re
        
        # Extract title
        title_patterns = [
            r"epic (?:for |to )?(.+?)(?:\s|$)",
            r"create (?:an? )?epic (?:for |to )?(.+?)(?:\s|$)",
            r"(.+?)\s*epic",
        ]
        
        title = "New Epic"
        for pattern in title_patterns:
            match = re.search(pattern, prompt, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                break
        
        return {
            "title": title,
            "objective": f"Implement {title}",
            "banking_domain": banking_context.get("primary_product", ""),
            "compliance_requirements": banking_context.get("compliance_areas", []),
            "owner": "TBD"
        }
    
    def _extract_feature_info(self, prompt: str, banking_context: Dict[str, Any], entities: Dict[str, Any]) -> Dict[str, Any]:
        """Extract feature information from prompt."""
        import re
        
        # Extract title
        title_patterns = [
            r"feature (?:for |to )?(.+?)(?:\s+under|\s*$)",
            r"create (?:a |an )?feature (?:for |to )?(.+?)(?:\s+under|\s*$)",
            r"add (?:a |an )?feature (?:for |to )?(.+?)(?:\s+under|\s*$)"
        ]
        
        title = "New Feature"
        for pattern in title_patterns:
            match = re.search(pattern, prompt, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                break
        
        # Extract parent epic
        parent_epic = None
        epic_refs = entities.get("epic_references", [])
        if epic_refs:
            parent_epic = epic_refs[0]
        else:
            epic_match = re.search(r"(?:under epic|epic)\s+([EF]\d{3})", prompt, re.IGNORECASE)
            if epic_match:
                parent_epic = epic_match.group(1).upper()
        
        return {
            "title": title,
            "parent_epic": parent_epic,
            "product_type": banking_context.get("primary_product", "").title() if banking_context.get("primary_product") else None,
            "goal": title,
            "banking_context": banking_context,
            "compliance_requirements": banking_context.get("compliance_areas", [])
        }
    
    def _extract_story_info(self, prompt: str, banking_context: Dict[str, Any], entities: Dict[str, Any]) -> Dict[str, Any]:
        """Extract story information from prompt."""
        import re
        
        # Extract title
        title_patterns = [
            r"story (?:for |to )?(.+?)(?:\s+under|\s*$)",
            r"create (?:a |an )?story (?:for |to )?(.+?)(?:\s+under|\s*$)",
            r"add (?:a |an )?story (?:for |to )?(.+?)(?:\s+under|\s*$)"
        ]
        
        title = "New Story"
        for pattern in title_patterns:
            match = re.search(pattern, prompt, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                break
        
        # Extract parent feature
        parent_feature = None
        feature_refs = entities.get("feature_references", [])
        if feature_refs:
            parent_feature = feature_refs[0]
        else:
            feature_match = re.search(r"(?:under feature|feature)\s+([F]\d{3})", prompt, re.IGNORECASE)
            if feature_match:
                parent_feature = feature_match.group(1).upper()
        
        # Extract stakeholder
        stakeholder = "user"
        if entities.get("stakeholders"):
            stakeholder = entities["stakeholders"][0]
        
        return {
            "title": title,
            "parent_feature": parent_feature,
            "stakeholder": stakeholder,
            "compliance_context": banking_context.get("compliance_areas", []),
            "banking_context": banking_context
        }
    
    def _create_epic_manually(self, epic_info: Dict[str, Any]) -> Optional[str]:
        """Create epic file manually if schema processor unavailable."""
        try:
            # Generate epic ID
            epic_id = self._get_next_epic_id()
            filename = f"{epic_id}-{self._slugify(epic_info['title'])}.md"
            filepath = project_root / "specs" / "epics" / filename
            
            # Ensure directory exists
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            # Create content
            content = f"""# Epic: {epic_info['title']}

**ID:** {epic_id}  
**Objective:** {epic_info['objective']}  
**Owner:** {epic_info['owner']}  
**Linked Features:** TBD  

## Business Context
{epic_info['objective']}

## Success Criteria
- Define measurable success criteria
- Include user impact metrics
- Specify completion conditions

## Banking Domain Context
- **Primary Product**: {epic_info.get('banking_domain', 'TBD')}
- **Compliance Requirements**: {', '.join(epic_info.get('compliance_requirements', []))}

## Created
Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} via Spec Agent

"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Created epic: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error creating epic manually: {e}")
            return None
    
    def _create_feature_manually(self, feature_info: Dict[str, Any], banking_context: Dict[str, Any]) -> Optional[str]:
        """Create feature file manually if schema processor unavailable."""
        try:
            # Generate feature ID
            feature_id = self._get_next_feature_id()
            filename = f"{feature_id}-{self._slugify(feature_info['title'])}.md"
            filepath = project_root / "specs" / "features" / filename
            
            # Ensure directory exists
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            # Create content
            product_section = ""
            if feature_info.get("product_type"):
                product_section = f"""
## Banking Product Type
**{feature_info['product_type']}**"""
            
            compliance_section = ""
            if feature_info.get("compliance_requirements"):
                compliance_section = f"""
## Compliance Requirements
{chr(10).join([f"- {req}" for req in feature_info['compliance_requirements']])}"""
            
            content = f"""# {"Banking " if banking_context.get("is_banking") else ""}Feature: {feature_info['title']}

**ID:** {feature_id}  
**Epic:** {feature_info.get('parent_epic', 'TBD')}  
**Product Type:** {feature_info.get('product_type', 'TBD')}  
**Linked Stories:** TBD  
{product_section}

## Goal
{feature_info['goal']}

## Business Value
- Define business impact and value proposition
- Specify customer experience improvements
- Include revenue or cost optimization goals

## Technical Requirements
- Define technical specifications and architecture
- List integration requirements with core banking systems
- Specify performance and scalability criteria
{compliance_section}

## Acceptance Criteria
- Define feature completion criteria
- Include user acceptance tests
- Specify quality gates and performance benchmarks

## Created
Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} via Spec Agent

"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Created feature: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error creating feature manually: {e}")
            return None
    
    def _create_story_manually(self, story_info: Dict[str, Any], banking_context: Dict[str, Any]) -> Optional[str]:
        """Create story file manually if schema processor unavailable."""
        try:
            # Generate story ID
            story_id = self._get_next_story_id()
            filename = f"{story_id}-{self._slugify(story_info['title'])}.md"
            filepath = project_root / "specs" / "stories" / filename
            
            # Ensure directory exists
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            # Determine story type
            is_compliance = bool(story_info.get("compliance_context"))
            story_type = "Compliance Story" if is_compliance else "User Story"
            
            # Create content
            compliance_section = ""
            if is_compliance:
                compliance_section = f"""
## Regulatory Context
This story ensures compliance with {', '.join(story_info['compliance_context'])} requirements.

## Compliance Requirements
{chr(10).join([f"- {req} compliance validation" for req in story_info['compliance_context']])}"""
            
            user_story_section = f"""
## User Story
As a **{story_info['stakeholder']}**, I want to **{story_info['title']}** so that I can **achieve business value**.
""" if not is_compliance else ""
            
            content = f"""# {story_type}: {story_info['title']}

**ID:** {story_id}  
**Feature:** {story_info.get('parent_feature', 'TBD')}  
{user_story_section}{compliance_section}

## Acceptance Criteria
- Define specific acceptance criteria
- Include testable conditions
- Specify success metrics

## Tasks
1. Define implementation steps
2. Add technical tasks
3. Include testing requirements

## Definition of Done
- Code is implemented and tested
- Documentation is updated
- Feature is deployed and verified
{"- Compliance requirements validated" if is_compliance else ""}

## Created
Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} via Spec Agent

"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Created story: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error creating story manually: {e}")
            return None
    
    def _get_next_epic_id(self) -> str:
        """Get next available epic ID."""
        return self._get_next_id("epic", "E")
    
    def _get_next_feature_id(self) -> str:
        """Get next available feature ID."""
        return self._get_next_id("feature", "F")
    
    def _get_next_story_id(self) -> str:
        """Get next available story ID."""
        return self._get_next_id("story", "S")
    
    def _get_next_id(self, spec_type: str, prefix: str) -> str:
        """Get next available ID for spec type."""
        try:
            spec_dir = project_root / "specs" / f"{spec_type}s"
            if not spec_dir.exists():
                return f"{prefix}001"
            
            # Find existing IDs
            import re
            existing_ids = []
            for file_path in spec_dir.glob(f"{prefix}*.md"):
                match = re.match(f"{prefix}(\d+)", file_path.stem)
                if match:
                    existing_ids.append(int(match.group(1)))
            
            next_id = max(existing_ids, default=0) + 1
            return f"{prefix}{next_id:03d}"
            
        except Exception:
            return f"{prefix}001"
    
    def _slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug."""
        import re
        return re.sub(r'[^\w\s-]', '', text).strip().replace(' ', '-')
    
    def get_spec_agent_status(self) -> Dict[str, Any]:
        """Get current spec agent status."""
        return {
            "agent_id": self.agent_id,
            "version": self.version,
            "status": "active",
            "schema_processor_available": self.schema_processor is not None,
            "supported_actions": ["create_epic", "create_feature", "create_story"],
            "inputs": ["specs/prompt_schema.json"],
            "outputs": ["specs/**"],
            "banking_domain_support": True,
            "compliance_story_support": True
        }


def main():
    """CLI interface for the spec agent."""
    import argparse
    
    parser = argparse.ArgumentParser(description="PromptToProduct Spec Agent")
    parser.add_argument("prompt", nargs="?", help="Prompt to process")
    parser.add_argument("--status", action="store_true", help="Show spec agent status")
    parser.add_argument("--intent", choices=["create_epic", "create_feature", "create_story"], 
                       help="Specify intent explicitly")
    args = parser.parse_args()
    
    # Initialize spec agent
    spec_agent = SpecAgent()
    
    if args.status:
        status = spec_agent.get_spec_agent_status()
        print("📝 Spec Agent Status")
        print("=" * 40)
        for key, value in status.items():
            print(f"{key}: {value}")
        return
    
    if not args.prompt:
        print("Usage: python spec_agent.py '<prompt>' or --status")
        return
    
    # Prepare agent parameters (simulating orchestrator input)
    agent_params = {
        "prompt": args.prompt,
        "intent": args.intent or "auto_detect",
        "banking_context": {"is_banking": False, "product_types": [], "compliance_areas": []},
        "entities": {"epic_references": [], "feature_references": [], "story_references": [], 
                    "technologies": [], "stakeholders": []}
    }
    
    # Process the specification request
    print(f"📝 Processing: {args.prompt}")
    print("-" * 50)
    
    result = spec_agent.process_specification_request(agent_params)
    
    # Display results
    print(f"✅ Action: {result.get('action', 'unknown')}")
    print(f"📁 Files Created: {len(result.get('created_files', []))}")
    
    for file_path in result.get('created_files', []):
        print(f"   📄 {file_path}")
    
    if result.get('errors'):
        print(f"❌ Errors: {', '.join(result['errors'])}")
    
    print(f"🔧 Method: {result.get('method', 'unknown')}")
    print(f"📊 Status: {result.get('status', 'unknown')}")


if __name__ == "__main__":
    main()