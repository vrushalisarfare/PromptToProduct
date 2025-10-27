# Quick Reference: PromptToProduct Prompts

## 🚀 Getting Started

```bash
# Check system status first
python prompttoproduct.py --status

# Use any prompt from the library
python prompttoproduct.py "<prompt_from_library>"

# Validate results
python prompttoproduct.py --validate-all
```

## 📚 Prompt Categories

### 🏦 Banking Domain (`prompts/banking/`)
- **epics.md**: High-level business initiatives and platform transformations
- **features.md**: Specific banking product capabilities and functionality  
- **stories.md**: Detailed user stories and implementation tasks
- **compliance.md**: Regulatory requirements and compliance controls

### 🔧 System Management (`prompts/system/`)
- **status.md**: System health monitoring and performance metrics
- **validation.md**: Quality assurance and compliance testing

### 💡 Complete Examples (`prompts/examples/`)
- **fraud_detection.md**: End-to-end fraud detection platform workflow
- **credit_cards.md**: Complete credit card system implementation

## ⚡ Quick Prompt Patterns

### Epic Creation
```
"Create an epic for [business_initiative] [banking_domain]"
"Add an epic for [technology_transformation] [product_area]"
```

### Feature Development  
```
"Add a feature for [capability] [product_type] under epic [ID]"
"Create a feature for [technology] [banking_process] with [compliance]"
```

### Story Implementation
```
"Create a story for [implementation_task] under feature [ID]"
"Add a story for [technical_component] [integration] under feature [ID]"
```

### Compliance & Security
```
"Create a compliance story for [regulation] [requirement] under feature [ID]"
"Add a compliance story for [security_control] [validation] under feature [ID]"
```

### System Operations
```
"Check [component] status"
"Validate [scope] [criteria]"
"Show [metrics] [timeframe]"
```

## 🏦 Banking Product Types

- **Loans**: Mortgage, personal, auto, business loans
- **Credit Cards**: Rewards, secured, corporate cards
- **Payments**: Wire transfers, ACH, mobile payments, P2P  
- **Investments**: Portfolio management, trading, robo-advisors
- **Accounts**: Savings, checking, certificates of deposit
- **Digital Banking**: Mobile apps, online platforms, APIs

## 🔒 Compliance Areas

- **KYC**: Customer verification, due diligence, monitoring
- **AML**: Transaction monitoring, suspicious activity reporting
- **PCI DSS**: Payment security, data protection, tokenization
- **SOX**: Financial controls, audit trails, reporting
- **GDPR**: Data privacy, consent management, breach response
- **Basel III**: Risk management, capital requirements, stress testing

## 🎯 Example Workflows

### Quick Epic → Feature → Story
```bash
python prompttoproduct.py "Create an epic for digital loan origination platform"
python prompttoproduct.py "Add a feature for AI credit scoring under epic E005"  
python prompttoproduct.py "Create a story for ML model training under feature F014"
```

### Compliance Implementation
```bash
python prompttoproduct.py "Add a feature for KYC automation under epic E005"
python prompttoproduct.py "Create a compliance story for customer verification under feature F015"
```

### System Validation
```bash
python prompttoproduct.py --status
python prompttoproduct.py --validate-all
python prompttoproduct.py --agent validation-agent "validate banking compliance"
```

---

**💡 Tip**: Start with examples in `prompts/examples/` for complete workflows, then use category-specific prompts for individual components.