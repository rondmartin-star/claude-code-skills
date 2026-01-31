---
name: corpus-convert
description: >
  Convert existing projects to corpus-enabled. Analyzes project structure, preserves
  content, creates corpus-config.json, imports to CorpusHub. Use when: migrating
  existing projects, adding corpus features to established codebases.
---

# Corpus Conversion

**Purpose:** Convert existing projects to corpus-enabled
**Size:** ~14 KB
**Type:** Core Pattern (Universal)

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Convert this to corpus"
- "Enable corpus on existing project"
- "Migrate to corpus"
- "Make existing project corpus-enabled"

**Context Indicators:**
- Existing project with content
- Not currently corpus-enabled
- Want to preserve existing structure
- Adding corpus features retroactively

## ❌ DO NOT LOAD WHEN

- New empty project (use corpus-init)
- Already corpus-enabled (use corpus-config)
- Just checking status (use corpus-detect)

---

## Conversion Workflow

### Step 1: Pre-Conversion Analysis

**Check current status:**
```javascript
const status = await detectCorpus(projectPath);

if (status.isCorpusEnabled) {
  console.log('✗ Already corpus-enabled');
  console.log(`  Name: ${status.config.name}`);
  console.log('Use corpus-config to update configuration');
  return;
}

console.log('✓ Not corpus-enabled, proceeding with conversion');
```

**Analyze project structure:**
```javascript
const analysis = await analyzeProject(projectPath);

console.log('Project Analysis:');
console.log(`  Type: ${analysis.projectType}`);
console.log(`  Files: ${analysis.fileCount}`);
console.log(`  Directories: ${analysis.dirCount}`);
console.log(`  Detected artifacts: ${analysis.artifacts.length}`);
console.log(`  Git repository: ${analysis.hasGit ? 'Yes' : 'No'}`);
```

### Step 2: Artifact Detection

**Auto-detect artifact types:**
```javascript
function detectArtifacts(projectPath) {
  const artifacts = {};

  // Source code
  if (exists(path.join(projectPath, 'src'))) {
    artifacts['source-code'] = {
      path: 'src',
      label: 'Source Code',
      extensions: detectExtensions(path.join(projectPath, 'src')),
      sourceMode: 'source'
    };
  }

  // Tests
  if (exists(path.join(projectPath, 'tests')) ||
      exists(path.join(projectPath, 'test'))) {
    const testPath = exists(path.join(projectPath, 'tests')) ? 'tests' : 'test';
    artifacts['tests'] = {
      path: testPath,
      label: 'Test Suite',
      extensions: ['.test.js', '.spec.js', '.test.ts'],
      sourceMode: 'source'
    };
  }

  // Documentation
  if (exists(path.join(projectPath, 'docs'))) {
    artifacts['documentation'] = {
      path: 'docs',
      label: 'Documentation',
      extensions: ['.md', '.html'],
      sourceMode: 'bidirectional'
    };
  }

  // Requirements/Specifications
  if (exists(path.join(projectPath, 'requirements')) ||
      exists(path.join(projectPath, 'specifications'))) {
    const reqPath = exists(path.join(projectPath, 'requirements'))
      ? 'requirements'
      : 'specifications';

    artifacts['requirements'] = {
      path: reqPath,
      label: 'Requirements',
      extensions: ['.md', '.html'],
      sourceMode: 'corpus'
    };
  }

  // README
  if (exists(path.join(projectPath, 'README.md'))) {
    artifacts['readme'] = {
      path: '.',
      label: 'README',
      extensions: ['README.md'],
      sourceMode: 'bidirectional'
    };
  }

  return artifacts;
}
```

### Step 3: User Customization

**Review and customize:**
```javascript
console.log('Detected Artifacts:');
Object.entries(artifacts).forEach(([key, config]) => {
  console.log(`  ${key}:`);
  console.log(`    Path: ${config.path}`);
  console.log(`    Mode: ${config.sourceMode}`);
  console.log(`    Extensions: ${config.extensions.join(', ')}`);
});

console.log('');
const customize = await promptUser('Customize artifacts?', [
  'Accept detected artifacts',
  'Add/remove artifacts',
  'Change source modes'
]);

if (customize !== 'Accept detected artifacts') {
  artifacts = await customizeArtifacts(artifacts);
}
```

### Step 4: Generate Configuration

**Create corpus-config.json:**
```javascript
const config = {
  corpus: {
    name: await detectProjectName(projectPath),
    description: await detectDescription(projectPath),
    version: '1.0.0',
    baseDir: path.resolve(projectPath)
  },
  artifacts: artifacts,
  framework: {
    categories: []
  },
  voice: {
    promptFile: 'voice/system-prompt.md',
    attributes: ['professional', 'clear'],
    avoid: ['jargon', 'ambiguity'],
    preferredTerms: {}
  },
  roles: {
    available: ['admin', 'editor', 'author', 'reviewer', 'viewer', 'pending'],
    defaultRole: 'pending',
    aiAccess: ['admin', 'editor', 'author'],
    editAccess: ['admin', 'editor', 'author']
  },
  consistency: {
    enabled: true,
    scanDirectories: detectScanDirectories(artifacts)
  },
  audit: generateAuditConfig(projectType, artifacts)
};

// Write configuration
await writeJSON(
  path.join(projectPath, 'corpus-config.json'),
  config,
  { spaces: 2 }
);

console.log('✓ Created corpus-config.json');
```

