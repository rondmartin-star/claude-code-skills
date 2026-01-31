---
name: corpus-detect
description: >
  Detect and validate corpus status for any project directory. Wrapper for
  CorpusHub detection API. Use when: checking if project is corpus-enabled,
  validating corpus infrastructure, or diagnosing corpus issues.
---

# Corpus Detection

**Purpose:** Detect and validate corpus status using CorpusHub API
**Size:** ~9 KB
**Type:** Core Pattern (Universal)

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Check if this is corpus-enabled"
- "Is this project a corpus?"
- "Validate corpus status"
- "Detect corpus infrastructure"
- "Check corpus health"

**Context Indicators:**
- Before initializing corpus
- Before converting project
- Debugging corpus issues
- CI/CD pipeline validation

## ❌ DO NOT LOAD WHEN

- Already confirmed corpus exists
- Creating new corpus from scratch (no detection needed)

---

## CorpusHub Detection API

### Endpoint: Detect Corpus Status

```
GET http://localhost:3000/api/corpora/detect?path={projectPath}
```

**Parameters:**
- `path` (required): Absolute path to project directory

**Response:**

```json
{
  "isCorpusEnabled": true|false,
  "projectPath": "/absolute/path",
  "checks": {
    "configExists": true|false,
    "configValid": true|false,
    "isRegistered": true|false,
    "infrastructureExists": true|false,
    "databaseExists": true|false
  },
  "config": {
    "name": "Project Name",
    "slug": "project-slug",
    "baseDir": "/path",
    "sourceMode": "traditional",
    "corpusDir": "corpus",
    "artifactCount": 5
  },
  "registration": {
    "slug": "project-slug",
    "registered_at": "2026-01-28T10:00:00Z",
    "last_accessed": "2026-01-30T14:00:00Z"
  },
  "infrastructure": {
    "corpusDirExists": true,
    "corpusDirPath": "/path/corpus",
    "databaseExists": true,
    "databasePath": "/corpushub/data/corpora/slug.db",
    "bitCount": 47,
    "fileCount": 47
  },
  "issues": [],
  "suggestions": []
}
```

---

## Detection Checks

### Stage 1: Path Validation
- Verify project path exists and is accessible
- Return error if path invalid

### Stage 2: Config File Check
- Look for `corpus-config.json` in project root
- If not found: `isCorpusEnabled = false` with suggestion

### Stage 3: Config Validation
- Parse JSON and validate structure
- Check required fields: `corpus.name`, `corpus.baseDir`, `artifacts`
- Validate artifact definitions
- Return validation errors

### Stage 4: Registration Check
- Query CorpusHub database for registration
- Check by config_path and base_dir
- Return registration details if found

### Stage 5: Infrastructure Verification
- Check if corpus directory exists
- Count files in corpus directory
- Check if database file exists
- Count bits in database

### Stage 6: Issue Analysis
- Collect all detected issues
- Categorize by severity (error/warning/info)
- Generate actionable suggestions

### Stage 7: Status Determination
Corpus is "enabled" only if:
- ✓ Config exists
- ✓ Config is valid
- ✓ Corpus is registered
- ✓ Infrastructure exists

---

## Usage Patterns

### Pattern 1: Check Before Init

```javascript
// Before running corpus-init
const status = await detectCorpus(projectPath);

if (status.isCorpusEnabled) {
  console.log(`⚠️  Already corpus-enabled: ${status.config.name}`);

  const choice = await askUser('What would you like to do?', [
    'Update configuration',
    'Re-initialize (overwrites existing)',
    'Cancel'
  ]);

  if (choice === 'Cancel') return;
  // Handle choice...
}

// Proceed with initialization
```

### Pattern 2: Diagnose Issues

```javascript
const status = await detectCorpus(projectPath);

if (status.checks.configExists && !status.isCorpusEnabled) {
  console.log('⚠️  Partial corpus infrastructure found with issues:');

  status.issues.forEach(issue => {
    console.log(`  [${issue.severity}] ${issue.message}`);
  });

  console.log('\nSuggestions:');
  status.suggestions.forEach(suggestion => {
    console.log(`  • ${suggestion.description}`);
  });
}
```

### Pattern 3: Validate in CI/CD

