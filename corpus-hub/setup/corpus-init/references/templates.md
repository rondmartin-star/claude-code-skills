# Corpus Configuration Templates

Full, commented `corpus-config.json` templates for each project type.

---

## Template 1: Software Application (Standard)

```jsonc
{
  // ===== CORPUS IDENTITY =====
  "corpus": {
    // Display name (shown in CorpusHub UI)
    "name": "My Application Project",

    // Brief description (1-2 sentences)
    "description": "Artifact corpus for the My Application Project",

    // Semantic version of the corpus schema
    "version": "1.0.0",

    // Base directory (relative to corpus-config.json location)
    // Use "." for project root
    "baseDir": "."
  },

  // ===== ARTIFACT TYPES =====
  // Maps artifact type IDs to file system locations
  "artifacts": {
    // Requirements documents
    "requirements": {
      // Path relative to baseDir
      "path": "docs/requirements",

      // Display label in UI
      "label": "Requirements",

      // Supported file extensions
      "extensions": [".md", ".html"]
    },

    // System design documents
    "design": {
      "path": "docs/design",
      "label": "Design Documents",
      "extensions": [".md", ".html"]
    },

    // API specifications (OpenAPI, Swagger, etc.)
    "api-specs": {
      "path": "docs/api",
      "label": "API Specifications",
      "extensions": [".md", ".yaml", ".json", ".openapi"]
    },

    // High-level architecture diagrams and descriptions
    "architecture": {
      "path": "docs/architecture",
      "label": "Architecture",
      "extensions": [".md", ".html"]
    },

    // Architecture Decision Records (ADRs)
    "decisions": {
      "path": "docs/decisions",
      "label": "Architecture Decisions",
      "extensions": [".md"]
    }
  },

  // ===== FRAMEWORK TERMS (Optional) =====
  // For consistency checking across the corpus
  "framework": {
    "categories": [
      {
        // Unique ID for this category
        "id": "quality-attributes",

        // Display label
        "label": "Quality Attributes",

        // Terms to track and check consistency for
        "terms": [
          "scalability",
          "reliability",
          "security",
          "performance",
          "maintainability",
          "availability",
          "usability"
        ],

        // Matching strategy:
        // - "word-boundary": Match whole words only
        // - "case-insensitive": Match regardless of case
        "matchMode": "word-boundary"
      },
      {
        "id": "design-patterns",
        "label": "Design Patterns",
        "terms": [
          "microservices",
          "event-driven",
          "layered architecture",
          "repository pattern",
          "CQRS",
          "API gateway"
        ],
        "matchMode": "case-insensitive"
      }
    ]
  },

  // ===== VOICE GUIDELINES (Optional) =====
  // For AI-assisted content generation
  // Set to null if not needed
  "voice": null,

  // ===== ROLES AND PERMISSIONS =====
  "roles": {
    // Available role types
    "available": ["admin", "editor", "viewer", "pending"],

    // Default role for new users
    "defaultRole": "pending",

    // Roles with AI assistance access
    "aiAccess": ["admin", "editor"],

    // Roles with edit permissions
    "editAccess": ["admin", "editor"]
  },

  // ===== CONSISTENCY CHECKING =====
  "consistency": {
    // Enable/disable consistency scanning
    "enabled": true,

    // Optional: Specific directories to scan
    // If omitted, scans all artifact paths
    "scanDirectories": [
      "docs/requirements",
      "docs/design",
      "docs/api"
    ]
  }
}
```

---

## Template 2: Documentation Only (Minimal)

```jsonc
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

  // No framework terms needed
  "framework": null,

  "voice": null,

  "roles": {
    "available": ["admin", "editor", "viewer", "pending"],
    "defaultRole": "pending"
  },

  // Consistency checking disabled
  "consistency": { "enabled": false }
}
```

---

## Template 3: Research/Writing

```jsonc
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

      // Include document formats
      "extensions": [".md", ".html", ".docx"]
    },
    "publications": {
      "path": "publications",
      "label": "Published Papers",

      // Include final formats
      "extensions": [".md", ".html", ".pdf"]
    }
  },

  "framework": {
    "categories": [
      {
        "id": "research-methods",
        "label": "Research Methods",
        "terms": [
          "qualitative analysis",
          "quantitative analysis",
          "case study",
          "survey",
          "experiment"
        ],
        "matchMode": "case-insensitive"
      }
    ]
  },

  "voice": null,

  "consistency": { "enabled": true }
}
```

---

## Template 4: Requirements Management

```jsonc
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
          "functional requirement",
          "non-functional requirement",
          "user story",
          "acceptance criteria",
          "business rule"
        ],
        "matchMode": "case-insensitive"
      }
    ]
  },

  "consistency": { "enabled": true }
}
```

---

## Advanced Template: Microservices Project

