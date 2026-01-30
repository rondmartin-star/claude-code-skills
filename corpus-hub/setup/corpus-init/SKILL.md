# Corpus Init - Initialize New Projects as Corpus-Enabled

## Purpose

This skill initializes brand-new projects as corpus-enabled from scratch. It creates the directory structure, generates `corpus-config.json` with smart defaults, and registers the project with CorpusHub—all through interactive prompts.

**Use this skill when:**
- Starting a new project that will use CorpusHub
- Setting up a greenfield documentation system
- Creating a new software project with structured docs
- Initializing a research/writing project with version control

**Don't use this skill for:**
- Converting existing projects (use `corpus-convert` instead)
- Projects that already have `corpus-config.json` (unless reinitializing)

---

## Workflow Overview

```
User: "Initialize corpus for my project" or "Enable CorpusHub"
↓
1. Ask if user wants to enable CorpusHub (OPT-OUT QUESTION)
   → If "No", stop here
2. Detect project location (current directory or ask)
3. Ask project name (default: directory name)
4. Ask project type (Software/Documentation/Research/Requirements)
5. Generate corpus-config.json with smart defaults
6. Create directory structure (corpus/, docs/, etc.)
7. Register with CorpusHub via API
8. Switch to newly created corpus
9. Update README.md with corpus info
10. Report success + next steps
```

**Total time:** 2-3 minutes with user input

---

## Interactive Prompts

### Step 1: Opt-Out Question (MOST IMPORTANT)

**Corpus-enablement is OPT-OUT by default.** The first question determines whether to proceed.

```
❓ Enable CorpusHub for this project?

CorpusHub provides:
  • Review and commenting on documentation
  • Consistency checking across artifacts
  • AI-assisted content generation
  • Change plan management with approval workflows
  • Version control integration

Options:
  ✅ Yes - enable CorpusHub (Recommended)
  ❌ No - skip corpus features

Default: Yes
```

**If user selects "No":**
```
✅ Project initialized without CorpusHub

You can enable CorpusHub later by running:
  "corpus convert"

or

  "corpus init" (to try again)
```

**Stop here. Do NOT create any corpus files.**

---

### Step 2: Project Name

```
❓ What is your project name?

Default: [directory name]
Example: "My Application Project"

Validation:
  • Non-empty
  • Max 64 characters
  • Will be slugified for corpus slug
```

---

### Step 3: Project Type

```
❓ What type of project is this?

Options:
  1. Software Application (code + documentation)
     → Creates: requirements/, design/, api/, architecture/, decisions/
     → Framework terms: quality-attributes, design-patterns

  2. Documentation Only (specs, guides, references)
     → Creates: specs/, guides/, references/
     → No code directories

  3. Research/Writing (articles, papers, reports)
     → Creates: research/, drafts/, publications/
     → Framework terms: research-methods

  4. Requirements Management (user stories, acceptance criteria)
     → Creates: requirements/, stories/, acceptance/
     → Framework terms: requirement-types

Default: Software Application

❓ Which option fits your project best? [1-4]
```

---

### Step 4: Corpus Directory Location

```
❓ Where should corpus files be stored?

Default: corpus/
Example: corpus/ or .corpus/ or docs/corpus/

The corpus directory will contain:
  • HTML versions of all documentation
  • Generated from source files (traditional mode)
  • OR direct edits (corpus mode)

Validation: Relative path from project root
```

---

### Step 5: Existing Directories

```
❓ Do you have existing documentation directories?

Options:
  • Yes - I'll specify custom paths
  • No - create standard structure (Recommended)

Default: No

If "Yes", ask for each artifact type's path.
If "No", create directories based on project type.
```

---

### Step 6: Consistency Checking

```
❓ Enable consistency checking?

Consistency checking helps maintain terminology across your corpus.

Options:
  • Yes - with domain term suggestions (Recommended)
  • No - I'll add terms manually later

Default: Yes

If "Yes", framework terms will be suggested based on project type.
```

---

## Smart Defaults by Project Type

### Type 1: Software Application

