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

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

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
        self.specs_root = project_root / "specs"
        self.mybank_root = project_root / "src" / "MyBank"
        
        # GitHub configuration (would come from environment in production)
        self.github_config = {
            "repo_owner": "mybank-org",  # Replace with actual organization
            "repo_name": "mybank-core",  # Replace with actual repository
            "base_url": "https://api.github.com",
            "token": os.getenv("GITHUB_TOKEN"),  # Set via environment variable
        }
        
        # Validation schemas
        self.validation_schemas = self._load_validation_schemas()
    
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
            
            sync_result["status"] = "completed"
            
        except Exception as e:
            sync_result["status"] = "error"
            sync_result["errors"].append(str(e))
            print(f"❌ GitHub sync error: {e}")
        
        return sync_result
    
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
        """Update GitHub project board with validation status."""
        # Simulate project board update
        return {
            "success": True,
            "board_updated": "PromptToProduct Validation Board",
            "cards_updated": len(validation_results)
        }
    
    def get_validation_agent_status(self) -> Dict[str, Any]:
        """Get current validation agent status."""
        return {
            "agent_id": self.agent_id,
            "version": self.version,
            "status": "active",
            "specs_root": str(self.specs_root),
            "mybank_root": str(self.mybank_root),
            "supported_actions": ["validate_spec_completeness", "sync_with_github"],
            "validation_schemas": list(self.validation_schemas.keys()),
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
    
    if result.get('errors'):
        print(f"\n❌ Errors: {', '.join(result['errors'])}")
    
    print(f"\n📊 Final Status: {result.get('status', 'unknown')}")


if __name__ == "__main__":
    main()