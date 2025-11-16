# PromptToProduct: Unified Agent System

> **A comprehensive LangGraph-powered agentic orchestration system for banking domain development with intelligent prompt-to-product workflows**

🏦 **Banking Domain Intelligence** | 🤖 **Multi-Agent Orchestration** | 📋 **Spec-Driven Development** | 🔄 **Complete Automation** | 🧪 **Comprehensive Testing**

---

## 🌟 Overview

PromptToProduct is an advanced agentic orchestration system that transforms natural language prompts into complete banking specifications, production-ready code, and comprehensive test suites. Built on LangGraph with intelligent routing, the system enforces spec-driven development, provides comprehensive banking domain intelligence, and automatically generates extensive test coverage for all components.

### 🎯 Core Value Proposition
- **Intelligent Routing**: Automatically directs prompts to appropriate agents based on intent and domain
- **Spec-Driven Development**: Enforces specification creation before code implementation 
- **Banking Domain Intelligence**: Built-in understanding of banking products, compliance, and workflows
- **Complete Automation**: End-to-end workflow from prompt to validated specifications and code
- **Multi-Agent Coordination**: Seamless collaboration between SpecAgent, CodeAgent, and ValidationAgent
- **Comprehensive Test Generation**: Automatic creation of extensive test suites with banking domain intelligence
- **BDD Integration**: Embedded Gherkin scenarios in stories and GitHub issues for behavior-driven development


## 📋 Spec-Driven Development Framework

### GitHub MCP Server Integration
This system is designed to work with GitHub's Model Context Protocol (MCP) server, providing seamless integration with VS Code and GitHub Copilot. For detailed setup instructions, see [GitHub MCP Setup Guide](GitHub-MCP-Setup-Guide.md).

### 🧠 LangGraph Orchestration

The system uses LangGraph for sophisticated workflow management with advanced agentic capabilities:

#### **Complete Workflow Architecture**
```
┌─────────────────┐    ┌───────────────┐    ┌─────────────┐    ┌─────────────────┐
│   Orchestrator  │───▶│  Spec Agent   │───▶│ Code Agent  │───▶│ Validation Agent│
│   (Router)      │    │  (Markdown)   │    │ (Python)    │    │ (QA & GitHub)   │
└─────────────────┘    └───────────────┘    └─────────────┘    └─────────────────┘
```
1. **Orchestrator Agent (orchestrator.py)**
- Purpose: Central routing and prompt classification system
- Capabilities:
- Natural language intent classification
  Banking domain detection (products, compliance, fraud)
  Multi-agent workflow routing
- Context memory and session management
- Real-time status monitoring

2. **Spec Agent (spec_agent.py)**
- Purpose: Convert prompts to structured markdown specifications
- Capabilities:
  Epic, Feature, and Story generation
  Banking domain intelligence (loans, credit cards, fraud detection)
  Compliance story creation (KYC, AML, PCI-DSS)
- Schema processor integration

3. **Code Agent (code_agent.py)**
- Purpose: Generate Python implementations from specifications
- Capabilities:
  Banking feature code generation (MyBank structure)
  Fraud detection models with ML capabilities
  Compliance validation systems
  Repository pattern implementations
  Automated Git commit workflows
4. **Validation Agent (validation_agent.py)**
- Purpose: Quality assurance and GitHub synchronization
- Capabilities:
  Specification completeness validation
  Banking compliance scoring
  GitHub issue creation and management
  Project board synchronization
  Quality recommendations

### 🔄 Workflow Enforcement
The system enforces a specification-first approach:

1. **Specification Check**: Before any code generation, system verifies relevant specifications exist
2. **Automatic Spec Creation**: If specs missing, routes to SpecAgent first
3. **Spec-Driven Implementation**: CodeAgent uses specifications as blueprints
4. **Validation Alignment**: ValidationAgent tests against specifications

### 📝 Specification Hierarchy
```
Epic (E001) - High-level business initiative
├── Feature (F001) - Specific product capability
│   ├── Story (S001) - Implementation task
│   ├── Story (S002) - Integration task
│   └── Compliance (C001) - Regulatory requirement
└── Feature (F002) - Additional capability
    ├── Story (S003) - API development
    └── Story (S004) - Testing requirements
```

### ✅ Benefits of Spec-Driven Development
- **Consistency**: All code aligns with documented requirements
- **Traceability**: Clear mapping from requirements to implementation
- **Quality**: Reduces implementation errors and misalignment
- **Compliance**: Ensures regulatory requirements are addressed
- **Maintainability**: Makes code changes more predictable and safe

