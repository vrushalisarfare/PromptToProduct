# Feature-Level Banking Prompts

Feature prompts create specific banking product capabilities linked to epics. These prompts generate detailed features with banking domain intelligence and compliance considerations.

## 💳 Credit Card Features

### Core Functionality
```
"Add a feature for credit card application processing under epic E001"
"Create a feature for real-time fraud detection in credit card transactions"
"Add a feature for rewards points calculation and redemption"
"Create a feature for contactless payment processing"
"Add a feature for credit limit management and automated adjustments"
```

### Advanced Capabilities  
```
"Create a feature for AI-powered spending insights and recommendations"
"Add a feature for dynamic pricing based on customer risk profile"
"Create a feature for virtual card generation for online purchases"
"Add a feature for dispute management and chargeback processing"
```

## 🏠 Loan Processing Features

### Origination & Underwriting
```
"Add a feature for automated loan underwriting using AI under epic E002"
"Create a feature for digital document collection and verification"
"Add a feature for real-time credit scoring and risk assessment"
"Create a feature for loan application status tracking"
"Add a feature for automated approval workflow engine"
```

### Servicing & Management
```
"Create a feature for automated payment processing and collections"
"Add a feature for loan modification and refinancing workflows"
"Create a feature for early payoff calculations and processing"
"Add a feature for delinquency management and workout plans"
```

## 💰 Payment Processing Features

### Real-Time Payments
```
"Create a feature for real-time P2P money transfers"
"Add a feature for instant account-to-account transfers"
"Create a feature for real-time payment settlement and clearing"
"Add a feature for cross-border payment processing with FX conversion"
```

### Payment Security
```
"Create a feature for tokenized payment processing"
"Add a feature for biometric payment authentication"
"Create a feature for transaction velocity monitoring"
"Add a feature for payment anomaly detection and blocking"
```

## 📈 Investment & Wealth Features

### Portfolio Management
```
"Add a feature for robo-advisor portfolio rebalancing under epic E003"
"Create a feature for automated tax-loss harvesting"
"Add a feature for ESG investment screening and reporting"
"Create a feature for risk tolerance assessment and profiling"
```

### Trading & Analytics
```
"Create a feature for real-time market data integration"
"Add a feature for algorithmic trading execution"
"Create a feature for portfolio performance analytics and reporting"
"Add a feature for social trading and copy investing"
```

## 🏦 Account Management Features

### Core Banking
```
"Create a feature for instant account opening and funding"
"Add a feature for real-time balance updates and notifications"
"Create a feature for mobile check deposit with fraud detection"
"Add a feature for automated savings and round-up transfers"
```

### Customer Experience
```
"Create a feature for personalized financial insights dashboard"
"Add a feature for spending categorization and budgeting tools"
"Create a feature for goal-based savings with progress tracking"
"Add a feature for financial health scoring and recommendations"
```

## 🎯 Feature Prompt Patterns

### Pattern 1: Product-Specific Features
```
"Create a feature for [specific_capability] in [product_type] [process]"

Examples:
- "Create a feature for fraud detection in credit card transactions"
- "Create a feature for risk assessment in loan underwriting" 
- "Create a feature for real-time monitoring in payment processing"
```

### Pattern 2: Technology-Enhanced Features
```
"Add a feature for [technology] [banking_capability] under epic [ID]"

Examples:
- "Add a feature for AI-powered fraud detection under epic E001"
- "Add a feature for blockchain payment settlement under epic E002"
- "Add a feature for ML-based credit scoring under epic E003"
```

### Pattern 3: Customer-Centric Features
```
"Create a feature for [customer_experience] [banking_service]"

Examples:
- "Create a feature for instant digital loan applications"
- "Create a feature for personalized investment recommendations"
- "Create a feature for self-service account management"
```

### Pattern 4: Compliance-Enabled Features
```
"Add a feature for [banking_process] with [compliance_requirement] compliance"

Examples:
- "Add a feature for payment processing with AML compliance"
- "Add a feature for data handling with GDPR compliance"
- "Add a feature for transaction monitoring with KYC compliance"
```

## 📊 Expected Outputs

### Feature File Structure
Each feature prompt generates:
```markdown
# Banking Feature: [Title]
**ID:** F###
**Epic:** E###
**Product Type:** [Banking domain]
**Linked Stories:** [Story IDs]

### Goal
### Business Value
### Technical Requirements
### Compliance Requirements
### Security Requirements
### Integration Points
### Acceptance Criteria
```

### Generated Artifacts
- Feature specification file in `specs/features/`
- Banking domain classification
- Product type assignment
- Compliance requirements mapping
- Technical architecture considerations
- Integration point identification

## ✅ Validation Criteria

Feature prompts should result in:
- [ ] Clear business value and customer impact
- [ ] Proper banking product classification
- [ ] Compliance requirements identification
- [ ] Technical feasibility assessment
- [ ] Security considerations
- [ ] Integration requirements
- [ ] Measurable acceptance criteria

## 🔗 Integration Points

Feature prompts integrate with:
- **SpecAgent**: Banking domain intelligence and product classification
- **Banking Schema**: Product types and compliance mapping
- **ValidationAgent**: Technical feasibility and compliance validation
- **CodeAgent**: Implementation architecture planning

---

**Next Steps**: Use story prompts to break down features into specific implementation tasks and user stories.