# Fix Coordinator for Multi-Methodology Convergence

**Document:** Fix Coordination Strategies
**Version:** 1.0.0
**Date:** 2026-02-12
**Status:** Design Specification

---

## Overview

The Fix Coordinator manages conflict detection and resolution when multiple methodologies identify issues at overlapping file locations. It determines whether fixes can be applied in parallel or must be applied sequentially, groups fixes intelligently, and ensures line-order preservation to prevent corruption.

---

## Core Responsibilities

1. **Conflict Detection** - Identify overlapping or conflicting fixes
2. **Strategy Selection** - Choose parallel vs sequential execution
3. **File Grouping** - Group fixes by file for efficient application
4. **Order Preservation** - Maintain line order to prevent corruption
5. **Verification** - Validate fixes after batch application
6. **Rollback** - Revert on failure

---

## Conflict Detection Algorithm

### Phase 1: Issue Classification

**Group issues by file and line range:**
```javascript
function classifyIssues(issues) {
  const byFile = new Map();

  for (const issue of issues) {
    if (!issue.file) continue;

    if (!byFile.has(issue.file)) {
      byFile.set(issue.file, []);
    }

    byFile.get(issue.file).push({
      ...issue,
      startLine: issue.line,
      endLine: issue.line + (issue.lineCount || 1) - 1
    });
  }

  return byFile;
}
```

### Phase 2: Overlap Detection

**Detect when issues affect overlapping lines:**
```javascript
function detectOverlaps(fileIssues) {
  const overlaps = [];

  // Sort by start line
  fileIssues.sort((a, b) => a.startLine - b.startLine);

  for (let i = 0; i < fileIssues.length - 1; i++) {
    for (let j = i + 1; j < fileIssues.length; j++) {
      const issue1 = fileIssues[i];
      const issue2 = fileIssues[j];

      // Check for overlap
      if (issue2.startLine <= issue1.endLine) {
        overlaps.push({
          issue1,
          issue2,
          type: determineOverlapType(issue1, issue2)
        });
      } else {
        // No more overlaps possible (sorted by start line)
        break;
      }
    }
  }

  return overlaps;
}

function determineOverlapType(issue1, issue2) {
  // Same exact line
  if (issue1.startLine === issue2.startLine &&
      issue1.endLine === issue2.endLine) {
    return 'exact';
  }

  // issue2 completely within issue1
  if (issue2.startLine >= issue1.startLine &&
      issue2.endLine <= issue1.endLine) {
    return 'contained';
  }

  // Partial overlap
  return 'partial';
}
```

### Phase 3: Conflict Classification

**Determine if overlaps are conflicts:**
```javascript
function classifyConflicts(overlaps) {
  const conflicts = [];
  const compatible = [];

  for (const overlap of overlaps) {
    const { issue1, issue2, type } = overlap;

    // Check if fixes are compatible
    const canMerge = canMergeFixes(issue1, issue2);

    if (!canMerge) {
      conflicts.push({
        ...overlap,
        resolution: determineResolution(issue1, issue2),
        reason: explainConflict(issue1, issue2)
      });
    } else {
      compatible.push({
        ...overlap,
        mergeStrategy: determineMergeStrategy(issue1, issue2)
      });
    }
  }

  return { conflicts, compatible };
}

function canMergeFixes(issue1, issue2) {
  // Same fix type at same location - compatible
  if (issue1.fixType === issue2.fixType) {
    return true;
  }

  // Read-only checks (no modifications) - compatible
  if (issue1.fixType === 'none' && issue2.fixType === 'none') {
    return true;
  }

  // Different fix types at same location - conflict
  if (issue1.fixType !== issue2.fixType) {
    return false;
  }

  return true;
}
```

---

## Parallel vs Sequential Strategy

### Decision Matrix

| Conflict Type | Strategy | Reason |
|--------------|----------|--------|
| No conflicts | Parallel | Safe - independent fixes |
| Read-only overlap | Parallel | Safe - no modifications |
| Same fix type | Parallel (merged) | Safe - mergeable fixes |
| Different fix types | Sequential | Unsafe - conflicting changes |
| Line order dependency | Sequential | Unsafe - order matters |
| Cross-file dependency | Parallel (different files) | Safe - file independence |

### Strategy Selection Algorithm

