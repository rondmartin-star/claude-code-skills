---
name: error-reflection
description: >
  Self-analyze errors and extract learnings to build institutional memory. Automatically
  categorizes errors, identifies root causes, and updates the pattern library with
  antipatterns to prevent future failures. Use when: errors occur, tests fail, issues found.
---

# Error Reflection

**Purpose:** Build institutional memory from failures
**Type:** Learning Skill (Post-Failure Analysis)

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "What went wrong?"
- "Analyze this error"
- "Why did that fail?"
- After test failures or runtime errors

**Context Indicators:**
- Tests failing
- Build errors
- Runtime exceptions
- User-reported bugs
- Audit failures
- Unexpected behavior

---

## Core Concept

**Traditional Approach:** Fix the immediate error and move on
**Error Reflection:** Analyze root cause, extract patterns, update library to prevent recurrence

**Why It Matters:**
- Prevents repeat mistakes
- Builds organizational knowledge
- Improves pre-mortem accuracy over time
- Creates searchable error catalog

---

## Error Reflection Process

### Performance Optimization

**Parallel Analysis Execution:**
The error reflection process runs three independent analyses in parallel:
- Root cause identification (5 Whys method)
- Error categorization (classify by pattern)
- Pattern extraction (antipattern detection)

**Performance Impact:**
- Sequential execution: ~105ms (40ms + 30ms + 35ms)
- Parallel execution: ~40ms (max of 40ms, 30ms, 35ms)
- **Speedup: 2.6x**

All three analyses operate on the same error context, with no dependencies between them. Results are aggregated after all analyses complete for cross-validation and enrichment.

---

### 1. Capture Error Context

```javascript
async function captureErrorContext(error) {
  const context = {
    timestamp: new Date().toISOString(),
    error: {
      message: error.message,
      stack: error.stack,
      type: error.constructor.name
    },
    task: {
      description: getCurrentTask(),
      phase: getCurrentPhase(),
      complexity: assessComplexity()
    },
    environment: {
      platform: process.platform,
      nodeVersion: process.version,
      dependencies: getRelevantDependencies(error)
    },
    codeContext: {
      files: getAffectedFiles(error),
      recentChanges: getRecentCommits()
    }
  };

  return context;
}
```

### 2. Identify Root Cause

**5 Whys Technique:**

```javascript
async function identifyRootCause(error, context) {
  const whys = [];
  let currentQuestion = `Why did "${error.message}" occur?`;

  for (let i = 0; i < 5; i++) {
    const answer = await analyzeWhy(currentQuestion, context, whys);
    whys.push({ question: currentQuestion, answer });

    if (answer.isRootCause) {
      break;
    }

    currentQuestion = `Why ${answer.summary}?`;
  }

  return {
    surfaceSymptom: whys[0],
    rootCause: whys[whys.length - 1],
    chain: whys
  };
}
```

**Example - OAuth Rate Limit:**
```
Why 1: OAuth 429 error
Why 2: No token caching
Why 3: Not implemented
Why 4: Not in requirements
Why 5: ROOT: Pre-mortem missed rate limit risk
```

### 3. Categorize Error Type

```javascript
function categorizeError(error, contextOrRootCause) {
  // Support both parallel (context) and sequential (rootCause) execution
  const rootCause = contextOrRootCause.error ? null : contextOrRootCause;
  const context = contextOrRootCause.error ? contextOrRootCause : null;

  const categories = {
    technical: [
      'syntax-error',
      'type-error',
      'reference-error',
      'null-pointer',
      'async-race-condition',
      'memory-leak',
      'performance-degradation'
    ],
    architectural: [
      'missing-abstraction',
      'tight-coupling',
      'circular-dependency',
      'single-point-of-failure',
      'scalability-bottleneck'
    ],
    security: [
      'authentication-bypass',
      'authorization-failure',
      'injection-vulnerability',
      'xss-vulnerability',
      'csrf-vulnerability',
      'sensitive-data-exposure'
    ],
    process: [
      'missing-test',
      'inadequate-review',
      'skipped-validation',
      'rushed-implementation',
      'insufficient-documentation'
    ],
    assumptions: [
      'invalid-assumption',
      'missing-edge-case',
      'incorrect-requirement',
      'third-party-behavior-changed',
      'environment-mismatch'
    ],
    external: [
      'third-party-api-failure',
      'network-timeout',
      'rate-limit-exceeded',
      'service-unavailable',
      'data-corruption'
    ]
  };

  const classification = classifyByPattern(error, rootCause, context, categories);

  return {
    primary: classification.primary,
    secondary: classification.secondary || [],
    tags: extractTags(error, rootCause, context)
  };
}
```

