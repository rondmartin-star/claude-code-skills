---
name: corpus-orchestrator
description: >
  Route corpus management operations to specialized skills with learning-first architecture.
  Detects intent, assesses complexity, and delegates to corpus-init, corpus-convert, corpus-config,
  source-mode-manager, or corpus-detect. Routes medium/complex tasks through corpus-battle-plan.
  Use when: user mentions corpus operations but specific skill unclear.
---

# Corpus Orchestrator

**Purpose:** Route corpus management operations with battle-plan integration
**Size:** ~10 KB
**Type:** Core Orchestrator (Universal)
**Learning Integration:** Uses corpus-battle-plan for medium/complex operations

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Manage this corpus"
- "Set up corpus"
- "Work with corpus"
- "Corpus operations"
- Generic corpus questions

**Context Indicators:**
- Ambiguous corpus request
- Multiple corpus operations needed
- User unsure which corpus skill to use

## ❌ DO NOT LOAD WHEN

- Specific operation clear:
  - "Initialize corpus" → corpus-init directly
  - "Convert to corpus" → corpus-convert directly
  - "Check corpus status" → corpus-detect directly
  - "Configure artifacts" → corpus-config directly
  - "Set up sync" → source-mode-manager directly

---

## Complexity Assessment for Corpus Operations

**Before routing, assess task complexity to determine if battle-plan workflow is needed:**

```javascript
function assessCorpusComplexity(operation, context) {
  const complexityIndicators = {
    trivial: [
      operation === 'status',
      operation === 'check',
      operation === 'verify',
      context.readOnly === true
    ],
    simple: [
      operation === 'configure' && context.singleSetting === true,
      operation === 'detect',
      context.noRisks === true
    ],
    medium: [
      operation === 'init' || operation === 'initialize',
      operation === 'configure' && context.multipleSettings === true,
      operation === 'source-mode' && context.singleArtifact === true
    ],
    complex: [
      operation === 'convert' || operation === 'migrate',
      operation === 're-initialize',
      operation === 'source-mode' && context.multipleArtifacts === true,
      context.hasExistingContent === true,
      context.requiresBackup === true
    ]
  };

  // Check from complex → trivial
  for (const level of ['complex', 'medium', 'simple', 'trivial']) {
    const matches = complexityIndicators[level].filter(indicator => indicator === true);
    if (matches.length > 0) {
      return {
        level,
        useBattlePlan: (level === 'medium' || level === 'complex'),
        confidence: matches.length / complexityIndicators[level].length
      };
    }
  }

  // Default to medium if unclear
  return { level: 'medium', useBattlePlan: true, confidence: 0.5 };
}
```

**Complexity Examples:**

| Operation | Complexity | Use Battle-Plan? | Reason |
|-----------|------------|------------------|--------|
| corpus-detect (status check) | Trivial | No | Read-only, no changes |
| corpus-config (single setting) | Simple | No | Single value update |
| corpus-init (new project) | Medium | Yes | Multi-step setup, risks |
| corpus-convert (existing) | Complex | Yes | Migration, backup, risks |
| source-mode-manager (multi) | Complex | Yes | Multiple artifacts, sync |

**Battle-Plan Integration:**
```javascript
async function routeWithComplexity(operation, context) {
  const complexity = assessCorpusComplexity(operation, context);

  if (!complexity.useBattlePlan) {
    // Trivial or simple - execute directly
    console.log(`${complexity.level} operation - executing directly`);
    return { skill: getSkillForOperation(operation), battlePlan: null };
  }

  // Medium or complex - use corpus-battle-plan
  console.log(`${complexity.level} operation - using corpus-battle-plan`);
  return {
    skill: getSkillForOperation(operation),
    battlePlan: 'corpus-battle-plan',
    complexity: complexity.level
  };
}
```

---

## Routing Decision Tree

### Step 1: Detect Corpus Status

**First, always check if project is corpus-enabled:**

```javascript
const status = await detectCorpus(projectPath);

if (!status.isCorpusEnabled) {
  // Not corpus-enabled → Initialize or Convert
  return routeToSetup(projectContext);
}

// Already corpus-enabled → Manage or Configure
return routeToManagement(projectContext);
```

### Step 2: Route to Setup (Not Corpus-Enabled)

