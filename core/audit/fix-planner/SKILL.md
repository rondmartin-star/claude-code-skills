---
name: fix-planner
description: >
  Generate and implement fix plans for audit issues. Groups related issues, creates
  actionable strategies, implements fixes, verifies results. Use during: convergence
  workflow, automated issue resolution, or manual fix planning.
---

# Fix Planner

**Purpose:** Generate and execute fix plans for audit issues
**Size:** ~14 KB
**Type:** Core Pattern (Universal)

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Plan fixes for these issues"
- "Generate fix strategy"
- "Implement audit fixes"
- "Resolve audit issues"

**Context Indicators:**
- During convergence automated phase
- After audit discovers issues
- Manual fix planning needed
- Batch issue resolution

## ❌ DO NOT LOAD WHEN

- Just running audits (use audit-orchestrator)
- Checking status (use corpus-detect)
- No issues to fix

---

## Fix Planning Workflow

### Step 1: Issue Analysis

**Group issues by category and severity:**
```javascript
function analyzeIssues(auditResults) {
  const grouped = {
    critical: [],
    high: [],
    medium: [],
    low: [],
    info: []
  };

  auditResults.forEach(result => {
    result.issues.forEach(issue => {
      grouped[issue.severity].push({
        ...issue,
        audit_type: result.audit_type,
        auto_fixable: issue.auto_fixable || false
      });
    });
  });

  return grouped;
}
```

**Identify dependencies between fixes:**
```javascript
function findDependencies(issues) {
  const dependencies = [];

  // Example: Fix broken links before checking orphaned pages
  const brokenLinks = issues.filter(i => i.category === 'broken_link');
  const orphanedPages = issues.filter(i => i.category === 'orphaned_page');

  if (brokenLinks.length > 0 && orphanedPages.length > 0) {
    dependencies.push({
      first: 'broken_link',
      then: 'orphaned_page',
      reason: 'Fixing links may resolve orphaned pages'
    });
  }

  return dependencies;
}
```

### Step 2: Fix Strategy Generation

**Generate strategy for each issue type:**
```javascript
const fixStrategies = {
  // Navigation issues
  broken_link: {
    auto_fixable: true,
    strategy: 'find-similar',
    steps: [
      'Search for similar filenames',
      'Check if file was renamed',
      'Update link to correct path'
    ],
    requires_backup: true
  },

  orphaned_page: {
    auto_fixable: false,
    strategy: 'user-decision',
    steps: [
      'Analyze page content',
      'Suggest parent pages',
      'Present options: link, delete, or index'
    ],
    requires_approval: true
  },

  // Security issues
  sql_injection: {
    auto_fixable: true,
    strategy: 'use-parameterized',
    steps: [
      'Identify vulnerable query',
      'Convert to parameterized query',
      'Update variable binding',
      'Verify query still works'
    ],
    requires_testing: true
  },

  xss_vulnerability: {
    auto_fixable: true,
    strategy: 'escape-output',
    steps: [
      'Identify unescaped output',
      'Apply escapeHtml function',
      'Verify rendering correct'
    ],
    requires_testing: true
  },

  // Consistency issues
  term_mismatch: {
    auto_fixable: true,
    strategy: 'replace-with-canonical',
    steps: [
      'Get canonical term',
      'Find all instances of variant',
      'Replace with canonical',
      'Update consistency index'
    ],
    requires_verification: true
  },

  // Quality issues
  dead_code: {
    auto_fixable: true,
    strategy: 'safe-remove',
    steps: [
      'Verify code truly unused',
      'Check for dynamic references',
      'Remove if safe',
      'Run tests to confirm'
    ],
    requires_testing: true
  }
};
```

### Step 3: Create Fix Plan

**Generate ordered fix plan:**
```javascript
async function createFixPlan(issues, strategies) {
  const plan = {
    total_issues: issues.length,
    auto_fixable: issues.filter(i => i.auto_fixable).length,
    manual_fixes: issues.filter(i => !i.auto_fixable).length,
    estimated_time: estimateTime(issues),
    phases: []
  };

  // Phase 1: Auto-fixable critical issues
  const criticalAuto = issues.filter(i =>
    i.severity === 'critical' && i.auto_fixable
  );

  if (criticalAuto.length > 0) {
    plan.phases.push({
      name: 'Critical Auto-Fixes',
      issues: criticalAuto,
      can_automate: true,
      requires_approval: false
    });
  }

  // Phase 2: Auto-fixable high issues
  const highAuto = issues.filter(i =>
    i.severity === 'high' && i.auto_fixable
  );

  if (highAuto.length > 0) {
    plan.phases.push({
      name: 'High Priority Auto-Fixes',
      issues: highAuto,
      can_automate: true,
      requires_approval: false
    });
  }

  // Phase 3: Manual critical/high issues
  const manual = issues.filter(i =>
    !i.auto_fixable && (i.severity === 'critical' || i.severity === 'high')
  );

  if (manual.length > 0) {
    plan.phases.push({
      name: 'Manual High-Priority Fixes',
      issues: manual,
      can_automate: false,
      requires_approval: true
    });
  }

  // Phase 4: Medium/low auto-fixes
  const remaining = issues.filter(i =>
    i.auto_fixable && (i.severity === 'medium' || i.severity === 'low')
  );

  if (remaining.length > 0) {
    plan.phases.push({
      name: 'Remaining Auto-Fixes',
      issues: remaining,
      can_automate: true,
      requires_approval: false
    });
  }

  return plan;
}
```

