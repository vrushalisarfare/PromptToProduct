#!/usr/bin/env python3
"""
Spec Agent - Converts Developer Prompts into Structured Markdown Specs

This agent specializes in converting natural language prompts into structured
specifications (epics, features, stories) with banking domain intelligence.
Enhanced with GitHub MCP integration for seamless repository synchronization.
"""
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

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
                print(f"✅ Schema processor initialized successfully")
            except Exception as e:
                print(f"Warning: Schema processor initialization failed: {e}")
    
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
            # Route to appropriate creation method
            if intent in ["create_epic"] or "epic" in prompt.lower():
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
        Generate GitHub issue body for the specification.
        
        Args:
            result: Processing result
            file_path: Relative file path
            content: File content
            
        Returns:
            GitHub issue body
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
        
        body += f"""

### Next Steps
- [ ] Review {spec_type.lower()} content
- [ ] Validate requirements and acceptance criteria
- [ ] Plan implementation approach
- [ ] Assign to development team
- [ ] Create related specifications if needed

### Links
- Specification file: [`{file_path}`]({file_path})
- Generated from prompt using PromptToProduct system

**Auto-generated by PromptToProduct Spec Agent**"""
        
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
            "version": "1.1",
            "status": "active",
            "schema_processor_available": self.schema_processor is not None,
            "github_mcp_integration": True,
            "github_configured": github_configured,
            "supported_actions": ["create_epic", "create_feature", "create_story"],
            "inputs": ["specs/prompt_schema.json"],
            "outputs": ["specs/**"],
            "banking_domain_support": True,
            "compliance_story_support": True,
            "langgraph_compatible": True
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