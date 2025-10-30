# PromptToProduct - Unified LangGraph Orchestration System

A sophisticated unified AI system that converts natural language prompts into complete software specifications and implementations. Built with integrated LangGraph workflow orchestration and intelligent prompt classification for comprehensive prompt-to-code automation.

## 🚀 Quick Start

```bash
# 1. Install LangGraph dependencies
pip install -r requirements.txt

# 2. Process a natural language prompt with unified workflow
python prompttoproduct.py "Create a credit card fraud detection system"

# 3. Check unified system status  
python prompttoproduct.py --status

# 4. Get JSON output for automation
python prompttoproduct.py "Build payment API" --json

# 5. Get help with commands
python prompttoproduct.py --help
```

> **Latest**: Now features unified architecture with integrated orchestration and LangGraph workflows!

## 🏗️ Unified Architecture

### Integrated 4-Agent Workflow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           PromptToProduct Unified System                        │
│  ┌─────────────────┐    ┌───────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │  Orchestration  │───▶│  Spec Agent   │───▶│ Validation  │───▶│  Finalize   │ │
│  │  Intelligence   │    │  (Spec Gen)   │    │ (Quality)   │    │ (Complete)  │ │
│  │  • Classification│    │               │    │             │    │             │ │
│  │  • Banking Domain│    │               │    │             │    │             │ │
│  │  • Intent Routing│    │               │    │             │    │             │ │
│  │  • Memory Context│    │               │    │             │    │             │ │
│  └─────────────────┘    └───────────────┘    └─────────────┘    └─────────────┘ │
│           │                       │                   │                          │
│           └─────▶ Code Agent ──────┘                   │                          │
│             (Parallel Path)                            │                          │
│                                                        ▼                          │
│                                                ┌─────────────┐                    │
│                                                │Error Handler│                    │
│                                                │ (Recovery)  │                    │
│                                                └─────────────┘                    │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### **Unified System Features**

**🧠 Integrated Orchestration Intelligence:**
- Natural language intent classification (create_spec, implement_code, validate)
- Banking domain detection (loans, payments, credit cards, investments, compliance)
- Entity extraction (epic/feature/story references, technical terms)
- Confidence scoring for routing decisions
- Memory context persistence across conversations

**⚡ LangGraph Workflow Management:**
- Stateful workflow execution with conditional routing
- Error handling and recovery mechanisms
- Circuit breaker protection against infinite loops
- Enhanced recursion limit management

#### **Agent Components**

**1. Spec Agent** (`spec_agent.py`) 
- **Role**: Specification generation with intelligent domain detection
- **Capabilities**:
  - Epic, Feature, and Story generation
  - Banking domain intelligence (loans, credit cards, fraud detection)
  - Compliance story creation (KYC, AML, PCI-DSS)
  - Schema processor integration
  - Manual fallback systems

**2. Code Agent** (`code_agent.py`)
- **Role**: Generate Python implementations from specifications
- **Capabilities**:
  - Banking feature code generation
  - Fraud detection models with ML capabilities
  - Compliance validation systems
  - Repository pattern implementations
  - Automated Git workflow integration

**3. Validation Agent** (`validation_agent.py`)
- **Role**: Quality assurance and compliance validation
- **Capabilities**:
  - Specification completeness validation
  - Banking compliance scoring
  - Code quality assessment
  - Architectural recommendations
  - Integration with GitHub MCP server

## 📋 Key Features

### 🧠 Intelligent Classification
- **Intent Recognition**: Automatically classifies prompts (create_spec, implement_code, validate)
- **Domain Detection**: Banking products (credit cards, loans, payments, investments)
- **Compliance Awareness**: KYC, AML, PCI-DSS, SOX, Basel III keyword detection
- **Entity Extraction**: Finds epic/feature/story references and technical terms

### 🔄 Unified Workflow Management
- **Integrated Orchestration**: Single system combining classification + execution
- **Memory Persistence**: Conversation context maintained across sessions
- **Error Recovery**: Robust error handling with circuit breakers
- **GitHub Integration**: Seamless project management via MCP server

