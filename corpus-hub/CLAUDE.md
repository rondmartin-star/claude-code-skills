# CorpusHub Skill Ecosystem

## Overview

CorpusHub is a plugin-based corpus management platform located at `G:\My Drive\Projects\CorpusHub`. It provides tools for reviewing, editing, authoring, and administering structured document corpora through a web interface and REST API.

## Architecture

- **Backend**: Express.js server with SQLite database
- **Frontend**: Vanilla JavaScript (no framework)
- **API**: REST endpoints at `http://localhost:3000`
- **Plugin System**: Each corpus is defined by a `corpus-config.json` file under `plugins/<name>/`
- **Data Storage**: SQLite for metadata, comments, plans; filesystem for artifact content

## Plugin System

Each corpus plugin is configured via `corpus-config.json`, which defines:
- **Artifacts**: Document types, their locations, and metadata
- **Framework Terms**: Domain-specific vocabulary and definitions for consistency
- **Voice**: Tone, style, and writing guidelines
- **Roles**: User roles and their permissions (reviewer, editor, author, admin)

## Available Skills

| Skill | Path | Purpose |
|-------|------|---------|
| **Orchestrator** | `corpus-hub-orchestrator/` | Entry point -- determines intent and routes to role skills |
| **Corpus Init** | `setup/corpus-init/` | Initialize new projects as corpus-enabled with interactive prompts |
| **Corpus Convert** | `setup/corpus-convert/` | Convert existing projects to corpus-enabled (preserves original files) |
| **Reviewer** | `reviewer/` | Browse artifacts, add comments, generate and manage change plans |
| **Editor** | `editor/` | Modify artifacts, use AI assistance, manage version history |
| **Author** | `author/` | Create new drafts, analyze implications, AI-assisted writing |
| **Admin** | `admin/` | User management, backups, consistency scans, system health |
| **Consistency Engine** | `shared/consistency-engine/` | Cross-artifact consistency scanning and issue tracking |
| **Corpus Config** | `shared/corpus-config/` | Understanding and managing corpus-config.json |
| **Project Templates** | `shared/project-templates/` | Creating corpus-config.json for application projects |
| **Backup & Archive** | `shared/backup-archive/` | Backup creation, restoration, and archive cleanup |

## How to Use

1. **First time setup?** Use `corpus-init` (new project) or `corpus-convert` (existing project) to enable CorpusHub for your project.
2. **Start with the Orchestrator** -- it will determine your intent and route you to the correct role skill.
3. If you already know your role, jump directly to the relevant skill (reviewer, editor, author, or admin).
4. Shared skills are referenced by role skills as needed; you rarely invoke them directly.

## Common Patterns

All API calls use the base URL `http://localhost:3000`. JSON request/response bodies. Standard HTTP methods (GET, POST, PUT, DELETE).

```bash
# Health check
curl http://localhost:3000/api/health

# List all artifacts
curl http://localhost:3000/api/artifacts

# Get system stats
curl http://localhost:3000/api/admin/stats
```

## Multi-Corpus Support

CorpusHub supports multiple corpora via hot-swap. Each project can register its own corpus, and you can switch between them at runtime.

### Corpus Management Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/corpora` | List all registered corpora |
| `GET` | `/api/corpora/active` | Get the currently active corpus |
| `POST` | `/api/corpora/register` | Register a project folder (admin only) |
| `POST` | `/api/corpora/switch` | Switch the active corpus |
| `DELETE` | `/api/corpora/:slug` | Unregister a corpus (admin only) |

### Project-Root Convention

Projects are discovered by placing a `corpus-config.json` at the project root. A template for application projects exists at `plugins/templates/application-project/corpus-config.json`.

### Important: Always Check Active Corpus First

Before performing any corpus operations, check which corpus is currently active:

```bash
curl http://localhost:3000/api/corpora/active
```

This ensures you are reading/writing artifacts in the correct corpus context. If no corpus is active, list available corpora with `GET /api/corpora` and switch to one.

### Per-Corpus Data Isolation

Each registered corpus gets its own SQLite database stored in `data/corpora/`. This ensures complete isolation of metadata, comments, and plans between corpora.

## Project Location

- **Source code**: `G:\My Drive\Projects\CorpusHub`
- **Server entry**: `server.js`
- **Plugins directory**: `plugins/`
- **Database (legacy)**: `data/corpushub.db`
- **Per-corpus databases**: `data/corpora/<slug>.db`
