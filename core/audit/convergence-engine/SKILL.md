---
name: convergence-engine
description: >
  Multi-methodology iterative audit engine implementing the 3-3-1 rule (3 methodologies
  × 3 iterations × 1 user validation). Runs automated convergence as a gate before
  user testing. Use when: preparing for production, pre-release validation, achieving
  stable clean state through systematic quality assurance.
---

# Convergence Engine

**Purpose:** Achieve production-ready state through multi-methodology iterative audits
**Size:** ~14 KB
**Type:** Core Pattern (Universal)
**Methodology:** 3-3-1 Rule (Proven: F→A grade, 5hrs, $27k+ savings)

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Run convergence audit"
- "Prepare for production"
- "Pre-release validation"
- "Make this production-ready"
- "Run full quality assurance"

**Context Indicators:**
- Late-stage development
- Pre-release milestone
- Production deployment preparation
- Major version release
- Post-development quality gate

## ❌ DO NOT LOAD WHEN

- Early development (not ready for comprehensive audits)
- Single audit needed (use specific audit directly)
- Quick spot-check (use single-run audit mode)

---

## The 3-3-1 Rule (Proven Methodology)

### 3 Methodologies (Run in Parallel)

Choose complementary perspectives covering:

1. **Technical/Internal** - How it works
   - Code architecture
   - Implementation quality
   - Technical correctness

2. **User/External** - How it's experienced
   - User flows
   - UX and accessibility
   - Feature usability

3. **Holistic/Meta** - How it fits together
   - Documentation
   - Consistency
   - Completeness

### 3 Iterations (Minimum)

**Iteration 1: Discovery (2-4 hours)**
- Find 60-80% of total issues
- Fix critical and high-priority items
- Establish baseline

**Iteration 2: Verification (1-2 hours)**
- Verify Iteration 1 fixes
- Catch incomplete implementations
- Find remaining 20-30% of issues
- Fix medium-priority items

**Iteration 3: Stabilization (0.5-1 hour)**
- Final comprehensive check
- Confirm 0 critical/high issues
- Clean pass verification

**Rule:** Continue until 3 consecutive clean passes

### 1 User Validation (Essential)

**After automated convergence:**
- Real users (not just developers)
- Real environment (not just localhost)
- Real workflows (end-to-end)
- Real data (not just test data)

**Critical:** Never skip - even after 3 clean automated passes

---

## Two-Phase Convergence Workflow

### PHASE 1: Automated Convergence (GATE)

**Purpose:** Reach stable automated clean state before user testing

**Workflow:**
```
consecutive_clean_passes = 0
iteration = 0
max_iterations = 10

WHILE consecutive_clean_passes < 3 AND iteration < max_iterations:

  iteration++

  # 1. Run all 3 methodologies in parallel
  results = run_methodologies([technical, user, holistic])

  # 2. Aggregate issues from all methodologies
  all_issues = aggregate(results)

  # 3. Check if clean
  IF all_issues.count == 0:
    consecutive_clean_passes++
    LOG "Clean pass {consecutive_clean_passes}/3"
    CONTINUE

  ELSE:
    consecutive_clean_passes = 0  # Reset on any issues

  # 4. Prioritize based on phase
  phase = iteration == 1 ? 'discovery' :
          iteration == 2 ? 'verification' :
          'stabilization'

  priority = get_priority_for_phase(phase)
  issues_to_fix = prioritize(all_issues, priority)

  # 5. Generate fix plan
  plan = generate_fix_plan(issues_to_fix)

  # 6. Get approval (optional)
  IF approval_required:
    approved = await user_approval(plan)
    IF NOT approved: ABORT

  # 7. Implement fixes with backup
  backup_create()
  results = implement_fixes(plan)

  IF results.failed > 0:
    backup_restore()

  # 8. Log iteration
  log_iteration(iteration, all_issues, results)

END WHILE

IF consecutive_clean_passes < 3:
  STATUS = "AUTOMATED CONVERGENCE FAILED"
  ABORT

LOG "✓ Automated convergence complete (3 clean passes)"
STATUS = "GATE PASSED"
```

### PHASE 2: User Validation (Clean System)

**Purpose:** Test clean system with real users to find UX/integration issues

**Workflow:**
```
LOG "Phase 2: User Validation (testing clean system)"

# Run user validation tests
user_results = run_user_validation({
  real_users: true,
  real_environment: true,
  real_workflows: true,
  real_data: true
})

IF user_results.issues.count == 0:
  STATUS = "PRODUCTION READY"
  RETURN SUCCESS

ELSE:
  LOG "⚠ User found {user_results.issues.count} issues"
  LOG "→ Returning to Phase 1 (automated convergence)"
  # Back to Phase 1 for another convergence cycle
```

