---
name: you-sure
description: >
  Confirmation gate before destructive or complex operations. Pauses execution,
  summarizes what will happen, lists impacts, shows rollback options, and requires
  explicit user approval. Use when: destructive operations, complex changes, high-risk tasks.
---

# You-Sure Confirmation Gate

**Purpose:** Pause before potentially destructive/irreversible operations
**Type:** Learning Skill (Pre-Execution / Safety Gate)
**Origin:** "Measure twice, cut once" - construction wisdom

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Are you sure?"
- "Confirm this action"
- Before irreversible operations

**Context Indicators:**
- Destructive operations (delete, drop, truncate)
- Database migrations
- Deployment to production
- Mass file operations
- Breaking API changes
- Dependency major version upgrades

---

## Core Concept

**The Problem:**
- Claude executes without pausing
- No checkpoint before destructive operations
- User can't review plan before execution
- No chance to catch mistakes

**The Solution:**
- Mandatory pause before high-risk operations
- Clear summary of what will happen
- List of potential impacts
- Explicit user confirmation required
- Rollback options presented

**Article Quote:** *"you-sure (confirm before execution)"* - Fourth step in battle-plan

---

## You-Sure Process

### 1. Detect High-Risk Operations

```javascript
function isHighRisk(operation) {
  const destructivePatterns = [
    /delete/i,
    /drop/i,
    /truncate/i,
    /remove/i,
    /destroy/i,
    /migrate/i,
    /deploy/i,
    /publish/i,
    /--force/i,
    /recursive.*delete/i
  ];

  const highImpactIndicators = {
    production: operation.environment === 'production',
    database: operation.affects === 'database',
    multipleFiles: operation.fileCount > 10,
    userFacing: operation.userImpact === 'high',
    breakingChange: operation.breaking === true,
    irreversible: operation.reversible === false
  };

  const matchesDestructive = destructivePatterns.some(pattern =>
    pattern.test(operation.description)
  );

  const hasHighImpact = Object.values(highImpactIndicators).some(Boolean);

  return matchesDestructive || hasHighImpact;
}
```

### 2. Summarize Operation

```javascript
async function summarizeOperation(operation) {
  return {
    title: operation.description,
    category: categorizeOperation(operation),
    severity: assessSeverity(operation),
    whatWillHappen: describeActions(operation),
    whatWillChange: listChanges(operation),
    affectedEntities: identifyAffected(operation),
    timeToExecute: estimateTime(operation)
  };
}
```

**Example:**
```
Operation: Drop database table "old_users"

Category: Database (DESTRUCTIVE)
Severity: CRITICAL
Time to execute: < 1 second

What will happen:
1. Connect to database: production_db
2. Execute: DROP TABLE old_users CASCADE
3. Remove 45,312 user records permanently
4. Remove all foreign key relationships
5. Remove all indexes on this table

What will change:
- Database: production_db
  - Table: old_users (DELETED)
  - Dependent tables: sessions, preferences, logs (orphaned records)
  - Size reduction: 2.3 GB freed

Affected entities:
- Records: 45,312 users
- Dependencies: 3 tables with foreign keys
- Indexes: 7 indexes removed
- Application code: May have references to this table
```

### 3. List Potential Impacts

```javascript
async function identifyImpacts(operation) {
  return {
    immediate: [],     // Happens right away
    downstream: [],    // Cascading effects
    userFacing: [],    // Affects end users
    technical: [],     // Technical debt/issues
    business: []       // Business consequences
  };
}
```

**Example:**
```
Potential Impacts:

Immediate:
⚠️ 45,312 user records deleted (IRREVERSIBLE)
⚠️ Sessions table has 12,453 orphaned records
⚠️ Preferences table has 38,901 orphaned records

Downstream:
⚠️ Login system may fail for users with orphaned sessions
⚠️ Reports querying old_users table will break
⚠️ Admin dashboard may show errors
⚠️ Scheduled jobs referencing this table will fail

User-Facing:
🔴 CRITICAL: Active users may be logged out
🔴 CRITICAL: User preferences may be lost
⚠️ Support tickets may increase

Technical:
⚠️ Application code may reference old_users table (needs audit)
⚠️ Database backup size will change
⚠️ Replication lag may occur during deletion

Business:
⚠️ Historical user data lost (compliance issue?)
⚠️ Analytics reports will have gaps
⚠️ Audit trail incomplete
```

### 4. Show Rollback Options

```javascript
async function identifyRollbackOptions(operation) {
  return {
    available: true/false,
    methods: [],
    timeToRollback: "",
    dataLoss: true/false,
    requirements: []
  };
}
```

