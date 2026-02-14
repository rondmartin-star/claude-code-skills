---
name: document-management
description: >
  Universal document CRUD operations for corpus artifacts. Create, read, update, delete, and organize
  documents across all artifact types. Respects source modes and integrates with CorpusHub when enabled.
---

# Document Management

**Purpose:** CRUD operations for corpus documents and artifacts
**Size:** ~12 KB
**Type:** Core Content Management (Universal)
**Status:** Production

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Create new document"
- "Delete this file"
- "Move document to..."
- "Organize artifacts"
- "List all documents"
- "Search documents"

**Context Indicators:**
- File system operations needed
- Document organization required
- Bulk operations requested
- Document search needed

## ❌ DO NOT LOAD WHEN

- Content editing (use review-edit-author)
- Publishing content (use content-creation)
- Version control (use version-control)
- Collaboration features (use collaboration)

---

## Core Operations

### Create Document

```javascript
async function createDocument(options) {
  const {
    artifactType,
    name,
    content = '',
    sourceMode = 'source',
    registerWithHub = true
  } = options;

  // Validate artifact type exists in corpus-config.json
  const config = await loadCorpusConfig();
  const artifact = config.artifacts[artifactType];

  if (!artifact) {
    throw new Error(`Unknown artifact type: ${artifactType}`);
  }

  // Build file path
  const filePath = path.join(
    config.corpus.baseDir,
    artifact.path,
    `${name}${artifact.extensions[0]}`
  );

  // Check if file already exists
  if (await fileExists(filePath)) {
    console.warn(`⚠️  File already exists: ${filePath}`);
    console.log('Options:');
    console.log('  1. Overwrite');
    console.log('  2. Create with different name');
    console.log('  3. Cancel');

    const choice = await promptUser();
    if (choice === 3) return;
    if (choice === 2) {
      name = await promptForName();
      return createDocument({ ...options, name });
    }
  }

  // Create file
  await writeFile(filePath, content);
  console.log(`✓ Created: ${filePath}`);

  // Register with CorpusHub if applicable
  if (registerWithHub && sourceMode !== 'source') {
    await registerDocumentWithHub(filePath, artifactType, sourceMode);
  }

  return { path: filePath, artifactType, sourceMode };
}
```

### Read Document

```javascript
async function readDocument(pathOrId) {
  // Resolve path (could be file path or CorpusHub bit ID)
  const filePath = await resolvePath(pathOrId);

  if (!await fileExists(filePath)) {
    throw new Error(`Document not found: ${filePath}`);
  }

  // Read file
  const content = await readFile(filePath);

  // Get metadata
  const metadata = await getDocumentMetadata(filePath);

  return {
    path: filePath,
    content,
    metadata: {
      size: metadata.size,
      created: metadata.birthtime,
      modified: metadata.mtime,
      sourceMode: metadata.sourceMode,
      artifactType: metadata.artifactType
    }
  };
}
```

### Update Document

```javascript
async function updateDocument(pathOrId, newContent, options = {}) {
  const {
    sourceMode,
    syncToHub = true,
    createBackup = true
  } = options;

  // Resolve path
  const filePath = await resolvePath(pathOrId);

  // Check source mode
  const metadata = await getDocumentMetadata(filePath);

  if (metadata.sourceMode === 'corpus') {
    console.warn('⚠️  This document has sourceMode=corpus');
    console.log('   Edits should be made in CorpusHub, not in files.');
    console.log('   CorpusHub is the source of truth.');
    console.log('');
    console.log('Do you want to continue anyway? [y/N]');

    const proceed = await promptUser();
    if (!proceed) {
      console.log('Opening in CorpusHub instead...');
      return openInCorpusHub(filePath);
    }
  }

  // Create backup if requested
  if (createBackup) {
    await createBackupCopy(filePath);
  }

  // Update file
  await writeFile(filePath, newContent);
  console.log(`✓ Updated: ${filePath}`);

  // Sync to CorpusHub if bidirectional
  if (syncToHub && metadata.sourceMode === 'bidirectional') {
    await syncToCorpusHub(filePath);
  }

  return { path: filePath, updated: true };
}
```

### Delete Document

