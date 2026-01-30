# CorpusHub Corpus Config (Shared Skill)

## Purpose

This skill explains the corpus-config.json structure, how to create and manage corpus plugins, and how the configuration drives all other CorpusHub operations.

## Config Location

There are two ways to provide a corpus configuration:

### 1. Plugin directory (legacy)
```
G:\My Drive\Projects\CorpusHub\plugins\<plugin-name>\corpus-config.json
```
For example: `plugins/america-4/corpus-config.json`

### 2. Project-root convention (multi-corpus)
Place `corpus-config.json` at the root of any project directory, then register it with CorpusHub:
```bash
curl -X POST http://localhost:3000/api/corpora/register \
  -H "Content-Type: application/json" \
  -d '{"path": "/absolute/path/to/my-project"}'
```
CorpusHub scans for `corpus-config.json` at the given path. This enables managing multiple corpora from different project folders.

### Application Project Template

A ready-made template for software projects is available at:
```
plugins/templates/application-project/corpus-config.json
```
This template includes artifact types for requirements, system design, API specs, architecture docs, data models, and ADRs. Copy it to your project root and customize it (see `shared/project-templates/SKILL.md` for details).

### Per-Corpus DB Isolation

Each registered corpus gets its own SQLite database stored in:
```
G:\My Drive\Projects\CorpusHub\data\corpora\<corpus-slug>.db
```
This provides complete isolation -- comments, plans, and metadata for each corpus are stored separately. When you switch corpora via `POST /api/corpora/switch`, the server reconnects to the appropriate database.

---

## Schema Overview

See `references/corpus-config-schema.md` for the full schema definition.

The config file has these top-level sections:

```json
{
  "corpus": { ... },
  "artifacts": [ ... ],
  "framework_terms": [ ... ],
  "voice": { ... },
  "roles": { ... },
  "settings": { ... }
}
```

### corpus
Metadata about the corpus itself: name, description, version, author.

### artifacts
Defines each document type in the corpus: type name, file patterns, locations, metadata fields, and display settings.

### framework_terms
Domain-specific vocabulary with canonical terms, definitions, aliases, and terms to avoid. Drives the consistency engine.

### voice
Writing style guidelines: tone, person, tense, formality level, specific do/don't rules.

### roles
Permission definitions for each user role (viewer, reviewer, editor, author, admin).

### settings
System-level settings: backup retention, scan frequency, AI model preferences.

---

## Creating a New Corpus Plugin

1. Create the plugin directory:
```bash
mkdir -p "G:\My Drive\Projects\CorpusHub\plugins\my-corpus"
```

2. Create `corpus-config.json` with required fields:
```json
{
  "corpus": {
    "name": "My Corpus",
    "description": "Description of the corpus",
    "version": "1.0.0",
    "author": "Your Name"
  },
  "artifacts": [
    {
      "type": "chapter",
      "display_name": "Chapter",
      "location": "chapters/",
      "file_pattern": "*.md",
      "metadata": {
        "title": { "type": "string", "required": true },
        "order": { "type": "number", "required": true }
      }
    }
  ],
  "framework_terms": [],
  "voice": {
    "tone": "professional",
    "person": "third",
    "formality": "formal"
  },
  "roles": {
    "admin": { "permissions": ["*"] },
    "editor": { "permissions": ["read", "write", "comment"] },
    "reviewer": { "permissions": ["read", "comment"] },
    "viewer": { "permissions": ["read"] }
  },
  "settings": {
    "backup_retention_days": 90,
    "scan_on_save": true
  }
}
```

3. Activate the plugin via one of these methods:

**Option A -- Legacy setup (plugin directory):**
```bash
curl -X POST http://localhost:3000/api/setup/configure \
  -H "Content-Type: application/json" \
  -d '{"plugin_path": "plugins/my-corpus"}'
```

**Option B -- Multi-corpus registration (project root):**
```bash
curl -X POST http://localhost:3000/api/corpora/register \
  -H "Content-Type: application/json" \
  -d '{"path": "/absolute/path/to/my-corpus"}'
```

### Creating a Corpus Config for a Software Project

For application/software projects, start from the template:

1. Copy `plugins/templates/application-project/corpus-config.json` to your project root
2. Customize the `corpus.name` and `corpus.description` fields
3. Adjust `artifacts` paths to match your project's directory structure
4. Add project-specific framework terms and categories
5. Register via `POST /api/corpora/register`

See `shared/project-templates/SKILL.md` for a detailed guide.

---

## Validating Config Changes

Before modifying a config, validate the structure:

1. Ensure all required fields are present (see schema reference)
2. Check that artifact type names are unique
3. Verify framework term entries have at minimum `term` and `definition`
4. Confirm file patterns match actual files in the artifact locations

After modifying config, restart the server or call the setup endpoint to reload.

---

## Common Config Operations

### Adding a framework term
Add to the `framework_terms` array:
```json
{
  "term": "civic infrastructure",
  "definition": "Public systems and institutions that support community function",
  "aliases": ["civic systems"],
  "avoid": ["government infrastructure", "public works"]
}
```

### Adding an artifact type
Add to the `artifacts` array:
```json
{
  "type": "policy-brief",
  "display_name": "Policy Brief",
  "location": "policy-briefs/",
  "file_pattern": "*.md",
  "metadata": {
    "title": { "type": "string", "required": true },
    "topic": { "type": "string", "required": true },
    "status": { "type": "string", "required": false, "default": "draft" }
  }
}
```

### Updating voice guidelines
Modify the `voice` object to adjust tone, add rules:
```json
{
  "voice": {
    "tone": "assertive and forward-looking",
    "person": "first-plural",
    "formality": "formal",
    "rules": [
      "Use active voice whenever possible",
      "Avoid hedging language (might, perhaps, possibly)",
      "Frame challenges as opportunities"
    ]
  }
}
```
