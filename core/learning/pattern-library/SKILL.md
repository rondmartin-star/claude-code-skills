---
name: pattern-library
description: >
  Maintain and apply learned patterns and antipatterns. Stores successful solutions
  and known failure modes, then retrieves and applies them automatically to similar
  tasks. Use when: starting new tasks, after discovering patterns, building on past work.
---

# Pattern Library

**Purpose:** Build institutional memory through reusable patterns
**Type:** Learning Skill (Knowledge Repository)

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Check for similar patterns"
- "Have we solved this before?"
- "Apply proven solutions"
- Before starting implementation

**Context Indicators:**
- Beginning a new task
- Encountering a familiar problem
- After successfully solving a problem
- After discovering an antipattern

---

## Core Concept

**Traditional Approach:** Each task solved from scratch, knowledge lost between sessions
**Pattern Library:** Capture solutions and failures, retrieve automatically, compound learning over time

**Why It Matters:**
- Prevents reinventing solutions
- Avoids repeating mistakes
- Accelerates development
- Creates searchable knowledge base

**Article Quote:** *"failure paths save more time than success paths"*

---

## Pattern Library Architecture

### Storage Structure

```
.corpus/learning/
├── patterns/
│   ├── index.json
│   ├── authentication/
│   │   ├── oauth-token-caching.md
│   │   ├── session-management.md
│   │   └── rate-limit-handling.md
│   ├── database/
│   │   ├── connection-pooling.md
│   │   ├── query-optimization.md
│   │   └── transaction-patterns.md
│   └── api/
│       ├── error-handling.md
│       ├── pagination.md
│       └── versioning.md
├── antipatterns/
│   ├── index.json
│   ├── authentication/
│   │   ├── no-token-caching.md
│   │   ├── weak-session-validation.md
│   │   └── tight-polling.md
│   ├── database/
│   │   ├── n-plus-one-queries.md
│   │   ├── missing-indexes.md
│   │   └── connection-leaks.md
│   └── api/
│       ├── missing-error-handling.md
│       ├── unbounded-results.md
│       └── breaking-changes.md
└── metrics/
    └── pattern-effectiveness.json
```

### Pattern Schema

```json
{
  "pattern": {
    "name": "oauth-token-caching",
    "type": "pattern",
    "category": "authentication",
    "subcategories": ["oauth", "performance", "third-party"],
    "context": "Third-party OAuth provider with rate limits",
    "problem": "Frequent OAuth token requests hitting rate limits",
    "solution": {
      "approach": "Implement caching layer with token refresh",
      "implementation": "Redis cache with expiration matching token TTL",
      "code": "...",
      "benefits": [
        "Reduces API calls by 95%",
        "Eliminates rate limit errors",
        "Improves auth response time"
      ],
      "tradeoffs": [
        "Requires Redis infrastructure",
        "Adds complexity to token management",
        "Must handle cache invalidation"
      ]
    },
    "metrics": {
      "proven": true,
      "timesApplied": 5,
      "successRate": 1.0,
      "averageTimeToImplement": "2 hours",
      "errorReductionRate": 0.95
    },
    "relatedPatterns": ["exponential-backoff", "circuit-breaker"],
    "relatedAntipatterns": ["no-caching", "tight-polling"],
    "tags": ["oauth", "rate-limiting", "caching", "third-party"],
    "firstUsed": "2026-01-15T10:00:00Z",
    "lastUsed": "2026-02-04T14:30:00Z",
    "updatedAt": "2026-02-04T14:30:00Z"
  }
}
```

### Antipattern Schema

```json
{
  "antipattern": {
    "name": "no-oauth-token-caching",
    "type": "antipattern",
    "category": "authentication",
    "subcategories": ["oauth", "performance"],
    "context": "OAuth integration without caching",
    "problem": "Making OAuth token requests on every user action",
    "symptoms": [
      "429 Too Many Requests errors",
      "Slow authentication response times",
      "Intermittent auth failures",
      "High OAuth API costs"
    ],
    "consequences": {
      "severity": "high",
      "userImpact": "Cannot authenticate during rate limits",
      "businessImpact": "Service unavailable, revenue loss",
      "technicalDebt": "Requires emergency hotfix"
    },
    "detection": {
      "metrics": [
        "OAuth requests per minute > threshold",
        "429 response rate > 1%",
        "Auth latency > 500ms"
      ],
      "code": [
        "No cache lookup before OAuth call",
        "Token stored only in request context",
        "Missing TTL management"
      ]
    },
    "prevention": {
      "rule": "Always cache OAuth tokens with proper expiration",
      "implementation": "Use pattern: oauth-token-caching",
      "validation": "Monitor OAuth request rate in staging",
      "testing": "Load test with realistic user concurrency"
    },
    "fix": {
      "immediate": "Add emergency rate limiting",
      "proper": "Implement oauth-token-caching pattern",
      "estimatedEffort": "4 hours",
      "priority": "critical"
    },
    "metrics": {
      "occurrences": 2,
      "preventedBy": "pre-mortem",
      "detectedBy": "error-reflection",
      "fixSuccessRate": 1.0
    },
    "relatedPatterns": ["oauth-token-caching"],
    "tags": ["oauth", "rate-limiting", "performance", "critical"],
    "firstSeen": "2026-01-15T10:00:00Z",
    "lastSeen": "2026-01-20T14:00:00Z",
    "updatedAt": "2026-01-20T14:30:00Z"
  }
}
```

