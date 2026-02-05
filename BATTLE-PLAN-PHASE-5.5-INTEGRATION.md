# Battle-Plan Phase 5.5 Integration Guide

**Date:** 2026-02-05
**Purpose:** Add Phase 5.5 (Iterative Phase Review) to battle-plan orchestrator
**Location:** `core/learning/orchestrators/battle-plan/SKILL.md`
**Status:** Ready for integration

---

## Overview

Add Phase 5.5 (Iterative Phase Review) between:
- **Phase 5: Execution (with Monitoring)**
- **Phase 6: Reflection**

This creates a quality gate that reviews task deliverables before moving to reflection and completion.

---

## Current Battle-Plan Flow

```
Phase 1: Clarification (clarify-requirements)
Phase 2: Knowledge Check (pattern-library check)
Phase 3: Risk Assessment (pre-mortem)
Phase 4: Confirmation (confirm-operation)
Phase 5: Execution (with verify-evidence, detect-infinite-loop, manage-context)
Phase 6: Reflection (error-reflection)
Phase 7: Completion (declare-complete)
Phase 8: Pattern Update (pattern-library update)
```

---

## New Battle-Plan Flow

```
Phase 1: Clarification (clarify-requirements)
Phase 2: Knowledge Check (pattern-library check)
Phase 3: Risk Assessment (pre-mortem)
Phase 4: Confirmation (confirm-operation)
Phase 5: Execution (with verify-evidence, detect-infinite-loop, manage-context)
🆕 Phase 5.5: Iterative Phase Review (iterative-phase-review) ← NEW
Phase 6: Reflection (error-reflection)
Phase 7: Completion (declare-complete)
Phase 8: Pattern Update (pattern-library update)
```

---

## Phase 5.5 Specification

### Purpose
Review task deliverables with multi-methodology convergence before declaring complete.

### When to Run
- **Always:** After Phase 5 (execution) completes
- **Condition:** If task produced deliverables (code, docs, config, etc.)
- **Skip:** Only if task was pure research/exploration with no artifacts

### Skill Used
`iterative-phase-review`

### Configuration
```javascript
{
  phase: {
    name: taskContext.phase || 'execution',
    scope: taskContext.deliverableTypes || ['implementation', 'tests', 'docs']
  },
  deliverables: identifyDeliverables(taskResult),
  requirements: taskContext.requirements || extractFromClarification()
}
```

### Expected Outcome
- **converged: true** → Proceed to Phase 6 (Reflection)
- **converged: false** → Either:
  1. Return to Phase 5 (fix issues and re-execute)
  2. Escalate to user (if max iterations exceeded)

---

## Integration Steps

### Step 1: Update Phase List (Line ~76)

**Current:**
```markdown
## Battle-Plan Phases

### Phase 1: Clarification
### Phase 2: Knowledge Check
### Phase 3: Risk Assessment
### Phase 4: Confirmation
### Phase 5: Execution (with Monitoring)
### Phase 6: Reflection
### Phase 7: Completion
### Phase 8: Pattern Update
```

**Updated:**
```markdown
## Battle-Plan Phases

### Phase 1: Clarification
### Phase 2: Knowledge Check
### Phase 3: Risk Assessment
### Phase 4: Confirmation
### Phase 5: Execution (with Monitoring)
### Phase 5.5: Iterative Phase Review (NEW)
### Phase 6: Reflection
### Phase 7: Completion
### Phase 8: Pattern Update
```

### Step 2: Add Phase 5.5 Section (After Phase 5, Before Phase 6)

**Insert Location:** After line ~251 (end of Phase 5 example), before Phase 6

**Content to Add:**

