# CorpusHub Admin Skill

## Purpose

The Admin skill covers user management, system health monitoring, backup/restore operations, consistency scanning, and initial system setup.

## API Base

`http://localhost:3000`

---

## User Management

### List all users
```bash
curl http://localhost:3000/api/admin/users
```

### Update a user's role
```bash
curl -X PUT http://localhost:3000/api/admin/users/{id}/role \
  -H "Content-Type: application/json" \
  -d '{"role": "editor"}'
```
**Role values:** `viewer`, `reviewer`, `editor`, `author`, `admin`

### Delete a user
```bash
curl -X DELETE http://localhost:3000/api/admin/users/{id}
```

---

## System Health

### Health check
```bash
curl http://localhost:3000/api/health
```
Returns server status, uptime, database connectivity, and plugin status.

### System statistics
```bash
curl http://localhost:3000/api/admin/stats
```
Returns artifact counts, comment counts, plan counts, recent activity, storage usage, and user counts by role.

---

## Backup & Restore

For detailed backup operations, see `shared/backup-archive/SKILL.md`.

### Quick backup
```bash
curl -X POST http://localhost:3000/api/backup \
  -H "Content-Type: application/json" \
  -d '{
    "type": "full",
    "name": "pre-release-backup"
  }'
```

### List backups
```bash
curl http://localhost:3000/api/backups
```

### Restore from backup
```bash
curl -X POST http://localhost:3000/api/restore \
  -H "Content-Type: application/json" \
  -d '{
    "backup_id": "backup-2025-01-15-001",
    "mode": "full",
    "create_backup_first": true
  }'
```

---

## Consistency Scanning

For detailed consistency operations, see `shared/consistency-engine/SKILL.md`.

### Run a full consistency scan
```bash
curl -X POST http://localhost:3000/api/consistency/scan
```
Returns a report of issues: broken references, term misuse, style deviations, orphaned artifacts.

---

## Archive Cleanup

### Clean up old archives
```bash
curl -X POST http://localhost:3000/api/archive/cleanup \
  -H "Content-Type: application/json" \
  -d '{"retention_days": 90}'
```
Removes backup archives older than the specified retention period.

---

## System Setup

### Initial configuration
```bash
curl -X POST http://localhost:3000/api/setup/configure \
  -H "Content-Type: application/json" \
  -d '{
    "admin_user": "admin",
    "corpus_name": "America 4.0",
    "plugin_path": "plugins/america-4"
  }'
```
Used for first-time setup or reconfiguration. Sets the active corpus plugin and admin credentials.

---

## Typical Admin Workflow

1. **Health check**: `GET /api/health` to confirm system is operational
2. **Stats review**: `GET /api/admin/stats` to see current state
3. **Backup**: `POST /api/backup` before any major operations
4. **Scan**: `POST /api/consistency/scan` to identify issues
5. **Cleanup**: `POST /api/archive/cleanup` to manage storage
6. **User management**: Review and adjust user roles as needed

## Tips

- Always create a backup before restore operations (use `create_backup_first: true`)
- Run consistency scans after bulk edits or imports
- Monitor system stats regularly for unusual activity
- Keep retention_days reasonable (90 days is a good default)
- The health endpoint is useful for automated monitoring or scripting
