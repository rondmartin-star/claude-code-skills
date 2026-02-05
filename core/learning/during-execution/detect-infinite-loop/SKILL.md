---
name: detect-infinite-loop
description: >
  Detects when same approach fails repeatedly and forces strategy change. Monitors
  failure patterns, counts attempts, generates alternatives, and pivots to different
  approaches after N failures. Use when: repeated failures, stuck in loops, same error recurring.
---

# Detect Infinite Loop

**Purpose:** Force strategy change after repeated failures (prevent infinite loops)
**Type:** Learning Skill (During-Execution / Strategy Management)
**Attribution:** Based on "Claude Skill Potions" by Elliot (pivot skill)

---

## Attribution

**Article:** "Your AI has infinite knowledge and zero habits - here's the fix"
**Author:** Elliot
**Published:** January 28, 2026
**Source:** Medium

**Quote:** *"Infinite loops on failed approaches. Claude fails at something, retries the exact same approach five times, burns 30 minutes. Never tries a different strategy. Never escalates. Just keeps going with the confidence of someone absolutely certain the wall will move this time."*

**Solution:** *"pivot - Detects repeated failures, forces strategy change"*

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Try a different approach"
- "This isn't working"
- "Pivot strategy"
- After repeated failures

**Context Indicators:**
- Same error occurring 3+ times
- Same approach failing repeatedly
- Stuck in implementation loop
- No progress after multiple attempts

---

## Core Concept

**The Problem (from article):**
> "Claude fails at something, retries the exact same approach five times, burns 30 minutes. Never tries a different strategy. Never escalates. Just keeps going with the confidence of someone absolutely certain the wall will move this time."

**The Solution:**
1. Monitor approach being used
2. Track failure count per approach
3. After N failures (default: 3), trigger pivot
4. Generate alternative strategies
5. Force Claude to try different approach
6. Escalate if all alternatives fail

**Why It Matters:**
- Prevents wasted time on dead-end approaches
- Forces creative problem-solving
- Breaks infinite retry loops
- Ensures progress or escalation

---

## Detection Process

### 1. Monitor Approach Signatures

```javascript
class ApproachMonitor {
  constructor() {
    this.attempts = [];
    this.currentApproach = null;
  }

  recordAttempt(approach, result) {
    const signature = this.generateSignature(approach);

    this.attempts.push({
      signature,
      approach,
      result,
      timestamp: new Date(),
      success: result.success
    });

    this.currentApproach = signature;
  }

  generateSignature(approach) {
    // Create unique identifier for approach
    return {
      method: approach.method,           // e.g., "npm install"
      target: approach.target,           // e.g., "package-name"
      parameters: approach.parameters,   // e.g., ["--save"]
      errorType: approach.errorType      // e.g., "NetworkTimeout"
    };
  }

  getAttemptCount(signature) {
    return this.attempts.filter(a =>
      this.signaturesMatch(a.signature, signature)
    ).length;
  }

  signaturesMatch(sig1, sig2) {
    return (
      sig1.method === sig2.method &&
      sig1.target === sig2.target &&
      sig1.errorType === sig2.errorType
    );
  }
}
```

**Example:**
```javascript
// Attempt 1
monitor.recordAttempt({
  method: "npm install",
  target: "react",
  parameters: [],
  errorType: "NetworkTimeout"
}, {success: false, error: "ETIMEDOUT"});

// Attempt 2 (same approach)
monitor.recordAttempt({
  method: "npm install",
  target: "react",
  parameters: [],
  errorType: "NetworkTimeout"
}, {success: false, error: "ETIMEDOUT"});

// Attempt 3 (same approach again)
monitor.recordAttempt({
  method: "npm install",
  target: "react",
  parameters: [],
  errorType: "NetworkTimeout"
}, {success: false, error: "ETIMEDOUT"});

// PIVOT TRIGGERED
```

### 2. Detect Infinite Loop

```javascript
function shouldPivot(monitor, thresholds = {maxAttempts: 3}) {
  const recentAttempts = monitor.attempts.slice(-10);
  const currentSignature = monitor.currentApproach;

  // Count failures with current approach
  const sameApproachFailures = recentAttempts.filter(a =>
    monitor.signaturesMatch(a.signature, currentSignature) &&
    !a.success
  );

  if (sameApproachFailures.length >= thresholds.maxAttempts) {
    return {
      shouldPivot: true,
      reason: `Same approach failed ${sameApproachFailures.length} times`,
      failedApproach: currentSignature,
      attempts: sameApproachFailures
    };
  }

  // Check for time-based loop (no progress in N minutes)
  const timeStuck = Date.now() - recentAttempts[0].timestamp;
  if (timeStuck > thresholds.maxTimeStuck * 60 * 1000) {
    return {
      shouldPivot: true,
      reason: `No progress for ${timeStuck / 60000} minutes`,
      failedApproach: currentSignature,
      timeStuck
    };
  }

  return {shouldPivot: false};
}
```

### 3. Generate Alternative Strategies

