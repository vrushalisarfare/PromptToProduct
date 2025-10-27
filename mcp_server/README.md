# PromptToProduct MCP Server

This is a Model Context Protocol (MCP) server specifically designed for the **PromptToProduct** repository (`vrushalisarfare/PromptToProduct`). It provides GitHub webhook integration and event processing for development workflow automation.

## Features

- **GET /health** => repository-aware health check with configuration status
- **GET /mcp** => MCP server info with repository details and endpoint information  
- **POST /github-webhook** => processes GitHub webhook events specifically for PromptToProduct repo

### Supported GitHub Events

- **Push events**: tracks commits, branches, and pusher information
- **Pull request events**: handles PR creation, updates, and state changes
- **Issues events**: processes issue creation, updates, and state changes  
- **Issue comment events**: handles comments on issues and pull requests

## Quick Start

### 1. Start the Server

```powershell
# Basic start (listens on 0.0.0.0:8080)
python -m mcp_server.main

# Custom host/port
python -m mcp_server.main --host 127.0.0.1 --port 8080

# Debug mode (verbose logging)
python -m mcp_server.main --debug
```

### 2. Test the Server

```powershell
# Health check
curl http://127.0.0.1:8080/health

# MCP info
curl http://127.0.0.1:8080/mcp

# Test webhook (simulated push event)
curl -X POST http://127.0.0.1:8080/github-webhook -H "Content-Type: application/json" -d '{\"action\":\"push\",\"repository\":{\"full_name\":\"vrushalisarfare/PromptToProduct\"},\"ref\":\"refs/heads/main\",\"commits\":[],\"pusher\":{\"name\":\"testuser\"}}'
```

## GitHub Webhook Setup

### 1. Configure the Webhook in GitHub

1. Go to your **PromptToProduct** repository: https://github.com/vrushalisarfare/PromptToProduct
2. Navigate to **Settings** → **Webhooks** → **Add webhook**
3. Configure:
   - **Payload URL**: `http://your-server-host:8080/github-webhook`
   - **Content type**: `application/json`
   - **Secret**: (recommended) generate a random string for security
   - **Events**: Select individual events or "Send me everything"

### 2. Configure Webhook Secret (Recommended)

For security, set a webhook secret:

```powershell
# Set environment variable for webhook secret
$env:GITHUB_WEBHOOK_SECRET="your-secret-here"

# Start server with secret configured
python -m mcp_server.main
```

### 3. For Production Deployment

```powershell
# Set all environment variables
$env:MCP_HOST="0.0.0.0"
$env:MCP_PORT="8080"  
$env:GITHUB_WEBHOOK_SECRET="your-webhook-secret"
$env:DEBUG="false"

# Start server
python -m mcp_server.main
```

## Configuration

The server can be configured via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_HOST` | `0.0.0.0` | Host to bind the server to |
| `MCP_PORT` | `8080` | Port to listen on |
| `GITHUB_WEBHOOK_SECRET` | _(none)_ | GitHub webhook secret for signature verification |
| `DEBUG` | `false` | Enable debug logging (`true`/`false`) |

## Repository Validation

The server **only** accepts webhooks from the PromptToProduct repository (`vrushalisarfare/PromptToProduct`). Webhooks from other repositories will be rejected with an error.

## Event Processing

When a webhook is received, the server:

1. **Validates** the repository matches PromptToProduct
2. **Verifies** the webhook signature (if secret is configured)
3. **Processes** the event based on type (push, PR, issues, comments)
4. **Logs** the event details (verbose in debug mode)
5. **Responds** with processing status

## Development Notes

- **Dependencies**: Uses only Python standard library (no external packages required)
- **Security**: Webhook signature verification supported via HMAC-SHA256
- **Logging**: Structured logging with debug mode for detailed output
- **Error handling**: Comprehensive error responses for invalid repos, signatures, etc.

## Production Considerations

For production use, consider:
- Using a proper ASGI server (FastAPI + uvicorn)  
- Adding authentication/authorization
- Setting up proper logging and monitoring
- Using HTTPS with valid SSL certificates
- Implementing rate limiting and request validation