**Directory Structure:**
```
my-project/
├── corpus-config.json
├── corpus/                    # Generated corpus files
├── docs/
│   ├── requirements/
│   ├── design/
│   ├── api/
│   ├── architecture/
│   └── decisions/             # Architecture Decision Records
├── src/                       # User's code (not created by this skill)
└── README.md
```

**corpus-config.json:**
```json
{
  "corpus": {
    "name": "My Application Project",
    "description": "Artifact corpus for the My Application Project",
    "version": "1.0.0",
    "baseDir": "."
  },
  "artifacts": {
    "requirements": {
      "path": "docs/requirements",
      "label": "Requirements",
      "extensions": [".md", ".html"]
    },
    "design": {
      "path": "docs/design",
      "label": "Design Documents",
      "extensions": [".md", ".html"]
    },
    "api-specs": {
      "path": "docs/api",
      "label": "API Specifications",
      "extensions": [".md", ".yaml", ".json", ".openapi"]
    },
    "architecture": {
      "path": "docs/architecture",
      "label": "Architecture",
      "extensions": [".md", ".html"]
    },
    "decisions": {
      "path": "docs/decisions",
      "label": "Architecture Decisions (ADRs)",
      "extensions": [".md"]
    }
  },
  "framework": {
    "categories": [
      {
        "id": "quality-attributes",
        "label": "Quality Attributes",
        "terms": [
          "scalability", "reliability", "security", "performance",
          "maintainability", "availability", "usability"
        ],
        "matchMode": "word-boundary"
      },
      {
        "id": "design-patterns",
        "label": "Design Patterns",
        "terms": [
          "microservices", "event-driven", "layered architecture",
          "repository pattern", "CQRS", "API gateway"
        ],
        "matchMode": "case-insensitive"
      }
    ]
  },
  "voice": null,
  "roles": {
    "available": ["admin", "editor", "viewer", "pending"],
    "defaultRole": "pending",
    "aiAccess": ["admin", "editor"],
    "editAccess": ["admin", "editor"]
  },
  "consistency": {
    "enabled": true
  }
}
```

---

### Type 2: Documentation Only

**Directory Structure:**
```
my-docs/
├── corpus-config.json
├── corpus/
├── specs/
├── guides/
├── references/
└── README.md
```

**corpus-config.json:**
```json
{
  "corpus": {
    "name": "My Documentation",
    "description": "Documentation corpus",
    "version": "1.0.0",
    "baseDir": "."
  },
  "artifacts": {
    "specifications": {
      "path": "specs",
      "label": "Specifications",
      "extensions": [".md", ".html"]
    },
    "guides": {
      "path": "guides",
      "label": "Guides",
      "extensions": [".md", ".html"]
    },
    "references": {
      "path": "references",
      "label": "References",
      "extensions": [".md", ".html"]
    }
  },
  "framework": null,
  "voice": null,
  "roles": {
    "available": ["admin", "editor", "viewer", "pending"],
    "defaultRole": "pending"
  },
  "consistency": { "enabled": false }
}
```

---

### Type 3: Research/Writing

**Directory Structure:**
```
my-research/
├── corpus-config.json
├── corpus/
├── research/
├── drafts/
├── publications/
└── README.md
```

**corpus-config.json:**
```json
{
  "corpus": {
    "name": "My Research Project",
    "description": "Research project corpus",
    "version": "1.0.0",
    "baseDir": "."
  },
  "artifacts": {
    "research": {
      "path": "research",
      "label": "Research Notes",
      "extensions": [".md", ".html"]
    },
    "drafts": {
      "path": "drafts",
      "label": "Draft Papers",
      "extensions": [".md", ".html", ".docx"]
    },
    "publications": {
      "path": "publications",
      "label": "Published Papers",
      "extensions": [".md", ".html", ".pdf"]
    }
  },
  "framework": {
    "categories": [
      {
        "id": "research-methods",
        "label": "Research Methods",
        "terms": [
          "qualitative analysis", "quantitative analysis",
          "case study", "survey", "experiment"
        ]
      }
    ]
  },
  "voice": null,
  "consistency": { "enabled": true }
}
```

---

### Type 4: Requirements Management