```javascript
async function generateAlternatives(failedApproach, context) {
  const alternatives = [];

  // Strategy 1: Different method for same goal
  if (failedApproach.method === "npm install") {
    alternatives.push({
      strategy: "Use yarn instead of npm",
      method: "yarn add",
      target: failedApproach.target,
      rationale: "Different package manager may succeed",
      estimatedEffort: "low"
    });

    alternatives.push({
      strategy: "Download from registry manually",
      method: "curl",
      target: `https://registry.npmjs.org/${failedApproach.target}`,
      rationale: "Bypass npm CLI issues",
      estimatedEffort: "medium"
    });

    alternatives.push({
      strategy: "Use cached package",
      method: "check ~/.npm cache",
      target: failedApproach.target,
      rationale: "Package may already be cached locally",
      estimatedEffort: "low"
    });
  }

  // Strategy 2: Check pattern library for known solutions
  const patterns = await patternLibrary.findSolutions({
    errorType: failedApproach.errorType,
    operation: failedApproach.method
  });

  if (patterns.length > 0) {
    patterns.forEach(pattern => {
      alternatives.push({
        strategy: `Apply pattern: ${pattern.name}`,
        method: pattern.solution.method,
        rationale: `Proven solution (${pattern.metrics.successRate * 100}% success rate)`,
        estimatedEffort: pattern.solution.effort,
        fromPattern: true
      });
    });
  }

  // Strategy 3: Escalation path
  alternatives.push({
    strategy: "Escalate to user",
    method: "request user intervention",
    rationale: "Cannot resolve automatically",
    estimatedEffort: "N/A",
    escalation: true
  });

  return alternatives;
}
```

**Example Output:**
```
⚠️ PIVOT TRIGGERED

Failed Approach:
  Method: npm install react
  Error: Network timeout (ETIMEDOUT)
  Attempts: 3 failures in a row
  Time wasted: 8 minutes

Alternative Strategies:

1. Use yarn instead of npm [RECOMMENDED]
   Rationale: Different package manager may bypass npm network issues
   Estimated effort: Low (1 min)
   Command: yarn add react

2. Check npm cache
   Rationale: Package may already be cached locally
   Estimated effort: Low (< 1 min)
   Command: ls ~/.npm/_cacache | grep react

3. Download from registry manually
   Rationale: Bypass npm CLI entirely
   Estimated effort: Medium (5 min)
   Command: curl https://registry.npmjs.org/react/latest

4. Apply pattern: network-timeout-recovery
   Rationale: Proven solution (85% success rate, used 12x)
   Estimated effort: Low
   From: Pattern library

5. Escalate to user
   Rationale: Cannot resolve automatically
   Message: "npm install failing due to network issues - manual intervention needed"