---

## Pattern Lifecycle

### 1. Pattern Discovery

```javascript
async function discoverPattern(task, solution, outcome) {
  // Determine if this is novel or variation
  const similar = await findSimilarPatterns(task);

  if (similar.length === 0) {
    // Novel pattern
    return await createNewPattern(task, solution, outcome);
  } else {
    // Variation of existing pattern
    return await updateExistingPattern(similar[0], solution, outcome);
  }
}

async function createNewPattern(task, solution, outcome) {
  const pattern = {
    name: generatePatternName(task, solution),
    type: outcome.success ? 'pattern' : 'antipattern',
    category: categorizeTask(task),
    context: task.context,
    problem: task.problem,
    solution: outcome.success ? solution : null,
    symptoms: outcome.success ? null : outcome.errors,
    metrics: {
      proven: outcome.success,
      timesApplied: 1,
      successRate: outcome.success ? 1.0 : 0.0
    },
    tags: extractTags(task, solution),
    firstUsed: new Date().toISOString(),
    lastUsed: new Date().toISOString()
  };

  await savePattern(pattern);
  return pattern;
}
```

### 2. Pattern Retrieval

```javascript
async function findRelevantPatterns(task) {
  const candidates = [];

  // 1. Exact category match
  const categoryMatches = await queryByCategory(task.category);
  candidates.push(...categoryMatches);

  // 2. Tag similarity
  const tagMatches = await queryByTags(task.tags);
  candidates.push(...tagMatches);

  // 3. Semantic similarity
  const semanticMatches = await queryByDescription(task.description);
  candidates.push(...semanticMatches);

  // 4. Score and rank
  const scored = candidates.map(pattern => ({
    pattern,
    score: calculateRelevanceScore(pattern, task)
  }));

  // 5. Filter by confidence threshold
  const confident = scored.filter(s => s.score >= 0.7);

  // 6. Sort by score and metrics
  return confident.sort((a, b) => {
    // Prioritize high success rate and recent usage
    const scoreA = a.score * a.pattern.metrics.successRate;
    const scoreB = b.score * b.pattern.metrics.successRate;
    return scoreB - scoreA;
  });
}

function calculateRelevanceScore(pattern, task) {
  let score = 0;

  // Category match (40%)
  if (pattern.category === task.category) {
    score += 0.4;
  }

  // Tag overlap (30%)
  const tagOverlap = intersection(pattern.tags, task.tags);
  const tagSimilarity = tagOverlap.length / union(pattern.tags, task.tags).length;
  score += tagSimilarity * 0.3;

  // Context similarity (20%)
  const contextSimilarity = calculateTextSimilarity(pattern.context, task.context);
  score += contextSimilarity * 0.2;

  // Problem similarity (10%)
  const problemSimilarity = calculateTextSimilarity(pattern.problem, task.problem);
  score += problemSimilarity * 0.1;

  return score;
}
```

### 3. Pattern Application

