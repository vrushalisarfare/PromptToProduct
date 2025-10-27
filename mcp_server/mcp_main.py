#!/usr/bin/env python3
"""
MCP (Model Context Protocol) server for PromptToProduct GitHub integration.
This module implements the MCP protocol for VS Code integration.
"""
import asyncio
import json
import sys
import os
from typing import Any, Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from mcp import ServerSession, StdioServerParameters
    from mcp.server import Server
    from mcp.types import (
        Resource, Tool, TextContent, 
        CallToolRequest, ReadResourceRequest,
        ListResourcesRequest, ListToolsRequest
    )
except ImportError as e:
    logger.error(f"MCP imports failed: {e}")
    print("Error: MCP package not properly installed. Please run:")
    print("pip install mcp")
    sys.exit(1)

from .config import get_config, REPO_CONFIG


async def main():
    """Main entry point for the MCP server."""
    config = get_config()
    repo_info = config['repo']
    
    logger.info(f"Starting PromptToProduct MCP server for {repo_info['full_name']}")
    
    # Define server capabilities
    server_info = {
        "name": "prompt-to-product-mcp",
        "version": "1.0.0"
    }
    
    # Define resources
    resources = [
        Resource(
            uri=f"github://{repo_info['full_name']}/info",
            name=f"Repository: {repo_info['full_name']}",
            description="PromptToProduct repository information and status",
            mimeType="application/json"
        ),
        Resource(
            uri=f"github://{repo_info['full_name']}/webhook-setup",
            name="Webhook Setup Guide",
            description="Instructions for setting up GitHub webhooks",
            mimeType="text/markdown"
        )
    ]
    
    # Define tools
    tools = [
        Tool(
            name="start_webhook_server",
            description="Start the GitHub webhook server for PromptToProduct",
            inputSchema={
                "type": "object",
                "properties": {
                    "port": {"type": "integer", "default": 8080},
                    "debug": {"type": "boolean", "default": False}
                }
            }
        ),
        Tool(
            name="get_repo_status",
            description="Get current repository and webhook server status",
            inputSchema={"type": "object", "properties": {}}
        )
    ]
    
    async def handle_list_resources(request: ListResourcesRequest) -> List[Resource]:
        return resources
    
    async def handle_read_resource(request: ReadResourceRequest) -> str:
        uri = request.uri
        
        if uri == f"github://{repo_info['full_name']}/info":
            info = {
                "repository": repo_info,
                "webhook_server": {
                    "host": config.get('host', '127.0.0.1'),
                    "port": config.get('port', 8080),
                    "endpoint": "/github-webhook"
                },
                "configuration": {
                    "secret_configured": bool(config.get('github_webhook_secret')),
                    "debug_mode": config.get('debug', False)
                }
            }
            return json.dumps(info, indent=2)
            
        elif uri == f"github://{repo_info['full_name']}/webhook-setup":
            setup_guide = f"""# GitHub Webhook Setup for {repo_info['full_name']}

## Quick Setup

1. **Start the webhook server:**
   ```
   python -m mcp_server.main --port 8080
   ```

2. **Configure GitHub webhook:**
   - Go to: https://github.com/{repo_info['full_name']}/settings/hooks
   - Click "Add webhook"
   - Payload URL: `http://your-server:8080/github-webhook`
   - Content type: `application/json`
   - Secret: (optional but recommended)
   - Events: Select events you want to track

3. **Test the webhook:**
   ```
   curl http://127.0.0.1:8080/health
   ```

## Supported Events
- Push events
- Pull request events  
- Issues events
- Issue comment events

## Environment Variables
- `GITHUB_WEBHOOK_SECRET`: Webhook secret for security
- `MCP_HOST`: Server host (default: 0.0.0.0)
- `MCP_PORT`: Server port (default: 8080)
- `DEBUG`: Enable debug logging (true/false)
"""
            return setup_guide
        
        else:
            raise ValueError(f"Unknown resource: {uri}")
    
    async def handle_list_tools(request: ListToolsRequest) -> List[Tool]:
        return tools
    
    async def handle_call_tool(request: CallToolRequest) -> List[TextContent]:
        name = request.params.name
        args = request.params.arguments or {}
        
        if name == "start_webhook_server":
            port = args.get("port", 8080)
            debug = args.get("debug", False)
            
            try:
                # Start the webhook server in the background
                import subprocess
                import threading
                
                cmd = [
                    sys.executable, "-m", "mcp_server.main",
                    "--host", "127.0.0.1",
                    "--port", str(port)
                ]
                
                if debug:
                    cmd.append("--debug")
                
                # Start server in background
                def start_server():
                    subprocess.run(cmd, cwd=os.getcwd())
                
                thread = threading.Thread(target=start_server, daemon=True)
                thread.start()
                
                return [TextContent(
                    type="text",
                    text=f"✅ GitHub webhook server starting...\n\n"
                         f"Server: http://127.0.0.1:{port}\n"
                         f"Repository: {repo_info['full_name']}\n"
                         f"Webhook URL: http://127.0.0.1:{port}/github-webhook\n"
                         f"Debug mode: {debug}\n\n"
                         f"Configure webhook at:\n"
                         f"https://github.com/{repo_info['full_name']}/settings/hooks"
                )]
                
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=f"❌ Error starting server: {str(e)}"
                )]
        
        elif name == "get_repo_status":
            try:
                # Try to check if webhook server is running
                import requests
                health_url = f"http://127.0.0.1:{config.get('port', 8080)}/health"
                
                try:
                    response = requests.get(health_url, timeout=3)
                    server_status = "✅ Running" if response.status_code == 200 else "⚠️ Issues"
                    health_data = response.json() if response.status_code == 200 else {}
                except:
                    server_status = "❌ Not running"
                    health_data = {}
                
                status_text = f"""## PromptToProduct Repository Status

**Repository:** {repo_info['full_name']}
**Clone URL:** {repo_info['clone_url']}

**Webhook Server:** {server_status}
**Health Data:** {json.dumps(health_data, indent=2) if health_data else 'N/A'}

**Configuration:**
- Host: {config.get('host', '127.0.0.1')}
- Port: {config.get('port', 8080)}
- Secret configured: {bool(config.get('github_webhook_secret'))}
- Debug mode: {config.get('debug', False)}

**Next Steps:**
1. Start webhook server: Use 'start_webhook_server' tool
2. Configure GitHub webhook: See webhook-setup resource
3. Test integration: Push to repository or create issues/PRs
"""
                
                return [TextContent(type="text", text=status_text)]
                
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=f"❌ Error checking status: {str(e)}"
                )]
        
        else:
            return [TextContent(
                type="text",
                text=f"❌ Unknown tool: {name}"
            )]
    
    # Create and run the server
    server_params = StdioServerParameters(
        name=server_info["name"],
        version=server_info["version"]
    )
    
    try:
        async with ServerSession(
            server_params,
            handle_list_resources=handle_list_resources,
            handle_read_resource=handle_read_resource,
            handle_list_tools=handle_list_tools,
            handle_call_tool=handle_call_tool
        ) as session:
            await session.run()
            
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())