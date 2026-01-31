---
name: corpus-config
description: >
  Manage corpus-config.json files. Read, validate, update artifacts, framework terms,
  voice settings, roles, and audit configuration. Use when: updating corpus configuration,
  adding artifacts, managing framework terms, or configuring audit settings.
---

# Corpus Configuration Manager

**Purpose:** Manage corpus-config.json files with validation
**Size:** ~13 KB
**Type:** Core Pattern (Universal)

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Update corpus config"
- "Add framework terms"
- "Configure artifacts"
- "Modify voice settings"
- "Change audit configuration"

**Context Indicators:**
- Updating corpus-config.json
- Adding/removing artifacts
- Changing framework categories
- Configuring roles or permissions
- Setting up audit methodologies

## ❌ DO NOT LOAD WHEN

- Initializing new corpus (use corpus-init)
- Converting existing project (use corpus-convert)
- Checking corpus status (use corpus-detect)
- Setting up sync (use source-mode-manager)

---

## Configuration Schema

### Complete Structure

```json
{
  "corpus": {
    "name": "Project Name",
    "description": "Project description",
    "version": "1.0.0",
    "baseDir": "/absolute/path",
    "slug": "project-slug"
  },
  "artifacts": {
    "artifact-key": {
      "path": "relative/path",
      "label": "Display Label",
      "extensions": [".ext"],
      "sourceMode": "corpus|source|bidirectional"
    }
  },
  "framework": {
    "categories": [{
      "id": "category-id",
      "label": "Category Label",
      "terms": ["Term 1", "Term 2"],
      "canonicalSource": "artifact-key",
      "matchMode": "word-boundary|case-insensitive|exact"
    }]
  },
  "voice": {
    "promptFile": "path/to/prompt.md",
    "attributes": ["professional", "clear"],
    "avoid": ["jargon", "ambiguity"],
    "preferredTerms": {}
  },
  "roles": {
    "available": ["admin", "editor", "author", "reviewer", "viewer", "pending"],
    "defaultRole": "pending",
    "aiAccess": ["admin", "editor", "author"],
    "editAccess": ["admin", "editor", "author"]
  },
  "consistency": {
    "enabled": true,
    "scanDirectories": ["src/", "docs/"]
  },
  "audit": {
    "methodology": "multi-methodology-3-3-1",
    "applicable_audits": ["security", "quality"],
    "convergence": { /* see audit config */ }
  }
}
```

---

## Reading Configuration

### Load and Validate

```javascript
async function loadCorpusConfig(projectPath) {
  const configPath = path.join(projectPath, 'corpus-config.json');

  if (!await exists(configPath)) {
    throw new Error('corpus-config.json not found');
  }

  const config = await readJSON(configPath);

  // Validate schema
  const validation = validateSchema(config);

  if (!validation.valid) {
    console.error('Configuration validation failed:');
    validation.errors.forEach(err => {
      console.error(`  [${err.severity}] ${err.path}: ${err.message}`);
    });
    throw new Error('Invalid configuration');
  }

  return config;
}
```

### Validation Rules

```javascript
function validateSchema(config) {
  const errors = [];

  // Required: corpus section
  if (!config.corpus) {
    errors.push({
      path: 'corpus',
      message: 'Missing required section',
      severity: 'error'
    });
  } else {
    if (!config.corpus.name) {
      errors.push({
        path: 'corpus.name',
        message: 'Name is required',
        severity: 'error'
      });
    }
    if (!config.corpus.baseDir) {
      errors.push({
        path: 'corpus.baseDir',
        message: 'baseDir is required',
        severity: 'error'
      });
    }
  }

  // Required: artifacts section (must be object)
  if (!config.artifacts) {
    errors.push({
      path: 'artifacts',
      message: 'Missing required section',
      severity: 'error'
    });
  } else if (typeof config.artifacts !== 'object') {
    errors.push({
      path: 'artifacts',
      message: 'Must be an object (not array)',
      severity: 'error'
    });
  }

  // Validate each artifact
  for (const [key, artifact] of Object.entries(config.artifacts || {})) {
    if (!artifact.path) {
      errors.push({
        path: `artifacts.${key}.path`,
        message: 'Path is required',
        severity: 'error'
      });
    }
    if (!artifact.sourceMode) {
      errors.push({
        path: `artifacts.${key}.sourceMode`,
        message: 'sourceMode is required',
        severity: 'error'
      });
    } else if (!['corpus', 'source', 'bidirectional'].includes(artifact.sourceMode)) {
      errors.push({
        path: `artifacts.${key}.sourceMode`,
        message: `Invalid sourceMode: ${artifact.sourceMode}`,
        severity: 'error'
      });
    }
  }

  // Framework categories validation
  if (config.framework?.categories) {
    config.framework.categories.forEach((cat, idx) => {
      if (!cat.id) {
        errors.push({
          path: `framework.categories[${idx}].id`,
          message: 'Category ID is required',
          severity: 'error'
        });
      }
      if (!cat.matchMode) {
        errors.push({
          path: `framework.categories[${idx}].matchMode`,
          message: 'matchMode is required',
          severity: 'warning',
          suggestion: 'Add matchMode: "word-boundary"'
        });
      }
    });
  }

  return {
    valid: errors.filter(e => e.severity === 'error').length === 0,
    errors
  };
}
```