Pivoting to strategy #1: Use yarn instead of npm
```

### 4. Execute Pivot

```javascript
async function executePivot(failedApproach, alternatives) {
  console.log("⚠️ PIVOT TRIGGERED");
  console.log(`Failed approach: ${failedApproach.method}`);
  console.log(`Attempts: ${failedApproach.attempts.length}`);

  // Select best alternative
  const recommended = alternatives.filter(a => !a.escalation)[0];

  if (!recommended) {
    // No alternatives - escalate
    console.log("🔴 ESCALATION: No automatic alternatives available");
    await escalateToUser({
      problem: failedApproach,
      attemptsMade: failedApproach.attempts,
      needsIntervention: true
    });
    throw new Error("Cannot proceed - user intervention required");
  }

  console.log(`\nPivoting to: ${recommended.strategy}`);
  console.log(`Rationale: ${recommended.rationale}`);

  // Execute alternative
  const result = await executeApproach(recommended);

  if (result.success) {
    console.log("✓ Pivot successful!");

    // Save as pattern if novel solution
    if (!recommended.fromPattern) {
      await patternLibrary.savePattern({
        problem: failedApproach.errorType,
        failedApproach: failedApproach.method,
        solution: recommended.method,
        successfulPivot: true
      });
    }

    return result;
  } else {
    // Alternative also failed - try next
    console.log(`✗ Alternative #1 failed, trying #2...`);
    return await executePivot(failedApproach, alternatives.slice(1));
  }
}
```

### 5. Track Pivot Effectiveness

```javascript
async function trackPivot(failedApproach, alternative, result) {
  const pivotRecord = {
    timestamp: new Date(),
    failedApproach: {
      method: failedApproach.method,
      attempts: failedApproach.attempts.length,
      timeWasted: calculateTimeWasted(failedApproach.attempts)
    },
    alternative: {
      strategy: alternative.strategy,
      method: alternative.method
    },
    result: {
      success: result.success,
      timeSaved: estimateTimeSaved(failedApproach, alternative)
    }
  };

  await savePivotRecord(pivotRecord);

  // Update metrics
  await updateMetrics({
    pivotsTriggered: 1,
    timeSaved: pivotRecord.result.timeSaved,
    successRate: result.success ? 1 : 0
  });
}
```

---

## Integration with Battle-Plan

**Position:** During Execution (Phase 5) - Continuous Monitoring

**Flow:**
```
Execute Task:
├─ Try approach A
│  └─ Fail (attempt 1)
├─ Try approach A again
│  └─ Fail (attempt 2)
├─ Try approach A again
│  └─ Fail (attempt 3)
│
├─ [DETECT-INFINITE-LOOP triggered]
│  ├─ Generate alternatives
│  ├─ Select best alternative (B)
│  └─ Pivot to approach B
│
├─ Try approach B
│  └─ Success ✓
│
└─ Complete
```

**Integration Points:**
- After each failure
- Before retrying same approach
- When time stuck exceeds threshold
- In convergence engine GATE

---

## Common Infinite Loop Patterns

### Pattern 1: Network Failures

```
Symptom: Repeated network timeouts
Failed approach: Direct API call
Alternatives:
1. Use cached data
2. Try alternative endpoint
3. Implement exponential backoff
4. Check for firewall/proxy issues
```

### Pattern 2: Compilation Errors

```
Symptom: Same compilation error 3+ times
Failed approach: Fix syntax without understanding root cause
Alternatives:
1. Check for missing dependencies
2. Verify TypeScript/Babel configuration
3. Look for conflicting versions
4. Consult error pattern library
```

### Pattern 3: Test Failures

```
Symptom: Same test failing repeatedly
Failed approach: Modify code blindly
Alternatives:
1. Read test carefully to understand expectation
2. Debug test in isolation
3. Check test fixtures/mocks
4. Verify test environment
```

### Pattern 4: Convergence Not Achieved

```
Symptom: GATE never reaches 3 clean passes
Failed approach: Keep running same fixes
Alternatives:
1. Analyze which issues keep reappearing
2. Fix root cause instead of symptoms
3. Disable problematic audit temporarily
4. Escalate to user
```

---

## Configuration

```json
{
  "detectInfiniteLoop": {
    "enabled": true,
    "thresholds": {
      "maxAttempts": 3,         // Pivot after 3 failures
      "maxTimeStuck": 10,        // Pivot after 10 min no progress
      "maxTotalAttempts": 10     // Escalate after 10 total attempts
    },
    "monitoring": {
      "trackApproaches": true,
      "logAttempts": true,
      "alertOnPivot": true
    },
    "alternatives": {
      "checkPatternLibrary": true,
      "generateN": 3,            // Generate 3 alternatives
      "autoSelect": true,        // Auto-select best alternative
      "requireUserConfirm": false // Don't require confirmation
    },
    "escalation": {
      "afterFailedAlternatives": 3,
      "notifyUser": true,
      "includeAttemptLog": true
    }
  }
}
```

---

## Quick Reference

**Monitor and pivot:**
```javascript
const monitor = new ApproachMonitor();

async function tryWithPivot(task, approach) {
  while (true) {
    const result = await tryApproach(task, approach);

    monitor.recordAttempt(approach, result);

    if (result.success) {
      return result;
    }

    // Check if should pivot
    const pivotDecision = shouldPivot(monitor);

    if (pivotDecision.shouldPivot) {
      const alternatives = await generateAlternatives(approach);
      approach = await executePivot(approach, alternatives);
    }
  }
}
```

**Check if stuck:**
```javascript
if (monitor.getAttemptCount(currentApproach) >= 3) {
  console.log("⚠️ Same approach failing repeatedly - pivot needed");
  await pivot();
}
```

---

## Pivot Decision Tree

```
Attempt fails
    ↓
Is this approach new?
    ├─ YES → Try again (1 retry allowed)
    └─ NO → Count previous attempts
        ↓
        Previous attempts >= 3?
            ├─ YES → PIVOT
            │   ├─ Generate alternatives
            │   ├─ Check pattern library
            │   ├─ Select best alternative
            │   └─ Execute
            │
            └─ NO → Try again
                ↓
                Still failing after 10 total attempts?
                    ├─ YES → ESCALATE
                    └─ NO → Continue
```

---

## Metrics Tracked

**Pivot Effectiveness:**
- Pivots triggered
- Successful pivots (solved problem)
- Failed pivots (alternative also failed)
- Average attempts before pivot
- Time saved by pivoting
- Time wasted before pivot

**Pattern Detection:**
- Most common failed approaches
- Most successful alternative strategies
- Error patterns that trigger pivots
- Success rate by alternative type

---

## Benefits

**Prevents:**
- Infinite retry loops
- Wasted time on dead ends
- Burning through API quotas
- User frustration

**Provides:**
- Automatic strategy change
- Alternative generation
- Pattern-based solutions
- Escalation path

**Enables:**
- Adaptive problem solving
- Creative alternatives
- Efficient failure handling
- Learning from failed approaches

---

*End of Detect-Infinite-Loop*
*Part of v4.0.0 Universal Skills Ecosystem*
*Category: Learning / During-Execution (Strategy Management)*
*Attribution: Based on "pivot" skill from Claude Skill Potions by Elliot*
*"The wall won't move - try a different door"*
