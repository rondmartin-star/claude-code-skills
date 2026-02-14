---
name: version-control
description: >
  Track changes, manage document history, and enable rollback for corpus artifacts.
  Provides versioning layer on top of git with corpus-specific metadata and CorpusHub integration.
---

# Version Control

**Purpose:** Document versioning, change tracking, and rollback capabilities
**Size:** ~11 KB
**Type:** Core Content Management (Universal)
**Status:** Production

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Track changes to this document"
- "Show document history"
- "Rollback to previous version"
- "View document versions"
- "Compare versions"
- "Restore previous version"

**Context Indicators:**
- Need to see document history
- Rollback required
- Version comparison needed
- Change tracking requested

## ❌ DO NOT LOAD WHEN

- Git operations (use git directly via Bash)
- Content editing (use review-edit-author)
- Document creation/deletion (use document-management)

---

## Core Operations

### Track Changes

```javascript
async function trackChanges(filePath, options = {}) {
  const {
    message = 'Update document',
    author = 'Claude Code',
    createSnapshot = true
  } = options;

  // Get current content
  const content = await readFile(filePath);

  // Create version snapshot
  if (createSnapshot) {
    const version = await createVersionSnapshot(filePath, content, {
      message,
      author,
      timestamp: new Date()
    });

    console.log(`✓ Version ${version.number} created`);
    return version;
  }

  // Use git for tracking
  await gitAdd(filePath);
  await gitCommit(message, author);

  console.log('✓ Changes tracked in git');
  return { tracked: true, method: 'git' };
}
```

### Create Version Snapshot

```javascript
async function createVersionSnapshot(filePath, content, metadata) {
  const versionsDir = path.join(
    path.dirname(filePath),
    '.versions',
    path.basename(filePath)
  );

  await ensureDir(versionsDir);

  // Get version number
  const versions = await listVersions(filePath);
  const versionNumber = versions.length + 1;

  // Create snapshot file
  const snapshotPath = path.join(versionsDir, `v${versionNumber}.txt`);
  await writeFile(snapshotPath, content);

  // Create metadata file
  const metadataPath = path.join(versionsDir, `v${versionNumber}.meta.json`);
  await writeFile(metadataPath, JSON.stringify({
    version: versionNumber,
    timestamp: metadata.timestamp.toISOString(),
    author: metadata.author,
    message: metadata.message,
    fileSize: content.length,
    hash: calculateHash(content)
  }, null, 2));

  return {
    number: versionNumber,
    path: snapshotPath,
    metadata: metadataPath
  };
}
```

### List Versions

```javascript
async function listVersions(filePath) {
  const versionsDir = path.join(
    path.dirname(filePath),
    '.versions',
    path.basename(filePath)
  );

  if (!await dirExists(versionsDir)) {
    return [];
  }

  const metaFiles = await listFiles(versionsDir, ['.meta.json']);
  const versions = [];

  for (const metaFile of metaFiles) {
    const metadata = JSON.parse(await readFile(metaFile));
    const versionNumber = metadata.version;

    versions.push({
      version: versionNumber,
      timestamp: new Date(metadata.timestamp),
      author: metadata.author,
      message: metadata.message,
      size: metadata.fileSize,
      hash: metadata.hash,
      snapshotPath: path.join(versionsDir, `v${versionNumber}.txt`)
    });
  }

  // Sort by version number descending
  versions.sort((a, b) => b.version - a.version);

  return versions;
}
```

### View Version

```javascript
async function viewVersion(filePath, versionNumber) {
  const versions = await listVersions(filePath);
  const version = versions.find(v => v.version === versionNumber);

  if (!version) {
    throw new Error(`Version ${versionNumber} not found`);
  }

  const content = await readFile(version.snapshotPath);

  return {
    version: version.version,
    content,
    metadata: {
      timestamp: version.timestamp,
      author: version.author,
      message: version.message,
      size: version.size
    }
  };
}
```

### Compare Versions

