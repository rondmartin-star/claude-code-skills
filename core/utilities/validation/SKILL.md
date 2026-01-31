---
name: validation
description: >
  Validation utility for corpus configuration, skill structure, and ecosystem integrity.
  Validates schemas, file structure, references, and compliance. Use when: validating
  setup, checking integrity, or quality assurance.
---

# Validation Utility

**Purpose:** Corpus and skill ecosystem validation
**Type:** Utility Skill (Universal)

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Validate corpus"
- "Check configuration"
- "Verify skill structure"
- "Validate setup"

**Context Indicators:**
- After configuration changes
- Before deployment
- Quality assurance
- Development/testing

---

## Validation Types

### 1. Corpus Configuration

**Schema Validation:**
```javascript
const CORPUS_CONFIG_SCHEMA = {
  type: 'object',
  required: ['name', 'version', 'artifacts'],
  properties: {
    name: { type: 'string', minLength: 1 },
    version: { type: 'string', pattern: '^\\d+\\.\\d+\\.\\d+$' },
    artifacts: {
      type: 'object',
      patternProperties: {
        '^[a-z0-9-]+$': {
          type: 'object',
          required: ['path', 'sourceMode'],
          properties: {
            path: { type: 'string' },
            sourceMode: { enum: ['corpus', 'source', 'bidirectional'] },
            title: { type: 'string' }
          }
        }
      }
    },
    voice: {
      type: 'object',
      properties: {
        attributes: { type: 'array', items: { type: 'string' } },
        avoid: { type: 'array', items: { type: 'string' } }
      }
    },
    roles: {
      type: 'object',
      properties: {
        editAccess: { type: 'array', items: { type: 'string' } },
        aiAccess: { type: 'array', items: { type: 'string' } }
      }
    },
    audit: { type: 'object' }
  }
};

async function validateCorpusConfig(configPath) {
  const errors = [];
  const warnings = [];

  // Check file exists
  if (!fs.existsSync(configPath)) {
    errors.push({
      type: 'missing_file',
      path: configPath,
      message: 'corpus-config.json not found'
    });
    return { valid: false, errors, warnings };
  }

  // Parse JSON
  let config;
  try {
    config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  } catch (e) {
    errors.push({
      type: 'invalid_json',
      message: e.message
    });
    return { valid: false, errors, warnings };
  }

  // Validate schema
  const ajv = new Ajv();
  const validate = ajv.compile(CORPUS_CONFIG_SCHEMA);
  const valid = validate(config);

  if (!valid) {
    errors.push(...validate.errors.map(err => ({
      type: 'schema_violation',
      path: err.instancePath,
      message: err.message
    })));
  }

  // Check artifact paths exist
  for (const [name, artifact] of Object.entries(config.artifacts || {})) {
    const artifactPath = path.join(path.dirname(configPath), artifact.path);

    if (!fs.existsSync(artifactPath)) {
      errors.push({
        type: 'missing_artifact',
        artifact: name,
        path: artifact.path,
        message: `Artifact path does not exist: ${artifact.path}`
      });
    }
  }

  // Check version format
  if (config.version && !/^\d+\.\d+\.\d+$/.test(config.version)) {
    warnings.push({
      type: 'invalid_version',
      version: config.version,
      message: 'Version should follow semver (X.Y.Z)'
    });
  }

  return {
    valid: errors.length === 0,
    errors,
    warnings,
    config
  };
}
```

### 2. Skill Structure

