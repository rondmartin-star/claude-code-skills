# Parallel Audit Execution - Implementation Reference

**Purpose:** Detailed implementation guide for parallel audit execution with dependency resolution

---

## Dependency Graph

### Known Dependencies

```javascript
const AUDIT_DEPENDENCIES = {
  'navigation': ['consistency'],
  'performance': ['quality'],
  'seo': ['content'],
  'accessibility': ['quality']
};
```

**Rationale:**

| Dependent Audit | Requires | Reason |
|----------------|----------|--------|
| **navigation** | consistency | Navigation audit validates links and cross-references, which requires framework terms to be validated first by consistency audit |
| **performance** | quality | Performance audit analyzes code efficiency, which requires the code to be syntactically valid and lint-clean from quality audit |
| **seo** | content | SEO audit checks meta tags and descriptions, which requires content to be grammatically correct from content audit |
| **accessibility** | quality | Accessibility audit checks DOM structure, which requires valid HTML/JSX from quality audit |

### Extending Dependencies

To add new dependencies, update the `AUDIT_DEPENDENCIES` constant:

```javascript
const AUDIT_DEPENDENCIES = {
  'navigation': ['consistency'],
  'performance': ['quality'],
  'seo': ['content'],
  'accessibility': ['quality'],
  'custom-audit': ['dependency-1', 'dependency-2']  // New dependency
};
```

---

## Implementation Functions

### 1. Dependency Detection

```javascript
/**
 * Detect dependencies between audits
 * @param {string[]} auditTypes - List of audit types to run
 * @returns {Array<{audit: string, requires: string, reason: string}>}
 */
function detectAuditDependencies(auditTypes) {
  const dependencies = [];

  auditTypes.forEach(audit => {
    if (AUDIT_DEPENDENCIES[audit]) {
      AUDIT_DEPENDENCIES[audit].forEach(requiredAudit => {
        if (auditTypes.includes(requiredAudit)) {
          dependencies.push({
            audit,
            requires: requiredAudit,
            reason: `${audit} needs ${requiredAudit} to complete first`
          });
        }
      });
    }
  });

  return dependencies;
}
```

### 2. Sequential Execution (Fallback)

```javascript
/**
 * Execute audits sequentially (fallback for parallel=false)
 * @param {string[]} auditTypes - List of audit types to run
 * @returns {Promise<Array>} - Array of audit results
 */
async function executeSequential(auditTypes) {
  const results = [];

  for (const auditType of auditTypes) {
    console.log(`Running ${auditType} audit...`);
    const result = await executeAudit(auditType);
    results.push(result);
  }

  return results;
}
```

### 3. Parallel Execution with Batching

```javascript
/**
 * Execute audits in parallel with batching to limit concurrency
 * @param {string[]} auditTypes - List of audit types to run
 * @param {number} maxConcurrent - Maximum concurrent operations
 * @returns {Promise<Array>} - Array of audit results
 */
async function executeParallel(auditTypes, maxConcurrent = 5) {
  const results = [];

  // Execute in batches to limit concurrent operations
  for (let i = 0; i < auditTypes.length; i += maxConcurrent) {
    const batch = auditTypes.slice(i, i + maxConcurrent);
    console.log(`Parallel batch ${Math.floor(i / maxConcurrent) + 1}: ${batch.join(', ')}`);

    const batchResults = await Promise.all(
      batch.map(auditType => executeAudit(auditType))
    );

    results.push(...batchResults);
  }

  return results;
}
```

### 4. Main Orchestrator

```javascript
/**
 * Execute audits with dependency resolution and parallel execution
 * @param {string[]} auditTypes - List of audit types to run
 * @param {Object} options - Execution options
 * @returns {Promise<Array>} - Array of audit results
 */
async function executeAuditsWithDependencies(auditTypes, options = {}) {
  const { maxConcurrent = 5, parallel = true } = options;

  // Detect dependencies
  const deps = detectAuditDependencies(auditTypes);

  if (!parallel || auditTypes.length === 1) {
    // Sequential fallback
    console.log('Executing audits sequentially');
    return await executeSequential(auditTypes);
  }

  if (deps.length === 0) {
    // No dependencies: full parallel with batching
    console.log('No dependencies detected - full parallel execution');
    return await executeParallel(auditTypes, maxConcurrent);
  }

  // Has dependencies: topological sort + level-based parallel
  console.log(`Dependencies detected (${deps.length}) - using level-based parallel`);
  deps.forEach(dep => {
    console.log(`  • ${dep.audit} requires ${dep.requires}`);
  });

  const levels = topologicalSort(auditTypes, deps);

  console.log(`Execution plan: ${levels.length} level(s)`);
  levels.forEach((level, i) => {
    console.log(`  Level ${i + 1}: ${level.join(', ')}`);
  });

  const results = [];
  for (let i = 0; i < levels.length; i++) {
    const level = levels[i];
    console.log(`\n═══ LEVEL ${i + 1} (${level.length} audit${level.length > 1 ? 's' : ''}) ═══`);
    const levelResults = await executeParallel(level, maxConcurrent);
    results.push(...levelResults);
  }

  return results;
}
```

