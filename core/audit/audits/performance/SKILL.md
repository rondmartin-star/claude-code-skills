---
name: performance
description: >
  Performance audit checking slow queries, N+1 problems, memory leaks, inefficient
  algorithms, bundle size, and response times. Validates runtime performance. Use when:
  performance review, optimization, or part of technical/user methodology audits.
---

# Performance Audit

**Purpose:** Comprehensive performance validation
**Type:** Audit Type (Technical + User Methodologies)

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Audit performance"
- "Find slow queries"
- "Check for N+1 problems"
- "Analyze memory leaks"
- "Optimize bundle size"

**Context Indicators:**
- Performance degradation
- Part of convergence (technical or user methodology)
- Pre-release optimization
- Production performance issues

---

## Performance Checks

### 1. Slow Database Queries

**Detects:** Slow queries, missing indexes, full table scans, unoptimized JOINs

**Query Analysis:**
```javascript
async function analyzeQueries(queries) {
  const issues = [];

  for (const query of queries) {
    // Check for SELECT *
    if (/SELECT\s+\*/i.test(query.sql)) {
      issues.push({
        type: 'select_star',
        query: query.sql,
        severity: 'medium',
        suggestion: 'Select specific columns instead of *'
      });
    }

    // Check for missing WHERE on large tables
    if (/DELETE|UPDATE/i.test(query.sql) &&
        !/WHERE/i.test(query.sql)) {
      issues.push({
        type: 'missing_where',
        query: query.sql,
        severity: 'critical',
        suggestion: 'Add WHERE clause to prevent full table modification'
      });
    }

    // Check execution time
    if (query.executionTime > 1000) {
      issues.push({
        type: 'slow_query',
        query: query.sql,
        executionTime: query.executionTime,
        threshold: 1000,
        severity: 'high',
        suggestion: 'Add index or optimize query'
      });
    }
  }

  return issues;
}
```

**Index Analysis:**
```javascript
async function analyzeIndexes(db) {
  const issues = [];

  // Get all queries from codebase
  const queries = await extractQueriesFromCode();

  for (const query of queries) {
    const plan = await db.explain(query.sql);

    // Check for full table scans
    if (plan.some(step => step.type === 'ALL')) {
      const table = plan.find(s => s.type === 'ALL').table;

      issues.push({
        type: 'missing_index',
        table,
        query: query.sql,
        location: query.location,
        severity: 'high',
        suggestion: `Add index on ${table}`
      });
    }

    // Check for filesort
    if (plan.some(step => step.Extra?.includes('Using filesort'))) {
      issues.push({
        type: 'filesort',
        query: query.sql,
        severity: 'medium',
        suggestion: 'Add composite index for ORDER BY clause'
      });
    }
  }

  return issues;
}
```

### 2. N+1 Query Problem

**Detection:**
```javascript
async function detectN1Problems(code) {
  const issues = [];

  // Find loops with database queries
  traverse(ast, {
    ForStatement: (path) => {
      const loopBody = path.node.body;

      // Check for queries inside loop
      traverse(loopBody, {
        CallExpression: (innerPath) => {
          if (isQueryCall(innerPath.node)) {
            issues.push({
              type: 'n_plus_1',
              location: path.node.loc,
              query: getQueryString(innerPath.node),
              severity: 'high',
              suggestion: 'Use JOIN or batch query instead of loop'
            });
          }
        }
      });
    }
  });

  return issues;
}

function isQueryCall(node) {
  return (
    node.callee.property?.name === 'query' ||
    node.callee.property?.name === 'findOne' ||
    node.callee.property?.name === 'findById'
  );
}
```

**Example:**
```javascript
// ✗ N+1: Query inside loop
for (const order of orders) {
  order.items = await OrderItem.findAll({ where: { orderId: order.id } });
}

// ✓ Optimized: Use JOIN
return await Order.findAll({ include: [{ model: OrderItem }] });
```

### 3. Memory Leaks

**Common Patterns:**
- Event listeners not removed
- Timers not cleared
- Closures holding references
- Global variable accumulation

**Detection:**
```javascript
function detectMemoryLeaks(ast) {
  const issues = [];
  const eventListeners = new Map();
  const timers = new Map();

  // Track addEventListener without removeEventListener
  traverse(ast, {
    CallExpression: (path) => {
      const callee = path.node.callee;

      // Track event listeners
      if (callee.property?.name === 'addEventListener') {
        const id = generateId(path.node);
        eventListeners.set(id, path.node.loc);
      }

      if (callee.property?.name === 'removeEventListener') {
        const id = generateId(path.node);
        eventListeners.delete(id);
      }

      // Track timers
      if (callee.name === 'setInterval' || callee.name === 'setTimeout') {
        const id = generateId(path.node);
        timers.set(id, path.node.loc);
      }

      if (callee.name === 'clearInterval' || callee.name === 'clearTimeout') {
        const id = generateId(path.node);
        timers.delete(id);
      }
    }
  });

  // Unmatched event listeners = potential leak
  for (const [id, location] of eventListeners) {
    issues.push({
      type: 'event_listener_leak',
      location,
      severity: 'medium',
      suggestion: 'Remove event listener in cleanup/unmount'
    });
  }

  // Uncleared timers = potential leak
  for (const [id, location] of timers) {
    issues.push({
      type: 'timer_leak',
      location,
      severity: 'medium',
      suggestion: 'Clear timer in cleanup/unmount'
    });
  }

  return issues;
}
```

