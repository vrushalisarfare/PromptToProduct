# PromptToProduct - Complete Agent Orchestration System

A sophisticated AI agent system that converts natural language prompts into complete banking software specifications and implementations. Built with a 4-agent architecture for comprehensive prompt-to-code workflow automation.

## 🚀 Quick Start

```bash
# 1. Setup GitHub MCP integration (one-time setup)
cat GitHub-MCP-Setup-Guide.md

# 2. Process a natural language prompt
python prompttoproduct.py "Create a credit card fraud detection system"

# 3. Check system status  
python prompttoproduct.py --status

# 4. Validate all specifications
python prompttoproduct.py --validate-all

# 5. Run specific agent
python prompttoproduct.py --agent orchestrator "Route banking loan requests"
```

> **Note**: This system integrates with GitHub's MCP server - no local server setup required!

## 🏗️ System Architecture

### 4-Agent System Overview

```
┌─────────────────┐    ┌───────────────┐    ┌─────────────┐    ┌─────────────────┐
│   Orchestrator  │───▶│  Spec Agent   │───▶│ Code Agent  │───▶│ Validation Agent│
│   (Router)      │    │  (Markdown)   │    │ (Python)    │    │ (QA & GitHub)   │
└─────────────────┘    └───────────────┘    └─────────────┘    └─────────────────┘
```

#### 1. **Orchestrator Agent** (`orchestrator.py`)
- **Purpose**: Central routing and prompt classification system
- **Capabilities**:
  - Natural language intent classification
  - Banking domain detection (products, compliance, fraud)
  - Multi-agent workflow routing
  - Context memory and session management
  - Real-time status monitoring

#### 2. **Spec Agent** (`spec_agent.py`) 
- **Purpose**: Convert prompts to structured markdown specifications
- **Capabilities**:
  - Epic, Feature, and Story generation
  - Banking domain intelligence (loans, credit cards, fraud detection)
  - Compliance story creation (KYC, AML, PCI-DSS)
  - Schema processor integration
  - Manual fallback systems

#### 3. **Code Agent** (`code_agent.py`)
- **Purpose**: Generate Python implementations from specifications
- **Capabilities**:
  - Banking feature code generation (MyBank structure)
  - Fraud detection models with ML capabilities
  - Compliance validation systems
  - Repository pattern implementations
  - Automated Git commit workflows

#### 4. **Validation Agent** (`validation_agent.py`)
- **Purpose**: Quality assurance and GitHub synchronization
- **Capabilities**:
  - Specification completeness validation
  - Banking compliance scoring
  - GitHub issue creation and management
  - Project board synchronization
  - Quality recommendations

## 📋 Features

### Banking Domain Intelligence
- **Product Types**: Credit Cards, Loans, Accounts, Payments, Investments
- **Compliance Areas**: KYC, AML, PCI-DSS, SOX, Basel III
- **Fraud Detection**: Real-time transaction monitoring, ML-powered risk scoring
- **Regulatory Support**: Automated compliance checking and reporting

### Code Generation Capabilities
- **Architecture Patterns**: Repository, Service, Model, API patterns
- **Banking Modules**: Account management, loan processing, fraud detection
- **Quality Assurance**: Automated testing, validation, and documentation
- **GitHub Integration**: Issue tracking, project boards, automated commits

### Intelligent Routing
- **Intent Classification**: Automatic prompt categorization and routing
- **Context Awareness**: Banking domain detection and specialization
- **Multi-Agent Coordination**: Seamless workflow between agents
- **Memory Management**: Session context and conversation history

## 🛠️ Installation & Setup

### Prerequisites
```bash
# Python 3.8+
python --version

# Git (for repository operations)
git --version
```

### Installation
```bash
# Clone repository
git clone <repository-url>
cd PromptToProduct

# Install dependencies (if needed)
pip install pyyaml requests

# Initialize system
python prompttoproduct.py --status
```

