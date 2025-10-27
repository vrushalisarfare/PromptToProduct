# Copilot Agents Manifest System

> **Automated workflow orchestration for turning natural-language prompts into epics, features, stories, and Python code for banking applications**

## 📋 Overview

The **Copilot Agents Manifest System** is a sophisticated workflow orchestration platform that enables developers to convert natural language prompts into structured development artifacts. This system is specifically designed for banking domain applications with comprehensive fraud detection, compliance, and customer experience capabilities.

## 🎯 Key Features

- **🤖 Intelligent Agent Orchestration**: Multi-agent system with specialized roles
- **📝 Natural Language Processing**: Convert prompts to structured specs
- **🏦 Banking Domain Intelligence**: Specialized for financial services workflows
- **🔄 Automated Code Generation**: From specs to production-ready Python code
- **✅ Validation & Compliance**: Automated validation and GitHub integration
- **📊 Manifest Import/Export**: YAML ↔ JSON conversion with validation

## 🏗️ System Architecture

### Agent Workflow
```
Natural Language Prompt
          ↓
    [Orchestrator] ← Entry Point
          ↓
    ┌─────────────────┐
    │   Route Logic   │
    └─────────────────┘
          ↓
    ┌─────────────┬─────────────┬─────────────┐
    │ Spec Agent  │ Code Agent  │ Validation  │
    │             │             │ Agent       │
    └─────────────┴─────────────┴─────────────┘
          ↓               ↓              ↓
    Create Specs    Generate Code    Validate & Sync
```

### 🤖 Agent Details

#### 1. **Orchestrator Agent**
- **File**: `src/agents/orchestrator.py`
- **Role**: Central hub for prompt classification and routing
- **Capabilities**:
  - `classify_prompt`: Analyze intent and context
  - `route_to_agent`: Delegate to appropriate specialist
  - `memory_context`: Maintain conversation context (10-window persistence)

**Routing Rules**:
```yaml
create/add/generate/build → spec-agent
code/implement/develop → code-agent
validate/check/audit → validation-agent
```

#### 2. **Spec Agent**
- **File**: `src/agents/spec_agent.py`
- **Role**: Convert prompts to structured markdown specifications
- **Actions**:
  - `create_epic`: Generate epic specifications
  - `create_feature`: Create feature specifications with banking context
  - `create_story`: Develop user stories and compliance stories
- **Inputs**: `prompt_schema.json`
- **Outputs**: `specs/**` (epics, features, stories)

#### 3. **Code Agent**
- **File**: `src/agents/code_agent.py`
- **Role**: Generate and update Python code from specifications
- **Actions**:
  - `generate_code_snippet`: Create code from story requirements
  - `commit_changes`: Automated Git operations
- **Inputs**: `specs/stories/**`, `src/MyBank/**`
- **Outputs**: `src/MyBank/**`

#### 4. **Validation Agent**
- **File**: `src/agents/validation_agent.py`
- **Role**: Ensure specification quality and GitHub synchronization
- **Actions**:
  - `validate_links`: Check hierarchical spec linkage
  - `sync_with_github`: Automated GitHub integration
- **Reports**: `github_issues`, `workflow_logs`

## 🚀 Quick Start

### Installation

1. **Clone Repository**
```powershell
git clone https://github.com/vrushalisarfare/PromptToProduct.git
cd PromptToProduct
```

2. **Install Dependencies**
```powershell
pip install PyYAML
pip install -r requirements.txt
```

3. **Verify Installation**
```powershell
python .github\workflows\manifest_loader.py
```

### Basic Usage

#### Import Manifest
```powershell
# Standard import with summary
python .github\workflows\manifest_loader.py

# Debug mode with detailed information
python .github\workflows\manifest_loader.py --debug

# Custom manifest file
python .github\workflows\manifest_loader.py custom_manifest.yaml
```

