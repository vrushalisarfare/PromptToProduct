# Compliance-Focused Banking Prompts

Compliance prompts create regulatory-focused stories and validation requirements. These prompts ensure banking applications meet regulatory standards and security requirements.

## 🔒 KYC (Know Your Customer) Compliance

### Customer Verification Stories
```
"Create a compliance story for KYC document verification under feature F001"
"Add a compliance story for identity verification API integration under feature F002"
"Create a compliance story for customer due diligence automation under feature F003"
"Add a compliance story for enhanced due diligence for high-risk customers under feature F004"
"Create a compliance story for beneficial ownership identification under feature F005"
```

### Ongoing Monitoring
```
"Add a compliance story for customer information updates and re-verification under feature F001"
"Create a compliance story for periodic KYC refresh workflow under feature F002"
"Add a compliance story for customer risk rating updates under feature F003"
"Create a compliance story for sanctions screening automation under feature F004"
```

## 🕵️ AML (Anti-Money Laundering) Compliance

### Transaction Monitoring
```
"Create a compliance story for AML transaction monitoring under feature F001"
"Add a compliance story for suspicious activity detection and reporting under feature F002"
"Create a compliance story for currency transaction report (CTR) automation under feature F003"
"Add a compliance story for suspicious activity report (SAR) filing under feature F004"
"Create a compliance story for wire transfer screening and monitoring under feature F005"
```

### Risk Assessment
```
"Add a compliance story for customer risk scoring algorithm under feature F001"
"Create a compliance story for transaction pattern analysis under feature F002"
"Add a compliance story for geographic risk assessment under feature F003"
"Create a compliance story for politically exposed person (PEP) screening under feature F004"
```

## 💳 PCI DSS (Payment Card Industry) Compliance

### Data Security
```
"Create a compliance story for PCI DSS payment data encryption under feature F001"
"Add a compliance story for cardholder data tokenization under feature F002"
"Create a compliance story for secure payment processing environment under feature F003"
"Add a compliance story for payment data access logging and monitoring under feature F004"
```

### Network Security
```
"Add a compliance story for network segmentation for payment systems under feature F001"
"Create a compliance story for firewall configuration for PCI compliance under feature F002"
"Add a compliance story for vulnerability scanning and penetration testing under feature F003"
"Create a compliance story for secure coding practices for payment applications under feature F004"
```

## 📊 SOX (Sarbanes-Oxley) Compliance

### Financial Reporting Controls
```
"Create a compliance story for SOX financial reporting controls under feature F001"
"Add a compliance story for automated control testing and monitoring under feature F002"
"Create a compliance story for change management controls under feature F003"
"Add a compliance story for access control and segregation of duties under feature F004"
```

### Audit Trail Requirements
```
"Add a compliance story for comprehensive audit logging under feature F001"
"Create a compliance story for data retention and archival policies under feature F002"
"Add a compliance story for audit trail integrity and protection under feature F003"
"Create a compliance story for automated compliance reporting under feature F004"
```

## 🛡️ GDPR (General Data Protection Regulation) Compliance

### Data Privacy & Protection
```
"Create a compliance story for GDPR data protection impact assessment under feature F001"
"Add a compliance story for customer consent management system under feature F002"
"Create a compliance story for data subject rights automation under feature F003"
"Add a compliance story for personal data inventory and mapping under feature F004"
```

### Data Breach Management
```
"Add a compliance story for GDPR breach detection and notification under feature F001"
"Create a compliance story for data breach response workflow under feature F002"
"Add a compliance story for regulatory breach reporting automation under feature F003"
"Create a compliance story for customer breach notification system under feature F004"
```

## 🏦 Basel III Risk Management

### Capital Requirements
```
"Create a compliance story for Basel III capital adequacy calculation under feature F001"
"Add a compliance story for risk-weighted asset computation under feature F002"
"Create a compliance story for stress testing and scenario analysis under feature F003"
"Add a compliance story for capital planning and forecasting under feature F004"
```

