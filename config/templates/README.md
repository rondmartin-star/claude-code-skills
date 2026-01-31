# Corpus Configuration Templates

Ready-to-use corpus-config.json templates for different project types.

---

## Available Templates

### minimal.json
**Purpose:** Bare-bones starting point for any corpus project

**Use when:**
- Starting a new corpus from scratch
- Need minimal configuration
- Want to customize everything yourself

**Includes:**
- Single artifact (docs)
- Basic voice attributes
- Minimal audit setup (consistency, navigation, content)
- Backup disabled by default

**Quick start:**
```bash
cp config/templates/minimal.json ./corpus-config.json
# Edit name, description, and artifacts
```

---

### default.json
**Purpose:** General-purpose corpus with sensible defaults

**Use when:**
- Creating a standard documentation project
- Need a balanced configuration
- Want common audits enabled

**Includes:**
- Multiple artifact types
- Comprehensive voice configuration
- Full audit suite enabled
- Backup and export configured

---

### web-app.json
**Purpose:** Web application development project

**Use when:**
- Building a web application
- Need source code + requirements + docs
- Want technical and user audits

**Includes:**
- Source modes: source (src), corpus (requirements), bidirectional (docs)
- Security, quality, performance audits
- Accessibility and SEO audits
- Development workflow support

---

### windows-app.json
**Purpose:** Windows desktop application project

**Use when:**
- Building a Windows application
- Using Node.js/Electron
- Need NSSM service deployment

**Includes:**
- Windows-specific artifacts (installers, services)
- Security patterns (OAuth, cookie separation)
- MSI packaging support
- NSSM service configuration

---

### content-corpus.json
**Purpose:** Content-focused projects (blogs, documentation sites)

**Use when:**
- Publishing content
- Writing documentation
- Creating educational materials

**Includes:**
- Content-centric artifacts
- Heavy emphasis on content quality audits
- SEO and accessibility
- Export presets for publishing

---

### framework-docs.json
**Purpose:** Framework or specification documentation

**Use when:**
- Documenting a framework
- Writing specifications
- Need term consistency validation

**Includes:**
- Framework categories and canonical terms
- Exact match mode for principles
- Consistency audit emphasized
- Comprehensive documentation structure

---

## Usage

### 1. Choose Template

Pick the template that best matches your project type.

### 2. Copy to Project

```bash
cp config/templates/<template-name>.json ./corpus-config.json
```

### 3. Customize

Edit the copied file:
- Update `name` and `description`
- Adjust `artifacts` paths
- Configure `voice` attributes
- Enable/disable audits as needed

### 4. Initialize

```bash
# Initialize corpus with your config
claude --skill corpus-init
```

---

## Template Structure

All templates follow this structure:

```json
{
  "name": "project-name",
  "version": "1.0.0",
  "description": "Brief description",

  "artifacts": {
    "artifact-name": {
      "path": "relative/path",
      "sourceMode": "corpus|source|bidirectional",
      "title": "Display Title"
    }
  },

  "voice": {
    "attributes": ["attribute1", "attribute2"],
    "avoid": ["pattern1", "pattern2"]
  },

  "roles": {
    "editAccess": ["role1", "role2"],
    "aiAccess": ["role1", "role2"]
  },

  "audit": {
    "methodology": "multi-methodology-3-3-1",
    "convergence": { /* ... */ }
  },

  "backup": { /* ... */ },
  "export": { /* ... */ }
}
```

---

## Customization Tips

### Adding Artifacts

```json
"artifacts": {
  "my-artifact": {
    "path": "path/to/artifact",
    "sourceMode": "corpus",  // or "source" or "bidirectional"
    "title": "My Artifact"
  }
}
```

### Enabling Audits

```json
"audits": [
  {
    "id": "security",
    "enabled": true,
    "config": {
      "check_sql_injection": true,
      "check_xss": true
    }
  }
]
```

### Setting Voice

```json
"voice": {
  "attributes": ["professional", "technical", "concise"],
  "avoid": ["marketing speak", "buzzwords"],
  "preferredTerms": {
    "JavaScript": "JS"
  }
}
```

---

## See Also

- **Examples:** `config/examples/` - Real project configurations
- **Schema Reference:** `ARCHITECTURE-v4.md` - Full schema documentation
- **Validation:** Use `utilities/validation` skill to check your config

---

*Part of v4.0.0 Universal Skills Ecosystem*
*All templates tested and validated*
