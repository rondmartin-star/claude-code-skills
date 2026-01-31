---
name: corpus-init
description: >
  Initialize any project as a corpus-enabled project. Auto-detects project type,
  generates corpus-config.json with CorpusHub schema, sets up source modes, and
  registers with CorpusHub. Use when: setting up new corpus, enabling corpus
  features on existing project, or bootstrapping corpus infrastructure.
---

# Corpus Initialization

**Purpose:** Initialize any project as corpus-enabled with full CorpusHub integration
**Size:** ~13 KB
**Type:** Core Pattern (Universal)

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Initialize this as a corpus"
- "Make this corpus-enabled"
- "Set up corpus for this project"
- "Convert to corpus"
- "Enable corpus features"

**Context Indicators:**
- New project setup
- Adding corpus capabilities to existing project
- Bootstrapping corpus infrastructure
- First-time corpus configuration

## ❌ DO NOT LOAD WHEN

- Project already corpus-enabled (use corpus-config to update)
- Just checking status (use corpus-detect)
- Converting existing corpus (use corpus-convert)

---

## Initialization Workflow

### Step 1: Detection Check

**Always check first:**
```javascript
const status = await detectCorpus(projectPath);

if (status.isCorpusEnabled) {
  console.log(`⚠️  Already corpus-enabled: ${status.config.name}`);

  const choice = await askUser('What would you like to do?', [
    'Update configuration',
    'Re-initialize (overwrites existing)',
    'Cancel'
  ]);

  if (choice === 'Cancel') return;
  if (choice === 'Update configuration') {
    return editCorpusConfig(projectPath);
  }

  console.warn('⚠️  Re-initializing will overwrite corpus-config.json');
}
```

**Why:** Prevent accidental overwrites, respect existing configuration

### Step 2: Project Type Detection

**Auto-detect from project structure:**

```javascript
function detectProjectType(projectPath) {
  // Check for web app indicators
  if (exists(path.join(projectPath, 'package.json'))) {
    const pkg = readJSON(path.join(projectPath, 'package.json'));
    if (pkg.dependencies?.express || pkg.dependencies?.fastify) {
      return 'web-app';
    }
  }

  // Check for documentation project
  if (exists(path.join(projectPath, 'docs')) &&
      !exists(path.join(projectPath, 'src'))) {
    return 'content-corpus';
  }

  // Check for Windows app
  if (exists(path.join(projectPath, 'app.js')) &&
      exists(path.join(projectPath, 'package.json'))) {
    return 'windows-app';
  }

  // Check for framework docs
  if (exists(path.join(projectPath, 'specifications')) ||
      exists(path.join(projectPath, 'framework'))) {
    return 'framework-docs';
  }

  // Default
  return 'content-corpus';
}
```

**Detection Indicators:**

| Project Type | Indicators |
|--------------|------------|
| **web-app** | package.json + express/fastify/next |
| **windows-app** | package.json + app.js + NSSM config |
| **content-corpus** | docs/ without src/ |
| **framework-docs** | specifications/ or framework/ |

### Step 3: Load Configuration Template

**Load appropriate template:**

```javascript
const templatePath = `config/templates/${projectType}.json`;
const template = readJSON(templatePath);
```

**Templates available:**
- `web-app.json` - Full stack web application
- `content-corpus.json` - Documentation/content repository
- `framework-docs.json` - Framework documentation
- `windows-app.json` - Windows desktop application
- `default.json` - Generic fallback

### Step 4: Customize Configuration

**Auto-fill from project:**

```javascript
// Basic metadata
template.corpus.name = await detectProjectName(projectPath);
template.corpus.baseDir = path.resolve(projectPath);
template.corpus.description = await detectDescription(projectPath);

// Auto-detect artifacts
template.artifacts = await detectArtifacts(projectPath, projectType);

// Customize for project
if (projectType === 'web-app') {
  // Check if has tests
  if (exists(path.join(projectPath, 'tests'))) {
    template.artifacts['tests'] = {
      path: 'tests',
      label: 'Test Suite',
      extensions: ['.test.js', '.spec.js'],
      sourceMode: 'source'
    };
  }
}
```

**Detection Strategies:**

**Project Name:**
1. From package.json `name` field
2. From directory name
3. Ask user if unclear

**Description:**
1. From package.json `description`
2. From README.md first paragraph
3. Ask user if missing

**Artifacts:**
1. Scan directory structure
2. Match to common patterns
3. Assign appropriate source modes

### Step 5: Source Mode Assignment

**Assign source modes based on artifact type:**

```javascript
function assignSourceMode(artifactType, path) {
  // Source code → 'source' mode
  if (path.includes('src/') || path.includes('app/')) {
    return 'source';
  }

  // Requirements, specs → 'corpus' mode
  if (path.includes('requirements/') ||
      path.includes('specifications/') ||
      path.includes('design/')) {
    return 'corpus';
  }

  // Documentation → 'bidirectional' mode
  if (path.includes('docs/') ||
      path.includes('guides/') ||
      path.includes('reference/')) {
    return 'bidirectional';
  }

  // Tests → 'source' mode
  if (path.includes('tests/') || path.includes('test/')) {
    return 'source';
  }

  // Default: bidirectional
  return 'bidirectional';
}
```