```javascript
async function routeToSetup(context) {
  // Check if has existing content/structure
  const hasContent = checkForExistingContent(context.projectPath);

  let operation, targetSkill;

  if (!hasContent || context.isNewProject) {
    // New project → Initialize
    operation = 'init';
    targetSkill = 'corpus-init';
    console.log('Operation: Initialize new corpus');
  } else {
    // Existing project → Convert
    operation = 'convert';
    targetSkill = 'corpus-convert';
    console.log('Operation: Convert existing project');
  }

  // Assess complexity and route
  const complexity = assessCorpusComplexity(operation, {
    ...context,
    hasExistingContent: hasContent,
    requiresBackup: hasContent
  });

  if (!complexity.useBattlePlan) {
    console.log(`Routing to: ${targetSkill} (direct execution)`);
    return loadSkill(targetSkill);
  }

  // Use corpus-battle-plan for medium/complex operations
  console.log(`\n═══ CORPUS BATTLE-PLAN ═══`);
  console.log(`Complexity: ${complexity.level}`);
  console.log(`Target skill: ${targetSkill}`);
  console.log(`═══════════════════════════\n`);

  const battlePlan = await loadSkill('corpus-battle-plan');
  return await battlePlan.execute({
    targetSkill,
    userRequest: context.userMessage,
    complexity: complexity.level,
    context
  });
}
```

### Step 3: Route to Management (Corpus-Enabled)

```javascript
async function routeToManagement(context) {
  // Analyze user intent
  const intent = analyzeIntent(context.userMessage);

  // Map operation to skill
  const operationMap = {
    'status': { skill: 'corpus-detect', operation: 'status' },
    'check': { skill: 'corpus-detect', operation: 'check' },
    'verify': { skill: 'corpus-detect', operation: 'verify' },
    'configure': { skill: 'corpus-config', operation: 'configure' },
    'update-config': { skill: 'corpus-config', operation: 'configure' },
    'change-artifacts': { skill: 'corpus-config', operation: 'configure' },
    'sync': { skill: 'source-mode-manager', operation: 'source-mode' },
    'source-modes': { skill: 'source-mode-manager', operation: 'source-mode' },
    'bidirectional': { skill: 'source-mode-manager', operation: 'source-mode' },
    're-initialize': { skill: 'corpus-init', operation: 'init' },
    'reset': { skill: 'corpus-init', operation: 'init' }
  };

  const mapping = operationMap[intent.operation];

  if (!mapping) {
    return provideGuidance(intent);
  }

  // Assess complexity
  const complexity = assessCorpusComplexity(mapping.operation, {
    ...context,
    readOnly: (mapping.operation === 'status' || mapping.operation === 'check'),
    singleSetting: intent.targetCount === 1,
    multipleSettings: intent.targetCount > 1,
    singleArtifact: intent.artifacts?.length === 1,
    multipleArtifacts: intent.artifacts?.length > 1
  });

  if (!complexity.useBattlePlan) {
    // Trivial or simple - execute directly
    console.log(`Routing to: ${mapping.skill} (${complexity.level})`);
    return loadSkill(mapping.skill, intent.options);
  }

  // Medium or complex - use corpus-battle-plan
  console.log(`\n═══ CORPUS BATTLE-PLAN ═══`);
  console.log(`Operation: ${intent.operation}`);
  console.log(`Complexity: ${complexity.level}`);
  console.log(`Target skill: ${mapping.skill}`);
  console.log(`═══════════════════════════\n`);

  const battlePlan = await loadSkill('corpus-battle-plan');
  return await battlePlan.execute({
    targetSkill: mapping.skill,
    userRequest: context.userMessage,
    complexity: complexity.level,
    context,
    options: intent.options
  });
}
```

---

## Intent Detection Patterns

### Initialize Intent

**Trigger Patterns:**
```
- "Initialize [this] [as] [a] corpus"
- "Make this corpus-enabled"
- "Set up corpus for this project"
- "Bootstrap corpus"
- "Create new corpus"
```

**Route To:** corpus-init

**Conditions:**
- Project not yet corpus-enabled, OR
- User explicitly requests re-initialization

### Convert Intent

**Trigger Patterns:**
```
- "Convert [this] [to] [a] corpus"
- "Enable corpus [features] [on] existing project"
- "Migrate to corpus"
- "Turn this into a corpus"
```