### Liquidity Management
```
"Add a compliance story for liquidity coverage ratio (LCR) monitoring under feature F001"
"Create a compliance story for net stable funding ratio (NSFR) calculation under feature F002"
"Add a compliance story for liquidity stress testing under feature F003"
"Create a compliance story for funding risk assessment under feature F004"
```

## 🎯 Compliance Prompt Patterns

### Pattern 1: Regulatory Framework Stories
```
"Create a compliance story for [regulation] [specific_requirement] under feature [ID]"

Examples:
- "Create a compliance story for KYC customer verification under feature F001"
- "Create a compliance story for PCI DSS data encryption under feature F002"
- "Create a compliance story for GDPR consent management under feature F003"
```

### Pattern 2: Automated Compliance Monitoring
```
"Add a compliance story for automated [regulation] [monitoring_process] under feature [ID]"

Examples:
- "Add a compliance story for automated AML transaction screening under feature F001"
- "Add a compliance story for automated SOX control testing under feature F002"
- "Add a compliance story for automated GDPR breach detection under feature F003"
```

### Pattern 3: Reporting & Documentation
```
"Create a compliance story for [regulation] [reporting_requirement] under feature [ID]"

Examples:
- "Create a compliance story for AML suspicious activity reporting under feature F001"
- "Create a compliance story for SOX compliance documentation under feature F002"
- "Create a compliance story for Basel III regulatory reporting under feature F003"
```

### Pattern 4: Risk Assessment & Controls
```
"Add a compliance story for [risk_type] [assessment_control] under feature [ID]"

Examples:
- "Add a compliance story for credit risk assessment controls under feature F001"
- "Add a compliance story for operational risk monitoring under feature F002"
- "Add a compliance story for market risk measurement under feature F003"
```

## 📊 Expected Outputs

### Compliance Story Structure
Each compliance prompt generates:
```markdown
# Compliance Story: [Regulation] - [Requirement]
**ID:** S###
**Feature:** F###
**Regulation:** [KYC/AML/PCI-DSS/SOX/GDPR/Basel III]
**Risk Level:** [High/Medium/Low]
**Compliance Officer:** [Assigned person]

### Regulatory Requirement
[Specific regulation citation and requirement]

### Business Context
[Why this compliance requirement matters]

### Acceptance Criteria
- [ ] Regulatory requirement implementation
- [ ] Control effectiveness validation
- [ ] Audit trail completeness
- [ ] Reporting accuracy
- [ ] Exception handling

### Compliance Validation
- [ ] Regulatory testing requirements
- [ ] Control design effectiveness
- [ ] Operating effectiveness testing
- [ ] Documentation requirements
- [ ] Regulatory reporting

### Risk Mitigation
- [ ] Risk identification and assessment
- [ ] Control implementation
- [ ] Monitoring and alerting
- [ ] Escalation procedures
- [ ] Remediation processes

### Audit Trail Requirements
- [ ] Data retention policies
- [ ] Access logging
- [ ] Change management records
- [ ] Approval workflows
- [ ] Regular compliance reviews
```

## ✅ Validation Criteria

Compliance prompts should result in:
- [ ] Clear regulatory requirement identification
- [ ] Specific compliance controls implementation
- [ ] Comprehensive audit trail requirements
- [ ] Risk assessment and mitigation strategies
- [ ] Regulatory reporting capabilities
- [ ] Exception handling and escalation procedures
- [ ] Regular monitoring and review processes

## 🔗 Integration Points

Compliance prompts integrate with:
- **SpecAgent**: Regulatory requirement mapping and compliance story generation
- **ValidationAgent**: Compliance testing and audit trail validation
- **Banking Schema**: Regulatory framework and requirement mapping
- **CodeAgent**: Compliance control implementation

---

**Next Steps**: Implement compliance stories through CodeAgent or validate existing compliance using ValidationAgent.