### Step 4: Backup Before Fixes

**Create backup before implementing:**
```javascript
async function backupBeforeFixes(projectPath, plan) {
  const timestamp = new Date().toISOString().replace(/:/g, '-');
  const backupPath = path.join(
    projectPath,
    '.corpus',
    'backups',
    `pre-fixes-${timestamp}`
  );

  // Identify affected files
  const affectedFiles = new Set();
  plan.phases.forEach(phase => {
    phase.issues.forEach(issue => {
      if (issue.location) {
        const file = issue.location.split(':')[0];
        affectedFiles.add(file);
      }
    });
  });

  // Backup affected files
  await mkdir(backupPath, { recursive: true });

  for (const file of affectedFiles) {
    const sourcePath = path.join(projectPath, file);
    const destPath = path.join(backupPath, file);

    await mkdir(path.dirname(destPath), { recursive: true });
    await copyFile(sourcePath, destPath);
  }

  console.log(`✓ Backup created: ${backupPath}`);
  console.log(`  Files backed up: ${affectedFiles.size}`);

  return backupPath;
}
```

### Step 5: Implement Fixes

**Execute fix plan phase by phase:**
```javascript
async function implementFixPlan(projectPath, plan) {
  const results = {
    successful: 0,
    failed: 0,
    skipped: 0,
    details: []
  };

  for (const phase of plan.phases) {
    console.log(`\nPhase: ${phase.name}`);
    console.log(`  Issues: ${phase.issues.length}`);

    if (phase.requires_approval) {
      const approved = await promptUser(
        `Approve ${phase.name}? (${phase.issues.length} issues)`
      );

      if (!approved) {
        results.skipped += phase.issues.length;
        continue;
      }
    }

    for (const issue of phase.issues) {
      try {
        const result = await implementFix(projectPath, issue);

        if (result.success) {
          results.successful++;
          console.log(`  ✓ Fixed: ${issue.message}`);
        } else {
          results.failed++;
          console.log(`  ✗ Failed: ${issue.message}`);
          console.log(`    Reason: ${result.error}`);
        }

        results.details.push(result);
      } catch (error) {
        results.failed++;
        console.error(`  ✗ Error fixing: ${issue.message}`);
        console.error(`    ${error.message}`);
      }
    }
  }

  return results;
}
```

### Step 6: Fix Implementation Strategies

**Broken Link Fix:**
```javascript
async function fixBrokenLink(projectPath, issue) {
  const [filePath, lineNum] = issue.location.split(':');
  const targetPath = issue.link;

  // Find similar files
  const similarFiles = await findSimilarFiles(projectPath, targetPath);

  if (similarFiles.length === 0) {
    return { success: false, error: 'No similar files found' };
  }

  if (similarFiles.length === 1) {
    // Auto-fix: Update link
    await updateLink(filePath, lineNum, targetPath, similarFiles[0]);
    return { success: true, fix: similarFiles[0] };
  }

  // Multiple matches: Ask user
  const choice = await promptUser(
    `Which file should ${targetPath} link to?`,
    similarFiles
  );

  await updateLink(filePath, lineNum, targetPath, choice);
  return { success: true, fix: choice };
}
```

