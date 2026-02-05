---
name: audit-battle-plan
description: >
  Battle-plan variant for audit operations (running audits, fixing issues, convergence).
  Specializes master battle-plan with audit-specific fix patterns, common issue antipatterns,
  and convergence monitoring. Use when: running audits, fixing issues, convergence-engine.
---

# Audit Battle-Plan

**Purpose:** Learning-first workflow for audit and fix operations
**Type:** Battle-Plan Variant (Specialized for Audits)
**Base:** Extends master battle-plan

---

## Specializations

### 1. Pattern Library Focus

**Category:** audit-operations

**Patterns Directory:**
```
.corpus/learning/patterns/audit-operations/
├── code-quality-fixes.json
├── security-fixes.json
├── performance-fixes.json
└── convergence-patterns.json
```

**Common Fix Patterns:**
- eslint-unused-vars-fix (prefix with underscore or remove)
- typescript-strict-mode-migration (incremental adoption)
- security-input-validation (sanitization patterns)
- performance-query-optimization (common database patterns)

**Common Antipatterns:**
- fix-symptom-not-cause (superficial fixes that reappear)
- break-tests-while-fixing (fix introduces new issues)
- ignore-eslint-everywhere (disable instead of fix)
- converge-without-understanding (blindly applying fixes)

### 2. Pre-Mortem Risk Database

**Risk Database:** `.corpus/learning/risks/audit-risks.json`

**Audit-Specific Risks:**
```json
{
  "code-quality": [
    {
      "risk": "Fixes break existing functionality",
      "likelihood": 4,
      "impact": 5,
      "prevention": "Run tests after each fix, verify no new issues"
    },
    {
      "risk": "Config conflicts between linters",
      "likelihood": 3,
      "impact": 3,
      "prevention": "Validate config before running audits"
    }
  ],
  "convergence": [
    {
      "risk": "GATE never converges (same issues reappear)",
      "likelihood": 3,
      "impact": 4,
      "prevention": "Fix root cause, not symptoms. Use detect-infinite-loop."
    },
    {
      "risk": "Fixes introduce new issues",
      "likelihood": 4,
      "impact": 4,
      "prevention": "Verify evidence after each fix, check for new issues"
    }
  ]
}
```

### 3. Convergence Integration

**Enhanced convergence-engine with battle-plan:**

```javascript
async function runConvergenceWithBattlePlan(config) {
  // Before convergence
  const preMortem = await preMortem.run({
    task: "Achieve audit convergence",
    risks: loadRisks("convergence")
  });

  // Phase 1: Discovery (with pattern check)
  const issues = await runAllAudits();
  const knownFixes = await patternLibrary.findFixes(issues);

  // Phase 2: Fix Planning (pattern-aware)
  for (const issue of issues) {
    if (knownFixes[issue.id]) {
      console.log(`Applying known fix: ${knownFixes[issue.id].name}`);
      await applyPattern(knownFixes[issue.id]);
    } else {
      const fix = await generateFix(issue);
      await applyFix(fix);
    }

    // Verify-evidence checkpoint
    await verifyEvidence.check({
      claim: `Issue ${issue.id} fixed`,
      evidence: ["Audit passes", "No new issues", "Tests pass"]
    });
  }

  // Phase 3: GATE (with detect-infinite-loop)
  let cleanPasses = 0;
  let attempts = 0;

  while (cleanPasses < 3 && attempts < 10) {
    const audit = await runAllAudits();

    if (audit.issues.length === 0) {
      cleanPasses++;
    } else {
      cleanPasses = 0;

      // Detect if stuck
      if (detectInfiniteLoop.shouldPivot(attempts)) {
        await pivot(audit.issues);
      }
    }

    attempts++;
  }

  if (cleanPasses >= 3) {
    await declareComplete.ship({task: "convergence"});
  }

  // Update pattern library
  await patternLibrary.updateFixPatterns(issues, fixes);
}
```

### 4. Example Flow: Run Code Quality Audit

```
User: "Run code quality audit"

═══ PHASE 2: KNOWLEDGE CHECK ═══
PATTERN-LIBRARY (audit-operations/code-quality):
  ✓ Found: eslint-common-fixes (124 patterns)
  ✓ Found: typescript-strict-mode-patterns (15 patterns)
  ⚠️ Antipattern: fix-symptom-not-cause (8 occurrences)

═══ PHASE 3: RISK ASSESSMENT ═══
PRE-MORTEM (audit-specific):
  Risk #1: Fixes break functionality (likelihood: 4, impact: 5)
    Prevention: Run tests after each fix
  Risk #2: GATE doesn't converge (likelihood: 3, impact: 4)
    Prevention: Fix root causes, use detect-infinite-loop

═══ PHASE 5: EXECUTION ═══
Running audits...
  ESLint: 45 issues
  TypeScript: 12 issues
  Prettier: 8 issues

Applying known patterns:
  ✓ eslint-unused-vars (23 issues) → prefix-with-underscore pattern
  ✓ prefer-const (12 issues) → auto-fix pattern
  ✓ Missing semicolons (8 issues) → prettier-fix pattern

Novel issues (require analysis):
  - Complex type inference issue (2 occurrences)
  - Circular dependency detected (1 occurrence)

Fixing novel issues:
  [VERIFY-EVIDENCE: Type issue fixed ✓]
  [VERIFY-EVIDENCE: Tests pass ✓]
  [DETECT-INFINITE-LOOP: No loops detected ✓]

Convergence GATE:
  Pass 1: 0 issues ✓
  Pass 2: 0 issues ✓
  Pass 3: 0 issues ✓
  GATE achieved ✓

═══ PHASE 7: DECLARE COMPLETE ═══
✓ SHIPPABLE - All audits pass, 3 clean GATE passes

═══ PHASE 8: PATTERN UPDATE ═══
New pattern saved:
  - complex-type-inference-fix (from novel issue)
Updated patterns:
  - eslint-unused-vars (148 uses, 96% success)
```

---

## Configuration

```json
{
  "auditBattlePlan": {
    "extends": "battle-plan",
    "patternLibrary": {
      "category": "audit-operations",
      "subcategories": ["code-quality", "security", "performance"]
    },
    "preMortem": {
      "riskDatabase": ".corpus/learning/risks/audit-risks.json",
      "alwaysCheckBreakingChanges": true
    },
    "verifyEvidence": {
      "runTestsAfterFix": true,
      "checkNoNewIssues": true
    },
    "convergence": {
      "detectInfiniteLoop": true,
      "maxAttempts": 10,
      "gateRequirement": 3
    }
  }
}
```

---

*End of Audit Battle-Plan*
*Specialized variant for audit and fix operations*
*Extends master battle-plan with fix patterns and convergence monitoring*