### Directory Structure
```
PromptToProduct/
├── prompttoproduct.py          # Main CLI interface
├── README.md                   # Main project documentation
├── README_Manifest.md          # Copilot Agents manifest documentation
├── GitHub-MCP-Setup-Guide.md   # GitHub MCP integration guide
├── .gitignore                  # Git ignore rules
├── src/
│   ├── agents/                 # 4-agent orchestration system
│   │   ├── orchestrator.py     # Central routing agent
│   │   ├── spec_agent.py       # Specification generator
│   │   ├── code_agent.py       # Code implementation agent
│   │   └── validation_agent.py # Quality & GitHub sync agent
│   └── MyBank/                 # Generated banking code structure
│       ├── accounts/           # Account management modules
│       ├── loans/              # Loan processing modules
│       ├── credit_cards/       # Credit card modules
│       ├── payments/           # Payment processing modules
│       ├── fraud_detection/    # Fraud detection modules
│       └── compliance/         # Compliance modules
├── specs/                      # Specification documents
│   ├── prompt_schema.json      # JSON schema for prompt processing
│   ├── epics/                  # Epic specifications
│   ├── features/               # Feature specifications  
│   └── stories/                # User story specifications
├── prompts/                    # Prompts library and examples
│   ├── banking/                # Banking domain prompts (epics, features, stories, compliance)
│   ├── system/                 # System management prompts (status, validation, deployment)
│   ├── examples/               # Complete workflow examples (fraud detection, credit cards)
│   └── README.md               # Prompts library documentation
└── .github/
    └── workflows/
        ├── manifest_loader.py      # Copilot Agents manifest loader
        ├── copilot_agents.yaml     # Copilot Agents workflow definition
        └── copilot_agents_manifest.json # Generated manifest (JSON)
```

## 📖 Usage Examples

### 📚 Prompts Library
Explore the comprehensive prompts library for tested and validated examples:

```bash
# Browse the prompts library
ls prompts/

# Banking domain prompts
cat prompts/banking/epics.md        # Epic-level initiatives
cat prompts/banking/features.md     # Product capabilities
cat prompts/banking/stories.md      # Implementation tasks
cat prompts/banking/compliance.md   # Regulatory requirements

# Complete workflow examples
cat prompts/examples/fraud_detection.md  # End-to-end fraud detection
cat prompts/examples/credit_cards.md     # Credit card platform example

# System management prompts
cat prompts/system/status.md        # Status monitoring
cat prompts/system/validation.md    # Quality assurance
```

### Basic Prompt Processing
```bash
# Generate fraud detection system
python prompttoproduct.py "Create a real-time fraud detection system for credit card transactions"

# Build loan application API
python prompttoproduct.py "Build a REST API for loan applications with approval workflow"

# Compliance validation system
python prompttoproduct.py "Create KYC compliance validation for new customer onboarding"
```

### Advanced Options
```bash
# With GitHub synchronization
python prompttoproduct.py "Create payment processing system" --sync-github

# Skip validation
python prompttoproduct.py "Generate account management API" --no-validate

# JSON output
python prompttoproduct.py "Build fraud alerts" --json

# Verbose logging
python prompttoproduct.py "Create loan calculator" --verbose
```

### Agent-Specific Operations
```bash
# Run orchestrator only
python prompttoproduct.py --agent orchestrator "Analyze banking request routing"

# Generate specs only  
python prompttoproduct.py --agent spec-agent "Create credit card application epic"

# Generate code only
python prompttoproduct.py --agent code-agent "Implement fraud detection models"

# Validate specifications
python prompttoproduct.py --agent validation-agent "Check spec completeness"
```

### System Management
```bash
# System status
python prompttoproduct.py --status

# Validate all specs
python prompttoproduct.py --validate-all

# Individual agent status
python src/agents/orchestrator.py --status
python src/agents/spec_agent.py --status  
python src/agents/code_agent.py --status
python src/agents/validation_agent.py --status
```

## 🏦 Banking Domain Examples

### Credit Card Features
```bash
python prompttoproduct.py "Create credit card application processing system with fraud detection"
```
**Generates:**
- Epic: Credit Card Management System
- Features: Application processing, fraud detection, account management
- Code: CreditCardModel, FraudDetector, TransactionMonitor
- Validation: Compliance checking, security validation

### Loan Processing
```bash  
python prompttoproduct.py "Build loan origination system with risk assessment"
```
**Generates:**
- Epic: Loan Origination Platform
- Features: Application intake, risk scoring, approval workflow
- Code: LoanModel, RiskAssessment, ApprovalEngine
- Validation: Regulatory compliance, data validation

### Fraud Detection
```bash
python prompttoproduct.py "Implement real-time fraud monitoring for all transactions"
```
**Generates:**
- Epic: Enterprise Fraud Detection
- Features: Real-time monitoring, ML scoring, alert management
- Code: FraudDetector, TransactionMonitor, AlertSystem
- Validation: Performance testing, accuracy validation

## 🔧 Configuration

### GitHub Integration
Set environment variable for GitHub synchronization:
```bash
export GITHUB_TOKEN="your_github_token"
```

### Agent Configuration
Each agent supports configuration through parameters:

