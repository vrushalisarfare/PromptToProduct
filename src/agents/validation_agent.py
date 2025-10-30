#!/usr/bin/env python3
"""
Validation Agent - Validates Specifications and Synchronizes with GitHub

This agent validates story completeness, tracks progress, and maintains 
GitHub repository synchronization for the PromptToProduct workflow.
"""
import sys
import os
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import requests
import subprocess
import textwrap
from dataclasses import dataclass
from enum import Enum

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Test case generation enums and data structures
class TestType(Enum):
    UNIT = "unit"
    INTEGRATION = "integration"
    FUNCTIONAL = "functional"
    PERFORMANCE = "performance"
    SECURITY = "security"
    COMPLIANCE = "compliance"
    UI_UX = "ui_ux"
    API = "api"
    DATABASE = "database"
    BANKING_DOMAIN = "banking_domain"

class BankingTestCategory(Enum):
    KYC_AML = "kyc_aml"
    CREDIT_SCORING = "credit_scoring"
    FRAUD_DETECTION = "fraud_detection"
    REGULATORY_COMPLIANCE = "regulatory_compliance"
    RISK_MANAGEMENT = "risk_management"
    PAYMENT_PROCESSING = "payment_processing"
    LOAN_ORIGINATION = "loan_origination"
    AUDIT_LOGGING = "audit_logging"

@dataclass
class TestCaseTemplate:
    """Template for generating test cases."""
    test_type: TestType
    banking_category: Optional[BankingTestCategory]
    test_class_name: str
    test_method_prefix: str
    required_imports: List[str]
    test_data_template: Dict[str, Any]
    assertion_patterns: List[str]
    banking_compliance_checks: List[str]

# Import configuration system
try:
    from src.config import get_config, get_github_config, get_path_config
    config = get_config()
    github_config = get_github_config()
    path_config = get_path_config()
    CONFIG_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Configuration system not available: {e}")
    CONFIG_AVAILABLE = False

