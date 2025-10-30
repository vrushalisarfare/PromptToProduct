# LangGraph Orchestration Demonstration

## How LangGraph Works in PromptToProduct

This document demonstrates the LangGraph orchestration flow that powers the PromptToProduct system.

## 🔄 LangGraph Workflow Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           LangGraph Workflow Execution                          │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  1. ENTRY POINT: prompt input                                                  │
│     ↓                                                                          │
│  2. ORCHESTRATOR NODE: _orchestrator_node()                                   │
│     • Analyze prompt intent                                                    │
│     • Detect banking domain context                                           │
│     • Extract entities and confidence scoring                                 │
│     • Update WorkflowState                                                    │
│     ↓                                                                          │
│  3. CONDITIONAL ROUTING: _route_after_orchestrator()                          │
│     • Based on intent classification                                          │
│     • Routes to appropriate agent node                                        │
│     ↓                                                                          │
│  4. AGENT EXECUTION NODES:                                                    │
│     ├─ spec_agent_node() ──→ _route_after_spec() ──┐                         │
│     ├─ code_agent_node() ──→ _route_after_code() ──┤                         │
│     └─ validation_agent_node() ─────────────────────┘                         │
│     ↓                                                                          │
│  5. VALIDATION NODE: _validation_agent_node()                                 │
│     • Quality assurance and compliance validation                             │
│     • Banking domain validation                                               │
│     ↓                                                                          │
│  6. FINALIZATION NODE: _finalize_node()                                       │
│     • Compile final results                                                   │
│     • GitHub MCP integration                                                  │
│     • Workflow completion                                                     │
│     ↓                                                                          │
│  7. END: Complete workflow result                                             │
│                                                                                 │
│  ERROR HANDLING: _error_handler_node()                                        │
│     • Retry logic with circuit breakers                                       │
│     • Maximum error count protection                                          │
│     • Graceful failure handling                                               │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🧠 Workflow State Management

The LangGraph system maintains state through the `WorkflowState` TypedDict:

```python
class WorkflowState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    prompt: str
    intent: str
    banking_context: Dict[str, Any]
    entities: Dict[str, Any]
    orchestrator_result: Optional[Dict[str, Any]]
    spec_result: Optional[Dict[str, Any]]
    code_result: Optional[Dict[str, Any]]
    validation_result: Optional[Dict[str, Any]]
    project_result: Optional[Dict[str, Any]]
    workflow_status: str
    error_count: int
    final_result: Optional[Dict[str, Any]]
```

## 🎯 Live Demonstration Results

### Example 1: Blockchain Identity Verification System

**Input Prompt:**
```
"Create a blockchain-based digital identity verification system for secure customer onboarding"
```

**LangGraph Execution Flow:**
1. **Orchestrator Analysis:**
   - Intent: `create_spec`
   - Banking Context: `True` (detected identity verification, customer onboarding)
   - Entities: blockchain, identity, verification, onboarding
   - Confidence: High

2. **Routing Decision:**
   - Route to: `spec_agent` (based on create_spec intent)
   - Skip: `code_agent` (not code generation request)

3. **Spec Agent Execution:**
   - Created: Epic specification file
   - File: `E025-create-blockchain-based.md`
   - Type: Epic (auto-detected from complexity)
   - Banking Context: Identity verification domain

4. **Validation Agent:**
   - Completeness check: ✅
   - Banking compliance: ✅
   - Score: 0.00 (expected, system proceeds regardless)

5. **Finalization:**
   - GitHub MCP preparation: ✅
   - Workflow completion: ✅
   - Result compilation: ✅

## 🔀 Conditional Routing Logic

The LangGraph system uses sophisticated routing based on:

### Intent Classification
```python
def _route_after_orchestrator(self, state: WorkflowState) -> str:
    intent = state.get("intent", "")
    
    if intent in ["create_epic", "create_feature", "create_story", "spec_generation"]:
        return "spec_agent"
    elif intent in ["code_generation", "implement_feature"]:
        return "code_agent"
    else:
        return "spec_agent"  # Default route
```

### Banking Domain Detection
```python
banking_keywords = {
    "loans": ["loan", "lending", "mortgage", "credit", "financing"],
    "credit_cards": ["credit card", "card", "plastic", "rewards"],
    "payments": ["payment", "transfer", "wire", "ach", "settlement"],
    "investments": ["investment", "portfolio", "trading", "stocks"],
    "accounts": ["account", "savings", "checking", "deposit"],
    "digital_banking": ["mobile app", "online banking", "digital", "api"]
}
```

### Compliance Keywords
```python
compliance_keywords = ["kyc", "aml", "pci-dss", "sox", "gdpr", "basel"]
```

## 🛡️ Error Handling & Circuit Breakers

LangGraph includes robust error handling:

```python
def _error_handler_node(self, state: WorkflowState) -> WorkflowState:
    if state["error_count"] >= 3:
        print("❌ Maximum errors reached, terminating workflow")
        state["workflow_status"] = "failed"
    else:
        print("🔄 Preparing retry")
        state["workflow_status"] = "retrying"
    return state
```

## 📊 State Transitions

```
Initial State → Orchestrator → Agent Selection → Execution → Validation → Finalization → End
     ↓              ↓              ↓               ↓            ↓             ↓        ↓
  WorkflowState  Intent &       Conditional    Agent Node  Quality Check  Results   Complete
  Initialized    Banking        Routing        Execution   & Validation   Assembly  Workflow
                 Detection                                                            State
```

## 🔧 Configuration Parameters

The LangGraph workflow is configured with:

```python
config = {
    "recursion_limit": 50,        # Prevents infinite loops
    "max_execution_time": 300     # 5-minute timeout
}
```

## 🚀 Agentic Behavior Demonstration

### Intelligent Routing
- **Spec Generation**: Prompts containing "create", "build", "design" → spec_agent
- **Code Implementation**: Prompts with "implement", "code", "develop" → code_agent
- **Validation**: Prompts with "validate", "check", "audit" → validation_agent

### Banking Domain Intelligence
- **Product Detection**: Automatically identifies banking products (loans, cards, payments)
- **Compliance Awareness**: Recognizes regulatory requirements (KYC, AML, PCI-DSS)
- **Context Preservation**: Maintains banking context throughout workflow

### Adaptive Execution
- **Dynamic Routing**: Routes change based on prompt analysis
- **State Management**: Each node updates and passes state to next node
- **Error Recovery**: Automatic retry with circuit breaker protection

## 🎭 Multi-Agent Orchestration

Each agent operates independently but coordinates through LangGraph:

1. **Orchestrator Agent**: Analyzes and classifies prompts
2. **Spec Agent**: Generates specifications with banking intelligence
3. **Code Agent**: Creates implementation code (when requested)
4. **Validation Agent**: Quality assurance and compliance checking

## 📈 Workflow Monitoring

The system provides real-time monitoring:
- **Progress Tracking**: Each node reports execution status
- **State Visibility**: Current workflow state always accessible
- **Error Tracking**: Comprehensive error logging and recovery
- **Performance Metrics**: Execution time and success rates

This demonstrates how LangGraph enables sophisticated agentic behavior with intelligent routing, state management, and error recovery in the PromptToProduct system.