### 5. Topological Sort

```javascript
/**
 * Topologically sort audits into levels for parallel execution
 * @param {string[]} auditTypes - List of audit types
 * @param {Array} dependencies - Dependency edges
 * @returns {Array<Array<string>>} - Array of levels, each containing audits to run in parallel
 */
function topologicalSort(auditTypes, dependencies) {
  // Build adjacency list and in-degree map
  const graph = new Map();
  const inDegree = new Map();

  // Initialize graph
  auditTypes.forEach(audit => {
    graph.set(audit, []);
    inDegree.set(audit, 0);
  });

  // Build dependency edges
  dependencies.forEach(({ audit, requires }) => {
    graph.get(requires).push(audit);
    inDegree.set(audit, inDegree.get(audit) + 1);
  });

  // Level-by-level BFS (Kahn's algorithm)
  const levels = [];
  let remaining = new Set(auditTypes);

  while (remaining.size > 0) {
    const currentLevel = [];

    // Find all nodes with in-degree 0 (no dependencies)
    remaining.forEach(audit => {
      if (inDegree.get(audit) === 0) {
        currentLevel.push(audit);
      }
    });

    if (currentLevel.length === 0) {
      // Circular dependency detected
      const remainingAudits = Array.from(remaining);
      throw new Error(
        `Circular dependency detected in audits: ${remainingAudits.join(', ')}`
      );
    }

    levels.push(currentLevel);

    // Remove current level and update in-degrees
    currentLevel.forEach(audit => {
      remaining.delete(audit);

      // Decrease in-degree for dependents
      graph.get(audit).forEach(dependent => {
        inDegree.set(dependent, inDegree.get(dependent) - 1);
      });
    });
  }

  return levels;
}
```

### 6. Audit Executor with Error Handling

```javascript
/**
 * Execute a single audit with error handling
 * @param {string} auditType - Type of audit to run
 * @returns {Promise<Object>} - Audit result with success status
 */
async function executeAudit(auditType) {
  const startTime = Date.now();

  try {
    console.log(`  Starting ${auditType}...`);

    // Load and execute the specific audit
    const auditSkill = await loadSkill(`audits/${auditType}`);
    const result = await auditSkill.run();

    const duration = ((Date.now() - startTime) / 1000).toFixed(1);
    const issueCount = result.issues?.length || 0;

    console.log(`  ✓ ${auditType} complete (${duration}s) - ${issueCount} issue${issueCount !== 1 ? 's' : ''}`);

    return {
      auditType,
      success: true,
      duration: parseFloat(duration),
      ...result
    };

  } catch (error) {
    const duration = ((Date.now() - startTime) / 1000).toFixed(1);

    console.error(`  ✗ ${auditType} failed (${duration}s): ${error.message}`);

    return {
      auditType,
      success: false,
      duration: parseFloat(duration),
      error: error.message,
      issues: []
    };
  }
}
```

---

## Configuration

### corpus-config.json

```json
{
  "audit_config": {
    "execution": {
      "parallel": true,
      "maxConcurrent": 5,
      "respectDependencies": true
    }
  }
}
```

### Runtime Override

```javascript
// Enable parallel with custom concurrency
await auditOrchestrator.run({
  parallel: true,
  maxConcurrent: 10
});

// Disable parallel (sequential)
await auditOrchestrator.run({
  parallel: false
});

// Force parallel without dependency checking (dangerous!)
await auditOrchestrator.run({
  parallel: true,
  respectDependencies: false
});
```

---

## Performance Metrics

### Tracking

