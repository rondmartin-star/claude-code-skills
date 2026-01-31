# Convergence Workflow: Corrected Design

**Date:** 2026-01-31
**Purpose:** Clarify the correct two-phase convergence workflow
**Key Principle:** Automated convergence is a GATE before user testing

---

## The Problem (Original Design)

**What we initially documented:**
```
Run audits → Fix issues → Iterate
↓
3 consecutive clean passes
↓
THEN user validation
```

**Issue identified:**
> "The convergence workflow should happen before manual user testing to minimize frustration due to detectable errors"

**Problem:**
- Users waste time finding bugs automation can catch
- Frustrating for users to encounter obvious errors
- Inefficient use of valuable user testing time
- Users should focus on UX, not detectable bugs

---

## The Solution (Corrected Design)

### Two-Phase Gate Pattern

```
┌─────────────────────────────────────────────────┐
│  CONVERGENCE CYCLE                              │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ PHASE 1: AUTOMATED CONVERGENCE (GATE)   │  │
│  │                                          │  │
│  │ Iterate automated audits until:         │  │
│  │ - 3 consecutive clean passes             │  │
│  │ - All detectable issues fixed            │  │
│  │                                          │  │
│  │ Status: GATE PASSED ✓                    │  │
│  └──────────────────────────────────────────┘  │
│                    ↓                            │
│  ┌──────────────────────────────────────────┐  │
│  │ PHASE 2: USER VALIDATION (CLEAN SYSTEM) │  │
│  │                                          │  │
│  │ Real users test the clean system:        │  │
│  │ - Find UX issues                         │  │
│  │ - Find edge cases                        │  │
│  │ - Find integration problems              │  │
│  │                                          │  │
│  │ If issues found → BACK TO PHASE 1        │  │
│  │ If clean → PRODUCTION READY ✓            │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## Detailed Workflow

### Convergence Cycle Loop

```
convergence_cycle = 0
max_cycles = 5

REPEAT until PRODUCTION READY or max_cycles:

  convergence_cycle++

  ┌─────────────────────────────────────────┐
  │ PHASE 1: AUTOMATED CONVERGENCE          │
  └─────────────────────────────────────────┘

  consecutive_clean_passes = 0
  iteration = 0
  max_iterations = 10

  REPEAT until 3 clean passes or max_iterations:

    iteration++

    1. Run all applicable audits (3 methodologies in parallel)
       - Technical: security-architecture, code-quality, performance
       - User: auth-flow-testing, ux-performance, accessibility
       - Holistic: documentation, dependency, consistency, navigation

    2. Aggregate all issues from all methodologies

    3. IF no issues found:
         consecutive_clean_passes++
         Log "Clean pass {consecutive_clean_passes}/3"
         CONTINUE
       ELSE:
         consecutive_clean_passes = 0  // Reset counter

    4. Prioritize issues based on phase:
       - Discovery (iteration 1): Fix critical + high
       - Verification (iteration 2): Fix all remaining
       - Stabilization (iteration 3+): Fix any found

    5. Generate fix plan for prioritized issues

    6. IF approval_required:
         Get user approval for fix plan
         IF not approved: ABORT

    7. Implement fixes with automatic backup

    8. Log iteration results

  END REPEAT

  IF consecutive_clean_passes < 3:
    Status: "AUTOMATED CONVERGENCE FAILED"
    ABORT (cannot proceed to user testing)

  Log: "✓ Automated convergence complete (3 clean passes)"
  Log: "System is clean - ready for user validation"

  ┌─────────────────────────────────────────┐
  │ PHASE 2: USER VALIDATION                │
  └─────────────────────────────────────────┘

  Log: "Starting user validation on clean system..."

  user_results = run_user_validation({
    real_users: true,
    real_environment: true,
    real_workflows: true,
    real_data: true
  })

  IF user_results.issues.count == 0:
    Status: "PRODUCTION READY"
    BREAK  // Exit loop - we're done!

  ELSE:
    Log: "⚠ User validation found {user_results.issues.count} issues"
    Log: "Issues found: {user_results.issues}"
    Log: "→ Returning to automated convergence..."
    // Loop continues - back to PHASE 1

