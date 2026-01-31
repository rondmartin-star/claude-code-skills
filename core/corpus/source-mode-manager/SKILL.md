---
name: source-mode-manager
description: >
  Manage three source modes (corpus, source, bidirectional) for artifacts. Handles
  file watchers, sync logic, and conflict resolution. Use when: configuring artifacts,
  setting up bidirectional sync, or resolving edit conflicts between IDE and CorpusHub.
---

# Source Mode Manager

**Purpose:** Manage corpus, source, and bidirectional editing modes
**Size:** ~14 KB
**Type:** Core Pattern (Universal)

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Set up bidirectional sync"
- "Configure source modes"
- "Sync between IDE and CorpusHub"
- "Resolve edit conflict"
- "Change artifact source mode"

**Context Indicators:**
- Configuring new artifacts
- Converting between source modes
- File sync issues
- Edit conflicts between IDE and CorpusHub

## ❌ DO NOT LOAD WHEN

- Just reading corpus-config.json (use corpus-config)
- Initializing new corpus (use corpus-init)
- General corpus questions (use corpus-orchestrator)

---

## Three Source Modes

### Mode: corpus

**Source of Truth:** CorpusHub HTML
**Edited In:** CorpusHub only (web interface)
**IDE Files:** Auto-generated from HTML (read-only)
**Use For:** Requirements, design docs, specifications, ADRs

**Characteristics:**
```
✓ Single source of truth (CorpusHub database)
✓ Version control via CorpusHub
✓ Rich HTML editing
✗ Cannot edit in VS Code
✗ IDE files are regenerated on change
```

**Example Artifacts:**
```json
{
  "requirements": {
    "path": "docs/requirements",
    "label": "Requirements",
    "extensions": [".html", ".md"],
    "sourceMode": "corpus"
  },
  "specifications": {
    "path": "specifications",
    "label": "Specifications",
    "extensions": [".md", ".html"],
    "sourceMode": "corpus"
  }
}
```

### Mode: source

**Source of Truth:** IDE files (VS Code, etc.)
**Edited In:** IDE only
**CorpusHub HTML:** Auto-generated from files (read-only in UI)
**Use For:** Implementation code, config files, test suites

**Characteristics:**
```
✓ Edit in preferred IDE
✓ Git version control
✓ Syntax highlighting, linting
✗ Cannot edit in CorpusHub
✗ CorpusHub displays read-only view
```

**Example Artifacts:**
```json
{
  "source-code": {
    "path": "src",
    "label": "Source Code",
    "extensions": [".js", ".ts", ".jsx", ".tsx"],
    "sourceMode": "source"
  },
  "tests": {
    "path": "tests",
    "label": "Test Suite",
    "extensions": [".test.js", ".spec.js"],
    "sourceMode": "source"
  }
}
```

### Mode: bidirectional

**Source of Truth:** Both locations (synchronized)
**Edited In:** Either CorpusHub or IDE
**Sync:** Two-way with conflict detection
**Use For:** Documentation, API docs, guides, tutorials

**Characteristics:**
```
✓ Edit anywhere (CorpusHub or IDE)
✓ Changes sync automatically
✓ Conflict detection
✓ Flexibility for different workflows
⚠ Requires file watchers
⚠ Potential for conflicts
```

**Example Artifacts:**
```json
{
  "documentation": {
    "path": "docs",
    "label": "Documentation",
    "extensions": [".md"],
    "sourceMode": "bidirectional"
  },
  "api-docs": {
    "path": "docs/api",
    "label": "API Documentation",
    "extensions": [".md", ".html"],
    "sourceMode": "bidirectional"
  }
}
```

---

## Mode Selection Guidelines

### Use corpus mode when:

```
✓ Content is requirements/design (not implementation)
✓ Rich HTML formatting needed
✓ Non-technical stakeholders editing
✓ Centralized approval workflow required
✓ CorpusHub is the canonical system
```

**Examples:** Requirements docs, design specifications, ADRs, stakeholder materials

### Use source mode when:

