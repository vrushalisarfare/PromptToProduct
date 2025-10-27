#!/usr/bin/env python3
"""
PromptToProduct Schema Processor
Reads from prompt_schema.json and enables spec-driven actions based on natural language prompts.
"""
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class PromptToProductSchema:
    """Main class for processing prompts according to the PromptToProduct schema."""
    
    def __init__(self, schema_path: str = "../prompt_schema.json"):
        """Initialize with schema file path."""
        self.schema_path = Path(schema_path)
        self.schema = self._load_schema()
        self.specs_dir = Path(".")  # Current directory (specs)
        
    def _load_schema(self) -> Dict[str, Any]:
        """Load the prompt schema from JSON file."""
        try:
            with open(self.schema_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Schema file not found: {self.schema_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in schema file: {e}")
    
    def get_next_id(self, spec_type: str) -> str:
        """Generate the next available ID for a spec type (epic/feature/story)."""
        prefix_map = {
            "epic": "E",
            "feature": "F", 
            "story": "S"
        }
        
        if spec_type not in prefix_map:
            raise ValueError(f"Invalid spec type: {spec_type}")
        
        prefix = prefix_map[spec_type]
        spec_dir = self.specs_dir / f"{spec_type}s"
        
        if not spec_dir.exists():
            return f"{prefix}001"
        
        # Find existing IDs
        existing_ids = []
        for file_path in spec_dir.glob(f"{prefix}*.md"):
            match = re.match(f"{prefix}(\d+)", file_path.stem)
            if match:
                existing_ids.append(int(match.group(1)))
        
        next_id = max(existing_ids, default=0) + 1
        return f"{prefix}{next_id:03d}"
    
    def parse_prompt(self, prompt: str) -> Dict[str, Any]:
        """Parse a natural language prompt to determine the action and extract details."""
        prompt_lower = prompt.lower()
        
        # Check for banking domain keywords first
        banking_context = self._detect_banking_context(prompt_lower)
        
        # Determine action type - check for explicit keywords first
        action = None
        if any(keyword in prompt_lower for keyword in ["create epic", "new epic", "add epic"]):
            action = "create_epic"
        elif any(keyword in prompt_lower for keyword in ["create feature", "new feature", "add feature", "feature for", "feature to"]):
            # Check if it's banking-specific
            if banking_context["is_banking"]:
                action = "create_banking_feature"
            else:
                action = "create_feature"
        elif any(keyword in prompt_lower for keyword in ["create story", "new story", "add story", "story for", "story to"]):
            # Check if it's compliance-focused
            if banking_context["is_compliance"]:
                action = "create_compliance_story"
            else:
                action = "create_story"
        elif any(keyword in prompt_lower for keyword in ["update", "modify", "change"]):
            action = "update_spec"
        elif any(keyword in prompt_lower for keyword in ["validate", "check", "verify"]):
            action = "validate_links"
        
        # If no explicit action found, infer from context
        if not action:
            if banking_context["is_banking"]:
                if "under epic" in prompt_lower or "epic e" in prompt_lower:
                    action = "create_banking_feature"
                elif banking_context["is_compliance"]:
                    action = "create_compliance_story"
                else:
                    action = "create_banking_feature"  # Default for banking context
            elif "under epic" in prompt_lower or "epic e" in prompt_lower:
                action = "create_feature"  # If mentioning epic, likely creating feature
            elif "under feature" in prompt_lower or "feature f" in prompt_lower:
                action = "create_story"  # If mentioning feature, likely creating story
            elif "epic" in prompt_lower:
                action = "create_epic"
            elif "story" in prompt_lower:
                action = "create_story"
            else:
                action = "create_feature"  # Default
        
        return {
            "action": action,
            "original_prompt": prompt,
            "banking_context": banking_context,
            "extracted_info": self._extract_info_from_prompt(prompt, action, banking_context)
        }
    
    def _detect_banking_context(self, prompt_lower: str) -> Dict[str, Any]:
        """Detect banking domain context and product types from prompt."""
        banking_domain = self.schema.get("banking_domain", {})
        product_types = banking_domain.get("product_types", {})
        compliance_areas = banking_domain.get("compliance_areas", {})
        
        context = {
            "is_banking": False,
            "is_compliance": False,
            "product_types": [],
            "compliance_requirements": [],
            "technologies": []
        }
        
        # Check for banking product types
        for product_type, config in product_types.items():
            keywords = config.get("keywords", [])
            if any(keyword in prompt_lower for keyword in keywords):
                context["is_banking"] = True
                context["product_types"].append(product_type)
        
        # Check for compliance keywords
        regulatory = compliance_areas.get("regulatory", [])
        if any(reg.lower() in prompt_lower for reg in regulatory):
            context["is_compliance"] = True
            context["compliance_requirements"].extend([reg for reg in regulatory if reg.lower() in prompt_lower])
        
        # Check for security keywords
        security = compliance_areas.get("security", [])
        if any(sec.lower() in prompt_lower for sec in security):
            context["is_banking"] = True
            context["technologies"].extend([sec for sec in security if sec.lower() in prompt_lower])
        
        return context
    
    def _extract_info_from_prompt(self, prompt: str, action: str, banking_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Extract structured information from the prompt based on the action type."""
        info = {}
        banking_context = banking_context or {}
        
        # Extract title/goal from prompt
        title_patterns = [
            r"create (?:an? )?(?:epic|feature|story|banking feature) (?:for |to )?(.+?)(?:\s+under|\s+in|\s*$)",
            r"add (?:an? )?(?:epic|feature|story|banking feature) (?:for |to )?(.+?)(?:\s+under|\s+in|\s*$)",
            r"(?:epic|feature|story) (?:for |to )?(.+?)(?:\s+under|\s+in|\s*$)",
            r"build (?:a |an )?(?:system|feature) (?:for |to )?(.+?)(?:\s+under|\s+in|\s*$)"
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, prompt, re.IGNORECASE)
            if match:
                info["title"] = match.group(1).strip()
                break
        
        # Extract parent reference (Epic/Feature ID)
        epic_match = re.search(r"(?:epic|under epic)\s+([EF]\d{3})", prompt, re.IGNORECASE)
        if epic_match:
            info["parent_epic"] = epic_match.group(1).upper()
        
        feature_match = re.search(r"(?:feature|under feature)\s+([F]\d{3})", prompt, re.IGNORECASE)
        if feature_match:
            info["parent_feature"] = feature_match.group(1).upper()
        
        # Extract technical details
        if "using" in prompt.lower():
            tech_match = re.search(r"using\s+(.+?)(?:\s*$|\.|,)", prompt, re.IGNORECASE)
            if tech_match:
                info["technology"] = tech_match.group(1).strip()
        
        # Add banking-specific information
        if banking_context.get("is_banking"):
            info["banking_context"] = banking_context
            info["product_types"] = banking_context.get("product_types", [])
            
            # Determine primary product type
            if banking_context["product_types"]:
                info["primary_product_type"] = banking_context["product_types"][0]
        
        if banking_context.get("is_compliance"):
            info["compliance_requirements"] = banking_context.get("compliance_requirements", [])
        
        return info
    
    def create_epic(self, title: str, objective: str = None, owner: str = "TBD") -> str:
        """Create a new epic specification."""
        epic_id = self.get_next_id("epic")
        filename = f"{epic_id}-{self._slugify(title)}.md"
        filepath = self.specs_dir / "epics" / filename
        
        # Ensure epics directory exists
        filepath.parent.mkdir(exist_ok=True)
        
        content = f"""# Epic: {title}
**ID:** {epic_id}  
**Objective:** {objective or title}  
**Owner:** {owner}  
**Linked Features:** TBD  

### Business Context
{objective or "Define the business context and rationale for this epic."}

### Success Criteria
- Define measurable success criteria
- Include user impact metrics
- Specify completion conditions

### Created
Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} via PromptToProduct Schema

"""
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        return str(filepath)
    
    def create_banking_feature(self, title: str, epic_id: str = None, product_type: str = None, 
                             compliance_requirements: List[str] = None, goal: str = None) -> str:
        """Create a new banking-specific feature specification."""
        feature_id = self.get_next_id("feature")
        filename = f"{feature_id}-{self._slugify(title)}.md"
        filepath = self.specs_dir / "features" / filename
        
        # Ensure features directory exists
        filepath.parent.mkdir(exist_ok=True)
        
        # Format compliance requirements
        compliance_text = ""
        if compliance_requirements:
            compliance_text = f"""
### Regulatory Requirements
{chr(10).join([f"- {req}" for req in compliance_requirements])}"""
        
        # Format product type section
        product_section = ""
        if product_type:
            product_section = f"""
### Banking Product Type
**{product_type.title()}**"""
        
        content = f"""# Banking Feature: {title}
**ID:** {feature_id}  
**Epic:** {epic_id or "TBD"}  
**Product Type:** {product_type or "TBD"}  
**Linked Stories:** TBD  
{product_section}

### Goal
{goal or title}

### Business Value
- Define business impact and value proposition
- Specify customer experience improvements
- Include revenue or cost optimization goals

### Technical Requirements
- Define technical specifications and architecture
- List integration requirements with core banking systems
- Specify performance and scalability criteria
- Include security and data protection requirements

### Security Requirements
- Authentication and authorization mechanisms
- Data encryption and tokenization requirements
- Fraud prevention and monitoring capabilities
- Audit trail and logging specifications
{compliance_text}

### Integration Points
- Core banking system interfaces
- Third-party service integrations
- API specifications and data formats
- Real-time vs batch processing requirements

### Acceptance Criteria
- Define feature completion criteria
- Include user acceptance tests
- Specify quality gates and performance benchmarks
- List compliance validation requirements

### Created
Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} via PromptToProduct Banking Schema

"""
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        return str(filepath)
    
    def create_compliance_story(self, title: str, feature_id: str = None, 
                              regulation: str = None, compliance_requirements: List[str] = None) -> str:
        """Create a new compliance-focused story specification."""
        story_id = self.get_next_id("story")
        filename = f"{story_id}-{self._slugify(title)}.md"
        filepath = self.specs_dir / "stories" / filename
        
        # Ensure stories directory exists
        filepath.parent.mkdir(exist_ok=True)
        
        requirements = compliance_requirements or ["Define compliance requirements"]
        requirements_text = "\n".join([f"- {req}" for req in requirements])
        
        content = f"""# Compliance Story: {title}
**ID:** {story_id}  
**Feature:** {feature_id or "TBD"}  
**Regulation:** {regulation or "TBD"}  

### Regulatory Context
This story ensures compliance with {regulation or "applicable regulations"} requirements for banking operations.

### Compliance Requirements
{requirements_text}

### Acceptance Criteria
- All regulatory requirements are implemented and tested
- Audit trail captures all required information
- Compliance reporting functionality is operational
- Risk controls are properly configured and monitored

### Audit & Logging Requirements
- Transaction logging with immutable audit trail
- User action tracking and accountability
- Compliance event monitoring and alerting
- Regulatory reporting data capture

### Testing Requirements
- Compliance validation testing
- Regulatory scenario testing
- Audit trail verification
- Risk control effectiveness testing

### Documentation Requirements
- Compliance control documentation
- Risk assessment documentation
- Audit procedure documentation
- Regulatory mapping documentation

### Definition of Done
- Code is implemented and tested
- Compliance controls are verified
- Audit capabilities are functional
- Documentation is complete and approved
- Regulatory sign-off obtained

### Created
Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} via PromptToProduct Banking Schema