```javascript
async function deleteDocument(pathOrId, options = {}) {
  const {
    createBackup = true,
    removeFromHub = true,
    confirmDeletion = true
  } = options;

  // Resolve path
  const filePath = await resolvePath(pathOrId);

  // Confirmation
  if (confirmDeletion) {
    console.log(`⚠️  About to delete: ${filePath}`);
    console.log('This action cannot be undone (unless backed up).');
    console.log('');
    console.log('Continue? [y/N]');

    const proceed = await promptUser();
    if (!proceed) {
      console.log('Deletion cancelled.');
      return { deleted: false };
    }
  }

  // Create backup
  if (createBackup) {
    await createBackupCopy(filePath);
    console.log('✓ Backup created');
  }

  // Delete file
  await deleteFile(filePath);
  console.log(`✓ Deleted: ${filePath}`);

  // Remove from CorpusHub
  if (removeFromHub) {
    await removeFromCorpusHub(filePath);
  }

  return { path: filePath, deleted: true };
}
```

### Move/Rename Document

```javascript
async function moveDocument(source, destination, options = {}) {
  const {
    updateReferences = true,
    syncToHub = true
  } = options;

  // Resolve paths
  const sourcePath = await resolvePath(source);
  const destPath = await resolvePath(destination);

  // Check if destination exists
  if (await fileExists(destPath)) {
    throw new Error(`Destination already exists: ${destPath}`);
  }

  // Move file
  await moveFile(sourcePath, destPath);
  console.log(`✓ Moved: ${sourcePath} → ${destPath}`);

  // Update internal references (links to this document)
  if (updateReferences) {
    await updateInternalReferences(sourcePath, destPath);
    console.log('✓ Updated references');
  }

  // Sync to CorpusHub
  if (syncToHub) {
    await syncMoveToHub(sourcePath, destPath);
  }

  return { from: sourcePath, to: destPath, moved: true };
}
```

---

## Bulk Operations

### Create Multiple Documents

```javascript
async function createBulkDocuments(documents) {
  console.log(`Creating ${documents.length} documents...`);

  const results = [];

  for (const doc of documents) {
    try {
      const result = await createDocument(doc);
      results.push({ ...result, success: true });
      console.log(`✓ ${doc.name}`);
    } catch (error) {
      results.push({ name: doc.name, success: false, error: error.message });
      console.error(`✗ ${doc.name}: ${error.message}`);
    }
  }

  console.log('');
  console.log(`Created: ${results.filter(r => r.success).length}/${documents.length}`);

  return results;
}
```

### Delete Multiple Documents

```javascript
async function deleteBulkDocuments(pathsOrIds, options = {}) {
  console.log(`⚠️  About to delete ${pathsOrIds.length} documents`);
  console.log('');
  pathsOrIds.forEach(p => console.log(`  - ${p}`));
  console.log('');
  console.log('Continue? [y/N]');

  const proceed = await promptUser();
  if (!proceed) {
    console.log('Bulk deletion cancelled.');
    return { deleted: 0 };
  }

  const results = [];

  for (const pathOrId of pathsOrIds) {
    try {
      const result = await deleteDocument(pathOrId, {
        ...options,
        confirmDeletion: false
      });
      results.push({ ...result, success: true });
    } catch (error) {
      results.push({
        path: pathOrId,
        success: false,
        error: error.message
      });
    }
  }

  console.log('');
  console.log(`Deleted: ${results.filter(r => r.success).length}/${pathsOrIds.length}`);

  return results;
}
```

---

## Search & Organization

### Search Documents

```javascript
async function searchDocuments(query, options = {}) {
  const {
    artifactTypes = [],
    searchContent = true,
    searchMetadata = true,
    maxResults = 50
  } = options;

  const config = await loadCorpusConfig();
  const results = [];

  // Search in file names
  const fileMatches = await searchFileNames(query, config, artifactTypes);
  results.push(...fileMatches);

  // Search in file content
  if (searchContent) {
    const contentMatches = await searchFileContent(query, config, artifactTypes);
    results.push(...contentMatches);
  }

  // Search in metadata
  if (searchMetadata) {
    const metadataMatches = await searchMetadata(query, config);
    results.push(...metadataMatches);
  }

  // Deduplicate and limit
  const uniqueResults = deduplicateResults(results);
  return uniqueResults.slice(0, maxResults);
}
```

### List Documents

