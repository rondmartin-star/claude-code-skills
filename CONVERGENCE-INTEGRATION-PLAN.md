# Convergence Pattern Integration Plan

**Date:** 2026-02-04
**Purpose:** Unify phase review convergence and audit convergence into shared pattern
**Status:** 📋 PLANNING

---

## Problem Statement

We currently have (or are planning) TWO separate convergence implementations:

**1. Audit Convergence (existing)**
- Location: `core/audit/convergence-engine/`
- Purpose: Iterative audit fixing until 3 clean GATE passes
- Methodologies: 3 audit methodologies (technical/user/holistic)
- Convergence: Run audits → Fix issues → Repeat until 3 clean passes

**2. Phase Review Convergence (planned)**
- Location: `core/learning/phase-transition/iterative-phase-review/`
- Purpose: Iterative phase review until 3 clean passes
- Methodologies: 3 review approaches (top-down/bottom-up/lateral)
- Convergence: Review phase → Fix issues → Repeat until 3 clean passes

**Key Observation:** These are the SAME PATTERN with different:
- Subject matter (code vs deliverables)
- Methodologies (audit types vs review approaches)
- Timing (pre-release vs phase transitions)

**Duplication:** ~80% of the convergence logic would be duplicated

---

## Proposed Solution: Unified Convergence Pattern

Extract the convergence pattern into a reusable component that both use.

### Architecture

```
convergence-pattern (NEW - shared)
    ├─ Generic convergence algorithm
    ├─ 3-pass clean requirement
    ├─ Methodology rotation
    ├─ verify-evidence integration
    ├─ error-reflection integration
    ├─ pattern-library integration
    └─ Configuration system

        ↓ Used by ↓

audit-convergence                    phase-review-convergence
├─ Audit-specific config             ├─ Review-specific config
├─ Methodologies:                    ├─ Methodologies:
│  - technical                       │  - top-down
│  - user                            │  - bottom-up
│  - holistic                        │  - lateral
├─ Subject: Code/issues              ├─ Subject: Deliverables/artifacts
└─ Timing: Pre-release               └─ Timing: Phase transitions
```

---

## Design: Generic Convergence Pattern

### Core Component: convergence-pattern

**Location:** `core/learning/convergence/convergence-pattern/`

**Purpose:** Reusable convergence algorithm for any multi-methodology quality process

**Interface:**

```javascript
async function runConvergence(config) {
  return await convergencePattern.execute({
    // What we're converging
    subject: {
      type: 'audit' | 'phase-review' | 'custom',
      data: /* subject-specific data */
    },

    // How we check it
    methodologies: [
      { name: 'methodology-a', executor: async (subject) => {...} },
      { name: 'methodology-b', executor: async (subject) => {...} },
      { name: 'methodology-c', executor: async (subject) => {...} }
    ],

    // How we verify clean
    verifyClean: async (result) => {
      return await verify_evidence.check({
        claim: "Subject is clean",
        evidence: result.evidence
      });
    },

    // How we fix issues
    fixIssues: async (issues) => {
      /* subject-specific fix logic */
    },

    // Convergence parameters
    convergence: {
      requiredCleanPasses: 3,
      maxPasses: 10,
      rotateMethodologies: true,
      clearContextBetweenPasses: true
    },

    // Learning integration
    learning: {
      logToPatternLibrary: true,
      runErrorReflection: true,
      trackMetrics: true
    }
  });
}
```

---

## Convergence Algorithm (Generic)

