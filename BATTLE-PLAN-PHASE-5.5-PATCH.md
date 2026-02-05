# Battle-Plan Phase 5.5 Integration Patch

**Date:** 2026-02-05
**Purpose:** Exact patch to add Phase 5.5 to battle-plan SKILL.md
**Location:** `core/learning/orchestrators/battle-plan/SKILL.md`
**Status:** ✅ READY TO APPLY

---

## Patch Instructions

### Location
Insert after line 250 (end of Phase 5 example), before line 252 (start of Phase 6).

### Exact Content to Insert

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

Task: "Implement OAuth authentication"

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
✓ Context cleared for fresh review
  → Found 2 issues:
    - Token not validated on refresh
    - CSRF protection missing
  ✗ Issues found, fixing...
  → Fixed 2 issues
  → Clean sequence reset

Pass 2: Bottom-Up-Quality (random selection)
✓ Context cleared for fresh review
  → Found 1 issue:
    - Missing error handling in token refresh
  ✗ Issues found, fixing...
  → Fixed 1 issue
  → Clean sequence reset

Pass 3: Top-Down-Requirements (random selection)
✓ Context cleared for fresh review
  → All requirements validated ✓
  ✓ Clean pass 1/3
  → Methodology 'Top-Down-Requirements' marked as used

Pass 4: Lateral-Performance (random selection)
✓ Context cleared for fresh review
  → Caching verified, no bottlenecks ✓
  ✓ Clean pass 2/3
  → Methodology 'Lateral-Performance' marked as used

Pass 5: Bottom-Up-Consistency (random selection)
✓ Context cleared for fresh review
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

---

## Additional Updates Required

### 1. Update Phase List (Around Line 76)

**Find:**
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

**Replace with:**
```markdown
## Battle-Plan Phases

### Phase 1: Clarification
### Phase 2: Knowledge Check
### Phase 3: Risk Assessment
### Phase 4: Confirmation
### Phase 5: Execution (with Monitoring)
### Phase 5.5: Iterative Phase Review
### Phase 6: Reflection
### Phase 7: Completion
### Phase 8: Pattern Update
```

### 2. Update Workflow Diagram (Around Line 57)

**Find:**
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

**Replace with:**
```markdown
**Battle-Plan Workflow:**
```
User Request →
  CLARIFY (understand) →
  CHECK PATTERNS (learn from past) →
  PRE-MORTEM (anticipate failures) →
  CONFIRM (get approval) →
  EXECUTE (with monitoring) →
  REVIEW (multi-methodology convergence) →
  REFLECT (analyze results) →
  COMPLETE (declare done) →
  UPDATE PATTERNS (feed back to library)
```
```

### 3. Update CHANGELOG.md

**File:** `core/learning/orchestrators/battle-plan/CHANGELOG.md`

**Add at top:**
```markdown
## [2.1.0] - 2026-02-05

### Added
- Phase 5.5: Iterative Phase Review
  - Multi-methodology quality gate on task deliverables
  - 8 orthogonal review methodologies with random selection
  - Context clearing between passes for fresh perspectives
  - Uses Claude Opus 4.5 for highest quality reviews
  - Integrates with iterative-phase-review skill
  - Automatic skip if no deliverables produced
  - Convergence to 3 consecutive clean passes
  - Full learning integration (pattern library updates)

### Changed
- Battle-plan now has 9 phases (added 5.5 between 5 and 6)
- Workflow diagram updated to include REVIEW step
- Phase completion now validates deliverables before proceeding

### Impact
- Increased quality: Catches issues before declaring complete
- Time impact: +10-20 minutes per task with deliverables
- Compound learning: Antipatterns captured for future tasks
```

### 4. Update README.md

**File:** `core/learning/orchestrators/battle-plan/README.md`

**Find:** Phase count reference (e.g., "8 phases")

**Replace with:** "9 phases (includes Phase 5.5: Iterative Phase Review)"

**Add to Quick Reference:**
```markdown
## Phases

1. Clarification - Understand the task
2. Knowledge Check - Check pattern library
3. Risk Assessment - Run pre-mortem
4. Confirmation - Get user approval
5. Execution - Execute with monitoring
5.5. **Iterative Phase Review** - Multi-methodology quality gate (NEW)
6. Reflection - Analyze errors
7. Completion - Declare done
8. Pattern Update - Update library
```

---

## Validation After Integration

### Checklist

- [ ] Phase 5.5 section added between Phase 5 and Phase 6
- [ ] Phase list updated to include Phase 5.5
- [ ] Workflow diagram updated to include REVIEW step
- [ ] CHANGELOG.md updated with version 2.1.0
- [ ] README.md updated with phase count and quick reference
- [ ] File compiles without errors
- [ ] Cross-references to iterative-phase-review skill correct

### Test

After applying patch:
```bash
# Verify file structure
cat core/learning/orchestrators/battle-plan/SKILL.md | grep "Phase 5.5"

# Should output:
# ### Phase 5.5: Iterative Phase Review

# Verify phase list
cat core/learning/orchestrators/battle-plan/SKILL.md | grep "### Phase" | head -10

# Should include:
# ### Phase 5: Execution (with Monitoring)
# ### Phase 5.5: Iterative Phase Review
# ### Phase 6: Reflection
```

---

## Implementation Status

**Phase 5.5 Content:** ✅ Ready (above)
**Phase List Update:** ✅ Specified
**Workflow Diagram Update:** ✅ Specified
**CHANGELOG.md Update:** ✅ Specified
**README.md Update:** ✅ Specified

**Status:** ✅ PATCH READY TO APPLY

**Estimated Application Time:** 15-20 minutes

---

## Notes

1. **Model Cost:** Phase 5.5 uses Claude Opus 4.5 which has higher cost than default. This is intentional for quality at critical checkpoints.

2. **Time Impact:** Adds 10-20 minutes to task execution when deliverables are produced. This is offset by reduced rework.

3. **Skip Logic:** Phase 5.5 is automatically skipped for research tasks or when no deliverables are produced.

4. **Integration:** Uses `iterative-phase-review` skill which wraps `multi-methodology-convergence` in phase-review mode.

---

*Patch Created: 2026-02-05*
*Target: core/learning/orchestrators/battle-plan/SKILL.md*
*Status: ✅ READY TO APPLY*
*Version After Apply: 2.1.0*