**Route To:** corpus-convert

**Conditions:**
- Project has existing content
- Not currently corpus-enabled
- Preserve existing structure

### Status Check Intent

**Trigger Patterns:**
```
- "Check corpus status"
- "Is this corpus-enabled?"
- "Show corpus info"
- "Corpus health check"
- "Verify corpus setup"
```

**Route To:** corpus-detect

**Conditions:**
- User wants information, not changes
- Diagnostic/verification purpose

### Configuration Intent

**Trigger Patterns:**
```
- "Configure corpus"
- "Update corpus-config.json"
- "Change artifacts"
- "Add framework terms"
- "Modify voice settings"
```

**Route To:** corpus-config

**Conditions:**
- corpus-config.json exists
- User wants to modify configuration
- Not changing source modes specifically

### Source Mode Intent

**Trigger Patterns:**
```
- "Set up [bidirectional] sync"
- "Change source mode"
- "Configure file watchers"
- "Sync between IDE and CorpusHub"
- "Handle edit conflicts"
```

**Route To:** source-mode-manager

**Conditions:**
- Specifically about source modes (corpus/source/bidirectional)
- Sync-related operations
- Conflict resolution

---

## Routing Examples

### Example 1: New Project (Battle-Plan Workflow)

```
User: "I want to set up corpus for this new project"

Analysis:
  - Intent: Initialize (new project)
  - Corpus Status: Not enabled
  - Context: New project
  - Operation: init

Complexity Assessment:
  - Level: MEDIUM (initialization, multi-step)
  - Use battle-plan: YES
  - Reason: Initialization has risks, requires configuration decisions

Routing Decision:
  → corpus-battle-plan → corpus-init

Battle-Plan Workflow:
═══ CORPUS BATTLE-PLAN ═══
Complexity: medium
Target skill: corpus-init

PHASE 1: CLARIFICATION
  Q: Which audits to enable?
  Q: Confirm directory location?
  ✓ Scope clarified

PHASE 2: KNOWLEDGE CHECK
  ✓ Found pattern: corpus-init-directory-structure (16 uses, 93% success)
  ⚠️ Antipattern: wrong-directory-init (3 occurrences)

PHASE 3: PRE-MORTEM
  Risk #1: Wrong directory (likelihood: 3, impact: 4)
    Prevention: Confirm pwd with user
  Risk #2: Overwrite existing corpus (likelihood: 2, impact: 5)
    Prevention: Check for .corpus/ directory
  Recommendation: GO (with confirmations)

PHASE 4: CONFIRMATION
  About to initialize in: /users/project
  Proceed? [Y/n] → YES

PHASE 5: EXECUTION
  [corpus-init executes with verify-evidence checkpoints]

PHASE 7: DECLARE COMPLETE
  ✓ SHIPPABLE (all requirements met)

PHASE 8: PATTERN UPDATE
  Updated pattern success rate

Reasoning:
  - Medium complexity operation
  - Initialization requires user decisions (audits, structure)
  - Has known risks (wrong directory, overwrite)
  - corpus-battle-plan sequences clarification → pre-mortem → execution
  - Builds institutional knowledge through pattern library
```

### Example 2: Existing Project (Complex - Battle-Plan Required)

