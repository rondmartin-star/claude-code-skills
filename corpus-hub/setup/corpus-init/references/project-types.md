# Project Types - Detailed Detection and Configuration

This reference provides in-depth information about the four supported project types in corpus-init, including detection heuristics, directory structures, and configuration variations.

---

## Type 1: Software Application

### Description
Projects that combine source code with technical documentation. Typical for web applications, APIs, microservices, desktop applications, and mobile apps.

### Detection Heuristics

Detect software projects by looking for:
- `src/`, `lib/`, `app/`, `server/`, `client/` directories
- `package.json`, `pom.xml`, `build.gradle`, `Cargo.toml`, `go.mod`
- `.git`, `.gitignore` (version control)
- `test/`, `tests/`, `__tests__/` (testing infrastructure)
- Code file extensions: `.js`, `.ts`, `.py`, `.java`, `.go`, `.rs`, `.cpp`

### Standard Directory Structure

```
my-app/
├── corpus-config.json
├── corpus/                         # Generated corpus HTML
├── docs/                           # Documentation source
│   ├── requirements/               # Functional/non-functional requirements
│   ├── design/                     # System design documents
│   ├── api/                        # API specifications (OpenAPI, etc.)
│   ├── architecture/               # Architecture diagrams and descriptions
│   └── decisions/                  # Architecture Decision Records (ADRs)
├── src/                            # Application source code
├── tests/                          # Test suite
├── package.json                    # Dependencies
└── README.md
```

### Artifact Types

| Type | Path | Extensions | Purpose |
|------|------|-----------|---------|
| requirements | `docs/requirements/` | `.md`, `.html` | Functional and non-functional requirements |
| design | `docs/design/` | `.md`, `.html` | System design documents |
| api-specs | `docs/api/` | `.md`, `.yaml`, `.json`, `.openapi` | API endpoint specifications |
| architecture | `docs/architecture/` | `.md`, `.html` | High-level architecture |
| decisions | `docs/decisions/` | `.md` | Architecture Decision Records |

### Framework Terms

**Quality Attributes:**
- scalability
- reliability
- security
- performance
- maintainability
- availability
- usability
- testability

**Design Patterns:**
- microservices architecture
- event-driven architecture
- layered architecture
- repository pattern
- CQRS
- API gateway pattern
- circuit breaker
- saga pattern

### Voice Guidelines (Optional)

Software projects typically don't need voice guidelines unless creating customer-facing documentation.

### Variations

**Microservices Project:**
```json
{
  "artifacts": {
    "requirements": { "path": "docs/requirements", "extensions": [".md"] },
    "api-specs": { "path": "docs/api", "extensions": [".yaml", ".openapi"] },
    "architecture": { "path": "docs/architecture", "extensions": [".md"] },
    "decisions": { "path": "docs/decisions", "extensions": [".md"] },
    "runbooks": { "path": "docs/runbooks", "extensions": [".md"] }
  },
  "framework": {
    "categories": [
      {
        "id": "services",
        "label": "Services",
        "terms": ["user-service", "auth-service", "payment-service"],
        "matchMode": "case-insensitive"
      }
    ]
  }
}
```

**Mobile App Project:**
```json
{
  "artifacts": {
    "requirements": { "path": "docs/requirements", "extensions": [".md"] },
    "design": { "path": "docs/design", "extensions": [".md"] },
    "screens": { "path": "docs/screens", "extensions": [".md", ".figma"] },
    "architecture": { "path": "docs/architecture", "extensions": [".md"] }
  },
  "framework": {
    "categories": [
      {
        "id": "platforms",
        "label": "Platforms",
        "terms": ["iOS", "Android", "cross-platform"],
        "matchMode": "case-insensitive"
      }
    ]
  }
}
```

---

## Type 2: Documentation Only

### Description
Pure documentation projects with no source code. Typical for product documentation, user guides, knowledge bases, and specification repositories.

### Detection Heuristics

Detect documentation projects by:
- Presence of `docs/`, `documentation/`, `wiki/` directories
- Absence of code directories (`src/`, `lib/`)
- Mostly `.md`, `.html`, `.rst` files
- May have `mkdocs.yml`, `docusaurus.config.js`, `sphinx.conf`

### Standard Directory Structure

```
my-docs/
├── corpus-config.json
├── corpus/
├── specs/                          # Technical specifications
├── guides/                         # How-to guides and tutorials
├── references/                     # Reference documentation
└── README.md
```

