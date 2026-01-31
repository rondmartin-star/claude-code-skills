# Backup & Restore

**Purpose:** Corpus backup and disaster recovery

**Size:** 12.3 KB

---

## Quick Start

```javascript
// Create backup
const backup = await createFullBackup('/path/to/corpus');

// List backups
const backups = await listBackups('/path/to/corpus');

// Restore
await restoreFromBackup('/path/to/corpus', backupPath);
```

## What It Does

- Creates full and incremental backups
- Manages retention policies
- Compresses backups (ZIP)
- Restores from backup points
- Selective artifact restoration
- Automated scheduled backups

## Backup Types

- **Full:** Complete corpus snapshot
- **Incremental:** Changed files only

## Retention Policy

- Daily: Keep 7 days
- Weekly: Keep 4 weeks
- Monthly: Keep 12 months

---

**Part of:** v4.0.0 Universal Skills  
**Category:** Utilities  
**Integration:** CorpusHub API
