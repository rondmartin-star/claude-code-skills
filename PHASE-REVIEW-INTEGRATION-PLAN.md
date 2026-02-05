# Iterative Phase Review Integration Plan

**Status:** 📋 PLANNING
**Date:** 2026-02-04
**Purpose:** Integrate rigorous phase review sequence into development workflows
**Model:** Claude Opus 4.5 (highest quality for reviews)

---

## Executive Summary

This plan integrates a systematic 3-pass iterative review sequence at every phase transition in development workflows. Each phase completion triggers an automated review cycle that identifies inconsistencies and gaps before proceeding. This ensures quality compounds through the development process and feeds learnings back to the pattern library.

**Key Innovation:** Multi-methodology review convergence (similar to audit convergence, but for phase quality)

---

## Requirements Analysis

### Core Requirements

1. **Model Selection:** Use Claude Opus 4.5 for all reviews (highest quality)
2. **Context Management:** Clear context between review passes to avoid contamination
3. **Review Tool:** Use /ultrathink for deep analysis
4. **Convergence:** 3 consecutive clean passes required
5. **Methodology Diversity:** Each clean pass uses different review methodology/order
6. **Learning Integration:** Feed issues to pattern-library as antipatterns
7. **Prevention Tracking:** Identify detection and prevention measures
8. **Flow Control:** Suggest next phase only after clean convergence

### Integration Points

**Primary:**
- Windows app development flow (5 phase transitions)
- Battle-plan workflow (between 8 phases)

**Secondary:**
- America 4.0 review/edit/author workflows
- CorpusHub development workflows
- Any multi-phase development process

### Success Criteria

- ✓ Reviews catch 95%+ of issues before next phase
- ✓ No major rework needed in later phases
- ✓ Pattern library grows with prevention measures
- ✓ Developer confidence in phase quality

---

## Architecture Design

### Component Overview

```
Phase Completion
    ↓
Phase Review Gate (NEW)
    ├─ Set model: opus
    ├─ Clear context
    ├─ Review Pass 1 (Methodology A)
    ├─ Review Pass 2 (Methodology B)
    ├─ Review Pass 3 (Methodology C)
    ├─ Verify 3 clean passes
    ├─ Log issues to pattern-library
    └─ Suggest next phase
    ↓
Next Phase Begins
```

### New Component: iterative-phase-review

**Location:** `core/learning/phase-transition/iterative-phase-review/`

**Type:** Learning Skill (Phase Transition Gate)

**Purpose:** Ensure phase quality before proceeding to next phase

**Dependencies:**
- verify-evidence (confirm clean passes)
- error-reflection (analyze issues found)
- pattern-library (log antipatterns and prevention measures)
- manage-context (clear context between passes)

### Integration Architecture

```
Windows App Orchestrator
    ↓
Phase 1: Requirements
    ↓
Phase Review Gate ← iterative-phase-review
    [3-pass review of requirements]
    ↓
Phase 2: System Design
    ↓
Phase Review Gate ← iterative-phase-review
    [3-pass review of system design]
    ↓
Phase 3: UI Design
    ↓
[... continues for all phases]
```

**Battle-Plan Integration:**

```
Battle-Plan Phase 5: Execution Complete
    ↓
Phase Review Gate ← iterative-phase-review
    [Review execution quality]
    ↓
Battle-Plan Phase 6: Error Reflection (if issues found)
    ↓
Battle-Plan Phase 7: Declare Complete
```

---

## Review Methodologies

### Methodology A: Top-Down Completeness Review

**Focus:** Requirements → Implementation (did we build what was specified?)

**Review Order:**
1. Original requirements/goals for this phase
2. Deliverables produced in this phase
3. Gap analysis (missing elements)
4. Consistency with prior phases
5. Readiness for next phase

**Questions:**
- Are all requirements from phase scope met?
- Are deliverables complete and correct?
- What's missing that should be present?
- Do deliverables align with previous phase outputs?
- Is next phase blocked by anything?

**Best For:** Catching missing features, incomplete implementations

---

### Methodology B: Bottom-Up Quality Review

**Focus:** Implementation → Quality (is what we built high quality?)

**Review Order:**
1. Individual deliverables (files, artifacts, code)
2. Internal consistency within each deliverable
3. Cross-deliverable consistency
4. Quality metrics (tests, coverage, errors)
5. Integration points

**Questions:**
- Is each deliverable internally consistent?
- Are naming conventions followed?
- Do components integrate correctly?
- Are quality standards met (tests, docs, etc.)?
- Are there technical debt or shortcuts taken?