## 📚 Comprehensive Prompts Library

### 📁 Library Structure
```
prompts/
├── banking/                     # Banking domain prompts
│   ├── epics.md                # Epic-level prompts
│   ├── features.md             # Feature-level prompts  
│   ├── stories.md              # Story-level prompts
│   ├── compliance.md           # Compliance-focused prompts
│   ├── code_implementation.md  # Code generation prompts
│   └── workflows.md            # Complete workflow prompts
├── system/                      # System management prompts
│   ├── status.md               # Status and monitoring prompts
│   ├── validation.md           # Validation and testing prompts
│   └── orchestration.md        # LangGraph orchestration prompts
└── examples/                    # Complete workflow examples
    ├── credit_cards.md         # Credit card system examples
    └── fraud_detection.md      # Fraud detection examples

```
### Mobile Banking App (Biometric) + Auth Service

1. Start Auth Service (FastAPI)

```powershell
# From repository root
pip install -r requirements.txt
$env:AUTH_JWT_SECRET="change-me-strong" ; uvicorn code.MyBank.api.auth_service.auth_api:app --reload --port 8000
```

2. Run Mobile App (Expo)

```powershell
cd code/mobile-banking-app
npm install
$env:EXPO_PUBLIC_API_BASE_URL="http://localhost:8000/api/v1" ; npm run start
```

Demo login: `demo` / `ChangeMe123!`

### Example Prompts

#### Epic Creation
```
"Create an epic for digital loan origination platform with AI-powered risk assessment"
```

#### Feature Development
```
"Add a feature for real-time fraud detection in credit card transactions under epic E001"
```

#### Code Implementation
```
"Implement REST API for loan application submission with validation"
```

#### Complete Workflow
```
"Create specifications and implement digital banking platform with mobile app"
```
#### Basic Pattern Structure
```
Action + Subject + Context + Constraints + Testing

Examples:
"Create a feature for fraud detection under epic E001 with comprehensive test coverage"
"Add a compliance story for PCI DSS under feature F002 with security testing"
"Build a loan origination system with AI risk assessment and full test automation"
```

## 🚀 Quick Start

### Prerequisites
```powershell
# Python 3.8+
python --version
```
### Installation & Setup
```powershell
# Clone and navigate
git clone <repository-url>
# Install requirements
pip install -r requirements.txt

# Add GitHub token for enhanced capabilities
$env:GITHUB_TOKEN = "your_github_token_here"
# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

```
### 📁 Updated Project Structure (Nov 2025)
```
.
├── prompttoproduct.py               # Main orchestrator (LangGraph routing)
├── langgraph_demo.py                # Demo runner / sample workflow
├── Agents.md                        # Unified agent system overview
├── README.md                        # High-level project introduction
├── requirements.txt                 # Python dependencies
├── setup-environment.ps1            # PowerShell environment bootstrap
├── orchestrator_memory.json         # Persisted session/orchestrator memory state
│
├── code/                            # Generated & domain implementation space (ignored in VCS per .gitignore)
│   ├── README.md
│   ├── docs/                        # Generated / supplemental documentation
│   ├── MyBank/                      # Banking domain packages
│   │   ├── accounts/                # Account lifecycle logic
│   │   ├── api/                     # API service modules (FastAPI endpoints, auth, etc.)
│   │   ├── compliance/              # Regulatory helpers & checks
│   │   ├── credit_cards/            # Credit card domain logic
│   │   ├── fraud_detection/         # Fraud & anomaly detection modules
│   │   ├── general/                 # Shared banking models/services
│   │   ├── investments/             # Investment product scaffolding
│   │   ├── loans/                   # Loan origination & underwriting logic
│   │   ├── payments/                # Payment processing abstractions
│   │   ├── shared/                  # Cross-cutting utilities (config, adapters)
│   │   └── tests/                   # Domain-level tests tied to generated specs
│   ├── samples/                     # Example generated artifacts/snippets
│   ├── tests/                       # (If present) additional generated test suites
│   └── utils/                       # Helper utilities for code generation/runtime
│
├── specs/                           # Source-of-truth specifications (epics/features/stories)
│   ├── prompt_schema.json           # Spec schema definition
│   ├── schema_processor.py          # Spec parsing/validation logic
│   ├── epics/                       # Epic markdown files (E001, E002, ...)
│   ├── features/                    # Feature specs (linked to epics)
│   ├── stories/                     # Story specs (implementation tasks)
│   └── featurefiles/                # Legacy / intermediate spec artifacts
│
├── prompts/                         # Prompt templates & domain prompt library
│   ├── banking/                     # Domain-specific prompt collections
│   ├── system/                      # Orchestration/status/validation prompts
│   └── examples/                    # End-to-end workflow examples
│
├── src/                             # Source code for agents & runtime logic
│   ├── config.py                    # Central configuration (env, constants)
│   ├── agents/                      # (If populated) explicit agent implementations
│   ├── MyBank/                      # Core business logic (may mirror `code/` stable parts)
│   └── utils/                       # Shared utilities for orchestrator & agents
│
├── tests/                           # Stable/manual test suites (non-generated)
│   ├── epics/                       # Tests validating epic spec integrity
│   ├── features/                    # Feature-level behavioral tests
│   ├── stories/                     # Story implementation validation
│   ├── banking/                     # Domain scenario tests
│   ├── compliance/                  # Regulatory rule enforcement tests
│   ├── integration/                 # Cross-module integration tests
│   └── README.md                    # Test framework overview
│
├── docs/                            # Human-authored documentation (deployment, architecture)
│   ├── deployment_guide.md          # Deployment & environment guidance
│   └── architecture/ (if present)   # Architectural deep-dives
│
└── __pycache__/                     # Python cache directories
```

