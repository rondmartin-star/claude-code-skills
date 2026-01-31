---
name: quality
description: >
  Code quality audit checking complexity, duplication, dead code, test coverage, and
  best practices. Validates technical implementation quality. Use when: quality review,
  pre-release validation, or part of technical methodology audits.
---

# Quality Audit

**Purpose:** Comprehensive code quality validation
**Size:** ~11 KB
**Type:** Audit Type (Part of Technical Methodology)

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Audit code quality"
- "Check code complexity"
- "Find code duplication"
- "Analyze test coverage"

**Context Indicators:**
- Pre-release quality review
- Part of convergence (technical methodology)
- Code quality assurance
- Refactoring preparation

---

## Quality Checks

### 1. Cyclomatic Complexity

**Measures:** Number of independent paths through code

**Thresholds:**
- 1-10: Simple (low risk)
- 11-20: Moderate (medium risk)
- 21-50: Complex (high risk)
- 51+: Untestable (critical risk)

**Detection:**
```javascript
function calculateComplexity(ast) {
  let complexity = 1; // Base complexity

  // Count decision points
  traverse(ast, {
    IfStatement: () => complexity++,
    WhileStatement: () => complexity++,
    ForStatement: () => complexity++,
    CaseClause: () => complexity++,
    LogicalExpression: (node) => {
      if (node.operator === '&&' || node.operator === '||') {
        complexity++;
      }
    },
    ConditionalExpression: () => complexity++,
    CatchClause: () => complexity++
  });

  return complexity;
}
```

**Example Issues:**
```javascript
// ✗ High complexity (15)
function processOrder(order) {
  if (order.status === 'pending') {
    if (order.items.length > 0) {
      for (let item of order.items) {
        if (item.inStock) {
          if (item.price > 0) {
            if (order.user.verified) {
              if (item.quantity > 0 && item.quantity <= item.maxQuantity) {
                // Process item
              }
            }
          }
        }
      }
    }
  }
}

// ✓ Lower complexity (split into smaller functions)
function processOrder(order) {
  if (!isValidOrder(order)) return;

  const validItems = getValidItems(order);
  validItems.forEach(item => processItem(item, order));
}
```

### 2. Code Duplication

**Types:**
- Exact duplicates (copy-paste)
- Structural duplicates (similar logic)
- Semantic duplicates (same behavior, different code)

**Detection:**
```javascript
async function findDuplicates(files, minTokens = 50) {
  const duplicates = [];
  const codeBlocks = new Map();

  for (const file of files) {
    const ast = parse(file.content);
    const blocks = extractCodeBlocks(ast, minTokens);

    blocks.forEach(block => {
      const hash = hashBlock(block);

      if (codeBlocks.has(hash)) {
        duplicates.push({
          locations: [codeBlocks.get(hash), block.location],
          tokens: block.tokens,
          similarity: 100
        });
      } else {
        codeBlocks.set(hash, block.location);
      }
    });
  }

  return duplicates;
}

function hashBlock(block) {
  // Normalize whitespace and variable names
  const normalized = block.code
    .replace(/\s+/g, ' ')
    .replace(/\b[a-z]\w*\b/g, 'VAR');

  return crypto.createHash('sha256')
    .update(normalized)
    .digest('hex');
}
```

**Thresholds:**
```json
{
  "config": {
    "min_duplicate_tokens": 50,
    "max_duplicate_percent": 5,
    "ignore_patterns": [
      "test/fixtures/*",
      "**/*.test.js"
    ]
  }
}
```

### 3. Dead Code Detection

**Types:**
- Unreachable code
- Unused variables
- Unused functions
- Unused imports
- Unused parameters

**Detection:**
```javascript
function findDeadCode(ast) {
  const issues = [];
  const declared = new Set();
  const used = new Set();

  // First pass: collect declarations
  traverse(ast, {
    VariableDeclarator: (path) => {
      declared.add(path.node.id.name);
    },
    FunctionDeclaration: (path) => {
      declared.add(path.node.id.name);
    },
    ImportSpecifier: (path) => {
      declared.add(path.node.local.name);
    }
  });

  // Second pass: track usage
  traverse(ast, {
    Identifier: (path) => {
      if (path.isReferencedIdentifier()) {
        used.add(path.node.name);
      }
    }
  });

  // Find unused
  for (const name of declared) {
    if (!used.has(name)) {
      issues.push({
        type: 'unused',
        name,
        severity: 'low'
      });
    }
  }

  return issues;
}
```

**Unreachable Code:**
```javascript
// Detect code after return/throw
traverse(ast, {
  BlockStatement: (path) => {
    const statements = path.node.body;

    for (let i = 0; i < statements.length - 1; i++) {
      const stmt = statements[i];

      if (isTerminating(stmt)) {
        // All statements after this are unreachable
        issues.push({
          type: 'unreachable',
          location: statements[i + 1].loc,
          severity: 'medium'
        });
        break;
      }
    }
  }
});

function isTerminating(stmt) {
  return stmt.type === 'ReturnStatement' ||
         stmt.type === 'ThrowStatement' ||
         (stmt.type === 'BreakStatement' && !stmt.label) ||
         (stmt.type === 'ContinueStatement' && !stmt.label);
}
```