```
✓ Content is code or configuration
✓ IDE tools needed (linting, debugging, autocomplete)
✓ Git workflows preferred
✓ Developers are primary editors
✓ Syntax highlighting essential
```

**Examples:** Source code, tests, build configs, deployment scripts

### Use bidirectional mode when:

```
✓ Both technical and non-technical users edit
✓ Flexibility needed for different workflows
✓ Documentation that references code
✓ API documentation
✓ Guides and tutorials
```

**Examples:** README.md, user guides, API documentation, tutorials

---

## Bidirectional Sync Architecture

### File Watchers

**IDE → CorpusHub:**
```javascript
// Watch for file changes in IDE
const watcher = chokidar.watch(artifactPath, {
  ignored: /(^|[\/\\])\../,
  persistent: true,
  ignoreInitial: true
});

watcher.on('change', async (filePath) => {
  // Read changed file
  const content = await fs.readFile(filePath, 'utf8');

  // Convert to HTML if needed
  const html = await convertToHTML(content, filePath);

  // Update CorpusHub
  await updateCorpusHub(filePath, html);
});
```

**CorpusHub → IDE:**
```javascript
// CorpusHub webhook on artifact update
app.post('/api/webhooks/artifact-updated', async (req, res) => {
  const { artifact_id, content_html } = req.body;

  // Get artifact configuration
  const artifact = await getArtifact(artifact_id);

  // Convert HTML to source format
  const sourceContent = await convertFromHTML(content_html, artifact.path);

  // Write to IDE file
  await fs.writeFile(artifact.path, sourceContent, 'utf8');

  res.json({ status: 'synced' });
});
```

### Conflict Detection

**Timestamp-based:**
```javascript
async function detectConflict(filePath) {
  // Get file modification time
  const fileStats = await fs.stat(filePath);
  const fileMtime = fileStats.mtime;

  // Get CorpusHub last update time
  const artifact = await getArtifactByPath(filePath);
  const corpusMtime = new Date(artifact.updated_at);

  // Check for conflict (both modified recently)
  const timeDiff = Math.abs(fileMtime - corpusMtime);

  if (timeDiff < 5000) { // 5 seconds
    return {
      hasConflict: true,
      fileVersion: fileMtime,
      corpusVersion: corpusMtime
    };
  }

  return { hasConflict: false };
}
```

### Conflict Resolution

**Strategy 1: Last-Write-Wins (Default)**
```javascript
function resolveConflict_LastWriteWins(fileVersion, corpusVersion) {
  if (fileVersion > corpusVersion) {
    return 'use_file';
  } else {
    return 'use_corpus';
  }
}
```

**Strategy 2: Manual Resolution (Safe)**
```javascript
async function resolveConflict_Manual(filePath, fileContent, corpusContent) {
  // Create backup
  await createBackup(filePath);

  // Show conflict to user
  console.log('CONFLICT DETECTED:');
  console.log(`File: ${filePath}`);
  console.log('Choose resolution:');
  console.log('  1. Keep IDE version');
  console.log('  2. Keep CorpusHub version');
  console.log('  3. Merge manually');

  const choice = await promptUser();

  switch (choice) {
    case 1:
      await updateCorpusHub(filePath, fileContent);
      break;
    case 2:
      await fs.writeFile(filePath, corpusContent, 'utf8');
      break;
    case 3:
      await openMergeTool(filePath, fileContent, corpusContent);
      break;
  }
}
```

**Strategy 3: Three-Way Merge**
```javascript
async function resolveConflict_ThreeWay(filePath) {
  // Get base version (last sync)
  const baseContent = await getLastSyncVersion(filePath);

  // Get current versions
  const fileContent = await fs.readFile(filePath, 'utf8');
  const corpusContent = await getCorpusContent(filePath);

  // Perform three-way merge
  const merged = merge(baseContent, fileContent, corpusContent);

  if (merged.conflicts) {
    // Has unresolvable conflicts
    return resolveConflict_Manual(filePath, fileContent, corpusContent);
  }

  // Apply merged result to both
  await fs.writeFile(filePath, merged.content, 'utf8');
  await updateCorpusHub(filePath, merged.content);
}
```