```javascript
async function applyPattern(pattern, task) {
  console.log(`Applying pattern: ${pattern.name}`);
  console.log(`Success rate: ${pattern.metrics.successRate * 100}%`);
  console.log(`Times applied: ${pattern.metrics.timesApplied}`);

  const application = {
    patternName: pattern.name,
    taskId: task.id,
    startTime: new Date().toISOString(),
    approach: pattern.solution.approach,
    implementation: pattern.solution.implementation,
    expectedBenefits: pattern.solution.benefits,
    potentialTradeoffs: pattern.solution.tradeoffs
  };

  // Apply the pattern
  const result = await implementSolution(
    task,
    pattern.solution.implementation
  );

  // Track outcome
  application.endTime = new Date().toISOString();
  application.success = result.success;
  application.actualBenefits = result.benefits;
  application.issues = result.issues;

  // Update pattern metrics
  await updatePatternMetrics(pattern, application);

  return application;
}

async function updatePatternMetrics(pattern, application) {
  pattern.metrics.timesApplied++;
  pattern.metrics.lastUsed = application.endTime;

  if (application.success) {
    // Update success rate
    const totalSuccess = pattern.metrics.successRate * (pattern.metrics.timesApplied - 1) + 1;
    pattern.metrics.successRate = totalSuccess / pattern.metrics.timesApplied;
  } else {
    // Pattern failed - recalculate
    const totalSuccess = pattern.metrics.successRate * (pattern.metrics.timesApplied - 1);
    pattern.metrics.successRate = totalSuccess / pattern.metrics.timesApplied;

    // If success rate drops below threshold, mark as questionable
    if (pattern.metrics.successRate < 0.5) {
      pattern.metrics.proven = false;
      pattern.metrics.needsReview = true;
    }
  }

  await savePattern(pattern);
}
```

### 4. Pattern Evolution

```javascript
async function evolvePattern(pattern, newLearnings) {
  // Accumulate variations and improvements
  if (newLearnings.betterApproach) {
    pattern.solution.variations = pattern.solution.variations || [];
    pattern.solution.variations.push({
      approach: newLearnings.betterApproach,
      improvement: newLearnings.improvement,
      addedAt: new Date().toISOString()
    });
  }

  // Update benefits based on real outcomes
  if (newLearnings.actualBenefits) {
    pattern.solution.actualBenefits = pattern.solution.actualBenefits || [];
    pattern.solution.actualBenefits.push(newLearnings.actualBenefits);
  }

  // Discover new tradeoffs
  if (newLearnings.newTradeoff) {
    pattern.solution.tradeoffs.push(newLearnings.newTradeoff);
  }

  // Identify edge cases
  if (newLearnings.edgeCase) {
    pattern.edgeCases = pattern.edgeCases || [];
    pattern.edgeCases.push({
      case: newLearnings.edgeCase,
      solution: newLearnings.edgeCaseSolution,
      discoveredAt: new Date().toISOString()
    });
  }

  pattern.updatedAt = new Date().toISOString();
  await savePattern(pattern);
}
```

---

## Integration with Workflow

### Before Starting Tasks

```javascript
async function executeTaskWithPatternLibrary(task) {
  // 1. Find relevant patterns
  console.log("Searching pattern library...");
  const relevantPatterns = await findRelevantPatterns(task);

  if (relevantPatterns.length > 0) {
    console.log(`Found ${relevantPatterns.length} relevant patterns`);

    // 2. Check for antipatterns
    const antipatterns = relevantPatterns.filter(p => p.pattern.type === 'antipattern');
    if (antipatterns.length > 0) {
      console.log("⚠️ Warning: Known antipatterns detected");
      antipatterns.forEach(ap => {
        console.log(`  - ${ap.pattern.name}: ${ap.pattern.problem}`);
        console.log(`    Prevention: ${ap.pattern.prevention.rule}`);
      });
    }

    // 3. Apply proven patterns
    const provenPatterns = relevantPatterns.filter(
      p => p.pattern.type === 'pattern' &&
           p.pattern.metrics.proven &&
           p.pattern.metrics.successRate >= 0.8
    );

    if (provenPatterns.length > 0) {
      console.log("✓ Applying proven patterns:");
      for (const pp of provenPatterns) {
        console.log(`  - ${pp.pattern.name} (${pp.pattern.metrics.successRate * 100}% success rate)`);
        await applyPattern(pp.pattern, task);
      }
    }

    // 4. Suggest medium-confidence patterns
    const suggestedPatterns = relevantPatterns.filter(
      p => p.pattern.type === 'pattern' &&
           p.pattern.metrics.successRate >= 0.5 &&
           p.pattern.metrics.successRate < 0.8
    );

    if (suggestedPatterns.length > 0) {
      console.log("💡 Suggested patterns (user approval needed):");
      suggestedPatterns.forEach(sp => {
        console.log(`  - ${sp.pattern.name} (${sp.pattern.metrics.successRate * 100}% success rate)`);
      });
    }
  } else {
    console.log("No existing patterns found - creating new solution");
  }

  // 5. Execute task
  const result = await executeTask(task);

  // 6. If successful and novel, save as pattern
  if (result.success && result.novel) {
    console.log("✓ Success! Saving as new pattern...");
    await discoverPattern(task, result.solution, result);
  }

  return result;
}
```