**Best For:** Catching quality issues, technical debt, inconsistencies

---

### Methodology C: Lateral Integration Review

**Focus:** Cross-cutting concerns (does everything fit together?)

**Review Order:**
1. Cross-phase dependencies
2. Architectural alignment
3. Security considerations
4. Performance implications
5. User experience flow

**Questions:**
- Do new components integrate with existing architecture?
- Are security patterns applied correctly?
- Are performance implications considered?
- Does UX flow remain coherent?
- Are all cross-cutting concerns addressed?

**Best For:** Catching integration issues, architectural misalignment

---

## Review Convergence Algorithm

### 3-Pass Convergence

```javascript
async function runPhaseReview(phase, deliverables) {
  const reviewState = {
    passes: [],
    consecutiveClean: 0,
    issues: [],
    methodologies: ['top-down', 'bottom-up', 'lateral'],
    currentMethodologyIndex: 0
  };

  // Set model to opus for highest quality
  setModel('claude-opus-4-5');

  while (reviewState.consecutiveClean < 3 && reviewState.passes.length < 10) {
    const passNumber = reviewState.passes.length + 1;
    const methodology = reviewState.methodologies[reviewState.currentMethodologyIndex];

    console.log(`\n═══ PHASE REVIEW PASS ${passNumber} ═══`);
    console.log(`Methodology: ${methodology}`);
    console.log(`Model: Claude Opus 4.5`);

    // Clear context before each review
    await manage_context.clear_context({
      preserve: ['phase_deliverables', 'phase_requirements']
    });

    // Run review with /ultrathink
    const reviewResult = await runReviewWithUltrathink({
      phase: phase,
      deliverables: deliverables,
      methodology: methodology,
      priorIssues: reviewState.issues
    });

    // Verify evidence of clean pass
    const isClean = await verify_evidence.check({
      claim: `Phase ${phase} is clean`,
      evidence: reviewResult.evidence
    });

    if (isClean) {
      reviewState.consecutiveClean++;
      console.log(`✓ Clean pass ${reviewState.consecutiveClean}/3`);

      // Rotate to next methodology for next clean pass
      reviewState.currentMethodologyIndex =
        (reviewState.currentMethodologyIndex + 1) % reviewState.methodologies.length;

    } else {
      // Issues found - reset consecutive counter
      reviewState.consecutiveClean = 0;
      reviewState.issues.push(...reviewResult.issues);

      console.log(`✗ Issues found: ${reviewResult.issues.length}`);

      // Analyze issues with error-reflection
      const reflection = await error_reflection.analyze(reviewResult.issues);

      // Log to pattern library
      await pattern_library.update({
        antipatterns: reflection.antipatterns,
        prevention: reflection.prevention_measures
      });

      // Fix issues before next pass
      await fixIssues(reviewResult.issues);
    }

    reviewState.passes.push({
      passNumber,
      methodology,
      isClean,
      issuesFound: reviewResult.issues.length
    });
  }

  if (reviewState.consecutiveClean >= 3) {
    console.log(`\n✓ PHASE REVIEW CONVERGED (3 clean passes)`);
    console.log(`  - Total passes: ${reviewState.passes.length}`);
    console.log(`  - Issues found and fixed: ${reviewState.issues.length}`);
    console.log(`\n→ Proceeding to next phase`);
    return { converged: true, issues: reviewState.issues };
  } else {
    console.log(`\n✗ PHASE REVIEW FAILED TO CONVERGE`);
    console.log(`  - Max passes reached`);
    console.log(`  - Manual review required`);
    return { converged: false, issues: reviewState.issues };
  }
}
```

---

## Integration Strategy

### Phase 1: Create iterative-phase-review Skill

**File:** `core/learning/phase-transition/iterative-phase-review/SKILL.md`

**Contents:**
- Review convergence algorithm
- 3 review methodology definitions
- Integration with verify-evidence, error-reflection, pattern-library
- Configuration options
- Examples

**Size Target:** ~12KB (core logic only, methodologies in references/)

---

### Phase 2: Enhance Battle-Plan

**File:** `core/learning/orchestrators/battle-plan/SKILL.md`

**Changes:**
- Add Phase 5.5: Phase Review (after execution, before reflection)
- Integrate iterative-phase-review between phases
- Configuration for when to trigger reviews

**New Flow:**
```
PHASE 5: EXECUTION
    ↓
PHASE 5.5: PHASE REVIEW ← NEW
    [iterative-phase-review runs]
    [3-pass convergence]
    ↓
PHASE 6: ERROR REFLECTION (if issues from review)
    ↓
PHASE 7: DECLARE COMPLETE
```

