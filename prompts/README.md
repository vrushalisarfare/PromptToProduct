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
│   └── validation.md           # Validation and testing prompts
├── examples/                    # Complete workflow examples
│   ├── credit_cards.md         # Credit card system examples
│   └── fraud_detection.md      # Fraud detection examples
```

## 🚀 Quick Start

### Basic Usage
```
# Direct prompt usage - system handles routing automatically
"Create an epic for digital loan origination platform"

# System status check
"Check system status"

# Validate all specs
"Validate all specifications"
```

### Agent-Specific Usage
The system automatically routes prompts to the appropriate agent based on prompt content and intent. Here are examples for each agent type:

#### SpecAgent Examples (Requirements & Architecture)
```
# Epic creation
"Create an epic for digital loan origination platform with AI-powered risk assessment"

# Feature specification
"Add a feature for real-time fraud detection in credit card transactions under epic E001"

# User story creation
"Create a story for KYC document verification API under feature F005"

# Compliance requirements
"Create a compliance story for PCI DSS tokenization requirements under feature F003"
```

#### CodeAgent Examples (Implementation & Development)
```
# API implementation
"Implement REST API for loan application submission with validation"

# Database schema
"Create database schema for customer onboarding with KYC compliance"

# Frontend component
"Build React component for credit card application form with real-time validation"

# Integration code
"Implement payment gateway integration for ACH transfers with fraud monitoring"
```

#### ValidationAgent Examples (Testing & Quality Assurance)
```
# Test suite creation
"Create comprehensive test suite for loan approval workflow"

# Security validation
"Validate PCI compliance for payment processing implementation"

# Performance testing
"Create performance tests for high-volume transaction processing"

# Integration testing
"Validate API integration between fraud detection and payment systems"
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

## 🎨 Prompt Patterns & Templates

All prompt patterns and templates are integrated directly into each category file:
- **Epic patterns** in `banking/epics.md`
- **Feature patterns** in `banking/features.md` 
- **Story patterns** in `banking/stories.md`
- **Compliance patterns** in `banking/compliance.md`
- **System patterns** in `system/status.md` and `system/validation.md`

### ⚡ Quick Prompt Patterns

#### Epic Creation
```
"Create an epic for [business_initiative] [banking_domain]"
"Add an epic for [technology_transformation] [product_area]"
```

#### Feature Development  
```
"Add a feature for [capability] [product_type] under epic [ID]"
"Create a feature for [technology] [banking_process] with [compliance]"
```

#### Story Implementation
```
"Create a story for [implementation_task] under feature [ID]"
"Add a story for [technical_component] [integration] under feature [ID]"
```

#### Compliance & Security
```
"Create a compliance story for [regulation] [requirement] under feature [ID]"
"Add a compliance story for [security_control] [validation] under feature [ID]"
```

#### System Operations
```
"Check [component] status"
"Validate [scope] [criteria]"
"Show [metrics] [timeframe]"
```

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

## 🎯 Example Quick Workflow

### Epic → Feature → Story Creation
```
# 1. Create an epic
"Create an epic for digital loan origination platform"

# 2. Add features to the epic
"Add a feature for AI credit scoring under epic E005"  
"Add a feature for automated document verification under epic E005"

# 3. Create implementation stories
"Create a story for ML model training under feature F014"
"Create a story for API integration under feature F015"

# 4. Add compliance requirements
"Create a compliance story for KYC verification under feature F015"

# 5. Validate the complete workflow
"Validate all specifications and implementations"
```

---

**Getting Started**: Begin with the `examples/` directory for complete workflow demonstrations, then explore category-specific prompts in `banking/` and `system/` directories.