```javascript
const status = await detectCorpus(process.env.PROJECT_ROOT);

if (!status.isCorpusEnabled) {
  console.error('❌ Corpus not properly enabled');
  process.exit(1);
}

if (status.issues.length > 0) {
  console.error('❌ Corpus has issues:');
  status.issues.forEach(i => console.error(`  - ${i.message}`));
  process.exit(1);
}

console.log('✅ Corpus validation passed');
```

---

## Common Issues and Solutions

### Issue: "Project path does not exist"
**Solution:** Verify path is absolute and directory exists
```bash
ls "/path/to/project"
realpath ./my-project
```

### Issue: "Config valid but not registered"
**Solution:** Register the corpus
```bash
curl -X POST http://localhost:3000/api/corpora/register \
  -H "Content-Type: application/json" \
  -d '{"path": "/path/to/project"}'
```

### Issue: "Database not found"
**Solution:** Re-scan corpus to rebuild database
```bash
curl -X POST http://localhost:3000/api/corpora/{slug}/refresh
```

### Issue: "Artifacts not accessible"
**Solution:** Check file permissions
```bash
ls -la /path/to/project/docs
chmod -R 755 /path/to/project/docs
```

### Issue: "Invalid JSON in config"
**Solution:** Validate JSON syntax
```bash
cat corpus-config.json | jq .
```

---

## CLI Tool Integration

CorpusHub provides a CLI tool for detection:

```bash
# Basic detection
node scripts/detect-corpus.js /path/to/project

# JSON output
node scripts/detect-corpus.js /path/to/project --json

# Health check
node scripts/detect-corpus.js --health corpus-slug
```

**Exit Codes:**
- 0: Corpus enabled/healthy
- 1: Corpus not enabled/degraded
- 2: Error or critical issues

---

## Integration Examples

### Used by corpus-init

```javascript
async function initializeCorpus(projectPath) {
  // Check if already enabled
  const status = await detectCorpus(projectPath);

  if (status.isCorpusEnabled) {
    // Handle existing corpus
    return handleExistingCorpus(status);
  }

  // Proceed with new initialization
  return createNewCorpus(projectPath);
}
```

### Used by corpus-convert

```javascript
async function convertToCorpus(projectPath) {
  const status = await detectCorpus(projectPath);

  if (status.checks.configExists && !status.isCorpusEnabled) {
    // Partial infrastructure - offer to fix
    return fixCorpusIssues(status);
  }

  // Clean conversion
  return performConversion(projectPath);
}
```

---

## API Response Fields

### checks

| Field | Type | Description |
|-------|------|-------------|
| configExists | boolean | corpus-config.json found |
| configValid | boolean | Valid JSON and schema |
| isRegistered | boolean | Registered in CorpusHub |
| infrastructureExists | boolean | Corpus directory exists |
| databaseExists | boolean | Database file exists |

### config (if exists)

| Field | Type | Description |
|-------|------|-------------|
| name | string | Corpus display name |
| slug | string | URL-safe identifier |
| baseDir | string | Absolute project path |
| sourceMode | string | traditional/v2 |
| corpusDir | string | Corpus directory name |
| artifactCount | number | Number of artifact types |

### issues

| Field | Type | Description |
|-------|------|-------------|
| severity | string | error/warning/info |
| category | string | config/infrastructure/registration |
| message | string | Human-readable description |
| details | string | Technical details |

### suggestions

| Field | Type | Description |
|-------|------|-------------|
| action | string | Suggested action |
| description | string | What to do |
| command | string | CLI command (optional) |
| apiEndpoint | string | API to call (optional) |

---

## Performance

**Detection Time:**
- Cold cache: 150-200ms
- Warm cache: 5-10ms (5-minute TTL)

**Optimization:**
- Results cached for 5 minutes
- Batch operations run in parallel
- Database indexes on corpus_registry table

---

## Quick Reference

**Detect Status:**
```javascript
const status = await detectCorpus('/path/to/project');
console.log(status.isCorpusEnabled); // true/false
```

**Check Specific:**
```javascript
if (status.checks.configExists) {
  // Has config file
}

if (status.checks.configValid) {
  // Config is valid
}

if (status.checks.isRegistered) {
  // Registered in CorpusHub
}
```

**Get Issues:**
```javascript
status.issues.forEach(issue => {
  console.log(`[${issue.severity}] ${issue.message}`);
});
```

**Get Suggestions:**
```javascript
status.suggestions.forEach(s => {
  console.log(`${s.action}: ${s.description}`);
});
```

---

*End of Corpus Detection Skill*
*Part of v4.0.0 Universal Skills Ecosystem*