---

## Updating Configuration

### Update Entire Section

```javascript
async function updateSection(projectPath, section, data) {
  const config = await loadCorpusConfig(projectPath);

  // Update section
  config[section] = data;

  // Validate
  const validation = validateSchema(config);
  if (!validation.valid) {
    throw new Error('Updated configuration would be invalid');
  }

  // Write
  await writeConfig(projectPath, config);

  console.log(`✓ Updated ${section}`);
}
```

---

## Artifact Management

### Add Artifact

```javascript
async function addArtifact(projectPath, key, config) {
  const corpusConfig = await loadCorpusConfig(projectPath);

  // Check if exists
  if (corpusConfig.artifacts[key]) {
    throw new Error(`Artifact '${key}' already exists`);
  }

  // Default values
  const artifact = {
    path: config.path,
    label: config.label || key,
    extensions: config.extensions || ['.md'],
    sourceMode: config.sourceMode || 'bidirectional'
  };

  // Add to config
  corpusConfig.artifacts[key] = artifact;

  // Validate
  const validation = validateSchema(corpusConfig);
  if (!validation.valid) {
    throw new Error('Invalid artifact configuration');
  }

  // Write
  await writeConfig(projectPath, corpusConfig);

  console.log(`✓ Added artifact: ${key}`);
  console.log(`  Path: ${artifact.path}`);
  console.log(`  Mode: ${artifact.sourceMode}`);
}
```

### Remove Artifact

```javascript
async function removeArtifact(projectPath, key) {
  const config = await loadCorpusConfig(projectPath);

  if (!config.artifacts[key]) {
    throw new Error(`Artifact '${key}' not found`);
  }

  // Remove from config
  delete config.artifacts[key];

  // Write
  await writeConfig(projectPath, config);

  console.log(`✓ Removed artifact: ${key}`);
}
```

### Update Artifact

```javascript
async function updateArtifact(projectPath, key, updates) {
  const config = await loadCorpusConfig(projectPath);

  if (!config.artifacts[key]) {
    throw new Error(`Artifact '${key}' not found`);
  }

  // Merge updates
  config.artifacts[key] = {
    ...config.artifacts[key],
    ...updates
  };

  // Validate
  const validation = validateSchema(config);
  if (!validation.valid) {
    throw new Error('Updated artifact configuration would be invalid');
  }

  // Write
  await writeConfig(projectPath, config);

  console.log(`✓ Updated artifact: ${key}`);
}
```

---

## Framework Term Management

### Add Category

```javascript
async function addFrameworkCategory(projectPath, category) {
  const config = await loadCorpusConfig(projectPath);

  if (!config.framework) {
    config.framework = { categories: [] };
  }

  // Check for duplicate ID
  if (config.framework.categories.some(c => c.id === category.id)) {
    throw new Error(`Category '${category.id}' already exists`);
  }

  // Default values
  const newCategory = {
    id: category.id,
    label: category.label || category.id,
    terms: category.terms || [],
    canonicalSource: category.canonicalSource,
    matchMode: category.matchMode || 'word-boundary'
  };

  config.framework.categories.push(newCategory);

  await writeConfig(projectPath, config);

  console.log(`✓ Added framework category: ${category.id}`);
  console.log(`  Terms: ${newCategory.terms.length}`);
}
```

### Add Terms to Category

```javascript
async function addTermsToCategory(projectPath, categoryId, terms) {
  const config = await loadCorpusConfig(projectPath);

  const category = config.framework?.categories?.find(c => c.id === categoryId);

  if (!category) {
    throw new Error(`Category '${categoryId}' not found`);
  }

  // Add new terms (avoid duplicates)
  const existingTerms = new Set(category.terms);
  const newTerms = terms.filter(t => !existingTerms.has(t));

  category.terms.push(...newTerms);

  await writeConfig(projectPath, config);

  console.log(`✓ Added ${newTerms.length} new terms to ${categoryId}`);
}
```

### Remove Category

```javascript
async function removeFrameworkCategory(projectPath, categoryId) {
  const config = await loadCorpusConfig(projectPath);

  if (!config.framework?.categories) {
    throw new Error('No framework categories defined');
  }

  const index = config.framework.categories.findIndex(c => c.id === categoryId);

  if (index === -1) {
    throw new Error(`Category '${categoryId}' not found`);
  }

  config.framework.categories.splice(index, 1);

  await writeConfig(projectPath, config);

  console.log(`✓ Removed framework category: ${categoryId}`);
}
```