**React Example:**
```javascript
// ✗ Leak: No cleanup
useEffect(() => {
  window.addEventListener('resize', handleResize);
}, []);

// ✓ Cleanup
useEffect(() => {
  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, []);
```

### 4. Inefficient Algorithms

**Complexity Analysis:**
```javascript
function analyzeAlgorithmComplexity(ast) {
  const issues = [];

  traverse(ast, {
    FunctionDeclaration: (path) => {
      const complexity = estimateComplexity(path.node.body);

      if (complexity.order === 'O(n^2)' || complexity.order === 'O(n^3)') {
        issues.push({
          type: 'inefficient_algorithm',
          function: path.node.id.name,
          complexity: complexity.order,
          location: path.node.loc,
          severity: 'high',
          suggestion: complexity.optimization
        });
      }
    }
  });

  return issues;
}

function estimateComplexity(body) {
  let nestedLoops = 0;
  let hasSort = false;

  traverse(body, {
    ForStatement: {
      enter() { nestedLoops++; },
      exit() { nestedLoops--; }
    },
    CallExpression: (path) => {
      if (path.node.callee.property?.name === 'sort') {
        hasSort = true;
      }
    }
  });

  if (nestedLoops >= 3) {
    return {
      order: 'O(n^3)',
      optimization: 'Consider using hash map or different data structure'
    };
  } else if (nestedLoops === 2) {
    return {
      order: 'O(n^2)',
      optimization: 'Consider using hash map or single-pass algorithm'
    };
  } else if (hasSort) {
    return {
      order: 'O(n log n)',
      optimization: 'Acceptable for most use cases'
    };
  }

  return { order: 'O(n)', optimization: null };
}
```

**Example:**
```javascript
// ✗ O(n^2): Nested loops
for (let i = 0; i < arr.length; i++) {
  for (let j = i + 1; j < arr.length; j++) {
    if (arr[i] === arr[j]) duplicates.push(arr[i]);
  }
}

// ✓ O(n): Hash map
const seen = new Set();
for (const item of arr) {
  if (seen.has(item)) duplicates.add(item);
  seen.add(item);
}
```

### 5. Bundle Size Analysis

**JavaScript Bundle:**
```javascript
async function analyzeBundleSize(buildDir) {
  const bundles = await glob(`${buildDir}/**/*.js`);
  const issues = [];

  for (const bundle of bundles) {
    const size = fs.statSync(bundle).size;
    const sizeKB = size / 1024;

    if (sizeKB > 250) {
      issues.push({
        type: 'large_bundle',
        file: bundle,
        size: sizeKB,
        threshold: 250,
        severity: 'high',
        suggestion: 'Split bundle or use code splitting'
      });
    }

    // Check for duplicate dependencies
    const content = fs.readFileSync(bundle, 'utf8');
    const duplicates = findDuplicateDeps(content);

    if (duplicates.length > 0) {
      issues.push({
        type: 'duplicate_dependencies',
        file: bundle,
        duplicates,
        severity: 'medium',
        suggestion: 'Deduplicate dependencies in build config'
      });
    }
  }

  return issues;
}
```

**Tree Shaking Check:**
```javascript
function checkTreeShaking(imports) {
  const issues = [];

  imports.forEach(imp => {
    // Default import prevents tree shaking
    if (imp.type === 'ImportDefaultSpecifier' &&
        isLibraryWithNamedExports(imp.source.value)) {
      issues.push({
        type: 'no_tree_shaking',
        library: imp.source.value,
        location: imp.loc,
        severity: 'medium',
        suggestion: `Use named imports: import { x } from '${imp.source.value}'`
      });
    }
  });

  return issues;
}
```

### 6. Render Performance (Web)

**React Performance:**
```javascript
function analyzeReactPerformance(ast) {
  const issues = [];

  traverse(ast, {
    JSXElement: (path) => {
      // Check for inline functions in JSX
      const attributes = path.node.openingElement.attributes;

      attributes.forEach(attr => {
        if (attr.value?.expression?.type === 'ArrowFunctionExpression') {
          issues.push({
            type: 'inline_function_jsx',
            location: attr.loc,
            severity: 'medium',
            suggestion: 'Move function outside JSX to prevent re-renders'
          });
        }

        if (attr.value?.expression?.type === 'ObjectExpression') {
          issues.push({
            type: 'inline_object_jsx',
            location: attr.loc,
            severity: 'medium',
            suggestion: 'Move object outside JSX to prevent re-renders'
          });
        }
      });

      // Check for missing keys in lists
      if (isMapCall(path.parent)) {
        const keyAttr = attributes.find(a => a.name?.name === 'key');

        if (!keyAttr || isIndexUsedAsKey(keyAttr)) {
          issues.push({
            type: 'missing_or_index_key',
            location: path.node.loc,
            severity: 'high',
            suggestion: 'Use stable unique ID as key, not array index'
          });
        }
      }
    }
  });

  return issues;
}
```

