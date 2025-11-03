#!/usr/bin/env python3
"""
Spec Agent - Converts Developer Prompts into Structured Markdown Specs

This agent specializes in converting natural language prompts into structured
specifications (epics, features, stories) with banking domain intelligence.
Enhanced with GitHub MCP integration for seamless repository synchronization.
Includes Gherkin feature file generation for BDD testing.
"""
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import re

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from specs.schema_processor import PromptToProductSchema
except ImportError:
    print("Warning: Could not import schema processor. Some functionality may be limited.")
    PromptToProductSchema = None

try:
    from src.config import get_github_config, get_system_config
    CONFIG_AVAILABLE = True
except ImportError:
    print("Warning: Could not import config system.")
    CONFIG_AVAILABLE = False

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
                print(f"✅ Schema processor initialized successfully with banking domain intelligence")
                print(f"   📋 Product types: {len(self.schema_processor.banking_domain.get('product_types', {}))}, Actions: {len(self.schema_processor.actions)}")
            except Exception as e:
                print(f"Warning: Schema processor initialization failed: {e}")
                self.schema_processor = None
        else:
            print("⚠️ Schema processor not available - using manual specification creation")
    
    def process_specification_request(self, agent_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for processing specification requests.
        
        Args:
            agent_params: Parameters from orchestrator including prompt, intent, etc.
            
        Returns:
            Processing result with created specifications and GitHub MCP integration data
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
            "github_mcp_data": [],
            "spec_type": None,
            "errors": []
        }
        
        try:
            # Handle complete workflow intent specifically
            if intent == "complete_workflow":
                print("📋 Complete Workflow: Creating comprehensive specifications...")
                spec_result = self._create_complete_workflow_specs(prompt, banking_context, entities)
                result["spec_type"] = spec_result.get("detected_type", "complete_workflow")
            # Route to appropriate creation method
            elif intent in ["create_epic"] or "epic" in prompt.lower():
                spec_result = self.create_epic(prompt, banking_context, entities)
                result["spec_type"] = "epic"
            elif intent in ["create_feature"] or "feature" in prompt.lower():
                spec_result = self.create_feature(prompt, banking_context, entities)
                result["spec_type"] = "feature"
            elif intent in ["create_story"] or "story" in prompt.lower():
                spec_result = self.create_story(prompt, banking_context, entities)
                result["spec_type"] = "story"
            else:
                # Auto-detect based on content and context
                spec_result = self._auto_detect_and_create(prompt, banking_context, entities)
                result["spec_type"] = spec_result.get("detected_type", "unknown")
            
            result.update(spec_result)
            result["status"] = "completed"
            
            # Gherkin feature files are now generated as part of story creation process
            
            # Prepare GitHub MCP integration data
            if result.get("created_files"):
                result["github_mcp_data"] = self._prepare_github_mcp_data(result)
            
        except Exception as e:
            result["status"] = "error"
            result["errors"].append(str(e))
            print(f"❌ Error in spec processing: {e}")
        
        return result
    
    def create_epic(self, prompt: str, banking_context: Dict[str, Any], entities: Dict[str, Any]) -> Dict[str, Any]:
        """Create an epic specification from prompt."""
        print("📋 Creating Epic Specification...")
        
        # Extract epic information for fallback
        epic_info = self._extract_epic_info(prompt, banking_context)
        
        if self.schema_processor:
            try:
                # Use schema processor with comprehensive banking intelligence
                print("   🧠 Using schema processor with banking domain intelligence")
                schema_result = self.schema_processor.process_prompt(prompt)
                
                if schema_result.get("success") and schema_result.get("file_created"):
                    print(f"   ✅ Schema processor created: {schema_result.get('file_created')}")
                    print(f"   🏦 Banking context: {schema_result.get('banking_context', {}).get('is_banking', False)}")
                    
                    return {
                        "action": "create_epic",
                        "method": "schema_processor",
                        "created_files": [schema_result["file_created"]],
                        "epic_info": epic_info,
                        "schema_result": schema_result,
                        "banking_intelligence": schema_result.get("banking_context", {}),
                        "compliance_context": schema_result.get("compliance_requirements", [])
                    }
                else:
                    print(f"   ⚠️ Schema processor failed: {schema_result.get('errors', ['Unknown error'])}")
            except Exception as e:
                print(f"   ❌ Schema processor error: {e}")
        
        # Fallback to manual epic creation
        print("   🔧 Using manual epic creation")
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
        
        # Extract feature information for fallback
        feature_info = self._extract_feature_info(prompt, banking_context, entities)
        
        if self.schema_processor:
            try:
                # Use schema processor with intelligent banking detection
                print("   🧠 Analyzing prompt with banking domain intelligence")
                schema_result = self.schema_processor.process_prompt(prompt)
                
                if schema_result.get("success") and schema_result.get("file_created"):
                    detected_action = schema_result.get("detected_action", {}).get("action", "create_feature")
                    is_banking = schema_result.get("banking_context", {}).get("is_banking", False)
                    
                    print(f"   ✅ Schema processor created: {schema_result.get('file_created')}")
                    print(f"   🎯 Detected action: {detected_action}")
                    print(f"   🏦 Banking context: {is_banking}")
                    
                    return {
                        "action": "create_banking_feature" if is_banking else "create_feature",
                        "method": "schema_processor",
                        "created_files": [schema_result["file_created"]],
                        "feature_info": feature_info,
                        "banking_context": schema_result.get("banking_context", {}),
                        "schema_result": schema_result,
                        "detected_action": detected_action,
                        "compliance_context": schema_result.get("compliance_requirements", []),
                        "title": feature_info["title"],
                        "prompt": prompt
                    }
                else:
                    print(f"   ⚠️ Schema processor failed: {schema_result.get('errors', ['Unknown error'])}")
            except Exception as e:
                print(f"   ❌ Schema processor error: {e}")
        
        # Fallback to manual feature creation
        print("   🔧 Using manual feature creation")
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
        
        # Extract story information for fallback
        story_info = self._extract_story_info(prompt, banking_context, entities)
        
        if self.schema_processor:
            try:
                # Use schema processor with compliance intelligence
                print("   🧠 Analyzing prompt for compliance and banking context")
                schema_result = self.schema_processor.process_prompt(prompt)
                
                if schema_result.get("success") and schema_result.get("file_created"):
                    detected_action = schema_result.get("detected_action", {}).get("action", "create_story")
                    compliance_reqs = schema_result.get("compliance_requirements", [])
                    is_compliance = detected_action == "create_compliance_story" or len(compliance_reqs) > 0
                    
                    print(f"   ✅ Schema processor created: {schema_result.get('file_created')}")
                    print(f"   🎯 Detected action: {detected_action}")
                    print(f"   📋 Compliance focus: {is_compliance}")
                    
                    if compliance_reqs:
                        print(f"   ⚖️ Compliance requirements: {', '.join(compliance_reqs)}")
                    
                    # Generate integrated Gherkin feature files for the story
                    story_result = {
                        "action": "create_compliance_story" if is_compliance else "create_story",
                        "method": "schema_processor",
                        "created_files": [schema_result["file_created"]],
                        "story_info": story_info,
                        "compliance_context": compliance_reqs,
                        "banking_context": schema_result.get("banking_context", {}),
                        "schema_result": schema_result,
                        "detected_action": detected_action,
                        "title": story_info["title"],
                        "prompt": prompt,
                        "spec_type": "story"
                    }
                    
                    # Generate Gherkin feature files as integral part of story creation
                    gherkin_files = self._generate_story_gherkin_files(story_result, prompt, schema_result.get("banking_context", {}))
                    if gherkin_files:
                        story_result["created_files"].extend(gherkin_files)
                        story_result["gherkin_files"] = gherkin_files
                        print(f"   ✅ Generated {len(gherkin_files)} integrated Gherkin feature file(s)")
                    
                    return story_result
                else:
                    print(f"   ⚠️ Schema processor failed: {schema_result.get('errors', ['Unknown error'])}")
            except Exception as e:
                print(f"   ❌ Schema processor error: {e}")
        
        # Fallback to manual story creation
        print("   🔧 Using manual story creation")
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
        
        # Extract title with improved regex patterns
        title_patterns = [
            r"create (?:an? )?epic (?:for |to )?(.+?)(?:\s+with|\s+using|\s*$)",  # More specific pattern first
            r"epic (?:for |to )?(.+?)(?:\s+with|\s+using|\s*$)",  # Capture everything until 'with' or end
            r"(?:create|add|build) (?:an? )?(.+?)\s*epic",  # Reverse pattern
            r"(.+?)\s*(?:epic|platform|system)"  # Fallback pattern
        ]
        
        title = "New Epic"
        prompt_clean = prompt.strip()
        
        for pattern in title_patterns:
            match = re.search(pattern, prompt_clean, re.IGNORECASE)
            if match:
                extracted_title = match.group(1).strip()
                # Clean up common words and improve title
                extracted_title = re.sub(r'^(?:a|an|the)\s+', '', extracted_title, flags=re.IGNORECASE)
                if len(extracted_title) > 3:  # Avoid too short titles
                    title = extracted_title
                    break
        
        # If still generic, try extracting key concepts
        if title == "New Epic":
            # Extract key banking/technical terms
            key_terms = re.findall(r'\b(?:loan|credit|fraud|detection|payment|banking|origination|platform|system|AI|risk|assessment)\b', prompt, re.IGNORECASE)
            if key_terms:
                title = ' '.join(key_terms[:3]).title()  # Use first 3 key terms
        
        return {
            "title": title,
            "objective": f"Implement {title}",
            "banking_domain": banking_context.get("primary_product", ""),
            "compliance_requirements": banking_context.get("compliance_areas", []),
            "owner": os.getenv("DEFAULT_OWNER", "TBD"),
            "assigned_to": os.getenv("DEFAULT_ASSIGNEE", "TBD"),
            "created_by": os.getenv("SYSTEM_USER", "PromptToProduct-Agent"),
            "priority": os.getenv("DEFAULT_PRIORITY", "Medium"),
            "status": os.getenv("DEFAULT_STATUS", "In Progress")
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
            "compliance_requirements": banking_context.get("compliance_areas", []),
            "owner": os.getenv("DEFAULT_OWNER", "TBD"),
            "assigned_to": os.getenv("DEFAULT_ASSIGNEE", "TBD"),
            "created_by": os.getenv("SYSTEM_USER", "PromptToProduct-Agent"),
            "priority": os.getenv("DEFAULT_PRIORITY", "Medium"),
            "status": os.getenv("DEFAULT_STATUS", "In Progress")
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
            "banking_context": banking_context,
            "owner": os.getenv("DEFAULT_OWNER", "TBD"),
            "assigned_to": os.getenv("DEFAULT_ASSIGNEE", "TBD"),
            "created_by": os.getenv("SYSTEM_USER", "PromptToProduct-Agent"),
            "priority": os.getenv("DEFAULT_PRIORITY", "Medium"),
            "status": os.getenv("DEFAULT_STATUS", "In Progress")
        }
    
    def _create_epic_manually(self, epic_info: Dict[str, Any]) -> Optional[str]:
        """Create epic file manually if schema processor unavailable."""
        try:
            # Generate epic ID and meaningful filename
            epic_id = self._get_next_epic_id()
            meaningful_name = self._generate_meaningful_name(epic_info['title'], epic_info.get('banking_domain'), 'epic')
            filename = f"{epic_id}-{meaningful_name}.md"
            filepath = project_root / "specs" / "epics" / filename
            
            # Ensure directory exists
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            # Create content
            content = f"""# Epic: {epic_info['title']}

**ID:** {epic_id}  
**Objective:** {epic_info['objective']}  
**Owner:** {epic_info['owner']}  
**Assigned To:** {epic_info['assigned_to']}  
**Priority:** {epic_info['priority']}  
**Status:** {epic_info['status']}  
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

## Metadata
**Created By:** {epic_info['created_by']}  
**Created:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Last Modified:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  

"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Created epic: {filepath}")
            
            # Create GitHub issue and file if configured
            github_result = self._sync_with_github(str(filepath), epic_info, "epic")
            if github_result:
                print(f"🚀 GitHub sync: {github_result}")
            
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error creating epic manually: {e}")
            return None
    
    def _create_feature_manually(self, feature_info: Dict[str, Any], banking_context: Dict[str, Any]) -> Optional[str]:
        """Create feature file manually if schema processor unavailable."""
        try:
            # Generate feature ID and meaningful filename
            feature_id = self._get_next_feature_id()
            meaningful_name = self._generate_meaningful_name(
                feature_info['title'], 
                banking_context.get('product_types', [None])[0], 
                'feature'
            )
            filename = f"{feature_id}-{meaningful_name}.md"
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
**Owner:** {feature_info['owner']}  
**Assigned To:** {feature_info['assigned_to']}  
**Priority:** {feature_info['priority']}  
**Status:** {feature_info['status']}  
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

## Metadata
**Created By:** {feature_info['created_by']}  
**Created:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Last Modified:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  

"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Created feature: {filepath}")
            
            # Create GitHub issue and file if configured
            github_result = self._sync_with_github(str(filepath), feature_info, "feature")
            if github_result:
                print(f"🚀 GitHub sync: {github_result}")
            
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error creating feature manually: {e}")
            return None
    
    def _create_story_manually(self, story_info: Dict[str, Any], banking_context: Dict[str, Any]) -> Optional[str]:
        """Create story file manually if schema processor unavailable."""
        try:
            # Generate story ID and meaningful filename
            story_id = self._get_next_story_id()
            meaningful_name = self._generate_meaningful_name(
                story_info['title'], 
                banking_context.get('product_types', [None])[0], 
                'story'
            )
            filename = f"{story_id}-{meaningful_name}.md"
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
**Owner:** {story_info['owner']}  
**Assigned To:** {story_info['assigned_to']}  
**Priority:** {story_info['priority']}  
**Status:** {story_info['status']}  
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

## Metadata
**Created By:** {story_info['created_by']}  
**Created:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Last Modified:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  

"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Created story: {filepath}")
            
            # Create GitHub issue and file if configured
            github_result = self._sync_with_github(str(filepath), story_info, "story")
            if github_result:
                print(f"🚀 GitHub sync: {github_result}")
            
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
    
    def _generate_meaningful_name(self, title: str, domain: str = None, spec_type: str = "spec") -> str:
        """Generate meaningful filename based on title and domain context."""
        # Clean and extract key terms from title
        title_clean = self._slugify(title.lower())
        
        # Banking domain keywords mapping
        domain_keywords = {
            'loans': ['loan', 'lending', 'credit', 'mortgage', 'personal-loan', 'auto-loan'],
            'payments': ['payment', 'transfer', 'transaction', 'p2p', 'wire', 'ach'],
            'accounts': ['account', 'checking', 'savings', 'deposit', 'withdrawal'],
            'cards': ['card', 'credit-card', 'debit', 'rewards', 'cashback'],
            'investments': ['investment', 'portfolio', 'trading', 'wealth', 'advisory'],
            'compliance': ['kyc', 'aml', 'compliance', 'audit', 'regulatory'],
            'security': ['security', 'fraud', 'authentication', 'authorization', '2fa'],
            'mobile': ['mobile', 'app', 'ios', 'android', 'responsive'],
            'api': ['api', 'integration', 'webhook', 'rest', 'graphql']
        }
        
        # Extract meaningful keywords from title
        meaningful_parts = []
        
        # Add domain prefix if banking domain detected
        if domain and domain.lower() in domain_keywords:
            meaningful_parts.append(domain.lower())
        
        # Extract key business terms from title
        title_words = title_clean.split('-')
        business_terms = []
        for word in title_words:
            if len(word) > 2 and word not in ['the', 'and', 'for', 'with', 'of', 'to', 'in', 'on', 'at']:
                business_terms.append(word)
        
        # Take first 3-4 most meaningful words
        if business_terms:
            meaningful_parts.extend(business_terms[:3])
        else:
            # Fallback to first few words of title
            meaningful_parts.extend(title_words[:3])
        
        # Create final meaningful name
        meaningful_name = '-'.join(meaningful_parts)
        
        # Ensure reasonable length (max 50 chars)
        if len(meaningful_name) > 50:
            meaningful_name = meaningful_name[:47] + '...'
        
        return meaningful_name
    
    def _sync_with_github(self, filepath: str, spec_info: Dict[str, Any], spec_type: str) -> Optional[Dict[str, Any]]:
        """Sync specification with GitHub repository via MCP integration."""
        try:
            # Check if GitHub integration is available and enabled
            if not CONFIG_AVAILABLE:
                return None
                
            github_config = get_github_config()
            system_config = get_system_config()
            
            # Check if GitHub is configured and auto-sync is enabled
            if not github_config.is_configured or not system_config.auto_sync_github:
                return None
            
            # Read the created file content
            with open(filepath, 'r', encoding='utf-8') as f:
                file_content = f.read()
            
            # Create meaningful GitHub issue title and body
            issue_title = self._create_github_issue_title(spec_info, spec_type)
            issue_body = self._create_github_issue_body(spec_info, spec_type, filepath)
            
            # Generate relative path for GitHub
            relative_path = str(Path(filepath).relative_to(project_root))
            
            result = {
                "spec_file": relative_path,
                "spec_type": spec_type,
                "issue_title": issue_title,
                "issue_body": issue_body,
                "file_content": file_content,
                "repo_owner": github_config.repo_owner,
                "repo_name": github_config.repo_name,
                "github_integration": "ready"
            }
            
            # Prepare data for GitHub MCP integration
            if CONFIG_AVAILABLE:
                github_config = get_github_config()
                mcp_data = self._prepare_github_mcp_data_simple(result, github_config, relative_path, file_content)
                if mcp_data:
                    result.update(mcp_data)
            
            print(f"📋 GitHub integration prepared for {spec_type}: {issue_title}")
            return result
            
        except Exception as e:
            print(f"⚠️ GitHub sync warning: {e}")
            return None
    
    def _prepare_github_mcp_data_simple(self, result: Dict[str, Any], github_config, relative_path: str, file_content: str) -> Optional[Dict[str, Any]]:
        """Prepare data structure for GitHub MCP server integration."""
        try:
            # Prepare file creation data
            mcp_file_data = {
                "owner": github_config.repo_owner,
                "repo": github_config.repo_name, 
                "path": relative_path,
                "content": file_content,
                "message": f"Add {result.get('spec_type', 'specification')} specification: {result.get('issue_title', 'New spec')}",
                "branch": "main"  # Could be configurable
            }
            
            # Prepare issue creation data
            mcp_issue_data = {
                "owner": github_config.repo_owner,
                "repo": github_config.repo_name,
                "title": result.get("issue_title", "New Specification"),
                "body": result.get("issue_body", "Auto-generated specification"),
                "labels": self._generate_github_labels(result.get("spec_type", "unknown"))
            }
            
            return {
                "mcp_file_data": mcp_file_data,
                "mcp_issue_data": mcp_issue_data
            }
        except Exception as e:
            print(f"Error preparing MCP data: {e}")
            return None
    
    def _generate_github_labels(self, spec_type: str) -> List[str]:
        """Generate appropriate GitHub labels for the spec type."""
        labels = [spec_type, "specification", "auto-generated"]
        
        # Add banking-specific labels
        labels.extend(["banking", "fintech"])
        
        return labels
    
    def _create_github_issue_title(self, spec_info: Dict[str, Any], spec_type: str) -> str:
        """Create meaningful GitHub issue title."""
        title = spec_info.get('title', 'Untitled Specification')
        
        # Add spec type prefix
        type_prefix = {
            'epic': '🎯 Epic:',
            'feature': '🔧 Feature:',
            'story': '📝 Story:'
        }.get(spec_type, '📄 Spec:')
        
        # Add banking domain context if available
        domain_context = ""
        if 'banking_domain' in spec_info:
            domain_context = f" [{spec_info['banking_domain'].title()}]"
        elif 'banking_context' in spec_info and spec_info['banking_context'].get('product_types'):
            domain_context = f" [{spec_info['banking_context']['product_types'][0].title()}]"
        
        return f"{type_prefix} {title}{domain_context}"
    
    def _create_github_issue_body(self, spec_info: Dict[str, Any], spec_type: str, filepath: str) -> str:
        """Create comprehensive GitHub issue body."""
        relative_path = str(Path(filepath).relative_to(project_root))
        
        body = f"""## {spec_type.title()} Specification

