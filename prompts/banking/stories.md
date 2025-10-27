# Story-Level Banking Prompts

Story prompts create detailed user stories and implementation tasks linked to features. These prompts generate actionable development tasks with specific acceptance criteria.

## 👤 User Story Prompts

### Account Management Stories
```
"Create a story for API authentication under feature F001"
"Add a story for biometric login implementation under feature F002"
"Create a story for account balance inquiry API under feature F003"
"Add a story for transaction history retrieval under feature F004"
"Create a story for account closure workflow under feature F005"
```

### Transaction Processing Stories
```
"Add a story for real-time payment validation under feature F001"
"Create a story for transaction settlement processing under feature F002"
"Add a story for payment retry logic implementation under feature F003"
"Create a story for transaction receipt generation under feature F004"
"Add a story for failed payment notification system under feature F005"
```

### Customer Onboarding Stories
```
"Create a story for KYC document verification API under feature F001"
"Add a story for identity verification service integration under feature F002"
"Create a story for customer risk profiling algorithm under feature F003"
"Add a story for automated account setup workflow under feature F004"
"Create a story for welcome message and tutorial system under feature F005"
```

## 🔒 Security & Fraud Stories

### Authentication & Authorization
```
"Add a story for multi-factor authentication implementation under feature F001"
"Create a story for OAuth 2.0 integration for third-party access under feature F002"
"Add a story for session management and timeout handling under feature F003"
"Create a story for role-based access control (RBAC) under feature F004"
```

### Fraud Detection Stories
```
"Create a story for transaction velocity monitoring under feature F001"
"Add a story for device fingerprinting implementation under feature F002"
"Create a story for behavioral analytics engine under feature F003"
"Add a story for real-time fraud scoring algorithm under feature F004"
"Create a story for suspicious activity alert system under feature F005"
```

## 💻 Technical Implementation Stories

### API Development Stories
```
"Add a story for REST API endpoint creation under feature F001"
"Create a story for API rate limiting implementation under feature F002"
"Add a story for API documentation generation under feature F003"
"Create a story for API versioning strategy under feature F004"
"Add a story for API error handling and logging under feature F005"
```

### Data Processing Stories
```
"Create a story for real-time data streaming pipeline under feature F001"
"Add a story for batch processing workflow implementation under feature F002"
"Create a story for data validation and cleansing rules under feature F003"
"Add a story for data encryption at rest implementation under feature F004"
"Create a story for audit trail and logging system under feature F005"
```

### Integration Stories
```
"Add a story for core banking system integration under feature F001"
"Create a story for payment gateway API integration under feature F002"
"Add a story for credit bureau data feed integration under feature F003"
"Create a story for regulatory reporting system integration under feature F004"
"Add a story for third-party service webhook handling under feature F005"
```

## 🎯 Story Prompt Patterns

### Pattern 1: User-Centric Stories
```
"Create a story for [user_action] [system_capability] under feature [ID]"

Examples:
- "Create a story for customer account registration under feature F001"
- "Create a story for merchant payment processing under feature F002"
- "Create a story for advisor portfolio review under feature F003"
```

### Pattern 2: Technical Implementation Stories
```
"Add a story for [technical_component] [implementation_detail] under feature [ID]"

Examples:
- "Add a story for API authentication middleware under feature F001"
- "Add a story for database connection pooling under feature F002"
- "Add a story for message queue processing under feature F003"
```

### Pattern 3: Integration Stories
```
"Create a story for [system_integration] [data_flow] under feature [ID]"

Examples:
- "Create a story for core banking data synchronization under feature F001"
- "Create a story for credit bureau API integration under feature F002"
- "Create a story for payment processor webhook handling under feature F003"
```

### Pattern 4: Quality Assurance Stories
```
"Add a story for [testing_type] [system_component] under feature [ID]"

Examples:
- "Add a story for load testing payment API under feature F001"
- "Add a story for security testing authentication flow under feature F002"
- "Add a story for integration testing fraud detection under feature F003"
```

## 📊 Expected Outputs

### Story File Structure
Each story prompt generates:
```markdown
# Story: [Title]
**ID:** S###
**Feature:** F###
**User Type:** [Customer/Admin/System]
**Priority:** [High/Medium/Low]

### User Story
As a [user_type], I want [capability] so that [benefit]

### Acceptance Criteria
- [ ] Specific testable criteria
- [ ] Performance requirements
- [ ] Security requirements
- [ ] Error handling requirements

### Technical Tasks
- [ ] Implementation steps
- [ ] Database changes
- [ ] API modifications
- [ ] Testing requirements

### Definition of Done
- [ ] Code complete and reviewed
- [ ] Unit tests written and passing
- [ ] Integration tests complete
- [ ] Security scan passed
- [ ] Documentation updated
```

### Generated Artifacts
- Story specification file in `specs/stories/`
- Clear acceptance criteria
- Technical implementation tasks
- Testing requirements
- Definition of done checklist

## ✅ Validation Criteria

Story prompts should result in:
- [ ] Clear user value and business justification
- [ ] Specific and testable acceptance criteria
- [ ] Detailed technical implementation tasks
- [ ] Security and compliance considerations
- [ ] Performance and scalability requirements
- [ ] Comprehensive testing strategy
- [ ] Clear definition of done

## 🔗 Integration Points

Story prompts integrate with:
- **SpecAgent**: User story generation and acceptance criteria
- **CodeAgent**: Technical implementation planning
- **ValidationAgent**: Testing strategy and quality assurance
- **Banking Schema**: Product-specific requirements and constraints

---

**Next Steps**: Use compliance prompts for regulatory requirements or implement stories using the CodeAgent for actual development.