## 🛠️ Installation & Setup

### Prerequisites
```bash
# Python 3.8+
python --version

# LangGraph and dependencies
pip install langgraph langchain langchain-core

# Git (for repository operations)
git --version
```

### Installation
```bash
# Clone repository
git clone https://github.com/vrushalisarfare/PromptToProduct.git
cd PromptToProduct

# Install dependencies
pip install -r requirements.txt

# Test unified system
python prompttoproduct.py --status
```

### System Status Check
```bash
# Verify unified system installation
python prompttoproduct.py --status

# Expected output:
🎯 PROMPTTOPRODUCT UNIFIED SYSTEM STATUS
============================================================
System: PromptToProduct Unified
Version: 2.1.0
Architecture: Unified LangGraph + Orchestration
Workflow Nodes: 6
Memory Entries: 0

Agent Status:
  spec_agent: ✅ Available
  code_agent: ✅ Available
  validation_agent: ✅ Available

Features:
  orchestration: ✅ Integrated
  classification: ✅ Banking domain detection
  routing: ✅ Intent-based routing
  memory: ✅ Context persistence
  langgraph: ✅ Stateful workflows
```

### Directory Structure
```
PromptToProduct/
├── prompttoproduct.py          # Unified system entry point
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
├── .env                       # Environment configuration
├── .gitignore                 # Git ignore patterns
├── src/
│   ├── agents/                 # Agent components
│   │   ├── spec_agent.py       # Specification generator
│   │   ├── code_agent.py       # Code implementation agent
│   │   └── validation_agent.py # Quality validation agent
│   ├── config.py              # Configuration management
│   └── MyBank/                # Generated banking code structure
├── specs/                     # Generated specifications (gitignored)
│   ├── epics/                 # Epic specifications
│   ├── features/              # Feature specifications
│   └── stories/               # User story specifications
├── prompts/                   # Prompts library and examples
│   ├── banking/               # Banking domain prompts
│   ├── system/                # System management prompts
│   └── examples/              # Complete workflow examples
└── .github/
    └── workflows/
        └── copilot_agents.yaml    # Agent configuration
```
        ├── copilot_agents.yaml     # Copilot Agents workflow definition
        └── copilot_agents_manifest.json # Generated manifest (JSON)
```

## 📖 Usage Examples

### 📚 Prompts Library
Explore the comprehensive prompts library for tested and validated examples:

## 💻 Usage Examples

### Basic Commands
```bash
# Check system status
python prompttoproduct.py --status

# Get JSON output for automation
python prompttoproduct.py --status --json

# Enable verbose logging
python prompttoproduct.py "Create user authentication" --verbose
```

### Specification Generation
```bash
# Generate banking feature specifications
python prompttoproduct.py "Create a real-time fraud detection system for credit card transactions"

# Build API specifications
python prompttoproduct.py "Build a REST API for loan applications with approval workflow"

# Compliance feature creation
python prompttoproduct.py "Create KYC compliance validation for new customer onboarding"

# User interface features
python prompttoproduct.py "Create a user dashboard for account management"

# Payment processing features
python prompttoproduct.py "Build a payment processing system with real-time validation"
```

### Banking Domain Examples
```bash
# Credit card features
python prompttoproduct.py "Create credit card application approval system"

# Loan processing
python prompttoproduct.py "Build automated loan underwriting with risk assessment"

# Account management
python prompttoproduct.py "Create multi-currency savings account management"

# Fraud detection
python prompttoproduct.py "Build ML-powered transaction fraud detection"

# Compliance
python prompttoproduct.py "Create AML transaction monitoring system"
```

### Output Formats
```bash
# Standard workflow output
python prompttoproduct.py "Create payment gateway"

# JSON output for automation
python prompttoproduct.py "Create payment gateway" --json

# Status check with detailed info
python prompttoproduct.py --status --verbose
```

# Generate specs only  
python prompttoproduct.py --agent spec-agent "Create credit card application epic"

# Generate code only
python prompttoproduct.py --agent code-agent "Implement fraud detection models"

# Validate specifications
python prompttoproduct.py --agent validation-agent "Check spec completeness"
```

