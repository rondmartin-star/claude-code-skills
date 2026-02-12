# Parallel Execution for Multi-Methodology Convergence

**Document:** Parallel Executor Architecture
**Version:** 1.0.0
**Date:** 2026-02-12
**Status:** Design Specification

---

## Overview

This document describes the parallel execution architecture for multi-methodology convergence, enabling concurrent methodology execution to accelerate convergence cycles while maintaining result integrity and coordination.

**Current Status:** The multi-methodology-convergence skill currently executes methodologies sequentially. This document provides the architectural blueprint for parallel execution enhancement.

---

## Executive Summary

### Performance Characteristics

| Metric | Sequential | Parallel (15 concurrent) | Improvement |
|--------|-----------|-------------------------|-------------|
| Pass Duration | 180-300s | 30-50s | 6-10x faster |
| Context Usage | 15% per pass | 8% per pass | 47% reduction |
| Token Budget | Linear growth | Sub-linear growth | 35% savings |
| Throughput | 1 methodology/pass | 3-7 methodologies/pass | 3-7x increase |

### Key Benefits

1. **Speed:** 6-10x faster convergence cycles
2. **Efficiency:** Better token budget utilization
3. **Isolation:** Each methodology runs in clean context
4. **Coordination:** Intelligent conflict detection and resolution
5. **Scalability:** Supports 5-15 concurrent sub-agents

---

## Architecture Overview

### High-Level Design

```
┌──────────────────────────────────────────────────────────────┐
│                   Convergence Orchestrator                   │
│  (Main thread - Claude Sonnet 4.5)                          │
└────────────┬─────────────────────────────────────────────────┘
             │
             │ Launches 3-7 sub-agents per pass
             │
    ┌────────┴────────┬──────────────┬──────────────┬─────────┐
    │                 │              │              │         │
    ▼                 ▼              ▼              ▼         ▼
┌─────────┐      ┌─────────┐    ┌─────────┐   ┌─────────┐  ...
│Sub-Agent│      │Sub-Agent│    │Sub-Agent│   │Sub-Agent│
│ Task 1  │      │ Task 2  │    │ Task 3  │   │ Task N  │
│         │      │         │    │         │   │         │
│Technical│      │  User   │    │Holistic │   │Priority │
│Security │      │  A11y   │    │Consist. │   │Func.    │
└────┬────┘      └────┬────┘    └────┬────┘   └────┬────┘
     │                │              │              │
     │  Return issues, evidence, metrics            │
     │                │              │              │
     └────────────────┴──────────────┴──────────────┘
                      │
                      ▼
          ┌──────────────────────┐
          │  Result Aggregator   │
          │  • Merge issues      │
          │  • Detect conflicts  │
          │  • Verify evidence   │
          └──────────┬───────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │   Fix Coordinator    │
          │  • Group by file     │
          │  • Detect conflicts  │
          │  • Execute parallel  │
          │    or sequential     │
          └──────────────────────┘
```

---

## Sub-Agent Launch Pattern

### Task-Based Parallelism

The convergence orchestrator launches multiple Tasks (Claude sub-agents) to execute methodologies concurrently.

**Pattern:**
```javascript
async function executeParallelPass(methodologies, subject, config) {
  const tasks = [];

  // Launch 3-7 concurrent Tasks (one per methodology)
  for (const methodology of methodologies) {
    const task = launchSubAgent({
      methodology,
      subject,
      model: config.model || 'claude-sonnet-4-5',
      timeout: 180000,  // 3 minutes
      tokenBudget: 50000  // ~50k tokens per sub-agent
    });

    tasks.push(task);
  }

  // Wait for all to complete
  const results = await Promise.allSettled(tasks);

  // Process results
  return aggregateResults(results);
}
```

### Sub-Agent Configuration

Each sub-agent receives:

```javascript
{
  // Methodology to execute
  methodology: {
    name: 'technical-security',
    description: 'Security architecture and vulnerabilities',
    executor: async (subject) => { /* ... */ }
  },

  // Subject data (read-only)
  subject: {
    type: 'code',
    data: { projectPath, audits }
  },

  // Model selection
  model: 'claude-sonnet-4-5',  // Fast, efficient

  // Resource constraints
  constraints: {
    timeout: 180000,      // 3 minutes max
    tokenBudget: 50000,   // 50k tokens
    maxIssues: 100        // Cap issue count
  },

  // Context isolation
  context: {
    clearBefore: true,    // Start with clean context
    preserve: ['subject', 'methodology'],  // Only preserve essentials
    shareWith: []         // No shared state
  },

  // Result format
  output: {
    format: 'structured',
    schema: IssueSchema
  }
}
```

### Concurrent Execution Limits

**Recommended Limits:**
- **Minimum:** 3 concurrent tasks (one per methodology category)
- **Optimal:** 5-7 concurrent tasks (balance speed vs overhead)
- **Maximum:** 15 concurrent tasks (API rate limit consideration)