**Specification File:** `{relative_path}`
**Created:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Priority:** {spec_info.get('priority', 'Medium')}
**Status:** {spec_info.get('status', 'In Progress')}

### Overview
{spec_info.get('objective', spec_info.get('goal', 'Specification details to be defined'))}

### Banking Context
"""
        
        # Add banking domain information
        if 'banking_context' in spec_info and spec_info['banking_context']:
            context = spec_info['banking_context']
            if context.get('product_types'):
                body += f"- **Product Types:** {', '.join(context['product_types'])}\n"
            if context.get('compliance_areas'):
                body += f"- **Compliance Areas:** {', '.join(context['compliance_areas'])}\n"
        
        body += f"""
### Acceptance Criteria
- [ ] Specification review completed
- [ ] Technical requirements defined
- [ ] Compliance requirements validated
- [ ] Implementation plan approved

### Labels
`{spec_type}`, `specification`, `{spec_info.get('priority', 'medium').lower()}-priority`"""

        # Add banking domain labels
        if 'banking_domain' in spec_info:
            body += f", `{spec_info['banking_domain'].lower()}`"
        
        return body
    
    def _prepare_github_mcp_data(self, result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Prepare GitHub MCP integration data for file creation and issue management.
        
        Args:
            result: The processing result containing created files and spec information
            
        Returns:
            List of MCP integration data items
        """
        mcp_data_items = []
        
        try:
            if CONFIG_AVAILABLE:
                github_config = get_github_config()
                
                for file_path in result.get("created_files", []):
                    # Read the created file content
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            file_content = f.read()
                    except Exception as e:
                        print(f"Warning: Could not read file {file_path}: {e}")
                        continue
                    
                    # Convert absolute path to relative path for GitHub
                    file_path_obj = Path(file_path)
                    try:
                        relative_path = str(file_path_obj.relative_to(project_root))
                    except ValueError:
                        relative_path = f"specs/{file_path_obj.name}"
                    
                    # Prepare file data for MCP
                    mcp_file_data = {
                        "owner": github_config.repo_owner,
                        "repo": github_config.repo_name,
                        "path": relative_path,
                        "content": file_content,
                        "message": f"Add {result.get('spec_type', 'specification')}: {self._extract_title_from_content(file_content)}",
                        "branch": "main"
                    }
                    
                    # Prepare issue data for MCP
                    mcp_issue_data = {
                        "owner": github_config.repo_owner,
                        "repo": github_config.repo_name,
                        "title": f"📝 {result.get('spec_type', 'Specification').title()}: {self._extract_title_from_content(file_content)}",
                        "body": self._generate_github_issue_body(result, relative_path, file_content),
                        "labels": self._generate_github_labels(result)
                    }
                    
                    mcp_data_items.append({
                        "spec_file": relative_path,
                        "spec_type": result.get("spec_type", "unknown"),
                        "mcp_file_data": mcp_file_data,
                        "mcp_issue_data": mcp_issue_data,
                        "issue_title": mcp_issue_data["title"]
                    })
                    
        except Exception as e:
            print(f"Warning: Could not prepare GitHub MCP data: {e}")
        
        return mcp_data_items
    
    def _extract_title_from_content(self, content: str) -> str:
        """
        Extract title from markdown content.
        
        Args:
            content: Markdown content
            
        Returns:
            Extracted title or default
        """
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                return line[2:].strip()
            elif line.startswith('**') and line.endswith('**'):
                return line[2:-2].strip()
        return "New Specification"
    
    def _generate_github_issue_body(self, result: Dict[str, Any], file_path: str, content: str) -> str:
        """
        Generate GitHub issue body for the specification with embedded feature files for stories.
        
        Args:
            result: Processing result
            file_path: Relative file path
            content: File content
            
        Returns:
            GitHub issue body with embedded feature files
        """
        title = self._extract_title_from_content(content)
        spec_type = result.get("spec_type", "specification").title()
        
        body = f"""## {spec_type} Created: {title}

**File:** `{file_path}`
**Type:** {spec_type}
**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Agent:** {self.agent_id}

### Overview
This {spec_type.lower()} was automatically generated from the prompt:
> {result.get('input_prompt', 'N/A')}

### Banking Context"""
        
        banking_context = result.get("banking_context", {})
        if banking_context.get("is_banking"):
            if banking_context.get("products"):
                body += f"\n- **Products:** {', '.join(banking_context['products'])}"
            if banking_context.get("compliance"):
                body += f"\n- **Compliance:** {', '.join(banking_context['compliance'])}"
        else:
            body += "\n- No specific banking context detected"
        
        # Add embedded feature files for stories
        if spec_type.lower() == "story" and result.get("gherkin_files"):
            body += "\n\n### 🧪 Acceptance Criteria (BDD Feature Files)\n"
            body += "The following Gherkin feature files define the acceptance criteria for this story:\n\n"
            
            # Embed main feature file content
            main_feature_info = result.get("main_feature_file")
            if main_feature_info and main_feature_info.get("content"):
                story_id = main_feature_info.get("story_id", "Story")
                relative_path = main_feature_info.get("relative_path", "")
                body += f"#### 🎯 Main Feature: {story_id}\n"
                body += f"**File:** `{relative_path}`\n\n"
                body += "```gherkin\n"
                body += main_feature_info["content"]
                body += "```\n\n"
            
            # Embed additional feature files (banking-specific, compliance)
            additional_files = result.get("additional_feature_files", [])
            for file_info in additional_files:
                if isinstance(file_info, dict) and file_info.get("content"):
                    file_type = file_info.get("type", "additional").title()
                    story_id = file_info.get("story_id", "Feature")
                    relative_path = file_info.get("relative_path", "")
                    
                    body += f"#### 🏦 {file_type} Feature: {story_id}\n"
                    body += f"**File:** `{relative_path}`\n\n"
                    body += "```gherkin\n"
                    body += file_info["content"]
                    body += "```\n\n"
        
        body += f"""### Next Steps
- [ ] Review {spec_type.lower()} content
- [ ] Validate requirements and acceptance criteria"""
        
        # Add story-specific next steps
        if spec_type.lower() == "story":
            body += """
- [ ] Review BDD acceptance criteria in feature files
- [ ] Validate scenarios cover all user requirements
- [ ] Ensure feature files are executable with testing framework"""
        
        body += f"""
- [ ] Plan implementation approach
- [ ] Assign to development team
- [ ] Create related specifications if needed

### Links
- Specification file: [`{file_path}`]({file_path})"""
        
        # Add feature file links for stories
        if spec_type.lower() == "story" and result.get("gherkin_files"):
            body += "\n- **Feature Files:**"
            for gherkin_file in result.get("gherkin_files", []):
                # Convert to relative path
                gherkin_path_obj = Path(gherkin_file)
                try:
                    gherkin_relative = str(gherkin_path_obj.relative_to(project_root))
                except ValueError:
                    gherkin_relative = gherkin_file
                body += f"\n  - [`{gherkin_relative}`]({gherkin_relative})"
        
        body += "\n- Generated from prompt using PromptToProduct system"
        body += "\n\n**Auto-generated by PromptToProduct Spec Agent**"
        
        return body
        
        return body
    
    def _generate_github_labels(self, result: Dict[str, Any]) -> List[str]:
        """
        Generate appropriate GitHub labels for the specification.
        
        Args:
            result: Processing result
            
        Returns:
            List of labels
        """
        labels = ["specification", "auto-generated"]
        
        spec_type = result.get("spec_type")
        if spec_type:
            labels.append(spec_type)
        
        # Add banking labels
        banking_context = result.get("banking_context", {})
        if banking_context.get("is_banking"):
            labels.append("banking")
            
            products = banking_context.get("products", [])
            for product in products[:2]:  # Limit to 2 product labels
                labels.append(f"banking-{product}")
            
            compliance = banking_context.get("compliance", [])
            if compliance:
                labels.append("compliance")
        
        # Add priority and type labels
        labels.extend(["medium-priority", "enhancement"])
        
        return labels
    
    def _generate_gherkin_files(self, result: Dict[str, Any], prompt: str, banking_context: Dict[str, Any]) -> List[str]:
        """
        Generate Gherkin feature files for the created specifications.
        
        Args:
            result: Processing result containing created specification files
            prompt: Original prompt for context
            banking_context: Banking domain context
            
        Returns:
            List of created Gherkin feature file paths
        """
        gherkin_files = []
        
        try:
            spec_type = result.get("spec_type", "feature")
            
            # Only generate Gherkin features for stories
            if spec_type == "story":
                print("   📋 Generating Gherkin feature files for story specification...")
                
                # Extract specification information
                spec_info = self._extract_spec_info_for_gherkin(result, prompt, banking_context)
                
                # Generate main feature file
                main_gherkin_file = self._create_main_gherkin_feature(spec_info, spec_type)
                if main_gherkin_file:
                    gherkin_files.append(main_gherkin_file)
                
                # Generate banking-specific scenarios if banking context
                if banking_context.get("is_banking") or self._is_banking_related(prompt):
                    banking_gherkin_files = self._create_banking_gherkin_features(spec_info, spec_type)
                    gherkin_files.extend(banking_gherkin_files)
                
                # Generate compliance scenarios if compliance requirements
                compliance_reqs = self._extract_compliance_requirements(result, banking_context)
                if compliance_reqs:
                    compliance_gherkin_file = self._create_compliance_gherkin_feature(spec_info, compliance_reqs)
                    if compliance_gherkin_file:
                        gherkin_files.append(compliance_gherkin_file)
            else:
                print(f"   ⏭️ Skipping Gherkin generation for {spec_type} - only generating for stories")
            
        except Exception as e:
            print(f"❌ Error generating Gherkin files: {e}")
        
        return gherkin_files
    
    def _generate_story_gherkin_files(self, result: Dict[str, Any], prompt: str, banking_context: Dict[str, Any]) -> List[str]:
        """
        Generate Gherkin feature files specifically for story specifications with same identifier and tags.
        
        Args:
            result: Story processing result containing created specification files
            prompt: Original prompt for context
            banking_context: Banking domain context
            
        Returns:
            List of created Gherkin feature file paths with story identifiers
        """
        gherkin_files = []
        
        try:
            print("   📋 Generating integrated Gherkin feature files for story...")
            
            # Extract story identifier from created files
            story_id = self._extract_story_identifier_from_result(result)
            
            # Extract specification information with story context
            spec_info = self._extract_story_spec_info_for_gherkin(result, prompt, banking_context, story_id)
            
            # Generate main story feature file with same identifier
            main_gherkin_file = self._create_story_gherkin_feature(spec_info, story_id)
            if main_gherkin_file:
                gherkin_files.append(main_gherkin_file)
            
            # Generate banking-specific scenarios if banking context
            if banking_context.get("is_banking") or self._is_banking_related(prompt):
                banking_gherkin_files = self._create_story_banking_gherkin_features(spec_info, story_id)
                gherkin_files.extend(banking_gherkin_files)
            
            # Generate compliance scenarios if compliance requirements
            compliance_reqs = self._extract_compliance_requirements(result, banking_context)
            if compliance_reqs:
                compliance_gherkin_file = self._create_story_compliance_gherkin_feature(spec_info, compliance_reqs, story_id)
                if compliance_gherkin_file:
                    gherkin_files.append(compliance_gherkin_file)
            
        except Exception as e:
            print(f"❌ Error generating story Gherkin files: {e}")
        
        return gherkin_files
    
    def _extract_spec_info_for_gherkin(self, result: Dict[str, Any], prompt: str, banking_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract specification information optimized for Gherkin feature generation.
        
        Args:
            result: Processing result
            prompt: Original prompt
            banking_context: Banking context
            
        Returns:
            Specification information for Gherkin generation
        """
        # Extract title from created files or result
        title = "Feature"
        description = prompt
        
        # Try to extract title from created markdown files
        for file_path in result.get("created_files", []):
            if file_path.endswith(".md"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Extract title from markdown
                    title_match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
                    if title_match:
                        title = title_match.group(1).strip()
                        # Clean up title (remove prefixes like "Epic:", "Feature:")
                        title = re.sub(r'^(?:Epic|Feature|Story):\s*', '', title, flags=re.IGNORECASE)
                        break
                except Exception:
                    continue
        
        # Extract key actors/users
        actors = self._extract_actors_from_prompt(prompt, banking_context)
        
        # Extract key actions/behaviors
        actions = self._extract_actions_from_prompt(prompt)
        
        # Extract business value/outcomes
        outcomes = self._extract_business_outcomes(prompt, banking_context)
        
        return {
            "title": title,
            "description": description,
            "actors": actors,
            "actions": actions,
            "outcomes": outcomes,
            "banking_context": banking_context,
            "spec_type": result.get("spec_type"),
            "prompt": prompt
        }
    
    def _create_main_gherkin_feature(self, spec_info: Dict[str, Any], spec_type: str) -> Optional[str]:
        """
        Create the main Gherkin feature file with meaningful naming and story ID mapping.
        
        Args:
            spec_info: Specification information
            spec_type: Type of specification
            
        Returns:
            Path to created Gherkin feature file
        """
        try:
            # Extract or generate story ID and meaningful name
            story_id = self._extract_or_generate_story_id(spec_info, spec_type)
            meaningful_name = self._generate_feature_file_name(spec_info, story_id)
            filename = f"{story_id}-{meaningful_name}.feature"
            
            # Create featurefiles directory under specs if it doesn't exist
            features_dir = project_root / "specs" / "featurefiles"
            features_dir.mkdir(parents=True, exist_ok=True)
            
            filepath = features_dir / filename
            
            # Generate Gherkin content with story mapping
            content = self._generate_main_gherkin_content(spec_info, spec_type, story_id)
            
            # Write Gherkin file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Created Gherkin feature: {filepath}")
            
            # Store feature file info for GitHub issue integration
            spec_info["main_feature_file"] = {
                "path": str(filepath),
                "story_id": story_id,
                "filename": filename,
                "relative_path": f"specs/featurefiles/{filename}"
            }
            
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error creating main Gherkin feature: {e}")
            return None
    
    def _create_banking_gherkin_features(self, spec_info: Dict[str, Any], spec_type: str) -> List[str]:
        """
        Create banking-specific Gherkin feature files with story ID mapping.
        
        Args:
            spec_info: Specification information
            spec_type: Type of specification
            
        Returns:
            List of created banking Gherkin feature files
        """
        banking_files = []
        
        try:
            banking_context = spec_info.get("banking_context", {})
            base_story_id = spec_info.get("main_feature_file", {}).get("story_id", "S001")
            
            # Create fraud detection scenarios if security-related
            if self._is_security_fraud_related(spec_info["prompt"]):
                fraud_file = self._create_fraud_detection_gherkin(spec_info, f"{base_story_id}-FRAUD")
                if fraud_file:
                    banking_files.append(fraud_file)
            
            # Create loan/credit scenarios if loan-related
            if self._is_loan_credit_related(spec_info["prompt"]):
                loan_file = self._create_loan_processing_gherkin(spec_info, f"{base_story_id}-LOAN")
                if loan_file:
                    banking_files.append(loan_file)
            
            # Create payment scenarios if payment-related
            if self._is_payment_related(spec_info["prompt"]):
                payment_file = self._create_payment_processing_gherkin(spec_info, f"{base_story_id}-PAY")
                if payment_file:
                    banking_files.append(payment_file)
            
            # Store additional feature files for GitHub integration
            spec_info.setdefault("additional_feature_files", []).extend([
                {"path": f, "type": "banking_specific"} for f in banking_files
            ])
            
        except Exception as e:
            print(f"❌ Error creating banking Gherkin features: {e}")
        
        return banking_files
    
    def _create_compliance_gherkin_feature(self, spec_info: Dict[str, Any], compliance_reqs: List[str]) -> Optional[str]:
        """
        Create compliance-focused Gherkin feature file with story ID mapping.
        
        Args:
            spec_info: Specification information
            compliance_reqs: List of compliance requirements
            
        Returns:
            Path to created compliance Gherkin feature file
        """
        try:
            # Generate compliance feature filename with story ID
            base_story_id = spec_info.get("main_feature_file", {}).get("story_id", "S001")
            compliance_story_id = f"{base_story_id}-COMP"
            meaningful_name = self._generate_compliance_feature_name(spec_info, compliance_reqs)
            filename = f"{compliance_story_id}-{meaningful_name}.feature"
            
            # Create compliance featurefiles directory
            compliance_dir = project_root / "specs" / "featurefiles" / "compliance"
            compliance_dir.mkdir(parents=True, exist_ok=True)
            
            filepath = compliance_dir / filename
            
            # Generate compliance Gherkin content with story mapping
            content = self._generate_compliance_gherkin_content(spec_info, compliance_reqs, compliance_story_id)
            
            # Write compliance Gherkin file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Created compliance Gherkin feature: {filepath}")
            
            # Store compliance feature file info
            spec_info.setdefault("additional_feature_files", []).append({
                "path": str(filepath),
                "story_id": compliance_story_id,
                "type": "compliance",
                "relative_path": f"specs/featurefiles/compliance/{filename}"
            })
            
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error creating compliance Gherkin feature: {e}")
            return None
    
    def _generate_main_gherkin_content(self, spec_info: Dict[str, Any], spec_type: str, story_id: str = None) -> str:
        """
        Generate the main Gherkin feature content with story ID mapping.
        
        Args:
            spec_info: Specification information
            spec_type: Type of specification
            story_id: Story ID for mapping
            
        Returns:
            Gherkin feature content
        """
        title = spec_info["title"]
        description = spec_info["description"]
        actors = spec_info.get("actors", ["user"])
        actions = spec_info.get("actions", ["interact with the system"])
        outcomes = spec_info.get("outcomes", ["achieve their goal"])
        
        # Create feature header with story mapping
        story_mapping = f"\n  # Story ID: {story_id}" if story_id else ""
        
        content = f"""@{spec_type} @{story_id.lower() if story_id else 'story'}
Feature: {title}{story_mapping}

  As a {actors[0] if actors else 'user'}
  I want to {actions[0] if actions else 'use the system'}
  So that I can {outcomes[0] if outcomes else 'achieve my goals'}

  Background:
    Given the system is available
    And I am authenticated
    And the feature is properly configured

"""
        
        # Add main scenarios
        content += self._generate_main_scenarios(spec_info, story_id)
        
        # Add error handling scenarios
        content += self._generate_error_scenarios(spec_info, story_id)
        
        return content
    
    def _generate_main_scenarios(self, spec_info: Dict[str, Any], story_id: str = None) -> str:
        """
        Generate main scenarios for the Gherkin feature with story ID context.
        
        Args:
            spec_info: Specification information
            story_id: Story ID for context
            
        Returns:
            Main scenarios content
        """
        title = spec_info["title"]
        actions = spec_info.get("actions", [])
        outcomes = spec_info.get("outcomes", [])
        
        story_context = f" [{story_id}]" if story_id else ""
        
        scenarios = f"""  @happy_path @{story_id.lower() if story_id else 'main'}
  Scenario: Successful {title}{story_context}
    Given I have the necessary permissions and valid data
    When I {actions[0] if actions else 'perform the required action'}
    Then I should {outcomes[0] if outcomes else 'see the expected result'}
    And the system should be in a consistent state
    And the operation should be logged for audit purposes

"""
        
        # Add data validation scenario if applicable
        if self._requires_data_validation(spec_info["prompt"]):
            scenarios += f"""  @validation @{story_id.lower() if story_id else 'data'}
  Scenario: Data Validation for {title}{story_context}
    Given I provide valid input data according to business rules
    When I submit the request
    Then the system should validate all inputs thoroughly
    And proceed with processing if validation passes
    And return a success confirmation with transaction details

"""
        
        return scenarios
    
    def _generate_error_scenarios(self, spec_info: Dict[str, Any], story_id: str = None) -> str:
        """
        Generate error handling scenarios with story ID context.
        
        Args:
            spec_info: Specification information
            story_id: Story ID for context
            
        Returns:
            Error scenarios content
        """
        title = spec_info["title"]
        story_context = f" [{story_id}]" if story_id else ""
        
        error_scenarios = f"""  @error_handling @{story_id.lower() if story_id else 'error'}
  Scenario: Invalid Input for {title}{story_context}
    Given I provide invalid or malformed input data
    When I attempt to perform the action
    Then I should see a clear and actionable error message
    And the system should remain in a stable state
    And the error should be logged for monitoring

  @security @{story_id.lower() if story_id else 'auth'}
  Scenario: Unauthorized Access for {title}{story_context}
    Given I do not have the necessary permissions
    When I attempt to perform the action
    Then I should be denied access immediately
    And receive an appropriate authorization error message
    And the security incident should be logged

"""
        
        return error_scenarios
    
    def _create_fraud_detection_gherkin(self, spec_info: Dict[str, Any], story_id: str = None) -> Optional[str]:
        """
        Create fraud detection specific Gherkin scenarios with story ID mapping.
        
        Args:
            spec_info: Specification information
            story_id: Story ID for this feature
            
        Returns:
            Path to fraud detection Gherkin file
        """
        try:
            if not story_id:
                story_id = f"{self._extract_or_generate_story_id(spec_info, 'story')}-FRAUD"
            
            meaningful_name = "fraud-detection-security"
            filename = f"{story_id}-{meaningful_name}.feature"
            fraud_dir = project_root / "specs" / "featurefiles" / "security"
            fraud_dir.mkdir(parents=True, exist_ok=True)
            filepath = fraud_dir / filename
            
            content = f"""@security @fraud_detection @{story_id.lower()}
Feature: Fraud Detection for {spec_info['title']}

  # Story ID: {story_id}
  # Related to: {spec_info.get('main_feature_file', {}).get('story_id', 'Main Feature')}

  As a security system
  I want to detect fraudulent activities in real-time
  So that I can protect users and prevent financial losses

  Background:
    Given the fraud detection system is active and monitoring
    And machine learning models are trained and deployed
    And monitoring rules are configured according to risk policies

  @ml_detection @{story_id.lower()}
  Scenario: Machine Learning Fraud Detection [{story_id}]
    Given the ML fraud model is trained with latest fraud patterns
    When a transaction is submitted for processing
    Then the system should calculate a comprehensive fraud risk score
    And apply appropriate risk thresholds
    And block transactions that exceed the fraud threshold
    And log all scoring decisions for audit

  @real_time @{story_id.lower()}
  Scenario: Real-time Fraud Alerts [{story_id}]
    Given fraud is detected in a transaction
    When the system processes the fraud alert
    Then it should notify the customer immediately via multiple channels
    And freeze the affected account temporarily
    And escalate to the fraud investigation team
    And log the complete incident for compliance reporting

  @pattern_analysis @{story_id.lower()}
  Scenario: Suspicious Transaction Pattern Detection [{story_id}]
    Given a customer has established normal transaction patterns
    When multiple transactions occur that deviate from normal behavior
    Then the system should flag these as potentially fraudulent
    And trigger enhanced verification procedures
    And maintain detailed analytics for pattern improvement

"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error creating fraud detection Gherkin: {e}")
            return None
    
    def _create_loan_processing_gherkin(self, spec_info: Dict[str, Any], story_id: str = None) -> Optional[str]:
        """
        Create loan processing specific Gherkin scenarios with story ID mapping.
        
        Args:
            spec_info: Specification information
            story_id: Story ID for this feature
            
        Returns:
            Path to loan processing Gherkin file
        """
        try:
            if not story_id:
                story_id = f"{self._extract_or_generate_story_id(spec_info, 'story')}-LOAN"
            
            meaningful_name = "loan-origination-processing"
            filename = f"{story_id}-{meaningful_name}.feature"
            loans_dir = project_root / "specs" / "featurefiles" / "loans"
            loans_dir.mkdir(parents=True, exist_ok=True)
            filepath = loans_dir / filename
            
            content = f"""@loans @credit @{story_id.lower()}
Feature: Loan Processing for {spec_info['title']}

  # Story ID: {story_id}
  # Related to: {spec_info.get('main_feature_file', {}).get('story_id', 'Main Feature')}

  As a loan applicant
  I want to apply for a loan through a streamlined digital process
  So that I can receive financial assistance quickly and efficiently

  Background:
    Given the loan origination system is available and operational
    And credit scoring services are connected and functional
    And regulatory compliance systems are active

  @application @{story_id.lower()}
  Scenario: Successful Loan Application [{story_id}]
    Given I provide complete and valid application information
    And I have the necessary supporting documentation
    When I submit my loan application through the digital platform
    Then the system should process my credit check automatically
    And calculate my loan eligibility based on comprehensive criteria
    And provide a loan decision within the committed SLA timeframe
    And present clear next steps for loan processing

  @ai_underwriting @{story_id.lower()}
  Scenario: AI-Powered Credit Scoring and Underwriting [{story_id}]
    Given my loan application is submitted and initial validation passed
    When the AI underwriting engine processes my financial data
    Then it should analyze multiple data sources and credit indicators
    And generate a comprehensive credit score with risk assessment
    And provide detailed underwriting recommendations
    And document the decision rationale for compliance purposes

  @approval @{story_id.lower()}
  Scenario: Automated Loan Approval Workflow [{story_id}]
    Given my application meets all approval criteria and risk thresholds
    When the automated decision engine processes my application
    Then I should receive instant approval notification
    And loan terms and conditions should be clearly presented
    And next steps should be communicated with timeline
    And the approval should be logged for audit purposes

  @rejection @{story_id.lower()}
  Scenario: Loan Rejection with Clear Explanation [{story_id}]
    Given my application does not meet current approval criteria
    When the system processes my application and determines rejection
    Then I should receive a clear and respectful rejection notice
    And understand the specific reasons for rejection
    And receive actionable guidance on improving my application
    And be offered alternative products or services if appropriate

"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error creating loan processing Gherkin: {e}")
            return None
    
    def _create_payment_processing_gherkin(self, spec_info: Dict[str, Any], story_id: str = None) -> Optional[str]:
        """
        Create payment processing specific Gherkin scenarios with story ID mapping.
        
        Args:
            spec_info: Specification information
            story_id: Story ID for this feature
            
        Returns:
            Path to payment processing Gherkin file
        """
        try:
            if not story_id:
                story_id = f"{self._extract_or_generate_story_id(spec_info, 'story')}-PAY"
            
            meaningful_name = "payment-gateway-processing"
            filename = f"{story_id}-{meaningful_name}.feature"
            payments_dir = project_root / "specs" / "featurefiles" / "payments"
            payments_dir.mkdir(parents=True, exist_ok=True)
            filepath = payments_dir / filename
            
            content = f"""@payments @transactions @{story_id.lower()}