```javascript
async function executeAuditsWithMetrics(auditTypes, options = {}) {
  const startTime = Date.now();
  const metrics = {
    totalAudits: auditTypes.length,
    parallelEnabled: options.parallel ?? true,
    levels: 0,
    totalDuration: 0,
    auditDurations: {}
  };

  const results = await executeAuditsWithDependencies(auditTypes, options);

  metrics.totalDuration = ((Date.now() - startTime) / 1000).toFixed(1);
  metrics.levels = results.filter(r => r.level !== undefined).length;

  results.forEach(result => {
    metrics.auditDurations[result.auditType] = result.duration;
  });

  // Calculate speedup estimate
  const sequentialEstimate = Object.values(metrics.auditDurations).reduce((a, b) => a + b, 0);
  metrics.speedup = (sequentialEstimate / parseFloat(metrics.totalDuration)).toFixed(2);

  console.log(`\n═══ PERFORMANCE METRICS ═══`);
  console.log(`Total audits: ${metrics.totalAudits}`);
  console.log(`Parallel: ${metrics.parallelEnabled ? 'enabled' : 'disabled'}`);
  console.log(`Execution levels: ${metrics.levels}`);
  console.log(`Total time: ${metrics.totalDuration}s`);
  console.log(`Sequential estimate: ${sequentialEstimate.toFixed(1)}s`);
  console.log(`Speedup: ${metrics.speedup}x`);

  return { results, metrics };
}
```

---

## Error Handling

### Handling Individual Failures

Individual audit failures don't block other audits:

```javascript
async function executeParallel(auditTypes, maxConcurrent = 5) {
  const results = [];

  for (let i = 0; i < auditTypes.length; i += maxConcurrent) {
    const batch = auditTypes.slice(i, i + maxConcurrent);

    // Use Promise.allSettled to continue on individual failures
    const batchResults = await Promise.allSettled(
      batch.map(auditType => executeAudit(auditType))
    );

    // Extract results from settled promises
    batchResults.forEach((settled, index) => {
      if (settled.status === 'fulfilled') {
        results.push(settled.value);
      } else {
        // Promise rejected - create error result
        results.push({
          auditType: batch[index],
          success: false,
          error: settled.reason.message,
          issues: []
        });
      }
    });
  }

  return results;
}
```

### Handling Critical Failures

If a critical audit fails, stop execution:

```javascript
async function executeWithCriticalCheck(auditTypes, criticalAudits = []) {
  const results = await executeAuditsWithDependencies(auditTypes);

  // Check if any critical audits failed
  const criticalFailures = results.filter(r =>
    criticalAudits.includes(r.auditType) && !r.success
  );

  if (criticalFailures.length > 0) {
    throw new Error(
      `Critical audits failed: ${criticalFailures.map(r => r.auditType).join(', ')}`
    );
  }

  return results;
}
```

---

## Testing

### Unit Test Example

```javascript
describe('Parallel Audit Execution', () => {
  test('detects dependencies correctly', () => {
    const audits = ['navigation', 'consistency', 'performance', 'quality'];
    const deps = detectAuditDependencies(audits);

    expect(deps).toHaveLength(2);
    expect(deps).toContainEqual({
      audit: 'navigation',
      requires: 'consistency',
      reason: expect.any(String)
    });
    expect(deps).toContainEqual({
      audit: 'performance',
      requires: 'quality',
      reason: expect.any(String)
    });
  });

  test('sorts audits into correct levels', () => {
    const audits = ['navigation', 'consistency'];
    const deps = [{ audit: 'navigation', requires: 'consistency' }];
    const levels = topologicalSort(audits, deps);

    expect(levels).toHaveLength(2);
    expect(levels[0]).toEqual(['consistency']);
    expect(levels[1]).toEqual(['navigation']);
  });

  test('throws on circular dependency', () => {
    const audits = ['a', 'b'];
    const deps = [
      { audit: 'a', requires: 'b' },
      { audit: 'b', requires: 'a' }
    ];

    expect(() => topologicalSort(audits, deps)).toThrow('Circular dependency');
  });
});
```

---

## Optimization Tips

### 1. Adjust maxConcurrent Based on Resources

```javascript
// Low memory environment
await executeAuditsWithDependencies(audits, { maxConcurrent: 2 });

// High-spec machine
await executeAuditsWithDependencies(audits, { maxConcurrent: 10 });
```

### 2. Profile Audit Duration

Track which audits take longest to optimize:

```javascript
const results = await executeAuditsWithDependencies(audits);
const sorted = results.sort((a, b) => b.duration - a.duration);

console.log('Slowest audits:');
sorted.slice(0, 5).forEach(r => {
  console.log(`  ${r.auditType}: ${r.duration}s`);
});
```

### 3. Cache Audit Results

For convergence, cache results within iteration:

```javascript
const auditCache = new Map();

async function executeAuditCached(auditType, cacheKey) {
  const cached = auditCache.get(`${auditType}-${cacheKey}`);
  if (cached) {
    console.log(`  ⚡ ${auditType} (cached)`);
    return cached;
  }

  const result = await executeAudit(auditType);
  auditCache.set(`${auditType}-${cacheKey}`, result);
  return result;
}
```

---

*End of Parallel Execution Reference*
*Part of audit-orchestrator v4.0*
