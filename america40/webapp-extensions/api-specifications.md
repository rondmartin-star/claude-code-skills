# America 4.0 Reference Hub API Specifications

## Base URL

```
http://localhost:3000/api
```

## Authentication

Most endpoints require authentication via Google OAuth. Include session cookie from login.
Setup and health endpoints are public.

## Roles

| Role | Permissions |
|------|-------------|
| admin | Full access, user management, restore, delete |
| editor | Create, edit, comment, generate plans and drafts |
| viewer | Read-only access to artifacts, add comments |
| pending | No access until approved |

---

## Setup Endpoints (Public)

### GET /api/setup/status
Check if initial configuration is required.

**Response:**
```json
{
  "setup_required": true,
  "configured": {
    "google_oauth": false,
    "anthropic_api": false,
    "session_secret": false,
    "base_url": false
  }
}
```

### POST /api/setup/configure
Save initial configuration. Credentials are encrypted with AES-256-GCM.

**Request:**
```json
{
  "google_client_id": "xxxxx.apps.googleusercontent.com",
  "google_client_secret": "GOCSPX-xxxxx",
  "anthropic_api_key": "sk-ant-api03-xxxxx",
  "session_secret": "random-string",
  "base_url": "http://localhost:3000"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Configuration saved successfully",
  "restart_required": false
}
```

### POST /api/setup/test
Test API credentials before saving.

**Request:**
```json
{
  "anthropic_api_key": "sk-ant-api03-xxxxx"
}
```

**Response:**
```json
{
  "anthropic": { "valid": true }
}
```

---

## User Endpoints