**Source Modes Explained:**

| Mode | Edited In | Corpus HTML | Use For |
|------|-----------|-------------|---------|
| **corpus** | CorpusHub only | Source of truth | Requirements, design docs, ADRs |
| **source** | IDE (VS Code) | Auto-generated | Implementation code, config files |
| **bidirectional** | Either location | Synced both ways | Documentation, guides, API docs |

### Step 6: User Customization (Optional)

**Interactive prompts:**

```javascript
const customize = await askUser('Customize configuration?', [
  'Use defaults (recommended)',
  'Customize now',
  'Edit corpus-config.json manually after'
]);

if (customize === 'Customize now') {
  // Framework terms
  template.framework.categories = await promptForFrameworkTerms();

  // Voice attributes
  template.voice.attributes = await promptForVoiceAttributes();

  // Roles
  template.roles.available = await promptForRoles();

  // Audit configuration
  template.audit.applicable_audits = await promptForAudits();
}
```

### Step 7: Write Configuration

**Write corpus-config.json:**

```javascript
const configPath = path.join(projectPath, 'corpus-config.json');

// Pretty-print with 2-space indent
await writeJSON(configPath, template, { spaces: 2 });

console.log(`✓ Created corpus-config.json`);
console.log(`  Name: ${template.corpus.name}`);
console.log(`  Type: ${projectType}`);
console.log(`  Artifacts: ${Object.keys(template.artifacts).length} types`);
```

### Step 8: Create Infrastructure

**Create .corpus/ directory:**

```javascript
const corpusDir = path.join(projectPath, '.corpus');

// Create directory structure
await mkdir(corpusDir, { recursive: true });
await mkdir(path.join(corpusDir, 'backups'), { recursive: true });
await mkdir(path.join(corpusDir, 'audit-logs'), { recursive: true });

console.log(`✓ Created .corpus/ infrastructure`);
```

**Create corpus/ directory (for corpus-mode artifacts):**

```javascript
// Only create if has corpus-mode artifacts
const hasCorpusMode = Object.values(template.artifacts)
  .some(a => a.sourceMode === 'corpus');

if (hasCorpusMode) {
  const corpusContentDir = path.join(projectPath, 'corpus');
  await mkdir(corpusContentDir, { recursive: true });

  console.log(`✓ Created corpus/ content directory`);
}
```

### Step 9: Register with CorpusHub

**Register via API:**

```javascript
const response = await fetch('http://localhost:3000/api/corpora/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    path: projectPath,
    config: template
  })
});

if (response.ok) {
  const result = await response.json();
  console.log(`✓ Registered with CorpusHub`);
  console.log(`  Slug: ${result.slug}`);
  console.log(`  Database: ${result.database_path}`);
} else {
  console.warn(`⚠️  CorpusHub registration failed (can register later)`);
}
```

### Step 10: Initialize Database

**Create SQLite database:**

```javascript
const dbPath = path.join(
  corpusHubDataDir,
  'corpora',
  `${template.corpus.slug}.db`
);

await initializeDatabase(dbPath, template);

console.log(`✓ Initialized database`);
console.log(`  Path: ${dbPath}`);
```

### Step 11: Set Up File Watchers (Bidirectional Mode)

**For artifacts with bidirectional mode:**

```javascript
const bidirectionalArtifacts = Object.entries(template.artifacts)
  .filter(([_, config]) => config.sourceMode === 'bidirectional');

if (bidirectionalArtifacts.length > 0) {
  console.log(`✓ Setting up file watchers for bidirectional sync`);

  for (const [type, config] of bidirectionalArtifacts) {
    await setupFileWatcher(projectPath, type, config);
  }
}
```

### Step 12: Generate Documentation

**Create README.md section:**

```javascript
const readmePath = path.join(projectPath, 'README.md');

if (!exists(readmePath)) {
  await createREADME(projectPath, template);
} else {
  // Append corpus section
  await appendCorpusSection(readmePath, template);
}

console.log(`✓ Updated README.md with corpus information`);
```

### Step 13: Final Verification

**Run detection to verify:**

```javascript
const verification = await detectCorpus(projectPath);

if (verification.isCorpusEnabled) {
  console.log('\n✅ Corpus initialization complete!');
  console.log('\nStatus:');
  console.log(`  ✓ Configuration valid`);
  console.log(`  ✓ Infrastructure created`);
  console.log(`  ✓ Registered with CorpusHub`);
  console.log(`  ✓ Database initialized`);

  if (verification.infrastructure.bitCount > 0) {
    console.log(`  ✓ ${verification.infrastructure.bitCount} bits indexed`);
  }
} else {
  console.error('❌ Initialization verification failed');
  verification.issues.forEach(issue => {
    console.error(`  [${issue.severity}] ${issue.message}`);
  });
}
```

