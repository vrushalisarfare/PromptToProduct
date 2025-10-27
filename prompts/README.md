# PromptToProduct Prompts Library

A comprehensive collection of tested and validated prompts for the PromptToProduct 4-Agent System. These prompts are designed to work seamlessly with the Orchestrator, SpecAgent, CodeAgent, and ValidationAgent.

## 📁 Library Structure

```
prompts/
├── README.md                    # This file
├── banking/                     # Banking domain prompts
│   ├── epics.md                # Epic-level prompts
│   ├── features.md             # Feature-level prompts  
│   ├── stories.md              # Story-level prompts
│   └── compliance.md           # Compliance-focused prompts
├── system/                      # System management prompts
│   ├── status.md               # Status and monitoring prompts
│   ├── validation.md           # Validation and testing prompts
│   └── deployment.md           # Deployment and sync prompts
├── examples/                    # Complete workflow examples
│   ├── credit_cards.md         # Credit card system examples
│   ├── fraud_detection.md      # Fraud detection examples
│   └── loan_processing.md      # Loan processing examples
└── templates/                   # Prompt templates and patterns
    ├── epic_templates.md       # Epic creation templates
    ├── feature_templates.md    # Feature creation templates
    └── story_templates.md      # Story creation templates
```

## 🚀 Quick Start

### Basic Usage
```bash
# Using main CLI
python prompttoproduct.py "<prompt_from_library>"

# Check system status first
python prompttoproduct.py --status

# Validate results
python prompttoproduct.py --validate-all
```

### Agent-Specific Usage
```bash
# Route to specific agent
python prompttoproduct.py --agent spec-agent "<spec_prompt>"
python prompttoproduct.py --agent code-agent "<code_prompt>"
python prompttoproduct.py --agent validation-agent "<validation_prompt>"
```

## 🏦 Banking Domain Categories

### 📊 Product Types Supported
- **Loans**: Mortgage, personal, auto, business loans
- **Credit Cards**: Rewards, secured, corporate cards  
- **Payments**: Wire transfers, ACH, mobile payments, P2P
- **Investments**: Portfolio management, trading, robo-advisors
- **Accounts**: Savings, checking, certificates of deposit
- **Digital Banking**: Mobile apps, online platforms, APIs

### 🔒 Compliance Areas Covered
- **Regulatory**: KYC, AML, SOX, GDPR, PCI-DSS, Basel III
- **Security**: Encryption, tokenization, fraud detection
- **Risk Management**: Credit risk, operational risk, stress testing

## 📝 Prompt Categories

### 🎯 **Epic Prompts** (High-Level Initiatives)
For creating comprehensive business initiatives and platform transformations.

### 🔧 **Feature Prompts** (Product Capabilities)  
For creating specific product features with banking domain intelligence.

### 📋 **Story Prompts** (Implementation Tasks)
For creating detailed user stories and technical implementation tasks.

### ✅ **Compliance Prompts** (Regulatory Requirements)
For creating compliance-focused stories and validation requirements.

### 🔍 **System Prompts** (Management & Operations)
For system status, validation, and operational tasks.

## 🎨 Prompt Patterns

### Basic Pattern Structure
```
Action + Subject + Context + Constraints

Examples:
"Create a feature for fraud detection under epic E001"
"Add a compliance story for PCI DSS under feature F002"
"Build a loan origination system with AI risk assessment"
```

### Banking-Specific Patterns
```
Product Type + Process + Technology + Compliance

Examples:
"Create a credit card application system with fraud detection and PCI compliance"
"Build a loan underwriting platform with AI scoring and regulatory reporting"
"Add a payment processing feature with real-time monitoring and AML validation"
```

## 🔗 Cross-References

Each prompt in this library includes:
- **Category**: Epic/Feature/Story/Compliance/System
- **Banking Domain**: Product type and compliance area
- **Expected Output**: What files/artifacts will be generated
- **Dependencies**: Required parent specs or external references
- **Validation**: How to verify successful completion

## 📊 Usage Analytics

Track your most effective prompts:
- **Success Rate**: Prompts that generate complete, valid specs
- **Reusability**: Prompts that work across different contexts
- **Compliance Coverage**: Prompts that address regulatory requirements
- **Integration Success**: Prompts that generate properly linked hierarchies

---

**Getting Started**: Begin with the `examples/` directory for complete workflow demonstrations, then explore category-specific prompts in `banking/` and `system/` directories.