### Step 5: Import Content to CorpusHub

**Import corpus-mode and bidirectional artifacts:**
```javascript
for (const [type, artifactConfig] of Object.entries(config.artifacts)) {
  // Only import corpus and bidirectional modes
  if (artifactConfig.sourceMode === 'source') {
    console.log(`⊘ Skipping ${type} (source mode)`);
    continue;
  }

  console.log(`→ Importing ${type}...`);

  const files = await findFiles(
    path.join(projectPath, artifactConfig.path),
    artifactConfig.extensions
  );

  for (const file of files) {
    const content = await fs.readFile(file, 'utf8');
    const html = await convertToHTML(content, file);

    await createCorpusArtifact({
      corpus_slug: config.corpus.slug,
      artifact_type: type,
      source_path: path.relative(projectPath, file),
      content_html: html
    });
  }

  console.log(`  ✓ Imported ${files.length} files`);
}
```

### Step 6: Create Infrastructure

**Create .corpus directory:**
```javascript
const corpusDir = path.join(projectPath, '.corpus');

await mkdir(corpusDir, { recursive: true });
await mkdir(path.join(corpusDir, 'backups'), { recursive: true });
await mkdir(path.join(corpusDir, 'audit-logs'), { recursive: true });

console.log('✓ Created .corpus/ infrastructure');
```

**Add to .gitignore:**
```javascript
const gitignorePath = path.join(projectPath, '.gitignore');
let gitignore = '';

if (await exists(gitignorePath)) {
  gitignore = await fs.readFile(gitignorePath, 'utf8');
}

if (!gitignore.includes('.corpus/')) {
  gitignore += '\n# Corpus infrastructure\n.corpus/\n';
  await fs.writeFile(gitignorePath, gitignore, 'utf8');
  console.log('✓ Updated .gitignore');
}
```

### Step 7: Register with CorpusHub

**Register via API:**
```javascript
const response = await fetch('http://localhost:3000/api/corpora/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    path: projectPath,
    config: config
  })
});

if (response.ok) {
  const result = await response.json();
  console.log('✓ Registered with CorpusHub');
  console.log(`  Slug: ${result.slug}`);
  console.log(`  Database: ${result.database_path}`);
} else {
  console.warn('⚠️  Registration failed (can register later)');
}
```

### Step 8: Set Up Bidirectional Sync

**Start file watchers for bidirectional artifacts:**
```javascript
const bidirectional = Object.entries(config.artifacts)
  .filter(([_, cfg]) => cfg.sourceMode === 'bidirectional');

if (bidirectional.length > 0) {
  console.log('✓ Setting up bidirectional sync');

  for (const [type, cfg] of bidirectional) {
    await setupFileWatcher(projectPath, type, cfg);
    console.log(`  ✓ Watching ${cfg.path}`);
  }
}
```

### Step 9: Verification

**Verify conversion:**
```javascript
const verification = await detectCorpus(projectPath);

console.log('');
console.log('Conversion Complete!');
console.log('===================');

if (verification.isCorpusEnabled) {
  console.log('Status:');
  console.log(`  ✓ Corpus-enabled: ${verification.config.name}`);
  console.log(`  ✓ Artifacts: ${Object.keys(verification.config.artifacts).length}`);
  console.log(`  ✓ Registered: ${verification.isRegistered ? 'Yes' : 'No'}`);
  console.log(`  ✓ Bits indexed: ${verification.infrastructure.bitCount}`);
} else {
  console.error('✗ Conversion verification failed');
  verification.issues.forEach(issue => {
    console.error(`  ${issue.message}`);
  });
}
```

---

## Project Type Detection

### Web Application

**Indicators:**
- package.json with express/fastify/next
- src/ directory with .js/.ts files
- Tests in tests/ or test/

**Default Artifacts:**
```json
{
  "source-code": { "path": "src", "sourceMode": "source" },
  "api-code": { "path": "src/api", "sourceMode": "source" },
  "frontend-code": { "path": "src/frontend", "sourceMode": "source" },
  "tests": { "path": "tests", "sourceMode": "source" },
  "documentation": { "path": "docs", "sourceMode": "bidirectional" }
}
```

### Content Repository

**Indicators:**
- docs/ directory without src/
- Multiple .md files
- No package.json

**Default Artifacts:**
```json
{
  "documents": { "path": "documents", "sourceMode": "corpus" },
  "guides": { "path": "guides", "sourceMode": "bidirectional" },
  "reference": { "path": "reference", "sourceMode": "bidirectional" }
}
```

### Framework Documentation

