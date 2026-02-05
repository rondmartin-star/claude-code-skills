---
name: manage-context
description: >
  Protects context window by monitoring token usage, chunking work when approaching limits,
  summarizing completed sections, and creating checkpoints. Prevents context degradation
  and quality loss in long sessions. Use when: long sessions, large tasks, context usage high.
---

# Manage Context

**Purpose:** Protect context window, prevent quality degradation in long sessions
**Type:** Learning Skill (During-Execution / Resource Management)
**Attribution:** Based on "Claude Skill Potions" by Elliot (dont-be-greedy skill)

---

## Attribution

**Article:** "Your AI has infinite knowledge and zero habits - here's the fix"
**Author:** Elliot
**Published:** January 28, 2026
**Source:** Medium

**Quote:** *"Context rot over long sessions. Instructions from 20 minutes ago get forgotten. The original goal drifts. Quality degrades even within the context limit."*

**Solution:** *"dont-be-greedy - Chunks data, protects the context window"*

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Context is getting full"
- "Chunk this work"
- "Save checkpoint"
- Before long operations

**Context Indicators:**
- Token usage > 80% of limit
- Session duration > 30 minutes
- Large data processing tasks
- Multi-phase operations
- Context quality degrading

---

## Core Concept

**The Problem (from article):**
> "Context rot over long sessions. Instructions from 20 minutes ago get forgotten. The original goal drifts. Quality degrades even within the context limit. Claude's even forgotten that you swore at it, or has it."

**The Solution:**
1. Monitor context/token usage continuously
2. Before hitting limit, trigger chunking
3. Summarize completed work
4. Write summaries to files
5. Clear detailed context, keep summaries
6. Continue with fresh context

**Why It Matters:**
- Prevents hitting context limit mid-task
- Maintains quality throughout session
- Preserves important context
- Enables indefinitely long operations

---

## Context Management Process

### 1. Monitor Context Usage

```javascript
class ContextMonitor {
  constructor(options = {}) {
    this.maxTokens = options.maxTokens || 200000;
    this.warningThreshold = options.warningThreshold || 0.7;  // 70%
    this.chunkThreshold = options.chunkThreshold || 0.8;      // 80%
    this.currentUsage = 0;
    this.conversationStart = Date.now();
  }

  updateUsage(tokens) {
    this.currentUsage = tokens;
    return this.getStatus();
  }

  getStatus() {
    const percentage = this.currentUsage / this.maxTokens;
    const sessionDuration = (Date.now() - this.conversationStart) / 60000; // minutes

    return {
      tokens: this.currentUsage,
      maxTokens: this.maxTokens,
      percentage,
      remaining: this.maxTokens - this.currentUsage,
      sessionDuration,
      status: this.determineStatus(percentage),
      shouldChunk: percentage >= this.chunkThreshold
    };
  }

  determineStatus(percentage) {
    if (percentage >= this.chunkThreshold) return 'CRITICAL';
    if (percentage >= this.warningThreshold) return 'WARNING';
    return 'OK';
  }
}
```

**Example Monitoring:**
```
Context Status:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tokens used: 165,000 / 200,000 (82.5%)
Remaining: 35,000 tokens
Session duration: 42 minutes
Status: ⚠️ CRITICAL - Chunking recommended

Progress bar:
[████████████████████████████████████░░░░] 82.5%

Breakdown:
- Conversation history: 85,000 tokens
- Current task context: 45,000 tokens
- Code artifacts: 25,000 tokens
- Tool results: 10,000 tokens
```

### 2. Decide When to Chunk

```javascript
function shouldChunk(status, task) {
  // Automatic triggers
  if (status.percentage >= 0.8) {
    return {
      shouldChunk: true,
      reason: `Context usage critical (${status.percentage * 100}%)`,
      urgency: 'immediate'
    };
  }

  if (status.percentage >= 0.7 && task.hasMoreWork()) {
    return {
      shouldChunk: true,
      reason: `Context warning + more work remaining`,
      urgency: 'soon'
    };
  }

  // Task-based triggers
  if (task.naturalBreakpoint && status.percentage >= 0.6) {
    return {
      shouldChunk: true,
      reason: `At natural breakpoint, good time to chunk`,
      urgency: 'opportunistic'
    };
  }

  return {shouldChunk: false};
}
```

**Natural Breakpoints:**
- After completing a major subtask
- Between phases of multi-phase operation
- After successful test run
- Between file processing batches
- After convergence GATE pass

### 3. Summarize Completed Work

