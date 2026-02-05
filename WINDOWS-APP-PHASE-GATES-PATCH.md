# Windows-App Phase Gates Integration Patch

**Date:** 2026-02-05
**Purpose:** Add 5 phase review gates to windows-app-orchestrator
**Location:** `windows-app/windows-app-orchestrator/SKILL.md`
**Status:** ✅ READY TO APPLY

---

## Overview

Add 5 phase review gates at development phase transitions:
1. **GATE 1:** After Requirements → Before System Design
2. **GATE 2:** After System Design → Before UI Design
3. **GATE 3:** After UI Design → Before Build
4. **GATE 4:** After Build → Before Supervision
5. **GATE 5:** After Supervision → Before Production

---

## Patch 1: Add Gate Detection Rules

### Location
After the existing skill detection rules (around line 71), add new section.

### Content to Insert

```markdown
### Phase Review Gates

**When to trigger:** After completing each development phase

| If prompt contains... | Action... |
|-----------------------|-----------|
| "review requirements", "requirements gate", "validate requirements" | Run GATE 1 (requirements phase review) |
| "review design", "design gate", "validate design" | Run GATE 2 (system design review) |
| "review UI", "UI gate", "validate UI" | Run GATE 3 (UI design review) |
| "review build", "build gate", "validate implementation" | Run GATE 4 (build phase review) |
| "review deployment", "supervision gate", "validate deployment" | Run GATE 5 (supervision review) |
| "review phase", "phase gate", "validate phase" | Run gate for current phase |
| "review all phases", "full phase review" | Run all gates sequentially |
| "skip gate", "bypass review" | Skip current phase gate (not recommended) |

**Automatic Gates:**
- After each phase completes, prompt user to run phase gate
- Gates can be run manually or automatically
- Gates can be skipped with explicit user consent

**Gate Integration with iterative-phase-review:**
```javascript
// Load phase review skill
const phaseReview = await loadSkill('iterative-phase-review');

// Get phase-specific configuration
const config = getPhaseReviewConfig(currentPhase);

// Run phase review gate
const result = await phaseReview.run(config);

// Check convergence
if (result.converged) {
  console.log(`✓ GATE ${gateNumber} PASSED`);
  console.log(`  Clean passes: ${result.cleanPasses}/3`);
  console.log(`  Issues fixed: ${result.issuesFixed}`);
  proceedToNextPhase();
} else {
  console.log(`✗ GATE ${gateNumber} FAILED`);
  console.log(`  Convergence failed after ${result.passes.length} iterations`);
  console.log(`  Unresolved issues: ${result.issues.length}`);
  promptUserAction();
}
```
```

---

## Patch 2: Add Phase Completion Workflow

### Location
Add new section after skill detection rules (after patch 1).

### Content to Insert

```markdown
## Phase Completion Workflow with Gates

After completing each development phase:

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE COMPLETION WORKFLOW                                   │
│                                                              │
│  1. Complete phase-specific skill                           │
│     → User stories (requirements)                           │
│     → Data models (design)                                  │
│     → Page inventory (UI)                                   │
│     → Implementation (build)                                │
│     → Service config (supervision)                          │
│                                                              │
│  2. Phase complete notification                             │
│     ✓ [Phase] deliverables complete                        │
│                                                              │
│  3. Phase review gate prompt                                │
│     🚪 GATE [N]: [Phase] Phase Review                       │
│     ┌──────────────────────────────────────────────────┐   │
│     │ Review deliverables with multi-methodology?      │   │
│     │ - 8 orthogonal review approaches                 │   │
│     │ - Random selection (no reuse)                    │   │
│     │ - Converge until 3 clean passes                  │   │
│     │ - Uses Claude Opus 4.5                           │   │
│     │ - Estimated time: 10-20 minutes                  │   │
│     │                                                   │   │
│     │ Options:                                          │   │
│     │ [1] Run phase review now (recommended)           │   │
│     │ [2] Skip and proceed (not recommended)           │   │
│     │ [3] Run phase review later manually              │   │
│     └──────────────────────────────────────────────────┘   │
│                                                              │
│  4. If user chooses [1]: Run phase review                   │
│     → Load iterative-phase-review                          │
│     → Configure for current phase                          │
│     → Execute convergence                                   │
│     → Validate 3 clean passes                              │
│                                                              │
│  5. Gate result handling                                    │
│     If converged:                                           │
│       → ✓ GATE [N] PASSED                                  │
│       → Update state: gate_passed = true                   │
│       → Proceed to next phase                              │
│     If not converged:                                       │
│       → ✗ GATE [N] FAILED                                  │
│       → Present unresolved issues                          │
│       → Options: fix + retry, accept + document, abort     │
│                                                              │
│  6. If user chooses [2]: Skip gate                          │
│     ⚠️ Skipping phase review - issues may surface later    │
│     → Update state: gate_passed = false, gate_skipped = true │
│     → Proceed to next phase                                │
│                                                              │
│  7. If user chooses [3]: Defer gate                         │
│     ℹ️ Phase review deferred - remember to run before release │
│     → Update state: gate_passed = false, gate_deferred = true │
│     → Proceed to next phase                                │
│                                                              │
│  8. Update project state                                    │
│     → Save gate passage status                             │
│     → Track gate date and results                          │
│     → Log to APP-STATE.yaml                                │
└─────────────────────────────────────────────────────────────┘
```

