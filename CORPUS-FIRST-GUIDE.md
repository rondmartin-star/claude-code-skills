# Corpus-First Guide

**Purpose:** Understand and implement the corpus-first approach
**Version:** v4.0.0
**Date:** 2026-02-14
**Audience:** All Claude Code users

---

## What is Corpus-First?

**Corpus-First** is a design philosophy where **every project is corpus-enabled by default**. This means all projects have structured artifacts, consistent terminology, and integrated knowledge management from the start.

### Core Principle

> "A corpus isn't a special type of project—it's the foundation of every project."

---

## Why Corpus-First?

### Traditional Approach (File-Based)

```
project/
├── src/
├── docs/
├── tests/
└── README.md
```

**Limitations:**
- Files disconnected from meaning
- No terminology consistency
- Limited discoverability
- Manual organization

### Corpus-First Approach

```
project/
├── corpus-config.json    ← Central configuration
├── src/                  ← Artifacts organized by type
├── docs/                 ← Bidirectional sync with CorpusHub
├── tests/
└── .corpus/             ← Metadata & indices
```

**Benefits:**
- Structured knowledge graph
- Enforced terminology consistency
- AI-powered discoverability
- Automatic organization

---

## The Corpus Philosophy

### 1. Everything is an Artifact

**Traditional thinking:**
- "This is just a README file"
- "This is just source code"

**Corpus thinking:**
- "This is a requirements artifact"
- "This is an implementation artifact with explicit purpose"

**Example:**

```json
{
  "artifacts": {
    "requirements": {
      "path": "docs/requirements",
      "label": "Requirements Documents",
      "extensions": [".md"],
      "sourceMode": "corpus"
    },
    "source-code": {
      "path": "src",
      "label": "Source Code",
      "extensions": [".js", ".ts"],
      "sourceMode": "source"
    }
  }
}
```

### 2. Source Modes Define Workflow

Every artifact has a **source mode** that determines where and how it's edited:

| Mode | Edit Location | Source of Truth | Use Case |
|------|---------------|-----------------|----------|
| **corpus** | CorpusHub only | CorpusHub HTML | Requirements, specs, ADRs |
| **source** | IDE (VS Code) | Files in repo | Code, configs, tests |
| **bidirectional** | Either location | Synced both ways | Documentation, guides |

**Example:**
```json
{
  "artifacts": {
    "requirements": {
      "sourceMode": "corpus"    // Edit in CorpusHub
    },
    "source-code": {
      "sourceMode": "source"    // Edit in IDE
    },
    "documentation": {
      "sourceMode": "bidirectional"  // Edit anywhere
    }
  }
}
```

### 3. Framework Terms Enforce Consistency

Define **canonical terms** and their source of truth:

```json
{
  "framework": {
    "categories": [
      {
        "id": "api-terminology",
        "label": "API Terminology",
        "terms": ["REST endpoint", "GraphQL query", "WebSocket connection"],
        "canonicalSource": "api-documentation",
        "matchMode": "word-boundary"
      }
    ]
  }
}
```

**Benefits:**
- Automatic consistency checking
- Prevents terminology drift
- Links terms to definitions
- Guides AI responses

### 4. Voice Attributes Guide AI

Define how AI should write content for your project:

```json
{
  "voice": {
    "promptFile": "docs/writing-style.md",
    "attributes": ["professional", "clear", "concise"],
    "avoid": ["jargon", "passive voice", "ambiguity"],
    "preferredTerms": {
      "user": "member",
      "login": "sign in"
    }
  }
}
```

---

## Getting Started: Three Paths

### Path 1: New Project (Blank Slate)

**Use when:** Starting from scratch

```bash
# 1. Create project directory
mkdir my-project
cd my-project

# 2. Initialize as corpus
claude "Initialize this as a corpus"

# 3. Choose template:
#    - web-app (full-stack web application)
#    - content-corpus (documentation repository)
#    - framework-docs (framework documentation)
#    - windows-app (Windows desktop app)
#    - default (minimal generic)

# 4. Customize corpus-config.json

# 5. Start working
claude "Create new document in requirements"
```

### Path 2: Existing Project (Preserve Content)

**Use when:** Migrating existing project with files

```bash
# 1. In your existing project directory
cd /path/to/existing/project

# 2. Convert to corpus
claude "Convert this to corpus"

# This will:
# - Detect existing files and structure
# - Create corpus-config.json
# - Preserve all existing content
# - Register with CorpusHub (if running)

# 3. Verify structure
claude "Check corpus status"

# 4. Customize configuration
edit corpus-config.json

# 5. Set up source modes
claude "Set documentation to bidirectional mode"
```

### Path 3: Template-Based (Pre-configured)

**Use when:** Project fits a standard pattern