**SKILL.md Validation:**
```javascript
const SKILL_FRONTMATTER_SCHEMA = {
  type: 'object',
  required: ['name', 'description'],
  properties: {
    name: {
      type: 'string',
      pattern: '^[a-z0-9]+(-[a-z0-9]+)*$'  // kebab-case
    },
    description: {
      type: 'string',
      minLength: 10,
      not: { pattern: '[<>]' }  // No angle brackets
    }
  }
};

async function validateSkill(skillDir) {
  const errors = [];
  const warnings = [];

  // Check SKILL.md exists
  const skillMdPath = path.join(skillDir, 'SKILL.md');
  if (!fs.existsSync(skillMdPath)) {
    errors.push({
      type: 'missing_skill_md',
      message: 'SKILL.md not found'
    });
    return { valid: false, errors, warnings };
  }

  // Read and parse frontmatter
  const content = fs.readFileSync(skillMdPath, 'utf8');
  const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);

  if (!frontmatterMatch) {
    errors.push({
      type: 'missing_frontmatter',
      message: 'SKILL.md missing YAML frontmatter'
    });
    return { valid: false, errors, warnings };
  }

  let frontmatter;
  try {
    frontmatter = yaml.parse(frontmatterMatch[1]);
  } catch (e) {
    errors.push({
      type: 'invalid_frontmatter',
      message: `YAML parse error: ${e.message}`
    });
    return { valid: false, errors, warnings };
  }

  // Validate frontmatter schema
  const ajv = new Ajv();
  const validate = ajv.compile(SKILL_FRONTMATTER_SCHEMA);
  const valid = validate(frontmatter);

  if (!valid) {
    errors.push(...validate.errors.map(err => ({
      type: 'frontmatter_schema',
      path: err.instancePath,
      message: err.message
    })));
  }

  // Check size limit (15KB)
  const size = fs.statSync(skillMdPath).size;
  if (size > 15360) {  // 15KB = 15360 bytes
    errors.push({
      type: 'size_exceeded',
      size,
      limit: 15360,
      message: `SKILL.md exceeds 15KB limit (${(size / 1024).toFixed(2)}KB)`
    });
  } else if (size > 14336) {  // 93% of limit
    warnings.push({
      type: 'size_warning',
      size,
      message: `SKILL.md approaching limit (${((size / 15360) * 100).toFixed(1)}%)`
    });
  }

  // Check README exists
  const readmePath = path.join(skillDir, 'README.md');
  if (!fs.existsSync(readmePath)) {
    warnings.push({
      type: 'missing_readme',
      message: 'README.md not found'
    });
  }

  return {
    valid: errors.length === 0,
    errors,
    warnings,
    frontmatter,
    size
  };
}
```

### 3. Reference Integrity

**Check Internal Links:**
```javascript
async function validateReferences(skillDir) {
  const errors = [];
  const warnings = [];

  const files = await glob(`${skillDir}/**/*.md`);

  for (const file of files) {
    const content = fs.readFileSync(file, 'utf8');

    // Find markdown links
    const links = content.match(/\[([^\]]+)\]\(([^)]+)\)/g) || [];

    for (const link of links) {
      const match = link.match(/\[([^\]]+)\]\(([^)]+)\)/);
      const href = match[2];

      // Skip external links
      if (href.startsWith('http://') || href.startsWith('https://')) {
        continue;
      }

      // Skip anchors
      if (href.startsWith('#')) {
        continue;
      }

      // Check file exists
      const targetPath = path.join(path.dirname(file), href);

      if (!fs.existsSync(targetPath)) {
        errors.push({
          type: 'broken_link',
          file: path.relative(skillDir, file),
          link: href,
          message: `Broken link: ${href}`
        });
      }
    }

    // Find code references to other skills
    const skillRefs = content.match(/['"]([\w-]+\/[\w-]+)['"]/g) || [];

    for (const ref of skillRefs) {
      const skillPath = ref.replace(/['"]/g, '');

      // Check if looks like a skill path
      if (/^[\w-]+\/[\w-]+$/.test(skillPath)) {
        const fullPath = path.join(skillDir, '..', '..', skillPath, 'SKILL.md');

        if (!fs.existsSync(fullPath)) {
          warnings.push({
            type: 'possible_broken_skill_ref',
            file: path.relative(skillDir, file),
            skillPath,
            message: `Possible broken skill reference: ${skillPath}`
          });
        }
      }
    }
  }

  return { valid: errors.length === 0, errors, warnings };
}
```

### 4. Ecosystem Integrity

