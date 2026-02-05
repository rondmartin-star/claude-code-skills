---
name: corpus-battle-plan
description: >
  Battle-plan variant for corpus operations (initialization, conversion, configuration).
  Specializes master battle-plan with corpus-specific patterns, antipatterns, and risk
  databases. Use when: corpus-init, corpus-convert, corpus management tasks.
---

# Corpus Battle-Plan

**Purpose:** Learning-first workflow for corpus operations
**Type:** Battle-Plan Variant (Specialized for Corpus)
**Base:** Extends master battle-plan

---

## Specializations

### 1. Pattern Library Focus

**Category:** corpus-operations

**Patterns Directory:**
```
.corpus/learning/patterns/corpus-operations/
├── initialization.json
├── conversion.json
├── configuration.json
├── migration.json
└── backup.json
```

**Common Patterns:**
- corpus-init-directory-structure (proven setup)
- config-template-application (standard config)
- git-hook-integration (automated workflows)
- backup-before-conversion (safety pattern)

**Common Antipatterns:**
- wrong-directory-init (initialization in wrong location)
- missing-corpus-config (forgot to create config)
- no-backup-before-migration (risky migrations)
- overwrite-existing-corpus (data loss)

### 2. Pre-Mortem Risk Database

**Risk Database:** `.corpus/learning/risks/corpus-risks.json`

**Corpus-Specific Risks:**
```json
{
  "initialization": [
    {
      "risk": "Initialize in wrong directory",
      "likelihood": 3,
      "impact": 4,
      "prevention": "Verify pwd, show full path, ask user to confirm"
    },
    {
      "risk": "Overwrite existing corpus",
      "likelihood": 2,
      "impact": 5,
      "prevention": "Check for existing .corpus/, require explicit confirmation"
    },
    {
      "risk": "Missing required dependencies",
      "likelihood": 2,
      "impact": 3,
      "prevention": "Check for git, required tools before init"
    }
  ],
  "conversion": [
    {
      "risk": "Lose existing project files",
      "likelihood": 2,
      "impact": 5,
      "prevention": "Create backup before conversion"
    },
    {
      "risk": "Invalid project structure",
      "likelihood": 3,
      "impact": 3,
      "prevention": "Validate project structure before conversion"
    }
  ],
  "configuration": [
    {
      "risk": "Invalid configuration format",
      "likelihood": 3,
      "impact": 3,
      "prevention": "Validate against schema before saving"
    },
    {
      "risk": "Audit configuration errors",
      "likelihood": 2,
      "impact": 3,
      "prevention": "Test audit config after changes"
    }
  ]
}
```

### 3. Verify-Evidence Checks

**Corpus-specific evidence requirements:**

**For corpus-init:**
```javascript
{
  requiredEvidence: [
    ".corpus/ directory exists",
    ".corpus/config.json exists and valid",
    ".corpus/audits/ directory exists",
    ".corpus/learning/ initialized",
    "Git hooks installed (if git repo)",
    "All required subdirectories present"
  ]
}
```

**For corpus-convert:**
```javascript
{
  requiredEvidence: [
    "Backup created",
    "Project structure validated",
    ".corpus/ structure created",
    "Existing files preserved",
    "corpus-config.json generated from project"
  ]
}
```

### 4. Example Flow: Corpus-Init

```
User: "Initialize this as a corpus"

═══ PHASE 1: CLARIFICATION ═══
CLARIFY-REQUIREMENTS:
  Q: What type of corpus?
  Q: Where initialize? (verify current directory)
  Q: Which audits to enable?
  [User answers questions]
  ✓ Scope clarified

═══ PHASE 2: KNOWLEDGE CHECK ═══
PATTERN-LIBRARY (corpus-operations):
  ✓ Found: corpus-init-directory-structure (15 uses, 93% success)
  ⚠️ Found antipattern: wrong-directory-init (3 occurrences)
  Recommendation: Verify directory before proceeding

═══ PHASE 3: RISK ASSESSMENT ═══
PRE-MORTEM (corpus-specific risks):
  Risk #1: Wrong directory (likelihood: 3, impact: 4, score: 12)
    Prevention: Show full path, ask user to confirm
    pwd = /users/you/project
    Confirm this is correct location? [Y/n]

  Risk #2: Overwrite existing corpus (likelihood: 2, impact: 5, score: 10)
    Prevention: Check for existing .corpus/
    ✓ No existing .corpus/ found

  Recommendation: GO
  Conditions: User confirms directory location

═══ PHASE 4: CONFIRMATION ═══
CONFIRM-OPERATION:
  About to initialize corpus in: /users/you/project
  Will create:
    - .corpus/ directory structure
    - .corpus/config.json with audits: [code-quality, security]
    - .corpus/learning/ pattern library
    - Git hooks (if git repo)

  Impacts:
    - 15 files created
    - ~50 KB disk space
    - Git hooks will run on commit

  Rollback: Delete .corpus/ directory

  Proceed? [Y/n] → YES

═══ PHASE 5: EXECUTION ═══
Applying pattern: corpus-init-directory-structure

  Creating .corpus/ structure...
  ├─ .corpus/config.json ✓
  │  [VERIFY-EVIDENCE: Config valid JSON ✓]
  ├─ .corpus/audits/ ✓
  ├─ .corpus/learning/ ✓
  │  ├─ patterns/corpus-operations/ ✓
  │  ├─ antipatterns/corpus-operations/ ✓
  │  ├─ risks/corpus-risks.json ✓
  │  └─ pre-mortems/ ✓
  ├─ .corpus/backups/ ✓
  └─ Git hooks installed ✓

  [VERIFY-EVIDENCE: All required directories exist ✓]
  [VERIFY-EVIDENCE: Config valid ✓]

═══ PHASE 6: REFLECTION ═══
No errors occurred ✓

═══ PHASE 7: DECLARE COMPLETE ═══
Requirements Met:
  - Core: 5/5 (100%) ✓
  - .corpus/ structure created
  - Config generated
  - Learning infrastructure initialized

Status: ✓ SHIPPABLE

═══ PHASE 8: PATTERN UPDATE ═══
Updated pattern: corpus-init-directory-structure
  Applications: 16 (was 15)
  Success rate: 93.75% (was 93%)

✓ Pattern library updated
```

---

## Configuration

```json
{
  "corpusBattlePlan": {
    "extends": "battle-plan",
    "patternLibrary": {
      "category": "corpus-operations",
      "subcategories": ["initialization", "conversion", "configuration"]
    },
    "preMortem": {
      "riskDatabase": ".corpus/learning/risks/corpus-risks.json",
      "alwaysCheckDirectory": true,
      "alwaysCheckExisting": true
    },
    "verifyEvidence": {
      "corpusStructure": true,
      "configValidity": true,
      "backupCreated": true
    }
  }
}
```

---

## Integration

**Core orchestrator routes corpus operations to corpus-battle-plan:**

```javascript
if (category === 'corpus') {
  return await corpusBattlePlan.execute(userRequest);
}
```

**Corpus orchestrator uses corpus-battle-plan for all operations:**

```javascript
// In corpus-orchestrator/SKILL.md
async function handleCorpusOperation(operation) {
  if (complexity >= 'medium') {
    return await corpusBattlePlan.execute(operation);
  } else {
    return await executeDirect(operation);
  }
}
```

---

*End of Corpus Battle-Plan*
*Specialized variant for corpus operations*
*Extends master battle-plan with corpus patterns, risks, and evidence checks*