END REPEAT

IF status == "PRODUCTION READY":
  Generate success report
ELSE:
  Generate failure report with manual review instructions
```

---

## Why This Order Matters

### ✅ Correct Order: Automated THEN User

**Benefits:**
1. **Respects user time** - Users only see clean systems
2. **Better user experience** - No obvious bugs during testing
3. **Focus on value** - Users find real UX issues, not detectable bugs
4. **More efficient** - Automation is cheap, user time is expensive
5. **Higher quality** - Catches both automated AND human-detectable issues

**User Testing Focuses On:**
- UX and user experience issues
- Edge cases automation might miss
- Integration problems
- Workflow confusion
- Real-world scenarios

### ❌ Wrong Order: User Before Automated

**Problems:**
1. **Wastes user time** - Users find bugs automation can catch
2. **Frustrating** - Users encounter obvious errors
3. **Inefficient** - Using expensive resource (users) for cheap task
4. **Lower morale** - Users lose confidence in product quality
5. **Missed issues** - Users give up before finding real UX problems

---

## Example: Real-World Scenario

### Convergence Cycle 1

**PHASE 1: Automated Convergence**
```
Iteration 1 (Discovery - 2 hours):
  Technical methodology:
    - security-architecture: 3 XSS vulnerabilities
    - code-quality: 8 linting errors
    - performance: 2 N+1 queries
  User methodology:
    - ux-performance: 5 unoptimized images
    - accessibility: 12 missing alt texts
  Holistic methodology:
    - documentation: 3 broken links
    - dependency: 2 outdated packages
    - consistency: 1 term misuse

  Total: 36 issues
  → Generate fix plan
  → User approves
  → Fixed 35/36 (1 needs manual research)

Iteration 2 (Verification - 1 hour):
  All audits: 1 issue (manual from iteration 1)
  → Research and fix
  → Success

Iteration 3 (Stabilization - 30 min):
  All audits: 0 issues
  → Clean pass 1/3

Iteration 4:
  All audits: 0 issues
  → Clean pass 2/3

Iteration 5:
  All audits: 0 issues
  → Clean pass 3/3

✓ Automated convergence complete (4.5 hours total)
```

**PHASE 2: User Validation (Clean System)**
```
User testing (1 hour):
  User flow: Sign up → Login → Use feature → Logout

  Issues found by user:
  1. CRITICAL: After OAuth login, app reverts to HTTP (security!)
  2. WARNING: Error message on signup unclear
     "Invalid input" should be "Email already registered"

  Status: 2 issues found
  → Back to automated convergence
```

### Convergence Cycle 2

**PHASE 1: Automated Convergence**
```
Iteration 1:
  security-architecture: 1 HTTPS reversion
  content: 1 error message clarity
  Total: 2 issues
  → Fix both
  → Success

Iteration 2:
  All audits: 0 issues
  → Clean pass 1/3

Iteration 3:
  All audits: 0 issues
  → Clean pass 2/3

Iteration 4:
  All audits: 0 issues
  → Clean pass 3/3

✓ Automated convergence complete (1 hour)
```

**PHASE 2: User Validation (Clean System)**
```
User testing (30 min):
  User flow: Sign up → Login → Use feature → Logout

  Issues found: 0
  ✓ User validation clean

