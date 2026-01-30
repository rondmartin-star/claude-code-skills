# corpus-config.json Schema Reference

## Top-Level Structure

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `corpus` | object | yes | Corpus metadata |
| `artifacts` | array | yes | Artifact type definitions |
| `framework_terms` | array | yes | Domain vocabulary (can be empty array) |
| `voice` | object | yes | Writing style guidelines |
| `roles` | object | yes | Role permission definitions |
| `settings` | object | no | System-level configuration |

---

## corpus (object)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Display name of the corpus |
| `description` | string | yes | Brief description |
| `version` | string | yes | Semantic version (e.g., "1.0.0") |
| `author` | string | no | Author or organization name |

## artifacts (array of objects)

Each entry defines an artifact type:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | yes | Unique identifier (e.g., "chapter", "appendix") |
| `display_name` | string | yes | Human-readable name |
| `location` | string | yes | Directory path relative to plugin root |
| `file_pattern` | string | yes | Glob pattern for matching files (e.g., "*.md") |
| `metadata` | object | no | Metadata field definitions (see below) |
| `template` | string | no | Path to a template file for new artifacts |

### metadata field definition

Each key in `metadata` maps to a field definition:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | yes | Data type: "string", "number", "boolean", "array" |
| `required` | boolean | yes | Whether the field is mandatory |
| `default` | any | no | Default value if not provided |
| `enum` | array | no | Allowed values (for constrained fields) |

## framework_terms (array of objects)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `term` | string | yes | The canonical term |
| `definition` | string | yes | What it means in this corpus |
| `aliases` | array of strings | no | Acceptable alternative forms |
| `avoid` | array of strings | no | Terms to flag and replace with this one |
| `category` | string | no | Grouping category for the term |

## voice (object)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tone` | string | yes | Overall tone description |
| `person` | string | yes | Narrative person: "first", "first-plural", "second", "third" |
| `formality` | string | yes | "informal", "semi-formal", "formal", "academic" |
| `tense` | string | no | Preferred tense: "present", "past", "mixed" |
| `rules` | array of strings | no | Specific writing rules to follow |
| `avoid_patterns` | array of strings | no | Patterns/phrases to avoid |

## roles (object)

Keys are role names. Each value is an object:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `permissions` | array of strings | yes | Allowed operations |

**Permission values:** `read`, `write`, `comment`, `plan`, `approve`, `admin`, `backup`, `*` (all)

## settings (object)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `backup_retention_days` | number | no | Days to keep backups (default: 90) |
| `scan_on_save` | boolean | no | Auto-scan after artifact edits (default: false) |
| `ai_model` | string | no | Preferred AI model for generation |
| `max_artifact_size_kb` | number | no | Maximum artifact file size in KB |

---

## Minimal Example

```json
{
  "corpus": {
    "name": "My Project",
    "description": "A sample corpus",
    "version": "1.0.0"
  },
  "artifacts": [
    {
      "type": "document",
      "display_name": "Document",
      "location": "docs/",
      "file_pattern": "*.md"
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
    "editor": { "permissions": ["read", "write"] },
    "viewer": { "permissions": ["read"] }
  }
}
```
