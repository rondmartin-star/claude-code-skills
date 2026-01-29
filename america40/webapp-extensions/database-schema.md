# America 4.0 Reference Hub Database Schema

## Database

SQLite database: `07-webapp/users.db`

---

## Tables

### users
Core user authentication and roles.

```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  google_id TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  picture TEXT,
  role TEXT DEFAULT 'pending',  -- admin/editor/viewer/pending
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  last_login DATETIME
);
```

---

### comments
Reviewer comments/annotations on artifacts.

```sql
CREATE TABLE comments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  artifact_type TEXT NOT NULL,
  artifact_name TEXT NOT NULL,
  user_id INTEGER NOT NULL,
  selection_start INTEGER,
  selection_end INTEGER,
  selection_text TEXT,
  section_id TEXT,
  comment_text TEXT NOT NULL,
  comment_type TEXT DEFAULT 'general',  -- general/clarification/correction/suggestion
  priority TEXT DEFAULT 'normal',        -- low/normal/high/critical
  status TEXT DEFAULT 'open',            -- open/addressed/resolved/rejected
  resolution_note TEXT,
  resolved_by INTEGER,
  resolved_at DATETIME,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (resolved_by) REFERENCES users(id)
);
```

---

### comment_replies
Threaded replies on comments.

```sql
CREATE TABLE comment_replies (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  comment_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  reply_text TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (comment_id) REFERENCES comments(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

### change_plans
Plans generated from reviewer comments.

```sql
CREATE TABLE change_plans (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  scope_type TEXT NOT NULL,              -- selected_comments/all_comments/artifact
  affected_artifacts TEXT,                -- JSON array of paths
  status TEXT DEFAULT 'draft',            -- draft/pending_review/approved/implementing/completed/rejected
  plan_summary TEXT,
  plan_details TEXT,                      -- Full Claude-generated plan (JSON)
  estimated_impact TEXT,                  -- Consistency analysis (JSON)
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  approved_at DATETIME,
  approved_by INTEGER,
  completed_at DATETIME,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (approved_by) REFERENCES users(id)
);
```

---

### plan_comments
Links comments to the plans that address them.

```sql
CREATE TABLE plan_comments (
  plan_id INTEGER NOT NULL,
  comment_id INTEGER NOT NULL,
  PRIMARY KEY (plan_id, comment_id),
  FOREIGN KEY (plan_id) REFERENCES change_plans(id),
  FOREIGN KEY (comment_id) REFERENCES comments(id)
);
```

---

### artifact_versions
Version history for all artifacts.

```sql
CREATE TABLE artifact_versions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  artifact_type TEXT NOT NULL,
  artifact_name TEXT NOT NULL,
  version_number INTEGER NOT NULL,
  content TEXT NOT NULL,
  content_hash TEXT NOT NULL,             -- SHA-256 hash
  change_source TEXT,                     -- direct_edit/plan/revert/backup/restore
  change_plan_id INTEGER,
  user_id INTEGER NOT NULL,
  change_summary TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (change_plan_id) REFERENCES change_plans(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_artifact_versions_lookup
ON artifact_versions(artifact_type, artifact_name, version_number DESC);
```

---

### drafts
Author-generated draft content.

```sql
CREATE TABLE drafts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  content_type TEXT NOT NULL,             -- post/article/specification_section
  target_location TEXT,
  content TEXT NOT NULL,
  status TEXT DEFAULT 'draft',            -- draft/editing/implications_reviewed/committed
  implications TEXT,                       -- JSON: framework implications analysis
  implications_status TEXT DEFAULT 'pending',  -- pending/reviewed/accepted/rejected
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  committed_at DATETIME,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

### framework_references
Tracks where principles, roles, and terms are referenced.

```sql
CREATE TABLE framework_references (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  artifact_type TEXT NOT NULL,
  artifact_name TEXT NOT NULL,
  reference_type TEXT NOT NULL,           -- principle/role/term/document
  reference_id TEXT NOT NULL,             -- e.g., "Human Dignity", "Citizen"
  section_id TEXT,
  line_number INTEGER,
  context_text TEXT,                      -- Surrounding text for context
  is_definition INTEGER DEFAULT 0,        -- 1 if this is THE canonical definition
  is_modified INTEGER DEFAULT 0,          -- 1 if differs from canonical
  last_verified DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

### consistency_issues
Detected consistency problems.

```sql
CREATE TABLE consistency_issues (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  issue_type TEXT NOT NULL,               -- definition_conflict/broken_reference/orphan/etc.
  severity TEXT DEFAULT 'warning',        -- critical/error/warning/info
  artifact_type TEXT NOT NULL,
  artifact_name TEXT NOT NULL,
  section_id TEXT,
  line_number INTEGER,
  description TEXT NOT NULL,
  expected_value TEXT,
  actual_value TEXT,
  status TEXT DEFAULT 'detected',         -- detected/reviewed/resolved/ignored
  resolution_note TEXT,
  resolved_by INTEGER,
  resolved_at DATETIME,
  detected_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (resolved_by) REFERENCES users(id)
);
```

---

## Relationships

```
users ──┬── comments (user_id)
        ├── comment_replies (user_id)
        ├── change_plans (user_id, approved_by)
        ├── artifact_versions (user_id)
        ├── drafts (user_id)
        └── consistency_issues (resolved_by)

comments ──── plan_comments ──── change_plans
          │
          └── comment_replies

change_plans ──── artifact_versions (change_plan_id)
```

---

## Indexes

```sql
-- Fast version lookup
CREATE INDEX idx_artifact_versions_lookup
ON artifact_versions(artifact_type, artifact_name, version_number DESC);

-- Comment lookup by artifact
CREATE INDEX idx_comments_artifact
ON comments(artifact_type, artifact_name);

-- Framework reference lookup
CREATE INDEX idx_framework_refs_type
ON framework_references(reference_type, reference_id);

-- Consistency issues by status
CREATE INDEX idx_consistency_status
ON consistency_issues(status, severity);
```

---

## Data Integrity

### Foreign Key Constraints
All tables use foreign keys referencing `users(id)` where applicable.

### Cascade Behavior
- Deleting a user: Should NOT cascade (preserve history)
- Deleting a plan: Reopens linked comments

### Soft Deletes
Consider adding `deleted_at` columns for recoverable deletion:
```sql
ALTER TABLE comments ADD COLUMN deleted_at DATETIME;
```