```javascript
async function summarizeCompleted(task, workCompleted) {
  const summary = {
    task: {
      original: task.description,
      startTime: task.startTime,
      currentPhase: task.phase
    },
    completed: {
      phases: [],
      artifacts: [],
      decisions: [],
      issues: []
    },
    state: {
      variables: {},
      nextSteps: []
    },
    metrics: {
      filesModified: 0,
      testsRun: 0,
      issuesFixed: 0
    }
  };

  // Summarize each completed phase
  for (const phase of workCompleted.phases) {
    summary.completed.phases.push({
      name: phase.name,
      status: 'completed',
      duration: phase.duration,
      keyOutcomes: phase.outcomes.slice(0, 3), // Top 3 outcomes
      artifacts: phase.artifacts.map(a => a.path)
    });
  }

  // Extract important decisions made
  summary.completed.decisions = workCompleted.decisions.map(d => ({
    decision: d.description,
    rationale: d.rationale,
    alternatives: d.alternativesConsidered
  }));

  // Capture current state
  summary.state.variables = extractCriticalState(task);
  summary.state.nextSteps = generateNextSteps(task);

  return summary;
}
```

**Example Summary:**
```json
{
  "task": {
    "original": "Implement OAuth authentication with token caching",
    "startTime": "2026-02-04T10:00:00Z",
    "currentPhase": "Implementation Phase 2"
  },
  "completed": {
    "phases": [
      {
        "name": "Phase 1: OAuth Configuration",
        "status": "completed",
        "duration": "15 minutes",
        "keyOutcomes": [
          "OAuth config created (src/config/oauth.js)",
          "Provider credentials configured",
          "Redirect URI set up"
        ],
        "artifacts": [
          "src/config/oauth.js",
          "src/config/providers.json"
        ]
      },
      {
        "name": "Phase 2: Route Implementation",
        "status": "completed",
        "duration": "20 minutes",
        "keyOutcomes": [
          "OAuth callback route implemented",
          "Authorization endpoint created",
          "Error handling added"
        ],
        "artifacts": [
          "src/routes/auth.js",
          "src/middleware/oauth.js"
        ]
      }
    ],
    "decisions": [
      {
        "decision": "Use Passport.js for OAuth",
        "rationale": "Most popular, well-tested, supports multiple providers",
        "alternatives": ["Grant.js", "Custom implementation"]
      },
      {
        "decision": "Redis for token caching",
        "rationale": "Fast, supports TTL, already in stack",
        "alternatives": ["In-memory cache", "Database"]
      }
    ],
    "issues": [
      {
        "issue": "Rate limit handling",
        "status": "resolved",
        "solution": "Implemented exponential backoff"
      }
    ]
  },
  "state": {
    "variables": {
      "oauthProviders": ["google", "github"],
      "cacheImplemented": false,
      "testsWritten": false
    },
    "nextSteps": [
      "Implement token caching layer",
      "Write tests for OAuth flow",
      "Integrate with session management"
    ]
  },
  "metrics": {
    "filesModified": 4,
    "testsRun": 0,
    "issuesFixed": 2
  }
}
```

### 4. Create Checkpoint

```javascript
async function createCheckpoint(summary, checkpointPath = '.corpus/learning/checkpoints') {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const filename = `checkpoint-${timestamp}.json`;
  const fullPath = path.join(checkpointPath, filename);

  // Write comprehensive checkpoint
  await writeFile(fullPath, JSON.stringify({
    version: '1.0',
    timestamp: new Date().toISOString(),
    summary,
    restoration: {
      instructions: generateRestorationInstructions(summary),
      criticalContext: extractCriticalContext(summary),
      requiredFiles: summary.completed.phases.flatMap(p => p.artifacts)
    }
  }, null, 2));

  // Also create human-readable summary
  const readmePath = path.join(checkpointPath, `checkpoint-${timestamp}.md`);
  await writeFile(readmePath, generateReadableSummary(summary));

  console.log(`✓ Checkpoint saved: ${fullPath}`);
  console.log(`✓ Summary saved: ${readmePath}`);

  return {checkpointPath: fullPath, summaryPath: readmePath};
}
```

**Checkpoint Structure:**
```
.corpus/learning/checkpoints/
├── checkpoint-2026-02-04T10-30-00.json    # Machine-readable
├── checkpoint-2026-02-04T10-30-00.md      # Human-readable
└── checkpoint-2026-02-04T11-15-00.json    # Next checkpoint
```