### Convergence Cycle Loop

**Outer loop:** Repeat Phase 1 → Phase 2 until production ready

```
convergence_cycle = 0
max_cycles = 5
production_ready = false

WHILE NOT production_ready AND convergence_cycle < max_cycles:

  convergence_cycle++

  # Phase 1: Automated Convergence (Gate)
  automated_status = run_automated_convergence()

  IF automated_status != "CONVERGED":
    ABORT "Cannot reach automated convergence"

  # Phase 2: User Validation (Clean System)
  user_status = run_user_validation()

  IF user_status.issues.count == 0:
    production_ready = true

END WHILE

IF production_ready:
  STATUS = "PRODUCTION READY"
ELSE:
  STATUS = "MAX CYCLES - Manual Review Required"
```

---

## Why This Order: Automated THEN User

### ✅ Benefits of Gate Pattern

1. **Respects user time** - Users only test clean systems
2. **Better UX** - No obvious bugs during user testing
3. **Focus on value** - Users find real UX issues, not detectable bugs
4. **More efficient** - Automation cheap, user time expensive
5. **Higher quality** - Catches both automated AND human issues

### ❌ Problems with User-First

1. **Wastes time** - Users find bugs automation can catch
2. **Frustrating** - Users encounter obvious errors
3. **Inefficient** - Expensive resource for cheap task
4. **Lower morale** - Users lose confidence
5. **Missed issues** - Users give up before finding UX problems

---

## Methodology Selection

### By Project Type

| Project Type | Technical | User | Holistic |
|--------------|-----------|------|----------|
| **web-app** | security-architecture, code-quality, performance | auth-flow-testing, ux-performance, accessibility | documentation, dependency, consistency, navigation |
| **content-corpus** | N/A | accessibility, content | consistency, navigation, documentation |
| **framework-docs** | code-quality | content, accessibility | consistency, documentation, navigation |
| **windows-app** | security-architecture, code-quality | auth-flow-testing, accessibility | dependency, documentation |

### Custom Selection

Configure in corpus-config.json:

```json
{
  "audit": {
    "convergence": {
      "methodologies": [
        {
          "name": "technical",
          "audits": ["security-architecture", "code-quality"]
        },
        {
          "name": "user",
          "audits": ["auth-flow-testing", "accessibility"]
        },
        {
          "name": "holistic",
          "audits": ["consistency", "navigation", "documentation"]
        }
      ]
    }
  }
}
```

---

## Fix Prioritization

### Discovery Phase (Iteration 1)

**Priority:** Critical + High
- Focus on severe issues first
- Build foundation for quality
- Quick wins for major problems

### Verification Phase (Iteration 2)

**Priority:** All remaining
- Verify previous fixes
- Fix medium-priority items
- Catch incomplete implementations

### Stabilization Phase (Iteration 3+)

**Priority:** Any found
- Should be very few issues
- Final cleanup
- Confirm stability

---

## Success Criteria

### Automated Convergence (Phase 1)

**CONVERGED:**
- ✓ 3 consecutive iterations with 0 issues
- ✓ All methodologies clean
- ✓ All audits pass
- ✓ No critical, high, or medium issues

**FAILED:**
- ✗ Max iterations reached (10)
- ✗ User aborted
- ✗ Unfixable blocker

### User Validation (Phase 2)

**PASS:**
- ✓ 0 critical issues
- ✓ 0 high issues
- ✓ <3 medium issues (documented acceptable risks)

**FAIL:**
- ✗ Any critical or high issues
- ✗ >3 medium issues
- ✗ Test scenarios incomplete

### Production Ready (Final)

**Requirements:**
- ✅ Automated convergence: CONVERGED
- ✅ User validation: PASS
- ✅ Both in same convergence cycle
- ✅ Final verification: All tests passing

---

## Configuration

### corpus-config.json

```json
{
  "audit": {
    "methodology": "multi-methodology-3-3-1",
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

      "max_convergence_cycles": 5,

      "time_budgets": {
        "discovery": "2-4 hours",
        "verification": "1-2 hours",
        "stabilization": "0.5-1 hour",
        "total_target": "5-12 hours"
      }
    }
  }
}
```

---

## Proven Results (CorpusHub Case Study)

