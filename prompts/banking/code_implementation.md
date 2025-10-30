# Code Implementation Banking Prompts

Code implementation prompts for generating production-ready banking code using the CodeAgent. These prompts leverage the spec-driven development framework and banking domain intelligence.

## 🌐 API Implementation Prompts

### Core Banking APIs
```
"Implement account management API with real-time balance updates"
"Generate loan origination API with automated underwriting workflow"
"Build payment processing API with fraud detection integration"
"Create customer onboarding API with KYC compliance automation"
"Implement transaction history API with audit trail capabilities"
```

### Security & Fraud APIs
```
"Implement fraud detection API with real-time scoring capabilities"
"Generate authentication API with multi-factor verification"
"Build tokenization API for PCI DSS payment security"
"Create risk assessment API with ML-powered scoring"
"Implement device fingerprinting API for transaction security"
```

### Compliance & Reporting APIs
```
"Generate AML monitoring API with suspicious activity detection"
"Implement regulatory reporting API with automated data aggregation"
"Build audit trail API with immutable transaction logging"
"Create KYC verification API with document processing"
"Generate compliance dashboard API with real-time metrics"
```

## 🗄️ Database Schema Implementation

### Core Banking Schemas
```
"Create database schema for customer accounts with encryption at rest"
"Generate transaction tables with audit trail for AML compliance"
"Build loan management schema with automated workflow states"
"Implement credit card schema with tokenization and security"
"Create investment portfolio schema with real-time valuation"
```

### Compliance & Security Schemas
```
"Generate KYC document storage schema with GDPR compliance"
"Create fraud detection schema with real-time scoring tables"
"Build regulatory reporting schema with automated aggregation"
"Implement audit trail schema with immutable logging"
"Generate compliance monitoring schema with alert management"
```

## 🔗 Integration Code Implementation

### Core Banking Integrations
```
"Implement core banking system integration with error handling"
"Generate payment gateway integration with retry logic"
"Build credit bureau integration with real-time scoring"
"Create regulatory reporting integration with automated submission"
"Implement third-party API integration with rate limiting"
```

### Security & Monitoring Integrations
```
"Generate fraud detection integration with real-time alerts"
"Build authentication integration with SSO and MFA"
"Implement monitoring integration with anomaly detection"
"Create compliance integration with automated validation"
"Generate audit integration with immutable logging"
```

## 💻 Frontend Code Implementation

### Customer-Facing Components
```
"Build loan application form with real-time validation"
"Create account dashboard with transaction history"
"Implement payment interface with tokenization security"
"Generate investment portfolio with real-time updates"
"Build mobile banking interface with biometric authentication"
```

### Administrative Components
```
"Create fraud investigation dashboard with case management"
"Build compliance monitoring interface with alert management"
"Implement risk assessment dashboard with ML insights"
"Generate regulatory reporting interface with automated exports"
"Create audit trail viewer with search and filtering"
```

## 🎯 Spec-Driven Implementation Patterns

### Pattern 1: Specification-Based Implementation
```
"Implement [System] based on [Specification_Type] [ID]"

Examples:
- "Implement payment gateway based on epic E028"
- "Generate fraud detection code based on feature F003"
- "Build API endpoints based on stories S021-S025"
```

### Pattern 2: Banking Product Implementation
```
"Implement [Banking_Product] [Component] with [Technology] and [Compliance]"

Examples:
- "Implement credit card processing API with tokenization and PCI DSS"
- "Generate loan underwriting service with ML scoring and regulatory compliance"
- "Build payment system with real-time fraud detection and AML monitoring"
```

### Pattern 3: Complete System Implementation
```
"Build complete [System] with [Architecture] for [Banking_Domain]"

Examples:
- "Build complete fraud detection system with microservices for transaction monitoring"
- "Create complete loan platform with API-first architecture for digital lending"
- "Implement complete payment gateway with cloud-native design for real-time processing"
```

### Pattern 4: Integration-Focused Implementation
```
"Implement [Integration] between [System_A] and [System_B] with [Requirements]"

Examples:
- "Implement integration between core banking and fraud detection with real-time alerts"
- "Create integration between loan origination and credit bureau with automated scoring"
- "Build integration between payment processing and compliance monitoring with audit trails"
```

## 📊 Expected Code Outputs

### API Implementation Structure
```python
# Generated API structure example
src/MyBank/api/
├── authentication/
│   ├── auth_api.py          # Authentication endpoints
│   ├── mfa_service.py       # Multi-factor authentication
│   └── session_manager.py   # Session management
├── payments/
│   ├── payment_api.py       # Payment processing endpoints
│   ├── fraud_detector.py    # Real-time fraud detection
│   └── tokenization.py     # PCI DSS tokenization
├── loans/
│   ├── origination_api.py   # Loan application endpoints
│   ├── underwriting.py     # Automated underwriting
│   └── risk_assessment.py  # ML-powered risk scoring
└── compliance/
    ├── kyc_api.py          # KYC verification endpoints
    ├── aml_monitor.py      # AML monitoring service
    └── audit_trail.py     # Audit logging service
```

### Database Schema Structure
```sql
-- Generated database schema example
CREATE SCHEMA banking_core;
CREATE SCHEMA compliance;
CREATE SCHEMA fraud_detection;

-- Customer accounts with encryption
CREATE TABLE banking_core.accounts (
    account_id UUID PRIMARY KEY,
    customer_id UUID NOT NULL,
    account_type VARCHAR(50) NOT NULL,
    balance_encrypted BYTEA NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Transaction audit trail
CREATE TABLE compliance.transaction_audit (
    audit_id UUID PRIMARY KEY,
    transaction_id UUID NOT NULL,
    account_id UUID NOT NULL,
    amount_encrypted BYTEA NOT NULL,
    audit_trail JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## ✅ Implementation Quality Standards

Code implementation prompts should generate:
- [ ] Production-ready code with proper error handling
- [ ] Banking-specific security controls and encryption
- [ ] Compliance requirements implementation (KYC, AML, PCI DSS)
- [ ] Real-time processing capabilities where required
- [ ] Comprehensive logging and audit trail functionality
- [ ] API documentation and testing frameworks
- [ ] Database optimization for high-volume transactions
- [ ] Integration patterns with external banking systems

## 🔗 Framework Integration

Code implementation prompts integrate with:
- **CodeAgent**: Direct code generation with banking intelligence
- **SpecAgent**: Specification-driven implementation guidance  
- **ValidationAgent**: Code quality and compliance validation
- **LangGraph Orchestration**: Multi-phase implementation coordination

---

**Usage**: These prompts work best when specifications already exist. Use spec-driven workflow to create specifications first, then implement code based on those specifications.