```
User: "Convert this existing documentation project to corpus"

Analysis:
  - Intent: Convert (existing → corpus)
  - Corpus Status: Not enabled
  - Context: Has existing content
  - Operation: convert

Complexity Assessment:
  - Level: COMPLEX (migration, has existing content, requires backup)
  - Use battle-plan: YES
  - Reason: High-risk migration with data preservation requirements

Routing Decision:
  → corpus-battle-plan → corpus-convert

Battle-Plan Workflow:
═══ CORPUS BATTLE-PLAN ═══
Complexity: complex
Target skill: corpus-convert

PHASE 2: KNOWLEDGE CHECK
  ✓ Found pattern: backup-before-conversion (safety pattern)
  ✓ Found pattern: preserve-existing-structure
  ⚠️ Antipattern: no-backup-before-migration (2 data loss incidents)

PHASE 3: PRE-MORTEM
  Risk #1: Lose existing files (likelihood: 2, impact: 5)
    Prevention: Create backup before conversion
  Risk #2: Invalid project structure (likelihood: 3, impact: 3)
    Prevention: Validate structure before conversion
  Recommendation: GO WITH CAUTION (backup required)

PHASE 4: CONFIRMATION
  About to convert project with existing files
  BACKUP REQUIRED before proceeding
  Proceed? [Y/n] → YES

PHASE 5: EXECUTION
  ✓ Creating backup...
  ✓ Validating project structure...
  [corpus-convert executes with verify-evidence at each step]
  ✓ Existing files preserved

PHASE 7: DECLARE COMPLETE
  ✓ SHIPPABLE (conversion complete, files preserved)

PHASE 8: PATTERN UPDATE
  Confirmed pattern: backup-before-conversion (successful application)

Reasoning:
  - Complex operation with data loss risk
  - Existing content must be preserved
  - Battle-plan enforces backup before conversion
  - Pre-mortem identified critical risks
  - Pattern library provided proven safety patterns
```

### Example 3: Status Check (Trivial - No Battle-Plan)

```
User: "Is this project corpus-enabled? What's the status?"

Analysis:
  - Intent: Status check (informational)
  - Operation: status
  - No changes requested

Complexity Assessment:
  - Level: TRIVIAL (read-only query)
  - Use battle-plan: NO
  - Reason: No risks, no changes, simple information retrieval

Routing Decision:
  → corpus-detect (direct execution)

Execution:
  - Load corpus-detect skill
  - Execute status check
  - Return results

Reasoning:
  - Trivial read-only operation
  - No risks involved
  - No battle-plan overhead needed
  - Fast, direct execution provides better UX
  - Pattern library not consulted (no value for simple query)
```

### Example 4: Configuration Update

```
User: "I need to add some framework terms to the corpus config"

Analysis:
  - Intent: Configure (modify existing)
  - Corpus Status: Enabled
  - Target: framework.categories

Routing Decision:
  → corpus-config

Reasoning:
  - Corpus already set up
  - User wants to modify configuration
  - corpus-config handles corpus-config.json updates
```

### Example 5: Sync Setup

```
User: "Set up bidirectional sync for the documentation folder"

Analysis:
  - Intent: Source mode (bidirectional)
  - Corpus Status: Enabled
  - Operation: Enable sync

Routing Decision:
  → source-mode-manager

Reasoning:
  - Specifically about source modes
  - Bidirectional sync requires file watchers
  - source-mode-manager handles sync setup
```

---

## Multi-Operation Workflows

### Workflow: Complete Setup

**User Request:** "Set up corpus for this project and configure it"

**Orchestration:**
```javascript
async function handleCompleteSetup(projectPath) {
  // Step 1: Check status
  const status = await runSkill('corpus-detect', { projectPath });

  if (!status.isCorpusEnabled) {
    // Step 2: Initialize or convert
    const hasContent = await checkContent(projectPath);

    if (hasContent) {
      await runSkill('corpus-convert', { projectPath });
    } else {
      await runSkill('corpus-init', { projectPath });
    }
  }

  // Step 3: Configure
  console.log('Corpus initialized. Now configuring...');
  await runSkill('corpus-config', {
    projectPath,
    mode: 'interactive'
  });

  // Step 4: Verify
  const finalStatus = await runSkill('corpus-detect', { projectPath });
  console.log('Setup complete:', finalStatus);
}
```

### Workflow: Migration

**User Request:** "Migrate this project to corpus and set up bidirectional sync for docs"

**Orchestration:**
```javascript
async function handleMigration(projectPath) {
  // Step 1: Convert to corpus
  await runSkill('corpus-convert', { projectPath });

  // Step 2: Configure source modes
  await runSkill('source-mode-manager', {
    operation: 'set-mode',
    artifact: 'documentation',
    mode: 'bidirectional'
  });

  // Step 3: Start watchers
  await runSkill('source-mode-manager', {
    operation: 'start-watchers'
  });

  console.log('✓ Migration complete with bidirectional sync active');
}
```

---

## Guidance Mode

**When intent is unclear, provide guidance:**

