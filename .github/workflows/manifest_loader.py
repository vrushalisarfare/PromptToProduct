#!/usr/bin/env python3
"""
Manifest Loader for PromptToProduct
Imports and processes the Copilot Agents workflow manifest.
"""
import yaml
import json
from pathlib import Path
from typing import Dict, List, Any, Optional


class CopilotAgentsManifest:
    """Loader and processor for the Copilot Agents workflow manifest."""
    
    def __init__(self, manifest_path: str = ".github/workflows/copilot_agents.yaml"):
        """Initialize with manifest file path."""
        self.manifest_path = Path(manifest_path)
        self.manifest = self._load_manifest()
        
    def _load_manifest(self) -> Dict[str, Any]:
        """Load the YAML manifest file."""
        try:
            with open(self.manifest_path, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)
                if content is None:
                    raise ValueError("YAML file is empty or invalid")
                return content
        except FileNotFoundError:
            raise FileNotFoundError(f"Manifest file not found: {self.manifest_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in manifest file: {e}")
        except Exception as e:
            raise ValueError(f"Error loading manifest: {e}")
    
    def get_project_info(self) -> Dict[str, str]:
        """Get basic project information from manifest."""
        if not self.manifest:
            return {"version": "unknown", "project": "unknown", "description": ""}
        
        return {
            "version": self.manifest.get("version", "unknown"),
            "project": self.manifest.get("project", "unknown"),
            "description": self.manifest.get("description", "").strip() if self.manifest.get("description") else ""
        }
    
    def get_agents(self) -> List[Dict[str, Any]]:
        """Get all agents defined in the manifest."""
        return self.manifest.get("agents", [])
    
    def get_agent_by_id(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific agent by ID."""
        for agent in self.get_agents():
            if agent.get("id") == agent_id:
                return agent
        return None
    
    def get_agent_capabilities(self, agent_id: str) -> List[str]:
        """Get capabilities for a specific agent."""
        agent = self.get_agent_by_id(agent_id)
        if agent:
            return agent.get("capabilities", [])
        return []
    
    def get_agent_routes(self, agent_id: str) -> List[Dict[str, Any]]:
        """Get routing rules for a specific agent."""
        agent = self.get_agent_by_id(agent_id)
        if agent:
            return agent.get("routes", [])
        return []
    
    def get_orchestrator_config(self) -> Dict[str, Any]:
        """Get orchestrator agent configuration."""
        orchestrator = self.get_agent_by_id("orchestrator")
        if orchestrator:
            return {
                "name": orchestrator.get("name"),
                "description": orchestrator.get("description"),
                "entrypoint": orchestrator.get("entrypoint"),
                "capabilities": orchestrator.get("capabilities", []),
                "routes": orchestrator.get("routes", []),
                "memory": orchestrator.get("memory", {})
            }
        return {}
    
    def get_spec_agent_config(self) -> Dict[str, Any]:
        """Get spec agent configuration."""
        spec_agent = self.get_agent_by_id("spec-agent")
        if spec_agent:
            return {
                "name": spec_agent.get("name"),
                "description": spec_agent.get("description"),
                "entrypoint": spec_agent.get("entrypoint"),
                "inputs": spec_agent.get("inputs", []),
                "outputs": spec_agent.get("outputs", []),
                "actions": spec_agent.get("actions", []),
                "on_complete": spec_agent.get("on_complete", [])
            }
        return {}
    
    def get_code_agent_config(self) -> Dict[str, Any]:
        """Get code agent configuration."""
        code_agent = self.get_agent_by_id("code-agent")
        if code_agent:
            return {
                "name": code_agent.get("name"),
                "description": code_agent.get("description"),
                "entrypoint": code_agent.get("entrypoint"),
                "inputs": code_agent.get("inputs", []),
                "outputs": code_agent.get("outputs", []),
                "actions": code_agent.get("actions", []),
                "on_complete": code_agent.get("on_complete", [])
            }
        return {}
    
    def get_validation_agent_config(self) -> Dict[str, Any]:
        """Get validation agent configuration."""
        validation_agent = self.get_agent_by_id("validation-agent")
        if validation_agent:
            return {
                "name": validation_agent.get("name"),
                "description": validation_agent.get("description"),
                "entrypoint": validation_agent.get("entrypoint"),
                "actions": validation_agent.get("actions", []),
                "reports": validation_agent.get("reports", [])
            }
        return {}
    
    def validate_manifest(self) -> Dict[str, Any]:
        """Validate the manifest structure and return validation results."""
        validation = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "agent_count": len(self.get_agents()),
            "agents_found": [agent.get("id") for agent in self.get_agents()],
            "missing_required_fields": []
        }
        
        # Check required fields
        required_fields = ["version", "project", "agents"]
        for field in required_fields:
            if field not in self.manifest:
                validation["errors"].append(f"Missing required field: {field}")
                validation["valid"] = False
        
        # Check agent structure
        for agent in self.get_agents():
            agent_id = agent.get("id", "unknown")
            if not agent.get("name"):
                validation["warnings"].append(f"Agent {agent_id} missing name")
            if not agent.get("description"):
                validation["warnings"].append(f"Agent {agent_id} missing description")
            if not agent.get("entrypoint"):
                validation["errors"].append(f"Agent {agent_id} missing entrypoint")
                validation["valid"] = False
        
        return validation
    
    def export_to_json(self, output_path: str = "copilot_agents_manifest.json") -> str:
        """Export manifest to JSON format."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.manifest, f, indent=2, ensure_ascii=False)
        return output_path
    
    def get_agent_workflow(self) -> Dict[str, Any]:
        """Get the complete agent workflow and routing logic."""
        orchestrator = self.get_orchestrator_config()
        workflow = {
            "entry_point": "orchestrator",
            "routing_rules": orchestrator.get("routes", []),
            "agent_chain": {},
            "memory_config": orchestrator.get("memory", {})
        }
        
        # Build agent chain from routing rules
        for route in orchestrator.get("routes", []):
            triggers = route.get("trigger", [])
            next_agent = route.get("next")
            for trigger in triggers:
                workflow["agent_chain"][trigger] = next_agent
        
        return workflow
    
    def print_summary(self) -> None:
        """Print a summary of the manifest."""
        project_info = self.get_project_info()
        agents = self.get_agents()
        
        print(f"📋 Copilot Agents Manifest Summary")
        print(f"=" * 50)
        print(f"Project: {project_info['project']}")
        print(f"Version: {project_info['version']}")
        print(f"Description: {project_info['description']}")
        print(f"\n🤖 Agents ({len(agents)}):")
        
        for agent in agents:
            print(f"  • {agent.get('id')} - {agent.get('name')}")
            print(f"    Description: {agent.get('description', 'N/A')}")
            print(f"    Entrypoint: {agent.get('entrypoint', 'N/A')}")
            if agent.get('capabilities'):
                print(f"    Capabilities: {', '.join(agent.get('capabilities', []))}")
            print()


def main():
    """Main function for CLI usage."""
    import sys
    
    # Check for debug flag
    debug = "--debug" in sys.argv
    
    if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        manifest_path = sys.argv[1]
    else:
        manifest_path = ".github/workflows/copilot_agents.yaml"
    
    try:
        # Load and process manifest
        if debug:
            print(f"🔍 Loading manifest from: {manifest_path}")
        
        manifest = CopilotAgentsManifest(manifest_path)
        
        if debug:
            print(f"🔍 Loaded manifest keys: {list(manifest.manifest.keys())}")
            print(f"🔍 Raw manifest: {manifest.manifest}")
        
        # Print summary
        manifest.print_summary()
        
        # Validate manifest
        validation = manifest.validate_manifest()
        print(f"✅ Validation Results:")
        print(f"Valid: {validation['valid']}")
        if validation['errors']:
            print(f"Errors: {validation['errors']}")
        if validation['warnings']:
            print(f"Warnings: {validation['warnings']}")
        
        # Export to JSON
        json_file = manifest.export_to_json()
        print(f"\n💾 Exported to: {json_file}")
        
        # Show workflow
        workflow = manifest.get_agent_workflow()
        print(f"\n🔄 Agent Workflow:")
        print(f"Entry Point: {workflow['entry_point']}")
        print(f"Routing Rules: {len(workflow['routing_rules'])} defined")
        
    except Exception as e:
        print(f"❌ Error loading manifest: {e}")
        if debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()