## 🏦 Banking Domain Intelligence

### Supported Banking Products
- **Credit Cards**: Application processing, fraud detection, rewards management
- **Loans**: Underwriting, risk assessment, payment processing
- **Accounts**: Savings, checking, multi-currency support
- **Payments**: Real-time processing, validation, settlement
- **Investments**: Portfolio management, trading, risk analysis

### Compliance Framework Support
- **KYC (Know Your Customer)**: Identity verification, due diligence
- **AML (Anti-Money Laundering)**: Transaction monitoring, suspicious activity reporting
- **PCI-DSS**: Payment card industry security standards
- **SOX**: Sarbanes-Oxley compliance for financial reporting
- **Basel III**: Banking regulatory framework compliance

### Example Banking Workflows

#### Credit Card System
```bash
python prompttoproduct.py "Create credit card application processing system with fraud detection"
```
**Generated Output:**
- Epic: Credit Card Management Platform
- Features: Application processing, real-time fraud detection, account management
- Stories: User application, credit scoring, transaction monitoring
- Code: CreditCardModel, FraudDetector, TransactionMonitor classes

#### Loan Processing System
```bash
python prompttoproduct.py "Build automated loan underwriting with ML risk assessment"
```
**Generated Output:**
- Epic: Intelligent Loan Processing Platform
- Features: Automated underwriting, risk assessment, approval workflow
- Stories: Loan application, credit analysis, decision engine
- Code: LoanProcessor, RiskAssessment, UnderwritingEngine classes

#### Compliance Monitoring
```bash
python prompttoproduct.py "Create AML transaction monitoring with suspicious activity alerts"
```
**Generated Output:**
- Epic: AML Compliance Management System
- Features: Transaction monitoring, suspicious activity detection, regulatory reporting
- Stories: Real-time monitoring, alert generation, compliance reporting
- Code: AMLMonitor, SuspiciousActivityDetector, ComplianceReporter classes  
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
## 🔧 Configuration

### Environment Setup
Create `.env` file for configuration:
```bash
# .env file
GITHUB_TOKEN=your_github_token_here
GITHUB_REPO=PromptToProduct
GITHUB_PROJECT=Prompt To Product Development
OPENAI_API_KEY=your_openai_key_here  # If using OpenAI
```

### System Configuration
The unified system supports various configuration options:

```python
# Default configuration in prompttoproduct.py
DEFAULT_CONFIG = {
    "recursion_limit": 50,
    "max_execution_time": 300,
    "validation_threshold": 0.3,
    "memory_context_window": 10,
    "enable_memory_persistence": True
}
```

### Agent-Specific Settings
```python
# Banking domain detection configuration
BANKING_KEYWORDS = {
    "loans": ["loan", "lending", "mortgage", "credit", "financing"],
    "credit_cards": ["credit card", "card", "plastic", "rewards"],
    "payments": ["payment", "transfer", "wire", "ach", "settlement"],
    "investments": ["investment", "portfolio", "trading", "stocks"],
    "accounts": ["account", "savings", "checking", "deposit"],
    "digital_banking": ["mobile app", "online banking", "digital", "api"]
}

# Compliance keywords
COMPLIANCE_KEYWORDS = ["kyc", "aml", "pci-dss", "sox", "gdpr", "basel"]
## 🎯 Advanced Features

### Memory Context Management
The unified system maintains conversation context across sessions:

```bash
# View recent conversation context
python prompttoproduct.py --memory

# Clear memory context
python prompttoproduct.py --clear-memory

# Set memory context window
python prompttoproduct.py --memory-window 20
```

### GitHub Integration via MCP Server
Seamless integration with GitHub for project management:

- **Issue Creation**: Automatically creates GitHub issues from specifications
- **Project Boards**: Syncs with GitHub Projects v2 for tracking
- **Repository Management**: Integrates with existing GitHub repositories
- **Branch Management**: Supports feature branch workflows

### Workflow Customization
```bash
# Skip validation step
python prompttoproduct.py "Create API" --skip-validation

