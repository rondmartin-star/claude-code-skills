# CorpusHub Orchestrator

## Purpose

The Orchestrator is the main entry point for CorpusHub operations. It determines the user's intent and routes to the appropriate role skill.

## Intent Detection

Analyze the user's request and route to the correct skill:

| Intent | Route To | Trigger Keywords |
|--------|----------|-----------------|
| **Initialize** | `setup/corpus-init/SKILL.md` | init, initialize, setup new, enable corpus, create corpus, corpus-enable new |
| **Convert** | `setup/corpus-convert/SKILL.md` | convert, enable existing, add corpus to project, migrate to corpus, corpus-enable existing |
| **Review** | `reviewer/SKILL.md` | browse, review, comment, feedback, change plan, approve |
| **Edit** | `editor/SKILL.md` | edit, modify, update, rewrite, change content, revert |
| **Author** | `author/SKILL.md` | create, draft, new, write, generate, author |
| **Admin** | `admin/SKILL.md` | backup, restore, users, health, scan, cleanup |

If the intent is ambiguous, ask the user to clarify their role for this session.

## Available Operations by Role

### Setup (Corpus Enablement)
- Initialize new projects as corpus-enabled
- Convert existing projects to use CorpusHub
- Auto-detect project structure and generate configuration
- Create directory structure and register with CorpusHub
- **corpus-init**: For new/greenfield projects
- **corpus-convert**: For existing projects with documentation

### Reviewer
- Browse and search artifacts
- Add comments with type (suggestion, issue, question, praise) and priority
- Generate change plans from grouped comments
- Approve or reject change plans
- Reply to existing comments

### Editor
- View and modify artifact content
- Use AI assistance for edits
- Preview changes before committing
- Browse version history and revert to prior versions

### Author
- Generate new drafts with AI assistance
- Specify content type, target location, and context artifacts
- Analyze implications of new content on existing corpus
- Iterate on drafts before publishing

### Admin
- Manage users and roles
- Create and restore backups (full, selective, incremental)
- Run consistency scans across the corpus
- Monitor system health and statistics
- Clean up old archives

## API Base

All endpoints use: `http://localhost:3000`

## Common First Steps

Regardless of role, these calls help orient the session:

```bash
# Check server is running
curl http://localhost:3000/api/health

# Check active corpus (always do this first)
curl http://localhost:3000/api/corpora/active

# List all artifact types and names
curl http://localhost:3000/api/artifacts

# Get system stats (artifact counts, recent activity)
curl http://localhost:3000/api/admin/stats
```

## Workflow

1. **Corpus Selection** (always first):
   a. Check if a corpus is active: `GET /api/corpora/active`
   b. If active, confirm with the user and proceed to step 2
   c. If not active, list available corpora: `GET /api/corpora`
   d. If corpora are available, present them and let the user choose, then switch: `POST /api/corpora/switch` with `{"slug": "chosen-slug"}`
   e. If no corpora are registered, guide the user to set one up:
      - **Recommended**: Use `corpus-init` (new project) or `corpus-convert` (existing project) skills
      - **Alternative**: Manually place a `corpus-config.json` at the project root and register via `POST /api/corpora/register`
2. Greet the user and determine intent
3. If needed, check server health first
4. Route to the appropriate role skill
5. If the user's request spans multiple roles (e.g., "review then edit"), handle sequentially -- complete the review workflow before switching to editor
6. For shared concerns (consistency, config, backup), reference the appropriate shared skill

## Error Handling

- If the server is unreachable, advise the user to start it: `cd "G:\My Drive\Projects\CorpusHub" && node server.js`
- If an endpoint returns 404, the artifact or resource may not exist -- confirm the name/type
- If 403, the user's role may lack permission for that operation
