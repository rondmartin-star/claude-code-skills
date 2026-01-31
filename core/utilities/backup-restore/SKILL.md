---
name: backup-restore
description: >
  Backup and restore utility for corpus projects. Creates timestamped backups,
  manages retention, and restores from backup points. Use when: creating backups,
  restoring previous states, or implementing disaster recovery.
---

# Backup & Restore

**Purpose:** Corpus backup and disaster recovery
**Type:** Utility Skill (Universal)

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Create backup"
- "Restore from backup"
- "Backup the corpus"
- "Rollback changes"

**Context Indicators:**
- Before major changes
- Implementing disaster recovery
- Regular backup schedule
- Testing/experimentation

---

## Backup Strategy

### 1. Backup Types

**Full Backup:**
```javascript
async function createFullBackup(corpusPath) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const backupDir = path.join(corpusPath, '.corpus', 'backups', timestamp);

  await fs.mkdir(backupDir, { recursive: true });

  // Backup corpus database
  const dbPath = path.join(corpusPath, '.corpus', 'corpus.db');
  if (fs.existsSync(dbPath)) {
    await fs.copyFile(
      dbPath,
      path.join(backupDir, 'corpus.db')
    );
  }

  // Backup configuration
  const configPath = path.join(corpusPath, 'corpus-config.json');
  if (fs.existsSync(configPath)) {
    await fs.copyFile(
      configPath,
      path.join(backupDir, 'corpus-config.json')
    );
  }

  // Backup all artifacts
  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

  for (const [name, artifact] of Object.entries(config.artifacts || {})) {
    const artifactPath = path.join(corpusPath, artifact.path);

    if (fs.existsSync(artifactPath)) {
      const backupArtifactPath = path.join(backupDir, 'artifacts', name);
      await copyRecursive(artifactPath, backupArtifactPath);
    }
  }

  // Create manifest
  const manifest = {
    timestamp,
    type: 'full',
    corpusName: config.name,
    artifacts: Object.keys(config.artifacts || {}),
    size: await calculateSize(backupDir)
  };

  await fs.writeFile(
    path.join(backupDir, 'manifest.json'),
    JSON.stringify(manifest, null, 2)
  );

  return { backupDir, manifest };
}
```

**Incremental Backup:**
```javascript
async function createIncrementalBackup(corpusPath, lastBackupTime) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const backupDir = path.join(
    corpusPath,
    '.corpus',
    'backups',
    `${timestamp}-incremental`
  );

  await fs.mkdir(backupDir, { recursive: true });

  // Only backup files modified since last backup
  const modifiedFiles = await findModifiedFiles(corpusPath, lastBackupTime);

  for (const file of modifiedFiles) {
    const relativePath = path.relative(corpusPath, file);
    const backupPath = path.join(backupDir, relativePath);

    await fs.mkdir(path.dirname(backupPath), { recursive: true });
    await fs.copyFile(file, backupPath);
  }

  const manifest = {
    timestamp,
    type: 'incremental',
    basedOn: lastBackupTime,
    filesCount: modifiedFiles.length,
    size: await calculateSize(backupDir)
  };

  await fs.writeFile(
    path.join(backupDir, 'manifest.json'),
    JSON.stringify(manifest, null, 2)
  );

  return { backupDir, manifest };
}
```

### 2. Backup Scheduling

**Configuration:**
```json
{
  "backup": {
    "enabled": true,
    "schedule": "daily",
    "retention": {
      "daily": 7,
      "weekly": 4,
      "monthly": 12
    },
    "strategy": "full",
    "compress": true,
    "location": ".corpus/backups"
  }
}
```

**Automated Backups:**
```javascript
function scheduleBackups(config) {
  const schedule = config.backup?.schedule || 'daily';

  let cronPattern;
  switch (schedule) {
    case 'hourly':
      cronPattern = '0 * * * *';
      break;
    case 'daily':
      cronPattern = '0 2 * * *';  // 2 AM daily
      break;
    case 'weekly':
      cronPattern = '0 2 * * 0';  // 2 AM Sunday
      break;
    case 'monthly':
      cronPattern = '0 2 1 * *';  // 2 AM 1st of month
      break;
  }

  cron.schedule(cronPattern, async () => {
    console.log('Running scheduled backup...');
    await createFullBackup(config.projectPath);
    await cleanupOldBackups(config);
  });
}
```