**Example:**
```
Rollback Options:

Option 1: Restore from backup
  - Availability: ✓ Available (last backup: 2 hours ago)
  - Time: 15-30 minutes
  - Data loss: ✓ YES - last 2 hours of data lost
  - Requirements:
    * Database access
    * Backup file: production_db_2026-02-04_08-00.sql
    * Downtime: Required (5-10 min)

Option 2: Recreate from archive
  - Availability: ✓ Available (if old_users was archived)
  - Time: 1-2 hours
  - Data loss: Depends on archive freshness
  - Requirements:
    * Archive system access
    * Table schema definition
    * Data validation after restore

Option 3: No rollback available
  - Availability: ✗ NOT AVAILABLE
  - This operation is IRREVERSIBLE if no backup exists
  - CRITICAL: Verify backup before proceeding
```

### 5. Highlight Risks from Pre-Mortem

```javascript
async function includePreMortemRisks(operation) {
  // If pre-mortem was run, include its findings
  const preMortem = await getPreMortem(operation.taskId);

  if (preMortem) {
    return {
      topRisks: preMortem.risks.slice(0, 5),
      preventions: preMortem.preventions,
      detections: preMortem.detections
    };
  }

  return null;
}
```

**Example:**
```
Known Risks (from pre-mortem):

Risk #1: Application breaks due to table references
  - Likelihood: 4/5 (HIGH)
  - Impact: 5/5 (CRITICAL)
  - Risk Score: 20 (CRITICAL)
  - Prevention: Audit all code for table references before dropping
  - Detection: Monitor error logs after operation
  - Mitigation: Have rollback ready

Risk #2: Orphaned records cause data integrity issues
  - Likelihood: 5/5 (CERTAIN)
  - Impact: 3/5 (MEDIUM)
  - Risk Score: 15 (HIGH)
  - Prevention: Clean up foreign key relationships first
  - Detection: Run data integrity checks
  - Mitigation: Script to clean orphaned records

Risk #3: Compliance violation (data retention)
  - Likelihood: 2/5 (LOW)
  - Impact: 5/5 (CRITICAL)
  - Risk Score: 10 (MEDIUM)
  - Prevention: Verify retention policy allows deletion
  - Detection: Audit trail check
  - Mitigation: Archive data before deletion
```

### 6. Require Explicit Confirmation

```javascript
async function requireConfirmation(summary, impacts, rollback, risks) {
  const confirmationPrompt = formatConfirmationPrompt({
    summary,
    impacts,
    rollback,
    risks
  });

  console.log(confirmationPrompt);
  console.log("\nType 'YES' to proceed, anything else to cancel:");

  const response = await getUserInput();

  if (response !== 'YES') {
    throw new Error("Operation cancelled by user");
  }

  // Additional confirmation for critical operations
  if (summary.severity === 'CRITICAL') {
    console.log("\nThis is a CRITICAL operation. Type 'I UNDERSTAND' to confirm:");
    const secondResponse = await getUserInput();

    if (secondResponse !== 'I UNDERSTAND') {
      throw new Error("Operation cancelled - critical confirmation not provided");
    }
  }

  return {confirmed: true, timestamp: new Date().toISOString()};
}
```

---

## Output Format

```
╔════════════════════════════════════════════════════════════════╗
║                    ⚠️  CONFIRMATION REQUIRED  ⚠️                ║
╚════════════════════════════════════════════════════════════════╝

Operation: Drop database table "old_users"
Category: Database (DESTRUCTIVE)
Severity: 🔴 CRITICAL
Environment: PRODUCTION

───────────────────────────────────────────────────────────────

WHAT WILL HAPPEN:

1. Connect to database: production_db
2. Execute: DROP TABLE old_users CASCADE
3. Delete 45,312 user records (PERMANENT)
4. Remove 7 indexes
5. Break 3 foreign key relationships

───────────────────────────────────────────────────────────────

POTENTIAL IMPACTS:

Immediate:
  ⚠️ 45,312 records deleted (IRREVERSIBLE)
  ⚠️ 51,354 orphaned records in dependent tables
  ⚠️ 2.3 GB disk space freed

Downstream:
  🔴 Login system may fail
  🔴 Reports will break
  ⚠️ Admin dashboard errors expected

User-Facing:
  🔴 CRITICAL: Active users may be logged out
  🔴 CRITICAL: Preferences lost

───────────────────────────────────────────────────────────────

ROLLBACK OPTIONS:

✓ Restore from backup (last backup: 2 hours ago)
  - Time: 15-30 minutes
  - Data loss: YES (last 2 hours)
  - Requires downtime

✗ NO OTHER OPTIONS - This is IRREVERSIBLE without backup

───────────────────────────────────────────────────────────────

KNOWN RISKS (from pre-mortem):

1. Application breaks (Risk Score: 20 - CRITICAL)
2. Orphaned records (Risk Score: 15 - HIGH)
3. Compliance violation (Risk Score: 10 - MEDIUM)

───────────────────────────────────────────────────────────────

SAFETY CHECKLIST:

Before proceeding, have you:
  [ ] Verified backup exists and is recent?
  [ ] Audited code for references to this table?
  [ ] Notified team of planned operation?
  [ ] Scheduled downtime window?
  [ ] Prepared rollback procedure?
  [ ] Verified compliance/retention policy?

───────────────────────────────────────────────────────────────

This operation cannot be undone without data loss.

Type 'YES' to proceed, anything else to cancel:
█
```