---

## Configuration

### corpus-config.json

```json
{
  "artifacts": {
    "requirements": {
      "path": "docs/requirements",
      "sourceMode": "corpus",
      "extensions": [".html", ".md"]
    },
    "source-code": {
      "path": "src",
      "sourceMode": "source",
      "extensions": [".js", ".ts"]
    },
    "documentation": {
      "path": "docs",
      "sourceMode": "bidirectional",
      "extensions": [".md"],
      "sync": {
        "conflict_resolution": "manual",
        "watch_interval_ms": 1000,
        "debounce_ms": 500
      }
    }
  },

  "sync": {
    "enabled": true,
    "default_conflict_resolution": "last-write-wins",
    "backup_before_sync": true,
    "backup_retention_days": 7
  }
}
```

### Sync Configuration Options

**conflict_resolution:**
- `"last-write-wins"` - Most recent change wins (default)
- `"manual"` - Prompt user for resolution
- `"three-way-merge"` - Attempt automatic merge
- `"prefer-corpus"` - CorpusHub always wins
- `"prefer-file"` - IDE file always wins

**watch_interval_ms:** How often to check for changes (default: 1000ms)

**debounce_ms:** Wait time after last change before syncing (default: 500ms)

---

## Changing Source Modes

### Corpus → Source

**Steps:**
1. Export HTML from CorpusHub to files
2. Update corpus-config.json: `"sourceMode": "source"`
3. Stop file watchers for this artifact
4. Mark CorpusHub view as read-only

```javascript
async function convertMode_CorpusToSource(artifactType) {
  // 1. Export current HTML to files
  const artifacts = await getArtifacts(artifactType);

  for (const artifact of artifacts) {
    const html = artifact.content_html;
    const markdown = await htmlToMarkdown(html);
    await fs.writeFile(artifact.source_path, markdown, 'utf8');
  }

  // 2. Update config
  await updateConfig({
    [`artifacts.${artifactType}.sourceMode`]: 'source'
  });

  // 3. Stop watchers
  await stopWatchers(artifactType);

  // 4. Mark CorpusHub as read-only
  await setCorpusHubMode(artifactType, 'read-only');
}
```

### Source → Corpus

**Steps:**
1. Import files to CorpusHub database
2. Update corpus-config.json: `"sourceMode": "corpus"`
3. Mark IDE files as auto-generated (add warning comments)

```javascript
async function convertMode_SourceToCorpus(artifactType) {
  // 1. Import files to CorpusHub
  const files = await findFiles(artifactConfig.path);

  for (const file of files) {
    const content = await fs.readFile(file, 'utf8');
    const html = await markdownToHTML(content);

    await createCorpusArtifact({
      type: artifactType,
      path: file,
      content_html: html
    });
  }

  // 2. Update config
  await updateConfig({
    [`artifacts.${artifactType}.sourceMode`]: 'corpus'
  });

  // 3. Mark IDE files
  await addAutoGeneratedWarning(artifactConfig.path);
}
```

### Bidirectional → Corpus or Source

**Steps:**
1. Stop file watchers
2. Choose canonical source (CorpusHub or IDE)
3. Update config
4. Set up appropriate read-only indicators

```javascript
async function convertMode_BidirectionalToSingle(artifactType, targetMode) {
  // 1. Stop watchers
  await stopWatchers(artifactType);

  // 2. Choose canonical source
  const canonicalSource = await promptUser(
    'Which version is canonical?',
    ['CorpusHub (use corpus mode)', 'IDE files (use source mode)']
  );

  // 3. Update config
  await updateConfig({
    [`artifacts.${artifactType}.sourceMode`]: targetMode
  });

  // 4. Set read-only indicators
  if (targetMode === 'corpus') {
    await addAutoGeneratedWarning(artifactConfig.path);
    await setCorpusHubMode(artifactType, 'editable');
  } else {
    await setCorpusHubMode(artifactType, 'read-only');
  }
}
```

---