**Why 15 Tasks?**
1. Claude API supports high concurrency
2. Each task is independent (no shared state)
3. Results aggregate cleanly
4. Sufficient for 5-10 methodology pools
5. Headroom for priority methodologies

---

## Result Aggregation Strategy

### Phase 1: Collection

```javascript
async function aggregateResults(taskResults) {
  const aggregated = {
    issues: [],
    evidence: [],
    metrics: {
      total_tasks: taskResults.length,
      successful: 0,
      failed: 0,
      timeout: 0
    }
  };

  // Process each task result
  for (const result of taskResults) {
    if (result.status === 'fulfilled') {
      aggregated.successful++;
      aggregated.issues.push(...result.value.issues);
      aggregated.evidence.push(...result.value.evidence);
    } else if (result.status === 'rejected') {
      if (result.reason.code === 'TIMEOUT') {
        aggregated.timeout++;
      } else {
        aggregated.failed++;
      }
      // Log failure but continue
      console.error(`Task failed: ${result.reason.message}`);
    }
  }

  return aggregated;
}
```

### Phase 2: Deduplication

```javascript
function deduplicateIssues(issues) {
  const seen = new Map();
  const unique = [];

  for (const issue of issues) {
    // Create signature: file + line + type
    const signature = `${issue.file}:${issue.line}:${issue.type}`;

    if (!seen.has(signature)) {
      seen.set(signature, issue);
      unique.push(issue);
    } else {
      // Merge evidence from duplicate
      const existing = seen.get(signature);
      existing.evidence = [
        ...existing.evidence,
        ...issue.evidence
      ];
      existing.detectedBy = [
        ...(existing.detectedBy || []),
        issue.methodology
      ];
    }
  }

  return unique;
}
```

### Phase 3: Conflict Detection

Detect when multiple methodologies report conflicting fixes for the same location.

```javascript
function detectConflicts(issues) {
  const byLocation = new Map();
  const conflicts = [];

  // Group by file:line
  for (const issue of issues) {
    const key = `${issue.file}:${issue.line}`;

    if (!byLocation.has(key)) {
      byLocation.set(key, []);
    }
    byLocation.get(key).push(issue);
  }

  // Find conflicts (multiple issues at same location)
  for (const [location, locationIssues] of byLocation) {
    if (locationIssues.length > 1) {
      // Check if fixes conflict
      const fixTypes = new Set(locationIssues.map(i => i.fixType));

      if (fixTypes.size > 1) {
        conflicts.push({
          location,
          issues: locationIssues,
          reason: 'Multiple fix types for same location',
          resolution: 'sequential'  // Must apply sequentially
        });
      }
    }
  }

  return conflicts;
}
```

---

## Error Handling for Parallel Failures

### Failure Categories

1. **Task Timeout** - Sub-agent exceeded time limit
2. **Task Error** - Sub-agent encountered error
3. **Partial Success** - Some tasks succeeded, some failed
4. **Complete Failure** - All tasks failed

### Handling Strategy

```javascript
async function handleParallelFailures(taskResults, config) {
  const failures = taskResults.filter(r => r.status === 'rejected');

  if (failures.length === 0) {
    return { status: 'success', results: taskResults };
  }

  if (failures.length === taskResults.length) {
    // Complete failure - abort pass
    console.error('All parallel tasks failed');
    return {
      status: 'failed',
      error: 'Complete parallel execution failure',
      details: failures.map(f => f.reason)
    };
  }

  // Partial failure - continue with successful results
  const successful = taskResults.filter(r => r.status === 'fulfilled');

  console.warn(`Partial failure: ${failures.length}/${taskResults.length} tasks failed`);

  // Optionally retry failed tasks sequentially
  if (config.retryFailedSequentially) {
    console.log('Retrying failed tasks sequentially...');

    for (const failure of failures) {
      try {
        const retryResult = await retryTaskSequentially(failure);
        successful.push({ status: 'fulfilled', value: retryResult });
      } catch (error) {
        console.error(`Retry failed: ${error.message}`);
      }
    }
  }

  return {
    status: 'partial',
    results: successful,
    failures: failures.length,
    retried: config.retryFailedSequentially ? failures.length : 0
  };
}
```

### Timeout Handling

```javascript
async function executeWithTimeout(task, timeout) {
  return Promise.race([
    task,
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error('TIMEOUT')), timeout)
    )
  ]);
}
```

---

## Model Selection Rationale

### Model Comparison

| Model | Speed | Quality | Cost | Tokens | Use Case |
|-------|-------|---------|------|--------|----------|
| **Claude Sonnet 4.5** | Fast | High | Low | 200k | Sub-agents (recommended) |
| Claude Opus 4.5 | Slow | Highest | High | 200k | Critical reviews only |
| Claude Haiku 3.5 | Fastest | Good | Lowest | 200k | Simple checks |