```python
# Orchestrator configuration
orchestrator_config = {
    "max_context_memory": 10,
    "banking_detection_threshold": 0.7,
    "default_routing": "spec-agent"
}

# Spec Agent configuration  
spec_config = {
    "output_format": "markdown",
    "banking_templates": True,
    "compliance_integration": True
}

# Code Agent configuration
code_config = {
    "target_language": "python",
    "architecture_patterns": ["repository", "service"],
    "auto_commit": True
}

# Validation Agent configuration
validation_config = {
    "completeness_threshold": 0.8,
    "github_sync": True,
    "auto_issue_creation": True
}
```

## 🎯 Advanced Workflows

### Complete Feature Development
```bash
# 1. Generate specifications
python prompttoproduct.py "Create mobile banking authentication system"

# 2. Validate specifications
python prompttoproduct.py --validate-all

# 3. Generate implementation
python prompttoproduct.py --agent code-agent "Implement authentication system"

# 4. Sync with GitHub
python prompttoproduct.py --agent validation-agent "Sync authentication features" --sync-github
```

### Banking Compliance Workflow
```bash
# Generate KYC compliance system
python prompttoproduct.py "Create KYC customer verification system with document validation"

# Validate compliance requirements
python prompttoproduct.py --agent validation-agent "Check KYC compliance coverage"

# Generate audit reports
python prompttoproduct.py --agent validation-agent "Generate compliance audit report" --sync-github
```

### Fraud Detection Pipeline
```bash
# Create fraud detection system
python prompttoproduct.py "Build ML-powered fraud detection with real-time alerts"

# Validate fraud models
python prompttoproduct.py --agent validation-agent "Validate fraud detection accuracy"

# Generate monitoring dashboards
python prompttoproduct.py --agent code-agent "Create fraud monitoring dashboard"
```

## 🤝 Integration

### GitHub MCP Server Integration
This system is designed to work with GitHub's Model Context Protocol (MCP) server, providing seamless integration with VS Code and GitHub Copilot. No local MCP server required - everything works through GitHub's cloud infrastructure.

### Copilot Agents Integration
The system includes Copilot Agents manifest support:
```bash
# Load and generate Copilot Agents manifest
python .github/workflows/manifest_loader.py

# View generated manifest
cat .github/workflows/copilot_agents_manifest.json

# View manifest documentation
cat README_Manifest.md

# Setup GitHub MCP integration
cat GitHub-MCP-Setup-Guide.md
```

## 🔍 Troubleshooting

### Common Issues

**Import Errors**
```bash
# Ensure Python path is correct
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python prompttoproduct.py --status
```

**Agent Initialization Failures**
```bash
# Check individual agent status
python src/agents/orchestrator.py --status
python src/agents/spec_agent.py --status
```

**GitHub Sync Issues**
```bash
# Verify GitHub token
echo $GITHUB_TOKEN

# Test GitHub connectivity
python prompttoproduct.py --agent validation-agent "test github connection"
```

**Validation Failures**
```bash
# Run comprehensive validation
python prompttoproduct.py --validate-all --verbose

# Check specific specs
python prompttoproduct.py --agent validation-agent "validate specific file" --file specs/stories/S001-Setup-MCP-Server.md
```

### Debug Mode
```bash
# Enable verbose logging
python prompttoproduct.py "your prompt" --verbose

# Get detailed agent status
python prompttoproduct.py --status --json
```

## 📚 Documentation

- **System Architecture**: See `README_Manifest.md` for Copilot Agents integration
- **Agent APIs**: Each agent includes comprehensive docstrings and CLI help
- **Banking Domain**: Built-in banking intelligence and compliance frameworks
- **Code Examples**: Generated code follows banking industry best practices

## 🚀 Future Enhancements

### Planned Features
- **Multi-language Code Generation**: Support for Java, JavaScript, Go
- **Advanced ML Integration**: Enhanced fraud detection models
- **Compliance Automation**: Automated regulatory report generation
- **Real-time Collaboration**: Multi-user specification editing
- **Cloud Integration**: AWS/Azure banking service integration

### Extensibility
- **Custom Agents**: Plugin architecture for specialized agents
- **Domain Extensions**: Support for other financial domains (insurance, trading)
- **Integration Hooks**: Webhook support for external system integration
- **Custom Templates**: User-defined specification and code templates

## 📄 License

This project is part of the PromptToProduct system for banking software development automation.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

**PromptToProduct** - Transforming natural language into production-ready banking software through intelligent agent orchestration.