PRODUCTION READY ✓
```

**Total Time:** 7 hours
**Total Issues Fixed:** 38
**User Time:** 1.5 hours (only on clean systems)
**Convergence Cycles:** 2

---

## Configuration

### corpus-config.json

```json
{
  "audit": {
    "convergence": {
      "enabled": true,

      "automated": {
        "max_iterations": 10,
        "required_clean_passes": 3,
        "approval_required": true
      },

      "user_validation": {
        "required": true,
        "after_automated_convergence": true,
        "min_testers": 2,
        "test_scenarios": [
          "complete-user-journey",
          "edge-cases",
          "error-handling",
          "performance-under-load"
        ]
      },

      "max_convergence_cycles": 5
    }
  }
}
```

### Key Settings

| Setting | Default | Purpose |
|---------|---------|---------|
| `max_iterations` | 10 | Max automated iterations per convergence |
| `required_clean_passes` | 3 | Clean passes needed to exit gate |
| `approval_required` | true | User approves fix plans |
| `user_validation.required` | true | Can't skip user testing |
| `user_validation.after_automated_convergence` | true | Only test clean systems |
| `max_convergence_cycles` | 5 | Max convergence → user cycles |

---

## Success Criteria

### Automated Convergence (Phase 1)

**PASS:**
- ✓ 3 consecutive iterations with 0 issues
- ✓ All methodologies clean (technical, user, holistic)
- ✓ All audits pass (9 total)
- ✓ No critical, high, or medium issues

**FAIL:**
- ✗ Max iterations reached without convergence
- ✗ User aborted fix plan approval
- ✗ Unfixable critical issue found

### User Validation (Phase 2)

**PASS:**
- ✓ Real users test clean system
- ✓ 0 critical issues found
- ✓ 0 high issues found
- ✓ <3 medium issues (acceptable risks)

**FAIL:**
- ✗ User finds critical or high issues
- ✗ User finds >3 medium issues
- ✗ Test scenarios incomplete

### Production Ready (Final)

**Requirements:**
- ✅ Automated convergence: PASS
- ✅ User validation: PASS
- ✅ Both achieved in same convergence cycle
- ✅ Final verification: All tests still passing

---

## Common Patterns

### Pattern 1: Quick Convergence

```
Cycle 1:
  Phase 1: 3 iterations → converged (few issues)
  Phase 2: User testing → 0 issues
  Status: PRODUCTION READY ✓

Time: 4-6 hours
Cycles: 1
```

### Pattern 2: User Finds Edge Cases

```
Cycle 1:
  Phase 1: 5 iterations → converged
  Phase 2: User testing → 2 issues (edge cases)

Cycle 2:
  Phase 1: 3 iterations → converged
  Phase 2: User testing → 0 issues
  Status: PRODUCTION READY ✓

Time: 7-10 hours
Cycles: 2
```

### Pattern 3: Complex System

```
Cycle 1:
  Phase 1: 8 iterations → converged
  Phase 2: User testing → 5 issues

Cycle 2:
  Phase 1: 4 iterations → converged
  Phase 2: User testing → 2 issues

Cycle 3:
  Phase 1: 3 iterations → converged
  Phase 2: User testing → 0 issues
  Status: PRODUCTION READY ✓

Time: 12-15 hours
Cycles: 3
```

### Pattern 4: Persistent Issues

```
Cycle 1-5:
  Phase 1: Converges each time
  Phase 2: User always finds issues
  Status: MAX CYCLES - Manual Review Required

Action: Deeper architectural review needed
```

---

## Key Takeaways

1. **Automated convergence is a GATE** - must pass before user testing
2. **Don't waste user time** - only test clean systems
3. **Users find different issues** - UX, edge cases, integration problems
4. **Expect multiple cycles** - rarely perfect on first try
5. **Budget 5-12 hours total** - for comprehensive production readiness

---

**Status:** CORRECTED AND DOCUMENTED
**Updated Files:**
- AUDIT-SYSTEM-DESIGN.md
- core/audit/audit-orchestrator/SKILL.md
- CORPUSHUB-INTEGRATED-PLAN.md
- CONVERGENCE-WORKFLOW-CORRECTED.md (this file)

**Next:** Implement two-phase convergence-engine