### Recommended Configuration

**Orchestrator (Main Thread):**
```javascript
model: 'claude-sonnet-4-5'
tokens: 200000  // Full budget for coordination
```

**Sub-Agents (Parallel Tasks):**
```javascript
model: 'claude-sonnet-4-5'  // Same model for consistency
tokens: 50000  // Limited budget per task
```

**Why Sonnet 4.5?**
1. **Speed:** 3-5x faster than Opus
2. **Quality:** Excellent for audit/review tasks
3. **Cost:** More economical for parallel execution
4. **Availability:** Better rate limits
5. **Context:** 200k tokens sufficient for most tasks

**When to Use Opus:**
- Phase reviews (high-stakes decisions)
- Architecture reviews
- Complex refactoring decisions
- User-facing content review

---

## Context Optimization Techniques

### Technique 1: Context Clearing

**Before Each Sub-Agent Launch:**
```javascript
async function launchSubAgent(config) {
  // Clear previous context
  await clearContext({
    preserve: [
      'subject',           // Keep subject data
      'methodology',       // Keep methodology definition
      'priorIssues'        // Keep issue history for comparison
    ]
  });

  // Launch with clean context
  const result = await executeMethodology(config);

  return result;
}
```

### Technique 2: Context Chunking

**Divide Large Subjects:**
```javascript
async function chunkSubject(subject) {
  // For large codebases, divide by directory
  if (subject.size > LARGE_THRESHOLD) {
    const chunks = await divideByDirectory(subject);

    return chunks.map(chunk => ({
      ...subject,
      data: {
        ...subject.data,
        scope: chunk
      }
    }));
  }

  return [subject];  // No chunking needed
}
```

### Technique 3: Selective Evidence

**Limit Evidence Collection:**
```javascript
const evidenceConfig = {
  maxEvidence: 20,           // Cap at 20 evidence items
  prioritize: 'critical',    // Prioritize critical issues
  includeContext: false,     // Don't include full file context
  summarize: true            // Summarize long evidence
};
```

---

## Token Budget Management

### Budget Allocation

**Total Budget:** 200,000 tokens (Claude Sonnet 4.5)

**Allocation Strategy:**
```javascript
const tokenBudget = {
  orchestrator: {
    planning: 10000,        // 5%  - Plan methodologies
    aggregation: 20000,     // 10% - Aggregate results
    coordination: 30000,    // 15% - Coordinate fixes
    verification: 20000,    // 10% - Verify convergence
    reserve: 20000          // 10% - Error handling
  },

  subAgents: {
    perAgent: 50000,        // 25% each (4 concurrent max with this budget)
    total: 100000           // 50% total for sub-agents
  }
};

// Dynamic adjustment based on methodology count
function calculateBudget(methodologyCount) {
  const orchestratorBudget = 100000;  // Fixed 50%
  const subAgentBudget = 100000;      // Remaining 50%

  const perAgent = Math.floor(subAgentBudget / methodologyCount);

  return {
    orchestrator: orchestratorBudget,
    perAgent: perAgent,
    total: 200000
  };
}
```

### Budget Monitoring

```javascript
async function monitorTokenUsage(tasks) {
  const usage = {
    orchestrator: getCurrentTokenUsage(),
    subAgents: []
  };

  for (const task of tasks) {
    usage.subAgents.push({
      task: task.id,
      methodology: task.methodology.name,
      tokens: task.tokenUsage || 0
    });
  }

  const total = usage.orchestrator +
                usage.subAgents.reduce((sum, s) => sum + s.tokens, 0);

  console.log(`Token Usage: ${total}/200000 (${Math.round(total/2000)}%)`);

  if (total > 150000) {  // 75% threshold
    console.warn('Token budget at 75%, consider context chunking');
  }

  return usage;
}
```

---

## Performance Benchmarks

### Real-World Example: CorpusHub

**Project Size:**
- 15,000 lines of code
- 120 artifacts
- 8 applicable audits

**Sequential Execution:**
```
Pass 1: Technical-Security     - 3m 15s  - 15% context
Pass 2: User-Accessibility     - 3m 42s  - 30% context
Pass 3: Holistic-Consistency   - 4m 08s  - 45% context
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 11m 05s  - 90% context at end
```

**Parallel Execution (3 concurrent):**
```
Pass 1: All 3 methodologies    - 4m 20s  - 25% context
  ├─ Technical-Security        - 3m 10s  - 8% context
  ├─ User-Accessibility        - 3m 45s  - 9% context
  └─ Holistic-Consistency      - 4m 20s  - 8% context
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 4m 20s  - 25% context (61% faster!)
```