### 3. Retention Management

**Cleanup Strategy:**
```javascript
async function cleanupOldBackups(config) {
  const backupsDir = path.join(
    config.projectPath,
    config.backup?.location || '.corpus/backups'
  );

  const backups = await listBackups(backupsDir);
  const retention = config.backup?.retention || {
    daily: 7,
    weekly: 4,
    monthly: 12
  };

  // Categorize backups
  const now = new Date();
  const toKeep = new Set();
  const toDelete = [];

  // Keep daily backups
  for (let i = 0; i < retention.daily; i++) {
    const date = new Date(now);
    date.setDate(date.getDate() - i);

    const backup = findBackupForDate(backups, date);
    if (backup) toKeep.add(backup);
  }

  // Keep weekly backups
  for (let i = 0; i < retention.weekly; i++) {
    const date = new Date(now);
    date.setDate(date.getDate() - (i * 7));

    const backup = findBackupForDate(backups, date);
    if (backup) toKeep.add(backup);
  }

  // Keep monthly backups
  for (let i = 0; i < retention.monthly; i++) {
    const date = new Date(now);
    date.setMonth(date.getMonth() - i);

    const backup = findBackupForDate(backups, date);
    if (backup) toKeep.add(backup);
  }

  // Mark others for deletion
  backups.forEach(backup => {
    if (!toKeep.has(backup)) {
      toDelete.push(backup);
    }
  });

  // Delete old backups
  for (const backup of toDelete) {
    await fs.rm(backup, { recursive: true, force: true });
    console.log(`Deleted old backup: ${path.basename(backup)}`);
  }

  return {
    kept: toKeep.size,
    deleted: toDelete.length
  };
}
```

### 4. Compression

**Compress Backup:**
```javascript
async function compressBackup(backupDir) {
  const archive = archiver('zip', { zlib: { level: 9 } });
  const outputPath = `${backupDir}.zip`;
  const output = fs.createWriteStream(outputPath);

  return new Promise((resolve, reject) => {
    output.on('close', () => {
      // Remove uncompressed directory
      fs.rm(backupDir, { recursive: true, force: true });
      resolve({
        path: outputPath,
        size: archive.pointer()
      });
    });

    archive.on('error', reject);
    archive.pipe(output);
    archive.directory(backupDir, false);
    archive.finalize();
  });
}
```

---

## Restore Operations

### 1. List Available Backups

**Query Backups:**
```javascript
async function listBackups(corpusPath) {
  const backupsDir = path.join(corpusPath, '.corpus', 'backups');

  if (!fs.existsSync(backupsDir)) {
    return [];
  }

  const entries = await fs.readdir(backupsDir);
  const backups = [];

  for (const entry of entries) {
    const backupPath = path.join(backupsDir, entry);
    const manifestPath = entry.endsWith('.zip')
      ? await extractManifestFromZip(backupPath)
      : path.join(backupPath, 'manifest.json');

    if (fs.existsSync(manifestPath)) {
      const manifest = JSON.parse(
        fs.readFileSync(manifestPath, 'utf8')
      );

      backups.push({
        timestamp: manifest.timestamp,
        type: manifest.type,
        path: backupPath,
        size: manifest.size,
        compressed: entry.endsWith('.zip')
      });
    }
  }

  return backups.sort((a, b) =>
    new Date(b.timestamp) - new Date(a.timestamp)
  );
}
```

### 2. Restore from Backup