"""
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        return str(filepath)
    
    def create_story(self, title: str, feature_id: str = None, acceptance_criteria: List[str] = None) -> str:
        """Create a new story specification."""
        story_id = self.get_next_id("story")
        filename = f"{story_id}-{self._slugify(title)}.md"
        filepath = self.specs_dir / "stories" / filename
        
        # Ensure stories directory exists
        filepath.parent.mkdir(exist_ok=True)
        
        criteria = acceptance_criteria or ["Define acceptance criteria"]
        criteria_text = "\n".join([f"- {criterion}" for criterion in criteria])
        
        content = f"""# Story: {title}
**ID:** {story_id}  
**Feature:** {feature_id or "TBD"}  

### Acceptance Criteria
{criteria_text}

### Tasks
1. Define implementation steps
2. Add technical tasks
3. Include testing requirements

### Definition of Done
- Code is implemented and tested
- Documentation is updated
- Feature is deployed and verified

### Created
Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} via PromptToProduct Schema

"""
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        return str(filepath)
    
    def create_feature(self, title: str, epic_id: str = None, goal: str = None) -> str:
        """Create a new feature specification."""
        feature_id = self.get_next_id("feature")
        filename = f"{feature_id}-{self._slugify(title)}.md"
        filepath = self.specs_dir / "features" / filename
        
        # Ensure features directory exists
        filepath.parent.mkdir(exist_ok=True)
        
        content = f"""# Feature: {title}