#### Generate Specifications
```powershell
# Navigate to specs directory
cd specs

# Create banking feature using schema processor
python prompt_cli.py "Create a feature for credit card fraud detection under epic E003"

# Create compliance story
python prompt_cli.py "Add a compliance story for PCI DSS requirements under feature F003"
```

## 📁 Project Structure

```
PromptToProduct/
├── .github/
│   └── workflows/
│       ├── copilot_agents.yaml      # Main agent manifest
│       ├── manifest_loader.py       # Manifest import/export tool
│       └── spec-sync.yml           # GitHub Actions workflow
├── specs/
│   ├── epics/                      # Epic specifications (E001, E002, ...)
│   ├── features/                   # Feature specifications (F001, F002, ...)
│   ├── stories/                    # Story specifications (S001, S002, ...)
│   ├── schema_processor.py         # Core schema processing logic
│   ├── prompt_cli.py              # Command-line interface
│   └── mcp_integration.py         # MCP server integration
├── src/
│   └── agents/                     # Agent implementation files
│       ├── orchestrator.py        # Main orchestration logic
│       ├── spec_agent.py          # Specification generation
│       ├── code_agent.py          # Code generation
│       └── validation_agent.py    # Validation and sync
├── mcp_server/                     # MCP server for GitHub integration
├── prompt_schema.json              # Banking domain schema v2.0
└── README.md                       # This file
```

## 🏦 Banking Domain Intelligence

The system includes specialized banking domain capabilities:

### Product Types
- **Loans**: Mortgage, personal, auto, business loans
- **Credit Cards**: Rewards, secured, corporate cards
- **Payments**: Wire transfers, ACH, mobile payments, P2P
- **Investments**: Portfolio management, trading, robo-advisors
- **Accounts**: Savings, checking, certificates of deposit
- **Digital Banking**: Mobile apps, online platforms, APIs

### Compliance Areas
- **Regulatory**: KYC, AML, SOX, GDPR, PCI-DSS, Basel III
- **Security**: Encryption, tokenization, fraud detection
- **Risk Management**: Credit risk, operational risk, stress testing

## 📊 Manifest Import/Export

### Import Workflow
```powershell
# Import and validate manifest
python .github\workflows\manifest_loader.py

# Output includes:
# ✅ Validation results
# 📋 Agent summary (4 agents detected)
# 💾 JSON export (copilot_agents_manifest.json)
# 🔄 Workflow routing (3 rules defined)
```

### Export Formats

#### YAML (Source)
```yaml
version: "1.0"
project: "Prompt to Product"
description: >
  Copilot Agent Orchestration Manifest for turning natural-language prompts
  into epics, features, stories, and Python code for MyBank.
agents:
  - id: orchestrator
    name: Prompt Orchestrator
    # ... agent configuration
```

#### JSON (Export)
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
    }
  ]
}
```

## 🛠️ Development Workflow

### 1. **Prompt to Specification**
```
Input: "Create a feature for real-time fraud detection in credit cards"
       ↓
Orchestrator → Spec Agent
       ↓
Output: F003-credit-card-fraud-detection.md
```

### 2. **Specification to Code**
```
Input: Story specification S001-real-time-transaction-monitoring.md
       ↓
Orchestrator → Code Agent
       ↓
Output: Python code in src/MyBank/fraud_detection/
```

### 3. **Validation and Sync**
```
Input: Generated specifications and code
       ↓
Validation Agent
       ↓
Output: GitHub issues, validation reports, automated commits
```

## 🔧 Configuration

### Environment Variables
```powershell
# GitHub integration
$env:GITHUB_PERSONAL_ACCESS_TOKEN = "your_token_here"