### GET /api/user
Get current authenticated user.

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "User Name",
  "picture": "https://...",
  "role": "editor"
}
```

### GET /api/admin/users
List all users (admin only).

### PUT /api/admin/users/:id/role
Update user role (admin only).

### DELETE /api/admin/users/:id
Delete user (admin only).

---

## Artifact Endpoints

### GET /api/artifacts
List all available artifacts.

**Response:**
```json
[
  {
    "name": "document.html",
    "type": "infographics",
    "path": "infographics/document.html",
    "extension": ".html"
  }
]
```

### GET /api/artifacts/:type/:name
Get artifact content.

**Response:**
```json
{
  "name": "document.html",
  "type": "infographics",
  "extension": ".html",
  "content": "...",
  "isHtml": true,
  "isMarkdown": false
}
```

### PUT /api/artifacts/:type/:name
Save artifact (editor/admin only). Creates version automatically.

**Request:**
```json
{
  "content": "new content",
  "change_summary": "Description of changes"
}
```

---

## Comment Endpoints

### POST /api/comments
Create new comment.

**Request:**
```json
{
  "artifact_type": "specifications",
  "artifact_name": "document.md",
  "selection_text": "selected text",
  "selection_start": 100,
  "selection_end": 120,
  "comment_text": "My comment",
  "comment_type": "suggestion",
  "priority": "normal"
}
```

### GET /api/comments/:type/:name
Get comments for artifact.

**Query params:** `status=open`

### PUT /api/comments/:id/status
Update comment status.

**Request:**
```json
{
  "status": "resolved",
  "resolution_note": "Fixed in version 3"
}
```

### POST /api/comments/:id/replies
Add reply to comment.

### GET /api/comments/:id/replies
Get replies for comment.

---

## Plan Endpoints

### POST /api/plans/generate
Generate change plan from comments.

**Request:**
```json
{
  "artifact_type": "specifications",
  "artifact_name": "document.md",
  "scope": "artifact"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Change Plan - 2026-01-28",
  "status": "pending_review",
  "plan_summary": "...",
  "plan_details": "..."
}
```

### GET /api/plans
List all plans.

### GET /api/plans/:id
Get plan details with linked comments.

### PUT /api/plans/:id/status
Approve or reject plan.

**Request:**
```json
{
  "status": "approved"
}
```

---

## Version History Endpoints

### GET /api/artifacts/:type/:name/history
Get version history for artifact.

**Response:**
```json
[
  {
    "version_number": 3,
    "content_hash": "sha256:...",
    "change_source": "direct_edit",
    "user_name": "Editor Name",
    "change_summary": "Updated introduction",
    "created_at": "2026-01-28T14:30:00Z"
  }
]
```

### GET /api/artifacts/:type/:name/version/:version
Get specific version content.

### POST /api/artifacts/:type/:name/revert/:version
Revert to specific version (creates new version).

---

## Consistency Endpoints

### POST /api/artifacts/:type/:name/preview-changes
Preview consistency implications before saving.

**Request:**
```json
{
  "newContent": "modified content"
}
```

**Response:**
```json
{
  "changes": [
    {
      "type": "principle",
      "term": "Human Dignity",
      "change": "added",
      "count_change": 2
    }
  ],
  "analysis": "{...}"
}
```

### POST /api/consistency/scan
Run full framework consistency scan.

### GET /api/consistency/issues
Get detected consistency issues.

### GET /api/consistency/references
Get framework reference map.

---

## Draft Endpoints (Author Role)

### POST /api/drafts/generate
Generate new draft with Claude.

**Request:**
```json
{
  "content_type": "article",
  "title": "New Article Title",
  "prompt": "Write about democratic renewal",
  "target_location": "optional/path"
}
```

### GET /api/drafts
List user's drafts.

### GET /api/drafts/:id
Get draft content.

### PUT /api/drafts/:id
Update draft.

### POST /api/drafts/:id/analyze-implications
Analyze framework implications of draft.

---

## Backup Endpoints

### POST /api/backup
Create backup.

**Request:**
```json
{
  "type": "full",
  "name": "pre-major-change"
}
```

### GET /api/backups
List all backups.

### GET /api/backups/:id
Get backup details.

### POST /api/restore
Restore from backup (admin only).

**Request:**
```json
{
  "backup_id": "backup-name",
  "mode": "full",
  "create_backup_first": true
}
```

### DELETE /api/backups/:id
Delete backup (admin only).

### POST /api/archive/cleanup
Apply retention policy (admin only).

---

## Claude Integration

### POST /api/claude
Send prompt to Claude for editing assistance.

**Request:**
```json
{
  "prompt": "Improve the introduction",
  "context": "Current document content..."
}
```

**Response:**
```json
{
  "response": "Claude's suggested text...",
  "usage": { "input_tokens": 100, "output_tokens": 500 }
}
```

---

## Health Endpoints (Public)

### GET /api/health
Full health check with metrics.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-28T14:30:00Z",
  "uptime": {
    "ms": 3600000,
    "formatted": "0d 1h 0m 0s"
  },
  "server": {
    "nodeVersion": "v20.10.0",
    "platform": "win32",
    "memoryUsage": { ... },
    "pid": 12345
  },
  "database": {
    "status": "connected",
    "path": "/path/to/users.db"
  },
  "metrics": {
    "requestCount": 1234,
    "errorCount": 2
  }
}
```

### GET /api/health/live
Kubernetes liveness probe.

**Response:**
```json
{
  "status": "alive",
  "timestamp": "2026-01-28T14:30:00Z"
}
```

### GET /api/health/ready
Kubernetes readiness probe.

**Response:**
```json
{
  "status": "ready",
  "timestamp": "2026-01-28T14:30:00Z"
}
```

---

## Admin Stats Endpoint

### GET /api/admin/stats
Server statistics (admin only).

**Response:**
```json
{
  "users": 5,
  "comments": 23,
  "plans": 3,
  "versions": 45,
  "drafts": 7,
  "server": {
    "uptime": 3600000,
    "requests": 1234,
    "errors": 2
  }
}
```

---

## Review Comments Endpoint

### GET /api/review/comments
Get all comments with filters (for review dashboard).

**Query params:** `status=open`, `artifact_type=specifications`

**Response:**
```json
[
  {
    "id": 1,
    "artifact_type": "specifications",
    "artifact_name": "framework.md",
    "user_name": "Reviewer Name",
    "comment_text": "...",
    "status": "open",
    "created_at": "2026-01-28T10:00:00Z"
  }
]
```

---

## Error Responses

All errors return:

```json
{
  "error": "Error message description"
}
```

HTTP Status Codes:
- 200: Success
- 400: Bad Request (missing/invalid params)
- 401: Unauthorized (not logged in)
- 403: Forbidden (insufficient permissions)
- 404: Not Found
- 500: Internal Server Error
- 503: Service Unavailable (API not configured)