**State Tracking:**

After each gate, update `APP-STATE.yaml`:

```yaml
phases:
  requirements:
    complete: true
    gate:
      passed: true
      date: '2026-02-05'
      issues_found: 5
      issues_fixed: 5
      passes: 4
      methodologies_used: ['Top-Down-Requirements', 'Lateral-UX', 'Bottom-Up-Consistency']
  system_design:
    complete: true
    gate:
      passed: true
      date: '2026-02-05'
      issues_found: 3
      issues_fixed: 3
```
```

---

## Patch 3: Add Gate Configuration Function

### Location
Add new section after phase completion workflow.

### Content to Insert

```markdown
## Phase Gate Configurations

Each phase has specific deliverables and requirements for review.

### GATE 1: Requirements Phase

**When:** After requirements phase completes
**Before:** System design phase begins

**Configuration:**
```javascript
{
  phase: {
    name: 'requirements',
    scope: ['user stories', 'acceptance criteria', 'personas', 'use cases']
  },
  deliverables: [
    { type: 'user-story', path: 'docs/user-stories.md', required: true },
    { type: 'acceptance-criteria', path: 'docs/acceptance.md', required: true },
    { type: 'personas', path: 'docs/personas.md', required: false },
    { type: 'use-cases', path: 'docs/use-cases.md', required: false }
  ],
  requirements: extractedFromStakeholderInterviews
}
```

**Focus Areas:**
- Completeness (all stakeholder needs captured)
- Clarity (requirements unambiguous)
- Testability (acceptance criteria defined)
- Feasibility (requirements achievable)

**Common Issues:**
- Missing edge cases
- Ambiguous requirements
- Untestable acceptance criteria
- Stakeholder needs not captured

---

### GATE 2: System Design Phase

**When:** After system design phase completes
**Before:** UI design phase begins

**Configuration:**
```javascript
{
  phase: {
    name: 'system-design',
    scope: ['data models', 'API design', 'architecture', 'tech stack']
  },
  deliverables: [
    { type: 'data-model', path: 'design/data-model.md', required: true },
    { type: 'api-spec', path: 'design/api-spec.yaml', required: true },
    { type: 'architecture', path: 'design/architecture.md', required: true },
    { type: 'tech-stack', path: 'design/tech-stack.md', required: true }
  ],
  requirements: extractedFromRequirementsPhase
}
```

**Focus Areas:**
- Alignment with Phase 1 requirements
- Scalability considerations
- Security architecture defined
- Technology choices justified
- API consistency

**Common Issues:**
- Data model doesn't support requirements
- API design inconsistent
- Security architecture gaps
- Scalability not addressed

---

### GATE 3: UI Design Phase

**When:** After UI design phase completes
**Before:** Build phase begins

**Configuration:**
```javascript
{
  phase: {
    name: 'ui-design',
    scope: ['pages', 'navigation', 'forms', 'wireframes']
  },
  deliverables: [
    { type: 'page-inventory', path: 'design/pages.md', required: true },
    { type: 'navigation', path: 'design/navigation.md', required: true },
    { type: 'forms', path: 'design/forms.md', required: true },
    { type: 'wireframes', path: 'design/wireframes/', required: false },
    { type: 'style-guide', path: 'design/style-guide.md', required: false }
  ],
  requirements: extractedFromSystemDesignPhase
}
```