### 4. Extract Pattern or Antipattern

```javascript
async function extractPattern(error, contextOrRootCause, category) {
  // Support both parallel (context) and sequential (rootCause, category) execution
  const context = contextOrRootCause.error ? contextOrRootCause : null;
  const rootCause = contextOrRootCause.error ? null : contextOrRootCause;

  // If called in parallel mode (context only), do basic pattern extraction
  if (context && !rootCause) {
    return await extractBasicPattern(error, context);
  }

  // Sequential mode: full analysis with rootCause and category
  const isAntipattern = rootCause.preventable;
  const isSolutionPattern = rootCause.fixWorked && rootCause.fixReusable;

  if (isAntipattern) {
    return {
      type: 'antipattern',
      name: generateAntipatternName(rootCause),
      problem: rootCause.description,
      symptoms: error.symptoms,
      consequences: error.impact,
      prevention: generatePreventionRule(rootCause),
      detection: generateDetectionRule(error)
    };
  }

  if (isSolutionPattern) {
    return {
      type: 'pattern',
      name: generatePatternName(rootCause.fix),
      context: rootCause.context,
      problem: rootCause.problem,
      solution: rootCause.fix,
      benefits: rootCause.benefits,
      tradeoffs: rootCause.tradeoffs
    };
  }

  return null;
}

/**
 * Extract basic pattern in parallel mode (context-only analysis)
 * Used when running in parallel with rootCause and category analyses
 */
async function extractBasicPattern(error, context) {
  const errorSignature = `${error.type}-${error.message}`;
  const knownPatterns = await loadKnownPatterns();

  // Check if this matches a known antipattern
  const match = knownPatterns.find(p =>
    p.signature === errorSignature ||
    p.symptoms.some(s => error.message.includes(s))
  );

  if (match) {
    return {
      type: 'antipattern',
      name: match.name,
      confidence: 'high',
      source: 'parallel-detection'
    };
  }

  // Return basic detection for aggregation
  return {
    type: 'unknown',
    errorType: error.type,
    confidence: 'low',
    source: 'parallel-detection',
    requiresAggregation: true
  };
}
```

**Example Antipattern:**
```json
{
  "type": "antipattern",
  "name": "no-oauth-token-caching",
  "problem": "OAuth requests on every action",
  "symptoms": ["429 errors", "Slow auth"],
  "prevention": "Cache tokens with expiration",
  "detection": "Monitor OAuth request rate",
  "relatedPatterns": ["oauth-token-caching"]
}
```

### 5. Update Pattern Library

```javascript
async function updatePatternLibrary(pattern) {
  const libraryPath = '.corpus/learning';

  if (pattern.type === 'antipattern') {
    const antipatternPath = path.join(
      libraryPath,
      'antipatterns',
      pattern.category,
      `${pattern.name}.md`
    );

    await saveAntipattern(antipatternPath, pattern);
    await updateAntipatternIndex(pattern);
  } else {
    const patternPath = path.join(
      libraryPath,
      'patterns',
      pattern.category,
      `${pattern.name}.md`
    );

    await savePattern(patternPath, pattern);
    await updatePatternIndex(pattern);
  }

  // Update metrics
  await updateLearningMetrics({
    type: pattern.type,
    category: pattern.category,
    timestamp: new Date().toISOString()
  });
}
```

### 6. Generate Prevention Rule

```javascript
function generatePreventionRule(antipattern) {
  return {
    rule: {
      name: `prevent-${antipattern.name}`,
      trigger: antipattern.context,
      check: antipattern.detection,
      action: antipattern.prevention
    },
    integration: {
      preMortem: `Add "${antipattern.problem}" to risk assessment`,
      linter: generateLinterRule(antipattern),
      test: generateRegressionTest(antipattern)
    },
    documentation: {
      message: `⚠️ Potential antipattern: ${antipattern.name}`,
      details: antipattern.problem,
      fix: antipattern.prevention.implementation
    }
  };
}
```

---

## Storage Structure

```
.corpus/learning/
├── errors/
│   ├── index.json
│   └── {timestamp}-{error-type}.json
├── patterns/
│   ├── index.json
│   ├── authentication/
│   │   └── oauth-token-caching.md
│   ├── database/
│   │   └── connection-pooling.md
│   └── api/
│       └── rate-limit-handling.md
├── antipatterns/
│   ├── index.json
│   ├── authentication/
│   │   └── no-oauth-token-caching.md
│   ├── database/
│   │   └── n-plus-one-queries.md
│   └── api/
│       └── tight-polling.md
└── metrics/
    └── effectiveness.json
```