```javascript
async function executeConvergence(config) {
  const state = {
    passes: [],
    consecutiveClean: 0,
    issues: [],
    currentMethodologyIndex: 0,
    totalIssuesFixed: 0
  };

  // Optional: Set model for high-quality execution
  if (config.model) {
    setModel(config.model);
  }

  console.log(`\n═══ CONVERGENCE: ${config.subject.type} ═══`);
  console.log(`Required clean passes: ${config.convergence.requiredCleanPasses}`);
  console.log(`Methodologies: ${config.methodologies.map(m => m.name).join(', ')}`);

  while (state.consecutiveClean < config.convergence.requiredCleanPasses
         && state.passes.length < config.convergence.maxPasses) {

    const passNumber = state.passes.length + 1;
    const methodology = config.methodologies[state.currentMethodologyIndex];

    console.log(`\n--- Pass ${passNumber}: ${methodology.name} ---`);

    // Optional: Clear context between passes
    if (config.convergence.clearContextBetweenPasses) {
      await manage_context.clear_context({
        preserve: config.convergence.preserveData || []
      });
    }

    // Execute methodology
    const result = await methodology.executor(config.subject.data);

    // Verify if clean
    const isClean = await config.verifyClean(result);

    if (isClean) {
      state.consecutiveClean++;
      console.log(`✓ Clean pass ${state.consecutiveClean}/${config.convergence.requiredCleanPasses}`);

      // Rotate to next methodology
      if (config.convergence.rotateMethodologies) {
        state.currentMethodologyIndex =
          (state.currentMethodologyIndex + 1) % config.methodologies.length;
      }

    } else {
      // Issues found - reset consecutive counter
      console.log(`✗ Issues found: ${result.issues.length}`);
      state.consecutiveClean = 0;
      state.issues.push(...result.issues);

      // Run error-reflection on issues
      if (config.learning.runErrorReflection) {
        const reflection = await error_reflection.analyze(result.issues);

        // Log to pattern library
        if (config.learning.logToPatternLibrary) {
          await pattern_library.update({
            antipatterns: reflection.antipatterns,
            prevention: reflection.prevention_measures
          });
        }
      }

      // Fix issues
      const fixResult = await config.fixIssues(result.issues);
      state.totalIssuesFixed += fixResult.fixed;
    }

    state.passes.push({
      passNumber,
      methodology: methodology.name,
      isClean,
      issuesFound: result.issues?.length || 0
    });
  }

  // Convergence result
  const converged = state.consecutiveClean >= config.convergence.requiredCleanPasses;

  console.log(`\n═══ CONVERGENCE ${converged ? 'COMPLETE' : 'FAILED'} ═══`);
  console.log(`Total passes: ${state.passes.length}`);
  console.log(`Issues found: ${state.issues.length}`);
  console.log(`Issues fixed: ${state.totalIssuesFixed}`);
  console.log(`Clean passes: ${state.consecutiveClean}/${config.convergence.requiredCleanPasses}`);

  return {
    converged,
    passes: state.passes,
    issues: state.issues,
    issuesFixed: state.totalIssuesFixed,
    cleanPasses: state.consecutiveClean
  };
}
```

---

## Usage: Audit Convergence

**File:** `core/audit/convergence-engine/SKILL.md`

**Changes:** Use convergence-pattern instead of custom logic

```javascript
async function runAuditConvergence(projectPath) {
  // Load convergence pattern
  const convergencePattern = await loadSkill('convergence-pattern');

  // Configure for audit convergence
  const result = await convergencePattern.execute({
    // Subject: Code and issues
    subject: {
      type: 'audit',
      data: { projectPath, audits: getApplicableAudits() }
    },

    // Methodologies: Technical, User, Holistic
    methodologies: [
      {
        name: 'technical',
        executor: async (data) => {
          return await runAudits(data, ['security', 'code-quality', 'performance']);
        }
      },
      {
        name: 'user',
        executor: async (data) => {
          return await runAudits(data, ['accessibility', 'ux-performance']);
        }
      },
      {
        name: 'holistic',
        executor: async (data) => {
          return await runAudits(data, ['consistency', 'navigation', 'documentation']);
        }
      }
    ],

    // Verify clean: All audits pass
    verifyClean: async (result) => {
      return await verify_evidence.check({
        claim: "All audits pass",
        evidence: [
          `All methodologies: ${result.issues.length} issues`,
          "No critical or high issues",
          "All audits completed successfully"
        ]
      });
    },

    // Fix issues: Use fix-planner
    fixIssues: async (issues) => {
      const plan = await generateFixPlan(issues);
      return await implementFixes(plan);
    },

    // Convergence config
    convergence: {
      requiredCleanPasses: 3,
      maxPasses: 10,
      rotateMethodologies: true,
      clearContextBetweenPasses: false  // Keep audit context
    },

    // Learning config
    learning: {
      logToPatternLibrary: true,
      runErrorReflection: true,
      trackMetrics: true
    }
  });

  return result;
}
```

---

## Usage: Phase Review Convergence