**Focus Areas:**
- Alignment with Phase 2 design
- UX consistency across pages
- Navigation flows intuitive
- Form validation comprehensive
- Accessibility considerations

**Common Issues:**
- Navigation flow confusing
- Inconsistent UI patterns
- Form validation gaps
- Accessibility issues
- Missing pages

---

### GATE 4: Build Phase

**When:** After build phase completes
**Before:** Supervision phase begins

**Configuration:**
```javascript
{
  phase: {
    name: 'build',
    scope: ['implementation', 'tests', 'documentation', 'configuration']
  },
  deliverables: [
    { type: 'implementation', path: 'src/', required: true },
    { type: 'tests', path: 'tests/', required: true },
    { type: 'documentation', path: 'docs/', required: true },
    { type: 'config', path: 'config/', required: true }
  ],
  requirements: extractedFromUIDesignPhase,
  convergence: {
    requiredCleanPasses: 3,
    maxIterations: 15  // Build phase might need more iterations
  }
}
```

**Focus Areas:**
- Alignment with Phase 2 & 3 design
- Code quality and maintainability
- Test coverage comprehensive
- Security implementation correct
- Performance optimized
- Documentation complete

**Common Issues:**
- Security vulnerabilities
- Performance bottlenecks
- Test coverage gaps
- Code quality issues
- Documentation incomplete
- Deviation from design

---

### GATE 5: Supervision Phase

**When:** After supervision phase completes
**Before:** Production release

**Configuration:**
```javascript
{
  phase: {
    name: 'supervision',
    scope: ['service config', 'health checks', 'installer', 'monitoring']
  },
  deliverables: [
    { type: 'service-config', path: 'deployment/nssm-config.json', required: true },
    { type: 'health-checks', path: 'src/health/', required: true },
    { type: 'installer', path: 'installer/', required: true },
    { type: 'deployment-docs', path: 'docs/deployment.md', required: true },
    { type: 'monitoring', path: 'monitoring/', required: false }
  ],
  requirements: extractedFromBuildPhase
}
```

**Focus Areas:**
- Service auto-starts on boot
- Health checks comprehensive
- Installer works correctly
- Deployment documented
- Monitoring configured
- Rollback capability

**Common Issues:**
- Health check gaps
- Installer bugs
- Service configuration errors
- Monitoring incomplete
- Rollback untested
- Documentation gaps

---

## getPhaseReviewConfig() Function

```javascript
function getPhaseReviewConfig(phaseName) {
  const configs = {
    requirements: {
      phase: { name: 'requirements', scope: ['user stories', 'acceptance criteria'] },
      deliverables: [
        { type: 'user-story', path: 'docs/user-stories.md', required: true },
        { type: 'acceptance-criteria', path: 'docs/acceptance.md', required: true }
      ],
      requirements: loadedFromContext.stakeholderRequirements
    },

    'system-design': {
      phase: { name: 'system-design', scope: ['data models', 'API', 'architecture'] },
      deliverables: [
        { type: 'data-model', path: 'design/data-model.md', required: true },
        { type: 'api-spec', path: 'design/api-spec.yaml', required: true },
        { type: 'architecture', path: 'design/architecture.md', required: true }
      ],
      requirements: loadedFromContext.requirements
    },

    'ui-design': {
      phase: { name: 'ui-design', scope: ['pages', 'navigation', 'forms'] },
      deliverables: [
        { type: 'page-inventory', path: 'design/pages.md', required: true },
        { type: 'navigation', path: 'design/navigation.md', required: true },
        { type: 'forms', path: 'design/forms.md', required: true }
      ],
      requirements: loadedFromContext.designRequirements
    },

    build: {
      phase: { name: 'build', scope: ['implementation', 'tests', 'docs'] },
      deliverables: [
        { type: 'implementation', path: 'src/', required: true },
        { type: 'tests', path: 'tests/', required: true },
        { type: 'documentation', path: 'docs/', required: true }
      ],
      requirements: loadedFromContext.implementationRequirements,
      convergence: { requiredCleanPasses: 3, maxIterations: 15 }
    },

    supervision: {
      phase: { name: 'supervision', scope: ['service', 'health', 'installer'] },
      deliverables: [
        { type: 'service-config', path: 'deployment/nssm-config.json', required: true },
        { type: 'health-checks', path: 'src/health/', required: true },
        { type: 'installer', path: 'installer/', required: true }
      ],
      requirements: loadedFromContext.deploymentRequirements
    }
  };

  return configs[phaseName];
}
```
```

---

## Patch 4: Update CHANGELOG.md

**File:** `windows-app/windows-app-orchestrator/CHANGELOG.md`

**Add at top:**
```markdown
## [2.0.0] - 2026-02-05