---

## Integration with Battle-Plan

**Position:** Phase 4 - After pre-mortem, before execution

**Flow:**
```
Battle-Plan:
├─ RUBBER-DUCK (clarified) ✓
├─ PATTERN-LIBRARY (checked) ✓
├─ PRE-MORTEM (risks identified) ✓
│
├─ YOU-SURE (you are here)
│  ├─ Summarize operation
│  ├─ List impacts
│  ├─ Show rollback options
│  ├─ Highlight pre-mortem risks
│  └─ Require confirmation
│
├─ [USER CONFIRMS OR CANCELS]
│
└─ EXECUTE (if confirmed) →
```

**Why Here:**
- After pre-mortem (so we know the risks)
- Before execution (last chance to abort)
- Gives user explicit control
- Prevents accidental destructive operations

---

## Severity Levels

```javascript
function assessSeverity(operation) {
  if (operation.environment === 'production' &&
      operation.affects === 'database' &&
      operation.reversible === false) {
    return 'CRITICAL';
  }

  if (operation.environment === 'production' ||
      operation.userImpact === 'high') {
    return 'HIGH';
  }

  if (operation.affects === 'multiple-files' ||
      operation.breakingChange) {
    return 'MEDIUM';
  }

  return 'LOW';
}
```

**Severity Thresholds:**
- **CRITICAL:** Requires double confirmation ("YES" + "I UNDERSTAND")
- **HIGH:** Requires single confirmation ("YES")
- **MEDIUM:** Warning displayed, optional confirmation
- **LOW:** Informational only, no confirmation

---

## Configuration

```json
{
  "youSure": {
    "enabled": true,
    "thresholds": {
      "critical": {
        "requireDoubleConfirmation": true,
        "triggers": [
          "production database operations",
          "mass deletions (>1000 records)",
          "breaking API changes"
        ]
      },
      "high": {
        "requireConfirmation": true,
        "triggers": [
          "production deployments",
          "database migrations",
          "file operations (>10 files)"
        ]
      },
      "medium": {
        "showWarning": true,
        "requireConfirmation": false
      }
    },
    "includePreMortemRisks": true,
    "requireSafetyChecklist": true
  }
}
```

---

## Common Confirmation Scenarios

### Database Operations
```
DROP TABLE, TRUNCATE, DELETE FROM, ALTER TABLE (breaking), DROP INDEX
→ Severity: CRITICAL (if production) / HIGH (if staging)
→ Confirmation: Double ("YES" + "I UNDERSTAND")
```

### File Operations
```
rm -rf, delete large directories, mass file modifications
→ Severity: HIGH (if >10 files) / MEDIUM (if <10 files)
→ Confirmation: Single ("YES")
```

### Deployments
```
Deploy to production, publish package, push to main
→ Severity: HIGH
→ Confirmation: Single ("YES")
```

### API Changes
```
Breaking API changes, deprecation, endpoint removal
→ Severity: HIGH (if user-facing) / MEDIUM (if internal)
→ Confirmation: Single ("YES")
```

### Dependency Updates
```
Major version upgrades, breaking dependency changes
→ Severity: MEDIUM
→ Confirmation: Optional (warning)
```

---

## Quick Reference

**Check if confirmation needed:**
```javascript
if (youSure.isRequired(operation)) {
  const confirmation = await youSure.confirm(operation);

  if (!confirmation.confirmed) {
    throw new Error("Operation cancelled by user");
  }
}
```

**Bypass confirmation (dangerous):**
```javascript
// Only for automated scripts with --force flag
if (operation.force && operation.nonInteractive) {
  console.log("⚠️ Force flag set - skipping confirmation");
  // Still log what would have been shown
  youSure.logWouldHaveConfirmed(operation);
}
```

---

## Benefits

**Prevents:**
- Accidental destructive operations
- Running wrong command in production
- Irreversible data loss
- Breaking changes without review

**Provides:**
- Explicit user control
- Clear understanding of impacts
- Rollback plan before execution
- Psychological pause to reconsider

**Enables:**
- Confident destructive operations
- Team awareness (show checklist)
- Audit trail (confirmation logged)
- Stress-free high-risk changes

---

*End of You-Sure*
*Part of v4.0.0 Universal Skills Ecosystem*
*Category: Learning / Pre-Execution (Safety Gate)*
*"Measure twice, cut once"*