**File:** `core/learning/phase-transition/iterative-phase-review/SKILL.md`

**Implementation:** Use convergence-pattern

```javascript
async function runPhaseReview(phase, deliverables) {
  // Load convergence pattern
  const convergencePattern = await loadSkill('convergence-pattern');

  // Configure for phase review
  const result = await convergencePattern.execute({
    // Subject: Phase deliverables
    subject: {
      type: 'phase-review',
      data: { phase, deliverables, requirements: phase.requirements }
    },

    // Methodologies: Top-Down, Bottom-Up, Lateral
    methodologies: [
      {
        name: 'top-down',
        executor: async (data) => {
          return await reviewTopDown(data.phase, data.deliverables);
        }
      },
      {
        name: 'bottom-up',
        executor: async (data) => {
          return await reviewBottomUp(data.deliverables);
        }
      },
      {
        name: 'lateral',
        executor: async (data) => {
          return await reviewLateral(data.phase, data.deliverables);
        }
      }
    ],

    // Verify clean: Phase is complete and consistent
    verifyClean: async (result) => {
      return await verify_evidence.check({
        claim: `Phase ${phase.name} is complete`,
        evidence: result.evidence
      });
    },

    // Fix issues: Update deliverables
    fixIssues: async (issues) => {
      return await fixPhaseIssues(phase, deliverables, issues);
    },

    // Convergence config
    convergence: {
      requiredCleanPasses: 3,
      maxPasses: 10,
      rotateMethodologies: true,
      clearContextBetweenPasses: true  // Clear context for fresh reviews
    },

    // Learning config
    learning: {
      logToPatternLibrary: true,
      runErrorReflection: true,
      trackMetrics: true
    },

    // Model config
    model: 'claude-opus-4-5'  // Use opus for high-quality reviews
  });

  return result;
}
```

---

## Benefits of Integration

### 1. Code Reuse
- **Before:** 2 implementations of convergence logic (~500 lines each)
- **After:** 1 shared implementation (~600 lines total)
- **Savings:** ~400 lines of code, easier maintenance

### 2. Consistency
- Same convergence behavior across all use cases
- Same verify-evidence integration
- Same error-reflection integration
- Same pattern-library updates

### 3. Extensibility
- Add new convergence use cases easily (e.g., documentation review, security review)
- Each new use case = configure methodologies, don't rewrite convergence
- Example: Could add "architecture convergence" for design reviews

### 4. Testing
- Test convergence logic once
- Each use case only tests its specific methodologies
- Reduced test surface area

### 5. Learning
- Pattern library captures convergence patterns regardless of use case
- Metrics tracked consistently
- Antipatterns identified uniformly

---

## Migration Path

### Phase 1: Create convergence-pattern Skill

**Week 1:**
1. Extract convergence logic from existing convergence-engine
2. Make it generic and configurable
3. Test standalone with mock methodologies
4. Document interface and usage

**Deliverable:** `core/learning/convergence/convergence-pattern/SKILL.md`

---

### Phase 2: Update Audit Convergence

**Week 1:**
1. Refactor convergence-engine to use convergence-pattern
2. Define audit-specific methodologies
3. Test audit convergence still works
4. Update documentation

**Deliverable:** Updated `core/audit/convergence-engine/SKILL.md`

---

### Phase 3: Create Phase Review Using Pattern

**Week 2:**
1. Create iterative-phase-review skill
2. Use convergence-pattern as base
3. Define review-specific methodologies
4. Test phase reviews
5. Document usage

**Deliverable:** `core/learning/phase-transition/iterative-phase-review/SKILL.md`

---

### Phase 4: Integration and Testing

**Week 2:**
1. Test audit convergence with convergence-pattern
2. Test phase review with convergence-pattern
3. Test both in same workflow
4. Verify pattern library integration
5. Update all documentation

**Deliverable:** Fully integrated and tested system

---

## Configuration Schema

### convergence-pattern Config

```json
{
  "convergencePattern": {
    "defaults": {
      "requiredCleanPasses": 3,
      "maxPasses": 10,
      "rotateMethodologies": true,
      "clearContextBetweenPasses": false,
      "model": null
    },
    "learning": {
      "logToPatternLibrary": true,
      "runErrorReflection": true,
      "trackMetrics": true
    }
  }
}
```