```javascript
async function listDocuments(options = {}) {
  const {
    artifactType = null,
    sortBy = 'modified',
    order = 'desc',
    includeMetadata = false
  } = options;

  const config = await loadCorpusConfig();
  const documents = [];

  // Get artifact types to list
  const artifactTypes = artifactType
    ? [artifactType]
    : Object.keys(config.artifacts);

  // List files for each artifact type
  for (const type of artifactTypes) {
    const artifact = config.artifacts[type];
    const artifactPath = path.join(config.corpus.baseDir, artifact.path);
    const files = await listFiles(artifactPath, artifact.extensions);

    for (const file of files) {
      documents.push({
        path: file,
        artifactType: type,
        metadata: includeMetadata ? await getDocumentMetadata(file) : null
      });
    }
  }

  // Sort
  documents.sort((a, b) => {
    if (sortBy === 'name') {
      return order === 'asc'
        ? a.path.localeCompare(b.path)
        : b.path.localeCompare(a.path);
    } else if (sortBy === 'modified') {
      return order === 'asc'
        ? a.metadata.mtime - b.metadata.mtime
        : b.metadata.mtime - a.metadata.mtime;
    }
  });

  return documents;
}
```

### Organize by Artifact Type

```javascript
async function organizeByArtifactType(sourceDir) {
  console.log('Organizing documents by artifact type...');

  const config = await loadCorpusConfig();
  const files = await getAllFiles(sourceDir);
  const moves = [];

  for (const file of files) {
    // Determine artifact type by extension
    const ext = path.extname(file);
    const artifactType = findArtifactByExtension(ext, config);

    if (!artifactType) {
      console.warn(`⚠️  Unknown type for: ${file}`);
      continue;
    }

    // Calculate destination
    const artifact = config.artifacts[artifactType];
    const destPath = path.join(
      config.corpus.baseDir,
      artifact.path,
      path.basename(file)
    );

    if (file !== destPath) {
      moves.push({ from: file, to: destPath, type: artifactType });
    }
  }

  // Confirm moves
  console.log(`Found ${moves.length} files to organize:`);
  moves.forEach(m => console.log(`  ${m.from} → ${m.type}/`));
  console.log('');
  console.log('Proceed? [Y/n]');

  const proceed = await promptUser();
  if (!proceed) {
    return { organized: 0 };
  }

  // Execute moves
  for (const move of moves) {
    await moveDocument(move.from, move.to, { syncToHub: true });
  }

  console.log(`✓ Organized ${moves.length} documents`);
  return { organized: moves.length, moves };
}
```

---

## CorpusHub Integration

### Register Document

```javascript
async function registerDocumentWithHub(filePath, artifactType, sourceMode) {
  const hubStatus = await checkCorpusHubStatus();

  if (!hubStatus.running) {
    console.warn('⚠️  CorpusHub not running - skipping registration');
    return { registered: false };
  }

  // Create bit in CorpusHub
  const bitData = {
    title: path.basename(filePath, path.extname(filePath)),
    filepath: filePath,
    artifact_type: artifactType,
    source_mode: sourceMode
  };

  const response = await fetch('http://localhost:3000/api/bits/create', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(bitData)
  });

  if (response.ok) {
    const bit = await response.json();
    console.log(`✓ Registered with CorpusHub (ID: ${bit.id})`);
    return { registered: true, bitId: bit.id };
  } else {
    console.error('✗ Failed to register with CorpusHub');
    return { registered: false };
  }
}
```

---

## Configuration

```json
{
  "documentManagement": {
    "autoBackup": true,
    "backupLocation": ".backups/",
    "confirmDeletions": true,
    "syncToHub": true,
    "updateReferences": true,
    "maxSearchResults": 50,
    "defaultSourceMode": "source"
  }
}
```

---

## Quick Reference

**Create document:**
```javascript
await createDocument({
  artifactType: 'documentation',
  name: 'api-guide',
  content: '# API Guide\n...'
});
```

**Search documents:**
```javascript
await searchDocuments('authentication', {
  searchContent: true,
  maxResults: 10
});
```

**List by type:**
```javascript
await listDocuments({
  artifactType: 'documentation',
  sortBy: 'modified'
});
```

---

*End of Document Management*
*Part of v4.0.0 Universal Skills Ecosystem*
*Integrates with: CorpusHub, source-mode-manager*
