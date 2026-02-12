# Complexity Assessment and Battle-Plan Integration

**Purpose:** Detailed guide for assessing audit operation complexity and routing through battle-plan

---

## Complexity Assessment for Audit Operations

**Before routing, assess complexity to determine if battle-plan workflow is needed:**

```javascript
function assessAuditComplexity(operation, context) {
  const complexityIndicators = {
    trivial: [
      operation === 'single-audit' && context.readOnly === true,
      context.auditCount === 1 && context.expectNoIssues === true
    ],
    simple: [
      operation === 'single-audit' && context.auditCount === 1,
      operation === 'quick-check',
      context.reportOnly === true
    ],
    medium: [
      operation === 'audit-all' && context.convergence === false,
      operation === 'multi-audit' && context.auditCount <= 3,
      operation === 'fix-issues' && context.issueCount < 10
    ],
    complex: [
      operation === 'convergence',
      operation === 'pre-release',
      operation === 'audit-all' && context.convergence === true,
      operation === 'fix-issues' && context.issueCount >= 10,
      context.multipleMethodologies === true,
      context.requiresGATE === true
    ]
  };

  // Check from complex → trivial
  for (const level of ['complex', 'medium', 'simple', 'trivial']) {
    const matches = complexityIndicators[level].filter(indicator => indicator === true);
    if (matches.length > 0) {
      return {
        level,
        useBattlePlan: (level === 'medium' || level === 'complex'),
        confidence: matches.length / complexityIndicators[level].length
      };
    }
  }

  // Default to medium
  return { level: 'medium', useBattlePlan: true, confidence: 0.5 };
}
```

---

## Complexity Examples

| Operation | Complexity | Use Battle-Plan? | Reason |
|-----------|------------|------------------|--------|
| Single security audit (read-only) | Trivial | No | One audit, no fixes |
| Quick quality check | Simple | No | Fast diagnostic |
| Audit all (single-run) | Medium | Yes | Multiple audits, planning |
| Fix 15 issues | Medium | Yes | Multi-step fixes, risks |
| Convergence (3-3-1 GATE) | Complex | Yes | Iterative, GATE, risks |
| Pre-release validation | Complex | Yes | Critical, comprehensive |

---

## Battle-Plan Integration

```javascript
async function routeAuditWithComplexity(operation, context) {
  const complexity = assessAuditComplexity(operation, context);

  if (!complexity.useBattlePlan) {
    // Trivial or simple - execute directly
    console.log(`${complexity.level} audit - executing directly`);
    return { skill: getSkillForOperation(operation), battlePlan: null };
  }

  // Medium or complex - use audit-battle-plan
  console.log(`${complexity.level} audit - using audit-battle-plan`);
  return {
    skill: getSkillForOperation(operation),
    battlePlan: 'audit-battle-plan',
    complexity: complexity.level
  };
}
```

---

## Battle-Plan Monitoring

During execution, battle-plan monitoring is active:

```javascript
{
  monitoring: {
    'verify-evidence': {
      enabled: true,
      checkpoints: [],
      passedCount: 0,
      failedCount: 0
    },
    'detect-infinite-loop': {
      enabled: true,
      loopsDetected: 0,
      pivotActions: []
    },
    'manage-context': {
      enabled: true,
      chunkingOccurred: false,
      contextUsage: []
    }
  }
}
```

---

## Configuration

### corpus-config.json

```json
{
  "audit_config": {
    "battle_plan": {
      "enabled": true,
      "variant": "audit-battle-plan",
      "use_for_convergence": true,
      "use_for_multi_audit": true,
      "complexity_threshold": "medium"
    },
    "convergence": {
      "use_monitoring": {
        "verify_evidence": true,
        "detect_infinite_loop": true,
        "manage_context": true
      }
    }
  }
}
```

---

## Example: Battle-Plan Workflow

```
User: "Run convergence audit for pre-release"

Complexity Assessment:
  - Operation: convergence
  - Level: COMPLEX
  - Use battle-plan: YES
  - Reason: Critical pre-release validation

═══ AUDIT BATTLE-PLAN ═══
Complexity: complex
Target: convergence-engine
Operation: pre-release validation

PHASE 2: KNOWLEDGE CHECK
  ✓ Found 45 fix patterns in library
  ✓ Found pattern: eslint-auto-fix (124 applications, 96% success)
  ⚠️ Antipattern: fix-symptom-not-cause (8 occurrences)

PHASE 3: PRE-MORTEM
  Risk #1: Fixes break functionality (likelihood: 4, impact: 5)
    Prevention: Run tests after each fix
  Risk #2: GATE doesn't converge (likelihood: 3, impact: 4)
    Prevention: detect-infinite-loop, fix root causes
  Recommendation: GO WITH CAUTION

PHASE 4: CONFIRMATION
  About to run convergence with 7 audit types
  Will implement fixes automatically
  Proceed? [Y/n] → YES

PHASE 5: EXECUTION (with full monitoring)
  [Convergence runs with monitoring enabled]

PHASE 7: DECLARE COMPLETE
  Requirements Met: ✓ SHIPPABLE
  - Core: 5/5 (100%)
  - Important: 4/4 (100%)

PHASE 8: PATTERN UPDATE
  New patterns saved: 3
  Updated patterns: 5
  Antipatterns updated: 1
```

---

*End of Complexity Assessment Reference*
*Part of audit-orchestrator v4.0*
