# corpus-config.json Reference

**Purpose:** Complete schema documentation for corpus-config.json
**Version:** v4.0.0
**Date:** 2026-02-14
**Audience:** Developers and system architects

---

## Overview

The `corpus-config.json` file is the central configuration for corpus-enabled projects. It defines:
- Project metadata
- Artifact types and locations
- Framework terminology
- Voice and writing standards
- Role-based permissions
- Audit configuration

---

## Complete Schema

```json
{
  "corpus": {
    "name": "string (required)",
    "description": "string (required)",
    "version": "string (required)",
    "baseDir": "string (required, absolute path)"
  },

  "artifacts": {
    "artifact-slug": {
      "path": "string (required, relative to baseDir)",
      "label": "string (required)",
      "extensions": ["string"] (required, array),
      "sourceMode": "corpus|source|bidirectional (required)"
    }
  },

  "framework": {
    "categories": [{
      "id": "string (required)",
      "label": "string (required)",
      "terms": ["string"] (required, array),
      "canonicalSource": "string (required, artifact-slug)",
      "matchMode": "word-boundary|case-insensitive|exact (optional, default: word-boundary)"
    }]
  },

  "voice": {
    "promptFile": "string (optional, relative path)",
    "attributes": ["string"] (optional, array),
    "avoid": ["string"] (optional, array),
    "preferredTerms": {
      "old-term": "new-term"
    }
  },

  "roles": {
    "available": ["string"] (optional, array),
    "defaultRole": "string (optional)",
    "aiAccess": ["string"] (optional, array),
    "editAccess": ["string"] (optional, array)
  },

  "audit": {
    "methodology": "string (optional)",
    "applicable_audits": ["string"] (optional, array),
    "convergence": {
      "enabled": "boolean (optional)",
      "automated": {
        "max_iterations": "number (optional)",
        "required_clean_passes": "number (optional)"
      },
      "user_validation": {
        "required": "boolean (optional)",
        "after_automated_convergence": "boolean (optional)",
        "min_testers": "number (optional)"
      },
      "methodologies": [{
        "name": "string (required)",
        "audits": [{"id": "string"}]
      }]
    }
  },

  "development": {
    "platform": "string (optional)",
    "framework": "string (optional)",
    "packaging": "string (optional)"
  }
}
```

---

## Section: corpus

**Purpose:** Project metadata and identification

### Fields

#### name
- **Type:** String
- **Required:** Yes
- **Description:** Human-readable project name
- **Example:** `"CorpusHub Platform"`

#### description
- **Type:** String
- **Required:** Yes
- **Description:** Brief project description
- **Example:** `"CorpusHub knowledge management platform"`

#### version
- **Type:** String
- **Required:** Yes
- **Format:** Semantic versioning (major.minor.patch)
- **Example:** `"2.0.0"`

#### baseDir
- **Type:** String
- **Required:** Yes
- **Format:** Absolute file path
- **Description:** Root directory of the project
- **Example:** `"C:/Projects/CorpusHub"` or `"/home/user/project"`
- **Note:** Use forward slashes even on Windows

### Example

```json
{
  "corpus": {
    "name": "My Project",
    "description": "Full-stack web application",
    "version": "1.0.0",
    "baseDir": "C:/Projects/my-project"
  }
}
```

---

## Section: artifacts

**Purpose:** Define project artifact types and their properties

### Structure

```json
{
  "artifacts": {
    "artifact-slug": {
      // artifact configuration
    }
  }
}
```

### Artifact Fields

#### path
- **Type:** String
- **Required:** Yes
- **Format:** Relative path from baseDir
- **Description:** Directory containing this artifact type
- **Example:** `"src"`, `"docs/api"`, `"requirements"`

#### label
- **Type:** String
- **Required:** Yes
- **Description:** Human-readable label for this artifact type
- **Example:** `"Source Code"`, `"API Documentation"`

#### extensions
- **Type:** Array of strings
- **Required:** Yes
- **Description:** File extensions for this artifact type
- **Format:** Include leading dot
- **Example:** `[".md"]`, `[".js", ".jsx", ".ts", ".tsx"]`

#### sourceMode
- **Type:** Enum
- **Required:** Yes
- **Options:** `"corpus"`, `"source"`, `"bidirectional"`
- **Description:** Editing workflow for this artifact type

**Source Mode Details:**

| Mode | Edit Location | Source of Truth | Typical Use |
|------|---------------|-----------------|-------------|
| `corpus` | CorpusHub only | CorpusHub HTML | Requirements, specs, ADRs |
| `source` | IDE (VS Code) | Files in repo | Code, configs, tests |
| `bidirectional` | Either location | Synced both ways | Documentation, guides |