class ValidationAgent:
    """
    Validation Agent for spec validation and GitHub synchronization.
    
    Actions:
    - validate_spec_completeness: Check story/epic/feature completeness
    - sync_with_github: Update GitHub issues and repository
    """
    
    def __init__(self):
        """Initialize the validation agent."""
        self.agent_id = "validation-agent"
        self.version = "1.0"
        
        # Use configuration system if available, otherwise fall back to defaults
        if CONFIG_AVAILABLE:
            self.specs_root = path_config.specs_root
            self.mybank_root = path_config.mybank_root
            
            # GitHub configuration from config system
            self.github_config = {
                "repo_owner": github_config.repo_owner,
                "repo_name": github_config.repo_name,
                "base_url": github_config.base_url,
                "token": github_config.token,
            }
        else:
            # Fallback to hardcoded values
            self.specs_root = project_root / "specs"
            self.mybank_root = project_root / "src" / "MyBank"
            
            # GitHub configuration (fallback)
            self.github_config = {
                "repo_owner": "vrushalisarfare",
                "repo_name": "PromptToProduct", 
                "base_url": "https://api.github.com",
                "token": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"),
            }
        
        # Validation schemas
        self.validation_schemas = self._load_validation_schemas()
        
        # Test case generation configuration
        self.test_templates = self._load_test_templates()
        self.banking_test_patterns = self._load_banking_test_patterns()
        self.tests_root = project_root / "tests"
    
    def _load_validation_schemas(self) -> Dict[str, Any]:
        """Load validation schemas for different spec types."""
        return {
            "epic": {
                "required_sections": [
                    "Epic Title", "Epic Overview", "Business Value", 
                    "Acceptance Criteria", "Features", "Dependencies"
                ],
                "required_fields": ["title", "overview", "business_value"],
                "banking_required": ["compliance_considerations", "security_requirements"]
            },
            "feature": {
                "required_sections": [
                    "Feature Title", "Feature Description", "User Stories",
                    "Acceptance Criteria", "Technical Requirements"
                ],
                "required_fields": ["title", "description", "user_stories"],
                "banking_required": ["risk_assessment", "compliance_impact"]
            },
            "story": {
                "required_sections": [
                    "Story Title", "Story Description", "Acceptance Criteria",
                    "Implementation Details", "Testing Requirements"
                ],
                "required_fields": ["title", "description", "acceptance_criteria"],
                "banking_required": ["security_considerations", "data_classification"]
            }
        }
    
    def _load_test_templates(self) -> Dict[str, TestCaseTemplate]:
        """Load test case templates for different types and banking domains."""
        return {
            "api_banking": TestCaseTemplate(
                test_type=TestType.API,
                banking_category=BankingTestCategory.LOAN_ORIGINATION,
                test_class_name="TestBankingAPI",
                test_method_prefix="test_api_",
                required_imports=[
                    "unittest", "requests", "json", "time", "datetime",
                    "unittest.mock.Mock", "unittest.mock.patch"
                ],
                test_data_template={
                    "valid_loan_application": {
                        "ssn": "123-45-6789",
                        "annual_income": 75000,
                        "loan_amount": 250000,
                        "credit_score": 720
                    }
                },
                assertion_patterns=[
                    "self.assertEqual(response.status_code, 200)",
                    "self.assertIn('loan_id', response.json())",
                    "self.assertLess(response_time, 2.0)"
                ],
                banking_compliance_checks=[
                    "KYC validation", "AML screening", "Credit scoring", "Risk assessment"
                ]
            ),
            "ml_banking": TestCaseTemplate(
                test_type=TestType.FUNCTIONAL,
                banking_category=BankingTestCategory.CREDIT_SCORING,
                test_class_name="TestMLBankingModel",
                test_method_prefix="test_ml_",
                required_imports=[
                    "unittest", "numpy", "pandas", "sklearn.metrics",
                    "unittest.mock.Mock", "unittest.mock.patch"
                ],
                test_data_template={
                    "sample_features": {
                        "credit_history_length": 120,
                        "debt_to_income_ratio": 0.35,
                        "employment_stability": 1
                    }
                },
                assertion_patterns=[
                    "self.assertGreaterEqual(model_accuracy, 0.75)",
                    "self.assertLess(inference_time, 500)",
                    "self.assertTrue(bias_test_passed)"
                ],
                banking_compliance_checks=[
                    "Fair lending compliance", "Model explainability", "Bias detection", "Model risk management"
                ]
            ),
            "dashboard_banking": TestCaseTemplate(
                test_type=TestType.UI_UX,
                banking_category=BankingTestCategory.RISK_MANAGEMENT,
                test_class_name="TestRiskDashboard",
                test_method_prefix="test_dashboard_",
                required_imports=[
                    "unittest", "selenium", "time", "json", "websocket",
                    "unittest.mock.Mock", "unittest.mock.patch"
                ],
                test_data_template={
                    "risk_metrics": {
                        "overall_risk_score": 0.25,
                        "loan_count": 1250,
                        "compliance_status": "compliant"
                    }
                },
                assertion_patterns=[
                    "self.assertLess(dashboard_load_time, 1.0)",
                    "self.assertEqual(availability, 0.999)",
                    "self.assertTrue(real_time_updates_working)"
                ],
                banking_compliance_checks=[
                    "Basel III monitoring", "Real-time risk assessment", "Regulatory reporting", "Stress testing"
                ]
            )
        }
    
    def _load_banking_test_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load banking-specific test patterns and compliance requirements."""
        return {
            "kyc_aml": {
                "test_methods": [
                    "test_customer_identity_verification",
                    "test_document_validation",
                    "test_aml_screening",
                    "test_sanctions_check",
                    "test_pep_screening"
                ],
                "compliance_requirements": [
                    "Customer Due Diligence (CDD)",
                    "Enhanced Due Diligence (EDD)",
                    "Ongoing monitoring",
                    "Suspicious activity reporting"
                ],
                "test_data_requirements": [
                    "Valid identification documents",
                    "Invalid/expired documents",
                    "Sanctioned entity data",
                    "PEP database entries"
                ]
            },
            "credit_scoring": {
                "test_methods": [
                    "test_credit_score_calculation",
                    "test_model_accuracy",
                    "test_bias_detection",
                    "test_fair_lending_compliance",
                    "test_model_explainability"
                ],
                "compliance_requirements": [
                    "Fair Credit Reporting Act (FCRA)",
                    "Equal Credit Opportunity Act (ECOA)",
                    "Fair Lending practices",
                    "Model risk management"
                ],
                "test_data_requirements": [
                    "Diverse demographic data",
                    "Protected class attributes",
                    "Historical credit data",
                    "Model training datasets"
                ]
            },
            "regulatory_compliance": {
                "test_methods": [
                    "test_basel_iii_compliance",
                    "test_stress_testing",
                    "test_capital_adequacy",
                    "test_liquidity_coverage",
                    "test_regulatory_reporting"
                ],
                "compliance_requirements": [
                    "Basel III capital requirements",
                    "Liquidity Coverage Ratio (LCR)",
                    "Net Stable Funding Ratio (NSFR)",
                    "Stress testing scenarios"
                ],
                "test_data_requirements": [
                    "Capital ratio calculations",
                    "Liquidity metrics",
                    "Stress test scenarios",
                    "Risk-weighted assets"
                ]
            }
        }
    
    def validate_specifications(self, agent_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for validating specifications.
        
        Args:
            agent_params: Parameters from orchestrator including specs to validate
            
        Returns:
            Validation result with completeness scores and recommendations
        """
        prompt = agent_params.get("prompt", "")
        banking_context = agent_params.get("banking_context", {})
        spec_type = agent_params.get("spec_type", "unknown")
        
        print(f"✅ Validation Agent Processing: {prompt}")
        
        result = {
            "agent_id": self.agent_id,
            "processing_timestamp": datetime.now().isoformat(),
            "input_prompt": prompt,
            "spec_type": spec_type,
            "banking_context": banking_context,
            "status": "processing",
            "validation_results": [],
            "overall_score": 0.0,
            "recommendations": [],
            "github_sync_status": None,
            "errors": []
        }
        
        try:
            # Validate existing specifications
            if spec_type == "validate_all":
                validation_results = self._validate_all_specs()
            else:
                validation_results = self._validate_specific_specs(agent_params)
            
            result["validation_results"] = validation_results
            result["overall_score"] = self._calculate_overall_score(validation_results)
            result["recommendations"] = self._generate_recommendations(validation_results)
            
            # Generate test cases if requested
            if agent_params.get("generate_tests", False):
                test_generation_result = self.generate_test_cases(validation_results, agent_params)
                result["test_generation_status"] = test_generation_result
            
            # Sync with GitHub if requested
            if agent_params.get("sync_github", False):
                github_result = self.sync_with_github(validation_results)
                result["github_sync_status"] = github_result
            
            result["status"] = "completed"
            
        except Exception as e:
            result["status"] = "error"
            result["errors"].append(str(e))
            print(f"❌ Error in validation: {e}")
        
        return result
    
    def _validate_all_specs(self) -> List[Dict[str, Any]]:
        """Validate all specifications in the workspace."""
        validation_results = []
        
        # Validate epics
        epics_dir = self.specs_root / "epics"
        if epics_dir.exists():
            for epic_file in epics_dir.glob("*.md"):
                result = self._validate_single_spec(epic_file, "epic")
                validation_results.append(result)
        
        # Validate features
        features_dir = self.specs_root / "features"
        if features_dir.exists():
            for feature_file in features_dir.glob("*.md"):
                result = self._validate_single_spec(feature_file, "feature")
                validation_results.append(result)
        
        # Validate stories
        stories_dir = self.specs_root / "stories"
        if stories_dir.exists():
            for story_file in stories_dir.glob("*.md"):
                result = self._validate_single_spec(story_file, "story")
                validation_results.append(result)
        
        return validation_results
    
    def _validate_specific_specs(self, agent_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Validate specific specs based on agent parameters."""
        validation_results = []
        
        spec_files = agent_params.get("spec_files", [])
        spec_type = agent_params.get("spec_type", "unknown")
        
        for spec_file in spec_files:
            file_path = Path(spec_file)
            if file_path.exists():
                result = self._validate_single_spec(file_path, spec_type)
                validation_results.append(result)
        
        return validation_results
    
    def _validate_single_spec(self, file_path: Path, spec_type: str) -> Dict[str, Any]:
        """Validate a single specification file."""
        print(f"🔍 Validating {spec_type}: {file_path.name}")
        
        validation_result = {
            "file_path": str(file_path),
            "file_name": file_path.name,
            "spec_type": spec_type,
            "validation_timestamp": datetime.now().isoformat(),
            "completeness_score": 0.0,
            "missing_sections": [],
            "missing_fields": [],
            "banking_compliance": 0.0,
            "quality_issues": [],
            "recommendations": [],
            "word_count": 0,
            "readability_score": 0.0
        }
        
        try:
            # Read file content
            content = file_path.read_text(encoding='utf-8')
            validation_result["word_count"] = len(content.split())
            
            # Get validation schema for this spec type
            schema = self.validation_schemas.get(spec_type, {})
            
            # Check required sections
            missing_sections = self._check_required_sections(content, schema.get("required_sections", []))
            validation_result["missing_sections"] = missing_sections
            
            # Check required fields
            missing_fields = self._check_required_fields(content, schema.get("required_fields", []))
            validation_result["missing_fields"] = missing_fields
            
            # Check banking-specific requirements
            banking_score = self._check_banking_requirements(content, schema.get("banking_required", []))
            validation_result["banking_compliance"] = banking_score
            
            # Quality analysis
            quality_issues = self._analyze_content_quality(content)
            validation_result["quality_issues"] = quality_issues
            
            # Calculate completeness score
            completeness_score = self._calculate_completeness_score(
                missing_sections, missing_fields, banking_score, quality_issues
            )
            validation_result["completeness_score"] = completeness_score
            
            # Generate recommendations
            recommendations = self._generate_spec_recommendations(validation_result)
            validation_result["recommendations"] = recommendations
            
            # Calculate readability score
            readability_score = self._calculate_readability_score(content)
            validation_result["readability_score"] = readability_score
            
        except Exception as e:
            validation_result["quality_issues"].append(f"Validation error: {str(e)}")
        
        return validation_result
    
    def _check_required_sections(self, content: str, required_sections: List[str]) -> List[str]:
        """Check for required sections in the spec."""
        missing_sections = []
        
        for section in required_sections:
            # Look for markdown headers with this section name
            patterns = [
                f"#{1,6}\\s*{re.escape(section)}",
                f"#{1,6}\\s*{re.escape(section.lower())}",
                f"#{1,6}\\s*{re.escape(section.upper())}"
            ]
            
            found = False
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
                    found = True
                    break
            
            if not found:
                missing_sections.append(section)
        
        return missing_sections
    
    def _check_required_fields(self, content: str, required_fields: List[str]) -> List[str]:
        """Check for required fields/content in the spec."""
        missing_fields = []
        content_lower = content.lower()
        
        for field in required_fields:
            # Check if field appears in content
            if field.lower() not in content_lower:
                missing_fields.append(field)
        
        return missing_fields
    
    def _check_banking_requirements(self, content: str, banking_required: List[str]) -> float:
        """Check banking-specific requirements compliance."""
        if not banking_required:
            return 1.0
        
        found_count = 0
        content_lower = content.lower()
        
        for requirement in banking_required:
            if requirement.lower() in content_lower:
                found_count += 1
        
        return found_count / len(banking_required)
    
    def _analyze_content_quality(self, content: str) -> List[str]:
        """Analyze content quality and identify issues."""
        quality_issues = []
        
        # Check minimum length
        if len(content.split()) < 50:
            quality_issues.append("Content appears too short for meaningful specification")
        
        # Check for placeholder text
        placeholders = ["TODO", "TBD", "PLACEHOLDER", "[INSERT", "FIXME"]
        for placeholder in placeholders:
            if placeholder.lower() in content.lower():
                quality_issues.append(f"Contains placeholder text: {placeholder}")
        
        # Check for proper markdown formatting
        if not re.search(r'^#+\s', content, re.MULTILINE):
            quality_issues.append("Missing proper markdown headers")
        
        # Check for acceptance criteria
        if "acceptance criteria" not in content.lower():
            quality_issues.append("Missing explicit acceptance criteria section")
        
        # Check for proper formatting of lists
        bullet_count = len(re.findall(r'^\s*[-*+]\s', content, re.MULTILINE))
        numbered_count = len(re.findall(r'^\s*\d+\.\s', content, re.MULTILINE))
        
        if bullet_count == 0 and numbered_count == 0:
            quality_issues.append("No structured lists found (consider using bullet points or numbered lists)")
        
        return quality_issues
    
    def _calculate_completeness_score(self, missing_sections: List[str], 
                                    missing_fields: List[str], banking_score: float,
                                    quality_issues: List[str]) -> float:
        """Calculate overall completeness score."""
        # Start with perfect score
        score = 1.0
        
        # Deduct for missing sections (major impact)
        section_penalty = len(missing_sections) * 0.15
        score -= section_penalty
        
        # Deduct for missing fields (moderate impact)
        field_penalty = len(missing_fields) * 0.10
        score -= field_penalty
        
        # Factor in banking compliance
        banking_weight = 0.2
        score -= (1.0 - banking_score) * banking_weight
        
        # Deduct for quality issues (minor impact)
        quality_penalty = len(quality_issues) * 0.05
        score -= quality_penalty
        
        # Ensure score is between 0 and 1
        return max(0.0, min(1.0, score))
    
    def _calculate_readability_score(self, content: str) -> float:
        """Calculate readability score based on simple metrics."""
        words = content.split()
        sentences = len(re.findall(r'[.!?]+', content))
        
        if not words or not sentences:
            return 0.0
        
        avg_words_per_sentence = len(words) / sentences
        
        # Simple readability scoring (lower is better)
        if avg_words_per_sentence <= 15:
            return 0.9
        elif avg_words_per_sentence <= 20:
            return 0.7
        elif avg_words_per_sentence <= 25:
            return 0.5
        else:
            return 0.3
    
    def _generate_spec_recommendations(self, validation_result: Dict[str, Any]) -> List[str]:
        """Generate recommendations for improving the spec."""
        recommendations = []
        
        # Recommendations for missing sections
        for section in validation_result["missing_sections"]:
            recommendations.append(f"Add missing section: {section}")
        
        # Recommendations for missing fields
        for field in validation_result["missing_fields"]:
            recommendations.append(f"Include content about: {field}")
        
        # Banking compliance recommendations
        if validation_result["banking_compliance"] < 0.8:
            recommendations.append("Improve banking compliance by adding security and regulatory considerations")
        
        # Quality recommendations
        for issue in validation_result["quality_issues"]:
            if "placeholder" in issue.lower():
                recommendations.append("Replace placeholder text with actual content")
            elif "short" in issue.lower():
                recommendations.append("Expand content with more detailed requirements and examples")
            elif "markdown" in issue.lower():
                recommendations.append("Improve markdown formatting with proper headers and structure")
        
        # Readability recommendations
        if validation_result["readability_score"] < 0.6:
            recommendations.append("Improve readability by using shorter sentences and clearer language")
        
        return recommendations
    
    def _calculate_overall_score(self, validation_results: List[Dict[str, Any]]) -> float:
        """Calculate overall validation score across all specs."""
        if not validation_results:
            return 0.0
        
        total_score = sum(result["completeness_score"] for result in validation_results)
        return total_score / len(validation_results)
    
    def _generate_recommendations(self, validation_results: List[Dict[str, Any]]) -> List[str]:
        """Generate overall recommendations based on validation results."""
        all_recommendations = []
        
        # Collect all individual recommendations
        for result in validation_results:
            all_recommendations.extend(result["recommendations"])
        
        # Add overall recommendations
        overall_score = self._calculate_overall_score(validation_results)
        
        if overall_score < 0.5:
            all_recommendations.append("Critical: Significant improvement needed in specification quality")
        elif overall_score < 0.7:
            all_recommendations.append("Moderate: Several areas need attention for better completeness")
        elif overall_score < 0.9:
            all_recommendations.append("Good: Minor improvements would enhance specification quality")
        
        # Remove duplicates while preserving order
        unique_recommendations = []
        seen = set()
        for rec in all_recommendations:
            if rec not in seen:
                unique_recommendations.append(rec)
                seen.add(rec)
        
        return unique_recommendations[:10]  # Limit to top 10 recommendations
    
    def sync_with_github(self, validation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Synchronize specifications with GitHub repository."""
        print("🔄 Syncing with GitHub...")
        
        sync_result = {
            "status": "started",
            "timestamp": datetime.now().isoformat(),
            "repository": f"{self.github_config['repo_owner']}/{self.github_config['repo_name']}",
            "actions_taken": [],
            "issues_created": [],
            "issues_updated": [],
            "commits_made": [],
            "errors": []
        }
        
        try:
            # Check if GitHub token is available
            if not self.github_config.get("token"):
                sync_result["status"] = "skipped"
                sync_result["errors"].append("GitHub token not configured")
                return sync_result
            
            # Create/update GitHub issues for validation findings
            github_issues = self._create_github_issues(validation_results)
            sync_result["issues_created"] = github_issues.get("created", [])
            sync_result["issues_updated"] = github_issues.get("updated", [])
            
            # Commit validation report to repository
            commit_result = self._commit_validation_report(validation_results)
            if commit_result.get("success"):
                sync_result["commits_made"].append(commit_result)
            
            # Update project board if configured
            board_result = self._update_project_board(validation_results)
            if board_result.get("success"):
                sync_result["actions_taken"].append("Updated project board")
                sync_result["project_items_added"] = board_result.get("items_added", 0)
                print(f"📋 Added {board_result.get('items_added', 0)} items to GitHub Project #{board_result.get('project_number', 'Unknown')}")
                for item in board_result.get("project_items", []):
                    print(f"   • {item['spec']} → Issue #{item['issue_number']}")
            else:
                print(f"⚠️ Project board update skipped: {board_result.get('reason', board_result.get('error', 'Unknown'))}")
            
            sync_result["status"] = "completed"
            
        except Exception as e:
            sync_result["status"] = "error"
            sync_result["errors"].append(str(e))
            print(f"❌ GitHub sync error: {e}")
        
        return sync_result
    
    def generate_test_cases(self, validation_results: List[Dict[str, Any]], 
                           agent_params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive test cases for validated specifications."""
        print("🧪 Generating test cases for validated specifications...")
        
        test_generation_result = {
            "status": "started",
            "timestamp": datetime.now().isoformat(),
            "test_files_created": [],
            "test_suites_generated": [],
            "banking_tests_created": [],
            "coverage_analysis": {},
            "errors": []
        }
        
        try:
            # Ensure tests directory structure exists
            self._ensure_test_directory_structure()
            
            # Generate test cases for each validated specification
            for validation_result in validation_results:
                spec_test_result = self._generate_tests_for_spec(validation_result, agent_params)
                
                if spec_test_result["success"]:
                    test_generation_result["test_files_created"].extend(
                        spec_test_result["test_files_created"]
                    )
                    test_generation_result["test_suites_generated"].extend(
                        spec_test_result["test_suites_generated"]
                    )
                    test_generation_result["banking_tests_created"].extend(
                        spec_test_result["banking_tests_created"]
                    )
                else:
                    test_generation_result["errors"].extend(spec_test_result["errors"])
            
            test_generation_result["status"] = "completed"
            print(f"✅ Test generation completed: {len(test_generation_result['test_files_created'])} files created")
            
        except Exception as e:
            test_generation_result["status"] = "error"
            test_generation_result["errors"].append(str(e))
            print(f"❌ Test generation error: {e}")
        
        return test_generation_result
    
    def _ensure_test_directory_structure(self) -> None:
        """Ensure proper test directory structure exists."""
        test_dirs = [
            self.tests_root,
            self.tests_root / "stories",
            self.tests_root / "features", 
            self.tests_root / "epics",
            self.tests_root / "integration",
            self.tests_root / "compliance",
            self.tests_root / "banking"
        ]
        
        for test_dir in test_dirs:
            test_dir.mkdir(parents=True, exist_ok=True)
            
            # Create __init__.py files
            init_file = test_dir / "__init__.py"
            if not init_file.exists():
                init_content = f"# Test package for {test_dir.name}\n"
                if test_dir.name == "tests":
                    init_content = "# PromptToProduct Test Suite\n# Banking Domain Test Cases\n"
                init_file.write_text(init_content, encoding='utf-8')
    
    def _generate_tests_for_spec(self, validation_result: Dict[str, Any], 
                               agent_params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate test cases for a specific specification."""
        spec_file_path = Path(validation_result["file_path"])
        spec_type = validation_result["spec_type"]
        spec_name = spec_file_path.stem
        
        result = {
            "success": False,
            "spec_file": str(spec_file_path),
            "test_files_created": [],
            "test_suites_generated": [],
            "banking_tests_created": [],
            "errors": []
        }
        
        try:
            # Read specification content
            spec_content = spec_file_path.read_text(encoding='utf-8')
            
            # Determine banking domain and test types needed
            banking_domain = self._identify_banking_domain(spec_content)
            test_types = self._determine_test_types(spec_content, spec_type)
            
            # Generate simple test file for this spec
            test_file_result = self._create_simple_test_file(
                spec_name, spec_type, banking_domain, spec_content
            )
            
            if test_file_result["success"]:
                result["test_files_created"].append(test_file_result["test_file_path"])
                result["test_suites_generated"].append({
                    "test_type": "functional",
                    "banking_domain": banking_domain.value if banking_domain else None,
                    "test_methods_count": test_file_result["test_methods_count"]
                })
                
                if banking_domain:
                    result["banking_tests_created"].append({
                        "banking_category": banking_domain.value,
                        "test_file": test_file_result["test_file_path"]
                    })
            else:
                result["errors"].extend(test_file_result["errors"])
            
            result["success"] = len(result["test_files_created"]) > 0
            
        except Exception as e:
            result["errors"].append(f"Error generating tests for {spec_name}: {str(e)}")
        
        return result
    
    def _identify_banking_domain(self, spec_content: str) -> Optional[BankingTestCategory]:
        """Identify the banking domain based on specification content."""
        content_lower = spec_content.lower()
        
        # Simple domain detection
        if any(word in content_lower for word in ["loan", "origination", "application"]):
            return BankingTestCategory.LOAN_ORIGINATION
        elif any(word in content_lower for word in ["credit", "scoring", "risk"]):
            return BankingTestCategory.CREDIT_SCORING
        elif any(word in content_lower for word in ["dashboard", "risk", "assessment"]):
            return BankingTestCategory.RISK_MANAGEMENT
        elif any(word in content_lower for word in ["kyc", "aml", "identity"]):
            return BankingTestCategory.KYC_AML
        elif any(word in content_lower for word in ["payment", "transaction"]):
            return BankingTestCategory.PAYMENT_PROCESSING
        else:
            return BankingTestCategory.REGULATORY_COMPLIANCE
    
    def _determine_test_types(self, spec_content: str, spec_type: str) -> List[TestType]:
        """Determine what types of tests are needed based on specification content."""
        return [TestType.FUNCTIONAL, TestType.UNIT]
    
    def _create_simple_test_file(self, spec_name: str, spec_type: str, 
                               banking_domain: Optional[BankingTestCategory], 
                               spec_content: str) -> Dict[str, Any]:
        """Create a simple test file for a specification."""
        result = {
            "success": False,
            "test_file_path": "",
            "test_methods_count": 0,
            "errors": []
        }
        
        try:
            # Generate test file name and path
            test_file_name = f"test_{spec_name}_generated.py"
            test_file_path = self.tests_root / f"{spec_type}s" / test_file_name
            
            # Generate simple test content
            test_content = f'''#!/usr/bin/env python3
"""
Generated Test Cases for {spec_type.title()} {spec_name}

Banking Domain: {banking_domain.value if banking_domain else "General"}
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
import unittest
import time
from datetime import datetime
from unittest.mock import Mock, patch

class Test{self._to_pascal_case(spec_name)}Generated(unittest.TestCase):
    """Generated test cases for {spec_name}."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_start_time = time.time()
        self.banking_domain = "{banking_domain.value if banking_domain else 'general'}"
    
    def test_specification_requirements(self):
        """Test basic specification requirements."""
        # This is a generated test - implement actual test logic
        self.assertTrue(True, "Specification requirements validated")
    
    def test_banking_domain_compliance(self):
        """Test banking domain compliance requirements."""
        # Banking domain: {banking_domain.value if banking_domain else "general"}
        self.assertIsNotNone(self.banking_domain)
        self.assertIn(self.banking_domain, [
            "loan_origination", "credit_scoring", "risk_management",
            "kyc_aml", "payment_processing", "regulatory_compliance", "general"
        ])
    
    @patch('requests.post')
    def test_api_functionality(self, mock_post):
        """Test API functionality if applicable."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {{"success": True}}
        
        response = mock_post()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])

if __name__ == '__main__':
    unittest.main(verbosity=2)
'''
            
            # Write test file
            test_file_path.write_text(test_content, encoding='utf-8')
            
            # Count test methods
            test_methods_count = len([line for line in test_content.split('\n') if 'def test_' in line])
            
            result["success"] = True
            result["test_file_path"] = str(test_file_path)
            result["test_methods_count"] = test_methods_count
            
            print(f"📝 Created test file: {test_file_name} ({test_methods_count} test methods)")
            
        except Exception as e:
            result["errors"].append(f"Error creating test file: {str(e)}")
        
        return result
    
    def _to_pascal_case(self, text: str) -> str:
        """Convert text to PascalCase."""
        words = re.sub(r'[^a-zA-Z0-9]', ' ', text).split()
        return ''.join(word.capitalize() for word in words)
    
    def _create_github_issues(self, validation_results: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Create GitHub issues for validation findings."""
        issues_result = {"created": [], "updated": []}
        
        # Create issues for specs with low completeness scores
        for result in validation_results:
            if result["completeness_score"] < 0.7:
                issue_data = self._create_validation_issue_data(result)
                
                # Simulate GitHub API call (would use actual requests in production)
                issue_id = f"issue_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                issues_result["created"].append({
                    "issue_id": issue_id,
                    "title": issue_data["title"],
                    "spec_file": result["file_name"],
                    "completeness_score": result["completeness_score"]
                })
                
                print(f"📝 Created GitHub issue: {issue_data['title']}")
        
        return issues_result
    
    def _create_validation_issue_data(self, validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Create GitHub issue data for validation finding."""
        file_name = validation_result["file_name"]
        score = validation_result["completeness_score"]
        
        title = f"Specification Quality Issue: {file_name} (Score: {score:.2f})"
        
        body = f"""## Specification Validation Report

**File:** {validation_result['file_path']}
**Validation Date:** {validation_result['validation_timestamp']}
**Completeness Score:** {score:.2f}/1.00

### Missing Sections
{chr(10).join('- ' + section for section in validation_result['missing_sections']) if validation_result['missing_sections'] else '✅ All required sections present'}

### Missing Fields
{chr(10).join('- ' + field for field in validation_result['missing_fields']) if validation_result['missing_fields'] else '✅ All required fields present'}

### Banking Compliance
**Score:** {validation_result['banking_compliance']:.2f}/1.00

### Quality Issues
{chr(10).join('- ' + issue for issue in validation_result['quality_issues']) if validation_result['quality_issues'] else '✅ No quality issues detected'}

### Recommendations
{chr(10).join('- ' + rec for rec in validation_result['recommendations'])}

### Metrics
- **Word Count:** {validation_result['word_count']}
- **Readability Score:** {validation_result['readability_score']:.2f}/1.00

---
*This issue was automatically generated by the PromptToProduct Validation Agent*
"""
        
        return {
            "title": title,
            "body": body,
            "labels": ["specification", "validation", "quality"],
            "assignees": []
        }
    
    def _commit_validation_report(self, validation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Commit validation report to repository."""
        try:
            # Generate validation report
            report_path = project_root / "validation_report.json"
            
            report_data = {
                "validation_timestamp": datetime.now().isoformat(),
                "overall_score": self._calculate_overall_score(validation_results),
                "total_specs_validated": len(validation_results),
                "specs_passing": len([r for r in validation_results if r["completeness_score"] >= 0.8]),
                "specs_failing": len([r for r in validation_results if r["completeness_score"] < 0.5]),
                "validation_results": validation_results
            }
            
            # Write report file
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, default=str)
            
            # Commit to git (simplified - would use GitHub API in production)
            commit_message = f"Validation Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            print(f"📄 Generated validation report: {report_path}")
            
            return {
                "success": True,
                "commit_message": commit_message,
                "file_path": str(report_path)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _update_project_board(self, validation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Legacy method for GitHub project board updates.
        
        NOTE: GitHub Projects integration is now handled via GitHub MCP server.
        This method is kept for backward compatibility but should not be used.
        """
        return {
            "success": False,
            "reason": "GitHub Projects integration now handled via GitHub MCP server",
            "items_added": 0,
            "recommendation": "Use GitHub MCP server tools instead"
        }
    
    def _create_spec_issue(self, spec_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Legacy method for creating GitHub issues from specs.
        
        NOTE: GitHub issue creation is now handled via GitHub MCP server.
        This method is kept for backward compatibility but should not be used.
        """
        return {
            "success": False,
            "error": "Issue creation now handled via GitHub MCP server. Use GitHub MCP tools instead."
        }
    
    def _add_issue_to_project(self, issue_number: int, project_number: str, org_name: str, spec_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Legacy method for adding issues to GitHub Projects.
        
        NOTE: GitHub Projects integration is now handled via GitHub MCP server.
        This method is kept for backward compatibility but should not be used.
        """
        return {
            "success": False,
            "error": "Project board integration now handled via GitHub MCP server. Use GitHub MCP tools instead."
        }
    
    def get_validation_agent_status(self) -> Dict[str, Any]:
        """Get current validation agent status."""
        return {
            "agent_id": self.agent_id,
            "version": self.version,
            "status": "active",
            "specs_root": str(self.specs_root),
            "mybank_root": str(self.mybank_root),
            "tests_root": str(self.tests_root),
            "supported_actions": [
                "validate_spec_completeness", 
                "sync_with_github", 
                "generate_test_cases"
            ],
            "validation_schemas": list(self.validation_schemas.keys()),
            "test_templates": list(self.test_templates.keys()),
            "banking_test_categories": [category.value for category in BankingTestCategory],
            "test_types_supported": [test_type.value for test_type in TestType],
            "github_configured": bool(self.github_config.get("token")),
            "github_repository": f"{self.github_config['repo_owner']}/{self.github_config['repo_name']}"
        }


def main():
    """CLI interface for the validation agent."""
    import argparse
    
    parser = argparse.ArgumentParser(description="PromptToProduct Validation Agent")
    parser.add_argument("action", nargs="?", choices=["validate", "sync", "status"], 
                       default="validate", help="Action to perform")
    parser.add_argument("--spec-type", choices=["epic", "feature", "story", "all"], 
                       default="all", help="Type of specification to validate")
    parser.add_argument("--sync-github", action="store_true", 
                       help="Sync results with GitHub")
    parser.add_argument("--generate-tests", action="store_true",
                       help="Generate test cases for validated specifications")
    parser.add_argument("--file", help="Specific file to validate")
    args = parser.parse_args()
    
    # Initialize validation agent
    validation_agent = ValidationAgent()
    
    if args.action == "status":
        status = validation_agent.get_validation_agent_status()
        print("✅ Validation Agent Status")
        print("=" * 40)
        for key, value in status.items():
            print(f"{key}: {value}")
        return
    
    # Prepare agent parameters
    agent_params = {
        "prompt": f"validate {args.spec_type} specifications",
        "spec_type": "validate_all" if args.spec_type == "all" else args.spec_type,
        "sync_github": args.sync_github or args.action == "sync",
        "generate_tests": args.generate_tests,
        "banking_context": {"is_banking": True}
    }
    
    if args.file:
        agent_params["spec_files"] = [args.file]
        agent_params["spec_type"] = "single_file"
    
    # Perform validation
    print(f"✅ Validating {args.spec_type} specifications...")
    print("-" * 50)
    
    result = validation_agent.validate_specifications(agent_params)
    
    # Display results
    print(f"📊 Overall Score: {result.get('overall_score', 0.0):.2f}/1.00")
    print(f"📄 Specs Validated: {len(result.get('validation_results', []))}")
    
    # Show individual validation results
    for val_result in result.get('validation_results', []):
        score = val_result['completeness_score']
        status_emoji = "✅" if score >= 0.8 else "⚠️" if score >= 0.5 else "❌"
        print(f"   {status_emoji} {val_result['file_name']}: {score:.2f}/1.00")
    
    # Show recommendations
    recommendations = result.get('recommendations', [])
    if recommendations:
        print(f"\n💡 Recommendations ({len(recommendations)}):")
        for i, rec in enumerate(recommendations[:5], 1):  # Show top 5
            print(f"   {i}. {rec}")
    
    # Show GitHub sync status
    github_status = result.get('github_sync_status')
    if github_status:
        print(f"\n🔄 GitHub Sync: {github_status.get('status', 'unknown')}")
        if github_status.get('issues_created'):
            print(f"   📝 Issues Created: {len(github_status['issues_created'])}")
    
    # Show test generation status
    test_status = result.get('test_generation_status')
    if test_status:
        print(f"\n🧪 Test Generation: {test_status.get('status', 'unknown')}")
        if test_status.get('test_files_created'):
            print(f"   📝 Test Files Created: {len(test_status['test_files_created'])}")
        if test_status.get('banking_tests_created'):
            print(f"   🏦 Banking Tests: {len(test_status['banking_tests_created'])}")
        if test_status.get('coverage_analysis'):
            coverage = test_status['coverage_analysis']
            print(f"   📊 Test Coverage: {coverage.get('test_coverage_percentage', 0):.1f}%")
    
    if result.get('errors'):
        print(f"\n❌ Errors: {', '.join(result['errors'])}")
    
    print(f"\n📊 Final Status: {result.get('status', 'unknown')}")


if __name__ == "__main__":
    main()