**Indicators:**
- specifications/ or framework/ directory
- Multiple .md/.html files
- Structured documentation

**Default Artifacts:**
```json
{
  "specifications": { "path": "specifications", "sourceMode": "corpus" },
  "reference": { "path": "reference", "sourceMode": "bidirectional" },
  "guides": { "path": "guides", "sourceMode": "bidirectional" }
}
```

---

## Content Preservation Strategies

### Git History

**Preserve commit history:**
```javascript
// Don't modify existing files during conversion
// Import copies to CorpusHub database
// Keep original files as source of truth for git

// For corpus-mode artifacts, mark IDE files as read-only
await addWarningComment(file, '<!-- Auto-generated from CorpusHub -->');
```

### Directory Structure

**Preserve existing layout:**
```javascript
// Don't reorganize files
// Map artifacts to existing directories
// Use relative paths in corpus-config.json

// Example: If docs already exist at ./documentation
artifacts['documentation'] = {
  path: 'documentation',  // Preserve existing name
  label: 'Documentation',
  sourceMode: 'bidirectional'
};
```

### File Formats

**Handle multiple formats:**
```javascript
async function convertToHTML(content, filePath) {
  const ext = path.extname(filePath);

  switch (ext) {
    case '.md':
      return await markdownToHTML(content);
    case '.html':
      return content; // Already HTML
    case '.txt':
      return `<pre>${escapeHtml(content)}</pre>`;
    case '.rst':
      return await rstToHTML(content);
    default:
      return `<pre>${escapeHtml(content)}</pre>`;
  }
}
```

---

## Migration Scenarios

### Scenario 1: Existing Documentation Site

```
User: "Convert my documentation site to corpus"

Structure:
  docs/
    index.md
    api/
      endpoints.md
      authentication.md
    guides/
      getting-started.md

Conversion:
  → Detect: Content repository
  → Artifacts:
    - documents (docs/, corpus mode)
    - guides (docs/guides/, bidirectional)
  → Import all .md files to CorpusHub
  → Set up watchers for bidirectional content
```

### Scenario 2: Active Development Project

```
User: "Enable corpus features on this web app"

Structure:
  src/
    api/
    frontend/
  tests/
  docs/
    README.md

Conversion:
  → Detect: Web application
  → Artifacts:
    - source-code (src/, source mode - no import)
    - tests (tests/, source mode - no import)
    - documentation (docs/, bidirectional - import)
  → Only import docs/ to CorpusHub
  → Source code stays in IDE only
```

### Scenario 3: Legacy Project

```
User: "Migrate legacy project to corpus"

Structure:
  /legacy-code/
  /old-docs/
  README.txt

Conversion:
  → Detect: Custom structure
  → Prompt user for artifact mapping
  → User maps:
    - legacy-code → source-code (source mode)
    - old-docs → documentation (corpus mode)
    - README.txt → readme (bidirectional)
  → Import corpus/bidirectional to CorpusHub
  → Preserve all existing files
```

---

## Error Handling

### CorpusHub Not Running

```javascript
if (!isCorpusHubRunning()) {
  console.warn('⚠️  CorpusHub not running');
  console.log('Conversion will proceed with:');
  console.log('  ✓ Create corpus-config.json');
  console.log('  ✓ Create .corpus/ infrastructure');
  console.log('  ✗ Registration (requires CorpusHub)');
  console.log('  ✗ Content import (requires CorpusHub)');
  console.log('');
  console.log('To complete conversion:');
  console.log('  1. Start CorpusHub');
  console.log('  2. Run: corpus-detect <project-path>');

  const proceed = await promptUser('Proceed with offline conversion?');
  if (!proceed) return;
}
```

### Existing corpus-config.json

```javascript
if (await exists(path.join(projectPath, 'corpus-config.json'))) {
  console.warn('⚠️  corpus-config.json already exists');

  const action = await promptUser('What to do?', [
    'Cancel conversion',
    'Backup and overwrite',
    'Merge with existing'
  ]);

  if (action === 'Cancel conversion') return;

  if (action === 'Backup and overwrite') {
    await backupConfig(projectPath);
    // Continue with conversion
  }

  if (action === 'Merge with existing') {
    const existing = await loadCorpusConfig(projectPath);
    // Merge detected artifacts with existing
    config.artifacts = { ...existing.artifacts, ...config.artifacts };
  }
}
```

---

## Quick Reference

**Convert project:**
```javascript
await convertToCorpus(projectPath);
```

**Convert with custom artifacts:**
```javascript
await convertToCorpus(projectPath, {
  artifacts: customArtifacts,
  projectType: 'web-app'
});
```

**Offline conversion:**
```javascript
await convertToCorpus(projectPath, {
  skipRegistration: true,
  skipImport: true
});
```

**Verify conversion:**
```javascript
const status = await detectCorpus(projectPath);
console.log('Converted:', status.isCorpusEnabled);
```

---

*End of Corpus Conversion*
*Part of v4.0.0 Universal Skills Ecosystem*
*Preserves existing structure, git history, and content*
