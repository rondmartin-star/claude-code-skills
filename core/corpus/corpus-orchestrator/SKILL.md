---
name: corpus-orchestrator
description: >
  Route corpus management operations to specialized skills. Detects intent and
  delegates to corpus-init, corpus-convert, corpus-config, source-mode-manager,
  or corpus-detect. Use when: user mentions corpus operations but specific skill unclear.
---

# Corpus Orchestrator

**Purpose:** Route corpus management operations to specialized skills
**Size:** ~8 KB
**Type:** Core Orchestrator (Universal)

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
function routeToSetup(context) {
  // Check if has existing content/structure
  const hasContent = checkForExistingContent(context.projectPath);

  if (!hasContent || context.isNewProject) {
    // New project → Initialize
    console.log('Routing to: corpus-init');
    console.log('Reason: New project setup');
    return loadSkill('corpus-init');
  }

  // Existing project → Convert
  console.log('Routing to: corpus-convert');
  console.log('Reason: Existing project with content');
  return loadSkill('corpus-convert');
}
```

### Step 3: Route to Management (Corpus-Enabled)

```javascript
function routeToManagement(context) {
  // Analyze user intent
  const intent = analyzeIntent(context.userMessage);

  switch (intent.operation) {
    case 'status':
    case 'check':
    case 'verify':
      return loadSkill('corpus-detect');

    case 'configure':
    case 'update-config':
    case 'change-artifacts':
      return loadSkill('corpus-config');

    case 'sync':
    case 'source-modes':
    case 'bidirectional':
      return loadSkill('source-mode-manager');

    case 're-initialize':
    case 'reset':
      return loadSkill('corpus-init', { force: true });

    default:
      return provideGuidance(intent);
  }
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

### Example 1: New Project

```
User: "I want to set up corpus for this new project"

Analysis:
  - Intent: Initialize (new project)
  - Corpus Status: Not enabled
  - Context: New project

Routing Decision:
  → corpus-init

Reasoning:
  - New project with no existing content
  - User wants to set up from scratch
  - corpus-init handles initialization workflow
```

### Example 2: Existing Project

```
User: "Convert this existing documentation project to corpus"

Analysis:
  - Intent: Convert (existing → corpus)
  - Corpus Status: Not enabled
  - Context: Has existing content

Routing Decision:
  → corpus-convert

Reasoning:
  - Existing project with documentation
  - Need to preserve existing structure
  - corpus-convert handles migration
```

### Example 3: Status Check

```
User: "Is this project corpus-enabled? What's the status?"

Analysis:
  - Intent: Status check (informational)
  - Operation: Diagnostic
  - No changes requested

Routing Decision:
  → corpus-detect

Reasoning:
  - User wants information only
  - corpus-detect provides comprehensive status
  - No modification needed
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