**Human-Readable Summary:**
```markdown
# Checkpoint: OAuth Implementation
**Created:** 2026-02-04 10:30:00
**Session Duration:** 42 minutes
**Context Usage:** 165,000 / 200,000 tokens (82.5%)

## What We've Accomplished

### Phase 1: OAuth Configuration ✓
- OAuth config created (src/config/oauth.js)
- Provider credentials configured (Google, GitHub)
- Redirect URI set up

### Phase 2: Route Implementation ✓
- OAuth callback route (src/routes/auth.js)
- Authorization endpoint
- Error handling with exponential backoff

## Key Decisions Made

1. **OAuth Library:** Passport.js
   - Rationale: Most popular, supports multiple providers
   - Alternatives considered: Grant.js, custom implementation

2. **Token Storage:** Redis
   - Rationale: Fast, TTL support, already in stack
   - Alternatives considered: In-memory, database

## Current State

**Variables:**
- OAuth providers: Google, GitHub
- Token caching: NOT YET IMPLEMENTED
- Tests: NOT YET WRITTEN

**Next Steps:**
1. Implement token caching layer (Redis)
2. Write OAuth flow tests
3. Integrate with session management

## Files Modified
- src/config/oauth.js (created)
- src/config/providers.json (created)
- src/routes/auth.js (created)
- src/middleware/oauth.js (created)

## To Resume
Load this checkpoint and continue with: "Implement token caching layer"
```

### 5. Clear Context, Keep Summaries

```javascript
async function chunkWork(monitor, task) {
  console.log("⚠️ Context usage high - chunking work...");

  // 1. Summarize what's completed
  const summary = await summarizeCompleted(task, task.completedWork);

  // 2. Create checkpoint
  const checkpoint = await createCheckpoint(summary);

  // 3. Notify user
  console.log("\n" + "=".repeat(60));
  console.log("CONTEXT CHECKPOINT CREATED");
  console.log("=".repeat(60));
  console.log(`Checkpoint: ${checkpoint.checkpointPath}`);
  console.log(`Summary: ${checkpoint.summaryPath}`);
  console.log("\nCompleted work summarized and saved.");
  console.log("Context will be cleared, keeping only essential state.");
  console.log("Next steps:");
  summary.state.nextSteps.forEach((step, i) => {
    console.log(`${i + 1}. ${step}`);
  });
  console.log("=".repeat(60) + "\n");

  // 4. Clear detailed context (would happen in practice)
  // In practice, this would involve starting a fresh conversation
  // with just the summary loaded

  // 5. Update monitor
  monitor.currentUsage = estimateReducedUsage(summary);

  return {
    chunked: true,
    checkpointPath: checkpoint.checkpointPath,
    summary,
    resumeWith: summary.state.nextSteps[0]
  };
}

function estimateReducedUsage(summary) {
  // Summary is much smaller than full context
  const summarySize = JSON.stringify(summary).length;
  const estimatedTokens = summarySize / 4; // Rough estimate
  return estimatedTokens;
}
```

### 6. Resume from Checkpoint

```javascript
async function resumeFromCheckpoint(checkpointPath) {
  console.log(`Loading checkpoint: ${checkpointPath}`);

  const checkpoint = JSON.parse(await readFile(checkpointPath));

  console.log("\n" + "=".repeat(60));
  console.log("RESUMING FROM CHECKPOINT");
  console.log("=".repeat(60));
  console.log(`Original task: ${checkpoint.summary.task.original}`);
  console.log(`Started: ${checkpoint.summary.task.startTime}`);
  console.log(`Checkpoint created: ${checkpoint.timestamp}`);
  console.log("\nWork completed:");
  checkpoint.summary.completed.phases.forEach((phase, i) => {
    console.log(`${i + 1}. ${phase.name} ✓`);
  });
  console.log("\nNext steps:");
  checkpoint.summary.state.nextSteps.forEach((step, i) => {
    console.log(`${i + 1}. ${step}`);
  });
  console.log("=".repeat(60) + "\n");

  // Restore state
  const state = checkpoint.summary.state;

  return {
    task: checkpoint.summary.task,
    completedPhases: checkpoint.summary.completed.phases,
    currentState: state.variables,
    nextSteps: state.nextSteps,
    resumePoint: state.nextSteps[0]
  };
}
```

---

## Integration with Battle-Plan

**Position:** During Execution (Phase 5) - Continuous Monitoring