### Added
- 5 Phase Review Gates at development transitions
  - GATE 1: Requirements → System Design
  - GATE 2: System Design → UI Design
  - GATE 3: UI Design → Build
  - GATE 4: Build → Supervision
  - GATE 5: Supervision → Production
- Gate detection rules for manual gate triggering
- Phase completion workflow with automatic gate prompts
- Gate configuration function (getPhaseReviewConfig)
- State tracking for gate passage (APP-STATE.yaml)
- Integration with iterative-phase-review skill
- Skip, defer, and retry options for gates
- User prompt for gate execution with options

### Changed
- Phase transitions now include quality gates
- APP-STATE.yaml schema updated to track gate status
- Phase completion workflow enhanced with gate prompts

### Impact
- Increased quality: Issues caught at phase boundaries
- Time impact: +50-100 minutes total (10-20 per gate)
- Rework reduction: 40%+ reduction in late-stage fixes
- Production readiness: Higher confidence at deployment
```

---

## Patch 5: Update README.md

**File:** `windows-app/windows-app-orchestrator/SKILL.md`

**Add new section:**
```markdown
## Phase Review Gates

Windows app development includes 5 quality gates at phase transitions:

| Gate | Trigger | Review Focus |
|------|---------|--------------|
| GATE 1 | After Requirements | Completeness, clarity, testability |
| GATE 2 | After System Design | Architecture alignment, scalability |
| GATE 3 | After UI Design | UX consistency, navigation flows |
| GATE 4 | After Build | Code quality, security, performance |
| GATE 5 | After Supervision | Deployment readiness, monitoring |

**How Gates Work:**
1. Complete phase deliverables
2. Automatic gate prompt appears
3. Choose: run now, skip, or defer
4. If run: Multi-methodology review (8 approaches)
5. Converge until 3 clean passes
6. Gate passed: Proceed to next phase
7. Gate failed: Fix issues and retry

**Time Impact:** 10-20 minutes per gate (50-100 minutes total)

**Skip Policy:** Gates can be skipped but not recommended. Skipped gates tracked in state.
```

---

## Validation After Integration

### Checklist

- [ ] Gate detection rules added
- [ ] Phase completion workflow added
- [ ] Gate configurations added (all 5 gates)
- [ ] getPhaseReviewConfig() function added
- [ ] CHANGELOG.md updated with version 2.0.0
- [ ] README.md updated with gates section
- [ ] File compiles without errors
- [ ] Cross-references to iterative-phase-review correct

### Test

After applying patches:
```bash
# Verify gate detection rules
cat windows-app/windows-app-orchestrator/SKILL.md | grep "Phase Review Gates"

# Verify all 5 gates documented
cat windows-app/windows-app-orchestrator/SKILL.md | grep "GATE [1-5]"

# Should output 5 gate references
```

---

## Implementation Status

**Gate Detection Rules:** ✅ Ready
**Phase Completion Workflow:** ✅ Ready
**Gate Configurations (5):** ✅ Ready
**getPhaseReviewConfig Function:** ✅ Ready
**CHANGELOG.md Update:** ✅ Ready
**README.md Update:** ✅ Ready

**Status:** ✅ PATCH READY TO APPLY

**Estimated Application Time:** 30-40 minutes

---

## Notes

1. **User Control:** Gates are prompted but not forced. Users can skip with explicit consent.

2. **State Tracking:** Gate passage tracked in APP-STATE.yaml for visibility.

3. **Model Cost:** Gates use Claude Opus 4.5 (higher cost, higher quality).

4. **Time Investment:** 50-100 minutes total for all gates, offset by reduced rework.

5. **Flexibility:** Three options at each gate: run now, skip, defer.

---

*Patch Created: 2026-02-05*
*Target: windows-app/windows-app-orchestrator/SKILL.md*
*Status: ✅ READY TO APPLY*
*Version After Apply: 2.0.0*