**Full Restore:**
```javascript
async function restoreFromBackup(corpusPath, backupPath, options = {}) {
  const { dryRun = false, skipDatabase = false } = options;

  // Extract if compressed
  let sourceDir = backupPath;
  if (backupPath.endsWith('.zip')) {
    sourceDir = await extractZip(backupPath);
  }

  const manifest = JSON.parse(
    fs.readFileSync(path.join(sourceDir, 'manifest.json'), 'utf8')
  );

  console.log(`Restoring backup from ${manifest.timestamp}...`);

  if (dryRun) {
    console.log('DRY RUN - No changes will be made');
    return { manifest, changes: await previewRestore(sourceDir, corpusPath) };
  }

  // Create restore point before restoring
  const restorePoint = await createFullBackup(corpusPath);
  console.log(`Created restore point: ${restorePoint.manifest.timestamp}`);

  // Restore database
  if (!skipDatabase) {
    const dbBackup = path.join(sourceDir, 'corpus.db');
    if (fs.existsSync(dbBackup)) {
      await fs.copyFile(
        dbBackup,
        path.join(corpusPath, '.corpus', 'corpus.db')
      );
      console.log('✓ Database restored');
    }
  }

  // Restore configuration
  const configBackup = path.join(sourceDir, 'corpus-config.json');
  if (fs.existsSync(configBackup)) {
    await fs.copyFile(
      configBackup,
      path.join(corpusPath, 'corpus-config.json')
    );
    console.log('✓ Configuration restored');
  }

  // Restore artifacts
  const artifactsBackup = path.join(sourceDir, 'artifacts');
  if (fs.existsSync(artifactsBackup)) {
    for (const artifact of manifest.artifacts) {
      const sourcePath = path.join(artifactsBackup, artifact);
      const config = JSON.parse(
        fs.readFileSync(path.join(corpusPath, 'corpus-config.json'), 'utf8')
      );
      const targetPath = path.join(
        corpusPath,
        config.artifacts[artifact].path
      );

      if (fs.existsSync(sourcePath)) {
        await copyRecursive(sourcePath, targetPath);
        console.log(`✓ Restored artifact: ${artifact}`);
      }
    }
  }

  // Cleanup extracted files if was compressed
  if (backupPath.endsWith('.zip')) {
    await fs.rm(sourceDir, { recursive: true, force: true });
  }

  return {
    restored: manifest,
    restorePoint: restorePoint.manifest
  };
}
```

### 3. Selective Restore

**Restore Specific Artifacts:**
```javascript
async function restoreArtifacts(corpusPath, backupPath, artifactNames) {
  const sourceDir = backupPath.endsWith('.zip')
    ? await extractZip(backupPath)
    : backupPath;

  const manifest = JSON.parse(
    fs.readFileSync(path.join(sourceDir, 'manifest.json'), 'utf8')
  );

  const config = JSON.parse(
    fs.readFileSync(path.join(corpusPath, 'corpus-config.json'), 'utf8')
  );

  const restored = [];

  for (const name of artifactNames) {
    if (!manifest.artifacts.includes(name)) {
      console.warn(`Artifact ${name} not found in backup`);
      continue;
    }

    const sourcePath = path.join(sourceDir, 'artifacts', name);
    const targetPath = path.join(corpusPath, config.artifacts[name].path);

    if (fs.existsSync(sourcePath)) {
      await copyRecursive(sourcePath, targetPath);
      console.log(`✓ Restored: ${name}`);
      restored.push(name);
    }
  }

  if (backupPath.endsWith('.zip')) {
    await fs.rm(sourceDir, { recursive: true, force: true });
  }

  return { restored, total: artifactNames.length };
}
```

---

## CorpusHub Integration

### API Endpoints

**Create Backup:**
```
POST /api/backups
Body: { corpusId: "slug", type: "full" }
Response: { backupId, timestamp, size }
```

**List Backups:**
```
GET /api/backups?corpusId=slug
Response: [{ backupId, timestamp, type, size }]
```

**Restore:**
```
POST /api/backups/:backupId/restore
Body: { dryRun: false }
Response: { restored, restorePoint }
```

---

## Configuration

```json
{
  "backup": {
    "enabled": true,
    "schedule": "daily",
    "retention": {
      "daily": 7,
      "weekly": 4,
      "monthly": 12
    },
    "strategy": "full",
    "compress": true,
    "location": ".corpus/backups",
    "exclude": [
      "node_modules",
      ".git",
      "*.log"
    ]
  }
}
```

---

## Quick Reference

**Create backup:**
```javascript
const backup = await createFullBackup('/path/to/corpus');
console.log(`Backup created: ${backup.manifest.timestamp}`);
```

**List backups:**
```javascript
const backups = await listBackups('/path/to/corpus');
backups.forEach(b => console.log(`${b.timestamp} (${b.type})`));
```

**Restore:**
```javascript
const result = await restoreFromBackup(
  '/path/to/corpus',
  backupPath,
  { dryRun: false }
);
console.log(`Restored from ${result.restored.timestamp}`);
```

---

*End of Backup & Restore*
*Part of v4.0.0 Universal Skills Ecosystem*
*Category: Utilities*
*Disaster recovery and version control*