```javascript
async function compareVersions(filePath, version1, version2 = 'current') {
  // Get version 1 content
  const v1Data = version1 === 'current'
    ? { content: await readFile(filePath), version: 'current' }
    : await viewVersion(filePath, version1);

  // Get version 2 content
  const v2Data = version2 === 'current'
    ? { content: await readFile(filePath), version: 'current' }
    : await viewVersion(filePath, version2);

  // Calculate diff
  const diff = calculateDiff(v1Data.content, v2Data.content);

  console.log(`Comparing v${v1Data.version} ↔ v${v2Data.version}`);
  console.log('');
  displayDiff(diff);

  return {
    version1: v1Data.version,
    version2: v2Data.version,
    diff,
    stats: {
      additions: diff.filter(d => d.type === 'add').length,
      deletions: diff.filter(d => d.type === 'remove').length,
      modifications: diff.filter(d => d.type === 'change').length
    }
  };
}
```

### Rollback to Version

```javascript
async function rollbackToVersion(filePath, versionNumber, options = {}) {
  const {
    createBackup = true,
    confirmRollback = true
  } = options;

  // Get target version
  const targetVersion = await viewVersion(filePath, versionNumber);

  // Confirmation
  if (confirmRollback) {
    console.log(`⚠️  About to rollback to version ${versionNumber}`);
    console.log(`   ${targetVersion.metadata.message}`);
    console.log(`   by ${targetVersion.metadata.author}`);
    console.log(`   on ${targetVersion.metadata.timestamp.toLocaleString()}`);
    console.log('');
    console.log('Current content will be replaced. Continue? [y/N]');

    const proceed = await promptUser();
    if (!proceed) {
      console.log('Rollback cancelled.');
      return { rolledBack: false };
    }
  }

  // Create backup of current state
  if (createBackup) {
    const currentContent = await readFile(filePath);
    await createVersionSnapshot(filePath, currentContent, {
      message: `Backup before rollback to v${versionNumber}`,
      author: 'System',
      timestamp: new Date()
    });
    console.log('✓ Current version backed up');
  }

  // Restore target version
  await writeFile(filePath, targetVersion.content);
  console.log(`✓ Rolled back to version ${versionNumber}`);

  // Create new version entry
  await trackChanges(filePath, {
    message: `Rolled back to v${versionNumber}: ${targetVersion.metadata.message}`,
    author: 'Claude Code'
  });

  return {
    rolledBack: true,
    targetVersion: versionNumber,
    newVersion: (await listVersions(filePath))[0].version
  };
}
```

---

## Git Integration

### Show Git History

```javascript
async function showGitHistory(filePath, options = {}) {
  const {
    maxCommits = 20,
    includePatches = false
  } = options;

  const log = await gitLog(filePath, maxCommits);

  console.log(`Git history for ${path.basename(filePath)}:`);
  console.log('');

  for (const commit of log) {
    console.log(`${commit.hash.substring(0, 7)} - ${commit.date}`);
    console.log(`Author: ${commit.author}`);
    console.log(`Message: ${commit.message}`);

    if (includePatches) {
      const patch = await gitShow(commit.hash, filePath);
      console.log('');
      console.log(patch);
    }

    console.log('');
  }

  return log;
}
```

### Git Diff

```javascript
async function gitDiffVersion(filePath, commit1, commit2 = 'HEAD') {
  const diff = await gitDiff(commit1, commit2, filePath);

  console.log(`Diff: ${commit1}...${commit2}`);
  console.log('');
  console.log(diff);

  return diff;
}
```

### Restore from Git

```javascript
async function restoreFromGit(filePath, commitHash, options = {}) {
  const {
    createBackup = true,
    confirmRestore = true
  } = options;

  // Get commit info
  const commit = await gitShowCommit(commitHash);

  // Confirmation
  if (confirmRestore) {
    console.log(`⚠️  Restore file from git commit ${commitHash.substring(0, 7)}`);
    console.log(`   ${commit.message}`);
    console.log(`   by ${commit.author}`);
    console.log(`   on ${commit.date}`);
    console.log('');
    console.log('Continue? [y/N]');

    const proceed = await promptUser();
    if (!proceed) {
      console.log('Restore cancelled.');
      return { restored: false };
    }
  }

  // Backup current
  if (createBackup) {
    await createVersionSnapshot(filePath, await readFile(filePath), {
      message: `Backup before git restore from ${commitHash.substring(0, 7)}`,
      author: 'System',
      timestamp: new Date()
    });
  }

  // Restore from git
  await gitCheckoutFile(commitHash, filePath);
  console.log(`✓ Restored from ${commitHash.substring(0, 7)}`);

  return { restored: true, commit: commitHash };
}
```

