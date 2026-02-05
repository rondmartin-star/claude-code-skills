---
name: audit-orchestrator
description: >
  Comprehensive audit orchestrator with learning-first architecture. Routes to applicable
  audit types and coordinates convergence workflow for production readiness. Uses audit-battle-plan
  for medium/complex operations. Use when: running pre-release audits, validating quality,
  ensuring production readiness, or achieving stable clean state through iterative improvement.
---

# Audit Orchestrator

**Purpose:** Coordinate comprehensive audits and convergence with battle-plan integration
**Size:** ~13 KB
**Type:** Core Pattern (Universal - Available to all projects)
**Learning Integration:** Uses audit-battle-plan for medium/complex audit operations

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Run convergence audit"
- "Pre-release audit"
- "Production readiness check"
- "Audit everything"
- "Quality validation"
- "Run all audits"
- "Prepare for release"
- "Make this production-ready"

**Context Indicators:**
- User mentions "production ready"
- User preparing for release/deployment
- User wants comprehensive quality check
- User mentions multiple quality dimensions
- Late-stage development phase

## ❌ DO NOT LOAD WHEN

- Single specific audit needed (load specific audit directly)
- Early development (not ready for comprehensive auditing)
- User just wants to fix one issue

---

## Audit Types Available

| Audit | Purpose | Applicable To |
|-------|---------|---------------|
| **consistency** | Term usage, cross-references, canonical definitions | All projects with framework terms |
| **security** | XSS, CSRF, SQL injection, OAuth, secrets | Web apps, APIs, Windows apps |
| **quality** | Test coverage, linting, code complexity | All code projects |
| **performance** | Load time, bundle size, N+1 queries | Web apps, APIs |
| **accessibility** | WCAG compliance, ARIA, keyboard navigation | Web apps, user interfaces |
| **seo** | Meta tags, sitemap, Open Graph | Websites, public content |
| **content** | Grammar, style, formatting, readability | All content projects |
| **navigation** | Broken links, orphaned pages, circular loops | All projects with navigation |
| **dependency** | Vulnerabilities, outdated packages | All projects with dependencies |

---

## Project Type Detection

Automatically detect applicable audits based on corpus-config.json:

| Project Type | Auto-Loaded Audits |
|--------------|-------------------|
| **web-app** | security, performance, accessibility, seo, quality, navigation, dependency |
| **content-corpus** | consistency, content, navigation |
| **framework-docs** | consistency, content, navigation |
| **windows-app** | security, quality, dependency |
| **publishing** | content, seo, accessibility |
| **api** | security, quality, performance, dependency |

### Manual Override

User can specify audits in corpus-config.json:

```json
{
  "audit_config": {
    "applicable_audits": [
      "consistency",
      "security",
      "quality"
    ]
  }
}
```

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

**Complexity Examples:**

| Operation | Complexity | Use Battle-Plan? | Reason |
|-----------|------------|------------------|--------|
| Single security audit (read-only) | Trivial | No | One audit, no fixes |
| Quick quality check | Simple | No | Fast diagnostic |
| Audit all (single-run) | Medium | Yes | Multiple audits, planning |
| Fix 15 issues | Medium | Yes | Multi-step fixes, risks |
| Convergence (3-3-1 GATE) | Complex | Yes | Iterative, GATE, risks |
| Pre-release validation | Complex | Yes | Critical, comprehensive |

**Battle-Plan Integration:**
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

## Routing Decision Tree

**Enhanced with complexity assessment and battle-plan routing:**

```
1. Load corpus-config.json from project root
2. Determine project type
3. Check audit_config.applicable_audits
4. Assess operation complexity
   ├─ Trivial/Simple → Execute directly (no battle-plan)
   └─ Medium/Complex → Route through audit-battle-plan

5. If convergence requested:
   → ALWAYS use audit-battle-plan (complex by nature)
   → Load convergence-engine via battle-plan
   → Run iterative audit workflow with full monitoring

6. Else if specific audit requested:
   → Assess complexity
   ├─ Simple (single audit, no fixes) → Direct execution
   └─ Medium (fixes needed) → audit-battle-plan

7. Else (audit all):
   → ALWAYS use audit-battle-plan (medium complexity minimum)
   → Load all applicable audits via battle-plan
   → Run once, report results
```

