#!/usr/bin/env python3
"""
Schema Processor for PromptToProduct System

This module processes prompts using the comprehensive banking domain intelligence
defined in prompt_schema.json to provide intelligent routing and specification generation.
"""
import json
import re
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class PromptToProductSchema:
    """
    Schema processor that uses prompt_schema.json for intelligent prompt processing.
    
    Features:
    - Banking domain detection and classification
    - Intelligent routing based on schema rules
    - Automatic spec type detection
    - Compliance requirement mapping
    - Product type identification
    """
    
    def __init__(self, schema_path: Optional[str] = None):
        """Initialize the schema processor."""
        self.schema_path = schema_path or (Path(__file__).parent / "prompt_schema.json")
        self.schema = self._load_schema()
        self.banking_domain = self.schema.get("banking_domain", {})
        self.actions = self.schema.get("actions", {})
        self.prompt_patterns = self.schema.get("prompt_patterns", {})
        self.routing_rules = self.schema.get("intelligent_routing", {}).get("rules", [])
        
    def _load_schema(self) -> Dict[str, Any]:
        """Load the prompt schema from JSON file."""
        try:
            with open(self.schema_path, 'r', encoding='utf-8') as f:
                schema = json.load(f)
            print(f"✅ Schema loaded: {schema.get('name', 'Unknown')} v{schema.get('version', '0.0')}")
            return schema
        except FileNotFoundError:
            print(f"❌ Schema file not found: {self.schema_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in schema file: {e}")
            return {}
    
    def process_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Main entry point for processing prompts using schema intelligence.
        
        Args:
            prompt: Natural language prompt to process
            
        Returns:
            Processing result with detected context, action, and file creation status
        """
        prompt_lower = prompt.lower()
        
        result = {
            "success": True,
            "prompt": prompt,
            "processing_timestamp": datetime.now().isoformat(),
            "banking_context": self._detect_banking_context(prompt),
            "detected_action": self._detect_action(prompt),
            "compliance_requirements": self._detect_compliance_requirements(prompt),
            "entities": self._extract_entities(prompt),
            "file_created": None,
            "spec_info": {},
            "recommendations": [],
            "errors": []
        }
        
        try:
            # Apply intelligent routing
            routing_result = self._apply_intelligent_routing(prompt, result)
            result.update(routing_result)
            
            # Create specification file based on detected action
            spec_result = self._create_specification_file(prompt, result)
            result.update(spec_result)
            
        except Exception as e:
            result["success"] = False
            result["errors"].append(str(e))
            print(f"❌ Schema processing error: {e}")
        
        return result
    
    def _detect_banking_context(self, prompt: str) -> Dict[str, Any]:
        """Detect banking domain context using schema intelligence."""
        prompt_lower = prompt.lower()
        
        context = {
            "is_banking": False,
            "product_types": [],
            "primary_product": None,
            "compliance_areas": [],
            "technology_stack": [],
            "confidence_score": 0.0
        }
        
        # Check banking product types
        product_scores = {}
        for product_type, config in self.banking_domain.get("product_types", {}).items():
            keywords = config.get("keywords", [])
            examples = config.get("examples", [])
            
            score = 0
            for keyword in keywords:
                if keyword in prompt_lower:
                    score += 2
            
            for example in examples:
                if example.lower() in prompt_lower:
                    score += 3
            
            if score > 0:
                product_scores[product_type] = score
                context["product_types"].append(product_type)
        
        if product_scores:
            context["is_banking"] = True
            context["primary_product"] = max(product_scores.keys(), key=product_scores.get)
            context["confidence_score"] = max(product_scores.values()) / 10.0
        
        # Detect compliance areas
        compliance_areas = self.banking_domain.get("compliance_areas", {})
        for area_type, regulations in compliance_areas.items():
            for regulation in regulations:
                if regulation.lower() in prompt_lower:
                    context["compliance_areas"].append(regulation)
        
        # Detect technology stack
        tech_stack = self.banking_domain.get("technology_stack", {})
        for category, technologies in tech_stack.items():
            for tech in technologies:
                if tech.lower() in prompt_lower:
                    context["technology_stack"].append(tech)
        
        return context
    
    def _detect_action(self, prompt: str) -> Dict[str, Any]:
        """Detect the intended action based on schema patterns."""
        prompt_lower = prompt.lower()
        
        action_scores = {}
        
        # Check each defined action
        for action_name, action_config in self.actions.items():
            score = 0
            
            # Check banking examples if available
            banking_examples = action_config.get("banking_examples", [])
            for example in banking_examples:
                if self._calculate_similarity(prompt_lower, example.lower()) > 0.6:
                    score += 5
            
            # Check description keywords
            description = action_config.get("description", "").lower()
            if any(word in prompt_lower for word in description.split() if len(word) > 3):
                score += 2
            
            # Specific keyword patterns
            if action_name == "create_epic" and any(word in prompt_lower for word in ["epic", "platform", "system", "initiative"]):
                score += 3
            elif action_name == "create_banking_feature" and any(word in prompt_lower for word in ["feature", "capability", "functionality"]):
                score += 3
            elif action_name == "create_story" and any(word in prompt_lower for word in ["story", "requirement", "task", "implement"]):
                score += 3
            elif action_name == "create_compliance_story" and any(word in prompt_lower for word in ["compliance", "regulation", "kyc", "aml", "pci"]):
                score += 4
            
            if score > 0:
                action_scores[action_name] = score
        
        if action_scores:
            best_action = max(action_scores.keys(), key=action_scores.get)
            return {
                "action": best_action,
                "confidence": action_scores[best_action] / 10.0,
                "alternatives": list(action_scores.keys())
            }
        
        return {"action": "create_feature", "confidence": 0.5, "alternatives": []}
    
    def _detect_compliance_requirements(self, prompt: str) -> List[str]:
        """Detect compliance requirements mentioned in the prompt."""
        prompt_lower = prompt.lower()
        requirements = []
        
        compliance_areas = self.banking_domain.get("compliance_areas", {})
        for area_type, regulations in compliance_areas.items():
            for regulation in regulations:
                if regulation.lower() in prompt_lower:
                    requirements.append(regulation)
        
        return list(set(requirements))
    
    def _extract_entities(self, prompt: str) -> Dict[str, List[str]]:
        """Extract entities from the prompt using schema patterns."""
        entities = {
            "epic_references": [],
            "feature_references": [],
            "story_references": [],
            "technologies": [],
            "stakeholders": [],
            "banking_products": []
        }
        
        # Extract ID references
        epic_matches = re.findall(r'\bE\d{3}\b', prompt, re.IGNORECASE)
        entities["epic_references"] = [match.upper() for match in epic_matches]
        
        feature_matches = re.findall(r'\bF\d{3}\b', prompt, re.IGNORECASE)
        entities["feature_references"] = [match.upper() for match in feature_matches]
        
        story_matches = re.findall(r'\bS\d{3}\b', prompt, re.IGNORECASE)
        entities["story_references"] = [match.upper() for match in story_matches]
        
        # Extract technologies
        tech_stack = self.banking_domain.get("technology_stack", {})
        for category, technologies in tech_stack.items():
            for tech in technologies:
                if tech.lower() in prompt.lower():
                    entities["technologies"].append(tech)
        
        # Extract banking products
        product_types = self.banking_domain.get("product_types", {})
        for product_type, config in product_types.items():
            examples = config.get("examples", [])
            for example in examples:
                if example.lower() in prompt.lower():
                    entities["banking_products"].append(example)
        
        return entities
    
    def _apply_intelligent_routing(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply intelligent routing rules from schema."""
        prompt_lower = prompt.lower()
        routing_result = {
            "recommended_action": None,
            "routing_confidence": 0.0,
            "routing_rationale": ""
        }
        
        # Apply schema routing rules
        for rule in self.routing_rules:
            if self._evaluate_routing_rule(rule, prompt_lower, context):
                action = self._extract_action_from_rule(rule)
                routing_result["recommended_action"] = action
                routing_result["routing_confidence"] = 0.8
                routing_result["routing_rationale"] = rule
                break
        
        return routing_result
    
    def _evaluate_routing_rule(self, rule: str, prompt_lower: str, context: Dict[str, Any]) -> bool:
        """Evaluate if a routing rule matches the prompt and context."""
        # Parse rule conditions
        if "loan/mortgage/credit keywords" in rule and any(kw in prompt_lower for kw in ["loan", "mortgage", "credit", "lending"]):
            return True
        elif "payment/transfer/wire keywords" in rule and any(kw in prompt_lower for kw in ["payment", "transfer", "wire", "transaction"]):
            return True
        elif "card/plastic/rewards keywords" in rule and any(kw in prompt_lower for kw in ["card", "plastic", "rewards", "credit card"]):
            return True
        elif "investment/portfolio/trading keywords" in rule and any(kw in prompt_lower for kw in ["investment", "portfolio", "trading", "wealth"]):
            return True
        elif "KYC/AML/compliance keywords" in rule and any(kw in prompt_lower for kw in ["kyc", "aml", "compliance", "regulation"]):
            return True
        elif "epic-level transformation" in rule and any(kw in prompt_lower for kw in ["epic", "platform", "system", "transformation"]):
            return True
        elif "implementation-focused" in rule and any(kw in prompt_lower for kw in ["implement", "create", "build", "develop"]):
            return True
        
        return False
    
    def _extract_action_from_rule(self, rule: str) -> str:
        """Extract the recommended action from a routing rule."""
        if "create_banking_feature" in rule:
            return "create_banking_feature"
        elif "create_compliance_story" in rule:
            return "create_compliance_story"
        elif "create_epic" in rule:
            return "create_epic"
        elif "create_story" in rule:
            return "create_story"
        
        return "create_feature"
    
    def _create_specification_file(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create specification file based on detected action and context."""
        action = context.get("detected_action", {}).get("action", "create_feature")
        banking_context = context.get("banking_context", {})
        
        result = {
            "file_created": None,
            "spec_info": {},
            "generation_method": "schema_processor"
        }
        
        try:
            if action == "create_epic":
                result.update(self._create_epic_spec(prompt, banking_context, context))
            elif action == "create_banking_feature":
                result.update(self._create_banking_feature_spec(prompt, banking_context, context))
            elif action == "create_compliance_story":
                result.update(self._create_compliance_story_spec(prompt, banking_context, context))
            elif action in ["create_story", "create_feature"]:
                result.update(self._create_feature_spec(prompt, banking_context, context))
            
        except Exception as e:
            result["errors"] = [str(e)]
            print(f"❌ Error creating specification file: {e}")
        
        return result
    
    def _create_epic_spec(self, prompt: str, banking_context: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Create an epic specification file."""
        # Generate next epic ID
        epic_id = self._generate_next_id("epic")
        
        # Extract title from prompt
        title = self._extract_title_from_prompt(prompt, "epic")
        
        # Create epic content
        epic_content = self._generate_epic_content(epic_id, title, prompt, banking_context, context)
        
        # Write file
        epic_dir = project_root / "specs" / "epics"
        epic_dir.mkdir(exist_ok=True)
        epic_file = epic_dir / f"{epic_id}-{title.lower().replace(' ', '-')}.md"
        
        with open(epic_file, 'w', encoding='utf-8') as f:
            f.write(epic_content)
        
        return {
            "file_created": str(epic_file),
            "spec_info": {
                "id": epic_id,
                "title": title,
                "type": "epic",
                "banking_domain": banking_context.get("primary_product", "general")
            }
        }
    
    def _create_banking_feature_spec(self, prompt: str, banking_context: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Create a banking feature specification file."""
        # Generate next feature ID
        feature_id = self._generate_next_id("feature")
        
        # Extract title from prompt
        title = self._extract_title_from_prompt(prompt, "feature")
        
        # Create feature content
        feature_content = self._generate_banking_feature_content(feature_id, title, prompt, banking_context, context)
        
        # Write file
        feature_dir = project_root / "specs" / "features"
        feature_dir.mkdir(exist_ok=True)
        feature_file = feature_dir / f"{feature_id}-{title.lower().replace(' ', '-')}.md"
        
        with open(feature_file, 'w', encoding='utf-8') as f:
            f.write(feature_content)
        
        return {
            "file_created": str(feature_file),
            "spec_info": {
                "id": feature_id,
                "title": title,
                "type": "banking_feature",
                "product_type": banking_context.get("primary_product", "general")
            }
        }
    
    def _create_feature_spec(self, prompt: str, banking_context: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Create a general feature specification file."""
        # Generate next feature ID
        feature_id = self._generate_next_id("feature")
        
        # Extract title from prompt
        title = self._extract_title_from_prompt(prompt, "feature")
        
        # Create feature content
        feature_content = self._generate_feature_content(feature_id, title, prompt, banking_context, context)
        
        # Write file
        feature_dir = project_root / "specs" / "features"
        feature_dir.mkdir(exist_ok=True)
        feature_file = feature_dir / f"{feature_id}-{title.lower().replace(' ', '-')}.md"
        
        with open(feature_file, 'w', encoding='utf-8') as f:
            f.write(feature_content)
        
        return {
            "file_created": str(feature_file),
            "spec_info": {
                "id": feature_id,
                "title": title,
                "type": "feature"
            }
        }
    
    def _create_compliance_story_spec(self, prompt: str, banking_context: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Create a compliance story specification file."""
        # Generate next story ID
        story_id = self._generate_next_id("story")
        
        # Extract title from prompt
        title = self._extract_title_from_prompt(prompt, "story")
        
        # Create compliance story content
        story_content = self._generate_compliance_story_content(story_id, title, prompt, banking_context, context)
        
        # Write file
        story_dir = project_root / "specs" / "stories"
        story_dir.mkdir(exist_ok=True)
        story_file = story_dir / f"{story_id}-{title.lower().replace(' ', '-')}.md"
        
        with open(story_file, 'w', encoding='utf-8') as f:
            f.write(story_content)
        
        return {
            "file_created": str(story_file),
            "spec_info": {
                "id": story_id,
                "title": title,
                "type": "compliance_story",
                "compliance_areas": context.get("compliance_requirements", [])
            }
        }
    
    def _generate_next_id(self, spec_type: str) -> str:
        """Generate the next available ID for a specification type."""
        if spec_type == "epic":
            prefix = "E"
            directory = project_root / "specs" / "epics"
        elif spec_type == "feature":
            prefix = "F"
            directory = project_root / "specs" / "features"
        elif spec_type == "story":
            prefix = "S"
            directory = project_root / "specs" / "stories"
        else:
            return f"{spec_type.upper()}001"
        
        if not directory.exists():
            return f"{prefix}001"
        
        # Find highest existing ID
        max_id = 0
        for file_path in directory.glob(f"{prefix}*.md"):
            match = re.match(rf"{prefix}(\d+)", file_path.name)
            if match:
                max_id = max(max_id, int(match.group(1)))
        
        return f"{prefix}{max_id + 1:03d}"
    
    def _extract_title_from_prompt(self, prompt: str, spec_type: str) -> str:
        """Extract a meaningful title from the prompt."""
        # Remove common action words
        cleaned = re.sub(r'\b(create|add|build|implement|develop|generate)\b', '', prompt, flags=re.IGNORECASE)
        cleaned = re.sub(r'\b(epic|feature|story)\b', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\b(for|with|using|under)\b', '', cleaned, flags=re.IGNORECASE)
        
        # Extract meaningful words
        words = [word.strip() for word in cleaned.split() if len(word.strip()) > 2]
        
        # Take first 5-6 words for title
        title_words = words[:6]
        title = ' '.join(title_words).strip()
        
        if not title:
            title = f"Generated {spec_type.title()}"
        
        return title.title()
    
    def _generate_epic_content(self, epic_id: str, title: str, prompt: str, banking_context: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate epic specification content."""
        return f"""# Epic {epic_id}: {title}

## Epic Overview
Generated from prompt: "{prompt}"

**Banking Domain**: {banking_context.get("primary_product", "General").title()}
**Primary Product Types**: {", ".join(banking_context.get("product_types", ["General"]))}

## Business Value
This epic delivers strategic value in the {banking_context.get("primary_product", "banking")} domain by implementing {title.lower()}.

## Scope and Objectives
- Implement core functionality for {title.lower()}
- Ensure compliance with banking regulations
- Deliver scalable and secure solution
- Enable future feature expansion

## Key Features
- Core {banking_context.get("primary_product", "banking")} functionality
- Regulatory compliance framework
- Security and audit controls
- API integration capabilities

## Acceptance Criteria
- [ ] All functional requirements implemented
- [ ] Security requirements validated
- [ ] Compliance requirements verified
- [ ] Performance benchmarks met
- [ ] Documentation completed

## Dependencies
- Core banking platform
- Regulatory framework
- Security infrastructure
- Integration APIs

## Risk Assessment
- **Technical Risk**: Medium - Standard banking domain implementation
- **Compliance Risk**: {("High" if banking_context.get("compliance_areas") else "Low")} - {"Regulatory requirements identified" if banking_context.get("compliance_areas") else "Standard compliance needed"}
- **Business Risk**: Medium - Strategic initiative

## Success Metrics
- Feature delivery on schedule
- Quality metrics achievement
- User acceptance validation
- Compliance certification

---
**Created**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Generator**: PromptToProduct Schema Processor v{self.schema.get("version", "2.0")}
**Banking Context**: {banking_context.get("confidence_score", 0.0):.1f} confidence
"""

    def _generate_banking_feature_content(self, feature_id: str, title: str, prompt: str, banking_context: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate banking feature specification content."""
        product_type = banking_context.get("primary_product", "general")
        compliance_reqs = context.get("compliance_requirements", [])
        
        return f"""# Feature {feature_id}: {title}

## Feature Overview
Generated from prompt: "{prompt}"

**Product Type**: {product_type.title()}
**Banking Domain**: {", ".join(banking_context.get("product_types", ["General"]))}
**Compliance Requirements**: {", ".join(compliance_reqs) if compliance_reqs else "Standard banking compliance"}

## Business Goal
Implement {title.lower()} functionality within the {product_type} domain to enhance customer experience and operational efficiency.

## Functional Requirements

### Core Capabilities
- Primary {product_type} functionality
- Real-time processing capabilities
- Data validation and verification
- Error handling and recovery

### Banking-Specific Features
{self._generate_banking_specific_features(product_type)}

### Integration Requirements
- Core banking system integration
- Third-party service connectivity
- API gateway compatibility
- Event streaming support

## Technical Requirements

### Architecture
- Microservices architecture
- Event-driven design
- RESTful API interfaces
- Database optimization

### Performance
- Response time < 500ms for standard operations
- Support for high transaction volumes
- Horizontal scaling capability
- 99.9% availability target

### Security Requirements
- End-to-end encryption
- Multi-factor authentication
- Audit trail logging
- PCI-DSS compliance (if applicable)

## Compliance & Regulatory

### Applicable Regulations
{self._generate_compliance_section(compliance_reqs, product_type)}

### Audit Requirements
- Transaction logging
- Access control monitoring
- Data retention policies
- Regulatory reporting

## User Stories
- [ ] Link to user stories (to be created)
- [ ] Acceptance criteria validation
- [ ] User experience testing
- [ ] Performance validation

## Testing Strategy
- Unit testing coverage > 90%
- Integration testing suite
- Security testing validation
- Compliance verification testing

## Implementation Plan
1. **Phase 1**: Core functionality development
2. **Phase 2**: Integration implementation
3. **Phase 3**: Security and compliance validation
4. **Phase 4**: Performance optimization and testing

---
**Created**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Generator**: PromptToProduct Schema Processor v{self.schema.get("version", "2.0")}
**Product Type**: {product_type}
**Schema Confidence**: {banking_context.get("confidence_score", 0.0):.1f}
"""

    def _generate_feature_content(self, feature_id: str, title: str, prompt: str, banking_context: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate general feature specification content."""
        return f"""# Feature {feature_id}: {title}

## Feature Overview
Generated from prompt: "{prompt}"

**Domain**: {"Banking" if banking_context.get("is_banking") else "General"}
**Type**: Feature Implementation

## Business Goal
Implement {title.lower()} to meet business requirements and enhance system capabilities.

## Functional Requirements

### Core Functionality
- Primary feature implementation
- Data processing capabilities
- User interface components
- Integration endpoints

### Technical Capabilities
- RESTful API design
- Database operations
- Error handling
- Logging and monitoring

## Technical Requirements

### Architecture
- Component-based design
- Service layer implementation
- Data access layer
- Presentation layer

### Performance
- Optimized response times
- Scalable architecture
- Resource efficiency
- Load balancing support

## User Stories
- [ ] User story implementation
- [ ] Acceptance criteria definition
- [ ] Testing requirements
- [ ] Documentation updates

## Implementation Details
1. **Design Phase**: Architecture and component design
2. **Development Phase**: Core functionality implementation
3. **Testing Phase**: Comprehensive testing suite
4. **Deployment Phase**: Production deployment and monitoring

---
**Created**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Generator**: PromptToProduct Schema Processor v{self.schema.get("version", "2.0")}
"""

    def _generate_compliance_story_content(self, story_id: str, title: str, prompt: str, banking_context: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate compliance story specification content."""
        compliance_reqs = context.get("compliance_requirements", [])
        primary_regulation = compliance_reqs[0] if compliance_reqs else "Banking Compliance"
        
        return f"""# Story {story_id}: {title}

## Story Overview
Generated from prompt: "{prompt}"

**Compliance Focus**: {primary_regulation}
**Regulatory Requirements**: {", ".join(compliance_reqs) if compliance_reqs else "Standard compliance"}
**Banking Context**: {banking_context.get("primary_product", "General").title()}

## User Story
As a **compliance officer**
I want **{title.lower()}**
So that **our system meets {primary_regulation} requirements and regulatory standards**

## Compliance Requirements

### Regulatory Framework
{self._generate_regulatory_framework(compliance_reqs)}

### Audit Trail Requirements
- Complete transaction logging
- User action tracking
- Data access monitoring
- Change management records

### Data Protection
- Encryption at rest and in transit
- Access control implementation
- Data retention policies
- Privacy protection measures

## Acceptance Criteria

### Functional Criteria
- [ ] All regulatory requirements implemented
- [ ] Audit trail generation verified
- [ ] Data protection measures validated
- [ ] Reporting capabilities tested

### Compliance Criteria
- [ ] {primary_regulation} requirements met
- [ ] Documentation completed
- [ ] Training materials prepared
- [ ] Compliance testing passed

### Technical Criteria
- [ ] Security controls implemented
- [ ] Performance requirements met
- [ ] Integration testing completed
- [ ] Monitoring and alerting configured

## Implementation Tasks

### Development Tasks
1. **Compliance Framework Setup**
   - Implement regulatory controls
   - Configure audit logging
   - Set up data protection

2. **Validation Implementation**
   - Create validation rules
   - Implement verification checks
   - Configure reporting

3. **Testing and Verification**
   - Compliance testing suite
   - Security validation
   - Performance verification

### Compliance Tasks
1. **Documentation**
   - Compliance documentation
   - Process documentation
   - Training materials

2. **Validation**
   - Regulatory review
   - Compliance testing
   - Audit preparation

## Risk Assessment
- **Compliance Risk**: {"High" if len(compliance_reqs) > 1 else "Medium"}
- **Implementation Risk**: Medium
- **Timeline Risk**: Low

## Success Criteria
- All compliance requirements validated
- Regulatory approval obtained
- System performance maintained
- Documentation completed

---
**Created**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Generator**: PromptToProduct Schema Processor v{self.schema.get("version", "2.0")}
**Compliance Focus**: {primary_regulation}
**Regulatory Count**: {len(compliance_reqs)}
"""

    def _generate_banking_specific_features(self, product_type: str) -> str:
        """Generate banking-specific features based on product type."""
        product_config = self.banking_domain.get("product_types", {}).get(product_type, {})
        common_features = product_config.get("common_features", [])
        
        if common_features:
            return "\n".join([f"- {feature.title()}" for feature in common_features])
        else:
            return "- Standard banking functionality\n- Regulatory compliance\n- Security controls\n- Audit capabilities"
    
    def _generate_compliance_section(self, compliance_reqs: List[str], product_type: str) -> str:
        """Generate compliance section based on requirements."""
        if compliance_reqs:
            return "\n".join([f"- **{req}**: Applicable requirements and controls" for req in compliance_reqs])
        else:
            return f"- **Banking Regulations**: Standard {product_type} compliance\n- **Data Protection**: Privacy and security requirements\n- **Audit Standards**: Logging and monitoring requirements"
    
    def _generate_regulatory_framework(self, compliance_reqs: List[str]) -> str:
        """Generate regulatory framework section."""
        if compliance_reqs:
            framework = []
            for req in compliance_reqs:
                if req == "KYC":
                    framework.append("- **Know Your Customer (KYC)**: Customer identification and verification requirements")
                elif req == "AML":
                    framework.append("- **Anti-Money Laundering (AML)**: Transaction monitoring and suspicious activity reporting")
                elif req == "PCI-DSS":
                    framework.append("- **PCI-DSS**: Payment card data security standards and requirements")
                elif req == "SOX":
                    framework.append("- **Sarbanes-Oxley (SOX)**: Financial reporting and internal controls")
                elif req == "GDPR":
                    framework.append("- **GDPR**: Data protection and privacy requirements")
                else:
                    framework.append(f"- **{req}**: Applicable regulatory requirements and controls")
            return "\n".join(framework)
        else:
            return "- **Standard Banking Compliance**: Applicable regulatory requirements\n- **Data Protection**: Privacy and security standards\n- **Audit Requirements**: Logging and monitoring standards"
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple similarity score between two texts."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0

def main():
    """CLI interface for testing the schema processor."""
    import argparse
    
    parser = argparse.ArgumentParser(description="PromptToProduct Schema Processor")
    parser.add_argument("prompt", nargs="?", help="Prompt to process")
    parser.add_argument("--test", action="store_true", help="Run test scenarios")
    parser.add_argument("--schema-info", action="store_true", help="Show schema information")
    args = parser.parse_args()
    
    # Initialize schema processor
    processor = PromptToProductSchema()
    
    if args.schema_info:
        print("📋 Schema Information")
        print("=" * 40)
        print(f"Name: {processor.schema.get('name', 'Unknown')}")
        print(f"Version: {processor.schema.get('version', '0.0')}")
        print(f"Product Types: {len(processor.banking_domain.get('product_types', {}))}")
        print(f"Actions: {len(processor.actions)}")
        print(f"Routing Rules: {len(processor.routing_rules)}")
        return
    
    if args.test:
        print("🧪 Running Test Scenarios")
        print("=" * 40)
        
        test_prompts = [
            "Create a credit card fraud detection system",
            "Add a feature for loan application processing",
            "Create a compliance story for KYC verification",
            "Build a payment processing API"
        ]
        
        for prompt in test_prompts:
            print(f"\n📝 Testing: {prompt}")
            result = processor.process_prompt(prompt)
            print(f"   Action: {result.get('detected_action', {}).get('action', 'unknown')}")
            print(f"   Banking: {result.get('banking_context', {}).get('is_banking', False)}")
            print(f"   File: {result.get('file_created', 'None')}")
        return
    
    if not args.prompt:
        print("Usage: python schema_processor.py '<prompt>' or --test or --schema-info")
        return
    
    # Process the prompt
    print(f"🔧 Processing: {args.prompt}")
    print("-" * 50)
    
    result = processor.process_prompt(args.prompt)
    
    # Display results
    print(f"✅ Success: {result.get('success', False)}")
    print(f"🎯 Action: {result.get('detected_action', {}).get('action', 'unknown')}")
    print(f"🏦 Banking: {result.get('banking_context', {}).get('is_banking', False)}")
    print(f"📁 File Created: {result.get('file_created', 'None')}")
    
    if result.get('compliance_requirements'):
        print(f"📋 Compliance: {', '.join(result['compliance_requirements'])}")
    
    if result.get('errors'):
        print(f"❌ Errors: {', '.join(result['errors'])}")

if __name__ == "__main__":
    main()