### 4. Test Coverage

**Metrics:**
- Line coverage
- Branch coverage
- Function coverage
- Statement coverage

**Coverage Analysis:**
```javascript
async function analyzeCoverage(coverageFile) {
  const coverage = JSON.parse(fs.readFileSync(coverageFile, 'utf8'));
  const summary = {
    lines: { covered: 0, total: 0 },
    branches: { covered: 0, total: 0 },
    functions: { covered: 0, total: 0 },
    statements: { covered: 0, total: 0 }
  };

  for (const file of Object.values(coverage)) {
    summary.lines.total += Object.keys(file.statementMap).length;
    summary.lines.covered += Object.values(file.s).filter(v => v > 0).length;

    summary.branches.total += Object.keys(file.branchMap).length;
    summary.branches.covered += Object.values(file.b)
      .filter(arr => arr.some(v => v > 0)).length;

    summary.functions.total += Object.keys(file.fnMap).length;
    summary.functions.covered += Object.values(file.f).filter(v => v > 0).length;
  }

  return {
    lines: (summary.lines.covered / summary.lines.total * 100).toFixed(2),
    branches: (summary.branches.covered / summary.branches.total * 100).toFixed(2),
    functions: (summary.functions.covered / summary.functions.total * 100).toFixed(2)
  };
}
```

**Thresholds from Config:**
```json
{
  "quality": {
    "config": {
      "min_line_coverage": 80,
      "min_branch_coverage": 75,
      "min_function_coverage": 90
    }
  }
}
```

### 5. Linting Issues

**Categories:**
- Style violations
- Best practice violations
- Potential bugs
- Code smells

**ESLint Integration:**
```javascript
async function runLinter(files, config) {
  const eslint = new ESLint({
    baseConfig: config.eslintConfig || {},
    useEslintrc: false
  });

  const results = await eslint.lintFiles(files);
  const issues = [];

  results.forEach(result => {
    result.messages.forEach(msg => {
      issues.push({
        severity: msg.severity === 2 ? 'high' : 'medium',
        category: 'linting',
        location: `${result.filePath}:${msg.line}:${msg.column}`,
        rule: msg.ruleId,
        message: msg.message,
        auto_fixable: msg.fix !== undefined
      });
    });
  });

  return issues;
}
```

### 6. Best Practices

**Checks:**
- Magic numbers
- Long functions
- Long parameter lists
- Deep nesting
- God objects (too many responsibilities)

**Magic Numbers:**
```javascript
function findMagicNumbers(ast) {
  const issues = [];

  traverse(ast, {
    Literal: (path) => {
      if (typeof path.node.value === 'number' &&
          path.node.value !== 0 &&
          path.node.value !== 1 &&
          !isInConstDeclaration(path)) {
        issues.push({
          type: 'magic_number',
          value: path.node.value,
          location: path.node.loc,
          suggestion: 'Extract to named constant'
        });
      }
    }
  });

  return issues;
}
```

**Long Functions:**
```javascript
function checkFunctionLength(ast, maxLines = 50) {
  const issues = [];

  traverse(ast, {
    FunctionDeclaration: (path) => {
      const lines = path.node.loc.end.line - path.node.loc.start.line;

      if (lines > maxLines) {
        issues.push({
          type: 'long_function',
          name: path.node.id.name,
          lines,
          maxLines,
          suggestion: 'Split into smaller functions'
        });
      }
    }
  });

  return issues;
}
```

**Deep Nesting:**
```javascript
function checkNesting(ast, maxDepth = 4) {
  const issues = [];

  traverse(ast, {
    BlockStatement: {
      enter(path) {
        const depth = getDepth(path);

        if (depth > maxDepth) {
          issues.push({
            type: 'deep_nesting',
            depth,
            maxDepth,
            location: path.node.loc,
            suggestion: 'Extract nested logic to separate function'
          });
        }
      }
    }
  });

  return issues;
}

function getDepth(path) {
  let depth = 0;
  let current = path;

  while (current.parent) {
    if (current.node.type === 'BlockStatement') {
      depth++;
    }
    current = current.parent;
  }

  return depth;
}
```

### 7. Documentation Coverage

**Check for:**
- Missing function documentation
- Missing parameter descriptions
- Missing return type documentation
- Outdated documentation