**Flow:**
```
Execute Large Task:
├─ Phase 1: Configuration
│  ├─ Work... work... work...
│  └─ Complete ✓ (Context: 40%)
│
├─ Phase 2: Implementation
│  ├─ Work... work... work...
│  └─ Complete ✓ (Context: 75%)
│
├─ [MANAGE-CONTEXT warning: 75%]
│  Monitor: Continue but watch closely
│
├─ Phase 3: Testing
│  ├─ Work... work... work...
│  └─ (Context: 85% - CRITICAL)
│
├─ [MANAGE-CONTEXT triggered]
│  ├─ Summarize Phases 1-3
│  ├─ Create checkpoint
│  ├─ Clear detailed context
│  └─ Load summary (Context: 15%)
│
├─ Phase 4: Integration
│  ├─ Work with fresh context...
│  └─ Complete ✓
└─ Success
```

**Automatic Triggers:**
- 70% usage: Warning displayed
- 80% usage: Automatic chunking
- Natural breakpoints: Opportunistic chunking

---

## Configuration

```json
{
  "manageContext": {
    "enabled": true,
    "thresholds": {
      "warningAt": 0.7,           // 70% - show warning
      "chunkAt": 0.8,             // 80% - auto chunk
      "criticalAt": 0.9           // 90% - urgent chunk
    },
    "chunking": {
      "autoChunk": true,          // Automatic at threshold
      "useNaturalBreakpoints": true,
      "maxChunkSize": 50000,      // Max tokens per chunk
      "minChunkSize": 10000       // Min tokens before chunking
    },
    "checkpoints": {
      "path": ".corpus/learning/checkpoints",
      "createSummary": true,      // Human-readable summary
      "retention": 20,            // Keep last 20 checkpoints
      "includeArtifacts": false   // Don't copy actual files
    },
    "monitoring": {
      "updateInterval": 1000,     // Check every 1000 tokens
      "showProgress": true,       // Show context usage
      "warnUser": true           // Alert at thresholds
    }
  }
}
```

---

## Chunking Strategies

### Strategy 1: Phase-Based Chunking

**Best for:** Multi-phase operations (design → implement → test)

```javascript
async function phaseBasedChunking(task) {
  for (const phase of task.phases) {
    await executePhase(phase);

    // Chunk after each phase
    if (monitor.status.percentage >= 0.6) {
      await chunkWork(monitor, task);
    }
  }
}
```

### Strategy 2: File-Based Chunking

**Best for:** Processing many files

```javascript
async function fileBasedChunking(files) {
  const batchSize = 10;

  for (let i = 0; i < files.length; i += batchSize) {
    const batch = files.slice(i, i + batchSize);
    await processBatch(batch);

    // Chunk after each batch
    if (monitor.status.percentage >= 0.7) {
      await chunkWork(monitor, {
        filesProcessed: i + batch.length,
        filesRemaining: files.length - (i + batch.length)
      });
    }
  }
}
```

### Strategy 3: Time-Based Chunking

**Best for:** Long-running operations

```javascript
async function timeBasedChunking(task) {
  const chunkInterval = 30 * 60 * 1000; // 30 minutes
  let lastChunk = Date.now();

  while (task.hasMoreWork()) {
    await task.doWork();

    if (Date.now() - lastChunk >= chunkInterval) {
      await chunkWork(monitor, task);
      lastChunk = Date.now();
    }
  }
}
```

---

## Benefits

**Prevents:**
- Hitting context limit mid-task
- Quality degradation over time
- Losing important context
- Session failures

**Provides:**
- Indefinite operation length
- Consistent quality
- Recovery points
- Progress preservation

**Enables:**
- Very large tasks
- Multi-session work
- Collaboration (checkpoints shareable)
- Fault tolerance

---

## Quick Reference

**Monitor context:**
```javascript
const monitor = new ContextMonitor({maxTokens: 200000});

// Update after each interaction
monitor.updateUsage(currentTokenCount);

// Check status
if (monitor.getStatus().shouldChunk) {
  await chunkWork(monitor, task);
}
```

**Create checkpoint manually:**
```javascript
const summary = await summarizeCompleted(task, completedWork);
const checkpoint = await createCheckpoint(summary);
console.log(`Checkpoint: ${checkpoint.checkpointPath}`);
```

**Resume from checkpoint:**
```javascript
const state = await resumeFromCheckpoint('path/to/checkpoint.json');
console.log(`Resuming from: ${state.resumePoint}`);
```

---

*End of Manage-Context*
*Part of v4.0.0 Universal Skills Ecosystem*
*Category: Learning / During-Execution (Resource Management)*
*Attribution: Based on "dont-be-greedy" skill from Claude Skill Potions by Elliot*
*"Chunk before you break"*