---

### Phase 3: Update Windows App Orchestrator

**File:** `windows-app/windows-app-orchestrator/SKILL.md`

**Changes:**
- Add phase review gates after each phase:
  - After Requirements → Review requirements completeness
  - After System Design → Review design quality
  - After UI Design → Review UI specifications
  - After Build → Review implementation quality
  - After Supervision → Review deployment readiness

**Configuration:**
```json
{
  "windowsApp": {
    "phaseReviews": {
      "enabled": true,
      "model": "claude-opus-4-5",
      "requiredCleanPasses": 3,
      "methodologies": ["top-down", "bottom-up", "lateral"],
      "phases": {
        "requirements": true,
        "systemDesign": true,
        "uiDesign": true,
        "build": true,
        "supervision": true
      }
    }
  }
}
```

---

### Phase 4: Update Other Orchestrators

**Files to Update:**
- `america40/review/review-orchestrator/`
- `america40/edit/edit-orchestrator/`
- `america40/author/author-orchestrator/`
- `corpus-hub/corpus-hub-orchestrator/`

**Integration Pattern:**
- Add phase review gates at natural transition points
- Use same 3-methodology convergence
- Feed issues to pattern-library

---

## Learning Skills Integration

### Issue Detection and Prevention

**When review finds issues:**

```javascript
// 1. Categorize issue
const issue = {
  type: 'inconsistency' | 'gap' | 'quality' | 'integration',
  phase: 'requirements' | 'design' | 'build' | 'deployment',
  description: "What was wrong",
  impact: "What could have happened",
  detection: "How we found it",
  prevention: "How to avoid in future"
};

// 2. Run error-reflection
const reflection = await error_reflection.analyze([issue]);

// 3. Extract prevention measures
const prevention = {
  checklistItem: "Add to phase checklist",
  verifyEvidenceCheck: "Add to verify-evidence requirements",
  preMortemRisk: "Add to pre-mortem risk database",
  pattern: "Add to pattern library as antipattern"
};

// 4. Update pattern library
await pattern_library.update({
  antipatterns: [{
    id: generate_id(),
    name: issue.type,
    category: issue.phase,
    problem: issue.description,
    prevention: prevention.checklistItem,
    detection: issue.detection,
    occurrences: 1
  }]
});

// 5. Update pre-mortem risk database
await update_risk_database({
  phase: issue.phase,
  risk: issue.description,
  likelihood: calculate_likelihood(issue),
  impact: calculate_impact(issue),
  prevention: issue.prevention
});
```

### Pattern Library Growth

**Example antipattern from review:**

```json
{
  "id": "incomplete-api-design",
  "name": "Incomplete API Design",
  "category": "system-design",
  "problem": "API endpoints defined but request/response schemas missing",
  "detection": "Bottom-up quality review caught missing schemas",
  "prevention": "Add verify-evidence check: 'All API endpoints have request/response schemas'",
  "occurrences": 1,
  "phase": "system-design",
  "tags": ["api", "design", "completeness"]
}
```

**Example prevention measure:**

```json
{
  "phase": "system-design",
  "checklist_addition": "Verify all API endpoints have request/response schemas defined",
  "verify_evidence_check": {
    "claim": "API design is complete",
    "evidence": [
      "All endpoints have request schemas",
      "All endpoints have response schemas",
      "All error codes documented"
    ]
  }
}
```

---

## Example Flows

### Example 1: Windows App - Requirements to System Design

```
User: "Design a Windows app for managing tasks"

═══ PHASE 1: REQUIREMENTS ═══
[windows-app-requirements skill executes]
Output:
  - User stories created
  - Acceptance criteria defined
  - Scope documented

═══ PHASE REVIEW GATE ═══
Model: Claude Opus 4.5

Review Pass 1 (Top-Down Completeness):
  Reviewing requirements against user request...
  Issue found: "No user story for task deletion"
  ✗ Not clean - fixing issue...
  Added: User story for task deletion

Review Pass 2 (Top-Down Completeness - retry):
  Reviewing requirements against user request...
  ✓ All user stories present
  ✓ All acceptance criteria defined
  ✓ Clean pass 1/3

[Context cleared]

Review Pass 3 (Bottom-Up Quality):
  Reviewing individual user stories...
  Issue found: "User story #3 missing acceptance criteria"
  ✗ Not clean - fixing issue...
  Added: Acceptance criteria for user story #3

Review Pass 4 (Bottom-Up Quality - retry):
  Reviewing individual user stories...
  ✓ All user stories have acceptance criteria
  ✓ Naming consistent
  ✓ Clean pass 1/3 (consecutive reset)

[Context cleared]

Review Pass 5 (Bottom-Up Quality - second try):
  ✓ All quality checks pass
  ✓ Clean pass 2/3

[Context cleared]

Review Pass 6 (Lateral Integration):
  Reviewing cross-cutting concerns...
  ✓ Security considerations noted
  ✓ Performance requirements defined
  ✓ Clean pass 3/3

✓ PHASE REVIEW CONVERGED (3 clean passes)
  - Total passes: 6
  - Issues found and fixed: 2
  - Antipatterns logged: 2

Issues logged to pattern library:
  1. missing-user-story-coverage (prevention: checklist for CRUD operations)
  2. incomplete-acceptance-criteria (prevention: verify-evidence check)

→ Proceeding to Phase 2: System Design

═══ PHASE 2: SYSTEM DESIGN ═══
[Process continues...]
```

