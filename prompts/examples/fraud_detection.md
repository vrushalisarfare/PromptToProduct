# Complete Fraud Detection Workflow Examples

End-to-end examples demonstrating the complete PromptToProduct workflow for building fraud detection systems in banking applications.

## 🚨 Complete Fraud Detection Platform

### Epic Creation Example
**Prompt:**
```
"Create an epic for enterprise-wide real-time fraud detection platform"
```

**Expected Output:**
- Epic file: `specs/epics/E003-Enterprise-Fraud-Detection-Platform.md`
- Banking domain: Fraud Detection & Security
- Compliance requirements: PCI DSS, AML, KYC
- Success criteria: Real-time detection, ML-powered scoring, regulatory compliance

**Generated Epic Structure:**
```markdown
# Epic: Enterprise-Wide Real-Time Fraud Detection Platform
**ID:** E003
**Objective:** Build comprehensive fraud detection across all banking channels
**Owner:** Security & Risk Management Team
**Banking Domain:** Fraud Detection & Security
**Compliance Requirements:** PCI DSS, AML, KYC, SOX
**Linked Features:** TBD

### Business Context
Implement enterprise-wide fraud detection to protect customers and reduce financial losses across all banking products and channels.

### Success Criteria
- Detect fraud within 100ms of transaction initiation
- Achieve 99%+ accuracy with <0.1% false positive rate
- Cover 100% of transaction types and channels
- Meet all regulatory compliance requirements
```

### Feature Development Examples

#### Feature 1: Real-Time Transaction Monitoring
**Prompt:**
```
"Add a feature for real-time transaction monitoring with ML fraud scoring under epic E003"
```

**Expected Output:**
- Feature file: `specs/features/F007-Real-Time-Transaction-Monitoring.md`
- Product type: Fraud Detection
- Integration points: Core banking, ML platform, alert system
- Compliance: AML transaction monitoring

#### Feature 2: Behavioral Analytics Engine
**Prompt:**
```
"Create a feature for customer behavioral analytics and anomaly detection under epic E003"
```

**Expected Output:**
- Feature file: `specs/features/F008-Behavioral-Analytics-Engine.md`
- Product type: Customer Analytics
- Technical requirements: ML models, pattern recognition, baseline profiling
- Security: Privacy protection, data encryption

#### Feature 3: Multi-Channel Fraud Prevention
**Prompt:**
```
"Add a feature for multi-channel fraud prevention across mobile, web, and ATM under epic E003"
```

**Expected Output:**
- Feature file: `specs/features/F009-Multi-Channel-Fraud-Prevention.md`
- Product type: Channel Security
- Integration points: Mobile app, web platform, ATM network
- Compliance: PCI DSS, device authentication

### Story Implementation Examples

#### Transaction Velocity Monitoring
**Prompt:**
```
"Create a story for transaction velocity monitoring algorithm under feature F007"
```

**Expected Output:**
- Story file: `specs/stories/S021-Transaction-Velocity-Monitoring.md`
- Implementation: Real-time velocity calculations
- Acceptance criteria: Configurable thresholds, real-time alerts
- Technical tasks: Algorithm development, database optimization

#### Device Fingerprinting
**Prompt:**
```
"Add a story for device fingerprinting and risk scoring under feature F009"
```

**Expected Output:**
- Story file: `specs/stories/S022-Device-Fingerprinting.md`
- Implementation: Device identification and risk assessment
- Security requirements: Data protection, secure storage
- Integration: Multi-channel device registry

#### ML Model Training Pipeline
**Prompt:**
```
"Create a story for ML model training and deployment pipeline under feature F008"
```

**Expected Output:**
- Story file: `specs/stories/S023-ML-Model-Training-Pipeline.md`
- Implementation: Automated model training and deployment
- Performance requirements: Model accuracy, latency targets
- Compliance: Model governance, audit trail

### Compliance Implementation Examples

#### AML Transaction Monitoring
**Prompt:**
```
"Create a compliance story for AML suspicious transaction detection under feature F007"
```

**Expected Output:**
- Compliance story: `specs/stories/S024-AML-Suspicious-Transaction-Detection.md`
- Regulation: Anti-Money Laundering (AML)
- Controls: Suspicious activity monitoring, SAR filing
- Audit trail: Transaction logging, investigation workflow

#### PCI DSS Data Protection
**Prompt:**
```
"Add a compliance story for PCI DSS payment data protection under feature F009"
```

