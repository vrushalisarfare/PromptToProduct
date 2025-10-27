# PromptToProduct Schema System

This directory contains the **PromptToProduct Schema** system that enables natural language prompts to be automatically converted into structured specifications (Epics, Features, and Stories).

## 🎯 Overview

The PromptToProduct Schema reads from `../prompt_schema.json` and provides intelligent parsing of developer prompts to create properly structured and linked specifications.

## 📁 Directory Structure

```
specs/
├── epics/          # Epic specifications (E001, E002, ...)
├── features/       # Feature specifications (F001, F002, ...)
├── stories/        # Story specifications (S001, S002, ...)
├── schema_processor.py  # Core schema processing logic
├── prompt_cli.py   # Command-line interface
└── README.md       # This file
```

## 🚀 Usage

### Command Line Interface

```bash
# Show current status
python prompt_cli.py --status

# Validate all spec links
python prompt_cli.py --validate

# Create specifications via natural language
python prompt_cli.py "Create an epic for user authentication system"
python prompt_cli.py "Add a feature for login validation under epic E001"
python prompt_cli.py "Create a story for password encryption under feature F001"
```

### Example Prompts

**Epic Creation:**
- "Create an epic for microservices architecture"
- "Add an epic for data analytics platform"

**Feature Creation:**
- "Add a feature for real-time notifications under epic E001"
- "Create a feature for user profile management under epic E002"

**Story Creation:**
- "Create a story for API authentication under feature F001"
- "Add a story for database optimization under feature F002"

## 📋 Schema Actions

The system supports these actions based on `prompt_schema.json`:

1. **create_epic** - Creates new Epic specifications
2. **create_feature** - Creates Feature specs linked to Epics
3. **create_story** - Creates Story specs linked to Features
4. **update_spec** - Updates existing specifications
5. **validate_links** - Validates hierarchical linkage

## 🔗 Hierarchical Structure

```
Epic (E001)
├── Feature (F001)
│   ├── Story (S001)
│   └── Story (S002)
└── Feature (F002)
    ├── Story (S003)
    └── Story (S004)
```

## 🧠 Intelligent Parsing

The schema processor intelligently parses prompts by:

- **Action Detection**: Identifies whether to create epic/feature/story
- **Context Extraction**: Extracts titles, parent references, and technical details
- **Link Resolution**: Automatically links to parent specs (Epic → Feature → Story)
- **ID Generation**: Generates sequential IDs (E001, F001, S001, etc.)

## ✅ Validation

The system validates:
- All features are linked to valid epics
- All stories are linked to valid features  
- No orphaned specifications exist
- Proper ID sequencing and format

## 🔧 Integration

### With MCP Server
The schema processor integrates with the MCP server for:
- GitHub repository operations
- Automated spec creation and updates
- VS Code integration via Copilot

### With VS Code
- Use through MCP tools in Copilot
- Direct CLI usage in integrated terminal
- File creation and validation

## 🎨 Generated Specification Format

Each generated spec follows a consistent format:

**Epic Template:**
```markdown
# Epic: Title
**ID:** E001
**Objective:** Goal description
**Owner:** Responsible person
**Linked Features:** F001, F002

### Business Context
### Success Criteria
```

**Feature Template:**
```markdown
# Feature: Title
**ID:** F001
**Epic:** E001
**Linked Stories:** S001, S002

### Goal
### Technical Requirements
### Acceptance Criteria
```

**Story Template:**
```markdown
# Story: Title
**ID:** S001
**Feature:** F001

### Acceptance Criteria
### Tasks
### Definition of Done
```

## 🔄 Workflow Example

1. **Input**: `"Create a feature for user authentication under epic E001"`
2. **Processing**: 
   - Parse action: `create_feature`
   - Extract title: `"user authentication"`
   - Extract parent: `"E001"`
3. **Output**: `features/F002-user-authentication.md` with proper linking

## 📊 Status Monitoring

Use `python prompt_cli.py --status` to see:
- Total count of epics, features, stories
- Current ID ranges
- Orphaned specifications
- Link validation status

## 🛠️ Development

The schema system is built using:
- **Python 3.7+** - Core processing logic
- **JSON Schema** - Configuration and validation
- **Regex Parsing** - Natural language interpretation
- **File I/O** - Markdown specification generation

## 🚨 Error Handling

The system handles:
- Invalid prompt formats
- Missing parent specifications
- File creation errors
- ID conflicts and resolution

---

**Working Directory**: Set to `PromptToProduct/specs` for proper operation
**Schema File**: `../prompt_schema.json`
**Generated**: Via PromptToProduct Schema System