---

## Convergence Mode

**When to Use:**
- Pre-release validation
- Production readiness check
- Achieving stable clean state
- Late-stage quality assurance

**How It Works (Two-Phase Gate):**

**PHASE 1: Automated Convergence (Gate)**
1. Run all applicable audits (3 methodologies in parallel)
2. Identify issues
3. Generate fix plan
4. Get user approval for fixes (optional)
5. Implement fixes
6. Repeat steps 1-5 until 3 consecutive clean passes
7. ✓ Gate passed - system is clean for automated audits

**PHASE 2: User Validation (Clean System)**
8. Real user testing on clean system
9. Users find issues automation can't detect (UX, edge cases, integration)
10. If user finds issues → back to PHASE 1 (automated convergence)
11. Repeat PHASE 1 → PHASE 2 until both are clean
12. ✓ **PRODUCTION READY** (automated clean + user validation clean)

**Why This Order:**
- Don't waste user time finding bugs automation can catch
- Users focus on real UX issues, not obvious errors
- More efficient use of valuable user testing time
- Minimizes frustration from detectable errors

**Configuration:**

```json
{
  "audit_config": {
    "convergence": {
      "enabled": true,
      "max_iterations": 10,
      "required_clean_passes": 3,
      "approval_required": true,
      "max_convergence_cycles": 5,
      "user_validation": {
        "required": true,
        "after_automated_convergence": true
      }
    }
  }
}
```

**Safety Mechanisms:**
- Max iterations per convergence (default: 10)
- Max convergence cycles (default: 5)
- Automatic backups before fixes
- Rollback on failure
- User approval gates for fixes
- Full audit trail

**Success Criteria:**
- Automated: 3 consecutive clean passes
- User Validation: 0 critical issues found
- Combined: **PRODUCTION READY** ✓

**Failure Modes:**
- Max iterations reached → Manual review required
- Max cycles reached → Persistent issues found
- User aborts → Intervention needed
- Critical blocker found → Cannot auto-fix

See: core/audit/convergence-engine/SKILL.md for detailed algorithm

---

## Single-Run Mode

**When to Use:**
- Quick validation
- Spot-checking specific areas
- Early development
- CI/CD integration

**How It Works:**
1. Run all applicable audits once
2. Report all issues found
3. Suggest fixes (no automatic implementation)
4. Exit

**Output Format:**

```json
{
  "timestamp": "2026-01-31T10:30:00Z",
  "project": "my-project",
  "project_type": "web-app",
  "audits_run": 9,
  "total_issues": 23,
  "by_severity": {
    "critical": 2,
    "warning": 15,
    "info": 6
  },
  "by_audit": {
    "security": 2,
    "performance": 8,
    "accessibility": 5,
    "quality": 4,
    "content": 3,
    "navigation": 1
  },
  "issues": [...]
}
```

---

## Workflow Examples

### Example 1: Web App Pre-Release (Complex - Battle-Plan Required)

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
    - security: 3 XSS vulnerabilities
    - performance: 5 unoptimized images
    - accessibility: 12 missing alt texts
    - quality: 8 linting errors
    - Total: 28 issues
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

### Example 2: Content Corpus Quick Check (Simple - No Battle-Plan)

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

→ Execute directly (no battle-plan overhead)
→ Single-run mode (no convergence)

Results:
  - consistency: 8 term misuses
  - content: 3 grammar errors
  - navigation: 1 broken link
  - Total: 12 issues

Fix suggestions provided
User decides whether to apply

[Battle-plan skipped for better UX - fast results for simple query]
```

### Example 3: Manual Audit Selection

```
User: "Run only security and performance audits"

→ audit-orchestrator loads
→ User override: ["security", "performance"]
→ Single-run mode

Results:
  - security: 2 CSRF issues
  - performance: 6 optimization opportunities
  - Total: 8 issues

