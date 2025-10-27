#!/usr/bin/env python3
"""
Project Agent - GitHub Projects and Issue Management

This agent handles GitHub Projects integration, issue creation, and project
management workflows for the PromptToProduct system.
"""
import os
import sys
import json
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional
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

class ProjectAgent:
    """
    Project Agent for GitHub Projects and issue management.
    
    Responsibilities:
    - Create GitHub issues for specs (epics, features, stories)
    - Add items to GitHub Projects boards
    - Update project status and assignments
    - Manage project workflows and automation
    """
    
    def __init__(self):
        """Initialize the project agent."""
        self.agent_id = "project-agent"
        self.version = "1.0"
        
        # Ensure environment variables are loaded
        try:
            from dotenv import load_dotenv
            env_path = project_root / ".env"
            if env_path.exists():
                load_dotenv(env_path, override=True)  # Force reload
        except ImportError:
            pass
        
        # Use configuration system if available
        if CONFIG_AVAILABLE:
            self.github_config = {
                "repo_owner": github_config.repo_owner,
                "repo_name": github_config.repo_name,
                "base_url": github_config.base_url,
                "token": github_config.token,
            }
            # Load project configuration from environment variables
            self.project_config = {
                "enabled": os.getenv("GITHUB_PROJECT_ENABLED", "false").lower() == "true",
                "project_number": os.getenv("GITHUB_PROJECT_NUMBER", "1"),
                "org_name": os.getenv("GITHUB_ORG_NAME", github_config.repo_owner)
            }
        else:
            # Fallback configuration
            self.github_config = {
                "repo_owner": "vrushalisarfare",
                "repo_name": "PromptToProduct",
                "base_url": "https://api.github.com",
                "token": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"),
            }
            self.project_config = {
                "enabled": os.getenv("GITHUB_PROJECT_ENABLED", "false").lower() == "true",
                "project_number": os.getenv("GITHUB_PROJECT_NUMBER", "1"),
                "org_name": os.getenv("GITHUB_ORG_NAME", "vrushalisarfare")
            }
    
    def create_spec_project_items(self, spec_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create GitHub issues and add to Projects board for specs.
        
        Args:
            spec_results: List of spec creation results from SpecAgent
            
        Returns:
            Integration result with created issues and project items
        """
        print("🔗 Creating GitHub Project Items...")
        
        # Show what we received
        print(f"   📊 Received {len(spec_results)} spec results")
        for i, spec in enumerate(spec_results):
            print(f"   📄 Spec {i+1}: {spec.get('spec_type', 'unknown')} - {spec.get('title', 'unknown')}")
        
        if not self.project_config["enabled"]:
            return {
                "success": False,
                "reason": "GitHub Projects integration disabled",
                "items_created": 0
            }
        
        if not self.github_config.get("token"):
            return {
                "success": False, 
                "reason": "GitHub token not configured",
                "items_created": 0
            }
        
        project_items = []
        errors = []
        
        for spec_result in spec_results:
            try:
                # Create GitHub issue for the spec
                issue_result = self._create_spec_issue(spec_result)
                
                if issue_result.get("success"):
                    # Add issue to project board
                    project_result = self._add_issue_to_project(
                        issue_result["issue_number"],
                        spec_result
                    )
                    
                    if project_result.get("success"):
                        project_items.append({
                            "spec_file": spec_result.get("file_path", "Unknown"),
                            "spec_type": spec_result.get("spec_type", "unknown"),
                            "issue_number": issue_result["issue_number"],
                            "issue_url": issue_result["issue_url"],
                            "project_item_id": project_result.get("item_id")
                        })
                        print(f"   ✅ {spec_result.get('spec_type', 'Spec').title()}: {spec_result.get('title', 'Unknown')} → Issue #{issue_result['issue_number']}")
                    else:
                        errors.append(f"Failed to add to project: {project_result.get('error')}")
                else:
                    errors.append(f"Failed to create issue: {issue_result.get('error')}")
                    
            except Exception as e:
                errors.append(f"Error processing {spec_result.get('file_path', 'unknown')}: {str(e)}")
        
        return {
            "success": len(project_items) > 0,
            "items_created": len(project_items),
            "project_items": project_items,
            "project_number": self.project_config["project_number"],
            "organization": self.project_config["org_name"],
            "errors": errors
        }
    
    def _create_spec_issue(self, spec_result: Dict[str, Any]) -> Dict[str, Any]:
        """Create a GitHub issue for a spec (epic/feature/story)."""
        try:
            spec_type = spec_result.get("spec_type", "spec").title()
            title = spec_result.get("title", "Unknown Spec")
            file_path = spec_result.get("file_path", "")
            file_name = Path(file_path).name if file_path else "unknown.md"
            
            # Extract spec ID from filename
            spec_id = file_name.split("-")[0] if "-" in file_name else "Unknown"
            
            issue_title = f"{spec_type}: {title}"
            issue_body = f"""# {spec_type}: {title}

**Spec ID:** {spec_id}  
**File:** `{file_name}`  
**Status:** {spec_result.get('status', 'In Progress')}  
**Owner:** {spec_result.get('owner', 'TBD')}  
**Assigned To:** {spec_result.get('assigned_to', 'TBD')}  
**Priority:** {spec_result.get('priority', 'Medium')}  

## Description
{spec_result.get('objective', f'Implementation of {title}')}

## Implementation Tasks
- [ ] Review and enhance specification
- [ ] Implement core functionality  
- [ ] Add tests and validation
- [ ] Deploy and verify

## Banking Context
- **Product Type:** {spec_result.get('banking_domain', 'TBD')}
- **Compliance:** {', '.join(spec_result.get('compliance_requirements', []))}

## Files
- Specification: `specs/{spec_type.lower()}s/{file_name}`

---
*Auto-generated by PromptToProduct ProjectAgent*
"""
            
            headers = {
                "Authorization": f"token {self.github_config['token']}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json"
            }
            
            issue_data = {
                "title": issue_title,
                "body": issue_body,
                "labels": [spec_type.lower(), "prompttoproduct", "banking"],
                "assignees": [spec_result.get('assigned_to', self.github_config['repo_owner'])]
            }
            
            url = f"{self.github_config['base_url']}/repos/{self.github_config['repo_owner']}/{self.github_config['repo_name']}/issues"
            response = requests.post(url, headers=headers, json=issue_data)
            
            if response.status_code == 201:
                issue = response.json()
                return {
                    "success": True,
                    "issue_number": issue["number"],
                    "issue_url": issue["html_url"]
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _add_issue_to_project(self, issue_number: int, spec_result: Dict[str, Any]) -> Dict[str, Any]:
        """Add an issue to GitHub Projects v2 board."""
        try:
            headers = {
                "Authorization": f"token {self.github_config['token']}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28"
            }
            
            # Get project ID using GraphQL - try user first, then organization
            project_number = self.project_config["project_number"]
            org_name = self.project_config["org_name"]
            
            # First try as user project
            graphql_query = f"""
            query {{
                user(login: "{org_name}") {{
                    projectV2(number: {project_number}) {{
                        id
                    }}
                }}
            }}
            """
            
            graphql_url = "https://api.github.com/graphql"
            graphql_response = requests.post(
                graphql_url,
                headers=headers,
                json={"query": graphql_query}
            )
            
            project_id = None
            if graphql_response.status_code == 200:
                project_data = graphql_response.json()
                if "errors" not in project_data and project_data.get("data", {}).get("user", {}).get("projectV2"):
                    project_id = project_data["data"]["user"]["projectV2"]["id"]
            
            # If user project not found, try organization
            if not project_id:
                graphql_query = f"""
                query {{
                    organization(login: "{org_name}") {{
                        projectV2(number: {project_number}) {{
                            id
                        }}
                    }}
                }}
                """
                
                graphql_response = requests.post(
                    graphql_url,
                    headers=headers,
                    json={"query": graphql_query}
                )
                
                if graphql_response.status_code == 200:
                    project_data = graphql_response.json()
                    if "errors" not in project_data and project_data.get("data", {}).get("organization", {}).get("projectV2"):
                        project_id = project_data["data"]["organization"]["projectV2"]["id"]
            
            if not project_id:
                return {
                    "success": False,
                    "error": f"Could not find project #{project_number} for user or organization '{org_name}'. Make sure the project exists and you have access."
                }
            
            # Get issue node ID
            issue_url = f"{self.github_config['base_url']}/repos/{self.github_config['repo_owner']}/{self.github_config['repo_name']}/issues/{issue_number}"
            issue_response = requests.get(issue_url, headers=headers)
            
            if issue_response.status_code != 200:
                return {
                    "success": False,
                    "error": f"Failed to get issue: {issue_response.status_code}"
                }
            
            issue_node_id = issue_response.json()["node_id"]
            
            # Add item to project
            add_item_mutation = f"""
            mutation {{
                addProjectV2ItemById(input: {{
                    projectId: "{project_id}"
                    contentId: "{issue_node_id}"
                }}) {{
                    item {{
                        id
                    }}
                }}
            }}
            """
            
            mutation_response = requests.post(
                graphql_url,
                headers=headers,
                json={"query": add_item_mutation}
            )
            
            if mutation_response.status_code == 200:
                mutation_data = mutation_response.json()
                if "errors" not in mutation_data:
                    return {
                        "success": True,
                        "item_id": mutation_data["data"]["addProjectV2ItemById"]["item"]["id"]
                    }
            
            return {
                "success": False,
                "error": f"Failed to add to project: {mutation_response.status_code}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_project_agent_status(self) -> Dict[str, Any]:
        """Get current project agent status."""
        return {
            "agent_id": self.agent_id,
            "version": self.version,
            "status": "active",
            "github_configured": bool(self.github_config.get("token")),
            "projects_enabled": self.project_config["enabled"],
            "project_number": self.project_config["project_number"],
            "organization": self.project_config["org_name"]
        }