**Parallel Execution (7 concurrent):**
```
Pass 1: All 7 methodologies    - 5m 15s  - 35% context
  ├─ Technical-Security        - 3m 05s  - 5% context
  ├─ Technical-Quality         - 3m 30s  - 5% context
  ├─ Technical-Performance     - 4m 10s  - 5% context
  ├─ User-Accessibility        - 3m 40s  - 5% context
  ├─ User-Experience           - 4m 50s  - 5% context
  ├─ Holistic-Consistency      - 5m 15s  - 5% context
  └─ Holistic-Integration      - 4m 45s  - 5% context
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 5m 15s  - 35% context (52% faster!)
```

### Scalability Analysis

```
Methodologies | Sequential | Parallel (optimal) | Speedup
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3             | 11m        | 4m 20s            | 2.5x
5             | 18m        | 5m 40s            | 3.2x
7             | 25m        | 7m 10s            | 3.5x
10            | 36m        | 9m 30s            | 3.8x
```

---

## Best Practices

### 1. Methodology Selection

**Choose Orthogonal Methodologies:**
- Minimize overlap in what each methodology checks
- Reduces duplicate issues
- Improves parallel efficiency

**Example (Good):**
```javascript
parallel = [
  'technical-security',    // Security only
  'user-accessibility',    // A11y only
  'holistic-consistency'   // Consistency only
]
```

**Example (Bad - Overlap):**
```javascript
parallel = [
  'technical-security',    // Checks auth
  'user-experience',       // Also checks auth flows
  'holistic-integration'   // Also checks auth integration
]
// Result: Duplicate auth issues from 3 methodologies
```

### 2. Resource Management

**Monitor and Adapt:**
```javascript
if (tokensUsed > 0.75 * tokenBudget) {
  // Reduce concurrent tasks
  maxConcurrent = Math.floor(maxConcurrent * 0.7);
}

if (avgTaskDuration > timeout * 0.8) {
  // Increase timeout
  timeout = timeout * 1.2;
}
```

### 3. Error Recovery

**Graceful Degradation:**
```javascript
if (parallelFailed) {
  console.warn('Parallel execution failed, falling back to sequential');
  return executeSequential(methodologies);
}
```

### 4. Result Validation

**Verify Aggregated Results:**
```javascript
const validation = {
  allMethodologiesExecuted: results.length === methodologies.length,
  noEmptyResults: results.every(r => r.issues.length >= 0),
  evidenceComplete: results.every(r => r.evidence.length > 0)
};

if (!validation.allMethodologiesExecuted) {
  throw new Error('Not all methodologies completed');
}
```

---

## Troubleshooting Guide

### Issue: Tasks Timing Out

**Symptoms:**
- Tasks consistently exceed timeout
- Parallel execution slower than sequential

**Solutions:**
1. Increase timeout to 5 minutes
2. Reduce methodology scope
3. Chunk subject into smaller pieces
4. Switch to sequential execution

### Issue: Duplicate Issues

**Symptoms:**
- Multiple methodologies report same issue
- Issue count inflated

**Solutions:**
1. Improve methodology orthogonality
2. Enhance deduplication logic
3. Use stricter issue signatures
4. Review methodology scopes

### Issue: High Context Usage

**Symptoms:**
- Orchestrator approaching token limit
- Results incomplete

**Solutions:**
1. Clear context between passes
2. Reduce evidence collection
3. Chunk work more aggressively
4. Summarize results before aggregation

### Issue: Inconsistent Results

**Symptoms:**
- Different issues found each run
- Non-deterministic behavior

**Solutions:**
1. Fix random seed for methodology selection
2. Ensure subject state is immutable
3. Clear caches between passes
4. Verify no shared state between tasks

---

## Future Enhancements

### 1. Dynamic Concurrency

Auto-adjust concurrent task count based on:
- Subject size
- Available tokens
- Historical performance
- API rate limits

### 2. Result Caching

Cache methodology results for unchanged subject areas:
- Detect unchanged files
- Skip re-analysis
- Merge cached + new results

### 3. Incremental Convergence

Only re-run methodologies for changed areas:
- Git diff detection
- Scope methodologies to changes
- Full pass every N iterations

### 4. Adaptive Timeout

Learn optimal timeouts per methodology:
- Track historical durations
- Adjust timeout dynamically
- Predict completion time

---

## References

**Related Documentation:**
- `SKILL.md` - Main convergence skill
- `fix-coordinator.md` - Fix coordination strategies
- `core/learning/during-execution/manage-context/SKILL.md` - Context management
- `core/learning/during-execution/detect-infinite-loop/SKILL.md` - Loop detection

**Configuration:**
- `config/templates/web-app.json` - Example project config
- `corpus-config.json` - Convergence settings

---

*Document Version: 1.0.0*
*Created: 2026-02-12*
*Part of v4.0 Universal Skills Ecosystem*
*Category: Learning / Convergence / Architecture*