```jsonc
{
  "corpus": {
    "name": "Microservices Platform",
    "description": "Multi-service architecture documentation",
    "version": "1.0.0",
    "baseDir": "."
  },

  "artifacts": {
    "requirements": {
      "path": "docs/requirements",
      "label": "Requirements",
      "extensions": [".md"]
    },
    "api-specs": {
      "path": "services/*/docs/api",  // Glob pattern
      "label": "Service APIs",
      "extensions": [".yaml", ".openapi"]
    },
    "architecture": {
      "path": "docs/architecture",
      "label": "System Architecture",
      "extensions": [".md"]
    },
    "decisions": {
      "path": "docs/adr",
      "label": "Architecture Decisions",
      "extensions": [".md"]
    },
    "runbooks": {
      "path": "docs/runbooks",
      "label": "Operational Runbooks",
      "extensions": [".md"]
    }
  },

  "framework": {
    "categories": [
      {
        "id": "services",
        "label": "Services",
        "terms": [
          "user-service",
          "auth-service",
          "payment-service",
          "notification-service"
        ],
        "matchMode": "case-insensitive"
      },
      {
        "id": "patterns",
        "label": "Architecture Patterns",
        "terms": [
          "circuit breaker",
          "saga pattern",
          "API gateway",
          "service mesh",
          "event sourcing"
        ],
        "matchMode": "word-boundary"
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
    "enabled": true,

    // Scan all docs but not service code
    "scanDirectories": [
      "docs/requirements",
      "docs/architecture",
      "docs/adr",
      "docs/runbooks"
    ]
  }
}
```

---

## Advanced Template: Monorepo

```jsonc
{
  "corpus": {
    "name": "Monorepo Documentation",
    "description": "Shared documentation for monorepo projects",
    "version": "1.0.0",
    "baseDir": "."
  },

  "artifacts": {
    // Shared requirements
    "requirements": {
      "path": "docs/requirements",
      "label": "Shared Requirements",
      "extensions": [".md"]
    },

    // Per-package documentation
    "package-docs": {
      "path": "packages/*/docs",  // Matches all packages
      "label": "Package Documentation",
      "extensions": [".md", ".html"]
    },

    // Architecture decisions affecting multiple packages
    "decisions": {
      "path": "docs/decisions",
      "label": "Architecture Decisions",
      "extensions": [".md"]
    },

    // Integration documentation
    "integration": {
      "path": "docs/integration",
      "label": "Integration Guides",
      "extensions": [".md"]
    }
  },

  "framework": {
    "categories": [
      {
        "id": "packages",
        "label": "Packages",
        "terms": [
          "@company/core",
          "@company/ui",
          "@company/api",
          "@company/utils"
        ],
        "matchMode": "case-insensitive"
      }
    ]
  },

  "consistency": {
    "enabled": true
  }
}
```

---

## Voice Configuration Example

For projects that need consistent writing style (customer-facing docs):

```jsonc
{
  "voice": {
    // Path to AI prompt file (relative to corpus-config.json)
    "promptFile": "ai-prompts/system-prompt.md",

    // Writing attributes to maintain
    "attributes": [
      "friendly and approachable",
      "technically accurate",
      "concise and clear"
    ],

    // Phrases to avoid
    "avoid": [
      "simply",
      "just",
      "very",
      "obviously"
    ],

    // Preferred terminology mappings
    "preferredTerms": {
      "user interface": "UI",
      "application programming interface": "API",
      "database": "data store"
    }
  }
}
```

And create `ai-prompts/system-prompt.md`:

```markdown
# Documentation Voice Guidelines

## Tone
- Friendly but professional
- Technically accurate without jargon
- Concise and scannable

## Structure
- Start with the "why" before the "how"
- Use bullet points for lists
- Include code examples where relevant
- Add diagrams for complex concepts

## Terminology
- Use "API" not "application programming interface"
- Use "UI" not "user interface"
- Use "data store" not "database"

## Avoid
- Marketing language
- Superlatives ("amazing", "incredible")
- Passive voice where possible
- Unnecessarily long sentences
```

---

## Extension Recommendations

### Documentation Formats
- **Markdown**: `.md` - Most common, GitHub-friendly
- **HTML**: `.html` - Rich formatting, embedded media
- **reStructuredText**: `.rst` - Python ecosystem standard
- **AsciiDoc**: `.adoc` - Advanced formatting features

### API Specifications
- **OpenAPI**: `.yaml`, `.json`, `.openapi`
- **GraphQL**: `.graphql`, `.gql`
- **Protocol Buffers**: `.proto`
- **WSDL**: `.wsdl` (SOAP APIs)

### Configuration
- **YAML**: `.yaml`, `.yml`
- **JSON**: `.json`
- **TOML**: `.toml`

### Diagrams
- **Mermaid**: `.mmd` (text-based diagrams)
- **PlantUML**: `.puml` (UML diagrams)
- **Draw.io**: `.drawio` (visual editor)

---

## Tips

1. **Start minimal:** Begin with 3-5 artifact types, add more as needed
2. **Consistent naming:** Use lowercase-with-hyphens for artifact type IDs
3. **Relative paths:** Always use relative paths from baseDir
4. **Extensions matter:** List all file extensions you'll use
5. **Framework terms:** Start with 10-20 terms, expand based on scanning results
6. **Voice optional:** Only add voice config if you have customer-facing docs
7. **Comments help:** Use JSON with comments (`.jsonc`) during development
8. **Version control:** Commit corpus-config.json to git
