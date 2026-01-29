# Backup and Archive Skill

## Purpose

Provides robust backup, archive, and recovery capabilities for America 4.0 framework artifacts. Ensures data protection, version history, and disaster recovery.

## Capabilities

### 1. Automatic Backup

**Triggers:**
- Before any artifact modification (save, revert, plan execution)
- Before bulk operations (consistency scan, plan batch apply)
- Scheduled daily backup of all artifacts
- Manual backup on demand

**Backup Types:**
- **Incremental**: Only changed files since last backup
- **Full**: Complete snapshot of all artifacts
- **Selective**: Specific artifact types or directories

### 2. Archive System

**Archive Structure:**
```
backups/
├── daily/
│   ├── 2026-01-28/
│   │   ├── manifest.json
│   │   ├── artifacts.tar.gz
│   │   └── database.sqlite.bak
│   └── ...
├── weekly/
│   └── 2026-W04/
├── monthly/
│   └── 2026-01/
└── manual/
    └── pre-major-change-20260128/
```

**Retention Policy:**
- Daily: 7 days
- Weekly: 4 weeks
- Monthly: 12 months
- Manual: Indefinite (user-managed)

### 3. Recovery Operations

**Recovery Modes:**
- **Point-in-Time**: Restore to any backup timestamp
- **Single Artifact**: Restore specific file only
- **Full Restore**: Complete rollback to backup state
- **Selective Restore**: Choose specific artifacts to recover

### 4. Verification

**Integrity Checks:**
- SHA-256 hash verification for all archived files
- Manifest validation on restore
- Database consistency check before backup
- Automatic corruption detection

## API Endpoints

### Backup Operations

```javascript
// Create manual backup
POST /api/backup
{
  type: 'full' | 'incremental' | 'selective',
  name: 'optional-backup-name',
  artifact_types: ['specifications', 'infographics']  // for selective
}
Response: { backup_id, path, manifest, created_at }

// List available backups
GET /api/backups
Response: [{ id, type, name, created_at, size, artifact_count }]

// Get backup details
GET /api/backups/:id
Response: { manifest, artifacts: [{path, hash, size}] }

// Delete backup
DELETE /api/backups/:id
```

### Recovery Operations

```javascript
// Preview restore (dry run)
POST /api/restore/preview
{
  backup_id: 'backup-id',
  mode: 'full' | 'artifact' | 'selective',
  artifacts: ['path/to/file']  // for artifact/selective modes
}
Response: { affected_files, current_versions, backup_versions }

// Execute restore
POST /api/restore
{
  backup_id: 'backup-id',
  mode: 'full' | 'artifact' | 'selective',
  artifacts: [],
  create_backup_first: true  // recommended
}
Response: { restored_count, backup_created_id }
```

### Archive Management

```javascript
// Apply retention policy (cleanup old backups)
POST /api/archive/cleanup
Response: { removed: [{ id, reason }], kept: [] }

// Export archive (downloadable)
GET /api/archive/export/:backup_id
Response: Binary tar.gz file

// Import archive
POST /api/archive/import
Content-Type: multipart/form-data
Response: { backup_id, imported_count }
```

## Pre-Operation Backup Protocol

**Before ANY modification:**

```javascript
async function safeModify(operation) {
  // 1. Create pre-operation backup
  const backup = await createBackup({
    type: 'incremental',
    name: `pre-${operation.type}-${Date.now()}`
  });

  // 2. Execute operation
  try {
    const result = await operation.execute();

    // 3. Verify result
    if (!await verifyIntegrity()) {
      throw new Error('Post-operation integrity check failed');
    }

    return result;
  } catch (error) {
    // 4. Auto-rollback on failure
    await restore({
      backup_id: backup.id,
      mode: 'full'
    });
    throw error;
  }
}
```

## Database Backup

**SQLite Backup Strategy:**
- Hot backup using `.backup` command
- WAL checkpoint before backup
- Verify backup integrity before archiving

```javascript
// Backup database
POST /api/backup/database
Response: { backup_path, size, verified: true }

// Restore database
POST /api/restore/database
{ backup_id }
Response: { restored: true, rows_restored: 1234 }
```

## Manifest Format

```json
{
  "version": "1.0",
  "created_at": "2026-01-28T14:30:00Z",
  "type": "full",
  "name": "daily-backup",
  "framework_version": "1.0",
  "artifacts": [
    {
      "path": "specifications/v1.0/core-specification.md",
      "type": "specifications",
      "hash": "sha256:abc123...",
      "size": 45678,
      "modified_at": "2026-01-27T10:00:00Z"
    }
  ],
  "database": {
    "path": "users.db.bak",
    "hash": "sha256:def456...",
    "tables": ["users", "comments", "versions"],
    "row_counts": { "users": 5, "comments": 123, "versions": 456 }
  },
  "total_size": 1234567,
  "integrity_verified": true
}
```

## Integration Points

### With Versioning System
- Backup includes version history tables
- Restore preserves version continuity
- Cross-reference backup ID in version records

### With Consistency Engine
- Backup consistency references
- Verify framework integrity after restore
- Flag any post-restore inconsistencies

### With Plan Execution
- Auto-backup before plan implementation
- Link backup to plan record
- Enable plan rollback via backup

## Monitoring and Alerts

**Health Checks:**
- Last backup age (alert if > 24 hours)
- Backup size trends (detect anomalies)
- Integrity verification status
- Storage capacity monitoring

**Notifications:**
- Backup completed successfully
- Backup failed with error
- Storage approaching capacity
- Integrity check failure detected