**Security Audit with 3-3-1 Methodology:**

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Grade | F | A | 500%+ ↑ |
| Critical Issues | 3 | 0 | -100% |
| High Issues | 7 | 0 | -100% |
| Medium Issues | 8 | 0 | -100% |
| Total Issues | 23 | 0 | -100% |
| Time to Production | N/A | 5 hours | N/A |
| Cost Savings | - | $27,600+ | Post-prod avoided |

**Details:**
- 3 methodologies run in parallel
- 23 issues found (vs. ~8 with single methodology)
- 3 iterations + 1 user-found critical issue
- Production-ready in 5 hours total
- ROI: 25x to 2,000x

---

## Example: Web App Pre-Release

```
=== Convergence Cycle 1 ===

PHASE 1: Automated Convergence

Iteration 1 (Discovery - 2.5 hours):
  Technical methodology:
    • security-architecture: 3 XSS vulnerabilities
    • code-quality: 8 linting errors
    • performance: 2 N+1 queries
  User methodology:
    • ux-performance: 5 unoptimized images
    • accessibility: 12 missing alt texts
  Holistic methodology:
    • navigation: 3 broken links
    • dependency: 2 outdated packages
    • consistency: 1 term misuse

  Total: 36 issues
  → Generated fix plan
  → User approved
  → Fixed 35/36 (1 manual research needed)

Iteration 2 (Verification - 1 hour):
  All audits: 1 issue (manual from iteration 1)
  → Researched and fixed
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

✓ Automated convergence complete (4.5 hours)

PHASE 2: User Validation (Clean System)

Real user testing (1 hour):
  User flow: Sign up → Login → Use feature → Logout

  Issues found:
  1. [CRITICAL] After OAuth login, reverts to HTTP
  2. [WARNING] Error message unclear on signup

  Status: 2 issues found
  → Returning to Phase 1

=== Convergence Cycle 2 ===

PHASE 1: Automated Convergence

Iteration 1 (1 hour):
  • security-architecture: 1 HTTPS reversion
  • content: 1 error message clarity
  → Fixed both issues

Iteration 2-4:
  All audits: 0 issues
  → Clean passes 1/3, 2/3, 3/3

✓ Automated convergence complete

PHASE 2: User Validation (Clean System)

Real user testing (30 min):
  User flow: Sign up → Login → Use feature → Logout
  Issues found: 0

  ✓ User validation clean

PRODUCTION READY ✓

Total time: 7 hours
Total issues fixed: 38
User testing time: 1.5 hours (only on clean systems)
Convergence cycles: 2
```

---

## Safety Mechanisms

1. **Max iterations** (default: 10) - Prevent infinite loops
2. **Max cycles** (default: 5) - Limit convergence attempts
3. **Automatic backups** - Before each fix implementation
4. **Rollback on failure** - Restore if fix fails
5. **User approval gates** - Optional approval for fix plans
6. **Full audit trail** - Log everything for review
7. **Progress monitoring** - Real-time status updates

---

## Time Budgets

### Expected Timeline

| Phase | Time | Parallelizable? |
|-------|------|-----------------|
| Discovery | 2-4 hours | Yes (3 methods) |
| Verification | 1-2 hours | Yes (3 methods) |
| Stabilization | 0.5-1 hour | Yes (3 methods) |
| User Testing | 0.5-1 hour | No |
| **Total** | **5-12 hours** | ~66% parallelized |

### ROI Calculation

**Pre-production fix:** $50 (30 min engineer time)
**Post-production fix:** $1,250-$100,250 (debugging + customer impact)

**ROI:** 25x to 2,000x

For 23 issues: Savings = 23 × ($1,250 - $50) = $27,600+

**Conclusion:** Multi-methodology convergence is extraordinarily cost-effective.

---

## Quick Reference

**Start Convergence:**
```javascript
const result = await runConvergence(projectConfig);
console.log(result.finalStatus); // "PRODUCTION READY" or error
```

**Check Progress:**
```javascript
result.convergenceCycles.forEach(cycle => {
  console.log(`Cycle ${cycle.cycleNumber}:`);
  console.log(`  Automated: ${cycle.automatedConvergence.status}`);
  console.log(`  User: ${cycle.userValidation.issues.length} issues`);
});
```

**Get Details:**
```javascript
const cycle = result.convergenceCycles[0];
const iterations = cycle.automatedConvergence.iterations;

iterations.forEach(iter => {
  console.log(`Iteration ${iter.number}: ${iter.totalIssues} issues`);
});
```

---

*End of Convergence Engine*
*Part of v4.0.0 Universal Skills Ecosystem*
*Methodology: 3-3-1 Rule (Proven in Production)*
