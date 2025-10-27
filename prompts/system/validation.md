# Validation & Testing Prompts

Validation prompts ensure quality, consistency, and compliance across all generated specifications and code. These prompts trigger comprehensive testing and validation workflows.

## ✅ Specification Validation

### Comprehensive Validation
```
"Validate all specifications for completeness and consistency"
"Check all spec links and hierarchical integrity"
"Validate banking domain classification across all specs"
"Check compliance requirements coverage across specifications"
"Validate specification ID sequencing and format"
```

### Hierarchy Validation
```
"Validate epic to feature linkage integrity"
"Check feature to story relationship consistency"
"Validate parent-child spec relationships"
"Check for orphaned specifications"
"Validate cross-reference accuracy"
```

### Content Quality Validation
```
"Validate specification content quality and completeness"
"Check acceptance criteria clarity and testability"
"Validate business value articulation"
"Check technical requirement specificity"
"Validate compliance requirement accuracy"
```

## 🏦 Banking Domain Validation

### Product Classification Validation
```
"Validate banking product type classification"
"Check product feature alignment with banking standards"
"Validate compliance requirement mapping accuracy"
"Check regulatory framework coverage"
"Validate risk assessment completeness"
```

### Compliance Validation
```
"Validate KYC compliance story completeness"
"Check AML requirement implementation coverage"
"Validate PCI DSS security control specifications"
"Check SOX audit trail requirement coverage"
"Validate GDPR data protection implementation"
```

### Financial Services Standards
```
"Validate specifications against banking industry standards"
"Check compliance with financial regulations"
"Validate security control implementation"
"Check data governance requirement coverage"
"Validate risk management control specifications"
```

## 🔒 Security & Compliance Testing

### Security Validation
```
"Validate security requirements in all banking features"
"Check encryption and tokenization specifications"
"Validate authentication and authorization controls"
"Check data protection and privacy requirements"
"Validate fraud detection and prevention controls"
```

### Regulatory Compliance Testing
```
"Test KYC compliance story implementation"
"Validate AML transaction monitoring specifications"
"Check PCI DSS payment security requirements"
"Test SOX financial control implementations"
"Validate Basel III risk management specifications"
```

### Audit Trail Validation
```
"Validate audit trail completeness across all specs"
"Check logging and monitoring requirement coverage"
"Validate data retention policy implementation"
"Check compliance reporting specification accuracy"
"Validate regulatory documentation completeness"
```

## 🧪 Quality Assurance Testing

### Acceptance Criteria Testing
```
"Test acceptance criteria clarity and measurability"
"Validate user story testability"
"Check acceptance criteria completeness"
"Test scenario coverage adequacy"
"Validate edge case handling specifications"
```

### Technical Validation
```
"Validate technical architecture specifications"
"Check API design and integration requirements"
"Validate database design specifications"
"Check performance requirement definitions"
"Validate scalability and reliability requirements"
```

### Integration Testing Validation
```
"Validate third-party integration specifications"
"Check core banking system integration requirements"
"Validate payment gateway integration specs"
"Check regulatory reporting system integration"
"Validate data synchronization specifications"
```

## 🎯 Validation Prompt Patterns

### Pattern 1: Comprehensive Validation
```
"Validate [scope] [validation_type] [criteria]"

Examples:
- "Validate all specifications for compliance requirements"
- "Validate banking features for security controls"
- "Validate epic hierarchy for business alignment"
```

### Pattern 2: Specific Component Validation
```
"Check [component] [quality_aspect] [standard]"

Examples:
- "Check acceptance criteria clarity and testability"
- "Check security requirements implementation completeness"
- "Check compliance controls effectiveness"
```

### Pattern 3: Cross-Validation Testing
```
"Validate [relationship] [consistency] [integrity]"

Examples:
- "Validate epic-feature linkage consistency"
- "Validate compliance-security alignment integrity"
- "Validate business-technical requirement consistency"
```

### Pattern 4: Standards Compliance Validation
```
"Test [specification_area] against [standard] [requirement]"

Examples:
- "Test payment features against PCI DSS requirements"
- "Test KYC stories against regulatory standards"
- "Test API specs against banking integration standards"
```