# MCP server configuration
$env:MCP_HOST = "127.0.0.1"
$env:MCP_PORT = "8080"
$env:GITHUB_WEBHOOK_SECRET = "your_webhook_secret"
```

### VS Code MCP Integration
```json
{
  "mcpServers": {
    "github": {
      "command": "mcp-server-github",
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    },
    "prompttoproduct-local": {
      "command": "python",
      "args": ["mcp_server/mcp_main.py"]
    }
  }
}
```

## 📈 Examples

### Example 1: Create Banking Epic
```powershell
python specs\prompt_cli.py "Create an epic for next-generation digital banking platform"
```

**Output**: `specs/epics/E004-next-generation-digital-banking-platform.md`

### Example 2: Add Compliance Feature
```powershell
python specs\prompt_cli.py "Add a feature for KYC customer onboarding under epic E004"
```

**Output**: `specs/features/F004-kyc-customer-onboarding.md` with banking domain intelligence

### Example 3: Generate User Story
```powershell
python specs\prompt_cli.py "Create a story for biometric authentication under feature F004"
```

**Output**: `specs/stories/S005-biometric-authentication.md`

## 🔍 Validation & Quality Assurance

### Automatic Validation
- **Manifest Structure**: Required fields, agent configurations
- **Spec Linkage**: Epic → Feature → Story hierarchy
- **Banking Compliance**: Regulatory requirements mapping
- **Code Quality**: Integration with validation agent

### Manual Validation
```powershell
# Validate all specifications
python specs\prompt_cli.py --validate

# Check manifest structure
python .github\workflows\manifest_loader.py --debug

# Status overview
python specs\prompt_cli.py --status
```

## 🚦 Status Monitoring

### Health Checks
```powershell
# Manifest system status
python .github\workflows\manifest_loader.py

# Schema system status  
python specs\prompt_cli.py --status

# MCP server health
curl http://127.0.0.1:8080/health
```

### Metrics Tracked
- **Agent Count**: 4 active agents
- **Routing Rules**: 3 defined trigger patterns
- **Specification Count**: Epics, features, stories
- **Validation Status**: Link integrity, orphaned specs
- **GitHub Integration**: Issues synced, workflow status

## 🔐 Security Considerations

### Token Management
- GitHub PAT stored in environment variables
- MCP webhook secret configuration
- Secure API endpoint configuration

### Compliance
- PCI DSS Level 1 requirements support
- KYC/AML workflow integration
- SOX financial reporting compliance
- GDPR data protection measures

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Install development dependencies: `pip install -r requirements-dev.txt`
4. Run tests: `python -m pytest`
5. Submit pull request

### Agent Development
- Follow agent interface patterns in `src/agents/`
- Update `copilot_agents.yaml` for new agents
- Add routing rules to orchestrator
- Include validation logic

## 📚 Documentation

### API Reference
- **Manifest Loader**: `.github/workflows/manifest_loader.py`
- **Schema Processor**: `specs/schema_processor.py`
- **Prompt CLI**: `specs/prompt_cli.py`
- **MCP Integration**: `specs/mcp_integration.py`

### Guides
- [GitHub MCP Setup Guide](GitHub-MCP-Setup-Guide.md)
- [Banking Schema Reference](prompt_schema.json)
- [Agent Development Guide](src/agents/README.md)

## 🐛 Troubleshooting

### Common Issues

**Manifest Import Fails**
```powershell
# Check file permissions and path
python .github\workflows\manifest_loader.py --debug
```

**Agent Routing Not Working**
```powershell
# Validate agent configuration
python .github\workflows\manifest_loader.py --debug
```

**Schema Validation Errors**
```powershell
# Check spec linkage
python specs\prompt_cli.py --validate
```

### Debug Mode
Always use `--debug` flag for detailed troubleshooting information.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎉 Acknowledgments

- GitHub Copilot integration
- Model Context Protocol (MCP) framework
- Banking domain expertise integration
- VS Code extension ecosystem

---

**Version**: 1.0  
**Last Updated**: October 27, 2025  
**Maintained by**: PromptToProduct Team

---

> 🚀 **Ready to transform natural language into production-ready banking applications!**