**SQL Injection Fix:**
```javascript
async function fixSQLInjection(projectPath, issue) {
  const [filePath, lineNum] = issue.location.split(':');

  // Read file
  const content = await fs.readFile(
    path.join(projectPath, filePath),
    'utf8'
  );

  const lines = content.split('\n');
  const vulnerableLine = lines[parseInt(lineNum) - 1];

  // Detect query pattern
  const queryMatch = vulnerableLine.match(/db\.query\s*\(\s*`([^`]+)`/);

  if (!queryMatch) {
    return { success: false, error: 'Could not parse query' };
  }

  // Convert to parameterized
  const originalQuery = queryMatch[1];
  const { parameterizedQuery, params } = convertToParameterized(originalQuery);

  // Replace line
  lines[parseInt(lineNum) - 1] = vulnerableLine.replace(
    queryMatch[0],
    `db.query(${parameterizedQuery}, ${params})`
  );

  // Write file
  await fs.writeFile(
    path.join(projectPath, filePath),
    lines.join('\n'),
    'utf8'
  );

  return { success: true, fix: 'Converted to parameterized query' };
}
```

**Term Consistency Fix:**
```javascript
async function fixTermMismatch(projectPath, issue) {
  const canonical = issue.canonical_term;
  const variant = issue.found_term;

  // Find all instances
  const files = await grepFiles(projectPath, variant);

  let replacements = 0;

  for (const file of files) {
    const content = await fs.readFile(file, 'utf8');
    const updated = content.replace(
      new RegExp(variant, 'g'),
      canonical
    );

    if (updated !== content) {
      await fs.writeFile(file, updated, 'utf8');
      replacements++;
    }
  }

  return {
    success: true,
    fix: `Replaced ${replacements} instances of '${variant}' with '${canonical}'`
  };
}
```

### Step 7: Verification

**Verify fixes resolved issues:**
```javascript
async function verifyFixes(projectPath, originalIssues, fixResults) {
  console.log('\nVerifying fixes...');

  // Re-run audits
  const reaudit = await runAudits(projectPath);

  // Compare issue counts
  const before = originalIssues.length;
  const after = reaudit.issues.length;
  const fixed = before - after;

  console.log(`Issues before: ${before}`);
  console.log(`Issues after: ${after}`);
  console.log(`Issues fixed: ${fixed}`);

  // Check for regressions
  const regressions = findRegressions(originalIssues, reaudit.issues);

  if (regressions.length > 0) {
    console.warn(`\n⚠️  ${regressions.length} new issues introduced:`);
    regressions.forEach(issue => {
      console.warn(`  - ${issue.message} (${issue.location})`);
    });
  }

  return {
    fixed,
    remaining: after,
    regressions: regressions.length
  };
}
```

### Step 8: Rollback if Needed

**Rollback on verification failure:**
```javascript
async function rollbackFixes(projectPath, backupPath) {
  console.log('\nRolling back fixes...');

  const files = await findFiles(backupPath);

  for (const file of files) {
    const relativePath = path.relative(backupPath, file);
    const targetPath = path.join(projectPath, relativePath);

    await copyFile(file, targetPath);
  }

  console.log('✓ Rollback complete');
  console.log(`  Restored from: ${backupPath}`);
}
```

---

## Fix Plan Output Format

```json
{
  "plan_id": "fp-2026-01-31-001",
  "created_at": "2026-01-31T10:00:00Z",
  "total_issues": 47,
  "auto_fixable": 38,
  "manual_fixes": 9,
  "estimated_time": "15-25 minutes",

  "phases": [
    {
      "name": "Critical Auto-Fixes",
      "issues": [
        {
          "severity": "critical",
          "category": "sql_injection",
          "location": "src/api/users.js:42",
          "message": "SQL injection vulnerability",
          "strategy": "use-parameterized",
          "auto_fixable": true
        }
      ],
      "can_automate": true,
      "requires_approval": false
    }
  ],

  "execution_results": {
    "successful": 38,
    "failed": 0,
    "skipped": 9,
    "backup_path": ".corpus/backups/pre-fixes-2026-01-31",
    "verification": {
      "issues_fixed": 38,
      "issues_remaining": 9,
      "regressions": 0
    }
  }
}
```

---

## Integration with Convergence

**Called by convergence-engine during automated phase:**
```javascript
// convergence-engine.js
async function runAutomatedConvergence() {
  let iteration = 0;
  let cleanPasses = 0;

  while (cleanPasses < 3 && iteration < maxIterations) {
    // Run audits
    const auditResults = await runAudits();

    if (auditResults.issues.length === 0) {
      cleanPasses++;
      continue;
    }

    // Generate and execute fix plan
    const plan = await createFixPlan(auditResults.issues);
    const backup = await backupBeforeFixes(projectPath, plan);
    const results = await implementFixPlan(projectPath, plan);

    // Verify
    const verification = await verifyFixes(
      projectPath,
      auditResults.issues,
      results
    );

    if (verification.regressions > 0) {
      // Rollback on regressions
      await rollbackFixes(projectPath, backup);
      console.error('Fixes introduced regressions, rolled back');
      break;
    }

    iteration++;
  }
}
```

---

## Quick Reference

**Create fix plan:**
```javascript
const plan = await createFixPlan(auditIssues);
```

**Execute plan:**
```javascript
const results = await implementFixPlan(projectPath, plan);
```

**Verify fixes:**
```javascript
const verification = await verifyFixes(projectPath, originalIssues, results);
```

**Rollback:**
```javascript
await rollbackFixes(projectPath, backupPath);
```

---

*End of Fix Planner*
*Part of v4.0.0 Universal Skills Ecosystem*
*Essential component of convergence workflow*
