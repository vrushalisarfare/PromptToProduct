# Copilot Agents Manifest System

> **GitHub Copilot Agents configuration and manifest management for the PromptToProduct 4-agent system**

## 📋 Overview

The **Copilot Agents Manifest System** manages the YAML-to-JSON workflow configuration for GitHub Copilot integration. This system defines the 4-agent orchestration (Orchestrator, SpecAgent, CodeAgent, ValidationAgent) and provides automated manifest generation for VS Code GitHub MCP integration.

## 🎯 Manifest-Specific Features

- **� YAML Source Management**: `copilot_agents.yaml` as the single source of truth
- **🔄 Automated JSON Export**: Generates `copilot_agents_manifest.json` for GitHub Copilot
- **✅ Manifest Validation**: Ensures proper agent configuration and routing rules
- **� GitHub MCP Integration**: Seamless VS Code Copilot agent registration

## 📁 Manifest Files

```
.github/workflows/
├── copilot_agents.yaml          # Source manifest (YAML)
├── manifest_loader.py           # Conversion and validation tool
└── copilot_agents_manifest.json # Generated manifest (JSON)
```
## 🚀 Manifest Usage

### Generate JSON Manifest
```powershell
# Standard generation with validation
python .github\workflows\manifest_loader.py

# Debug mode with detailed output
python .github\workflows\manifest_loader.py --debug
```

### Expected Output
```
🔍 Loading manifest from: copilot_agents.yaml
✅ Manifest validation successful
📋 Agent Summary: 4 agents detected
🔄 Routing Rules: 3 workflow patterns defined
💾 Exported to: copilot_agents_manifest.json
```

## 📊 Manifest Structure

### YAML Source (`copilot_agents.yaml`)
```yaml
version: "1.0"
project: "Prompt to Product"
description: >
  Copilot Agent Orchestration Manifest for turning natural-language prompts
  into epics, features, stories, and Python code for MyBank.

agents:
  - id: orchestrator
    name: Prompt Orchestrator
    description: Central hub for prompt classification and routing
    entrypoint: src/agents/orchestrator.py
    capabilities: [classify_prompt, route_to_agent, memory_context]
    
  - id: spec-agent
    name: Spec Agent
    description: Converts developer prompts into structured markdown specs
    entrypoint: src/agents/spec_agent.py
    actions: [create_epic, create_feature, create_story]
    
  - id: code-agent
    name: Code Agent
    description: Reads story specs and generates Python code
    entrypoint: src/agents/code_agent.py
    actions: [generate_code_snippet, commit_changes]
    
  - id: validation-agent
    name: Validation Agent
    description: Validates specifications and syncs with GitHub
    entrypoint: src/agents/validation_agent.py
    actions: [validate_links, sync_with_github]
```
### JSON Output (`copilot_agents_manifest.json`)
```json
{
  "version": "1.0",
  "project": "Prompt to Product", 
  "description": "Copilot Agent Orchestration Manifest...",
  "agents": [
    {
      "id": "orchestrator",
      "name": "Prompt Orchestrator",
      "capabilities": ["classify_prompt", "route_to_agent", "memory_context"]
    },
    {
      "id": "spec-agent", 
      "name": "Spec Agent",
      "actions": ["create_epic", "create_feature", "create_story"]
    },
    {
      "id": "code-agent",
      "name": "Code Agent", 
      "actions": ["generate_code_snippet", "commit_changes"]
    },
    {
      "id": "validation-agent",
      "name": "Validation Agent",
      "actions": ["validate_links", "sync_with_github"]
    }
  ]
}
```

## 🔧 GitHub MCP Integration

### VS Code Configuration
The generated `copilot_agents_manifest.json` integrates with GitHub's MCP server for VS Code Copilot:

```json
{
  "mcpServers": {
    "github": {
      "command": "mcp-server-github",
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

### Environment Setup
```powershell
# Required for GitHub MCP integration
$env:GITHUB_PERSONAL_ACCESS_TOKEN = "your_github_token"
```

## ✅ Validation & Quality Assurance

### Automatic Validation
The manifest loader performs:
- **Structure Validation**: Required fields, agent configurations
- **Agent Discovery**: Verification of 4 expected agents
- **Routing Rules**: Validation of workflow patterns
- **File Export**: JSON generation with proper formatting

### Manual Validation
```powershell
# Validate manifest structure
python .github\workflows\manifest_loader.py --debug

# Check generated JSON
Get-Content .github\workflows\copilot_agents_manifest.json | ConvertFrom-Json
```

## 🚦 Status Monitoring

### Health Checks
```powershell
# Manifest system status
python .github\workflows\manifest_loader.py

# Verify JSON output exists
Test-Path .github\workflows\copilot_agents_manifest.json
```

### Metrics Tracked
- **Agent Count**: 4 active agents detected
- **Manifest Version**: Current version validation
- **Export Status**: JSON file generation success
- **File Integrity**: YAML source vs JSON output consistency

## � Troubleshooting

### Common Issues

**Manifest Generation Fails**
```powershell
# Check YAML syntax and structure
python .github\workflows\manifest_loader.py --debug
```

**JSON Export Issues**
```powershell
# Verify YAML source file exists
Test-Path .github\workflows\copilot_agents.yaml

# Check output directory permissions
Test-Path .github\workflows\
```

**GitHub MCP Integration Issues**
```powershell
# Verify environment variable
echo $env:GITHUB_PERSONAL_ACCESS_TOKEN

# Check VS Code MCP configuration
Get-Content "$env:APPDATA\Code\User\globalStorage\rooveterinaryinc.roo-cline\settings\cline_mcp_settings.json"
```

### Debug Mode
Use `--debug` flag for detailed troubleshooting information:
```powershell
python .github\workflows\manifest_loader.py --debug
```

## 📚 Related Documentation

- **Main System Documentation**: [README.md](README.md)
- **GitHub MCP Setup**: [GitHub-MCP-Setup-Guide.md](GitHub-MCP-Setup-Guide.md)
- **Banking Schema Reference**: [specs/prompt_schema.json](specs/prompt_schema.json)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Version**: 1.0  
**Last Updated**: October 27, 2025  
**Maintained by**: PromptToProduct Team

> 🚀 **Streamlined manifest management for GitHub Copilot Agents integration!**