#### Key Structural Conventions
- `specs/` is authoritative; agents must never mutate spec files without versioning rules.
- `prompts/` drives generation; changes here can alter downstream artifacts—treat as configuration.
- `code/` is treated as a generated/workspace area and currently ignored by Git (per updated `.gitignore`) to prevent noise; promote stable modules to `src/` when hardened.
- `tests/` distinguishes stable manually curated tests from generated domain tests inside `code/MyBank/tests/`.
- `orchestrator_memory.json` enables continuity across sessions (routing decisions, artifact lineage).

#### Evolution & Promotion Workflow
1. Generate initial domain implementation in `code/MyBank/...`.
2. Validate against specs + tests.
3. Promote hardened modules into `src/MyBank/` for long-term maintenance.
4. Update or backfill tests in root `tests/` to ensure stability outside regeneration cycles.

#### Spec Linking
- Each epic (e.g., `specs/epics/E001-*.md`) should reference associated features and story IDs.
- Features and stories must back-reference their parent epic ID for traceability.
- Validation agent emits coverage metrics mapping spec sections → code modules.

#### Ignored Directories
- `code/`, `deploy/`, `docs/` (per `.gitignore` adjustments) to reduce commit surface; selectively stage promotions only.

#### Recommended Next Additions
- `CONTRIBUTING.md` (if absent) cross-linking Agents.md guidelines.
- `SECURITY.md` enumerating compliance control mapping strategy.
- `specs/index.json` for quick artifact discovery & lineage API.

##  Learning & Best Practices

### Best Practices for Prompts
1. **Be Specific**: Include domain context and compliance requirements
2. **Use Hierarchy**: Build epic → feature → story progressions
3. **Include Constraints**: Specify security, performance, and compliance needs
4. **Provide Context**: Reference existing specifications when building on them

### Banking Domain Guidelines
1. **Security First**: Always consider security implications
2. **Compliance Aware**: Include relevant regulatory requirements
3. **Risk Assessment**: Consider risk factors in all implementations
4. **Integration Focus**: Design for system integration and interoperability

### Code Quality Standards
1. **Documentation**: All generated code includes comprehensive documentation
2. **Testing**: Comprehensive test coverage for all generated code
3. **Security**: Security-first approach with built-in protections
4. **Maintainability**: Clean, readable, and maintainable code structure

## 🚨 Troubleshooting

### Common Issues
1. **Agent Routing Problems**: Check prompt clarity and domain context
2. **Specification Gaps**: Ensure all parent specifications exist
3. **Code Generation Errors**: Verify specification completeness
4. **Validation Failures**: Check compliance requirements alignment


### Support & Resources
- **Documentation**: Comprehensive guides in `docs/` directory
- **Examples**: Working examples in `examples/` directory  
- **Community**: GitHub discussions and issues
- **Support**: Enterprise support available for production deployments

---

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

## 🤝 Contributing

We welcome contributions! Please see CONTRIBUTING.md for guidelines on:
- Code style and standards
- Testing requirements
- Documentation standards
- Banking domain expertise
- Security considerations

## 📞 Support

- **Issues**: GitHub Issues for bug reports and feature requests
- **Discussions**: GitHub Discussions for questions and community support
- **Enterprise**: Contact for enterprise support and consulting

---

**Made with ❤️ for the GCC CIOA | Powered by LangGraph & Advanced AI**