```bash
# 1. Clone template
cp config/templates/web-app.json corpus-config.json

# 2. Update project details
edit corpus-config.json
# - Change name, description, baseDir
# - Adjust artifact paths for your structure

# 3. Initialize
claude "Initialize corpus from config"

# 4. Start working
```

---

## Corpus Configuration Structure

### Minimal Configuration

```json
{
  "corpus": {
    "name": "My Project",
    "description": "Project description",
    "version": "1.0.0",
    "baseDir": "/absolute/path/to/project"
  },
  "artifacts": {
    "documentation": {
      "path": "docs",
      "label": "Documentation",
      "extensions": [".md"],
      "sourceMode": "bidirectional"
    }
  }
}
```

### Complete Configuration

See `CONFIG-REFERENCE.md` for full schema documentation.

---

## Common Workflows

### Creating Content

```bash
# Content automatically routed based on artifact type
claude "Create new requirements document about authentication"

# Respects source mode
# - corpus mode: Opens CorpusHub editor
# - source mode: Creates file in IDE
# - bidirectional mode: Your choice
```

### Reviewing Content

```bash
# Universal review workflow
claude "Review docs/api.md"

# Loads review-edit-author in reviewer mode
# - Read-only view
# - Can add comments
# - No direct edits
```

### Editing Content

```bash
# Universal edit workflow
claude "Edit docs/api.md"

# Respects source mode:
# - corpus: Warning + offer to open CorpusHub
# - source: Direct file edit
# - bidirectional: Edit with auto-sync
```

### Auditing Quality

```bash
# Run consistency audit
claude "Check consistency"

# Validates:
# - Framework terms used correctly
# - Canonical sources followed
# - Cross-references valid
```

---

## Source Mode Best Practices

### Use **corpus** mode when:
- Content is requirements or specifications
- Single source of truth in CorpusHub needed
- Rich HTML formatting required
- Collaborative review workflows important
- Version control at paragraph level needed

**Examples:**
- Product requirements documents
- Architecture decision records (ADRs)
- Technical specifications
- Design documents

### Use **source** mode when:
- Content is code or configuration
- IDE is natural editing environment
- File-based version control essential
- Build/test processes depend on files

**Examples:**
- Source code (`.js`, `.ts`, `.py`, etc.)
- Configuration files (`.json`, `.yaml`, etc.)
- Test files
- Build scripts

### Use **bidirectional** mode when:
- Content bridges code and docs
- Team works in both locations
- Flexibility is valuable
- Sync overhead acceptable

**Examples:**
- API documentation
- User guides
- README files
- Tutorials

---

## Integration with CorpusHub

### When CorpusHub is Running

**Full features:**
- Real-time sync for bidirectional artifacts
- Rich HTML editing for corpus-mode artifacts
- Collaborative comments and reviews
- Advanced search across all artifacts
- AI-powered content generation

### When CorpusHub is Offline

**File-based operations:**
- All source-mode artifacts work normally
- Bidirectional artifacts edit files directly
- Corpus-mode artifacts warn but allow file editing
- Sync happens when CorpusHub starts

**Best practice:** Start CorpusHub before working with corpus-mode artifacts

---

## Terminology Consistency

### Defining Framework Terms

```json
{
  "framework": {
    "categories": [
      {
        "id": "user-terminology",
        "label": "User Terminology",
        "terms": ["member", "contributor", "administrator"],
        "canonicalSource": "requirements",
        "matchMode": "word-boundary"
      },
      {
        "id": "technical-terminology",
        "label": "Technical Terms",
        "terms": ["API endpoint", "database schema", "authentication flow"],
        "canonicalSource": "technical-docs",
        "matchMode": "case-insensitive"
      }
    ]
  }
}
```

### Match Modes

| Mode | Behavior | Example |
|------|----------|---------|
| **word-boundary** | Match whole words only | "user" matches "user" not "username" |
| **case-insensitive** | Ignore case | "API" matches "api", "Api", "API" |
| **exact** | Exact string match | "REST API" only matches "REST API" |

### Enforcing Consistency

```bash
# Run consistency audit
claude "Run consistency audit"

# Finds:
# - Terms not defined in framework
# - Inconsistent terminology usage
# - Missing canonical sources
# - Broken term references
```

---

## Voice Configuration

### Defining Project Voice

```json
{
  "voice": {
    "attributes": [
      "professional",
      "clear",
      "concise",
      "action-oriented"
    ],
    "avoid": [
      "jargon",
      "passive voice",
      "unnecessary complexity"
    ],
    "preferredTerms": {
      "user": "member",
      "click": "select",
      "login": "sign in"
    }
  }
}
```

### Using Voice Guidance

**AI respects voice when:**
- Generating new content
- Editing existing content
- Creating documentation
- Writing commit messages

**Example:**
```bash
claude "Create user guide for authentication"

# AI will:
# - Use "member" instead of "user"
# - Use "sign in" instead of "login"
# - Write professionally and clearly
# - Avoid jargon
```