### Example 2: Battle-Plan with Phase Review

```
User: "Create a newsletter about OAuth"

═══ BATTLE-PLAN: PHASE 5 EXECUTION ═══
[content-creation-ecosystem creates newsletter]

═══ BATTLE-PLAN: PHASE 5.5 PHASE REVIEW ═══
Model: Claude Opus 4.5

Review Pass 1 (Top-Down Completeness):
  Checking newsletter against requirements...
  Issue found: "Missing unsubscribe link"
  ✗ Not clean - fixing...

Review Pass 2 (Top-Down Completeness):
  ✓ All required elements present
  ✓ Clean pass 1/3

[Context cleared]

Review Pass 3 (Bottom-Up Quality):
  Checking content quality...
  Issue found: "Code example on line 42 doesn't run"
  ✗ Not clean - fixing...

Review Pass 4 (Bottom-Up Quality):
  ✓ All code examples tested and work
  ✓ Clean pass 2/3

[Context cleared]

Review Pass 5 (Lateral Integration):
  Checking cross-cutting concerns...
  ✓ Links validated
  ✓ SEO metadata present
  ✓ Clean pass 3/3

✓ PHASE REVIEW CONVERGED (3 clean passes)

Issues logged:
  - missing-unsubscribe-link (added to content-risks.json)
  - untested-code-examples (added to verify-evidence checks)

═══ BATTLE-PLAN: PHASE 7 DECLARE COMPLETE ═══
✓ SHIPPABLE
```

---

## Configuration

### Global Configuration

**File:** `.corpus/learning/config.json` (new file)

```json
{
  "phaseReview": {
    "enabled": true,
    "model": "claude-opus-4-5",
    "requiredCleanPasses": 3,
    "maxPasses": 10,
    "methodologies": {
      "default": ["top-down", "bottom-up", "lateral"],
      "order": "rotate",
      "customMethodologies": []
    },
    "contextManagement": {
      "clearBetweenPasses": true,
      "preserve": ["deliverables", "requirements", "priorIssues"]
    },
    "learningIntegration": {
      "logToPatternLibrary": true,
      "updateRiskDatabase": true,
      "createPreventionMeasures": true
    }
  }
}
```

### Per-Orchestrator Configuration

**Windows App:**
```json
{
  "windowsApp": {
    "phaseReviews": {
      "enabled": true,
      "phases": {
        "requirements": { "enabled": true, "requiredPasses": 3 },
        "systemDesign": { "enabled": true, "requiredPasses": 3 },
        "uiDesign": { "enabled": true, "requiredPasses": 3 },
        "build": { "enabled": true, "requiredPasses": 3 },
        "supervision": { "enabled": true, "requiredPasses": 2 }
      }
    }
  }
}
```

**Battle-Plan:**
```json
{
  "battlePlan": {
    "phaseReview": {
      "enabled": true,
      "reviewAfterExecution": true,
      "requiredPasses": 3
    }
  }
}
```

---

## Migration Strategy

### Phase 1: Create Core Skill (Week 1)

1. Create `iterative-phase-review` skill
2. Define 3 review methodologies
3. Implement convergence algorithm
4. Test standalone

### Phase 2: Battle-Plan Integration (Week 1)

1. Add Phase 5.5 to battle-plan
2. Test with simple task
3. Verify pattern library updates
4. Document integration

### Phase 3: Windows App Integration (Week 2)

1. Add phase review gates to windows-app-orchestrator
2. Test with complete app development flow
3. Verify all 5 phase transitions work
4. Collect initial antipatterns

### Phase 4: Other Orchestrators (Week 2-3)