**Expected Output:**
- Compliance story: `specs/stories/S025-PCI-DSS-Payment-Data-Protection.md`
- Regulation: Payment Card Industry Data Security Standard
- Controls: Data encryption, tokenization, secure storage
- Validation: Security testing, compliance certification

## 🔄 Complete Workflow Execution

### Step 1: Epic Creation
```bash
python prompttoproduct.py "Create an epic for enterprise-wide real-time fraud detection platform"
```

### Step 2: Feature Development
```bash
python prompttoproduct.py "Add a feature for real-time transaction monitoring with ML fraud scoring under epic E003"
python prompttoproduct.py "Create a feature for customer behavioral analytics and anomaly detection under epic E003"
python prompttoproduct.py "Add a feature for multi-channel fraud prevention across mobile, web, and ATM under epic E003"
```

### Step 3: Story Implementation
```bash
python prompttoproduct.py "Create a story for transaction velocity monitoring algorithm under feature F007"
python prompttoproduct.py "Add a story for device fingerprinting and risk scoring under feature F009"
python prompttoproduct.py "Create a story for ML model training and deployment pipeline under feature F008"
```

### Step 4: Compliance Integration
```bash
python prompttoproduct.py "Create a compliance story for AML suspicious transaction detection under feature F007"
python prompttoproduct.py "Add a compliance story for PCI DSS payment data protection under feature F009"
```

### Step 5: Code Generation
```bash
python prompttoproduct.py --agent code-agent "Implement fraud detection models from story S023"
python prompttoproduct.py --agent code-agent "Generate transaction monitoring API from story S021"
```

### Step 6: Validation & Deployment
```bash
python prompttoproduct.py --validate-all
python prompttoproduct.py --agent validation-agent "validate fraud detection compliance"
python prompttoproduct.py --sync-github
```

## 📊 Expected Generated Artifacts

### Specification Files
```
specs/
├── epics/
│   └── E003-Enterprise-Fraud-Detection-Platform.md
├── features/
│   ├── F007-Real-Time-Transaction-Monitoring.md
│   ├── F008-Behavioral-Analytics-Engine.md
│   └── F009-Multi-Channel-Fraud-Prevention.md
└── stories/
    ├── S021-Transaction-Velocity-Monitoring.md
    ├── S022-Device-Fingerprinting.md
    ├── S023-ML-Model-Training-Pipeline.md
    ├── S024-AML-Suspicious-Transaction-Detection.md
    └── S025-PCI-DSS-Payment-Data-Protection.md
```

### Generated Code Structure
```
src/MyBank/fraud_detection/
├── __init__.py
├── fraud_detector.py           # Main fraud detection engine
├── transaction_monitor.py      # Real-time transaction monitoring
├── behavioral_analytics.py     # Customer behavior analysis
├── device_fingerprint.py       # Device identification and scoring
├── ml_models/
│   ├── velocity_model.py       # Transaction velocity detection
│   ├── anomaly_model.py        # Behavioral anomaly detection
│   └── risk_scorer.py          # Combined risk scoring
├── compliance/
│   ├── aml_monitor.py          # AML compliance monitoring
│   └── pci_controls.py         # PCI DSS security controls
└── tests/
    ├── test_fraud_detector.py
    ├── test_transaction_monitor.py
    └── test_compliance.py
```

## ✅ Success Metrics

### Specification Quality
- [ ] All specs properly linked (E003 → F007/F008/F009 → S021-S025)
- [ ] Banking domain properly classified (Fraud Detection)
- [ ] Compliance requirements mapped (AML, PCI DSS, SOX)
- [ ] Technical requirements detailed and implementable
- [ ] Acceptance criteria clear and testable

### Code Quality
- [ ] Fraud detection algorithms implemented
- [ ] Real-time monitoring capabilities functional
- [ ] ML models trained and deployable
- [ ] Compliance controls implemented
- [ ] Integration points properly configured

### Compliance Validation
- [ ] AML monitoring controls operational
- [ ] PCI DSS security requirements met
- [ ] Audit trails comprehensive and accurate
- [ ] Regulatory reporting capabilities functional
- [ ] Security testing completed successfully

## 🔗 Integration Points

This example demonstrates:
- **Orchestrator**: Prompt routing and banking domain classification
- **SpecAgent**: Fraud detection domain intelligence and compliance mapping
- **CodeAgent**: ML model implementation and security control development
- **ValidationAgent**: Compliance testing and security validation

---

**Next Steps**: Adapt this pattern for other banking domains like credit cards or loan processing using similar workflow patterns.