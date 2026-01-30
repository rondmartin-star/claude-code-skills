# Corpus Status - Check and Toggle Corpus-Enabled State

## Purpose

This skill checks if the current project is corpus-enabled and offers to toggle its state:
- **If enabled** → Offers to disable (unregister)
- **If not enabled** → Offers to enable (initialize or convert)

**Use this skill when:**
- User asks "is this project corpus-enabled?"
- User wants to quickly toggle corpus features on/off
- Checking project status before other operations
- Managing corpus-enabled state interactively

---

## Workflow

```
User: "Is this project corpus-enabled?" or "Check corpus status"
↓
1. Detect current project location (cwd)
2. Call detection API to check corpus status
3. Display status clearly (enabled or not)
4. Ask user if they want to toggle the state
5. If yes:
   → If NOT enabled: Route to corpus-init or corpus-convert
   → If enabled: Offer to disable (unregister)
6. Execute the chosen action
```

**Total time:** 1-2 minutes

---

## Detection Phase

### Step 1: Get Current Directory

```javascript
const projectPath = process.cwd();
console.log(`Checking corpus status for: ${projectPath}`);
```

### Step 2: Ensure Server is Running

**IMPORTANT: Auto-start server if not running**

```javascript
// Check if server is accessible
async function ensureServerRunning() {
  try {
    const health = await fetch('http://localhost:3000/api/health');
    if (health.ok) return true;
  } catch (err) {
    console.log('Server not running. Starting CorpusHub server...');

    // Try MSI installed version first (most reliable)
    const msiPath = 'C:\\Program Files\\CorpusHub';
    if (fs.existsSync(path.join(msiPath, 'node', 'node.exe'))) {
      console.log('Using MSI installed version...');
      exec(`cd "${msiPath}" && .\\node\\node.exe .\\server\\index.js`, {
        detached: true,
        stdio: 'ignore'
      });
    } else {
      // Try npm start in current directory
      console.log('Using development version...');
      exec('npm start', {
        cwd: process.cwd(),
        detached: true,
        stdio: 'ignore'
      });
    }

    // Wait for server to be ready
    console.log('Waiting for server to start...');
    for (let i = 0; i < 30; i++) {
      await new Promise(resolve => setTimeout(resolve, 1000));
      try {
        const health = await fetch('http://localhost:3000/api/health');
        if (health.ok) {
          console.log('✓ Server started successfully');
          return true;
        }
      } catch {}
    }

    throw new Error('Server failed to start after 30 seconds');
  }
}

// Ensure server is running before detection
await ensureServerRunning();
```

### Step 3: Call Detection API

```javascript
const response = await fetch(
  `http://localhost:3000/api/corpora/detect?path=${encodeURIComponent(projectPath)}`
);
const status = await response.json();
```

### Step 3: Display Status

**If Corpus-Enabled:**
```
✅ This project IS corpus-enabled

Details:
  • Name: My Project
  • Slug: my-project
  • Source Mode: traditional
  • Registered: Yes
  • Infrastructure: Valid
  • Database: Accessible
  • Bits: 47 files

Last accessed: 2026-01-30 14:00:00
```

**If NOT Corpus-Enabled:**
```
❌ This project is NOT corpus-enabled

Current state:
  • No corpus-config.json found

This appears to be a standard project without CorpusHub features.
```

**If Partially Enabled (has issues):**
```
⚠️  This project has partial corpus infrastructure

Status:
  • Config: ✓ Found
  • Valid: ✗ Errors detected
  • Registered: ✗ Not registered

Issues:
  [ERROR] Missing required field: corpus.name
  [WARNING] Corpus not registered in CorpusHub

You may need to fix these issues before proceeding.
```

---

## Toggle Prompt

### Case A: Currently Enabled → Offer to Disable

```javascript
const choice = await askUser({
  question: 'Would you like to disable corpus features for this project?',
  header: 'Toggle Status',
  options: [
    {
      label: 'Yes, disable corpus (Recommended)',
      description: 'Unregister from CorpusHub and optionally remove corpus files',
      value: 'disable'
    },
    {
      label: 'View health report',
      description: 'Check detailed health status before deciding',
      value: 'health'
    },
    {
      label: 'No, keep enabled',
      description: 'Keep corpus features active',
      value: 'keep'
    }
  ]
});
```

**If user chooses "disable":**
```javascript
// Ask what to remove
const removeOptions = await askUser({
  question: 'What would you like to remove?',
  header: 'Removal Options',
  multiSelect: true,
  options: [
    {
      label: 'Unregister from CorpusHub',
      description: 'Remove from corpus registry (required)',
      value: 'unregister'
    },
    {
      label: 'Delete corpus directory',
      description: 'Remove generated corpus files',
      value: 'corpus-dir'
    },
    {
      label: 'Delete corpus-config.json',
      description: 'Remove configuration file',
      value: 'config'
    },
    {
      label: 'Delete database',
      description: 'Remove corpus database',
      value: 'database'
    }
  ]
});