**ID:** {feature_id}  
**Epic:** {epic_id or "TBD"}  
**Linked Stories:** TBD  

### Goal
{goal or title}

### Technical Requirements
- Define technical specifications
- List integration requirements
- Specify performance criteria

### Acceptance Criteria
- Define feature completion criteria
- Include user acceptance tests
- Specify quality gates

### Created
Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} via PromptToProduct Schema

"""
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        return str(filepath)
    
    def process_prompt(self, prompt: str) -> Dict[str, Any]:
        """Main method to process a natural language prompt."""
        parsed = self.parse_prompt(prompt)
        action = parsed["action"]
        info = parsed["extracted_info"]
        banking_context = parsed.get("banking_context", {})
        
        result = {
            "action": action,
            "prompt": prompt,
            "banking_context": banking_context,
            "success": False,
            "file_created": None,
            "error": None
        }
        
        try:
            if action == "create_epic":
                title = info.get("title", "New Epic")
                filepath = self.create_epic(title)
                result["success"] = True
                result["file_created"] = filepath
                
            elif action == "create_banking_feature":
                title = info.get("title", "New Banking Feature")
                epic_id = info.get("parent_epic")
                product_type = info.get("primary_product_type", "").title() if info.get("primary_product_type") else None
                compliance_reqs = info.get("compliance_requirements", [])
                goal = info.get("title", title)
                
                filepath = self.create_banking_feature(
                    title=title,
                    epic_id=epic_id,
                    product_type=product_type,
                    compliance_requirements=compliance_reqs,
                    goal=goal
                )
                result["success"] = True
                result["file_created"] = filepath
                result["product_type"] = product_type
                
            elif action == "create_feature":
                title = info.get("title", "New Feature")
                epic_id = info.get("parent_epic")
                filepath = self.create_feature(title, epic_id)
                result["success"] = True
                result["file_created"] = filepath
                
            elif action == "create_compliance_story":
                title = info.get("title", "New Compliance Story")
                feature_id = info.get("parent_feature")
                compliance_reqs = info.get("compliance_requirements", [])
                regulation = compliance_reqs[0] if compliance_reqs else None
                
                filepath = self.create_compliance_story(
                    title=title,
                    feature_id=feature_id,
                    regulation=regulation,
                    compliance_requirements=compliance_reqs
                )
                result["success"] = True
                result["file_created"] = filepath
                result["regulation"] = regulation
                
            elif action == "create_story":
                title = info.get("title", "New Story")
                feature_id = info.get("parent_feature")
                filepath = self.create_story(title, feature_id)
                result["success"] = True
                result["file_created"] = filepath
                
            elif action == "validate_links":
                validation_result = self.validate_spec_links()
                result["success"] = True
                result["validation"] = validation_result
                
            else:
                result["error"] = f"Action '{action}' not yet implemented"
                
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def validate_spec_links(self) -> Dict[str, Any]:
        """Validate the hierarchical linkage across all specs."""
        validation = {
            "epics": [],
            "features": [],
            "stories": [],
            "orphaned_features": [],
            "orphaned_stories": [],
            "issues": []
        }
        
        # Get all existing specs
        epics = list((self.specs_dir / "epics").glob("E*.md"))
        features = list((self.specs_dir / "features").glob("F*.md"))
        stories = list((self.specs_dir / "stories").glob("S*.md"))
        
        epic_ids = [self._extract_id_from_filename(e.name) for e in epics]
        feature_ids = [self._extract_id_from_filename(f.name) for f in features]
        story_ids = [self._extract_id_from_filename(s.name) for s in stories]
        
        validation["epics"] = epic_ids
        validation["features"] = feature_ids
        validation["stories"] = story_ids
        
        # Check for orphaned features and stories
        for feature_file in features:
            content = feature_file.read_text()
            epic_match = re.search(r"\*\*Epic:\*\*\s*([E]\d{3})", content)
            if epic_match:
                epic_id = epic_match.group(1)
                if epic_id not in epic_ids:
                    validation["orphaned_features"].append({
                        "feature": self._extract_id_from_filename(feature_file.name),
                        "missing_epic": epic_id
                    })
        
        for story_file in stories:
            content = story_file.read_text()
            feature_match = re.search(r"\*\*Feature:\*\*\s*([F]\d{3})", content)
            if feature_match:
                feature_id = feature_match.group(1)
                if feature_id not in feature_ids:
                    validation["orphaned_stories"].append({
                        "story": self._extract_id_from_filename(story_file.name),
                        "missing_feature": feature_id
                    })
        
        return validation
    
    def _extract_id_from_filename(self, filename: str) -> str:
        """Extract ID from filename (e.g., 'E001-Title.md' -> 'E001')."""
        match = re.match(r"([EFS]\d{3})", filename)
        return match.group(1) if match else ""
    
    def _slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug."""
        return re.sub(r'[^\w\s-]', '', text).strip().replace(' ', '-')


def main():
    """CLI interface for the PromptToProduct Schema processor."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python schema_processor.py '<prompt>'")
        print("Example: python schema_processor.py 'Create a feature for user authentication'")
        return
    
    prompt = " ".join(sys.argv[1:])
    processor = PromptToProductSchema()
    
    print(f"Processing prompt: {prompt}")
    print("-" * 50)
    
    result = processor.process_prompt(prompt)
    
    if result["success"]:
        if result.get("file_created"):
            print(f"✅ Success! Created: {result['file_created']}")
        elif result.get("validation"):
            print("✅ Validation completed:")
            validation = result["validation"]
            print(f"   Epics: {len(validation['epics'])}")
            print(f"   Features: {len(validation['features'])}")
            print(f"   Stories: {len(validation['stories'])}")
            if validation["orphaned_features"]:
                print(f"   ⚠️  Orphaned features: {validation['orphaned_features']}")
            if validation["orphaned_stories"]:
                print(f"   ⚠️  Orphaned stories: {validation['orphaned_stories']}")
    else:
        print(f"❌ Error: {result['error']}")


if __name__ == "__main__":
    main()