**Validate All Skills:**
```javascript
async function validateEcosystem(rootDir) {
  const results = {
    totalSkills: 0,
    valid: 0,
    invalid: 0,
    errors: [],
    warnings: [],
    skills: []
  };

  // Find all SKILL.md files
  const skillFiles = await glob(`${rootDir}/**/SKILL.md`);

  for (const skillFile of skillFiles) {
    const skillDir = path.dirname(skillFile);
    const skillName = path.basename(skillDir);

    results.totalSkills++;

    const validation = await validateSkill(skillDir);
    const references = await validateReferences(skillDir);

    const isValid = validation.valid && references.valid;

    if (isValid) {
      results.valid++;
    } else {
      results.invalid++;
    }

    results.skills.push({
      name: skillName,
      path: path.relative(rootDir, skillDir),
      valid: isValid,
      errors: [...validation.errors, ...references.errors],
      warnings: [...validation.warnings, ...references.warnings],
      size: validation.size
    });

    results.errors.push(...validation.errors, ...references.errors);
    results.warnings.push(...validation.warnings, ...references.warnings);
  }

  return results;
}
```

### 5. CorpusHub Integration

**Check API Connectivity:**
```javascript
async function validateCorpusHubIntegration(corpusPath) {
  const errors = [];
  const warnings = [];

  const config = JSON.parse(
    fs.readFileSync(path.join(corpusPath, 'corpus-config.json'), 'utf8')
  );

  // Check if registered with CorpusHub
  try {
    const response = await fetch('http://localhost:3000/api/health');

    if (!response.ok) {
      errors.push({
        type: 'corpushub_unavailable',
        message: 'CorpusHub API not responding'
      });
      return { valid: false, errors, warnings };
    }

    // Check corpus registration
    const corpusResponse = await fetch(
      `http://localhost:3000/api/corpora/detect?path=${encodeURIComponent(corpusPath)}`
    );

    if (corpusResponse.ok) {
      const data = await corpusResponse.json();

      if (!data.isCorpusEnabled) {
        warnings.push({
          type: 'not_registered',
          message: 'Corpus not registered with CorpusHub'
        });
      }

      if (!data.isRegistered) {
        warnings.push({
          type: 'registration_incomplete',
          message: 'Corpus detected but registration incomplete'
        });
      }
    }

  } catch (e) {
    warnings.push({
      type: 'corpushub_connection',
      message: `Cannot connect to CorpusHub: ${e.message}`
    });
  }

  return { valid: errors.length === 0, errors, warnings };
}
```

---

## Validation Reports

### CLI Output

**Summary format:**
```
Validating Ecosystem...

✓ 18 skills valid
✗ 3 skills with errors

Errors (5):
  • corpus-detect: SKILL.md exceeds 15KB limit
  • quality: Broken link in README.md
  • seo: Missing frontmatter property: description

Warnings (8):
  • performance: SKILL.md at 98% of size limit
  • accessibility: README.md not found
  • consistency: Possible broken skill reference: audits/quality

Total: 21 skills scanned in 1.2s
```

### JSON Output

```json
{
  "timestamp": "2026-01-31T10:00:00Z",
  "totalSkills": 21,
  "valid": 18,
  "invalid": 3,
  "errors": [
    {
      "skill": "corpus-detect",
      "type": "size_exceeded",
      "size": 16234,
      "limit": 15360
    }
  ],
  "warnings": [
    {
      "skill": "performance",
      "type": "size_warning",
      "size": 15100
    }
  ]
}
```

---

## Configuration

```json
{
  "validation": {
    "checkSize": true,
    "maxSkillSize": 15360,
    "checkReferences": true,
    "checkFrontmatter": true,
    "strict": false
  }
}
```

---

## Quick Reference

**Validate corpus config:**
```javascript
const result = await validateCorpusConfig('./corpus-config.json');
if (!result.valid) {
  console.error('Errors:', result.errors);
}
```

**Validate skill:**
```javascript
const result = await validateSkill('./core/corpus/corpus-init');
console.log(`Valid: ${result.valid}, Size: ${result.size} bytes`);
```

**Validate entire ecosystem:**
```javascript
const result = await validateEcosystem('./core');
console.log(`${result.valid}/${result.totalSkills} skills valid`);
```

---

*End of Validation Utility*
*Part of v4.0.0 Universal Skills Ecosystem*
*Category: Utilities*
*Quality assurance and integrity checking*