```markdown
### Phase 5.5: Iterative Phase Review

**Skill:** iterative-phase-review

**Purpose:** Multi-methodology quality gate on task deliverables

**When:** After execution completes, if deliverables produced

**Process:**
1. Identify deliverables (code, tests, docs, config, etc.)
2. Extract requirements from Phase 1 clarification
3. Run iterative phase review with 8 methodologies:
   - Top-Down-Requirements (completeness)
   - Top-Down-Architecture (alignment)
   - Bottom-Up-Quality (quality standards)
   - Bottom-Up-Consistency (internal consistency)
   - Lateral-Integration (component interfaces)
   - Lateral-Security (security implementation)
   - Lateral-Performance (performance characteristics)
   - Lateral-UX (user experience)
4. Random methodology selection (no reuse in clean sequence)
5. Context cleared between passes (fresh perspective)
6. Converge until 3 consecutive clean passes
7. If issues found → fix and iterate
8. If converged → proceed to Phase 6

**Configuration:**
- Model: claude-opus-4-5 (highest quality)
- Clean passes required: 3 consecutive
- Max iterations: 10
- Context clearing: true (fresh reviews)

**Output:** Convergence result, issues found/fixed, learning captured

**Example:**
```
PHASE 5.5: ITERATIVE PHASE REVIEW

Deliverables identified:
├─ src/auth/oauth.js (implementation)
├─ tests/auth/oauth.test.js (tests)
├─ docs/auth.md (documentation)
└─ config/oauth-config.json (configuration)

Requirements (from Phase 1):
├─ OAuth authentication with Google
├─ Session management with Redis
├─ Token caching for performance
└─ Security best practices

═══ PHASE REVIEW: execution ═══
Model: claude-opus-4-5

Pass 1: Lateral-Security (random selection)
  → Found 2 issues:
    - Token not validated on refresh
    - CSRF protection missing
  ✗ Issues found, fixing...
  → Fixed 2 issues
  → Clean sequence reset

Pass 2: Bottom-Up-Quality (random selection)
  → Found 1 issue:
    - Missing error handling in token refresh
  ✗ Issues found, fixing...
  → Fixed 1 issue
  → Clean sequence reset

Pass 3: Top-Down-Requirements (random selection)
  → All requirements validated ✓
  ✓ Clean pass 1/3
  → Methodology 'Top-Down-Requirements' marked as used

Pass 4: Lateral-Performance (random selection)
  → Caching verified, no bottlenecks ✓
  ✓ Clean pass 2/3
  → Methodology 'Lateral-Performance' marked as used

Pass 5: Bottom-Up-Consistency (random selection)
  → Naming consistent, patterns uniform ✓
  ✓ Clean pass 3/3
  → Methodology 'Bottom-Up-Consistency' marked as used

═══ CONVERGENCE COMPLETE ✓ ═══
Total passes: 5
Issues found: 3
Issues fixed: 3
Clean passes: 3/3

Learnings captured:
├─ Antipattern: Missing CSRF on OAuth endpoints
├─ Prevention: Add CSRF check to authentication checklist
└─ Pattern library updated ✓

→ Proceeding to Phase 6 (Reflection)
```

**Skip Condition:**
```
If no deliverables produced (pure research/exploration):
  → Skip Phase 5.5
  → Proceed directly to Phase 6
```

**Failure Handling:**
```
If convergence fails (max iterations exceeded):
  → Escalate to user
  → Present unresolved issues
  → Options:
    1. Manual fixes + re-run Phase 5.5
    2. Accept issues + document technical debt
    3. Abort task
```
```

### Step 3: Update Core Concept Diagram (Line ~47)

**Current:**
```markdown
**Battle-Plan Workflow:**
```
User Request →
  CLARIFY (understand) →
  CHECK PATTERNS (learn from past) →
  PRE-MORTEM (anticipate failures) →
  CONFIRM (get approval) →
  EXECUTE (with monitoring) →
  REFLECT (analyze results) →
  COMPLETE (declare done) →
  UPDATE PATTERNS (feed back to library)
```
```

**Updated:**
```markdown
**Battle-Plan Workflow:**
```
User Request →
  CLARIFY (understand) →
  CHECK PATTERNS (learn from past) →
  PRE-MORTEM (anticipate failures) →
  CONFIRM (get approval) →
  EXECUTE (with monitoring) →
  REVIEW (multi-methodology convergence) → ← NEW
  REFLECT (analyze results) →
  COMPLETE (declare done) →
  UPDATE PATTERNS (feed back to library)
