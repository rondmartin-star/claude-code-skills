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

## [\!] LOAD THIS SKILL WHEN

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

## [X] DO NOT LOAD WHEN

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

**Complexity Levels:**
- **Trivial:** Single audit, read-only -> Execute directly
- **Simple:** Quick check, report-only -> Execute directly
- **Medium:** Multi-audit, <10 issues -> Use battle-plan
- **Complex:** Convergence, pre-release, ≥10 issues -> Use battle-plan

**Routing:** Medium/Complex operations use audit-battle-plan for safety and learning

See `references/complexity-assessment.md` for detailed assessment logic and examples

---

## Routing Decision Tree

**Enhanced with complexity assessment and battle-plan routing:**

```
1. Load corpus-config.json from project root
2. Determine project type
3. Check audit_config.applicable_audits
4. Assess operation complexity
   ├─ Trivial/Simple -> Execute directly (no battle-plan)
   └─ Medium/Complex -> Route through audit-battle-plan

5. If convergence requested:
   -> ALWAYS use audit-battle-plan (complex by nature)
   -> Load convergence-engine via battle-plan
   -> Run iterative audit workflow with full monitoring
   -> Run audits in parallel where independent

6. Else if specific audit requested:
   -> Assess complexity
   ├─ Simple (single audit, no fixes) -> Direct execution
   └─ Medium (fixes needed) -> audit-battle-plan

7. Else (audit all):
   -> ALWAYS use audit-battle-plan (medium complexity minimum)
   -> Load all applicable audits via battle-plan
   -> Detect dependencies between audits
   -> Execute in parallel levels (topological order)
   -> Run once, report results
```

---

## Parallel Execution

**Purpose:** Execute multiple independent audits simultaneously for faster results

**Performance Gains:**
- 5 independent audits: 5×30s = 150s -> 30s (5x speedup)
- 10 independent audits: 10×30s = 300s -> 60s (5x speedup with batching)
- Respects dependencies to ensure correct ordering

### Dependency Detection

Some audits have dependencies and must run in order:

| Dependent Audit | Requires | Reason |
|----------------|----------|--------|
| **navigation** | consistency | Navigation needs validated terms from consistency |
| **performance** | quality | Performance needs valid code from quality |
| **seo** | content | SEO meta tags need validated content |
| **accessibility** | quality | A11y checks need valid DOM from quality |

### Parallel Execution Strategy

**Algorithm:** Topological sort + level-based parallel execution with batching

**Key Features:**
- Automatic dependency detection
- Level-based execution (satisfies dependencies)
- Batching to limit concurrent load (default: 5)
- Individual audit failures don't block others
- Sequential fallback when parallel disabled

**Implementation:** See `references/parallel-execution.md` for:
- Complete dependency graph
- Topological sort algorithm
- Error handling patterns
- Performance optimization tips
- Testing examples

### Configuration

**Enable/disable parallel execution in corpus-config.json:**

```json
{
  "audit_config": {
    "execution": {
      "parallel": true,
      "maxConcurrent": 5,
      "respectDependencies": true
    }
  }
}
```

**Override per execution:**

```javascript
await auditOrchestrator.run({
  parallel: true,
  maxConcurrent: 3
});
```

### Example: Web App with Dependencies

```
Audits: [consistency, security, quality, navigation, performance, accessibility]

Dependencies: navigation->consistency, performance->quality, accessibility->quality

Levels:
  L1: [consistency, security, quality] -> parallel (15s)
  L2: [navigation, performance, accessibility] -> parallel (18s)

Result: ~33s (vs ~77s sequential = 57% faster)
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
7. [OK] Gate passed - system is clean for automated audits

**PHASE 2: User Validation (Clean System)**
8. Real user testing on clean system
9. Users find issues automation can't detect (UX, edge cases, integration)
10. If user finds issues -> back to PHASE 1 (automated convergence)
11. Repeat PHASE 1 -> PHASE 2 until both are clean
12. [OK] **PRODUCTION READY** (automated clean + user validation clean)

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
- Combined: **PRODUCTION READY** [OK]

**Failure Modes:**
- Max iterations reached -> Manual review required
- Max cycles reached -> Persistent issues found
- User aborts -> Intervention needed
- Critical blocker found -> Cannot auto-fix

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

See `references/workflow-examples.md` for detailed execution traces

### Example 1: Web App Pre-Release (Complex - Battle-Plan Required)

```
Type: web-app | Complexity: COMPLEX | Battle-plan: YES

Parallel: L1 [security, quality, seo], L2 [performance, accessibility, navigation, dependency]

Cycle 1: 28 issues -> Fixed 27/28 -> 3 clean passes (31s parallel vs 72s sequential)
User validation: 2 issues found
Cycle 2: 2 issues -> Fixed -> 3 clean passes

Result: PRODUCTION READY [OK] (6 hours, 30 issues fixed)
```

### Example 2: Content Corpus Quick Check (Simple - No Battle-Plan)

```
Type: framework-docs | Complexity: SIMPLE | Battle-plan: NO

Parallel: L1 [consistency, content], L2 [navigation]
Result: 12 issues, 12s (vs 18s = 33% faster)
```

### Example 3: Manual Audit Selection

```
User override: [security, performance] | No dependencies

Parallel: L1 [security, performance]
Result: 8 issues, 13s (vs 24s = 46% faster)
```

---

## Performance Benchmarks

**Typical Speedups:**
- 3 audits: 1.5x faster
- 5-7 audits: 2-2.3x faster
- Convergence (5 iterations): 2.3x faster

**Real Example (CorpusHub):**
- 7 audits × 5 iterations: 525s -> 195s
- **Speedup: 2.7x (saved 5.5 minutes)**

See `references/parallel-execution.md` for detailed benchmarks

---

## Integration with Fix Planner

Auto-generates fix plans for detected issues.

**Auto-Fix Capabilities:** Term misuse, broken links, XSS, missing alt text, linting, outdated deps
**User Approval Required:** Grammar, performance optimizations

See: `core/audit/fix-planner/SKILL.md` for implementation details

---

## Configuration Reference

### Full corpus-config.json Audit Section (with Battle-Plan Integration)

```json
{
  "audit_config": {
    "auto_run": false,
    "execution": {
      "parallel": true,
      "maxConcurrent": 5,
      "respectDependencies": true
    },
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
# -> Runs with parallel execution enabled (2-3x faster)

# Quick single-run audit
"Audit this project"
# -> Detects dependencies, runs in parallel levels

# Specific audits only
"Run security and performance audits"
# -> Runs in parallel (independent audits)

# Custom configuration
"Audit with max 15 iterations and no approval required"

# Sequential mode (disable parallel)
"Run audits sequentially" or "Audit without parallel execution"

# Resume from previous
"Resume convergence audit"

# Performance testing
"Run audits with maxConcurrent=10"
# -> Increase concurrent limit (default: 5)
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