```javascript
function selectStrategy(issues, conflicts) {
  const strategy = {
    parallel: [],
    sequential: [],
    merged: []
  };

  // Group by file
  const byFile = classifyIssues(issues);

  for (const [file, fileIssues] of byFile) {
    // Detect conflicts within file
    const overlaps = detectOverlaps(fileIssues);
    const { conflicts: fileConflicts, compatible } =
      classifyConflicts(overlaps);

    if (fileConflicts.length === 0) {
      // No conflicts - can apply in parallel
      strategy.parallel.push({
        file,
        issues: fileIssues,
        method: 'batch'
      });
    } else {
      // Has conflicts - must apply sequentially
      strategy.sequential.push({
        file,
        issues: fileIssues,
        conflicts: fileConflicts,
        method: 'ordered'
      });
    }

    // Merge compatible overlaps
    if (compatible.length > 0) {
      strategy.merged.push({
        file,
        merges: compatible.map(c => ({
          issues: [c.issue1, c.issue2],
          strategy: c.mergeStrategy
        }))
      });
    }
  }

  return strategy;
}
```

### Execution Flow

```javascript
async function executeFixStrategy(strategy, projectPath) {
  const results = {
    parallel: { completed: 0, failed: 0 },
    sequential: { completed: 0, failed: 0 },
    merged: { completed: 0, failed: 0 }
  };

  // Step 1: Execute merged fixes (combine compatible issues)
  for (const merge of strategy.merged) {
    try {
      await executeMergedFixes(merge, projectPath);
      results.merged.completed++;
    } catch (error) {
      console.error(`Merge failed for ${merge.file}: ${error.message}`);
      results.merged.failed++;
    }
  }

  // Step 2: Execute parallel fixes (independent files)
  await executeParallelFixes(strategy.parallel, projectPath, results);

  // Step 3: Execute sequential fixes (conflicting issues)
  for (const sequential of strategy.sequential) {
    try {
      await executeSequentialFixes(sequential, projectPath);
      results.sequential.completed++;
    } catch (error) {
      console.error(`Sequential fix failed for ${sequential.file}: ${error.message}`);
      results.sequential.failed++;
    }
  }

  return results;
}
```

---

## File-Level Grouping Logic

### Grouping Strategy

```javascript
function groupIssuesByFile(issues) {
  const groups = new Map();

  for (const issue of issues) {
    const file = issue.file || 'unknown';

    if (!groups.has(file)) {
      groups.set(file, {
        file,
        issues: [],
        stats: {
          critical: 0,
          high: 0,
          medium: 0,
          low: 0
        }
      });
    }

    const group = groups.get(file);
    group.issues.push(issue);
    group.stats[issue.severity]++;
  }

  return Array.from(groups.values());
}
```

### Priority Ordering

```javascript
function prioritizeGroups(groups) {
  // Sort by:
  // 1. Critical count (descending)
  // 2. High count (descending)
  // 3. Total issues (descending)
  return groups.sort((a, b) => {
    if (a.stats.critical !== b.stats.critical) {
      return b.stats.critical - a.stats.critical;
    }
    if (a.stats.high !== b.stats.high) {
      return b.stats.high - a.stats.high;
    }
    return b.issues.length - a.issues.length;
  });
}
```

---

## Line-Order Preservation

### Problem Statement

When applying multiple fixes to the same file, line numbers shift as edits are made. Applying fixes in arbitrary order can corrupt the file.

**Example:**
```javascript
// Original file (lines 1-5)
1: function calculateTotal(items) {
2:   let total = 0;
3:   for (let item of items) {
4:     total += item.price;
5:   }
6:   return total;
7: }

// Issues found:
Issue 1: Line 2 - Replace 'let' with 'const'
Issue 2: Line 4 - Add null check
Issue 3: Line 6 - Add JSDoc comment

// WRONG ORDER (line 2, then 4, then 6):
// After fix 1 (line 2): Lines shift if multiline
// After fix 2 (line 4): Now fixing WRONG line!
// After fix 3 (line 6): Now fixing WRONG line!

// CORRECT ORDER (line 6, then 4, then 2):
// After fix 3 (line 6): Lines 1-5 unchanged
// After fix 2 (line 4): Lines 1-3 unchanged
// After fix 1 (line 2): Lines 1 unchanged
```

### Solution: Bottom-Up Application