```
```

### Step 4: Update Execution Flow Example (Optional - if full flow example exists)

If there's a complete workflow example in the SKILL.md, add Phase 5.5 execution to it.

---

## Benefits of Phase 5.5 Integration

### 1. Quality Gate Before Completion
- Catches issues before declaring task done
- Prevents incomplete deliverables from passing
- Multi-methodology ensures comprehensive review

### 2. Fresh Perspective
- Context cleared between passes
- Random methodology selection
- No cumulative blindness

### 3. Highest Quality Reviews
- Claude Opus 4.5 for all reviews
- Worth the cost at critical checkpoints
- Better than human review for consistency

### 4. Compound Learning
- Issues feed into pattern library
- Prevention measures applied to future tasks
- Antipatterns identified and documented

### 5. Consistent with Battle-Plan Philosophy
- Fits naturally between execution and reflection
- Maintains learning-first approach
- Complements existing monitoring (verify-evidence, etc.)

---

## Impact on Battle-Plan Behavior

### No Impact (Existing Phases)
- Phase 1-5: Unchanged
- Phase 6-8: Unchanged (except now receive validated deliverables)

### New Behavior (Phase 5.5)
- **When:** Automatically after Phase 5 if deliverables exist
- **Duration:** 10-35 minutes (depends on deliverable complexity)
- **Model:** Claude Opus 4.5 (higher cost, higher quality)
- **Result:** Either converged (proceed) or failed (escalate/retry)

### User Experience
- **Transparent:** User sees Phase 5.5 execution in progress
- **Informative:** Shows methodology being used, issues found
- **Actionable:** Clear next steps if convergence fails

---

## Testing Phase 5.5 Integration

### Test Case 1: Simple Task (Converges Quickly)

**Input:**
```javascript
Task: "Add health check endpoint"
Deliverables:
  - src/routes/health.js
  - tests/routes/health.test.js
Requirements:
  - Return 200 OK if service healthy
  - Include database connection status
```

**Expected:**
- Pass 1-2: Find minor issues (error handling, test coverage)
- Pass 3-5: Achieve 3 clean passes
- Total time: ~10 minutes
- Result: converged = true

### Test Case 2: Complex Task (Multiple Iterations)

**Input:**
```javascript
Task: "Implement OAuth authentication"
Deliverables:
  - src/auth/oauth.js
  - tests/auth/oauth.test.js
  - config/oauth-config.json
  - docs/auth.md
Requirements:
  - OAuth with Google and GitHub
  - Session management
  - Token refresh
  - Security best practices
```

**Expected:**
- Pass 1-3: Find security issues, missing validation
- Pass 4-6: Find consistency issues, documentation gaps
- Pass 7-9: Achieve 3 clean passes
- Total time: ~25-35 minutes
- Result: converged = true

### Test Case 3: Research Task (No Deliverables)

**Input:**
```javascript
Task: "Research OAuth providers"
Deliverables: None (pure research)
```

**Expected:**
- Phase 5.5 skipped (no deliverables)
- Proceeds directly to Phase 6
- Total time: 0 minutes

### Test Case 4: Failed Convergence

**Input:**
```javascript
Task: "Add complex feature"
Deliverables: Multiple files
Issue: Architectural mismatch with requirements
```

**Expected:**
- Pass 1-10: Repeatedly find architectural issues
- Issues not fixable without redesign
- Max iterations (10) exceeded
- Result: converged = false
- User escalation with clear issue summary

---

## Configuration Options

### Default Configuration (Recommended)

```javascript
{
  phaseReview: {
    enabled: true,  // Enable Phase 5.5
    model: 'claude-opus-4-5',
    convergence: {
      requiredCleanPasses: 3,
      maxIterations: 10,
      clearContextBetweenPasses: true
    },
    skipIfNoDeliverables: true
  }
}
```

### Custom Configuration