---

## Artifact Detection Patterns

### Web Application

```javascript
{
  "source-code": {
    "path": "src",
    "label": "Source Code",
    "extensions": [".js", ".ts"],
    "sourceMode": "source"
  },
  "tests": {
    "path": "tests",
    "label": "Tests",
    "extensions": [".test.js"],
    "sourceMode": "source"
  },
  "documentation": {
    "path": "docs",
    "label": "Documentation",
    "extensions": [".md"],
    "sourceMode": "bidirectional"
  }
}
```

### Content Corpus

```javascript
{
  "documents": {
    "path": "documents",
    "label": "Documents",
    "extensions": [".md", ".html"],
    "sourceMode": "corpus"
  },
  "guides": {
    "path": "guides",
    "label": "Guides",
    "extensions": [".md"],
    "sourceMode": "bidirectional"
  }
}
```

### Framework Documentation

```javascript
{
  "specifications": {
    "path": "specifications",
    "label": "Specifications",
    "extensions": [".md", ".html"],
    "sourceMode": "corpus"
  },
  "reference": {
    "path": "reference",
    "label": "Reference",
    "extensions": [".md"],
    "sourceMode": "bidirectional"
  }
}
```

---

## Configuration Examples

### Minimal Initialization

```bash
User: "Initialize this project as a corpus"

→ Detects: Not corpus-enabled
→ Detects project type: web-app
→ Loads template: config/templates/web-app.json
→ Auto-fills: name, baseDir, artifacts
→ Writes: corpus-config.json
→ Creates: .corpus/, corpus/
→ Registers: CorpusHub
→ Verifies: Success

✅ Done in 5 seconds
```

### Custom Initialization

```bash
User: "Initialize with custom configuration"

→ Detects: Not corpus-enabled
→ Prompts: Project type? [web-app, content-corpus, framework-docs, windows-app]
→ User selects: framework-docs
→ Prompts: Framework terms?
→ User provides: 7 principles, 14 roles
→ Prompts: Audit configuration?
→ User selects: consistency, content, navigation
→ Writes: corpus-config.json
→ Creates: infrastructure
→ Registers: CorpusHub

✅ Done in 2 minutes
```

### Re-initialization

```bash
User: "Initialize this project"

→ Detects: Already corpus-enabled
→ Shows: Current config (Project Name, 5 artifacts)
→ Prompts: What to do? [Update, Re-initialize, Cancel]
→ User selects: Re-initialize
→ Warns: Will overwrite existing
→ Confirms: Yes
→ Backs up: corpus-config.json.backup
→ Proceeds: with initialization

✅ Done with backup preserved
```

---

## Error Handling

### CorpusHub Not Running

```javascript
if (!isCorpusHubRunning()) {
  console.warn('⚠️  CorpusHub not running');
  console.log('Configuration created, but not registered.');
  console.log('To register later:');
  console.log('  1. Start CorpusHub');
  console.log('  2. Run: corpus-detect <project-path>');
  console.log('  3. Or use CorpusHub UI to register manually');

  // Still create config and infrastructure
  return initializeOffline(projectPath, template);
}
```

### Permission Errors

```javascript
try {
  await mkdir(corpusDir);
} catch (error) {
  if (error.code === 'EACCES') {
    console.error('❌ Permission denied creating .corpus/');
    console.log('Try:');
    console.log(`  sudo mkdir ${corpusDir}`);
    console.log(`  sudo chown $USER ${corpusDir}`);
  }
  throw error;
}
```

### Invalid Project Path

```javascript
if (!exists(projectPath)) {
  throw new Error(`Project path does not exist: ${projectPath}`);
}

if (!isDirectory(projectPath)) {
  throw new Error(`Not a directory: ${projectPath}`);
}
```

---

## Post-Initialization

### Next Steps Shown to User

```
✅ Corpus initialization complete!

Next steps:
  1. Review corpus-config.json and customize if needed
  2. Open CorpusHub: http://localhost:3000
  3. Switch to your corpus: <corpus-name>
  4. Start working in CorpusHub or your IDE

Documentation:
  - README.md updated with corpus information
  - See: ~/.claude/skills/core/corpus/corpus-init/README.md

Need help?
  - "How do I use corpus features?"
  - "What are source modes?"
  - "How do I add framework terms?"
```

---

## Quick Reference

**Initialize Project:**
```javascript
await initializeCorpus('/path/to/project');
```

**Initialize with Type:**
```javascript
await initializeCorpus('/path/to/project', {
  projectType: 'web-app',
  customize: false
});
```

**Re-initialize:**
```javascript
await initializeCorpus('/path/to/project', {
  force: true,
  backup: true
});
```

**Offline Mode:**
```javascript
await initializeCorpus('/path/to/project', {
  skipRegistration: true
});
```

---

*End of Corpus Initialization*
*Part of v4.0.0 Universal Skills Ecosystem*
*Integration: CorpusHub Production API*