// Execute removal
await unregisterCorpus(projectPath, removeOptions);
```

### Case B: Currently NOT Enabled → Offer to Enable

```javascript
const choice = await askUser({
  question: 'Would you like to enable corpus features for this project?',
  header: 'Toggle Status',
  options: [
    {
      label: 'Yes, enable corpus (Recommended)',
      description: 'Initialize or convert this project to be corpus-enabled',
      value: 'enable'
    },
    {
      label: 'Learn more',
      description: 'See what corpus features provide',
      value: 'info'
    },
    {
      label: 'No, keep disabled',
      description: 'Continue without corpus features',
      value: 'skip'
    }
  ]
});
```

**If user chooses "enable":**
```javascript
// Determine if new or existing project
const hasFiles = await hasDocumentationFiles(projectPath);

if (hasFiles) {
  // Route to corpus-convert
  console.log('Detected existing documentation. Using corpus-convert...');
  // Launch corpus-convert skill
} else {
  // Route to corpus-init
  console.log('Creating new corpus structure. Using corpus-init...');
  // Launch corpus-init skill
}
```

### Case C: Partially Enabled (Issues) → Offer to Fix or Reset

```javascript
const choice = await askUser({
  question: 'This project has corpus issues. What would you like to do?',
  header: 'Fix Issues',
  options: [
    {
      label: 'Fix issues automatically',
      description: 'Attempt to repair corpus infrastructure',
      value: 'fix'
    },
    {
      label: 'Re-initialize from scratch',
      description: 'Start fresh (preserves original files)',
      value: 'reinit'
    },
    {
      label: 'Disable corpus features',
      description: 'Remove all corpus infrastructure',
      value: 'disable'
    },
    {
      label: 'View detailed report',
      description: 'See all detected issues',
      value: 'report'
    }
  ]
});
```

---

## Disabling Corpus Features

### Unregister API Call

```javascript
async function unregisterCorpus(projectPath, options) {
  const corpus = await getCorpusByPath(projectPath);

  if (!corpus) {
    console.log('Project is not registered in CorpusHub.');
    return;
  }

  console.log(`Unregistering corpus: ${corpus.name} (${corpus.slug})`);

  // Call unregister API
  const response = await fetch(
    `http://localhost:3000/api/corpora/${corpus.slug}`,
    {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        deleteFiles: options.includes('corpus-dir'),
        deleteConfig: options.includes('config'),
        deleteDatabase: options.includes('database')
      })
    }
  );

  if (response.ok) {
    console.log('✅ Corpus unregistered successfully');

    // Show what was removed
    console.log('\nRemoved:');
    if (options.includes('unregister')) {
      console.log('  ✓ Registration from CorpusHub');
    }
    if (options.includes('corpus-dir')) {
      console.log('  ✓ Corpus directory');
    }
    if (options.includes('config')) {
      console.log('  ✓ corpus-config.json');
    }
    if (options.includes('database')) {
      console.log('  ✓ Corpus database');
    }

    console.log('\nYou can re-enable corpus features later using "corpus init"');
  } else {
    const error = await response.json();
    console.error('❌ Failed to unregister:', error.message);
  }
}
```

### What Gets Removed

**Unregister only (minimal):**
- Removes entry from corpus_registry table
- Keeps all files intact
- Can re-register immediately

**Unregister + Delete corpus directory:**
- Removes registration
- Deletes `corpus/` directory with all generated HTML
- Keeps corpus-config.json
- Keeps database

**Full removal:**
- Removes registration
- Deletes `corpus/` directory
- Deletes `corpus-config.json`
- Deletes database file
- Project returns to non-corpus state

---

## Enabling Corpus Features

### Route to Appropriate Skill

**New Project (no existing docs):**
```
Routing to corpus-init...

This skill will:
  • Create directory structure
  • Generate corpus-config.json
  • Register with CorpusHub
  • Set up artifact types
```

**Existing Project (has docs):**
```
Routing to corpus-convert...

This skill will:
  • Scan existing documentation
  • Infer artifact types
  • Generate corpus-config.json
  • Convert files to corpus format
  • Register with CorpusHub
```

---

## API Endpoints Used

### 1. Detect Status
```
GET /api/corpora/detect?path=/absolute/path/to/project
```

### 2. Unregister Corpus
```
DELETE /api/corpora/:slug
Body: {
  "deleteFiles": boolean,
  "deleteConfig": boolean,
  "deleteDatabase": boolean
}
```

### 3. Health Check (optional)
```
GET /api/corpora/:slug/health
```

---

## User Experience Examples

### Example 1: Checking Enabled Project

```
User: "Is this project corpus-enabled?"