Fix suggestions provided
```

---

## Integration with Fix Planner

When issues found, automatically generate fix plans:

**Fix Plan Structure:**

```json
{
  "plan_id": "plan-2026-01-31-001",
  "timestamp": "2026-01-31T10:30:00Z",
  "issues_count": 28,
  "fixes": [
    {
      "location": "src/auth.js:42",
      "issues": [
        {
          "severity": "critical",
          "audit": "security",
          "category": "xss",
          "description": "User input not escaped"
        }
      ],
      "actions": [
        {
          "type": "code_replace",
          "old": "res.send(req.body.name)",
          "new": "res.send(escapeHtml(req.body.name))"
        }
      ],
      "estimated_risk": "low",
      "backup_required": true
    }
  ]
}
```

**Auto-Fix Capabilities:**

| Issue Type | Auto-Fix | Strategy |
|------------|----------|----------|
| Term misuse | ✓ | Replace with canonical term |
| Broken link | ✓ | Update to correct path |
| Missing alt text | ✓ | AI-generated description |
| XSS vulnerability | ✓ | Add escapeHtml() |
| Missing meta tag | ✓ | Insert from template |
| Outdated dependency | ✓ | Update to latest secure version |
| Linting error | ✓ | Run eslint --fix |
| Grammar error | User approval | Suggest correction |
| Performance issue | User approval | Suggest optimization |

See: core/audit/fix-planner/SKILL.md for implementation details

---

## Configuration Reference

### Full corpus-config.json Audit Section (with Battle-Plan Integration)

```json
{
  "audit_config": {
    "auto_run": false,
    "battle_plan": {
      "enabled": true,
      "variant": "audit-battle-plan",
      "use_for_convergence": true,
      "use_for_multi_audit": true,
      "complexity_threshold": "medium"
    },
    "convergence": {
      "enabled": true,
      "max_iterations": 10,
      "required_clean_passes": 3,
      "approval_required": true,
      "backup_before_fix": true,
      "rollback_on_failure": true,
      "use_monitoring": {
        "verify_evidence": true,
        "detect_infinite_loop": true,
        "manage_context": true
      }
    },
    "applicable_audits": [
      "consistency",
      "security",
      "quality",
      "performance",
      "accessibility",
      "seo",
      "content",
      "navigation",
      "dependency"
    ],
    "audit_specific_config": {
      "consistency": {
        "canonical_source": "corpus-config.json",
        "severity_threshold": "warning"
      },
      "security": {
        "include_checks": ["xss", "csrf", "sql_injection", "secrets"],
        "exclude_patterns": ["test/**"]
      },
      "quality": {
        "min_coverage": 80,
        "max_complexity": 10,
        "linting_config": ".eslintrc.json"
      },
      "performance": {
        "max_bundle_size_kb": 500,
        "max_load_time_ms": 3000
      },
      "accessibility": {
        "wcag_level": "AA",
        "skip_third_party": true
      }
    }
  }
}
```

---

## Exit Criteria

### Success (Single-Run)
- All applicable audits executed
- Results reported to user
- Fix suggestions provided

### Success (Convergence)
- 3 consecutive clean passes achieved
- Status: **PRODUCTION READY**
- Final report generated
- Audit log saved to .corpus/audit-logs/

### Failure (Convergence)
- Max iterations reached without convergence
- Status: **MANUAL REVIEW REQUIRED**
- Issue summary provided
- Recommendations for manual fixes

### User Abort
- User cancels during approval gate
- Status: **ABORTED**
- Current state preserved
- Progress saved for resume

---

## Quick Reference: Commands

```bash
# Run convergence audit (recommended for production)
"Run convergence audit"

# Quick single-run audit
"Audit this project"

# Specific audits only
"Run security and performance audits"

# Custom configuration
"Audit with max 15 iterations and no approval required"

# Resume from previous
"Resume convergence audit"
```

---

## References

**Detailed Documentation:**
- core/audit/convergence-engine/SKILL.md - Iterative algorithm
- core/audit/fix-planner/SKILL.md - Fix generation and implementation
- core/audit/audits/*/SKILL.md - Individual audit types
- config/templates/web-app.json - Example configuration
- AUDIT-SYSTEM-DESIGN.md - Full system architecture

**Configuration Examples:**
- config/examples/america40-config.json - Framework docs
- config/examples/corpushub-config.json - Web application
- config/templates/*.json - Template configurations

---

*End of Audit Orchestrator*
*Part of v4.0.0 Universal Skills Ecosystem*
*Learning Integration: Uses audit-battle-plan for medium/complex operations*
*Convergence operations ALWAYS use battle-plan for safety and learning*
