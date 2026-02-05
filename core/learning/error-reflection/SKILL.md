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

**Example - OAuth Rate Limit Error:**
```
Why 1: "Why did authentication fail?"
→ "OAuth provider returned 429 Too Many Requests"

Why 2: "Why are we hitting rate limits?"
→ "Application makes new OAuth request for each user action"

Why 3: "Why don't we cache tokens?"
→ "No caching mechanism was implemented"

Why 4: "Why wasn't caching implemented?"
→ "Requirements didn't mention rate limits as a risk"

Why 5: "Why weren't rate limits in requirements?"
→ ROOT CAUSE: "Pre-mortem didn't identify third-party rate limits as a risk"
```

### 3. Categorize Error Type

```javascript
function categorizeError(error, rootCause) {
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

  const classification = classifyByPattern(error, rootCause, categories);

  return {
    primary: classification.primary,
    secondary: classification.secondary || [],
    tags: extractTags(error, rootCause)
  };
}
```

### 4. Extract Pattern or Antipattern

```javascript
async function extractPattern(error, rootCause, category) {
  // Determine if this reveals an antipattern or a solution pattern
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
```

**Example Antipattern:**
```json
{
  "type": "antipattern",
  "name": "no-oauth-token-caching",
  "category": "authentication",
  "problem": "Making OAuth token requests on every user action",
  "symptoms": [
    "429 Too Many Requests errors",
    "Slow authentication",
    "Intermittent auth failures"
  ],
  "consequences": {
    "severity": "high",
    "userImpact": "Cannot log in during rate limit",
    "businessImpact": "Service unavailable"
  },
  "prevention": {
    "rule": "Always cache OAuth tokens with proper expiration",
    "implementation": "Use Redis or in-memory cache with token refresh logic",
    "validation": "Monitor OAuth API request rate in development"
  },
  "detection": {
    "metrics": ["OAuth requests per minute > threshold"],
    "alerts": ["429 responses from OAuth provider"]
  },
  "relatedPatterns": ["oauth-token-caching", "exponential-backoff"],
  "occurrences": 1,
  "firstSeen": "2026-02-04T10:00:00Z",
  "lastSeen": "2026-02-04T10:00:00Z"
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

### Automatic Error Capture

```javascript
async function executeTaskWithErrorReflection(task) {
  try {
    const result = await executeTask(task);
    return result;
  } catch (error) {
    console.log("⚠️ Error detected - running error reflection...");

    // Capture context
    const context = await captureErrorContext(error);

    // Analyze root cause
    const rootCause = await identifyRootCause(error, context);

    // Categorize
    const category = categorizeError(error, rootCause);

    // Extract pattern/antipattern
    const pattern = await extractPattern(error, rootCause, category);

    if (pattern) {
      // Update library
      await updatePatternLibrary(pattern);

      // Generate prevention
      const prevention = generatePreventionRule(pattern);

      console.log(`✓ Antipattern recorded: ${pattern.name}`);
      console.log(`✓ Prevention rule generated`);
    }

    // Save error report
    await saveErrorReport({
      context,
      rootCause,
      category,
      pattern
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
  "errorReport": {
    "id": "err-2026-02-04-10-30-45",
    "timestamp": "2026-02-04T10:30:45Z",
    "context": {
      "task": "Implement OAuth authentication",
      "phase": "implementation",
      "files": ["src/auth/oauth.js"]
    },
    "error": {
      "message": "429 Too Many Requests",
      "type": "HttpError",
      "stack": "..."
    },
    "rootCause": {
      "description": "Pre-mortem didn't identify third-party rate limits",
      "chain": [...]
    },
    "category": {
      "primary": "external",
      "secondary": ["assumptions"],
      "tags": ["oauth", "rate-limiting", "third-party"]
    },
    "pattern": {
      "type": "antipattern",
      "name": "no-oauth-token-caching",
      "saved": ".corpus/learning/antipatterns/authentication/"
    },
    "prevention": {
      "rule": "prevent-no-oauth-token-caching",
      "integrated": true,
      "preMortemUpdated": true
    }
  }
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