### Artifact Types

| Type | Path | Extensions | Purpose |
|------|------|-----------|---------|
| specifications | `specs/` | `.md`, `.html` | Technical specs |
| guides | `guides/` | `.md`, `.html` | User guides and tutorials |
| references | `references/` | `.md`, `.html` | Reference documentation |

### Framework Terms

Typically not needed for documentation-only projects unless enforcing terminology consistency.

### Variations

**Product Documentation:**
```json
{
  "artifacts": {
    "getting-started": { "path": "getting-started", "extensions": [".md"] },
    "user-guides": { "path": "user-guides", "extensions": [".md"] },
    "api-reference": { "path": "api-reference", "extensions": [".md"] },
    "troubleshooting": { "path": "troubleshooting", "extensions": [".md"] },
    "faqs": { "path": "faqs", "extensions": [".md"] }
  }
}
```

**Knowledge Base:**
```json
{
  "artifacts": {
    "articles": { "path": "articles", "extensions": [".md", ".html"] },
    "how-to": { "path": "how-to", "extensions": [".md"] },
    "concepts": { "path": "concepts", "extensions": [".md"] },
    "glossary": { "path": "glossary", "extensions": [".md"] }
  },
  "framework": {
    "categories": [
      {
        "id": "product-terms",
        "label": "Product Terminology",
        "terms": ["product-name", "feature-a", "feature-b"],
        "matchMode": "case-insensitive"
      }
    ]
  }
}
```

---

## Type 3: Research/Writing

### Description
Academic research projects, writing projects, or document repositories for papers, reports, and publications.

### Detection Heuristics

Detect research projects by:
- Directories like `research/`, `papers/`, `publications/`, `drafts/`
- Academic file types: `.tex`, `.bib`, `.docx`, `.pdf`
- Bibliography management files
- Absence of code infrastructure

### Standard Directory Structure

```
my-research/
├── corpus-config.json
├── corpus/
├── research/                       # Research notes and literature reviews
├── drafts/                         # Work-in-progress papers
├── publications/                   # Published or submitted papers
├── data/                           # (optional) Research data
└── README.md
```

### Artifact Types

| Type | Path | Extensions | Purpose |
|------|------|-----------|---------|
| research | `research/` | `.md`, `.html` | Research notes, lit reviews |
| drafts | `drafts/` | `.md`, `.html`, `.docx` | Draft papers |
| publications | `publications/` | `.md`, `.html`, `.pdf` | Published work |

### Framework Terms

**Research Methods:**
- qualitative analysis
- quantitative analysis
- case study
- survey
- experiment
- literature review
- systematic review

**Paper Sections:**
- introduction
- methodology
- results
- discussion
- conclusion

### Variations

**Dissertation Project:**
```json
{
  "artifacts": {
    "proposal": { "path": "proposal", "extensions": [".md", ".docx"] },
    "literature-review": { "path": "literature-review", "extensions": [".md"] },
    "chapters": { "path": "chapters", "extensions": [".md", ".docx"] },
    "appendices": { "path": "appendices", "extensions": [".md"] }
  },
  "framework": {
    "categories": [
      {
        "id": "theories",
        "label": "Theoretical Frameworks",
        "terms": ["theory-a", "theory-b", "framework-c"],
        "matchMode": "case-insensitive"
      }
    ]
  }
}
```

**Blog/Writing Project:**
```json
{
  "artifacts": {
    "drafts": { "path": "drafts", "extensions": [".md"] },
    "published": { "path": "published", "extensions": [".md", ".html"] },
    "series": { "path": "series", "extensions": [".md"] }
  }
}
```

---

## Type 4: Requirements Management

### Description
Dedicated requirements repositories, user story backlogs, or specification databases.

### Detection Heuristics

Detect requirements projects by:
- Directories like `requirements/`, `stories/`, `acceptance/`
- Agile terminology in file names
- Structured requirement formats
- Lack of implementation code

### Standard Directory Structure

```
my-requirements/
├── corpus-config.json
├── corpus/
├── requirements/                   # High-level requirements
├── stories/                        # User stories
├── acceptance/                     # Acceptance criteria
├── business-rules/                 # (optional) Business rules
└── README.md
```

### Artifact Types

| Type | Path | Extensions | Purpose |
|------|------|-----------|---------|
| requirements | `requirements/` | `.md`, `.html` | Functional/non-functional requirements |
| stories | `stories/` | `.md`, `.html` | User stories |
| acceptance | `acceptance/` | `.md`, `.html` | Acceptance criteria |

