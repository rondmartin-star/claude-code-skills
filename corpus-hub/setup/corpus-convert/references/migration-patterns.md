# Migration Patterns - Common Project Conversions

Real-world patterns for converting different project types.

---

## Pattern 1: Standard Software Project

### Before
```
my-app/
├── docs/
│   ├── requirements/
│   ├── design/
│   └── api/
├── src/
└── tests/
```

### Conversion
- Scan: `docs/**/*.md`
- Mode: Traditional (team edits in IDE)
- Watchers: Enabled
- Framework terms: quality-attributes, design-patterns

### After
```
my-app/
├── corpus-config.json         # NEW
├── corpus/                    # NEW (generated)
│   ├── requirements/
│   ├── design/
│   └── api/
├── docs/                      # Source of truth
│   ├── requirements/
│   ├── design/
│   └── api/
├── src/
└── tests/
```

---

## Pattern 2: Documentation-Only Project

### Before
```
product-docs/
├── getting-started/
├── user-guides/
├── api-reference/
└── troubleshooting/
```

### Conversion
- Scan: `**/*.md`
- Mode: Corpus (browser editing)
- Watchers: Disabled
- Original files: Marked deprecated

### After
```
product-docs/
├── corpus-config.json         # NEW
├── corpus/                    # NEW (source of truth)
│   ├── getting-started/
│   ├── user-guides/
│   ├── api-reference/
│   └── troubleshooting/
├── getting-started/           # DEPRECATED
│   └── .DEPRECATED            # Marker file
├── user-guides/               # DEPRECATED
└── api-reference/             # DEPRECATED
```

---

## Pattern 3: Monorepo with Multiple Packages

### Before
```
monorepo/
├── packages/
│   ├── core/
│   │   └── docs/
│   ├── ui/
│   │   └── docs/
│   └── api/
│       └── docs/
└── docs/                      # Shared docs
```

### Conversion Strategy

**Option A: One corpus per package**
- Register each package separately
- Separate corpus-config.json in each

**Option B: Single unified corpus**
- Scan all package docs
- Use glob patterns: `packages/*/docs/**`
- Single corpus-config.json at root

### Recommended: Option B (Unified)

```json
{
  "artifacts": {
    "package-docs": {
      "path": "packages/*/docs",
      "label": "Package Documentation",
      "extensions": [".md"]
    },
    "shared-docs": {
      "path": "docs",
      "label": "Shared Documentation",
      "extensions": [".md"]
    }
  }
}
```

---

## Pattern 4: Mixed Documentation Formats

### Before
```
mixed-docs/
├── markdown/                  # Markdown files
├── asciidoc/                  # AsciiDoc files
├── rst/                       # reStructuredText
└── html/                      # Raw HTML
```

### Conversion
- Convert all to HTML
- Use content-converter utility
- Store originals as deprecated
- Corpus becomes unified HTML

### Configuration
```json
{
  "artifacts": {
    "documentation": {
      "path": "corpus",
      "label": "Documentation",
      "extensions": [".html"]
    }
  }
}
```

---

## Pattern 5: API-First Project (OpenAPI Specs)

### Before
```
api-project/
├── specs/
│   ├── users-api.yaml
│   ├── auth-api.yaml
│   └── payments-api.yaml
└── docs/
    └── overview.md
```

### Conversion
- Mode: Traditional
- Watchers on YAML files
- Generate HTML docs from OpenAPI

### Configuration
```json
{
  "artifacts": {
    "api-specs": {
      "path": "specs",
      "label": "API Specifications",
      "extensions": [".yaml", ".openapi", ".json"]
    },
    "guides": {
      "path": "docs",
      "label": "Guides",
      "extensions": [".md"]
    }
  }
}
```

---

## Pattern 6: Academic Research Project

### Before
```
dissertation/
├── chapters/
│   ├── 01-introduction.md
│   ├── 02-literature-review.md
│   └── 03-methodology.md
├── references/
│   └── bibliography.bib
└── data/
    └── analysis.csv
```

### Conversion
- Mode: Corpus
- Framework terms: research methods, theories
- Relationships: chapter dependencies

### Configuration
```json
{
  "artifacts": {
    "chapters": {
      "path": "chapters",
      "label": "Dissertation Chapters",
      "extensions": [".md", ".docx"]
    },
    "references": {
      "path": "references",
      "label": "References",
      "extensions": [".md", ".bib"]
    }
  },
  "framework": {
    "categories": [
      {
        "id": "research-methods",
        "label": "Research Methods",
        "terms": ["qualitative analysis", "case study", "survey"]
      }
    ]
  }
}
```

---

## Pattern 7: Requirements Database Conversion

### Before
```
requirements/
├── functional/
│   ├── FR-001.md
│   ├── FR-002.md
│   └── FR-003.md
├── non-functional/
│   ├── NFR-001.md
│   └── NFR-002.md
└── stories/
    └── US-*.md
```

### Conversion
- Mode: Corpus
- Extract requirement IDs
- Infer relationships (stories → requirements)
- Framework terms: requirement types

### After Relationships
```
US-001 → IMPLEMENTS → FR-001
US-002 → IMPLEMENTS → FR-001, FR-002
NFR-001 → CONSTRAINS → FR-003
```

---

## Pattern 8: Legacy Wiki Migration

### Before
- Confluence/MediaWiki/GitBook
- Export to markdown
- Flat or nested structure

### Conversion Steps
1. Export wiki to markdown
2. Organize by artifact type
3. Convert to CorpusHub
4. Infer relationships from wiki links
5. Mark originals deprecated

### Configuration
```json
{
  "artifacts": {
    "articles": {
      "path": "wiki-export",
      "label": "Wiki Articles",
      "extensions": [".md"]
    }
  }
}
```

---

## Anti-Patterns (Avoid)

### ❌ Deep Nesting
```
docs/
  team-a/
    subteam-1/
      project-x/
        feature-y/
          doc.md
```
**Problem:** Hard to navigate, infer types
**Solution:** Flatten to 2-3 levels max

### ❌ Mixed Content in Single Directory
```
docs/
  requirement-1.md
  design-doc-1.md
  api-spec-1.yaml
  random-notes.md
```
**Problem:** Can't infer artifact types
**Solution:** Separate by type

### ❌ No Naming Convention
```
docs/
  stuff.md
  notes.md
  misc.md
```
**Problem:** No semantic meaning
**Solution:** Use descriptive names

---

## Best Practices

1. **Consistent structure** - Use standard directories
2. **Clear naming** - Descriptive file names
3. **Flat hierarchy** - 2-3 levels deep max
4. **Separate concerns** - One artifact type per directory
5. **Use READMEs** - Document directory purpose
6. **Version control** - Commit before converting
7. **Test small first** - Convert one artifact type, validate
8. **Gradual migration** - Don't convert everything at once
9. **Team alignment** - Communicate changes to team
10. **Preserve originals** - Always keep backups

---

## Rollback Strategy

If conversion doesn't work:

1. **Delete corpus-config.json**
2. **Remove deprecation notices** from files
3. **Delete .DEPRECATED markers**
4. **Delete corpus/ directory**
5. **Unregister from CorpusHub:**
   ```bash
   curl -X DELETE http://localhost:3000/api/corpora/my-project-slug
   ```

Original files are preserved, so rollback is safe.
