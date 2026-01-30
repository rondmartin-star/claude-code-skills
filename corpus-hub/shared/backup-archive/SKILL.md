# CorpusHub Backup & Archive (Shared Skill)

## Purpose

This skill covers backup creation, restoration, management, and archive cleanup operations. It provides detailed guidance for protecting corpus data.

## API Base

`http://localhost:3000`

---

## Create Backup

### Full backup
```bash
curl -X POST http://localhost:3000/api/backup \
  -H "Content-Type: application/json" \
  -d '{
    "type": "full",
    "name": "pre-release-backup"
  }'
```

### Selective backup (specific artifact types only)
```bash
curl -X POST http://localhost:3000/api/backup \
  -H "Content-Type: application/json" \
  -d '{
    "type": "selective",
    "name": "chapters-only",
    "artifact_types": ["chapter", "appendix"]
  }'
```

### Incremental backup (changes since last backup)
```bash
curl -X POST http://localhost:3000/api/backup \
  -H "Content-Type: application/json" \
  -d '{
    "type": "incremental",
    "name": "daily-incremental"
  }'
```

**Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | yes | `full`, `selective`, or `incremental` |
| `name` | string | yes | Human-readable backup name |
| `artifact_types` | array | selective only | Which artifact types to include |

**Response:**
```json
{
  "backup_id": "backup-2025-01-15-001",
  "type": "full",
  "name": "pre-release-backup",
  "timestamp": "2025-01-15T10:30:00Z",
  "size_bytes": 2457600,
  "artifact_count": 42,
  "status": "completed"
}
```

---

## List Backups

```bash
curl http://localhost:3000/api/backups
```

Returns an array of backup records sorted by timestamp (newest first), each containing `backup_id`, `type`, `name`, `timestamp`, `size_bytes`, `artifact_count`, and `status`.

---

## Backup Details

```bash
curl http://localhost:3000/api/backups/{backup_id}
```

Returns full backup details including the manifest -- a list of every artifact included with its type, name, version, and checksum.

### Manifest Format

```json
{
  "backup_id": "backup-2025-01-15-001",
  "manifest": [
    {
      "artifact_type": "chapter",
      "artifact_name": "introduction",
      "version": 5,
      "checksum": "sha256:abc123...",
      "size_bytes": 15360
    }
  ]
}
```

The manifest enables selective restore -- you can pick individual artifacts from a backup.

---

## Restore from Backup

### Full restore
```bash
curl -X POST http://localhost:3000/api/restore \
  -H "Content-Type: application/json" \
  -d '{
    "backup_id": "backup-2025-01-15-001",
    "mode": "full",
    "create_backup_first": true
  }'
```

### Selective restore (specific artifacts only)
```bash
curl -X POST http://localhost:3000/api/restore \
  -H "Content-Type: application/json" \
  -d '{
    "backup_id": "backup-2025-01-15-001",
    "mode": "selective",
    "artifacts": [
      {"type": "chapter", "name": "introduction"},
      {"type": "chapter", "name": "economic-policy"}
    ],
    "create_backup_first": true
  }'
```

**Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `backup_id` | string | yes | ID of the backup to restore from |
| `mode` | string | yes | `full` or `selective` |
| `artifacts` | array | selective only | Specific artifacts to restore |
| `create_backup_first` | boolean | no | Create a safety backup before restoring (default: false) |

Always set `create_backup_first: true` for production restores as a safety net.

---

## Delete a Backup

```bash
curl -X DELETE http://localhost:3000/api/backups/{backup_id}
```

Permanently removes the backup. This cannot be undone.

---

## Archive Cleanup

### Remove old backups by retention period
```bash
curl -X POST http://localhost:3000/api/archive/cleanup \
  -H "Content-Type: application/json" \
  -d '{"retention_days": 90}'
```

**Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `retention_days` | number | yes | Delete backups older than this many days |

**Response:**
```json
{
  "deleted_count": 3,
  "freed_bytes": 7340032,
  "remaining_count": 12
}
```

---

## Backup Strategy Recommendations

| Scenario | Backup Type | Frequency |
|----------|-------------|-----------|
| Daily protection | incremental | Daily |
| Before major edits | full | As needed |
| Before release | full | Per release |
| Specific artifact work | selective | As needed |
| Archive cleanup | -- | Monthly |

## Tips

- Use `create_backup_first: true` on every restore operation
- Name backups descriptively (e.g., "pre-v2-release", "before-chapter-rewrite")
- Check backup details/manifest before restoring to confirm contents
- Incremental backups are fast but require the base full backup to exist
- Set retention_days in corpus-config.json settings for consistent cleanup policy
