# Performance Audit

**Purpose:** Performance validation checking slow queries, N+1 problems, memory leaks, and inefficient algorithms

**Size:** 15.3 KB

---

## Quick Start

```javascript
// Run performance audit
const issues = await runAudit('performance', projectConfig);

// Analyze specific areas
const slowQueries = await analyzeQueries(queries);
const n1Problems = await detectN1Problems(code);
const memoryLeaks = await detectMemoryLeaks(ast);
```

## What It Does

- Detects slow database queries
- Finds N+1 query problems
- Identifies memory leaks
- Analyzes algorithm complexity
- Checks bundle size
- Monitors API response times
- Validates React render performance

## When to Use

✅ Performance degradation
✅ Pre-release optimization
✅ Part of technical/user methodologies

❌ Code quality (use quality audit)
❌ Security issues (use security audit)

## Thresholds

- Query time: Max 1000ms
- Bundle size: Max 250KB
- API p95: Max 1000ms
- API p99: Max 3000ms

---

**Part of:** v4.0.0 Universal Skills  
**Categories:** Technical + User Methodologies  
**Auto-fix:** Memory leak cleanup, inline function extraction
