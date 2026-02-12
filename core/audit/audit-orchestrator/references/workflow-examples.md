# Audit Orchestrator - Workflow Examples

**Purpose:** Detailed execution examples showing battle-plan integration and parallel execution

---

## Example 1: Web App Pre-Release (Complex - Battle-Plan Required)

### Full Workflow

```
User: "Run convergence audit for pre-release"

→ audit-orchestrator loads
→ Reads corpus-config.json: type = "web-app"
→ Applicable audits: security, performance, accessibility, seo, quality, navigation, dependency

Complexity Assessment:
  - Operation: convergence
  - Level: COMPLEX (iterative, GATE requirement, multiple methodologies)
  - Use battle-plan: YES
  - Reason: Critical pre-release validation with known risks

Parallel Execution Setup:
  - Parallel: enabled (maxConcurrent: 5)
  - Dependencies detected: 3
    • navigation requires consistency (not in list)
    • performance requires quality
    • accessibility requires quality
  - Topological sort: 2 levels
    • Level 1: [security, quality, seo]
    • Level 2: [performance, accessibility, navigation, dependency]

→ Route through audit-battle-plan
→ Load convergence-engine via battle-plan

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
  → Starts two-phase workflow

=== Convergence Cycle 1 ===

PHASE 1: Automated Convergence
  Iteration 1 (discovery):
    ═══ LEVEL 1 (3 audits in parallel) ═══
      Starting security...
      Starting quality...
      Starting seo...
      ✓ security complete (10s) - 3 XSS vulnerabilities
      ✓ seo complete (12s) - 0 issues
      ✓ quality complete (15s) - 8 linting errors

    ═══ LEVEL 2 (4 audits in parallel, batched) ═══
    Batch 1 (3 audits):
      Starting performance...
      Starting accessibility...
      Starting navigation...
      ✓ performance complete (14s) - 5 unoptimized images
      ✓ navigation complete (9s) - 0 issues
      ✓ accessibility complete (16s) - 12 missing alt texts
    Batch 2 (1 audit):
      Starting dependency...
      ✓ dependency complete (8s) - 0 issues

    - Total: 28 issues (parallel time: ~39s vs ~72s sequential)
    → Generate fix plan
    → User approves
    → Fixed 27/28 (1 needs manual review)

  Iteration 2 (verification):
    - All audits: 1 issue (manual from iteration 1)
    → Fix manual issue
    → Success

  Iteration 3 (stabilization):
    - All audits: 0 issues
    → Clean pass 1/3

  Iteration 4:
    - All audits: 0 issues
    → Clean pass 2/3

  Iteration 5:
    - All audits: 0 issues
    → Clean pass 3/3

  ✓ Automated convergence complete

PHASE 2: User Validation
  Real user testing on clean system...
  → User found: HTTPS reversion after OAuth login (critical!)
  → User found: Confusing error message on signup form
  ⚠ User validation found 2 issues
  → Returning to automated convergence...

=== Convergence Cycle 2 ===

PHASE 1: Automated Convergence
  Iteration 1:
    - security: 1 HTTPS issue
    - content: 1 error message issue
    - Total: 2 issues
    → Fix both issues

  Iteration 2:
    - All audits: 0 issues
    → Clean pass 1/3

  Iteration 3:
    - All audits: 0 issues
    → Clean pass 2/3

  Iteration 4:
    - All audits: 0 issues
    → Clean pass 3/3

  ✓ Automated convergence complete

PHASE 2: User Validation
  Real user testing on clean system...
  ✓ User validation clean (0 issues)

PRODUCTION READY ✓
- Automated: 3 clean passes
- User validation: 0 issues
- Total time: 6 hours
- Total issues fixed: 30

[During execution, battle-plan monitoring was active:]
  - verify-evidence: 42 checkpoints (all passed)
  - detect-infinite-loop: 0 loops detected
  - manage-context: Chunked work after iteration 4 (context 78%)

PHASE 7: DECLARE COMPLETE
  Requirements Met:
    - Core: 5/5 (100%) ✓
      - All audits passing
      - 3 clean GATE passes
      - User validation clean
      - No critical blockers
      - Tests passing
    - Important: 4/4 (100%) ✓
  Status: ✓ SHIPPABLE (PRODUCTION READY)

PHASE 8: PATTERN UPDATE
  New patterns saved: 3
    - xss-input-sanitization-fix (from security audit)
    - accessibility-aria-label-auto-add (from a11y audit)
    - performance-image-lazy-load (from perf audit)
  Updated patterns: 5
    - eslint-auto-fix (148 applications, 96% success)
  Antipatterns updated: 1
    - fix-symptom-not-cause (verified prevention works)

✓ Pattern library updated with learnings from this convergence
```

---

## Example 2: Content Corpus Quick Check (Simple - No Battle-Plan)