### audit-convergence Config

```json
{
  "auditConvergence": {
    "extends": "convergencePattern",
    "convergence": {
      "requiredCleanPasses": 3,
      "clearContextBetweenPasses": false
    },
    "methodologies": ["technical", "user", "holistic"]
  }
}
```

### phase-review Config

```json
{
  "phaseReview": {
    "extends": "convergencePattern",
    "convergence": {
      "requiredCleanPasses": 3,
      "clearContextBetweenPasses": true
    },
    "methodologies": ["top-down", "bottom-up", "lateral"],
    "model": "claude-opus-4-5"
  }
}
```

---

## Comparison: Before vs After

### Before Integration

```
audit-convergence (500 lines)
├─ Convergence algorithm
├─ verify-evidence integration
├─ error-reflection integration
├─ pattern-library integration
├─ Audit-specific logic
└─ Technical/User/Holistic methodologies

phase-review (500 lines)
├─ Convergence algorithm        ← DUPLICATE
├─ verify-evidence integration  ← DUPLICATE
├─ error-reflection integration ← DUPLICATE
├─ pattern-library integration  ← DUPLICATE
├─ Review-specific logic
└─ Top-Down/Bottom-Up/Lateral methodologies
```

### After Integration

```
convergence-pattern (400 lines)
├─ Generic convergence algorithm
├─ verify-evidence integration
├─ error-reflection integration
├─ pattern-library integration
└─ Configuration system

    ↓ Used by ↓

audit-convergence (150 lines)        phase-review (150 lines)
├─ Configure convergence-pattern     ├─ Configure convergence-pattern
├─ Audit-specific logic              ├─ Review-specific logic
└─ Methodologies                     └─ Methodologies
```

**Total:** 700 lines vs 1000 lines (30% reduction)

---

## Example: New Use Case (Architecture Review)

With convergence-pattern, adding a new convergence use case is simple:

```javascript
async function runArchitectureReview(architecture) {
  const convergencePattern = await loadSkill('convergence-pattern');

  return await convergencePattern.execute({
    subject: {
      type: 'architecture-review',
      data: { architecture, requirements, constraints }
    },

    methodologies: [
      { name: 'scalability', executor: reviewScalability },
      { name: 'security', executor: reviewSecurityArchitecture },
      { name: 'maintainability', executor: reviewMaintainability }
    ],

    verifyClean: async (result) => {
      return result.issues.length === 0;
    },

    fixIssues: async (issues) => {
      return await updateArchitecture(issues);
    },

    convergence: {
      requiredCleanPasses: 3,
      maxPasses: 10
    }
  });
}
```

**Implementation:** ~50 lines (vs 500 lines if building from scratch)

---

## Recommendation

**Strongly recommend integrating** for these reasons:

1. **DRY Principle:** Don't repeat the convergence logic
2. **Consistency:** Same behavior across all convergence use cases
3. **Maintainability:** Fix bugs once, benefits all use cases
4. **Extensibility:** Easy to add new convergence types
5. **Learning:** Pattern library captures convergence patterns uniformly

**Implementation Order:**
1. Create convergence-pattern (Week 1)
2. Refactor audit convergence to use it (Week 1)
3. Create phase review using it (Week 2)
4. Test and document (Week 2)

**Total Effort:** ~2 weeks (vs ~3 weeks if building separately)

---

## Updated Implementation Plan

### Revised Phase Review Integration Plan

**Changes to PHASE-REVIEW-INTEGRATION-PLAN.md:**

1. **Architecture section:** Use convergence-pattern instead of custom logic
2. **Implementation Phase 1:** Create convergence-pattern FIRST
3. **Implementation Phase 2:** Refactor audit convergence to use it
4. **Implementation Phase 3:** Create phase review using it
5. **Benefits section:** Add code reuse and consistency benefits

**New Timeline:**
- Week 1: convergence-pattern + audit refactor
- Week 2: phase review + other integrations
- Week 3: Testing + documentation

**Net Result:** Same functionality, less code, more maintainable

---

*End of Convergence Integration Plan*
*Recommendation: INTEGRATE - significant benefits, minimal additional effort*
*Next: Approve integration approach and update implementation plan*
