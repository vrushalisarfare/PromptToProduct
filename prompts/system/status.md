# System Status & Monitoring Prompts

System prompts for monitoring the PromptToProduct 4-Agent System health, performance, and operational status.

## 🚀 System Health Monitoring

### Overall System Status
```
"Check system status"
"Show system health dashboard"
"Display agent operational status"
"Get system performance metrics"
"Show current system configuration"
```

### Agent-Specific Status
```
"Check orchestrator agent status"
"Show spec agent operational health"
"Display code agent current tasks"
"Get validation agent sync status"
"Show agent memory and context status"
```

### Resource Monitoring
```
"Check system resource utilization"
"Show memory usage across agents"
"Display processing queue status"
"Get disk space and file counts"
"Show network connectivity status"
```

## 📊 Specification Status Monitoring

### Specification Inventory
```
"Show total count of epics, features, and stories"
"Display current specification hierarchy"
"Get orphaned specifications report"
"Show specification link validation status"
"Display specification creation timeline"
```

### Banking Domain Analytics
```
"Show banking product distribution across specs"
"Display compliance coverage analysis"
"Get banking domain completeness report"
"Show product type specification coverage"
"Display compliance requirement mapping"
```

### Quality Metrics
```
"Check specification quality scores"
"Show validation failure rates"
"Display spec creation success metrics"
"Get link integrity validation results"
"Show specification approval status"
```

## 🔗 Integration Status Monitoring

### GitHub Integration Health
```
"Check GitHub MCP connection status"
"Show GitHub sync operation results"
"Display repository access permissions"
"Get GitHub API rate limit status"
"Show commit and push operation logs"
```

### VS Code Integration Status
```
"Check VS Code Copilot agent registration"
"Show MCP server connectivity status"
"Display Copilot agent manifest validity"
"Get VS Code extension integration health"
"Show agent routing and classification metrics"
```

### External Service Connectivity
```
"Check banking API integration status"
"Show third-party service connectivity"
"Display payment gateway connection health"
"Get compliance service integration status"
"Show data provider connectivity metrics"
```

## 🎯 System Prompt Patterns

### Pattern 1: Component Status Queries
```
"Check [component] [status_type]"

Examples:
- "Check orchestrator agent status"
- "Check GitHub integration health"
- "Check specification validation status"
```

### Pattern 2: Metric Reporting
```
"Show [metric_category] [time_period]"

Examples:
- "Show system performance last 24 hours"
- "Show specification creation this week"
- "Show validation results today"
```

### Pattern 3: Health Dashboards
```
"Display [system_area] dashboard"

Examples:
- "Display agent health dashboard"
- "Display specification quality dashboard"
- "Display integration status dashboard"
```

### Pattern 4: Diagnostic Reports
```
"Get [diagnostic_type] report"

Examples:
- "Get system diagnostic report"
- "Get specification validation report"
- "Get integration connectivity report"
```

## 📋 System Commands

### Status Check Commands
```bash
# Main system status
python prompttoproduct.py --status

# Individual agent status
python src/agents/orchestrator.py --status
python src/agents/spec_agent.py --status
python src/agents/code_agent.py --status
python src/agents/validation_agent.py --status

# System health with verbose output
python prompttoproduct.py --status --verbose

# JSON formatted status for automation
python prompttoproduct.py --status --json
```

### Performance Monitoring Commands
```bash
# Memory and resource usage
python prompttoproduct.py --system-info

# Processing queue status
python prompttoproduct.py --queue-status

# Session history and memory
python src/agents/orchestrator.py --memory

# Agent performance metrics
python prompttoproduct.py --performance-metrics
```

## 📊 Expected Status Outputs

### System Health Report
```
🚀 PromptToProduct System Status
========================================
Version: 1.0
System Health: operational
Active Agents: orchestrator, spec-agent, code-agent, validation-agent
Sessions: 15 completed, 2 active
Memory Usage: 245MB / 1GB available
Uptime: 2 days, 14 hours

Agent Status:
✅ Orchestrator: operational (routing: 98% success)
✅ Spec Agent: operational (generation: 95% success)
✅ Code Agent: operational (compilation: 92% success)
✅ Validation Agent: operational (sync: 100% success)

Integration Health:
✅ GitHub MCP: connected (API limit: 4,500/5,000)
✅ VS Code Copilot: registered (4 agents active)
⚠️  External APIs: 2/3 connected (1 timeout)

Specification Metrics:
📊 Total Specs: 25 (8 epics, 12 features, 15 stories)
🔗 Link Integrity: 100% valid
🏦 Banking Coverage: 85% (loans: 100%, cards: 75%, payments: 80%)
✅ Validation Status: 23/25 passing (2 warnings)
```

### Agent-Specific Status
```
📋 Spec Agent Status
=====================
Agent ID: spec-agent
Version: 1.0
Status: operational
Uptime: 2 days, 14 hours

Performance Metrics:
- Requests Processed: 45
- Success Rate: 95.5%
- Average Processing Time: 2.3 seconds
- Memory Usage: 78MB

Banking Domain Intelligence:
- Product Types Recognized: 6/6
- Compliance Areas Covered: 8/8
- Schema Processor: active
- Banking Context Success: 98%

Recent Activity:
[2025-10-27 14:30] Created epic E003 (fraud detection)
[2025-10-27 14:25] Generated feature F008 (loan underwriting)
[2025-10-27 14:20] Processed compliance story S015 (KYC)

Errors/Warnings:
⚠️  Schema processor timeout (2 occurrences, auto-recovered)
✅ No critical errors
```

## ✅ Monitoring Checklist

System health monitoring should verify:
- [ ] All agents operational and responsive
- [ ] Memory usage within acceptable limits
- [ ] GitHub MCP connectivity stable
- [ ] VS Code Copilot registration active
- [ ] Specification creation success rate >90%
- [ ] Validation success rate >95%
- [ ] Link integrity 100% valid
- [ ] Banking domain intelligence functioning
- [ ] No critical errors in agent logs
- [ ] External service integrations healthy

## 🔗 Integration Points

Status prompts integrate with:
- **All Agents**: Individual status and health reporting
- **Orchestrator**: System-wide coordination and memory management
- **ValidationAgent**: Quality metrics and validation results
- **GitHub MCP**: Integration health and sync status

---

**Next Steps**: Use validation prompts for quality assurance or deployment prompts for system operations.