```javascript
function provideGuidance(context) {
  console.log('Corpus Operations Available:');
  console.log('');
  console.log('Setup:');
  console.log('  - Initialize new corpus → corpus-init');
  console.log('  - Convert existing project → corpus-convert');
  console.log('');
  console.log('Management:');
  console.log('  - Check status → corpus-detect');
  console.log('  - Update configuration → corpus-config');
  console.log('  - Manage source modes → source-mode-manager');
  console.log('');
  console.log('Current Status:');

  if (context.status.isCorpusEnabled) {
    console.log(`  ✓ Corpus-enabled: ${context.status.config.name}`);
    console.log(`  ✓ ${context.status.infrastructure.bitCount} bits indexed`);
    console.log('');
    console.log('What would you like to do?');
    console.log('  1. View detailed status');
    console.log('  2. Update configuration');
    console.log('  3. Manage source modes');
  } else {
    console.log('  ✗ Not corpus-enabled');
    console.log('');
    console.log('Would you like to:');
    console.log('  1. Initialize new corpus (blank slate)');
    console.log('  2. Convert existing project (preserve content)');
  }

  return promptUserChoice();
}
```

---

## Error Handling

### Invalid Operation

```javascript
if (!isValidCorpusOperation(intent.operation)) {
  console.error(`❌ Unknown corpus operation: ${intent.operation}`);
  console.log('');
  console.log('Valid operations:');
  console.log('  - init, initialize, setup');
  console.log('  - convert, migrate, enable');
  console.log('  - status, check, verify');
  console.log('  - config, configure, update');
  console.log('  - sync, source-modes');
  return;
}
```

### CorpusHub Not Running

```javascript
const hubStatus = await checkCorpusHubStatus();

if (!hubStatus.running) {
  console.warn('⚠️  CorpusHub not running');
  console.log('');
  console.log('Some operations require CorpusHub:');
  console.log('  - Registration (corpus-init, corpus-convert)');
  console.log('  - Detection API (corpus-detect)');
  console.log('  - Bidirectional sync (source-mode-manager)');
  console.log('');
  console.log('Start CorpusHub:');
  console.log('  1. Open CorpusHub application');
  console.log('  2. Or run: C:\\Program Files\\CorpusHub\\CorpusHub.exe');
  console.log('');
  console.log('Continue with offline operations? [y/N]');

  const proceed = await promptUser();
  if (!proceed) return;
}
```

---

## Quick Reference

**Route to skill by intent:**
```javascript
const skill = routeCorpusOperation(userMessage, projectPath);
await loadSkill(skill);
```

**Check status first:**
```javascript
const status = await detectCorpus(projectPath);
if (!status.isCorpusEnabled) {
  // Route to setup
} else {
  // Route to management
}
```

**Multi-step workflows:**
```javascript
// Initialize → Configure → Verify
await runWorkflow('complete-setup', projectPath);

// Convert → Set modes → Start sync
await runWorkflow('migration', projectPath);
```

---

## Configuration

**Battle-Plan Integration Settings:**

```json
{
  "corpusOrchestrator": {
    "battlePlan": {
      "enabled": true,
      "variant": "corpus-battle-plan",
      "complexityThresholds": {
        "init": "medium",
        "convert": "complex",
        "configure": "simple",
        "status": "trivial",
        "source-mode": "medium"
      },
      "autoAssessComplexity": true,
      "alwaysUseForConvert": true,
      "requireBackupForConvert": true
    }
  }
}
```

**Override complexity for specific operations:**
```javascript
await routeCorpusOperation('init', {
  forceComplexity: 'complex',  // Use battle-plan even for init
  skipBattlePlan: false
});
```

---

## Skill Summary

**Corpus Management Skills:**

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| **corpus-detect** | Check corpus status | Status checks, verification |
| **corpus-init** | Initialize new corpus | New projects, re-initialization |
| **corpus-convert** | Convert existing project | Migrate existing content |
| **corpus-config** | Manage configuration | Update corpus-config.json |
| **source-mode-manager** | Handle source modes | Sync, mode changes, conflicts |
| **corpus-orchestrator** | Route operations | Ambiguous or multi-step requests |

---

*End of Corpus Orchestrator*
*Part of v4.0.0 Universal Skills Ecosystem*
*Routes to: corpus-init, corpus-convert, corpus-detect, corpus-config, source-mode-manager*
*Learning Integration: Uses corpus-battle-plan for medium/complex operations*