```
User: "Quick audit of framework docs - just show me issues"

→ audit-orchestrator loads
→ Reads corpus-config.json: type = "framework-docs"
→ Applicable audits: consistency, content, navigation

Complexity Assessment:
  - Operation: audit-all (single-run, report-only)
  - Level: SIMPLE (read-only, no fixes)
  - Use battle-plan: NO
  - Reason: Quick diagnostic, no changes

Parallel Execution Setup:
  - Dependencies detected: navigation requires consistency
  - Topological sort: 2 levels
    • Level 1: [consistency, content]
    • Level 2: [navigation]

→ Execute directly (no battle-plan overhead)
→ Single-run mode (no convergence)

Execution:
  ═══ LEVEL 1 (2 audits in parallel) ═══
    Starting consistency...
    Starting content...
    ✓ consistency complete (7s) - 8 term misuses
    ✓ content complete (6s) - 3 grammar errors

  ═══ LEVEL 2 (1 audit) ═══
    Starting navigation...
    ✓ navigation complete (5s) - 1 broken link

Total time: ~12s (vs ~18s sequential = 33% faster)
Total issues: 12

Results:
  - consistency: 8 term misuses
  - content: 3 grammar errors
  - navigation: 1 broken link

Fix suggestions provided:
  1. Replace "data structure" with "Content Unit" (8 locations)
  2. Fix grammar: "Each artifacts has" → "Each artifact has"
  3. Update broken link: /old-path → /new-path

User decides whether to apply

[Battle-plan skipped for better UX - fast results for simple query]
[Parallel execution still used for speed optimization]
```

---

## Example 3: Manual Audit Selection

```
User: "Run only security and performance audits"

→ audit-orchestrator loads
→ User override: ["security", "performance"]
→ Single-run mode

Complexity Assessment:
  - Operation: multi-audit
  - Level: SIMPLE (2 audits, no convergence)
  - Use battle-plan: NO

Parallel Execution Setup:
  - Dependencies detected: performance requires quality (not selected)
  - No dependencies between selected audits
  - Topological sort: 1 level
    • Level 1: [security, performance]

Execution:
  ═══ LEVEL 1 (2 audits in parallel) ═══
    Starting security...
    Starting performance...
    ✓ security complete (11s) - 2 CSRF issues
    ✓ performance complete (13s) - 6 optimization opportunities

Total time: ~13s (vs ~24s sequential = 46% faster)
Total issues: 8

Results:
  - security: 2 CSRF issues
    • POST /api/data missing CSRF token
    • DELETE /api/user/:id missing CSRF token

  - performance: 6 optimization opportunities
    • Bundle size: 2.3MB (target: 500KB)
    • Load time: 4.2s (target: 3s)
    • 4 unoptimized images (total: 1.5MB)

Fix suggestions provided:
  1. Add CSRF middleware to Express app
  2. Enable image lazy loading
  3. Code-split large bundle
  4. Compress images with imagemin
```

---

## Example 4: Error Handling (Audit Failure)

```
User: "Run all audits"

→ audit-orchestrator loads
→ Applicable audits: [security, quality, performance]

Execution:
  ═══ LEVEL 1 (3 audits in parallel) ═══
    Starting security...
    Starting quality...
    Starting performance...
    ✓ security complete (10s) - 2 issues
    ✗ quality failed (3s): ESLint config not found
    ✓ performance complete (12s) - 5 issues

Results:
  ✓ security: 2 XSS vulnerabilities
  ✗ quality: FAILED (ESLint config not found)
  ✓ performance: 5 optimization opportunities

⚠️ Warning: quality audit failed but other audits completed

Recommendations:
  1. Fix quality audit: Create .eslintrc.json
  2. Review security and performance issues
  3. Re-run all audits after fixing quality config

Total: 7 issues (2 audits succeeded, 1 failed)
```

---

## Example 5: Custom Configuration

```
User: "Run audits with max 15 iterations and no approval required"

→ audit-orchestrator loads
→ Override configuration:
    max_iterations: 15 (default: 10)
    approval_required: false (default: true)

Execution:
  [Runs convergence with custom config]
  [Auto-approves all fix plans]
  [Will iterate up to 15 times if needed]

⚠️ Running without approval - all fixes will be applied automatically
✓ Convergence complete after 8 iterations
```

---

## Example 6: Resume from Previous

```
User: "Resume convergence audit"

→ audit-orchestrator loads
→ Checks for saved state in .corpus/audit-logs/
→ Found: audit-2026-01-31-001.json

Resuming from:
  - Iteration: 3
  - Clean passes: 1
  - Issues remaining: 5

Execution:
  [Continues from where it left off]
  [Completes convergence]

✓ Convergence complete (resumed from iteration 3)
```

---

*End of Workflow Examples*
*Part of audit-orchestrator v4.0*
