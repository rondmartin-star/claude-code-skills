# CorpusHub Editor Skill

## Purpose

The Editor skill enables modifying artifact content, using AI assistance for edits, previewing changes, and managing version history.

## API Base

`http://localhost:3000`

---

## View Artifact

### Get artifact content
```bash
curl http://localhost:3000/api/artifacts/{type}/{name}
```
Returns the full artifact including `content`, `metadata`, `version`, and `last_modified`.

---

## Edit Artifact

### Update artifact content
```bash
curl -X PUT http://localhost:3000/api/artifacts/{type}/{name} \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# Introduction\n\nThe revised opening paragraph...",
    "change_summary": "Rewrote opening paragraph for stronger thesis"
  }'
```

**Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `content` | string | yes | The full updated artifact content |
| `change_summary` | string | yes | Brief description of what changed |

The server automatically increments the version number and stores the previous version in history.

---

## AI Assistance

### Request AI help for editing
```bash
curl -X POST http://localhost:3000/api/claude \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Rewrite this paragraph to be more concise while keeping the key arguments",
    "context": "The current paragraph text goes here..."
  }'
```

**Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt` | string | yes | What you want the AI to do |
| `context` | string | no | Relevant content for the AI to work with |

Returns an AI-generated response that can be used to update the artifact.

---

## Preview Changes

### Preview changes before committing
```bash
curl -X POST http://localhost:3000/api/artifacts/{type}/{name}/preview-changes \
  -H "Content-Type: application/json" \
  -d '{
    "newContent": "The updated content to preview..."
  }'
```

Returns a diff-style comparison between current and proposed content, including:
- Added/removed/changed sections
- Consistency implications (references to framework terms, other artifacts)
- Word count delta

Use this before committing edits to understand the full impact.

---

## Version History

### View version history
```bash
curl http://localhost:3000/api/artifacts/{type}/{name}/history
```
Returns an array of version records with `version`, `change_summary`, `timestamp`, and `author`.

### View a specific version
```bash
curl http://localhost:3000/api/artifacts/{type}/{name}/version/{version}
```
Returns the full artifact content as it existed at that version number.

### Revert to a previous version
```bash
curl -X POST http://localhost:3000/api/artifacts/{type}/{name}/revert/{version}
```
Reverts the artifact to the specified version. This creates a new version entry (it does not delete history). The change summary is auto-generated as "Reverted to version {N}".

---

## Typical Editor Workflow

1. **Review plan**: Check approved change plans (`GET /api/plans?status=approved`)
2. **Read artifact**: `GET /api/artifacts/{type}/{name}` to see current content
3. **AI assist** (optional): `POST /api/claude` to get AI-generated suggestions
4. **Preview**: `POST /api/artifacts/{type}/{name}/preview-changes` to see the diff
5. **Commit**: `PUT /api/artifacts/{type}/{name}` to save changes
6. **Verify**: `GET /api/artifacts/{type}/{name}` to confirm the update

## Tips

- Always include a meaningful `change_summary` -- it becomes the version history entry
- Use preview-changes to catch consistency issues before committing
- If an edit goes wrong, check history and revert rather than trying to manually undo
- For large edits, break them into logical chunks with separate change summaries
- The AI assist endpoint respects the corpus config's voice and framework terms
- After editing, consider running a consistency scan (see `shared/consistency-engine/SKILL.md`)