```javascript
{
  phaseReview: {
    enabled: true,
    model: 'claude-sonnet-4-5',  // Use sonnet instead (faster, cheaper)
    convergence: {
      requiredCleanPasses: 2,     // Lower bar (faster)
      maxIterations: 15,           // More attempts
      clearContextBetweenPasses: false  // Keep context
    },
    skipIfNoDeliverables: true,
    methodologyPool: 'custom',    // Use custom methodologies
    methodologies: [...]          // Define custom methodologies
  }
}
```

---

## Rollout Strategy

### Phase 1: Soft Launch (Week 2, Day 1-2)
- Add Phase 5.5 to battle-plan SKILL.md
- Test with simple tasks
- Monitor convergence rates
- Gather initial feedback

### Phase 2: Integration Testing (Week 2, Day 3-4)
- Test with windows-app-orchestrator
- Test with corpus-hub workflows
- Test with content creation workflows
- Verify pattern library integration

### Phase 3: Documentation Update (Week 2, Day 5)
- Update battle-plan README
- Update battle-plan CHANGELOG
- Update integration documentation
- Create user guide for Phase 5.5

### Phase 4: Production (Week 3)
- Enable by default for all battle-plan executions
- Monitor effectiveness metrics
- Iterate based on real-world usage

---

## Success Metrics

### Primary Metrics
- **Convergence Rate:** 80%+ tasks converge within 10 iterations
- **Issue Detection:** 70%+ tasks have issues found in Phase 5.5
- **False Positives:** <10% clean tasks flagged with issues

### Secondary Metrics
- **Time to Convergence:** Average 5-7 passes
- **Issues per Task:** Average 3-8 issues found
- **Pattern Library Growth:** 1-3 antipatterns per task

### Learning Metrics
- **Issue Recurrence:** Decreases over time (compound learning)
- **Prevention Effectiveness:** 60%+ of identified prevention measures work
- **User Satisfaction:** Positive feedback on quality improvements

---

## Troubleshooting

### Problem: Phase 5.5 Taking Too Long

**Symptoms:** Convergence takes >15 iterations, >45 minutes

**Causes:**
- Deliverables too complex
- Requirements ambiguous
- Architectural misalignment

**Solutions:**
1. Break task into smaller subtasks
2. Improve Phase 1 (clarification)
3. Lower convergence bar (requiredCleanPasses: 2)
4. Use sonnet instead of opus (faster)

### Problem: Phase 5.5 Finding Too Many False Positives

**Symptoms:** Clean code flagged with "issues"

**Causes:**
- Methodology too strict
- Context not preserved properly
- Hallucinated issues

**Solutions:**
1. Strengthen verify-evidence checks
2. Adjust methodology executors
3. Improve issue validation

### Problem: Phase 5.5 Missing Real Issues

**Symptoms:** Issues slip through, found later

**Causes:**
- Methodology pool too narrow
- Insufficient methodologies
- Specific domain not covered

**Solutions:**
1. Expand methodology pool
2. Add domain-specific methodologies
3. Strengthen specific methodology executors

---

## Next Steps

1. **Immediate:** Integrate Phase 5.5 into battle-plan SKILL.md
2. **Day 2:** Test Phase 5.5 with simple task
3. **Day 3:** Integrate into windows-app-orchestrator
4. **Day 4:** Test end-to-end workflows
5. **Day 5:** Update all documentation

---

## File Changes Required

### Modified Files
1. `core/learning/orchestrators/battle-plan/SKILL.md`
   - Add Phase 5.5 to phase list
   - Add Phase 5.5 detailed section
   - Update workflow diagram
   - Update examples

2. `core/learning/orchestrators/battle-plan/README.md`
   - Update phase count (8 → 9 phases including 5.5)
   - Add Phase 5.5 to quick reference

3. `core/learning/orchestrators/battle-plan/CHANGELOG.md`
   - Document Phase 5.5 addition
   - Version bump to v2.1.0

### No Changes Required
- All other battle-plan variant files (corpus-battle-plan, audit-battle-plan, content-battle-plan)
- These can adopt Phase 5.5 independently

---

*Integration Guide Created: 2026-02-05*
*Ready for Implementation: Week 2, Day 1-2*
*Part of v4.0 Universal Skills Ecosystem - Learning Integration*
