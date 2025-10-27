"""
MCP Integration for PromptToProduct Schema
Provides MCP server integration for the schema processor.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from schema_processor import PromptToProductSchema
import json


class MCPSchemaIntegration:
    """Integration class for MCP server to use PromptToProduct schema."""
    
    def __init__(self):
        """Initialize with schema processor."""
        self.processor = PromptToProductSchema()
    
    def process_prompt_for_mcp(self, prompt: str) -> dict:
        """Process a prompt and return MCP-compatible result."""
        result = self.processor.process_prompt(prompt)
        
        # Convert to MCP format
        mcp_result = {
            "success": result["success"],
            "action": result["action"],
            "prompt": result["prompt"]
        }
        
        if result["success"]:
            if result.get("file_created"):
                mcp_result["file_created"] = result["file_created"]
                mcp_result["message"] = f"✅ Created: {os.path.basename(result['file_created'])}"
                
                # Read file content for preview
                try:
                    with open(result["file_created"], 'r') as f:
                        content = f.read()
                        mcp_result["content_preview"] = content[:500] + "..." if len(content) > 500 else content
                except:
                    pass
                    
            elif result.get("validation"):
                validation = result["validation"]
                mcp_result["validation_summary"] = {
                    "epics": len(validation["epics"]),
                    "features": len(validation["features"]),
                    "stories": len(validation["stories"]),
                    "issues": len(validation["orphaned_features"]) + len(validation["orphaned_stories"])
                }
                mcp_result["message"] = "✅ Validation completed"
        else:
            mcp_result["error"] = result["error"]
            mcp_result["message"] = f"❌ Error: {result['error']}"
        
        return mcp_result
    
    def get_schema_status(self) -> dict:
        """Get current schema status for MCP."""
        validation = self.processor.validate_spec_links()
        
        return {
            "schema_name": self.processor.schema["name"],
            "schema_version": self.processor.schema["version"],
            "working_directory": str(self.processor.specs_dir.absolute()),
            "specs_count": {
                "epics": len(validation["epics"]),
                "features": len(validation["features"]),
                "stories": len(validation["stories"])
            },
            "health": {
                "orphaned_features": len(validation["orphaned_features"]),
                "orphaned_stories": len(validation["orphaned_stories"]),
                "status": "healthy" if not validation["orphaned_features"] and not validation["orphaned_stories"] else "issues"
            },
            "available_actions": list(self.processor.schema["actions"].keys())
        }
    
    def get_next_ids(self) -> dict:
        """Get next available IDs for each spec type."""
        return {
            "epic": self.processor.get_next_id("epic"),
            "feature": self.processor.get_next_id("feature"),
            "story": self.processor.get_next_id("story")
        }


# Example usage for MCP server
def mcp_schema_handler(prompt: str) -> str:
    """Handler function that can be used by MCP server."""
    integration = MCPSchemaIntegration()
    result = integration.process_prompt_for_mcp(prompt)
    return json.dumps(result, indent=2)


def mcp_status_handler() -> str:
    """Status handler for MCP server."""
    integration = MCPSchemaIntegration()
    status = integration.get_schema_status()
    return json.dumps(status, indent=2)


if __name__ == "__main__":
    # Test the integration
    integration = MCPSchemaIntegration()
    
    print("🔧 MCP Schema Integration Test")
    print("=" * 40)
    
    # Test status
    status = integration.get_schema_status()
    print(f"Schema: {status['schema_name']} v{status['schema_version']}")
    print(f"Working Directory: {status['working_directory']}")
    print(f"Specs: {status['specs_count']['epics']} epics, {status['specs_count']['features']} features, {status['specs_count']['stories']} stories")
    print(f"Health: {status['health']['status']}")
    
    # Test next IDs
    next_ids = integration.get_next_ids()
    print(f"Next IDs: {next_ids}")
    
    # Test prompt processing
    test_prompt = "Create an epic for mobile application development"
    print(f"\n🧪 Testing prompt: {test_prompt}")
    result = integration.process_prompt_for_mcp(test_prompt)
    print(f"Result: {result['message']}")
    if result.get('file_created'):
        print(f"File: {result['file_created']}")