### 7. API Response Times

**Monitor Response Times:**
```javascript
async function analyzeAPIPerformance(endpoints, logs) {
  const issues = [];

  for (const endpoint of endpoints) {
    const stats = calculateStats(logs, endpoint.path);

    if (stats.p95 > 1000) {
      issues.push({
        type: 'slow_endpoint',
        endpoint: endpoint.path,
        p95: stats.p95,
        threshold: 1000,
        severity: 'high',
        suggestion: 'Add caching or optimize database queries'
      });
    }

    if (stats.p99 > 3000) {
      issues.push({
        type: 'tail_latency',
        endpoint: endpoint.path,
        p99: stats.p99,
        severity: 'critical',
        suggestion: 'Investigate slow queries or external API calls'
      });
    }
  }

  return issues;
}

function calculateStats(logs, path) {
  const times = logs
    .filter(l => l.path === path)
    .map(l => l.responseTime)
    .sort((a, b) => a - b);

  return {
    p50: percentile(times, 50),
    p95: percentile(times, 95),
    p99: percentile(times, 99),
    avg: times.reduce((a, b) => a + b, 0) / times.length
  };
}
```

---

## Configuration

### corpus-config.json

```json
{
  "audit": {
    "convergence": {
      "methodologies": [
        {
          "name": "technical",
          "audits": [
            {
              "id": "performance",
              "config": {
                "max_query_time_ms": 1000,
                "max_bundle_size_kb": 250,
                "max_api_p95_ms": 1000,
                "max_api_p99_ms": 3000,
                "check_n1_queries": true,
                "check_memory_leaks": true,
                "check_algorithm_complexity": true
              }
            }
          ]
        },
        {
          "name": "user",
          "audits": [
            {
              "id": "performance",
              "config": {
                "max_page_load_ms": 3000,
                "max_time_to_interactive_ms": 5000,
                "max_bundle_size_kb": 200
              }
            }
          ]
        }
      ]
    }
  }
}
```

---

## Output Format

```json
{
  "audit_type": "performance",
  "timestamp": "2026-01-31T10:00:00Z",
  "project_path": "/path/to/project",
  "summary": {
    "slow_queries": 5,
    "n_plus_1_problems": 3,
    "memory_leaks": 2,
    "inefficient_algorithms": 4,
    "bundle_issues": 2,
    "api_performance_issues": 6
  },
  "issues": [
    {
      "severity": "high",
      "category": "slow_query",
      "location": "src/models/user.js:45",
      "query": "SELECT * FROM users WHERE status = 'active'",
      "executionTime": 1523,
      "threshold": 1000,
      "suggestion": "Add index on status column",
      "auto_fixable": false
    },
    {
      "severity": "high",
      "category": "n_plus_1",
      "location": "src/controllers/orders.js:28",
      "suggestion": "Use JOIN or eager loading",
      "auto_fixable": false
    },
    {
      "severity": "medium",
      "category": "memory_leak",
      "type": "event_listener_leak",
      "location": "src/components/Chart.jsx:15",
      "suggestion": "Remove event listener in cleanup",
      "auto_fixable": true
    }
  ]
}
```

---

## Auto-Fix Capabilities

### ✓ Fully Automatic

**Memory Leaks (React):**
```
Issue: Missing cleanup for event listener
Fix: Add return statement with cleanup function
Strategy: Generate cleanup code automatically
```

**Inline Functions in JSX:**
```
Issue: Arrow function in JSX prop
Fix: Extract to component method
Strategy: Hoist function automatically
```

### ⚠ User Approval Required

**N+1 Queries:**
```
Issue: Query inside loop
Fix: Replace with JOIN or batch query
Strategy: Suggest optimized query, user approves
```

**Algorithm Optimization:**
```
Issue: O(n^2) nested loops
Fix: Replace with hash map approach
Strategy: Generate optimized version, user reviews
```

### ✗ Manual Only

**Database Indexes:**
```
Issue: Missing index causing slow query
Fix: Requires database migration
Strategy: Generate migration file, user applies
```

**Architecture Changes:**
```
Issue: Synchronous API calls blocking render
Fix: Requires architectural refactoring
Strategy: Provide guidance on async patterns
```

---

## Integration with Methodologies

Performance audit applies to **both technical and user** methodologies:

**Technical Methodology:**
- Database query performance
- Algorithm efficiency
- Memory management
- Code optimization

**User Methodology:**
- Page load times
- Time to interactive
- Perceived performance
- Bundle size impact

---

*End of Performance Audit*
*Part of v4.0.0 Universal Skills Ecosystem*
*Methodologies: Technical + User*
*Supports runtime performance optimization*