### Failed Attempts Section

**From Article:** *"Every skill in my collection includes a 'Failed Attempts' section — documentation of approaches that didn't work. This gets read more than any other section, because failure paths save more time than success paths."*

```markdown
## Failed Attempts

### oauth-no-expiration-tracking
**Problem:** Cached tokens without tracking expiration
**What Went Wrong:** Tokens expired in cache, caused auth failures
**Why It Failed:** Assumed OAuth provider would reject expired tokens (it didn't)
**Lesson:** Always track token expiration explicitly
**Fixed By:** Adding TTL to cache entries matching token exp claim

### oauth-aggressive-refresh
**Problem:** Refreshing tokens on every request "to be safe"
**What Went Wrong:** Hit rate limits on refresh endpoint
**Why It Failed:** Misunderstanding of refresh token purpose
**Lesson:** Only refresh when token is expired or near expiration
**Fixed By:** Implementing refresh-on-expiry pattern with 5-min buffer
```

---

## Self-Improving CLAUDE.md Pattern

**From Article:**
```
Reflect on what went wrong
→ Abstract the general pattern
→ Generalize into a reusable decision framework
→ Write it to CLAUDE.md
```

```javascript
async function reflectAndUpdateCLAUDE(error, fix) {
  const reflection = {
    // 1. What went wrong
    error: {
      description: error.message,
      context: error.context,
      rootCause: error.rootCause
    },

    // 2. Abstract the pattern
    pattern: {
      generalProblem: abstractProblem(error),
      conditions: identifyConditions(error),
      symptoms: extractSymptoms(error)
    },

    // 3. Generalize into framework
    framework: {
      rule: generateDecisionRule(error, fix),
      trigger: identifyTrigger(error),
      prevention: createPreventionRule(fix),
      validation: createValidationRule(fix)
    }
  };

  // 4. Update CLAUDE.md
  await appendToCLAUDE(reflection);

  // 5. Create antipattern in library
  await createAntipattern(reflection);

  // 6. Update pre-mortem risk database
  await updatePreMortemRisks(reflection);
}
```

---

## Query Operations

```javascript
// Query patterns by category
const authPatterns = await queryPatterns({ category: 'authentication' });

// Query patterns by tags
const rateLimit = await queryPatterns({ tags: ['rate-limiting', 'oauth'] });

// Query by success rate
const proven = await queryPatterns({
  successRate: { $gte: 0.8 },
  timesApplied: { $gte: 3 }
});

// Full-text search
const results = await searchPatterns("token caching oauth");

// Find antipatterns for a category
const authAntipatterns = await queryAntipatterns({ category: 'authentication' });

// Get pattern with relationships
const pattern = await getPatternWithRelated('oauth-token-caching');
// Returns: pattern + related patterns + related antipatterns
```

---

## Metrics and Effectiveness

```javascript
async function calculatePatternLibraryMetrics() {
  const metrics = {
    library: {
      totalPatterns: await countPatterns(),
      totalAntipatterns: await countAntipatterns(),
      categories: await countByCategory(),
      provenPatterns: await countProven(),
      questionablePatterns: await countQuestionable()
    },
    usage: {
      patternsAppliedThisWeek: await countRecentApplications(7),
      averageSuccessRate: await calculateAverageSuccessRate(),
      mostUsedPatterns: await getTopPatterns(10),
      highestImpactPatterns: await getHighestImpact(10)
    },
    impact: {
      errorsPreventedByAntipatterns: await countPreventedErrors(),
      timesSavedByPatterns: await calculateTimeSaved(),
      repeatErrorReduction: await calculateRepeatErrorReduction(),
      implementationAcceleration: await calculateSpeedup()
    }
  };

  await saveMetrics(metrics);
  return metrics;
}
```

---

## Quick Reference

**Find patterns before starting:**
```javascript
const patterns = await findRelevantPatterns({
  category: 'authentication',
  tags: ['oauth', 'third-party'],
  description: 'Implement OAuth login'
});
```

**Check for antipatterns:**
```javascript
const antipatterns = await queryAntipatterns({
  category: 'authentication'
});
console.log("Watch out for:", antipatterns.map(ap => ap.name));
```

**Save successful solution:**
```javascript
await discoverPattern(task, solution, {
  success: true,
  novel: true,
  benefits: ['Fast', 'Reliable', 'Maintainable']
});
```

---

*End of Pattern Library*
*Part of v4.0.0 Universal Skills Ecosystem*
*Category: Learning (Knowledge Repository)*
*"Failure paths save more time than success paths" - Elliot*