---

## Change History Display

### Show History Table

```javascript
async function showHistoryTable(filePath) {
  const versions = await listVersions(filePath);

  if (versions.length === 0) {
    console.log('No version history found.');
    console.log('Tip: Use git log for git-tracked changes.');
    return;
  }

  console.log(`Version history for ${path.basename(filePath)}:`);
  console.log('');
  console.log('Ver | Date & Time         | Author       | Message');
  console.log('----+---------------------+--------------+------------------');

  for (const v of versions) {
    const ver = `v${v.version}`.padEnd(3);
    const date = v.timestamp.toISOString().substring(0, 19).replace('T', ' ');
    const author = v.author.padEnd(12).substring(0, 12);
    const message = v.message.substring(0, 40);

    console.log(`${ver} | ${date} | ${author} | ${message}`);
  }

  console.log('');
  console.log(`Total versions: ${versions.length}`);
}
```

---

## Automatic Versioning

### Auto-save Versions

```javascript
async function enableAutoVersioning(filePath, options = {}) {
  const {
    interval = 3600000, // 1 hour
    maxVersions = 50
  } = options;

  // Set up file watcher
  const watcher = watchFile(filePath, async (curr, prev) => {
    if (curr.mtime > prev.mtime) {
      // File modified, create version
      const content = await readFile(filePath);
      await createVersionSnapshot(filePath, content, {
        message: 'Auto-save',
        author: 'System',
        timestamp: new Date()
      });

      // Cleanup old versions if exceeding max
      await cleanupOldVersions(filePath, maxVersions);
    }
  });

  console.log(`✓ Auto-versioning enabled for ${path.basename(filePath)}`);
  console.log(`  Interval: ${interval / 1000}s`);
  console.log(`  Max versions: ${maxVersions}`);

  return { enabled: true, watcher };
}
```

### Cleanup Old Versions

```javascript
async function cleanupOldVersions(filePath, maxVersions) {
  const versions = await listVersions(filePath);

  if (versions.length <= maxVersions) {
    return { cleaned: 0 };
  }

  // Keep newest maxVersions, delete older ones
  const toDelete = versions.slice(maxVersions);

  for (const version of toDelete) {
    await deleteFile(version.snapshotPath);
    await deleteFile(version.snapshotPath.replace('.txt', '.meta.json'));
  }

  console.log(`✓ Cleaned up ${toDelete.length} old versions`);
  return { cleaned: toDelete.length };
}
```

---

## Configuration

```json
{
  "versionControl": {
    "autoVersioning": {
      "enabled": false,
      "interval": 3600000,
      "maxVersions": 50
    },
    "rollback": {
      "autoBackup": true,
      "confirmRequired": true
    },
    "git": {
      "preferGitForTracking": true,
      "autoCommit": false
    },
    "versionsDir": ".versions"
  }
}
```

---

## Usage Examples

### Example 1: Track and Rollback

```
# Make changes to document
await updateDocument('docs/api.md', newContent);

# Track changes
await trackChanges('docs/api.md', {
  message: 'Updated API endpoints'
});

# Later... need to rollback
await showHistoryTable('docs/api.md');
await rollbackToVersion('docs/api.md', 3);
```

### Example 2: Compare Versions

```
# Show history
await showHistoryTable('docs/api.md');

# Compare current vs version 5
await compareVersions('docs/api.md', 5, 'current');

# Compare two specific versions
await compareVersions('docs/api.md', 3, 5);
```

### Example 3: Git Integration

```
# Show git history
await showGitHistory('src/app.js');

# Restore from specific commit
await restoreFromGit('src/app.js', 'a1b2c3d');

# Diff between commits
await gitDiffVersion('src/app.js', 'HEAD~3', 'HEAD');
```

---

## Quick Reference

**Track changes:**
```javascript
await trackChanges(filePath, {
  message: 'Updated content'
});
```

**View history:**
```javascript
await showHistoryTable(filePath);
```

**Rollback:**
```javascript
await rollbackToVersion(filePath, versionNumber);
```

**Compare:**
```javascript
await compareVersions(filePath, 3, 5);
```

---

*End of Version Control*
*Part of v4.0.0 Universal Skills Ecosystem*
*Integrates with: git, document-management*