```javascript
function preserveLineOrder(fileIssues) {
  // Sort by line number DESCENDING
  // Apply from bottom to top
  return fileIssues.sort((a, b) => {
    // Primary: start line (descending)
    if (a.startLine !== b.startLine) {
      return b.startLine - a.startLine;
    }

    // Secondary: end line (descending)
    // For overlapping ranges, apply larger range first
    return b.endLine - a.endLine;
  });
}
```

### Application Algorithm

```javascript
async function applyFixesBottomUp(file, issues, projectPath) {
  // Sort bottom-up
  const ordered = preserveLineOrder(issues);

  // Read original file
  const content = await fs.readFile(
    path.join(projectPath, file),
    'utf8'
  );

  let lines = content.split('\n');

  // Apply fixes from bottom to top
  for (const issue of ordered) {
    try {
      lines = await applyFix(lines, issue);
    } catch (error) {
      console.error(`Fix failed for ${file}:${issue.startLine}: ${error.message}`);
      throw error;
    }
  }

  // Write updated file
  await fs.writeFile(
    path.join(projectPath, file),
    lines.join('\n'),
    'utf8'
  );

  return {
    file,
    fixesApplied: ordered.length
  };
}
```

---

## Conflict Scenarios (Examples)

### Scenario 1: Exact Overlap - Same Line

**Issues:**
```javascript
Issue A: Line 42 - Security: Escape user input
Issue B: Line 42 - Quality: Extract to variable
```

**Analysis:**
- Both modify line 42
- Different fix types (escape vs extract)
- **Conflict Type:** Incompatible

**Resolution:**
```javascript
{
  strategy: 'sequential',
  order: ['security', 'quality'],  // Security first (higher priority)
  reason: 'Different fix types at same location'
}
```

### Scenario 2: Partial Overlap - Adjacent Lines

**Issues:**
```javascript
Issue A: Lines 10-15 - Refactor function
Issue B: Line 12 - Fix typo in comment
```

