# CorpusHub Project Templates (Shared Skill)

## Purpose

This skill guides the creation of `corpus-config.json` files for application (software) projects, enabling them to be managed as CorpusHub corpora.

## When to Use the Application Project Template

Use the application project template when:

- You have a software project with structured documentation (requirements, design docs, API specs, etc.)
- You want to use CorpusHub's review, commenting, and consistency-checking features on project artifacts
- You need to track cross-references between requirements, architecture, and implementation docs
- You want AI-assisted review of application project documentation

The template is located at:
```
G:\My Drive\Projects\CorpusHub\plugins\templates\application-project\corpus-config.json
```

---

## Common Artifact Types for Software Projects

The application project template includes these artifact types by default:

| Artifact Type | Default Path | Extensions | Description |
|---------------|-------------|------------|-------------|
| `requirements` | `docs/requirements/` | `.md`, `.html`, `.yaml` | Functional and non-functional requirements |
| `system-design` | `docs/design/` | `.md`, `.html` | System design documents and diagrams |
| `api-specs` | `docs/api/` | `.md`, `.yaml`, `.json` | OpenAPI specs, endpoint docs |
| `architecture` | `docs/architecture/` | `.md`, `.html` | High-level architecture descriptions |
| `data-models` | `docs/data-models/` | `.md`, `.sql`, `.prisma` | Database schemas, entity models |
| `decisions` | `docs/decisions/` | `.md` | Architecture Decision Records (ADRs) |

You can add, remove, or rename these to match your project structure.

---

## Customizing Framework Categories

The template includes two default framework categories:

### Quality Attributes
Terms like `scalability`, `reliability`, `security`, `performance`. These are matched at word boundaries in your artifacts for consistency scanning.

### Design Patterns
Terms like `microservices`, `event-driven`, `CQRS`, `saga`. Matched case-insensitively.

### How to Customize

Add categories relevant to your project domain:

```json
{
  "id": "business-domain",
  "label": "Business Domain Terms",
  "terms": ["invoice", "payment", "subscription", "tenant"],
  "matchMode": "case-insensitive"
}
```

Add project-specific stakeholders:

```json
{
  "id": "stakeholders",
  "label": "Stakeholders",
  "terms": ["product-owner", "platform-team", "security-team", "SRE"],
  "matchMode": "case-insensitive"
}
```

**matchMode options:**
- `word-boundary` -- matches whole words only
- `case-insensitive` -- matches regardless of case

---

## Step-by-Step: Setting Up a New Application Project Corpus

### 1. Copy the template

```bash
cp "G:\My Drive\Projects\CorpusHub\plugins\templates\application-project\corpus-config.json" \
   /path/to/your-project/corpus-config.json
```

### 2. Customize identity

Open `corpus-config.json` and update the `corpus` section:

```json
{
  "corpus": {
    "name": "My App Project",
    "description": "Artifact corpus for the My App project",
    "version": "1.0.0",
    "baseDir": "."
  }
}
```

`baseDir` is relative to the project root. Use `"."` to resolve artifact paths from the project root.

### 3. Customize artifact paths

Adjust the `artifacts` section to match your project's directory layout. For example, if your docs live in `documentation/` instead of `docs/`:

```json
{
  "requirements": {
    "path": "documentation/requirements",
    "label": "Requirements",
    "extensions": [".md"]
  }
}
```

Remove artifact types you don't use. Add custom ones if needed:

```json
{
  "runbooks": {
    "path": "ops/runbooks",
    "label": "Runbooks",
    "extensions": [".md"]
  }
}
```

### 4. Place at project root

The `corpus-config.json` file must be at the root of your project directory:

```
my-project/
  corpus-config.json    <-- here
  docs/
    requirements/
    design/
    api/
  src/
  ...
```

### 5. Register via API

```bash
curl -X POST http://localhost:3000/api/corpora/register \
  -H "Content-Type: application/json" \
  -d '{"path": "/absolute/path/to/my-project"}'
```

This registers the corpus with CorpusHub. The server will:
- Read the `corpus-config.json` from the given path
- Create a slug from the corpus name
- Create an isolated SQLite database in `data/corpora/<slug>.db`
- Index all artifacts found at the configured paths

### 6. Switch to the new corpus

```bash
curl -X POST http://localhost:3000/api/corpora/switch \
  -H "Content-Type: application/json" \
  -d '{"slug": "my-app-project"}'
```

### 7. Verify

```bash
# Confirm active corpus
curl http://localhost:3000/api/corpora/active

# List indexed artifacts
curl http://localhost:3000/api/artifacts
```

---

## Tips

- Keep `corpus-config.json` in version control alongside your project docs
- Use the consistency engine to enforce framework term usage across all artifacts
- For monorepos with multiple sub-projects, register each sub-project as a separate corpus
- The `voice` field can be set to `null` for application projects where writing style guidelines are not needed
- ADRs (Architecture Decision Records) work well as the `decisions` artifact type -- each ADR is a separate markdown file
