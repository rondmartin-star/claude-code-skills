# America 4.0 Review & Update System Orchestrator

## Overview

This skill orchestrates the America 4.0 Review & Update System, routing requests to specialized sub-skills based on the current user role and task context.

## When to Activate

Activate when the user is working with:
- America 4.0 framework documents (specifications, marketing, publications)
- The Reference Hub webapp (`07-webapp/`)
- Framework consistency and cross-reference management
- Content creation aligned with the 7 principles and 14 roles

## User Roles

### Reviewer Role
Navigates artifacts and adds comments/annotations. Periodically requests change plans.
- Route to: `review/review-orchestrator`
- Capabilities: Add comments, generate plans, track resolutions

### Editor Role
Makes direct changes and monitors consistency implications.
- Route to: `edit/edit-orchestrator`
- Capabilities: Edit artifacts, preview consistency, version history

### Author Role
Requests Claude to draft new content with framework alignment.
- Route to: `author/author-orchestrator`
- Capabilities: Generate drafts, analyze implications, commit with updates

## Role Detection

Detect role from:
1. Explicit user statement ("as a reviewer...", "I'm editing...")
2. Task context (adding comments = reviewer, direct edits = editor, new content = author)
3. Default to viewer if unclear

## Framework Context

Always load these canonical sources for consistency:
- Principles: `03-specifications/v1.0/america40.comprehensive-framework-synthesis-streamlined.md`
- Roles: `03-specifications/v1.0/america40.stakeholder-roles.md`
- Style: `04-marketing/messaging/america40-style-guide.md`

## Routing Logic

```
IF task involves adding comments or reviewing:
  → review/review-orchestrator

IF task involves direct file editing:
  → edit/edit-orchestrator

IF task involves creating new content:
  → author/author-orchestrator

IF task involves consistency checking:
  → shared/consistency-engine

IF task involves applying approved changes:
  → shared/implementation-executor

IF task involves backup or restore:
  → shared/backup-archive

IF task involves framework context lookup:
  → shared/framework-context
```

## Backup Protocol

**Before ANY modification:**
1. Create pre-operation backup via `/api/backup`
2. Execute the operation
3. Verify with consistency check
4. On failure: auto-rollback via `/api/restore`

**Backup Types:**
- `full`: Complete snapshot of all artifacts + database
- `incremental`: Only changed files since last backup
- `selective`: Specific artifact types only

## Key Principles

1. **Framework Alignment**: All content must align with the 7 immutable principles
2. **Consistency Tracking**: Monitor cross-references across documents
3. **Version Control**: Create versions before any modifications
4. **Voice Consistency**: Maintain bridge-building, practical idealism tone

## API Endpoints (Reference Hub)

- Comments: `POST/GET /api/comments`
- Plans: `POST /api/plans/generate`, `PUT /api/plans/:id/status`
- Versions: `GET /api/artifacts/:type/:name/history`
- Consistency: `POST /api/artifacts/:type/:name/preview-changes`
- Drafts: `POST /api/drafts/generate`, `POST /api/drafts/:id/analyze-implications`

## Error Handling

- If consistency issues detected: Present to user before proceeding
- If API errors: Graceful degradation with clear error messages
- If framework violations: Flag and require explicit override