---

## Voice Configuration

### Update Voice Settings

```javascript
async function updateVoice(projectPath, voiceConfig) {
  const config = await loadCorpusConfig(projectPath);

  config.voice = {
    ...config.voice,
    ...voiceConfig
  };

  await writeConfig(projectPath, config);

  console.log('✓ Updated voice configuration');
}
```

### Add Voice Attributes

```javascript
async function addVoiceAttributes(projectPath, attributes) {
  const config = await loadCorpusConfig(projectPath);

  if (!config.voice) {
    config.voice = { attributes: [] };
  }

  // Merge attributes
  const existing = new Set(config.voice.attributes || []);
  const newAttrs = attributes.filter(a => !existing.has(a));

  config.voice.attributes = [...config.voice.attributes, ...newAttrs];

  await writeConfig(projectPath, config);

  console.log(`✓ Added ${newAttrs.length} voice attributes`);
}
```

---

## Role Configuration

### Update Roles

```javascript
async function updateRoles(projectPath, roleConfig) {
  const config = await loadCorpusConfig(projectPath);

  config.roles = {
    ...config.roles,
    ...roleConfig
  };

  // Validate role references
  const availableRoles = new Set(config.roles.available);

  for (const role of config.roles.aiAccess || []) {
    if (!availableRoles.has(role)) {
      throw new Error(`aiAccess references undefined role: ${role}`);
    }
  }

  for (const role of config.roles.editAccess || []) {
    if (!availableRoles.has(role)) {
      throw new Error(`editAccess references undefined role: ${role}`);
    }
  }

  await writeConfig(projectPath, config);

  console.log('✓ Updated role configuration');
}
```

---

## Audit Configuration

### Update Applicable Audits

```javascript
async function updateApplicableAudits(projectPath, audits) {
  const config = await loadCorpusConfig(projectPath);

  if (!config.audit) {
    config.audit = {};
  }

  config.audit.applicable_audits = audits;

  await writeConfig(projectPath, config);

  console.log(`✓ Updated applicable audits: ${audits.join(', ')}`);
}
```

### Configure Methodology

```javascript
async function configureMethodology(projectPath, methodologyConfig) {
  const config = await loadCorpusConfig(projectPath);

  if (!config.audit) {
    config.audit = {};
  }

  if (!config.audit.convergence) {
    config.audit.convergence = {};
  }

  config.audit.convergence = {
    ...config.audit.convergence,
    ...methodologyConfig
  };

  await writeConfig(projectPath, config);

  console.log('✓ Updated audit methodology configuration');
}
```

---

## Backup and Restore

### Create Backup

```javascript
async function backupConfig(projectPath) {
  const configPath = path.join(projectPath, 'corpus-config.json');
  const timestamp = new Date().toISOString().replace(/:/g, '-');
  const backupPath = path.join(
    projectPath,
    '.corpus',
    'backups',
    `corpus-config.${timestamp}.json`
  );

  await copyFile(configPath, backupPath);

  console.log(`✓ Backup created: ${backupPath}`);
  return backupPath;
}
```

### Restore Backup

```javascript
async function restoreConfig(projectPath, backupPath) {
  const configPath = path.join(projectPath, 'corpus-config.json');

  // Validate backup
  const backup = await readJSON(backupPath);
  const validation = validateSchema(backup);

  if (!validation.valid) {
    throw new Error('Backup file is invalid');
  }

  // Create backup of current config before restore
  await backupConfig(projectPath);

  // Restore
  await copyFile(backupPath, configPath);

  console.log('✓ Configuration restored from backup');
}
```

---

## Utility Functions

### Write Configuration

```javascript
async function writeConfig(projectPath, config) {
  const configPath = path.join(projectPath, 'corpus-config.json');

  // Pretty-print with 2-space indent
  await writeJSON(configPath, config, { spaces: 2 });
}
```

### Get Configuration Value

```javascript
function getConfigValue(config, path) {
  const parts = path.split('.');
  let current = config;

  for (const part of parts) {
    if (current === undefined) return undefined;
    current = current[part];
  }

  return current;
}
```

---

## Quick Reference

**Load config:**
```javascript
const config = await loadCorpusConfig(projectPath);
```

**Add artifact:**
```javascript
await addArtifact(projectPath, 'api-docs', {
  path: 'docs/api',
  sourceMode: 'bidirectional'
});
```

**Update field:**
```javascript
await updateField(projectPath, 'corpus.version', '2.0.0');
```

**Add framework terms:**
```javascript
await addTermsToCategory(projectPath, 'security-concepts', [
  'OAuth 2.0',
  'CSRF protection'
]);
```

**Backup:**
```javascript
await backupConfig(projectPath);
```

---

*End of Corpus Configuration Manager*
*Part of v4.0.0 Universal Skills Ecosystem*
*Schema: CorpusHub Production*