## 📋 Validation Commands

### Main Validation Commands
```bash
# Comprehensive validation
python prompttoproduct.py --validate-all

# Specific validation with verbose output
python prompttoproduct.py --validate-all --verbose

# JSON validation report
python prompttoproduct.py --validate-all --json

# Validation with specific focus
python prompttoproduct.py --agent validation-agent "validate compliance requirements"
```

### Agent-Specific Validation
```bash
# Spec validation
python src/agents/spec_agent.py --validate

# Code validation
python src/agents/code_agent.py --validate

# System validation
python src/agents/validation_agent.py --full-validation

# Banking domain validation
python prompttoproduct.py --agent validation-agent "validate banking domain classifications"
```

## 📊 Expected Validation Outputs

### Comprehensive Validation Report
```
✅ PromptToProduct Validation Report
====================================
Validation Date: 2025-10-27 15:30:00
Scope: All specifications and code
Status: PASSED (2 warnings)

Specification Validation:
✅ Total Specs: 25 validated
✅ Hierarchy Integrity: 100% valid
✅ Link Consistency: 100% accurate
⚠️  Content Quality: 23/25 complete (2 missing acceptance criteria)
✅ ID Sequencing: Valid format

Banking Domain Validation:
✅ Product Classification: 100% accurate
✅ Compliance Mapping: 100% covered
✅ Security Requirements: 98% complete
✅ Risk Assessment: 95% comprehensive
⚠️  Regulatory Alignment: 1 minor gap (Basel III stress testing)

Code Quality Validation:
✅ Syntax: 100% valid
✅ Security Scans: No vulnerabilities
✅ Integration Tests: 95% passing
✅ Banking Standards: Compliant
✅ Documentation: 90% coverage

Compliance Validation:
✅ KYC Implementation: Compliant
✅ AML Controls: Compliant
✅ PCI DSS Security: Compliant
✅ SOX Controls: Compliant
✅ GDPR Privacy: Compliant

Recommendations:
1. Complete acceptance criteria for S012 and S018
2. Add Basel III stress testing specification to E002
3. Increase integration test coverage for payment module
```

### Issue-Specific Validation
```
🔍 Banking Domain Validation Results
====================================
Product Type Classification:
✅ Loans: 8 features correctly classified
✅ Credit Cards: 6 features correctly classified
✅ Payments: 4 features correctly classified
✅ Investments: 3 features correctly classified

Compliance Coverage:
✅ KYC: 100% coverage (5/5 required controls)
✅ AML: 100% coverage (7/7 required controls)
✅ PCI DSS: 95% coverage (19/20 required controls)
⚠️  SOX: 90% coverage (18/20 required controls)
✅ GDPR: 100% coverage (6/6 required controls)

Missing Requirements:
⚠️  PCI DSS: Vulnerability scanning schedule (Control 11.2)
⚠️  SOX: Automated control testing (Control ITGC-04)

Security Controls:
✅ Encryption: Specified in 100% of payment features
✅ Authentication: Specified in 100% of access features
✅ Authorization: Specified in 95% of API features
✅ Audit Logging: Specified in 100% of transaction features
```

## ✅ Validation Checklist

Validation should verify:
- [ ] All specifications have proper ID format and sequencing
- [ ] Hierarchical relationships are valid and complete
- [ ] Banking product classifications are accurate
- [ ] Compliance requirements are properly mapped
- [ ] Security controls are comprehensively specified
- [ ] Acceptance criteria are clear and testable
- [ ] Technical requirements are implementable
- [ ] Integration points are well-defined
- [ ] Audit trails are complete
- [ ] Regulatory standards are met

## 🔗 Integration Points

Validation prompts integrate with:
- **ValidationAgent**: Quality assurance and compliance testing
- **SpecAgent**: Specification content and structure validation
- **CodeAgent**: Technical implementation validation
- **Banking Schema**: Regulatory and compliance standard validation

---

**Next Steps**: Use deployment prompts for system operations or address validation findings through corrective actions.