## File Watcher Management

### Starting Watchers

```javascript
async function startWatchers(corpusConfig) {
  const bidirectionalArtifacts = Object.entries(corpusConfig.artifacts)
    .filter(([_, config]) => config.sourceMode === 'bidirectional');

  for (const [type, config] of bidirectionalArtifacts) {
    await startWatcher(type, config);
  }
}

async function startWatcher(artifactType, config) {
  const watcher = chokidar.watch(config.path, {
    ignored: /(^|[\/\\])\../,
    persistent: true,
    ignoreInitial: true,
    awaitWriteFinish: {
      stabilityThreshold: config.sync?.debounce_ms || 500,
      pollInterval: 100
    }
  });

  watcher.on('change', async (filePath) => {
    await handleFileChange(artifactType, filePath);
  });

  // Store watcher for cleanup
  activeWatchers.set(artifactType, watcher);

  console.log(`✓ Started watcher for ${artifactType} (${config.path})`);
}
```

### Stopping Watchers

```javascript
async function stopWatchers(artifactType = null) {
  if (artifactType) {
    // Stop specific watcher
    const watcher = activeWatchers.get(artifactType);
    if (watcher) {
      await watcher.close();
      activeWatchers.delete(artifactType);
      console.log(`✓ Stopped watcher for ${artifactType}`);
    }
  } else {
    // Stop all watchers
    for (const [type, watcher] of activeWatchers) {
      await watcher.close();
      console.log(`✓ Stopped watcher for ${type}`);
    }
    activeWatchers.clear();
  }
}
```

### Health Checks

```javascript
async function checkWatcherHealth() {
  const issues = [];

  for (const [type, watcher] of activeWatchers) {
    // Check if watcher is still running
    if (!watcher.getWatched()) {
      issues.push({
        type,
        issue: 'Watcher not running',
        severity: 'critical'
      });
    }

    // Check if files exist
    const config = corpusConfig.artifacts[type];
    if (!await pathExists(config.path)) {
      issues.push({
        type,
        issue: `Path does not exist: ${config.path}`,
        severity: 'critical'
      });
    }
  }

  return {
    healthy: issues.length === 0,
    issues
  };
}
```

---

## Validation

### Validate Source Mode Configuration

```javascript
async function validateSourceModes(corpusConfig) {
  const issues = [];

  for (const [type, config] of Object.entries(corpusConfig.artifacts)) {
    // Check valid mode
    if (!['corpus', 'source', 'bidirectional'].includes(config.sourceMode)) {
      issues.push({
        artifact: type,
        issue: `Invalid sourceMode: ${config.sourceMode}`,
        severity: 'error'
      });
    }

    // Check bidirectional has sync config
    if (config.sourceMode === 'bidirectional' && !config.sync) {
      issues.push({
        artifact: type,
        issue: 'Bidirectional mode requires sync configuration',
        severity: 'warning',
        suggestion: 'Add sync config or use default settings'
      });
    }

    // Check path exists
    if (!await pathExists(config.path)) {
      issues.push({
        artifact: type,
        issue: `Path does not exist: ${config.path}`,
        severity: 'error'
      });
    }
  }

  return {
    valid: issues.filter(i => i.severity === 'error').length === 0,
    issues
  };
}
```

---

## Quick Reference

**Check current mode:**
```javascript
const mode = corpusConfig.artifacts['documentation'].sourceMode;
// Returns: 'corpus', 'source', or 'bidirectional'
```

**Start bidirectional sync:**
```javascript
await startWatchers(corpusConfig);
```

**Convert mode:**
```javascript
await convertMode('requirements', 'corpus', 'source');
```

**Resolve conflict manually:**
```javascript
await resolveConflict('docs/api.md', 'manual');
```

**Check watcher health:**
```javascript
const health = await checkWatcherHealth();
if (!health.healthy) {
  console.log('Issues:', health.issues);
}
```

---

*End of Source Mode Manager*
*Part of v4.0.0 Universal Skills Ecosystem*
*Integration: CorpusHub Bidirectional Architecture*