Feature: Payment Processing for {spec_info['title']}

  # Story ID: {story_id}
  # Related to: {spec_info.get('main_feature_file', {}).get('story_id', 'Main Feature')}

  As a user
  I want to make secure and reliable payments
  So that I can complete transactions safely and efficiently

  Background:
    Given the payment gateway is operational and secure
    And security protocols are active and up to date
    And fraud detection systems are monitoring transactions

  @successful_payment @{story_id.lower()}
  Scenario: Successful Payment Transaction [{story_id}]
    Given I have sufficient funds in my account
    And my payment method is valid and verified
    When I initiate a payment transaction
    Then the system should validate my payment method thoroughly
    And process the transaction securely with encryption
    And provide immediate transaction confirmation
    And update account balances accurately

  @real_time @{story_id.lower()}
  Scenario: Real-time Payment Processing [{story_id}]
    Given I make a real-time payment request
    When the transaction is submitted to the payment gateway
    Then it should be processed instantly without delays
    And funds should be transferred immediately between accounts
    And both parties should receive real-time notifications
    And transaction status should be updated in real-time

  @security @{story_id.lower()}
  Scenario: Payment Security Validation [{story_id}]
    Given I submit payment information through the secure channel
    When the system processes the payment
    Then it should validate all security tokens and certificates
    And encrypt all sensitive data using industry standards
    And comply with PCI DSS and other security requirements
    And log security events for monitoring and audit

  @failure_handling @{story_id.lower()}
  Scenario: Failed Payment Handling and Recovery [{story_id}]
    Given my payment fails due to insufficient funds or system error
    When the system processes the payment failure
    Then I should receive a clear and actionable error message
    And the transaction should be safely rolled back
    And alternative payment options should be suggested
    And the failure should be logged for analysis and improvement