**Detection:**
```javascript
function checkDocumentation(ast) {
  const issues = [];

  traverse(ast, {
    FunctionDeclaration: (path) => {
      const comments = path.node.leadingComments;

      if (!comments || comments.length === 0) {
        issues.push({
          type: 'missing_docs',
          function: path.node.id.name,
          severity: 'low'
        });
        return;
      }

      const jsdoc = parseJSDoc(comments[comments.length - 1].value);

      // Check parameters documented
      const params = path.node.params.map(p => p.name);
      const documented = jsdoc.params.map(p => p.name);

      params.forEach(param => {
        if (!documented.includes(param)) {
          issues.push({
            type: 'undocumented_param',
            function: path.node.id.name,
            param,
            severity: 'low'
          });
        }
      });

      // Check return documented
      if (!jsdoc.returns && hasReturn(path.node.body)) {
        issues.push({
          type: 'undocumented_return',
          function: path.node.id.name,
          severity: 'low'
        });
      }
    }
  });

  return issues;
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
          "description": "How it's built",
          "audits": [
            {
              "id": "quality",
              "config": {
                "max_complexity": 10,
                "max_function_length": 50,
                "max_nesting_depth": 4,
                "max_parameters": 5,
                "max_duplicate_percent": 5,
                "min_duplicate_tokens": 50,
                "min_line_coverage": 80,
                "min_branch_coverage": 75,
                "min_function_coverage": 90,
                "check_dead_code": true,
                "check_documentation": true,
                "eslint_config": {
                  "extends": ["eslint:recommended"],
                  "rules": {
                    "no-console": "warn",
                    "no-unused-vars": "error"
                  }
                }
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

## Auto-Fix Capabilities

### ✓ Fully Automatic

**Dead Code Removal:**
```
Issue: Unused import 'fs'
Fix: Remove import statement
Strategy: Safe to remove if truly unused
```

**Simple Linting:**
```
Issue: Missing semicolon
Fix: Add semicolon
Strategy: ESLint auto-fix
```

### ⚠ User Approval Required

**Complexity Reduction:**
```
Issue: Function has complexity 25
Fix: Extract nested logic to helper functions
Strategy: Suggest refactoring, user approves
```

**Duplication Removal:**
```
Issue: 50 lines duplicated in 3 files
Fix: Extract to shared utility function
Strategy: Generate refactoring plan, user approves
```

### ✗ Manual Only

**Architecture Issues:**
```
Issue: God object with 20 responsibilities
Fix: Requires architectural redesign
Strategy: Flag for manual review
```

**Deep Refactoring:**
```
Issue: Deep nesting (7 levels)
Fix: Requires logic restructuring
Strategy: Provide refactoring guidance
```

---

## Output Format

```json
{
  "audit_type": "quality",
  "timestamp": "2026-01-31T10:00:00Z",
  "project_path": "/path/to/project",
  "summary": {
    "files_scanned": 150,
    "complexity_issues": 8,
    "duplication_percent": 3.2,
    "dead_code_items": 12,
    "coverage": {
      "lines": 85.3,
      "branches": 78.2,
      "functions": 92.1
    },
    "linting_issues": 25,
    "best_practice_violations": 15
  },
  "issues": [
    {
      "severity": "high",
      "category": "complexity",
      "location": "src/processor.js:42",
      "function": "processData",
      "complexity": 18,
      "threshold": 10,
      "suggestion": "Split into smaller functions",
      "auto_fixable": false
    },
    {
      "severity": "medium",
      "category": "duplication",
      "locations": [
        "src/utils/validator.js:10-35",
        "src/helpers/check.js:45-70"
      ],
      "tokens": 87,
      "suggestion": "Extract to shared function",
      "auto_fixable": false
    },
    {
      "severity": "low",
      "category": "dead_code",
      "location": "src/index.js:5",
      "type": "unused_import",
      "name": "fs",
      "auto_fixable": true
    }
  ]
}
```

---

## Integration with Technical Methodology

Quality audit is part of the **technical methodology** in 3-3-1 convergence:

```json
{
  "methodologies": [
    {
      "name": "technical",
      "description": "How it's built",
      "audits": [
        "quality",          // ← This audit
        "security",
        "dependency",
        "performance"
      ]
    }
  ]
}
```

**Technical Perspective:**
- Is code maintainable and readable?
- Are functions appropriately sized?
- Is test coverage adequate?
- Are best practices followed?

---

## Quick Reference

**Run quality audit:**
```javascript
const issues = await runAudit('quality', projectConfig);
```

**Check specific metrics:**
```javascript
const complexity = calculateComplexity(ast);
const duplicates = await findDuplicates(files);
const coverage = await analyzeCoverage('coverage.json');
```

**Generate quality report:**
```javascript
const report = await generateQualityReport(projectPath);
console.log(`Complexity issues: ${report.summary.complexity_issues}`);
console.log(`Coverage: ${report.summary.coverage.lines}%`);
```

---

*End of Quality Audit*
*Part of v4.0.0 Universal Skills Ecosystem*
*Methodology: Technical (How it's built)*
*Supports code quality and maintainability*