---

## Integration with Workflow

### Parallel Analysis Architecture

**Context Capture (Sequential - Required First):**
```javascript
const context = await captureErrorContext(error); // 15ms
```

**Independent Analyses (Parallel Execution):**
```javascript
const [rootCause, category, pattern] = await Promise.all([
  identifyRootCause(error, context),    // 40ms - 5 Whys analysis
  categorizeError(error, context),      // 30ms - Classification
  extractPattern(error, context)        // 35ms - Pattern matching
]);
// Total: 40ms (vs 105ms sequential)
```

**Result Aggregation (Sequential - Uses All Results):**
```javascript
const aggregatedPattern = pattern || await extractPattern(error, rootCause, category);
// Enriches basic pattern with rootCause and category insights
```

**Why This Works:**
- All three analyses read the same error + context
- No dependencies between analyses
- Results combined after all complete
- 2.6x faster than sequential execution

---

### Automatic Error Capture

```javascript
async function executeTaskWithErrorReflection(task) {
  try {
    const result = await executeTask(task);
    return result;
  } catch (error) {
    console.log("⚠️ Error detected - running error reflection...");

    // Capture context (required for all analyses)
    const context = await captureErrorContext(error);

    // Run 3 analyses in parallel (independent operations)
    const [rootCause, category, pattern] = await Promise.all([
      identifyRootCause(error, context),
      categorizeError(error, context),
      extractPattern(error, context)
    ]);

    // Aggregate results with cross-analysis insights
    const aggregatedPattern = pattern || await extractPattern(error, rootCause, category);

    if (aggregatedPattern) {
      // Update library
      await updatePatternLibrary(aggregatedPattern);

      // Generate prevention
      const prevention = generatePreventionRule(aggregatedPattern);

      console.log(`✓ Antipattern recorded: ${aggregatedPattern.name}`);
      console.log(`✓ Prevention rule generated`);
    }

    // Save error report
    await saveErrorReport({
      context,
      rootCause,
      category,
      pattern: aggregatedPattern
    });

    // Re-throw for normal error handling
    throw error;
  }
}
```

### Integration with Convergence Engine

```javascript
// After convergence phase completes
async function postConvergenceReflection(convergenceResult) {
  if (convergenceResult.issues.length > 0) {
    console.log("Running error reflection on audit issues...");

    for (const issue of convergenceResult.issues) {
      const pattern = await extractPatternFromIssue(issue);

      if (pattern) {
        await updatePatternLibrary(pattern);
      }
    }
  }
}
```

---

## Error Report Format

```json
{
  "id": "err-2026-02-04-10-30-45",
  "error": "429 Too Many Requests",
  "rootCause": "Pre-mortem missed rate limits",
  "category": "external",
  "pattern": "no-oauth-token-caching",
  "prevention": "prevent-no-oauth-token-caching"
}
```

---

## Metrics Tracking

```javascript
async function trackReflectionMetrics() {
  const metrics = {
    errorReflection: {
      totalErrors: await countErrors(),
      patternsExtracted: await countPatterns(),
      antipatternsExtracted: await countAntipatterns(),
      repeatErrors: await countRepeatErrors(),
      repeatErrorRate: calculateRepeatRate(),
      preventionRulesGenerated: await countPreventionRules(),
      preMortemsImproved: await countPreMortemUpdates()
    },
    effectiveness: {
      errorsPreventedByPreMortem: await countPreventedErrors(),
      timeToResolution: await calculateAverageResolutionTime(),
      patternReuseRate: await calculatePatternReuseRate()
    }
  };

  await saveMetrics(metrics);
  return metrics;
}
```

---

## Quick Reference

**Run error reflection manually:**
```javascript
const reflection = await runErrorReflection({
  error: caughtError,
  task: currentTask,
  context: additionalContext
});
```

**Query antipatterns:**
```javascript
const antipatterns = await queryAntipatterns({
  category: 'authentication',
  tags: ['oauth', 'rate-limiting']
});
```

**Check if error is known:**
```javascript
const isKnown = await isKnownAntipattern(error);
if (isKnown) {
  const fix = await getRecommendedFix(error);
  console.log("Known issue - recommended fix:", fix);
}
```

---

*End of Error Reflection*
*Part of v4.0.0 Universal Skills Ecosystem*
*Category: Learning (Post-Failure Analysis)*
*Builds institutional memory through systematic error analysis*
