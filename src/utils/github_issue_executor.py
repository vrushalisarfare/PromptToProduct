#!/usr/bin/env python3
"""
GitHub Issue Executor

Direct MCP tool executor for creating GitHub issues from PromptToProduct specifications.
This utility provides a clean interface to execute GitHub MCP tools.
"""
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def execute_github_issue_creation(spec_results: List[Dict[str, Any]], 
                                 owner: str = "vrushalisarfare", 
                                 repo: str = "PromptToProduct") -> Dict[str, Any]:
    """
    Execute GitHub issue creation using MCP tools for spec results.
    
    Args:
        spec_results: List of specification results from SpecAgent
        owner: GitHub repository owner
        repo: GitHub repository name
        
    Returns:
        Execution results with issue creation status
    """
    print("🚀 Executing GitHub Issue Creation via MCP...")
    
    created_issues = []
    errors = []
    
    for spec_result in spec_results:
        try:
            # Extract specification details
            spec_type = spec_result.get("spec_type", "specification")
            title = spec_result.get("title", "Unknown Specification")
            created_files = spec_result.get("created_files", [])
            banking_context = spec_result.get("banking_context", {})
            gherkin_files = spec_result.get("gherkin_files", [])
            
            # Generate issue title
            issue_title = f"📝 {spec_type.title()}: {title}"
            
            # Generate issue body with embedded content
            issue_body = generate_issue_body(spec_result, spec_type, title, created_files, 
                                           banking_context, gherkin_files)
            
            # Generate labels
            labels = generate_issue_labels(spec_result, spec_type, banking_context)
            
            # Prepare MCP parameters
            issue_params = {
                "method": "create",
                "owner": owner,
                "repo": repo,
                "title": issue_title,
                "body": issue_body,
                "labels": labels
            }
            
            print(f"   🔧 Preparing issue: {issue_title}")
            print(f"   📋 Repository: {owner}/{repo}")
            print(f"   🏷️ Labels: {', '.join(labels)}")
            
            # Store for execution
            created_issues.append({
                "spec_type": spec_type,
                "title": title,
                "mcp_params": issue_params,
                "status": "ready_for_execution"
            })
            
        except Exception as e:
            print(f"   ❌ Error preparing issue for {spec_result.get('title', 'Unknown')}: {e}")
            errors.append(str(e))
    
    return {
        "success": len(created_issues) > 0,
        "items_prepared": len(created_issues),
        "items": created_issues,
        "errors": errors,
        "instructions": {
            "next_step": "Call execute_mcp_tools() to create actual GitHub issues",
            "tools_required": ["mcp_github_issue_write"],
            "environment": "VS Code MCP environment"
        }
    }


def generate_issue_body(spec_result: Dict[str, Any], spec_type: str, title: str, 
                       created_files: List[str], banking_context: Dict[str, Any], 
                       gherkin_files: List[str]) -> str:
    """Generate comprehensive issue body with embedded content."""
    
    body = f"""## {spec_type.title()} Created: {title}

**Type:** {spec_type.title()}
**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Agent:** PromptToProduct SpecAgent

### Overview
This {spec_type.lower()} was automatically generated from the prompt:
> {spec_result.get('prompt', spec_result.get('input_prompt', 'N/A'))}

### Banking Context"""
    
    if banking_context.get("is_banking"):
        if banking_context.get("products"):
            body += f"\n- **Products:** {', '.join(banking_context['products'])}"
        if banking_context.get("compliance"):
            body += f"\n- **Compliance:** {', '.join(banking_context['compliance'])}"
    else:
        body += "\n- No specific banking context detected"
    
    # Add embedded feature files for stories
    if spec_type.lower() == "story" and gherkin_files:
        body += "\n\n### 🧪 Acceptance Criteria (BDD Feature Files)\n"
        body += "The following Gherkin feature files define the acceptance criteria for this story:\n\n"
        
        # Add main feature file info
        main_feature_info = spec_result.get("main_feature_file")
        if main_feature_info and main_feature_info.get("content"):
            story_id = main_feature_info.get("story_id", "Story")
            relative_path = main_feature_info.get("relative_path", "")
            body += f"#### 🎯 Main Feature: {story_id}\n"
            body += f"**File:** `{relative_path}`\n\n"
            body += "```gherkin\n"
            body += main_feature_info["content"]
            body += "```\n\n"
        
        # Add additional banking feature files
        additional_files = spec_result.get("additional_feature_files", [])
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
- [ ] Review {spec_type.lower()} content and requirements
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