"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error creating payment processing Gherkin: {e}")
            return None
    
    def _generate_compliance_gherkin_content(self, spec_info: Dict[str, Any], compliance_reqs: List[str], story_id: str = None) -> str:
        """
        Generate compliance-focused Gherkin content with story ID mapping.

        Args:
            spec_info: Specification information
            compliance_reqs: List of compliance requirements
            story_id: Story ID for mapping

        Returns:
            Compliance Gherkin content
        """
        title = spec_info["title"]
        compliance_tags = " ".join([f"@{req.lower().replace(' ', '_')}" for req in compliance_reqs])
        story_context = f"\n  # Story ID: {story_id}" if story_id else ""

        content = f"""@compliance {compliance_tags} @{story_id.lower() if story_id else 'comp'}
Feature: Compliance Validation for {title}{story_context}

  As a compliance officer
  I want to ensure all regulatory requirements are met
  So that the organization remains compliant with financial regulations

  Background:
    Given compliance monitoring is active
    And regulatory rules are up to date
    And audit trails are properly configured

"""

        # Add specific compliance scenarios
        for req in compliance_reqs:
            content += self._generate_compliance_scenario(req, title, story_id)

        # Add general compliance scenarios
        content += f"""  @audit @{story_id.lower() if story_id else 'audit'}
  Scenario: Audit Trail Maintenance [{story_id or 'COMP'}]
    Given any transaction or operation is performed
    When the system processes the action
    Then it should maintain a complete audit trail
    And log all relevant compliance data with timestamps
    And ensure data integrity and non-repudiation
    And store audit records according to retention policies

  @reporting @{story_id.lower() if story_id else 'report'}
  Scenario: Regulatory Reporting [{story_id or 'COMP'}]
    Given compliance data needs to be reported
    When the reporting period arrives
    Then the system should generate accurate reports automatically
    And submit them to regulatory authorities on time
    And maintain records as required by law
    And notify compliance team of successful submission

"""

        return content
    
    def _generate_compliance_scenario(self, compliance_req: str, title: str, story_id: str = None) -> str:
        """
        Generate specific compliance scenario with story ID mapping.

        Args:
            compliance_req: Compliance requirement
            title: Feature title
            story_id: Story ID for context

        Returns:
            Compliance scenario content
        """
        story_context = f" [{story_id}]" if story_id else ""

        scenarios = {
            "KYC": f"""  @kyc @{story_id.lower() if story_id else 'kyc'}
  Scenario: Know Your Customer (KYC) Validation{story_context}
    Given a customer wants to use {title}
    When they provide identity information and supporting documents
    Then the system should verify their identity against trusted sources
    And validate against current KYC requirements and risk policies
    And maintain comprehensive KYC documentation with audit trail
    And update customer risk profile based on verification results

""",
            "AML": f"""  @aml @{story_id.lower() if story_id else 'aml'}
  Scenario: Anti-Money Laundering (AML) Checks{story_context}
    Given a financial transaction is initiated
    When the system processes the transaction
    Then it should perform comprehensive AML screening
    And check against sanctions lists and PEP databases
    And flag suspicious activities based on risk indicators
    And report to authorities if required by regulations

""",
            "PCI DSS": f"""  @pci_dss @{story_id.lower() if story_id else 'pci'}
  Scenario: PCI DSS Compliance for Payment Data{story_context}
    Given payment card data is processed
    When the system handles the transaction
    Then it should encrypt all sensitive cardholder data
    And comply with PCI DSS security requirements
    And maintain secure payment processing environment
    And regularly validate compliance through assessments

""",
            "SOX": f"""  @sox @{story_id.lower() if story_id else 'sox'}
  Scenario: Sarbanes-Oxley (SOX) Financial Controls{story_context}
    Given financial data is processed
    When the system handles the information
    Then it should maintain proper financial controls and segregation
    And ensure data accuracy and integrity through validation
    And provide comprehensive audit capabilities and reports
    And document all financial processes for compliance review

"""
        }

        return scenarios.get(compliance_req, f"""  @{compliance_req.lower().replace(' ', '_')} @{story_id.lower() if story_id else 'comp'}
  Scenario: {compliance_req} Compliance{story_context}
    Given {compliance_req} requirements must be met
    When the system processes related data
    Then it should ensure {compliance_req} compliance
    And maintain necessary documentation with proper controls
    And provide audit trails for regulatory review

""")
    
    def _extract_actors_from_prompt(self, prompt: str, banking_context: Dict[str, Any]) -> List[str]:
        """
        Extract key actors/users from the prompt.
        
        Args:
            prompt: Original prompt
            banking_context: Banking context
            
        Returns:
            List of actors
        """
        actors = []
        prompt_lower = prompt.lower()
        
        # Common banking actors
        banking_actors = {
            "customer": ["customer", "client", "user", "applicant"],
            "loan_officer": ["loan officer", "underwriter", "analyst"],
            "compliance_officer": ["compliance", "auditor", "regulator"],
            "bank_employee": ["employee", "teller", "representative", "agent"],
            "system_admin": ["admin", "administrator", "operator"]
        }
        
        for actor_type, keywords in banking_actors.items():
            if any(keyword in prompt_lower for keyword in keywords):
                actors.append(actor_type.replace("_", " "))
        
        return actors if actors else ["user"]
    
    def _extract_actions_from_prompt(self, prompt: str) -> List[str]:
        """
        Extract key actions from the prompt.
        
        Args:
            prompt: Original prompt
            
        Returns:
            List of actions
        """
        actions = []
        
        # Common action patterns
        action_patterns = [
            r"\b(?:create|build|implement|develop|generate)\s+(.+?)(?:\s+(?:for|with|using)|$)",
            r"\b(?:process|handle|manage|validate)\s+(.+?)(?:\s+(?:for|with|using)|$)",
            r"\b(?:detect|monitor|analyze|assess)\s+(.+?)(?:\s+(?:for|with|using)|$)"
        ]
        
        for pattern in action_patterns:
            matches = re.findall(pattern, prompt, re.IGNORECASE)
            for match in matches:
                cleaned_action = re.sub(r'\s+', ' ', match.strip())
                if len(cleaned_action) > 3:
                    actions.append(cleaned_action)
        
        return actions if actions else ["interact with the system"]
    
    def _extract_business_outcomes(self, prompt: str, banking_context: Dict[str, Any]) -> List[str]:
        """
        Extract business outcomes from the prompt.
        
        Args:
            prompt: Original prompt
            banking_context: Banking context
            
        Returns:
            List of business outcomes
        """
        outcomes = []
        
        # Banking-specific outcomes
        if banking_context.get("is_banking") or self._is_banking_related(prompt):
            banking_outcomes = [
                "improve customer experience",
                "reduce operational costs",
                "ensure regulatory compliance",
                "minimize risk exposure",
                "increase operational efficiency"
            ]
            outcomes.extend(banking_outcomes[:2])  # Add top 2 relevant outcomes
        
        # Generic outcomes
        generic_outcomes = [
            "achieve business objectives",
            "improve system reliability",
            "enhance user satisfaction"
        ]
        
        outcomes.extend(generic_outcomes[:1])
        
        return outcomes if outcomes else ["achieve their goals"]
    
    def _is_banking_related(self, prompt: str) -> bool:
        """
        Check if prompt is banking-related.
        
        Args:
            prompt: Prompt to check
            
        Returns:
            True if banking-related
        """
        banking_keywords = [
            "bank", "loan", "credit", "payment", "transaction", "financial",
            "fraud", "compliance", "kyc", "aml", "underwriting", "origination"
        ]
        prompt_lower = prompt.lower()
        return any(keyword in prompt_lower for keyword in banking_keywords)
    
    def _is_security_fraud_related(self, prompt: str) -> bool:
        """
        Check if prompt is security/fraud-related.
        
        Args:
            prompt: Prompt to check
            
        Returns:
            True if security/fraud-related
        """
        security_keywords = ["fraud", "security", "detect", "monitor", "alert", "threat"]
        prompt_lower = prompt.lower()
        return any(keyword in prompt_lower for keyword in security_keywords)
    
    def _is_loan_credit_related(self, prompt: str) -> bool:
        """
        Check if prompt is loan/credit-related.
        
        Args:
            prompt: Prompt to check
            
        Returns:
            True if loan/credit-related
        """
        loan_keywords = ["loan", "credit", "lending", "underwriting", "origination", "approval"]
        prompt_lower = prompt.lower()
        return any(keyword in prompt_lower for keyword in loan_keywords)
    
    def _is_payment_related(self, prompt: str) -> bool:
        """
        Check if prompt is payment-related.
        
        Args:
            prompt: Prompt to check
            
        Returns:
            True if payment-related
        """
        payment_keywords = ["payment", "transaction", "transfer", "gateway", "processing"]
        prompt_lower = prompt.lower()
        return any(keyword in prompt_lower for keyword in payment_keywords)
    
    def _requires_data_validation(self, prompt: str) -> bool:
        """
        Check if prompt requires data validation scenarios.
        
        Args:
            prompt: Prompt to check
            
        Returns:
            True if data validation required
        """
        validation_keywords = ["data", "input", "form", "validate", "verify", "check"]
        prompt_lower = prompt.lower()
        return any(keyword in prompt_lower for keyword in validation_keywords)
    
    def _extract_compliance_requirements(self, result: Dict[str, Any], banking_context: Dict[str, Any]) -> List[str]:
        """
        Extract compliance requirements from result and context.
        
        Args:
            result: Processing result
            banking_context: Banking context
            
        Returns:
            List of compliance requirements
        """
        compliance_reqs = []
        
        # From banking context
        if banking_context.get("compliance_areas"):
            compliance_reqs.extend(banking_context["compliance_areas"])
        
        # From result
        if result.get("compliance_context"):
            compliance_reqs.extend(result["compliance_context"])
        
        # Remove duplicates and return
        return list(set(compliance_reqs))
    
    def _extract_or_generate_story_id(self, spec_info: Dict[str, Any], spec_type: str) -> str:
        """
        Extract existing story ID or generate a new one.
        
        Args:
            spec_info: Specification information
            spec_type: Type of specification
            
        Returns:
            Story ID (e.g., S001, F001, E001)
        """
        # Try to extract from title if it contains an ID
        title = spec_info.get("title", "")
        
        # Look for existing IDs in the title
        import re
        id_match = re.search(r'\b([SFE]\d{3})\b', title)
        if id_match:
            return id_match.group(1)
        
        # Look for feature ID in created files
        for file_path in spec_info.get("created_files", []):
            if ".md" in file_path:
                file_match = re.search(r'([SFE]\d{3})', file_path)
                if file_match:
                    # Convert to story ID if it's a feature or epic
                    base_id = file_match.group(1)
                    if base_id.startswith('F'):
                        story_num = base_id[1:]
                        return f"S{story_num}"
                    elif base_id.startswith('E'):
                        story_num = base_id[1:]
                        return f"S{story_num}"
                    return base_id
        
        # Generate new story ID based on spec type
        if spec_type in ["story", "feature", "epic"]:
            return self._get_next_story_id()
        
        return "S001"  # Default fallback
    
    def _generate_feature_file_name(self, spec_info: Dict[str, Any], story_id: str) -> str:
        """
        Generate meaningful feature file name.
        
        Args:
            spec_info: Specification information
            story_id: Story ID
            
        Returns:
            Meaningful feature file name
        """
        title = spec_info.get("title", "feature")
        prompt = spec_info.get("prompt", "")
        
        # Extract key business terms
        business_terms = []
        
        # Banking domain terms
        banking_terms = {
            "fraud": ["fraud", "detection", "security"],
            "loan": ["loan", "credit", "origination", "underwriting"],
            "payment": ["payment", "transaction", "gateway"],
            "account": ["account", "banking", "customer"],
            "compliance": ["compliance", "kyc", "aml", "regulatory"]
        }
        
        prompt_lower = prompt.lower()
        title_lower = title.lower()
        
        # Find relevant banking domain
        for domain, keywords in banking_terms.items():
            if any(keyword in prompt_lower or keyword in title_lower for keyword in keywords):
                business_terms.append(domain)
                break
        
        # Extract specific action words
        action_words = re.findall(r'\b(real-time|digital|automated|AI|smart|secure|mobile)\b', 
                                prompt_lower + " " + title_lower)
        business_terms.extend(action_words[:2])  # Limit to 2 action words
        
        # Clean and join terms
        if business_terms:
            meaningful_name = "-".join(business_terms)
        else:
            # Fallback to cleaned title
            cleaned_title = re.sub(r'\b(feature|story|epic|specification|for|the|and)\b', '', title_lower)
            cleaned_title = re.sub(r'\s+', '-', cleaned_title.strip())
            meaningful_name = cleaned_title[:30]  # Limit length
        
        return self._slugify(meaningful_name)
    
    def _generate_compliance_feature_name(self, spec_info: Dict[str, Any], compliance_reqs: List[str]) -> str:
        """
        Generate meaningful compliance feature file name.
        
        Args:
            spec_info: Specification information
            compliance_reqs: Compliance requirements
            
        Returns:
            Meaningful compliance feature name
        """
        if compliance_reqs:
            # Use primary compliance requirement
            primary_req = compliance_reqs[0].lower().replace(' ', '-')
            return f"compliance-{primary_req}"
        
        return "compliance-validation"
    
    def _create_complete_workflow_specs(self, prompt: str, banking_context: Dict[str, Any], entities: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive specifications for complete workflow with epic, features, and stories."""
        print("📋 Complete Workflow: Generating Epic, Features, and Stories...")
        
        # Phase 1: Create Epic specification
        epic_result = self.create_epic(prompt, banking_context, entities)
        epic_result["detected_type"] = "complete_workflow_epic"
        epic_result["is_complete_workflow"] = True
        epic_result["workflow_phase"] = "specification"
        print("✅ Epic Created: Digital Loan Origination Platform")
        
        # Phase 2: Create Feature specifications for loan platform
        features_created = []
        
        # Feature 1: AI-Powered Underwriting Engine
        feature1_prompt = "AI-powered underwriting engine with machine learning risk assessment and automated decision making"
        feature1_result = self.create_feature(feature1_prompt, banking_context, entities)
        feature1_result["epic_id"] = epic_result.get("spec_id", "E063")
        features_created.append(feature1_result)
        print("✅ Feature 1 Created: AI-Powered Underwriting Engine")
        
        # Feature 2: Digital Application Processing
        feature2_prompt = "Digital loan application processing with document verification and KYC automation"
        feature2_result = self.create_feature(feature2_prompt, banking_context, entities)
        feature2_result["epic_id"] = epic_result.get("spec_id", "E063")
        features_created.append(feature2_result)
        print("✅ Feature 2 Created: Digital Application Processing")
        
        # Feature 3: Real-time Risk Assessment
        feature3_prompt = "Real-time risk assessment with compliance monitoring and regulatory reporting"
        feature3_result = self.create_feature(feature3_prompt, banking_context, entities)
        feature3_result["epic_id"] = epic_result.get("spec_id", "E063")
        features_created.append(feature3_result)
        print("✅ Feature 3 Created: Real-time Risk Assessment")
        
        # Phase 3: Create Story specifications with integrated Gherkin
        stories_created = []
        
        # Story 1: Loan Application API
        story1_prompt = "As a loan applicant, I want to submit my loan application through a secure API so that I can get real-time validation and faster processing"
        print("📖 Creating Story Specification...")
        story1_result = self._create_manual_story(
            story1_prompt, 
            "S029", 
            "Loan Application Submission API",
            banking_context, 
            entities,
            feature2_result.get("spec_id", "F014"),
            epic_result.get("spec_id", "E064")
        )
        stories_created.append(story1_result)
        print("✅ Story 1 Created: Loan Application API with Gherkin tests")
        
        # Story 2: ML Risk Scoring Engine  
        story2_prompt = "As a loan officer, I want to use ML risk scoring to automatically assess loan applications so that I can make faster and more accurate decisions"
        print("📖 Creating Story Specification...")
        story2_result = self._create_manual_story(
            story2_prompt,
            "S030", 
            "ML Risk Scoring for Loan Assessment",
            banking_context, 
            entities,
            feature1_result.get("spec_id", "F015"),
            epic_result.get("spec_id", "E064")
        )
        stories_created.append(story2_result)
        print("✅ Story 2 Created: ML Risk Scoring Engine with Gherkin tests")
        
        # Story 3: Real-time Risk Assessment
        story3_prompt = "As a risk manager, I want real-time risk assessment during loan processing so that I can identify and mitigate risks immediately"
        print("📖 Creating Story Specification...")
        story3_result = self._create_manual_story(
            story3_prompt,
            "S031", 
            "Real-time Risk Assessment Dashboard",
            banking_context, 
            entities,
            feature3_result.get("spec_id", "F013"),
            epic_result.get("spec_id", "E064")
        )
        stories_created.append(story3_result)
        print("✅ Story 3 Created: Real-time Risk Assessment with Gherkin tests")
        
        # Phase 4: Prepare GitHub MCP data for all specifications
        github_mcp_data = []
        
        # Add epic to GitHub MCP data
        if epic_result.get("github_mcp_data"):
            github_mcp_data.extend(epic_result["github_mcp_data"])
        
        # Add features to GitHub MCP data
        for feature in features_created:
            if feature.get("github_mcp_data"):
                github_mcp_data.extend(feature["github_mcp_data"])
        
        # Add stories to GitHub MCP data
        for story in stories_created:
            if story.get("github_mcp_data"):
                github_mcp_data.extend(story["github_mcp_data"])
        
        # Update epic result with comprehensive workflow data
        epic_result.update({
            "features_created": len(features_created),
            "stories_created": len(stories_created),
            "total_specifications": 1 + len(features_created) + len(stories_created),
            "github_mcp_data": github_mcp_data,
            "workflow_summary": {
                "epic": epic_result.get("title", "Digital Loan Origination Platform"),
                "features": [f.get("title", "Unknown") for f in features_created],
                "stories": [s.get("title", "Unknown") for s in stories_created],
                "gherkin_files": len([s for s in stories_created if s.get("gherkin_file_created")]),
                "banking_domain": banking_context.get("domain", "loans"),
                "compliance_requirements": banking_context.get("compliance_requirements", [])
            }
        })
        
        print(f"✅ Complete Workflow: Created {epic_result['total_specifications']} specifications")
        print(f"   📋 Epic: 1, Features: {len(features_created)}, Stories: {len(stories_created)}")
        print(f"   🧪 Gherkin files: {epic_result['workflow_summary']['gherkin_files']}")
        print(f"   🚀 GitHub MCP actions: {len(github_mcp_data)}")
        
        return epic_result
    
    def _create_manual_story(self, prompt: str, story_id: str, title: str, banking_context: Dict[str, Any], 
                           entities: Dict[str, Any], feature_id: str, epic_id: str) -> Dict[str, Any]:
        """Create a story specification manually to ensure proper story creation."""
        
        # Extract user story components from prompt
        user_story_parts = self._parse_user_story(prompt)
        
        # Generate Gherkin content first
        gherkin_content = self._generate_gherkin_content(story_id, title, user_story_parts)
        
        # Create story content with integrated Gherkin
        story_content = f"""# Story {story_id}: {title}

## Story Overview
**Epic:** {epic_id} - Digital Loan Origination Platform  
**Feature:** {feature_id}  
**Story ID:** {story_id}  
**Priority:** High  
**Status:** In Progress  

## User Story
**As a** {user_story_parts.get('actor', 'user')}  
**I want** {user_story_parts.get('action', 'to interact with the system')}  
**So that** {user_story_parts.get('benefit', 'I can achieve my goal')}  

## Acceptance Criteria

### Functional Requirements
- [ ] Core functionality implemented
- [ ] User interface responsive
- [ ] Data validation working
- [ ] Error handling robust
- [ ] Performance requirements met

### Technical Requirements
- [ ] API response time < 2 seconds
- [ ] Security measures implemented
- [ ] Data encryption enforced
- [ ] Audit logging enabled
- [ ] Integration testing passed

### Business Rules
- [ ] Compliance requirements met
- [ ] Regulatory standards followed
- [ ] Business logic validated
- [ ] User experience optimized

## Definition of Done
- [ ] Code implementation completed
- [ ] Unit tests written and passing
- [ ] Integration tests successful
- [ ] Security testing passed
- [ ] Performance benchmarks met
- [ ] User acceptance testing completed
- [ ] Documentation updated

## BDD Feature File Content
**File:** `specs/featurefiles/{story_id}-{title.lower().replace(' ', '-')}.feature`

```gherkin
{gherkin_content}
```

## Dependencies
- Authentication service
- Database connectivity
- External API integrations
- Compliance validation services

## Banking Context
- **Domain:** {banking_context.get('domain', 'loans')}
- **Product Types:** {', '.join(banking_context.get('product_types', []))}
- **Compliance:** {', '.join(banking_context.get('compliance_requirements', []))}

---
**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Generator:** PromptToProduct Spec-Driven Development  
**Banking Domain:** {banking_context.get('domain', 'loans')}  
**Method:** manual_story_creation
"""
        
        # Create story file
        story_file_path = project_root / "specs" / "stories" / f"{story_id}-{title.lower().replace(' ', '-')}.md"
        try:
            with open(story_file_path, 'w', encoding='utf-8') as f:
                f.write(story_content)
            
            print(f"   ✅ Created story file: {story_file_path}")
            
            # Create Gherkin feature file (content already generated)
            gherkin_file_created = False
            try:
                gherkin_file_path = project_root / "specs" / "featurefiles" / f"{story_id}-{title.lower().replace(' ', '-')}.feature"
                
                with open(gherkin_file_path, 'w', encoding='utf-8') as f:
                    f.write(gherkin_content)
                
                print(f"   ✅ Created Gherkin file: {gherkin_file_path}")
                gherkin_file_created = True
                
            except Exception as e:
                print(f"   ⚠️ Gherkin generation warning: {e}")
            
            # Prepare GitHub MCP data
            github_mcp_data = self._prepare_story_github_mcp_data(story_id, title, story_content, str(story_file_path))
            
            return {
                "spec_type": "story",
                "story_id": story_id,
                "title": title,
                "spec_file_path": str(story_file_path),
                "feature_id": feature_id,
                "epic_id": epic_id,
                "user_story": user_story_parts,
                "gherkin_file_created": gherkin_file_created,
                "banking_context": banking_context,
                "github_mcp_data": [github_mcp_data] if github_mcp_data else [],
                "method": "manual_story_creation",
                "created_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"   ❌ Error creating story file: {e}")
            return {
                "spec_type": "story",
                "story_id": story_id,
                "title": title,
                "error": str(e),
                "method": "manual_story_creation_failed"
            }
    
    def _parse_user_story(self, prompt: str) -> Dict[str, str]:
        """Parse user story format from prompt."""
        # Extract "As a...", "I want...", "So that..." format
        import re
        
        as_match = re.search(r'As a ([^,]+)', prompt, re.IGNORECASE)
        want_match = re.search(r'I want ([^,]+)', prompt, re.IGNORECASE)
        so_match = re.search(r'so that (.+)', prompt, re.IGNORECASE)
        
        return {
            'actor': as_match.group(1).strip() if as_match else 'user',
            'action': want_match.group(1).strip() if want_match else 'to interact with the system',
            'benefit': so_match.group(1).strip() if so_match else 'I can achieve my goal'
        }
    
    def _generate_gherkin_content(self, story_id: str, title: str, user_story_parts: Dict[str, str]) -> str:
        """Generate Gherkin feature file content for the story."""
        story_tag = story_id.lower()
        
        return f"""@story @{story_tag}
Feature: {title}
  # Story ID: {story_id}

  As a {user_story_parts.get('actor', 'user')}
  I want {user_story_parts.get('action', 'to interact with the system')}
  So that {user_story_parts.get('benefit', 'I can achieve my goal')}

  Background:
    Given the system is available and operational
    And I am authenticated as a valid user
    And the story feature is properly configured

  @acceptance @{story_tag}
  Scenario: Successful {title} [{story_id}]
    Given I have the necessary permissions and valid input data
    When I perform the required action
    Then I should achieve the expected outcome
    And the system should be in a consistent state
    And the operation should be logged for audit purposes

  @validation @{story_tag}
  Scenario: Input Validation for {title} [{story_id}]
    Given I provide input data for the story
    When the system validates my input
    Then it should accept valid data and proceed
    And reject invalid data with clear error messages
    And maintain system stability throughout the process

  @error_handling @{story_tag}
  Scenario: Error Handling for {title} [{story_id}]
    Given I encounter an error condition
    When the system processes my request
    Then I should receive a clear and actionable error message
    And the system should remain in a stable state
    And the error should be logged for analysis

  @security @{story_tag}
  Scenario: Security Validation for {title} [{story_id}]
    Given I attempt to access the story functionality
    When the system checks my authorization
    Then it should verify my permissions appropriately
    And deny access if I lack proper authorization
    And log any security-related events

  @performance @{story_tag}
  Scenario: Performance Requirements for {title} [{story_id}]
    Given I have a high volume of concurrent requests
    When the system processes multiple operations
    Then response times should remain within acceptable limits
    And system resources should be efficiently utilized
    And performance metrics should be logged
"""
    
    def _prepare_story_github_mcp_data(self, story_id: str, title: str, content: str, file_path: str) -> Optional[Dict[str, Any]]:
        """Prepare GitHub MCP data for story."""
        try:
            # Convert file path to relative path for GitHub
            relative_path = file_path.replace(str(project_root), "").replace("\\", "/")
            if relative_path.startswith("/"):
                relative_path = relative_path[1:]
            
            return {
                "spec_file": relative_path,
                "spec_type": "story",
                "spec_id": story_id,
                "issue_title": f"Story {story_id}: {title}",
                "issue_body": content,  # Use the full story content including Gherkin
                "file_content": content,
                "repo_owner": "vrushalisarfare",
                "repo_name": "PromptToProduct",
                "github_integration": "ready"
            }
        except Exception as e:
            print(f"   ⚠️ Error preparing GitHub MCP data: {e}")
            return None

    def get_spec_agent_status(self) -> Dict[str, Any]:
        """Get current spec agent status."""
        github_configured = False
        if CONFIG_AVAILABLE:
            try:
                github_config = get_github_config()
                github_configured = github_config.is_configured
            except:
                pass
        
        return {
            "agent_id": self.agent_id,
            "version": "1.2",
            "status": "active",
            "schema_processor_available": self.schema_processor is not None,
            "schema_processor_info": self._get_schema_info(),
            "github_mcp_integration": True,
            "github_configured": github_configured,
            "supported_actions": ["create_epic", "create_feature", "create_story", "create_banking_feature", "create_compliance_story"],
            "inputs": ["specs/prompt_schema.json"],
            "outputs": ["specs/epics/**", "specs/features/**", "specs/stories/**", "specs/featurefiles/**/*.feature"],
            "banking_domain_support": True,
            "compliance_story_support": True,
            "gherkin_feature_generation": True,
            "bdd_testing_support": True,
            "intelligent_routing": self.schema_processor is not None,
            "langgraph_compatible": True
        }

    def _get_schema_info(self) -> Dict[str, Any]:
        """Get schema processor information."""
        if self.schema_processor:
            return {
                "schema_version": self.schema_processor.schema.get("version", "unknown"),
                "product_types": len(self.schema_processor.banking_domain.get("product_types", {})),
                "actions_defined": len(self.schema_processor.actions),
                "routing_rules": len(self.schema_processor.routing_rules),
                "compliance_areas": len(self.schema_processor.banking_domain.get("compliance_areas", {}))
            }
        return {}

    def _extract_story_identifier_from_result(self, result: Dict[str, Any]) -> str:
        """Extract story identifier from result created files."""
        created_files = result.get("created_files", [])
        for file_path in created_files:
            if file_path.endswith(".md"):
                filename = Path(file_path).name
                # Extract story ID (e.g., S001, F001, etc.)
                match = re.search(r'([SEFP]\d+)', filename)
                if match:
                    return match.group(1)
        
        # Fallback: generate from title or default
        return "S001"

    def _extract_story_spec_info_for_gherkin(self, result: Dict[str, Any], prompt: str, banking_context: Dict[str, Any], story_id: str) -> Dict[str, Any]:
        """Extract story specification information optimized for Gherkin generation."""
        # Extract title from created files or result
        title = f"Story {story_id}"
        description = prompt
        
        # Try to extract title from created markdown files
        for file_path in result.get("created_files", []):
            if file_path.endswith(".md"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Extract title from markdown
                    title_match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
                    if title_match:
                        title = title_match.group(1).strip()
                        break
                except Exception:
                    continue
        
        # Extract user story components
        actors = self._extract_actors_from_prompt(prompt, banking_context)
        actions = self._extract_actions_from_prompt(prompt)
        outcomes = self._extract_business_outcomes(prompt, banking_context)
        
        return {
            "title": title,
            "description": description,
            "actors": actors,
            "actions": actions,
            "outcomes": outcomes,
            "banking_context": banking_context,
            "spec_type": "story",
            "story_id": story_id,
            "prompt": prompt
        }

    def _create_story_gherkin_feature(self, spec_info: Dict[str, Any], story_id: str) -> Optional[str]:
        """Create main Gherkin feature file for story with same identifier."""
        try:
            # Use story ID as feature filename
            meaningful_name = self._generate_feature_file_name(spec_info, story_id)
            filename = f"{story_id}-{meaningful_name}.feature"
            
            # Create featurefiles directory under specs if it doesn't exist
            features_dir = project_root / "specs" / "featurefiles"
            features_dir.mkdir(parents=True, exist_ok=True)
            
            filepath = features_dir / filename
            
            # Generate Gherkin content with story mapping
            content = self._generate_story_gherkin_content(spec_info, story_id)
            
            # Write Gherkin file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Created story Gherkin feature: {filepath}")
            
            # Store feature file info for GitHub issue integration
            spec_info["main_feature_file"] = {
                "path": str(filepath),
                "story_id": story_id,
                "filename": filename,
                "relative_path": f"specs/featurefiles/{filename}",
                "content": content
            }
            
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error creating story Gherkin feature: {e}")
            return None

    def _create_story_banking_gherkin_features(self, spec_info: Dict[str, Any], story_id: str) -> List[str]:
        """Create banking-specific Gherkin feature files for story."""
        banking_files = []
        
        try:
            # Create fraud detection scenarios if security-related
            if self._is_security_fraud_related(spec_info["prompt"]):
                fraud_file = self._create_fraud_detection_gherkin(spec_info, f"{story_id}-FRAUD")
                if fraud_file:
                    banking_files.append(fraud_file)
            
            # Create loan/credit scenarios if loan-related
            if self._is_loan_credit_related(spec_info["prompt"]):
                loan_file = self._create_loan_processing_gherkin(spec_info, f"{story_id}-LOAN")
                if loan_file:
                    banking_files.append(loan_file)
            
            # Create payment scenarios if payment-related
            if self._is_payment_related(spec_info["prompt"]):
                payment_file = self._create_payment_processing_gherkin(spec_info, f"{story_id}-PAY")
                if payment_file:
                    banking_files.append(payment_file)
            
            # Store additional feature files for GitHub integration
            for banking_file in banking_files:
                try:
                    with open(banking_file, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                    
                    file_path_obj = Path(banking_file)
                    relative_path = str(file_path_obj.relative_to(project_root))
                    
                    spec_info.setdefault("additional_feature_files", []).append({
                        "path": banking_file,
                        "type": "banking_specific",
                        "story_id": story_id,
                        "relative_path": relative_path,
                        "content": file_content
                    })
                except Exception as e:
                    print(f"Warning: Could not read banking file content {banking_file}: {e}")
            
        except Exception as e:
            print(f"❌ Error creating story banking Gherkin features: {e}")
        
        return banking_files

    def _generate_story_gherkin_content(self, spec_info: Dict[str, Any], story_id: str) -> str:
        """Generate Gherkin content specifically for story with same tags and identifier."""
        title = spec_info["title"]
        description = spec_info["description"]
        actors = spec_info.get("actors", ["user"])
        actions = spec_info.get("actions", ["interact with the system"])
        outcomes = spec_info.get("outcomes", ["achieve their goal"])
        
        # Extract user story format if present
        as_match = re.search(r'As\s+(?:a|an)\s+(.+?),\s*I\s+want\s+to\s+(.+?)\s+so\s+that\s+(.+)', description, re.IGNORECASE)
        if as_match:
            actor = as_match.group(1).strip()
            action = as_match.group(2).strip()
            outcome = as_match.group(3).strip()
        else:
            actor = actors[0] if actors else 'user'
            action = actions[0] if actions else 'use the system'
            outcome = outcomes[0] if outcomes else 'achieve my goals'
        
        # Create feature header with story mapping
        content = f"""@story @{story_id.lower()}
Feature: {title}
  # Story ID: {story_id}

  As a {actor}
  I want to {action}
  So that I can {outcome}

  Background:
    Given the system is available and operational
    And I am authenticated as a valid user
    And the story feature is properly configured

  @acceptance @{story_id.lower()}
  Scenario: Successful {title} [{story_id}]
    Given I have the necessary permissions and valid input data
    When I {action}
    Then I should {outcome}
    And the system should be in a consistent state
    And the operation should be logged for audit purposes

  @validation @{story_id.lower()}
  Scenario: Input Validation for {title} [{story_id}]
    Given I provide input data for the story
    When the system validates my input
    Then it should accept valid data and proceed
    And reject invalid data with clear error messages
    And maintain system stability throughout the process

  @error_handling @{story_id.lower()}
  Scenario: Error Handling for {title} [{story_id}]
    Given I encounter an error condition
    When the system processes my request
    Then I should receive a clear and actionable error message
    And the system should remain in a stable state
    And the error should be logged for analysis

  @security @{story_id.lower()}
  Scenario: Security Validation for {title} [{story_id}]
    Given I attempt to access the story functionality
    When the system checks my authorization
    Then it should verify my permissions appropriately
    And deny access if I lack proper authorization
    And log any security-related events

"""
        
        return content


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