**Directory Structure:**
```
my-requirements/
├── corpus-config.json
├── corpus/
├── requirements/
├── stories/
├── acceptance/
└── README.md
```

**corpus-config.json:**
```json
{
  "corpus": {
    "name": "My Requirements",
    "description": "Requirements management corpus",
    "version": "1.0.0",
    "baseDir": "."
  },
  "artifacts": {
    "requirements": {
      "path": "requirements",
      "label": "Requirements",
      "extensions": [".md", ".html"]
    },
    "stories": {
      "path": "stories",
      "label": "User Stories",
      "extensions": [".md", ".html"]
    },
    "acceptance": {
      "path": "acceptance",
      "label": "Acceptance Criteria",
      "extensions": [".md", ".html"]
    }
  },
  "framework": {
    "categories": [
      {
        "id": "requirement-types",
        "label": "Requirement Types",
        "terms": [
          "functional requirement", "non-functional requirement",
          "user story", "acceptance criteria", "business rule"
        ]
      }
    ]
  },
  "consistency": { "enabled": true }
}
```

---

## Implementation Steps

### 1. Check Prerequisites

```bash
# Verify CorpusHub server is running
curl http://localhost:3000/api/health

# If not running:
echo "CorpusHub server is not running. Please start it with:"
echo "cd \"G:\\My Drive\\Projects\\CorpusHub\" && npm start"
exit 1
```

### 2. Detect Project Location

Use current working directory or ask user:
```bash
PROJECT_DIR=$(pwd)
echo "Project location: $PROJECT_DIR"
```

### 3. Check for Existing Configuration

```bash
if [ -f "$PROJECT_DIR/corpus-config.json" ]; then
  echo "⚠️  This project already has corpus-config.json"
  echo ""
  echo "What would you like to do?"
  echo "  1. Overwrite (creates new config)"
  echo "  2. Upgrade (preserves existing, adds new features)"
  echo "  3. Cancel"

  # Handle user choice
fi
```

### 4. Create Directory Structure

Based on project type, create directories:

```bash
mkdir -p "$PROJECT_DIR/corpus"
mkdir -p "$PROJECT_DIR/docs/requirements"
mkdir -p "$PROJECT_DIR/docs/design"
mkdir -p "$PROJECT_DIR/docs/api"
mkdir -p "$PROJECT_DIR/docs/architecture"
mkdir -p "$PROJECT_DIR/docs/decisions"
```

### 5. Generate corpus-config.json

Write the appropriate template to `corpus-config.json`:

```javascript
const fs = require('fs');
const config = generateConfigForProjectType(projectType, projectName);
fs.writeFileSync(
  path.join(PROJECT_DIR, 'corpus-config.json'),
  JSON.stringify(config, null, 2)
);
```

### 6. Register with CorpusHub

```bash
curl -X POST http://localhost:3000/api/corpora/register \
  -H "Content-Type: application/json" \
  -d "{\"path\": \"$PROJECT_DIR\"}"
```

Expected response:
```json
{
  "success": true,
  "slug": "my-application-project",
  "message": "Corpus registered successfully"
}
```

### 7. Switch to New Corpus

```bash
curl -X POST http://localhost:3000/api/corpora/switch \
  -H "Content-Type: application/json" \
  -d "{\"slug\": \"my-application-project\"}"
```

### 8. Verify Active Corpus

```bash
curl http://localhost:3000/api/corpora/active
```

Expected response:
```json
{
  "name": "My Application Project",
  "slug": "my-application-project",
  "baseDir": "/path/to/project"
}
```

### 9. Update README.md (If Exists)

Append corpus information section to README:

```markdown
## CorpusHub Integration

This project uses [CorpusHub](http://localhost:3000) for documentation management.

**Corpus:** My Application Project
**Slug:** `my-application-project`

### Getting Started with CorpusHub

1. Start the server:
   ```bash
   cd "G:\My Drive\Projects\CorpusHub"
   npm start
   ```

2. Browse to: http://localhost:3000

3. Switch to this corpus if not active:
   - Click corpus dropdown in header
   - Select "My Application Project"

### Workflows

- **Review documentation:** Use reviewer role
- **Edit artifacts:** Use editor role
- **Create new content:** Use author role
- **Manage system:** Use admin role

### Corpus Configuration

Configuration file: `corpus-config.json`
Artifact directories: `docs/requirements/`, `docs/design/`, `docs/api/`, etc.
Corpus HTML: `corpus/`
```