---

## Multi-Methodology Audits

### Configuring Audits

```json
{
  "audit": {
    "methodology": "multi-methodology-3-3-1",
    "applicable_audits": [
      "consistency",
      "navigation",
      "security",
      "quality",
      "performance"
    ],
    "convergence": {
      "enabled": true,
      "automated": {
        "max_iterations": 10,
        "required_clean_passes": 3
      },
      "user_validation": {
        "required": true
      }
    }
  }
}
```

### Running Convergence

```bash
# Start convergence audit
claude "Run convergence audit"

# Process:
# 1. Automated convergence (3 clean passes required)
# 2. User validation (only after automation succeeds)
# 3. Grade improvement (F → A proven in 5 hours for CorpusHub)
```

---

## Real-World Examples

### Example 1: Documentation Repository

**Use case:** Open source project documentation

```json
{
  "corpus": {
    "name": "Framework Documentation",
    "description": "Complete framework documentation",
    "version": "1.0.0"
  },
  "artifacts": {
    "guides": {
      "path": "guides",
      "extensions": [".md"],
      "sourceMode": "corpus"
    },
    "api-docs": {
      "path": "api",
      "extensions": [".md"],
      "sourceMode": "bidirectional"
    }
  },
  "framework": {
    "categories": [{
      "id": "framework-terms",
      "terms": ["component", "directive", "service"],
      "canonicalSource": "guides"
    }]
  }
}
```

### Example 2: Full-Stack Web App

**Use case:** Modern web application

```json
{
  "corpus": {
    "name": "Web Application",
    "description": "Full-stack web app",
    "version": "2.0.0"
  },
  "artifacts": {
    "requirements": {
      "path": "docs/requirements",
      "sourceMode": "corpus"
    },
    "source-code": {
      "path": "src",
      "extensions": [".js", ".jsx", ".ts", ".tsx"],
      "sourceMode": "source"
    },
    "documentation": {
      "path": "docs",
      "sourceMode": "bidirectional"
    }
  },
  "audit": {
    "applicable_audits": ["security", "quality", "performance"]
  }
}
```

### Example 3: Windows Desktop App

**Use case:** Enterprise Windows application

```json
{
  "corpus": {
    "name": "Operations Hub",
    "description": "Windows operations management",
    "version": "1.0.0"
  },
  "artifacts": {
    "source-code": {
      "path": "app",
      "extensions": [".cs", ".xaml"],
      "sourceMode": "source"
    },
    "installers": {
      "path": "installers",
      "extensions": [".wxs"],
      "sourceMode": "source"
    }
  },
  "development": {
    "platform": "windows",
    "packaging": "msi"
  }
}
```

---

## Best Practices

### Configuration

1. **Start with a template** - Don't build from scratch
2. **Use absolute paths** - For `baseDir` field
3. **Be specific** - Clear artifact labels and descriptions
4. **Plan source modes** - Think about workflows before choosing
5. **Define terms early** - Framework consistency from day 1

### Workflows

1. **Let skills auto-load** - Use intent-based loading, not manual
2. **Respect source modes** - Don't fight the configured workflow
3. **Run audits regularly** - Catch inconsistencies early
4. **Use CorpusHub** - When applicable, leverage full features
5. **Document voice** - Define and maintain writing standards

### Team Collaboration

1. **Share corpus-config.json** - Version control this file
2. **Train team** - Ensure everyone understands source modes
3. **Establish terms** - Build framework terms as team
4. **Review together** - Use collaborative review workflows
5. **Iterate configuration** - Refine as project evolves

---

## Troubleshooting

### "Project not corpus-enabled"

**Solution:**
```bash
claude "Initialize this as a corpus"
```

### "Can't edit corpus-mode artifact"

**Solution:**
```bash
# Start CorpusHub first
"C:\Program Files\CorpusHub\CorpusHub.exe"
```

### "Inconsistent terminology detected"

**Solution:**
```json
// Add term to framework
{
  "framework": {
    "categories": [{
      "terms": ["your-term-here"]
    }]
  }
}
```

---

## Next Steps

1. **Initialize your project** - Choose initialization path above
2. **Customize configuration** - Adapt template to your needs
3. **Define framework terms** - Establish terminology
4. **Set up audits** - Configure applicable audit types
5. **Start working** - Create, review, and iterate

---

## Additional Resources

- **CONFIG-REFERENCE.md** - Complete schema documentation
- **MIGRATION-v3-to-v4.md** - Migration from v3.0
- **ARCHITECTURE-v4.md** - Architecture overview
- **config/templates/** - Pre-built configuration templates
- **config/examples/** - Real-world examples

---

**Corpus-First = Better Knowledge Management from Day 1** 🚀

---

**Last Updated:** 2026-02-14
**Version:** v4.0.0
**Status:** Complete guide
