# Implementation Executor Skill

## Purpose

Safely applies approved changes from plans, managing version control, rollback capability, and post-change verification.

## Execution Protocol

### Pre-Execution Checklist

```
[ ] Plan status is 'approved'
[ ] Backup created before execution
[ ] All affected artifacts identified
[ ] No conflicting changes in progress
[ ] User has confirmed execution
```

### Execution Workflow

```
1. Create pre-execution backup
2. Lock affected artifacts
3. Apply changes sequentially
4. Create version records
5. Verify changes applied correctly
6. Run consistency check
7. Update plan status to 'completed'
8. Unlock artifacts
```

## API Integration

```javascript
// Execute approved plan
POST /api/plans/:id/execute
{
  dry_run: false,           // Set true to preview without applying
  create_backup: true,      // Recommended: always true
  notify_on_complete: true  // Send notification when done
}

Response: {
  execution_id: 'exec-123',
  status: 'completed' | 'partial' | 'failed',
  changes_applied: [
    { artifact: 'path', version: 5, status: 'success' }
  ],
  backup_id: 'backup-123',
  consistency_check: { passed: true, issues: [] }
}
```

## Change Application

### File Modifications

```javascript
async function applyChange(change) {
  const { artifact_type, artifact_name, proposed_text, change_type } = change;

  // 1. Read current content
  const current = await readArtifact(artifact_type, artifact_name);

  // 2. Apply change based on type
  let newContent;
  switch (change_type) {
    case 'replace':
      newContent = proposed_text;
      break;
    case 'edit':
      newContent = applyEdit(current, change.location, proposed_text);
      break;
    case 'add':
      newContent = insertContent(current, change.location, proposed_text);
      break;
    case 'remove':
      newContent = removeContent(current, change.location);
      break;
  }

  // 3. Save with versioning
  await saveArtifact(artifact_type, artifact_name, newContent, {
    change_source: 'plan',
    change_plan_id: change.plan_id,
    change_summary: change.rationale
  });

  return { success: true, version: newVersion };
}
```

### Atomic Transactions

All changes in a plan are applied atomically:
- All succeed → Commit all changes
- Any fails → Rollback all changes

```javascript
async function executeAtomically(plan) {
  const transaction = await startTransaction();

  try {
    for (const change of plan.changes) {
      await applyChange(change, transaction);
    }

    await transaction.commit();
    return { status: 'completed' };

  } catch (error) {
    await transaction.rollback();
    return { status: 'failed', error: error.message };
  }
}
```

## Rollback Capability

### Automatic Rollback

Triggered when:
- Any change fails to apply
- Post-execution consistency check fails
- User cancels during execution

### Manual Rollback

```javascript
// Rollback specific execution
POST /api/executions/:id/rollback
{
  restore_backup: true
}

Response: {
  rolled_back: true,
  backup_restored: 'backup-123',
  artifacts_reverted: ['path1', 'path2']
}
```

## Post-Execution Verification

### Integrity Checks

```javascript
async function verifyExecution(execution) {
  const checks = [];

  // 1. File integrity
  for (const change of execution.changes_applied) {
    const content = await readArtifact(change.artifact);
    const expected = change.expected_hash;
    const actual = hash(content);

    checks.push({
      type: 'file_integrity',
      artifact: change.artifact,
      passed: expected === actual
    });
  }

  // 2. Consistency check
  const consistency = await runConsistencyCheck();
  checks.push({
    type: 'consistency',
    passed: consistency.issues.length === 0,
    issues: consistency.issues
  });

  // 3. Reference validation
  const refs = await validateReferences();
  checks.push({
    type: 'references',
    passed: refs.broken.length === 0,
    broken: refs.broken
  });

  return checks;
}
```

## Execution Status Tracking

### Status Values

| Status | Meaning |
|--------|---------|
| pending | Plan approved, awaiting execution |
| in_progress | Execution started |
| completed | All changes applied successfully |
| partial | Some changes applied, some failed |
| failed | Execution failed, rollback completed |
| rolled_back | User-initiated rollback completed |

### Execution Log

```javascript
db.exec(`
  CREATE TABLE IF NOT EXISTS execution_log (
    id INTEGER PRIMARY KEY,
    plan_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    started_at DATETIME,
    completed_at DATETIME,
    backup_id TEXT,
    changes_applied TEXT,  -- JSON array
    errors TEXT,           -- JSON array
    user_id INTEGER NOT NULL
  )
`);
```

## Safety Features

### Conflict Detection

Before execution, check for:
- Other executions in progress on same artifacts
- Unsaved changes in active editor sessions
- Recent modifications since plan creation

### Change Size Limits

```javascript
const LIMITS = {
  max_changes_per_plan: 50,
  max_file_size_change: 100000,  // 100KB
  max_total_changes_size: 500000  // 500KB
};
```

### Rate Limiting

- Maximum 1 execution per minute per user
- Maximum 10 executions per hour per plan