1. Integrate into america40 orchestrators
2. Integrate into corpus-hub orchestrator
3. Test each integration
4. Document patterns found

### Phase 5: Documentation and Rollout (Week 3)

1. Update CLAUDE.md
2. Create migration guide
3. Update all README files
4. Announce to users

---

## Risk Assessment

### Risk 1: Review Overhead

**Risk:** Phase reviews add significant time to development
**Likelihood:** Medium (3/5)
**Impact:** Medium (3/5)
**Mitigation:**
- Make reviews configurable (can be disabled for rapid prototyping)
- Use opus model only for reviews (high quality, worth the time)
- Cache review results for unchanged phases
- Skip trivial phases (status checks, etc.)

### Risk 2: False Positives

**Risk:** Reviews flag non-issues as problems
**Likelihood:** Medium (3/5)
**Impact:** Low (2/5)
**Mitigation:**
- Use verify-evidence to confirm issues are real
- Allow user override of review findings
- Track false positive rate, refine methodologies
- Learning from false positives improves accuracy over time

### Risk 3: Methodology Overlap

**Risk:** 3 methodologies find the same issues (redundant)
**Likelihood:** Low (2/5)
**Impact:** Low (2/5)
**Mitigation:**
- Design methodologies to be complementary
- Track which methodology finds which issue types
- Refine methodologies based on coverage data
- Allow custom methodology definitions

### Risk 4: Context Clearing Issues

**Risk:** Clearing context loses important information
**Likelihood:** Low (2/5)
**Impact:** Medium (3/5)
**Mitigation:**
- Preserve critical data (deliverables, requirements)
- Document what should be preserved
- Test context preservation thoroughly
- Allow configuration of what to preserve

---

## Success Metrics

### Immediate (Week 1-2)

- ✓ Phase review skill created and tested
- ✓ Battle-plan integration working
- ✓ Windows app integration working
- ✓ At least 5 antipatterns captured

### Short Term (Month 1)

- ✓ 20+ antipatterns in pattern library
- ✓ 90%+ of issues caught before next phase
- ✓ Zero major rework needed in later phases
- ✓ All orchestrators integrated

### Long Term (Quarter 1)

- ✓ 100+ antipatterns with prevention measures
- ✓ Review time decreases as patterns prevent issues
- ✓ Developer confidence in phase quality: 95%+
- ✓ Cross-project pattern sharing working

---

## Implementation Checklist

### Pre-Implementation

- [ ] Review this plan with stakeholders
- [ ] Get approval for architecture
- [ ] Confirm opus model availability
- [ ] Verify /ultrathink integration approach

### Implementation Phase 1

- [ ] Create iterative-phase-review skill
- [ ] Define 3 review methodologies
- [ ] Implement convergence algorithm
- [ ] Test standalone
- [ ] Document skill

### Implementation Phase 2

- [ ] Add Phase 5.5 to battle-plan
- [ ] Test battle-plan integration
- [ ] Verify pattern library updates
- [ ] Create example flows

### Implementation Phase 3

- [ ] Update windows-app-orchestrator
- [ ] Add 5 phase review gates
- [ ] Test complete app development
- [ ] Collect initial antipatterns

### Implementation Phase 4

- [ ] Update america40 orchestrators
- [ ] Update corpus-hub orchestrator
- [ ] Test all integrations
- [ ] Document patterns

### Implementation Phase 5

- [ ] Update documentation
- [ ] Create migration guide
- [ ] Update CLAUDE.md
- [ ] Announce rollout

---

## Questions for Stakeholder Review

1. **Model Selection:** Confirm opus usage for reviews is acceptable (cost vs quality)?
2. **Required Passes:** Is 3 clean passes the right threshold, or should it be configurable?
3. **Methodology Definitions:** Are the 3 methodologies comprehensive enough?
4. **Integration Points:** Are we covering all the right phase transitions?
5. **Override Capability:** Should users be able to skip reviews for rapid prototyping?

---

## Next Steps

### Immediate

1. **Stakeholder Review:** Present this plan for approval
2. **Refinement:** Incorporate feedback
3. **Estimation:** Estimate effort for each phase
4. **Scheduling:** Create implementation timeline

### After Approval

1. **Begin Phase 1:** Create iterative-phase-review skill
2. **Test Thoroughly:** Ensure quality before integration
3. **Iterate:** Refine based on testing
4. **Roll Out:** Follow migration strategy

---

*End of Phase Review Integration Plan*
*Status: 📋 READY FOR REVIEW*
*Next: Stakeholder approval and implementation*
