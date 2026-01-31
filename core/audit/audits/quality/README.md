# Quality Audit

**Purpose:** Code quality validation checking complexity, duplication, dead code, and test coverage

**Size:** 15.0 KB

---

## Quick Start

```javascript
// Run quality audit
const issues = await runAudit('quality', projectConfig);

// Check specific metrics
const complexity = calculateComplexity(ast);
const duplicates = await findDuplicates(files);
const coverage = await analyzeCoverage('coverage.json');
```

## What It Does

- Calculates cyclomatic complexity
- Detects code duplication
- Finds dead code (unused vars, functions, imports)
- Analyzes test coverage
- Runs linting checks
- Validates best practices
- Checks documentation coverage

## When to Use

✅ Pre-release quality review
✅ Refactoring preparation
✅ Part of technical methodology

❌ Security audits (use security audit)
❌ Performance analysis (use performance audit)

## Thresholds

- Complexity: Max 10 per function
- Duplication: Max 5% of codebase
- Coverage: Min 80% lines, 75% branches
- Function length: Max 50 lines
- Nesting depth: Max 4 levels

---

**Part of:** v4.0.0 Universal Skills  
**Category:** Technical Methodology  
**Auto-fix:** Dead code removal, simple linting