### Example

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
      "extensions": [".js", ".jsx", ".ts", ".tsx"],
      "sourceMode": "source"
    },
    "documentation": {
      "path": "docs",
      "label": "Documentation",
      "extensions": [".md"],
      "sourceMode": "bidirectional"
    }
  }
}
```

---

## Section: framework

**Purpose:** Define canonical terminology and consistency rules

### Structure

```json
{
  "framework": {
    "categories": [
      {
        "id": "category-id",
        "label": "Category Label",
        "terms": ["Term 1", "Term 2"],
        "canonicalSource": "artifact-slug",
        "matchMode": "word-boundary"
      }
    ]
  }
}
```

### Category Fields

#### id
- **Type:** String
- **Required:** Yes
- **Format:** Lowercase, hyphen-separated
- **Description:** Unique identifier for this category
- **Example:** `"api-terminology"`, `"user-roles"`

#### label
- **Type:** String
- **Required:** Yes
- **Description:** Human-readable category name
- **Example:** `"API Terminology"`, `"User Roles"`

#### terms
- **Type:** Array of strings
- **Required:** Yes
- **Description:** List of canonical terms in this category
- **Example:** `["REST endpoint", "GraphQL query", "WebSocket connection"]`

#### canonicalSource
- **Type:** String
- **Required:** Yes
- **Description:** Artifact slug where these terms are defined
- **Must match:** An artifact slug from `artifacts` section
- **Example:** `"api-documentation"`

#### matchMode
- **Type:** Enum
- **Required:** No
- **Default:** `"word-boundary"`
- **Options:**
  - `"word-boundary"`: Match whole words only
  - `"case-insensitive"`: Ignore case differences
  - `"exact"`: Exact string match

**Match Mode Examples:**

| Mode | Term | Matches | Doesn't Match |
|------|------|---------|---------------|
| `word-boundary` | `"user"` | `"user account"` | `"username"` |
| `case-insensitive` | `"API"` | `"api"`, `"Api"`, `"API"` | `"APIs"` (plural) |
| `"exact"` | `"REST API"` | `"REST API"` | `"rest api"`, `"REST APIs"` |

### Example

```json
{
  "framework": {
    "categories": [
      {
        "id": "api-terms",
        "label": "API Terminology",
        "terms": [
          "REST endpoint",
          "GraphQL query",
          "authentication token"
        ],
        "canonicalSource": "api-docs",
        "matchMode": "case-insensitive"
      },
      {
        "id": "user-roles",
        "label": "User Roles",
        "terms": [
          "administrator",
          "editor",
          "viewer"
        ],
        "canonicalSource": "requirements",
        "matchMode": "word-boundary"
      }
    ]
  }
}
```

---

## Section: voice

**Purpose:** Define writing style and AI guidance

### Fields

#### promptFile
- **Type:** String
- **Required:** No
- **Format:** Relative path from baseDir
- **Description:** Path to detailed writing style guide
- **Example:** `"docs/writing-style.md"`

#### attributes
- **Type:** Array of strings
- **Required:** No
- **Description:** Positive writing characteristics to emphasize
- **Example:** `["professional", "clear", "concise", "action-oriented"]`

#### avoid
- **Type:** Array of strings
- **Required:** No
- **Description:** Writing characteristics to avoid
- **Example:** `["jargon", "passive voice", "ambiguity"]`

#### preferredTerms
- **Type:** Object (key-value pairs)
- **Required:** No
- **Description:** Term replacements (old → new)
- **Format:** `{ "avoid-term": "preferred-term" }`
- **Example:**
```json
{
  "user": "member",
  "click": "select",
  "login": "sign in"
}
```

### Example

```json
{
  "voice": {
    "promptFile": "docs/writing-style.md",
    "attributes": [
      "professional",
      "clear",
      "concise"
    ],
    "avoid": [
      "jargon",
      "passive voice",
      "unnecessary complexity"
    ],
    "preferredTerms": {
      "user": "member",
      "login": "sign in",
      "click": "select"
    }
  }
}
```

---

## Section: roles

**Purpose:** Define role-based access control

### Fields

#### available
- **Type:** Array of strings
- **Required:** No
- **Default:** `["admin", "editor", "author", "reviewer", "viewer", "pending"]`
- **Description:** Roles available in this corpus
- **Example:** `["admin", "editor", "viewer"]`

#### defaultRole
- **Type:** String
- **Required:** No
- **Default:** `"pending"`
- **Description:** Role assigned to new users
- **Example:** `"viewer"`

#### aiAccess
- **Type:** Array of strings
- **Required:** No
- **Default:** `["admin", "editor", "author"]`
- **Description:** Roles that can use AI features
- **Example:** `["admin", "editor"]`

#### editAccess
- **Type:** Array of strings
- **Required:** No
- **Default:** `["admin", "editor", "author"]`
- **Description:** Roles that can edit content
- **Example:** `["admin", "editor"]`

### Role Hierarchy

**Standard roles (default):**
1. **admin** - Full access, manage users and settings
2. **editor** - Edit content, manage artifacts, use AI
3. **author** - Create new content, use AI
4. **reviewer** - Read content, add comments (no edits)
5. **viewer** - Read-only access
6. **pending** - No access (awaiting approval)

### Example

```json
{
  "roles": {
    "available": ["admin", "editor", "author", "reviewer", "viewer", "pending"],
    "defaultRole": "pending",
    "aiAccess": ["admin", "editor", "author"],
    "editAccess": ["admin", "editor", "author"]
  }
}
```

---

## Section: audit

**Purpose:** Configure audit system and convergence workflow

### Fields

#### methodology
- **Type:** String
- **Required:** No
- **Default:** `"multi-methodology-3-3-1"`
- **Description:** Audit methodology to use
- **Options:** `"multi-methodology-3-3-1"`, `"single-audit"`

#### applicable_audits
- **Type:** Array of strings
- **Required:** No
- **Description:** Which audit types apply to this project
- **Options:**
  - `"consistency"` - Framework term validation
  - `"navigation"` - Link and structure validation
  - `"security"` - Vulnerability scanning
  - `"quality"` - Code quality, test coverage
  - `"performance"` - Load time, bundle size
  - `"accessibility"` - WCAG compliance
  - `"seo"` - Meta tags, sitemap
  - `"content"` - Grammar, style, readability
  - `"dependency"` - Package vulnerabilities

### convergence

**Purpose:** Configure multi-methodology convergence workflow

#### convergence.enabled
- **Type:** Boolean
- **Required:** No
- **Default:** `false`
- **Description:** Enable convergence workflow

#### convergence.automated
- **Type:** Object
- **Description:** Automated convergence settings

**automated.max_iterations:**
- **Type:** Number
- **Default:** `10`
- **Description:** Maximum automated passes

**automated.required_clean_passes:**
- **Type:** Number
- **Default:** `3`
- **Description:** Consecutive clean passes required before user validation

#### convergence.user_validation
- **Type:** Object
- **Description:** User validation settings

**user_validation.required:**
- **Type:** Boolean
- **Default:** `true`
- **Description:** Require user testing after automation

**user_validation.after_automated_convergence:**
- **Type:** Boolean
- **Default:** `true`
- **Description:** Only start user testing after automation succeeds

**user_validation.min_testers:**
- **Type:** Number
- **Default:** `2`
- **Description:** Minimum number of testers required

#### convergence.methodologies
- **Type:** Array of objects
- **Description:** Methodology configuration

### Example

```json
{
  "audit": {
    "methodology": "multi-methodology-3-3-1",
    "applicable_audits": [
      "consistency",
      "navigation",
      "security",
      "quality"
    ],
    "convergence": {
      "enabled": true,
      "automated": {
        "max_iterations": 10,
        "required_clean_passes": 3
      },
      "user_validation": {
        "required": true,
        "after_automated_convergence": true,
        "min_testers": 2
      },
      "methodologies": [
        {
          "name": "technical",
          "audits": [
            {"id": "security"},
            {"id": "quality"}
          ]
        },
        {
          "name": "user",
          "audits": [
            {"id": "content"},
            {"id": "accessibility"}
          ]
        },
        {
          "name": "holistic",
          "audits": [
            {"id": "consistency"},
            {"id": "navigation"}
          ]
        }
      ]
    }
  }
}
```

---

## Section: development

**Purpose:** Development-specific settings (primarily for Windows apps)

### Fields

#### platform
- **Type:** String
- **Required:** No
- **Description:** Target platform
- **Example:** `"windows"`, `"web"`, `"cross-platform"`

#### framework
- **Type:** String
- **Required:** No
- **Description:** Development framework
- **Example:** `"wpf"`, `"electron"`, `"react"`

#### packaging
- **Type:** String
- **Required:** No
- **Description:** Packaging format
- **Example:** `"msi"`, `"exe"`, `"appx"`

### Example

```json
{
  "development": {
    "platform": "windows",
    "framework": "wpf",
    "packaging": "msi"
  }
}
```

---

## Complete Examples

### Example 1: Documentation Repository

```json
{
  "corpus": {
    "name": "Framework Documentation",
    "description": "Complete framework documentation",
    "version": "1.0.0",
    "baseDir": "/home/user/framework-docs"
  },
  "artifacts": {
    "guides": {
      "path": "guides",
      "label": "User Guides",
      "extensions": [".md"],
      "sourceMode": "corpus"
    },
    "api-docs": {
      "path": "api",
      "label": "API Documentation",
      "extensions": [".md"],
      "sourceMode": "bidirectional"
    },
    "examples": {
      "path": "examples",
      "label": "Code Examples",
      "extensions": [".js", ".ts"],
      "sourceMode": "source"
    }
  },
  "framework": {
    "categories": [
      {
        "id": "framework-terms",
        "label": "Framework Terminology",
        "terms": ["component", "directive", "service", "pipe"],
        "canonicalSource": "guides",
        "matchMode": "word-boundary"
      }
    ]
  },
  "audit": {
    "applicable_audits": ["consistency", "content", "navigation"]
  }
}
```

### Example 2: Full-Stack Web Application

```json
{
  "corpus": {
    "name": "CorpusHub Platform",
    "description": "Knowledge management platform",
    "version": "2.0.0",
    "baseDir": "C:/Projects/corpushub"
  },
  "artifacts": {
    "requirements": {
      "path": "docs/requirements",
      "label": "Requirements",
      "extensions": [".md"],
      "sourceMode": "corpus"
    },
    "source-code": {
      "path": "src",
      "label": "Source Code",
      "extensions": [".js", ".jsx", ".ts", ".tsx"],
      "sourceMode": "source"
    },
    "tests": {
      "path": "tests",
      "label": "Tests",
      "extensions": [".test.js", ".spec.ts"],
      "sourceMode": "source"
    },
    "documentation": {
      "path": "docs",
      "label": "Documentation",
      "extensions": [".md"],
      "sourceMode": "bidirectional"
    }
  },
  "framework": {
    "categories": [
      {
        "id": "platform-terms",
        "label": "Platform Terminology",
        "terms": ["corpus", "bit", "artifact", "framework term"],
        "canonicalSource": "requirements"
      }
    ]
  },
  "voice": {
    "attributes": ["professional", "clear", "precise"],
    "avoid": ["jargon", "ambiguity"],
    "preferredTerms": {
      "user": "member",
      "document": "bit"
    }
  },
  "audit": {
    "methodology": "multi-methodology-3-3-1",
    "applicable_audits": [
      "security",
      "quality",
      "performance",
      "consistency"
    ],
    "convergence": {
      "enabled": true,
      "automated": {
        "max_iterations": 10,
        "required_clean_passes": 3
      }
    }
  }
}
```

### Example 3: Windows Desktop Application

```json
{
  "corpus": {
    "name": "Operations Hub",
    "description": "Windows operations management application",
    "version": "1.0.0",
    "baseDir": "C:/Projects/operations-hub"
  },
  "artifacts": {
    "source-code": {
      "path": "app",
      "label": "Application Code",
      "extensions": [".cs", ".xaml"],
      "sourceMode": "source"
    },
    "installers": {
      "path": "installers",
      "label": "WiX Installer Sources",
      "extensions": [".wxs", ".wxi"],
      "sourceMode": "source"
    },
    "documentation": {
      "path": "docs",
      "label": "Documentation",
      "extensions": [".md"],
      "sourceMode": "bidirectional"
    }
  },
  "development": {
    "platform": "windows",
    "framework": "wpf",
    "packaging": "msi"
  },
  "audit": {
    "applicable_audits": ["quality", "security"]
  }
}
```

---

## Validation

### Required Fields

**Minimum valid configuration:**

```json
{
  "corpus": {
    "name": "Project Name",
    "description": "Description",
    "version": "1.0.0",
    "baseDir": "/absolute/path"
  },
  "artifacts": {
    "docs": {
      "path": "docs",
      "label": "Documentation",
      "extensions": [".md"],
      "sourceMode": "source"
    }
  }
}
```

### Common Validation Errors

**Missing baseDir:**
```
Error: corpus.baseDir is required and must be an absolute path
```

**Invalid artifact slug reference:**
```
Error: framework.categories[0].canonicalSource "docs-xyz"
       does not match any artifact slug
```

**Invalid sourceMode:**
```
Error: artifacts.code.sourceMode must be one of:
       "corpus", "source", "bidirectional"
```

---

## Tools

### Validate Configuration

```bash
# Use corpus-config skill to validate
claude "Validate corpus configuration"

# Or use validation utility
python tools/validate_config.py corpus-config.json
```

### Generate Template

```bash
# Generate from template
cp config/templates/web-app.json corpus-config.json

# Customize for your project
edit corpus-config.json
```

---

## Additional Resources

- **CORPUS-FIRST-GUIDE.md** - Conceptual guide to corpus-first approach
- **MIGRATION-v3-to-v4.md** - Migration from v3.0 to v4.0
- **config/templates/** - Pre-built configuration templates
- **config/examples/** - Real-world examples

---

**Complete Configuration Reference** ✅

---

**Last Updated:** 2026-02-14
**Version:** v4.0.0
**Status:** Complete reference documentation