### Framework Terms

**Requirement Types:**
- functional requirement
- non-functional requirement
- user story
- acceptance criteria
- business rule
- technical constraint

**Agile Terms:**
- epic
- feature
- sprint
- backlog
- story points

### Variations

**Agile Product Backlog:**
```json
{
  "artifacts": {
    "epics": { "path": "epics", "extensions": [".md"] },
    "stories": { "path": "stories", "extensions": [".md"] },
    "tasks": { "path": "tasks", "extensions": [".md"] },
    "acceptance": { "path": "acceptance", "extensions": [".md"] }
  },
  "framework": {
    "categories": [
      {
        "id": "story-types",
        "label": "Story Types",
        "terms": ["user story", "technical story", "spike", "bug fix"],
        "matchMode": "case-insensitive"
      },
      {
        "id": "personas",
        "label": "User Personas",
        "terms": ["admin user", "end user", "power user"],
        "matchMode": "case-insensitive"
      }
    ]
  }
}
```

**Enterprise Requirements:**
```json
{
  "artifacts": {
    "business-requirements": { "path": "business-requirements", "extensions": [".md"] },
    "functional-requirements": { "path": "functional-requirements", "extensions": [".md"] },
    "technical-requirements": { "path": "technical-requirements", "extensions": [".md"] },
    "constraints": { "path": "constraints", "extensions": [".md"] }
  },
  "framework": {
    "categories": [
      {
        "id": "stakeholders",
        "label": "Stakeholders",
        "terms": ["business owner", "product manager", "technical lead"],
        "matchMode": "case-insensitive"
      }
    ]
  }
}
```

---

## Choosing the Right Type

### Decision Tree

```
Does the project have source code?
├─ Yes → Type 1: Software Application
└─ No ↓

Is it primarily research/academic writing?
├─ Yes → Type 3: Research/Writing
└─ No ↓

Is it focused on requirements/stories?
├─ Yes → Type 4: Requirements Management
└─ No → Type 2: Documentation Only
```

### Mixed Projects

If a project doesn't fit neatly into one type, choose the **primary focus** and customize:

**Example: Software + Research (prototype)**
- Choose Type 1 (Software Application)
- Add research artifact type:
  ```json
  {
    "artifacts": {
      "requirements": { "path": "docs/requirements", "extensions": [".md"] },
      "design": { "path": "docs/design", "extensions": [".md"] },
      "research-notes": { "path": "research", "extensions": [".md"] },
      "api-specs": { "path": "docs/api", "extensions": [".yaml"] }
    }
  }
  ```

**Example: Documentation + Requirements**
- Choose Type 2 (Documentation Only)
- Add stories artifact type:
  ```json
  {
    "artifacts": {
      "specifications": { "path": "specs", "extensions": [".md"] },
      "guides": { "path": "guides", "extensions": [".md"] },
      "user-stories": { "path": "stories", "extensions": [".md"] }
    }
  }
  ```

---

## Custom Types

Beyond the four standard types, users can create fully custom configurations.

### Custom Type Example: DevOps Project

```json
{
  "corpus": {
    "name": "DevOps Project",
    "description": "Infrastructure and deployment documentation",
    "version": "1.0.0",
    "baseDir": "."
  },
  "artifacts": {
    "runbooks": {
      "path": "runbooks",
      "label": "Operational Runbooks",
      "extensions": [".md"]
    },
    "infrastructure": {
      "path": "infrastructure",
      "label": "Infrastructure as Code Docs",
      "extensions": [".md"]
    },
    "monitoring": {
      "path": "monitoring",
      "label": "Monitoring and Alerting",
      "extensions": [".md", ".yaml"]
    },
    "incident-reports": {
      "path": "incidents",
      "label": "Post-Mortem Reports",
      "extensions": [".md"]
    }
  },
  "framework": {
    "categories": [
      {
        "id": "services",
        "label": "Services",
        "terms": ["kubernetes", "docker", "terraform", "ansible"],
        "matchMode": "word-boundary"
      }
    ]
  },
  "consistency": { "enabled": true }
}
```

---

## Tips for Choosing Types

1. **Start simple:** Pick the closest match, customize later
2. **Primary focus:** Choose based on what most files will be
3. **Consistent structure:** Use standard directories for easier collaboration
4. **Expandable:** Add new artifact types as project evolves
5. **Team alignment:** Discuss with team before finalizing structure