### Links"""
    
    # Add file links
    for file_path in created_files:
        file_path_obj = Path(file_path)
        try:
            relative_path = str(file_path_obj.relative_to(project_root))
        except ValueError:
            relative_path = file_path
        body += f"\n- [`{relative_path}`]({relative_path})"
    
    # Add feature file links for stories
    if spec_type.lower() == "story" and gherkin_files:
        body += "\n- **Feature Files:**"
        for gherkin_file in gherkin_files:
            gherkin_path_obj = Path(gherkin_file)
            try:
                gherkin_relative = str(gherkin_path_obj.relative_to(project_root))
            except ValueError:
                gherkin_relative = gherkin_file
            body += f"\n  - [`{gherkin_relative}`]({gherkin_relative})"
    
    body += "\n\n**Auto-generated by PromptToProduct Spec Agent**"
    
    return body


def generate_issue_labels(spec_result: Dict[str, Any], spec_type: str, 
                         banking_context: Dict[str, Any]) -> List[str]:
    """Generate appropriate labels for the GitHub issue."""
    
    labels = ["specification", "auto-generated", spec_type.lower()]
    
    # Add banking labels
    if banking_context.get("is_banking"):
        labels.append("banking")
        
        # Add product-specific labels
        products = banking_context.get("products", [])
        for product in products:
            if product in ["loans", "credit_cards", "payments", "investments", "accounts"]:
                labels.append(product)
        
        # Add compliance labels
        compliance = banking_context.get("compliance", [])
        if compliance:
            labels.append("compliance")
    
    # Add BDD label for stories with feature files
    if spec_type.lower() == "story" and spec_result.get("gherkin_files"):
        labels.extend(["bdd", "acceptance-criteria"])
    
    # Add priority and type labels
    labels.extend(["medium-priority", "enhancement"])
    
    return labels


def execute_mcp_tools(prepared_issues: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Execute the actual MCP tools to create GitHub issues.
    This function would be called in VS Code MCP environment.
    
    Args:
        prepared_issues: List of prepared issue data
        
    Returns:
        Execution results
    """
    print("🔧 Executing MCP GitHub Issue Tools...")
    
    results = []
    
    for issue_data in prepared_issues:
        try:
            params = issue_data["mcp_params"]
            
            print(f"   📝 Creating: {params['title']}")
            
            # This is where the actual MCP tool call would happen in VS Code:
            # result = mcp_github_issue_write(**params)
            
            # For demonstration, return prepared data
            results.append({
                "success": True,
                "title": params["title"],
                "repository": f"{params['owner']}/{params['repo']}",
                "labels": params["labels"],
                "status": "mcp_tool_ready"
            })
            
        except Exception as e:
            print(f"   ❌ Error with {issue_data.get('title', 'Unknown')}: {e}")
            results.append({
                "success": False,
                "title": issue_data.get("title", "Unknown"),
                "error": str(e)
            })
    
    successful = [r for r in results if r.get("success")]
    
    return {
        "success": len(successful) > 0,
        "total_processed": len(prepared_issues),
        "successful": len(successful),
        "failed": len(results) - len(successful),
        "results": results,
        "summary": f"Prepared {len(successful)} GitHub issues for MCP execution"
    }


def main():
    """CLI interface for GitHub issue execution."""
    print("🔧 GitHub Issue Executor")
    print("This utility prepares GitHub issues from PromptToProduct specifications")
    print("Use this in conjunction with VS Code MCP tools for actual issue creation")


if __name__ == "__main__":
    main()