---

## Success Report

After successful initialization, display:

```
✅ Corpus initialized successfully!

Corpus: "My Application Project"
Slug: "my-application-project"
Database: data/corpora/my-application-project.db

Created:
  📁 docs/requirements/
  📁 docs/design/
  📁 docs/api/
  📁 docs/architecture/
  📁 docs/decisions/
  📁 corpus/
  📄 corpus-config.json
  📝 README.md (updated)

Registered with CorpusHub: ✅
Active corpus: ✅

Next Steps:
  1. Start adding documentation files to docs/ directories
  2. Browse to http://localhost:3000
  3. Begin reviewing/editing your corpus

Example: Create your first requirement
  echo "# User Authentication" > docs/requirements/authentication.md
  echo "" >> docs/requirements/authentication.md
  echo "Users must be able to log in with email and password." >> docs/requirements/authentication.md

Then refresh CorpusHub to see it appear!

Useful Commands:
  • View artifacts: GET /api/artifacts
  • Add comment: Use reviewer role in UI
  • Create change plan: Group comments and generate
  • Run consistency scan: Use admin role
```

---

## Error Handling

### Error: CorpusHub Server Not Running

```
❌ Cannot connect to CorpusHub server

The server is not responding at http://localhost:3000

To start the server:
  cd "G:\My Drive\Projects\CorpusHub"
  npm start

Then try again.
```

**Recovery:** Wait for user to start server, retry

---

### Error: corpus-config.json Already Exists

```
⚠️  corpus-config.json already exists in this project

What would you like to do?

Options:
  1. Overwrite - Delete existing config and create new
  2. Upgrade - Keep existing, add new features
  3. Cancel - Exit without changes

[1-3]?
```

**Recovery:** Follow user's choice

---

### Error: Permission Denied

```
❌ Permission denied writing to: /path/to/project

Cannot create directories or files.

Solutions:
  • Run with elevated permissions (sudo/admin)
  • Check directory ownership
  • Choose a different project location

Try again? [Y/n]
```

**Recovery:** Ask user to fix permissions or change location

---

### Error: Invalid Project Name

```
❌ Invalid project name: ""

Project name:
  • Must not be empty
  • Max 64 characters
  • Will become corpus slug (alphanumeric + hyphens)

Please enter a valid project name:
```

**Recovery:** Re-prompt for project name

---

### Error: Duplicate Corpus Name

```
❌ A corpus with this name already exists

Slug "my-application-project" is already registered.

Suggestions:
  • Use different project name: "My Application Project v2"
  • Unregister existing corpus first
  • Or switch to existing corpus

What would you like to do?
  1. Enter different name
  2. Switch to existing corpus
  3. Cancel

[1-3]?
```

**Recovery:** Follow user's choice

---

## References

**Detailed information:**
- Project type detection: See `references/project-types.md`
- Full template examples: See `references/templates.md`

**Related skills:**
- Convert existing projects: `corpus-convert`
- Review artifacts: `reviewer`
- Edit artifacts: `editor`

**API Endpoints:**
- Register corpus: `POST /api/corpora/register`
- Switch corpus: `POST /api/corpora/switch`
- Check active: `GET /api/corpora/active`
- Health check: `GET /api/health`

---

## Tips

1. **Use defaults:** For standard projects, accept all defaults for quickest setup

2. **Consistency checking:** Enable by default - helps maintain terminology

3. **Project type matters:** Choose carefully as it determines directory structure

4. **Opt-out available:** If you're not ready for corpus features, select "No" on first question

5. **Re-initialize anytime:** Run corpus-init again to upgrade or reconfigure

6. **README integration:** The corpus info added to README helps other developers

7. **Empty directories OK:** It's fine to create directories with no files yet

8. **Version control:** Commit corpus-config.json to git for team sharing