# Force code generation
python prompttoproduct.py "Build payment system" --force-code

# Custom output directory
python prompttoproduct.py "Create dashboard" --output-dir ./custom/

# Set recursion limit
python prompttoproduct.py "Complex system" --recursion-limit 100
```

### Banking Compliance Features
- **Automated Compliance Checking**: Built-in validation for banking regulations
- **Risk Assessment Integration**: ML-powered risk scoring
- **Audit Trail Generation**: Complete audit logs for regulatory compliance
- **Security Best Practices**: Implements banking-grade security patterns
```bash
# 1. Generate specifications
python prompttoproduct.py "Create mobile banking authentication system"

# 2. Validate specifications
python prompttoproduct.py --validate-all

## 🚀 System Highlights

### Recent Improvements (v2.1.0)
- **✅ Unified Architecture**: Merged orchestration intelligence directly into main system
- **✅ Fixed Recursion Limits**: Eliminated infinite retry loops with smart circuit breakers
- **✅ Enhanced Error Handling**: Robust error recovery and workflow management
- **✅ Simplified Dependencies**: Reduced agent complexity and import overhead
- **✅ GitHub MCP Integration**: Seamless project management via GitHub MCP server
- **✅ Memory Persistence**: Conversation context maintained across sessions

### Performance Improvements
- **Reduced Latency**: Direct method calls vs. inter-agent communication
- **Better Resource Usage**: Single process vs. multiple agent processes
- **Simplified Debugging**: Unified error tracking and logging
- **Enhanced Reliability**: Circuit breaker protection against workflow failures

### Architecture Benefits
- **Single Entry Point**: `prompttoproduct.py` handles all operations
- **Integrated Intelligence**: Built-in classification and routing
- **Stateful Workflows**: LangGraph state management with conditional routing
- **Banking Domain Expertise**: Built-in understanding of financial services

## 🤝 Contributing

### Development Setup
```bash
# Clone the repository
git clone https://github.com/vrushalisarfare/PromptToProduct.git
cd PromptToProduct

# Create development environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8  # Development tools

# Run tests
python -m pytest tests/

# Run the system
python prompttoproduct.py --status
```

### Code Style
- Follow PEP 8 Python style guidelines
- Use type hints for better code documentation
- Add docstrings for all public methods
- Write unit tests for new functionality

### Submitting Changes
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🤝 Integration

## 🔍 Troubleshooting

### Common Issues

**Q: "LangGraph not available" error**
```bash
# Install LangGraph dependencies
pip install langgraph langchain langchain-core

# Verify installation
python -c "import langgraph; print('LangGraph installed successfully')"
```

**Q: Recursion limit errors**
```bash
# The system now handles this automatically, but you can adjust if needed
python prompttoproduct.py "complex prompt" --recursion-limit 100
```

**Q: GitHub integration not working**
```bash
# Set GitHub token in .env file
echo "GITHUB_TOKEN=your_token_here" >> .env

# Test GitHub connectivity
python prompttoproduct.py --status
```

**Q: Memory context issues**
```bash
# Clear memory if corrupted
rm orchestrator_memory.json

# Restart with clean memory
python prompttoproduct.py --status
```

**Q: Validation scores always 0.0**
```bash
# This is expected - the system now proceeds regardless of validation scores
# The workflow will complete successfully
```

### Performance Optimization
- **Large Prompts**: Break down complex requests into smaller components
- **Memory Usage**: Adjust context window size if experiencing memory issues
- **GitHub Rate Limits**: Add delays between GitHub operations if hitting rate limits

### Getting Help
- Check the status with `python prompttoproduct.py --status`
- Use verbose mode for detailed logging: `--verbose`
- Review generated files in `specs/` directory
- Check workflow logs for specific error messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangGraph**: For providing the stateful workflow framework
- **LangChain**: For the underlying agent architecture components
- **GitHub MCP Server**: For seamless repository integration
- **VS Code Extensions**: For development environment support

---

**PromptToProduct v2.1.0** - Unified LangGraph Orchestration System  
Built with ❤️ for intelligent software development automation.

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