**Analysis:**
- Issue B within Issue A's range
- Compatible (comment fix doesn't affect refactor)
- **Conflict Type:** Compatible overlap

**Resolution:**
```javascript
{
  strategy: 'merged',
  method: 'apply-both-sequentially',
  order: ['refactor', 'typo'],  // Refactor first, then typo
  reason: 'Typo fix preserves through refactor'
}
```

### Scenario 3: No Overlap - Different Lines

**Issues:**
```javascript
Issue A: Line 10 - Add null check
Issue B: Line 50 - Fix SQL injection
Issue C: Line 100 - Update deprecated API
```

**Analysis:**
- No line overlap
- Independent changes
- **Conflict Type:** None

**Resolution:**
```javascript
{
  strategy: 'parallel',
  method: 'batch-apply-bottom-up',
  order: [100, 50, 10],  // Bottom to top
  reason: 'Independent non-overlapping fixes'
}
```

### Scenario 4: Cross-File Dependencies

**Issues:**
```javascript
Issue A: api/users.js:42 - Update function signature
Issue B: components/UserList.js:15 - Update function call
```

**Analysis:**
- Different files
- Logical dependency (call depends on signature)
- **Conflict Type:** Cross-file dependency

**Resolution:**
```javascript
{
  strategy: 'sequential-cross-file',
  order: ['api/users.js', 'components/UserList.js'],
  reason: 'Caller must be updated after callee'
}
```

---

## Verification After Batch Fixes

### Verification Levels

**Level 1: Syntax Check**
```javascript
async function verifySyntax(file, projectPath) {
  const ext = path.extname(file);

  if (ext === '.js' || ext === '.ts') {
    // Parse as JavaScript/TypeScript
    const content = await fs.readFile(
      path.join(projectPath, file),
      'utf8'
    );

    try {
      // Use babel or typescript parser
      await parse(content, { sourceType: 'module' });
      return { valid: true };
    } catch (error) {
      return {
        valid: false,
        error: error.message,
        line: error.loc?.line
      };
    }
  }

  return { valid: true, skipped: 'No parser for extension' };
}
```

**Level 2: Lint Check**
```javascript
async function verifyLinting(file, projectPath) {
  // Use execFileNoThrow for safe command execution
  import { execFileNoThrow } from '../utils/execFileNoThrow.js';

  const result = await execFileNoThrow('eslint', [file], {
    cwd: projectPath
  });

  if (result.status !== 0) {
    return {
      valid: false,
      errors: parseEslintOutput(result.stdout)
    };
  }

  return { valid: true };
}
```

**Level 3: Test Execution**
```javascript
async function verifyTests(projectPath) {
  // Use execFileNoThrow for safe command execution
  import { execFileNoThrow } from '../utils/execFileNoThrow.js';

  const result = await execFileNoThrow('npm', ['test'], {
    cwd: projectPath,
    timeout: 300000
  });

  return {
    valid: result.status === 0,
    passed: parseTestResults(result.stdout).passed,
    failed: parseTestResults(result.stdout).failed
  };
}
```

### Verification Workflow

```javascript
async function verifyBatchFixes(files, projectPath) {
  const verification = {
    syntax: { passed: 0, failed: 0 },
    linting: { passed: 0, failed: 0 },
    tests: { passed: false }
  };

  // Level 1: Syntax
  for (const file of files) {
    const syntaxCheck = await verifySyntax(file, projectPath);

    if (syntaxCheck.valid) {
      verification.syntax.passed++;
    } else {
      verification.syntax.failed++;
      console.error(`Syntax error in ${file}:${syntaxCheck.line}`);
      console.error(syntaxCheck.error);
    }
  }

  if (verification.syntax.failed > 0) {
    return { ...verification, status: 'failed', level: 'syntax' };
  }

  // Level 2: Linting
  for (const file of files) {
    const lintCheck = await verifyLinting(file, projectPath);

    if (lintCheck.valid) {
      verification.linting.passed++;
    } else {
      verification.linting.failed++;
      console.warn(`Linting errors in ${file}:`, lintCheck.errors);
    }
  }

  // Level 3: Tests
  const testResults = await verifyTests(projectPath);
  verification.tests = testResults;

  if (!testResults.valid) {
    return { ...verification, status: 'tests-failed', level: 'tests' };
  }

  return { ...verification, status: 'passed' };
}
```

---

## Integration with detect-infinite-loop

### Loop Detection at Fix Level

```javascript
async function applyFixWithLoopDetection(issue, loopDetector) {
  // Generate signature for this fix
  const signature = `${issue.file}:${issue.line}:${issue.type}`;

  // Check if we've tried this fix before
  loopDetector.recordAttempt(signature);

  if (loopDetector.isStuck(signature)) {
    console.warn(`Infinite loop detected for fix: ${signature}`);
    console.warn(`Attempted ${loopDetector.count(signature)} times`);

    // Generate alternative approach
    const alternative = await generateAlternativeFix(issue);

    if (alternative) {
      console.log('Trying alternative approach...');
      return await applyFix(alternative);
    } else {
      console.error('No alternative available, skipping fix');
      return { success: false, reason: 'infinite-loop' };
    }
  }

  // Apply fix normally
  return await applyFix(issue);
}
```

### Alternative Fix Generation

```javascript
async function generateAlternativeFix(issue) {
  const alternatives = {
    'sql-injection': [
      'use-parameterized-queries',
      'use-orm',
      'use-query-builder',
      'manual-escaping'
    ],

    'xss-vulnerability': [
      'use-escape-function',
      'use-sanitize-library',
      'use-template-engine',
      'manual-encoding'
    ],

    'broken-link': [
      'find-similar-file',
      'search-git-history',
      'ask-user',
      'remove-link'
    ]
  };

  const currentStrategy = issue.fixStrategy;
  const availableStrategies = alternatives[issue.type] || [];

  // Find next strategy
  const currentIndex = availableStrategies.indexOf(currentStrategy);
  const nextIndex = currentIndex + 1;

  if (nextIndex >= availableStrategies.length) {
    return null;  // No more alternatives
  }

  return {
    ...issue,
    fixStrategy: availableStrategies[nextIndex]
  };
}
```

---

## Performance Metrics

### Tracking Coordination Overhead

```javascript
const metrics = {
  conflictDetection: {
    duration: 0,      // Time spent detecting conflicts
    conflictsFound: 0 // Number of conflicts detected
  },

  strategySelection: {
    duration: 0,      // Time spent selecting strategy
    parallel: 0,      // Fixes applied in parallel
    sequential: 0,    // Fixes applied sequentially
    merged: 0         // Fixes merged
  },

  fixApplication: {
    duration: 0,      // Time spent applying fixes
    successful: 0,    // Successful applications
    failed: 0         // Failed applications
  },

  verification: {
    duration: 0,      // Time spent verifying
    passed: 0,        // Files that passed verification
    failed: 0         // Files that failed verification
  }
};
```

### Example Metrics Report

```
Fix Coordination Metrics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Conflict Detection:
  Duration: 2.3s
  Conflicts Found: 12
  Files Affected: 8

Strategy Selection:
  Duration: 0.8s
  Parallel: 35 fixes (73%)
  Sequential: 8 fixes (17%)
  Merged: 5 fixes (10%)

Fix Application:
  Duration: 18.5s
  Successful: 47/48 (98%)
  Failed: 1/48 (2%)

Verification:
  Duration: 12.2s
  Syntax: 48/48 passed (100%)
  Linting: 46/48 passed (96%)
  Tests: 142/142 passed (100%)

Total Duration: 33.8s
Overall Success Rate: 98%
```

---

## Rollback Strategies

### Backup Before Coordination

```javascript
async function createCoordinationBackup(files, projectPath) {
  const timestamp = Date.now();
  const backupPath = path.join(
    projectPath,
    '.corpus',
    'backups',
    `coordination-${timestamp}`
  );

  await mkdir(backupPath, { recursive: true });

  for (const file of files) {
    const source = path.join(projectPath, file);
    const dest = path.join(backupPath, file);

    await mkdir(path.dirname(dest), { recursive: true });
    await copyFile(source, dest);
  }

  return backupPath;
}
```

### Selective Rollback

```javascript
async function rollbackFailedFixes(failures, backupPath, projectPath) {
  console.log(`Rolling back ${failures.length} failed fixes...`);

  for (const failure of failures) {
    const file = failure.file;
    const backupFile = path.join(backupPath, file);
    const targetFile = path.join(projectPath, file);

    try {
      await copyFile(backupFile, targetFile);
      console.log(`  ✓ Rolled back ${file}`);
    } catch (error) {
      console.error(`  ✗ Failed to rollback ${file}: ${error.message}`);
    }
  }
}
```

### Complete Rollback

```javascript
async function rollbackAll(backupPath, projectPath) {
  console.log('Rolling back all fixes...');

  const files = await findFiles(backupPath);

  for (const file of files) {
    const relativePath = path.relative(backupPath, file);
    const targetPath = path.join(projectPath, relativePath);

    await copyFile(file, targetPath);
  }

  console.log(`✓ Rolled back from ${backupPath}`);
}
```

---

## Decision Flowchart

```
┌─────────────────────┐
│  Issues Found       │
│  (from methodologies)│
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Group by File       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Detect Overlaps     │
│ (line ranges)       │
└──────────┬──────────┘
           │
           ▼
     ┌────┴────┐
     │ Overlaps?│
     └────┬────┘
          │
    ┌─────┴─────┐
    │           │
   Yes         No
    │           │
    ▼           ▼
┌────────┐  ┌──────────┐
│Classify│  │ Parallel │
│Conflict│  │ Strategy │
└───┬────┘  └────┬─────┘
    │            │
    ▼            │
┌────────────┐   │
│Compatible? │   │
└───┬────────┘   │
    │            │
┌───┴───┐        │
│       │        │
Yes    No        │
│       │        │
▼       ▼        │
┌────┐ ┌────┐   │
│Merge││Seq.│   │
└──┬─┘ └─┬──┘   │
   │     │      │
   └──┬──┴──────┘
      │
      ▼
┌─────────────────┐
│ Create Backup   │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Apply Fixes     │
│ (bottom-up)     │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Verify Results  │
└──────┬──────────┘
       │
   ┌───┴───┐
   │Success?│
   └───┬───┘
       │
   ┌───┴───┐
   │       │
  Yes     No
   │       │
   ▼       ▼
┌────┐ ┌────────┐
│Done│ │Rollback│
└────┘ └────────┘
```

---

## References

**Related Documentation:**
- `SKILL.md` - Main convergence skill
- `parallel-executor.md` - Parallel execution architecture
- `core/audit/fix-planner/SKILL.md` - Fix planning strategies
- `core/learning/during-execution/detect-infinite-loop/SKILL.md` - Loop detection

**Configuration:**
- `corpus-config.json` - Convergence settings

---

*Document Version: 1.0.0*
*Created: 2026-02-12*
*Part of v4.0 Universal Skills Ecosystem*
*Category: Learning / Convergence / Coordination*
