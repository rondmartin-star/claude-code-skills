# Windows App Phase Review Gates Integration

**Date:** 2026-02-05
**Purpose:** Add 5 phase review gates to Windows application development workflow
**Location:** `windows-app/windows-app-orchestrator/SKILL.md`
**Status:** Ready for integration

---

## Overview

Add phase review gates at 5 key transition points in Windows app development:

1. **After Requirements** → Before System Design
2. **After System Design** → Before UI Design
3. **After UI Design** → Before Build
4. **After Build** → Before Supervision/Deployment
5. **After Supervision** → Before Production Release

Each gate uses `iterative-phase-review` with phase-specific deliverables and requirements.

---

## Windows App Development Phases

### Current Flow

```
Phase 1: Requirements (windows-app-requirements)
  → User stories, acceptance criteria

Phase 2: System Design (windows-app-system-design)
  → Data models, API design, architecture

Phase 3: UI Design (windows-app-ui-design)
  → Page inventory, navigation flows, forms

Phase 4: Build (windows-app-build)
  → Implementation, testing, validation

Phase 5: Supervision (windows-app-supervision)
  → NSSM service, health checks, MSI packaging
```

### New Flow with Phase Review Gates

```
Phase 1: Requirements
  → Complete deliverables
  🚪 GATE 1: Review requirements deliverables
  ✓ Converge until clean
  → Proceed to System Design

Phase 2: System Design
  → Complete deliverables
  🚪 GATE 2: Review design deliverables
  ✓ Converge until clean
  → Proceed to UI Design

Phase 3: UI Design
  → Complete deliverables
  🚪 GATE 3: Review UI deliverables
  ✓ Converge until clean
  → Proceed to Build

Phase 4: Build
  → Complete deliverables
  🚪 GATE 4: Review implementation deliverables
  ✓ Converge until clean
  → Proceed to Supervision

Phase 5: Supervision
  → Complete deliverables
  🚪 GATE 5: Review deployment deliverables
  ✓ Converge until clean
  → Production Ready
```

---

## Gate Specifications

### GATE 1: Requirements Phase Review

**Trigger:** After windows-app-requirements completes

**Deliverables:**
```javascript
{
  deliverables: [
    { type: 'user-story', path: 'docs/user-stories.md', required: true },
    { type: 'acceptance-criteria', path: 'docs/acceptance.md', required: true },
    { type: 'personas', path: 'docs/personas.md', required: false },
    { type: 'use-cases', path: 'docs/use-cases.md', required: false }
  ]
}
```

**Requirements:**
- All stakeholder needs captured
- User stories follow standard format
- Acceptance criteria testable
- Requirements clear and unambiguous
- Technical feasibility assessed

**Focus Methodologies:**
- Top-Down-Requirements (completeness)
- Bottom-Up-Consistency (internal consistency)
- Lateral-UX (user experience perspective)

**Expected Issues:**
- Missing edge cases
- Ambiguous requirements
- Untestable acceptance criteria
- Stakeholder needs not captured

---

### GATE 2: System Design Phase Review

**Trigger:** After windows-app-system-design completes

**Deliverables:**
```javascript
{
  deliverables: [
    { type: 'data-model', path: 'design/data-model.md', required: true },
    { type: 'api-spec', path: 'design/api-spec.yaml', required: true },
    { type: 'architecture', path: 'design/architecture.md', required: true },
    { type: 'tech-stack', path: 'design/tech-stack.md', required: true }
  ]
}
```

**Requirements:**
- Alignment with Phase 1 requirements
- Scalability considerations
- Security architecture defined
- Technology choices justified
- API consistency

**Focus Methodologies:**
- Top-Down-Architecture (design alignment)
- Lateral-Security (security architecture)
- Lateral-Performance (scalability)
- Bottom-Up-Consistency (design consistency)

**Expected Issues:**
- Data model doesn't support requirements
- API design inconsistent
- Security architecture gaps
- Scalability not addressed

---

### GATE 3: UI Design Phase Review

**Trigger:** After windows-app-ui-design completes

**Deliverables:**
```javascript
{
  deliverables: [
    { type: 'page-inventory', path: 'design/pages.md', required: true },
    { type: 'navigation', path: 'design/navigation.md', required: true },
    { type: 'forms', path: 'design/forms.md', required: true },
    { type: 'wireframes', path: 'design/wireframes/', required: false },
    { type: 'style-guide', path: 'design/style-guide.md', required: false }
  ]
}
```

**Requirements:**
- Alignment with Phase 2 design
- UX consistency across pages
- Navigation flows intuitive
- Form validation comprehensive
- Accessibility considerations

**Focus Methodologies:**
- Lateral-UX (user experience)
- Top-Down-Architecture (design alignment)
- Bottom-Up-Consistency (UI consistency)
- Lateral-Integration (navigation flows)

**Expected Issues:**
- Navigation flow confusing
- Inconsistent UI patterns
- Form validation gaps
- Accessibility issues
- Missing pages

---

### GATE 4: Build Phase Review

**Trigger:** After windows-app-build completes

**Deliverables:**
```javascript
{
  deliverables: [
    { type: 'implementation', path: 'src/', required: true },
    { type: 'tests', path: 'tests/', required: true },
    { type: 'documentation', path: 'docs/', required: true },
    { type: 'config', path: 'config/', required: true },
    { type: 'scripts', path: 'scripts/', required: false }
  ]
}
```

**Requirements:**
- Alignment with Phase 2 & 3 design
- Code quality and maintainability
- Test coverage comprehensive
- Security implementation correct
- Performance optimized
- Documentation complete

**Focus Methodologies:**
- Bottom-Up-Quality (code quality)
- Lateral-Security (security implementation)
- Lateral-Performance (performance)
- Top-Down-Architecture (design alignment)
- Lateral-Integration (component integration)

**Expected Issues:**
- Security vulnerabilities
- Performance bottlenecks
- Test coverage gaps
- Code quality issues
- Documentation incomplete
- Deviation from design

---

### GATE 5: Supervision Phase Review

**Trigger:** After windows-app-supervision completes

**Deliverables:**
```javascript
{
  deliverables: [
    { type: 'service-config', path: 'deployment/nssm-config.json', required: true },
    { type: 'health-checks', path: 'src/health/', required: true },
    { type: 'installer', path: 'installer/', required: true },
    { type: 'deployment-docs', path: 'docs/deployment.md', required: true },
    { type: 'monitoring', path: 'monitoring/', required: false }
  ]
}
```

**Requirements:**
- Service auto-starts on boot
- Health checks comprehensive
- Installer works correctly
- Deployment documented
- Monitoring configured
- Rollback capability

**Focus Methodologies:**
- Top-Down-Requirements (deployment requirements met)
- Bottom-Up-Quality (deployment quality)
- Lateral-Integration (service integration)
- Lateral-Performance (production performance)

**Expected Issues:**
- Health check gaps
- Installer bugs
- Service configuration errors
- Monitoring incomplete
- Rollback untested
- Documentation gaps

---

## Implementation Strategy

### Option 1: Orchestrator-Managed Gates (Recommended)

**Approach:** Orchestrator automatically triggers phase review after each phase

**Implementation:**
```javascript
// In windows-app-orchestrator

async function completePhase(phase) {
  // 1. Complete phase-specific skill
  await executePhaseSkill(phase);

  // 2. Automatically trigger phase review gate
  const gateResult = await runPhaseReviewGate(phase);

  // 3. If converged, proceed to next phase
  if (gateResult.converged) {
    updateState({ currentPhase: nextPhase(phase) });
    return { status: 'ready-for-next-phase', nextPhase: nextPhase(phase) };
  }

  // 4. If not converged, require manual intervention
  return {
    status: 'review-failed',
    issues: gateResult.issues,
    unresolved: gateResult.unresolved,
    action: 'fix-issues-and-retry'
  };
}

async function runPhaseReviewGate(phase) {
  const phaseReview = await loadSkill('iterative-phase-review');

  const config = getPhaseReviewConfig(phase);

  return await phaseReview.run({
    phase: config.phase,
    deliverables: config.deliverables,
    requirements: config.requirements
  });
}
```

**Benefits:**
- Automatic enforcement
- Consistent across all phases
- User doesn't need to remember
- Clear quality gates

**Drawbacks:**
- Adds time to each phase
- Might feel restrictive

### Option 2: User-Triggered Gates

**Approach:** User explicitly requests phase review

**Implementation:**
```javascript
// User says: "Review requirements phase"
→ windows-app-orchestrator detects review request
→ Loads iterative-phase-review
→ Configures for requirements phase
→ Runs review
```

**Benefits:**
- User control
- Flexible workflow
- Can skip if confident

**Drawbacks:**
- Easy to forget
- Inconsistent usage
- Quality varies

### Option 3: Hybrid (Recommended)

**Approach:** Automatic with skip option

**Implementation:**
```javascript
// After phase completes
console.log('✓ Requirements phase complete');
console.log('');
console.log('🚪 GATE 1: Requirements Phase Review');
console.log('   This will review deliverables with 8 methodologies until 3 clean passes.');
console.log('   Estimated time: 10-20 minutes');
console.log('');
console.log('   Options:');
console.log('   1. [Recommended] Run phase review now');
console.log('   2. Skip and proceed to System Design (not recommended)');
console.log('   3. Run phase review later manually');

if (userChoice === 'run-now') {
  await runPhaseReviewGate('requirements');
} else if (userChoice === 'skip') {
  console.warn('⚠️ Skipping phase review - issues may be found later');
  updateState({ phaseReviewSkipped: true });
} else {
  console.log('ℹ️ Phase review deferred - remember to run before final release');
}
```

**Benefits:**
- Recommended but not forced
- User aware of trade-offs
- Flexibility when needed

---

## Gate Configuration Details

### Requirements Gate (GATE 1)

```javascript
{
  phase: {
    name: 'requirements',
    scope: ['user stories', 'acceptance criteria', 'personas', 'use cases'],
    dependencies: ['stakeholder interviews complete']
  },

  deliverables: [
    {
      type: 'user-story',
      path: 'docs/user-stories.md',
      required: true,
      checks: [
        'Format follows standard (As a... I want... So that...)',
        'Acceptance criteria defined',
        'Priority assigned',
        'Estimation provided'
      ]
    },
    {
      type: 'acceptance-criteria',
      path: 'docs/acceptance.md',
      required: true,
      checks: [
        'Testable criteria',
        'Clear pass/fail conditions',
        'Edge cases covered'
      ]
    }
  ],

  requirements: extractedFromStakeholderInterviews,

  convergence: {
    requiredCleanPasses: 3,
    maxIterations: 10
  }
}
```

### System Design Gate (GATE 2)

```javascript
{
  phase: {
    name: 'system-design',
    scope: ['data models', 'API design', 'architecture', 'tech stack'],
    dependencies: ['requirements phase complete', 'GATE 1 passed']
  },

  deliverables: [
    {
      type: 'data-model',
      path: 'design/data-model.md',
      required: true,
      checks: [
        'Entities defined',
        'Relationships clear',
        'Supports requirements',
        'Normalized appropriately'
      ]
    },
    {
      type: 'api-spec',
      path: 'design/api-spec.yaml',
      required: true,
      checks: [
        'OpenAPI 3.0 format',
        'All endpoints documented',
        'Request/response schemas',
        'Error handling defined'
      ]
    },
    {
      type: 'architecture',
      path: 'design/architecture.md',
      required: true,
      checks: [
        'Component diagram',
        'Data flow documented',
        'Security architecture',
        'Scalability considerations'
      ]
    }
  ],

  requirements: extractedFromRequirementsPhase,

  convergence: {
    requiredCleanPasses: 3,
    maxIterations: 10
  }
}
```

### UI Design Gate (GATE 3)

```javascript
{
  phase: {
    name: 'ui-design',
    scope: ['pages', 'navigation', 'forms', 'wireframes'],
    dependencies: ['system design complete', 'GATE 2 passed']
  },

  deliverables: [
    {
      type: 'page-inventory',
      path: 'design/pages.md',
      required: true,
      checks: [
        'All pages listed',
        'Purpose defined',
        'Data requirements',
        'User flows'
      ]
    },
    {
      type: 'navigation',
      path: 'design/navigation.md',
      required: true,
      checks: [
        'Navigation flows documented',
        'Entry points identified',
        'Error paths defined',
        'Accessibility considered'
      ]
    },
    {
      type: 'forms',
      path: 'design/forms.md',
      required: true,
      checks: [
        'All forms documented',
        'Fields and validation rules',
        'Error messages defined',
        'CSRF protection planned'
      ]
    }
  ],

  requirements: extractedFromSystemDesignPhase,

  convergence: {
    requiredCleanPasses: 3,
    maxIterations: 10
  }
}
```

### Build Gate (GATE 4)

```javascript
{
  phase: {
    name: 'build',
    scope: ['implementation', 'tests', 'documentation', 'configuration'],
    dependencies: ['UI design complete', 'GATE 3 passed']
  },

  deliverables: [
    {
      type: 'implementation',
      path: 'src/',
      required: true,
      checks: [
        'Code follows design',
        'Security patterns implemented',
        'Error handling comprehensive',
        'Performance optimized'
      ]
    },
    {
      type: 'tests',
      path: 'tests/',
      required: true,
      checks: [
        'Unit tests for business logic',
        'Integration tests for APIs',
        'End-to-end tests for critical flows',
        'Test coverage > 80%'
      ]
    },
    {
      type: 'documentation',
      path: 'docs/',
      required: true,
      checks: [
        'API documentation',
        'Setup instructions',
        'Configuration guide',
        'Troubleshooting section'
      ]
    }
  ],

  requirements: extractedFromUIDesignPhase,

  convergence: {
    requiredCleanPasses: 3,
    maxIterations: 15  // Build phase might need more iterations
  }
}
```

### Supervision Gate (GATE 5)

```javascript
{
  phase: {
    name: 'supervision',
    scope: ['service config', 'health checks', 'installer', 'monitoring'],
    dependencies: ['build complete', 'GATE 4 passed']
  },

  deliverables: [
    {
      type: 'service-config',
      path: 'deployment/nssm-config.json',
      required: true,
      checks: [
        'Service configured for auto-start',
        'Restart policy defined',
        'Log configuration',
        'Environment variables'
      ]
    },
    {
      type: 'health-checks',
      path: 'src/health/',
      required: true,
      checks: [
        'Database connectivity check',
        'External service checks',
        'Disk space check',
        'Memory usage check'
      ]
    },
    {
      type: 'installer',
      path: 'installer/',
      required: true,
      checks: [
        'MSI builds successfully',
        'Installation tested',
        'Uninstallation tested',
        'Upgrade path tested'
      ]
    }
  ],

  requirements: extractedFromBuildPhase,

  convergence: {
    requiredCleanPasses: 3,
    maxIterations: 10
  }
}
```

---

## Integration Steps

### Step 1: Update Orchestrator Phase Detection

Add phase review gate detection to skill detection rules:

```javascript
// In windows-app-orchestrator SKILL.md

### Phase Review Gates

| If prompt contains... | Action... |
|-----------------------|-----------|
| "review requirements", "requirements gate" | Run GATE 1 (requirements review) |
| "review design", "design gate" | Run GATE 2 (design review) |
| "review UI", "UI gate" | Run GATE 3 (UI review) |
| "review build", "build gate" | Run GATE 4 (build review) |
| "review deployment", "supervision gate" | Run GATE 5 (supervision review) |
| "review all phases", "full review" | Run all gates sequentially |
```

### Step 2: Add Phase Completion Hooks

After each phase completes, prompt for gate review:

```markdown
## Phase Completion Workflow

After completing each phase:

1. Execute phase-specific skill
2. Generate deliverables
3. **[NEW] Prompt for phase review gate**
   ```
   ✓ [Phase] complete

   🚪 GATE [N]: [Phase] Phase Review
      Review deliverables with multi-methodology convergence?
      [Y/n] →
   ```
4. If 'Y': Run iterative-phase-review
5. If converged: Proceed to next phase
6. If not converged: Fix issues and retry
```

### Step 3: Add Gate Configuration Function

```javascript
function getPhaseReviewConfig(phase) {
  const configs = {
    requirements: {
      phase: { name: 'requirements', scope: [...] },
      deliverables: [...],
      requirements: extractedRequirements
    },
    'system-design': {
      phase: { name: 'system-design', scope: [...] },
      deliverables: [...],
      requirements: extractedFromRequirements
    },
    'ui-design': {
      phase: { name: 'ui-design', scope: [...] },
      deliverables: [...],
      requirements: extractedFromDesign
    },
    build: {
      phase: { name: 'build', scope: [...] },
      deliverables: [...],
      requirements: extractedFromUIDesign
    },
    supervision: {
      phase: { name: 'supervision', scope: [...] },
      deliverables: [...],
      requirements: extractedFromBuild
    }
  };

  return configs[phase];
}
```

### Step 4: Update State Tracking

Track gate passage in APP-STATE.yaml:

```yaml
project_state:
  current_phase: 'build'
  phases:
    requirements:
      complete: true
      gate_passed: true  # NEW
      gate_date: '2026-02-05'
    system_design:
      complete: true
      gate_passed: true  # NEW
      gate_date: '2026-02-05'
    ui_design:
      complete: true
      gate_passed: false  # NEW - not yet reviewed
    build:
      complete: false
      gate_passed: false
    supervision:
      complete: false
      gate_passed: false
```

---

## Testing Strategy

### Test Case 1: Happy Path (All Gates Pass)

```
1. Complete requirements phase
2. Run GATE 1 → Converge (3 clean passes)
3. Proceed to system design
4. Complete system design phase
5. Run GATE 2 → Converge (3 clean passes)
6. Proceed to UI design
7. Complete UI design phase
8. Run GATE 3 → Converge (3 clean passes)
9. Proceed to build
10. Complete build phase
11. Run GATE 4 → Converge (3 clean passes)
12. Proceed to supervision
13. Complete supervision phase
14. Run GATE 5 → Converge (3 clean passes)
15. Production Ready ✓
```

**Expected Time:** 60-90 minutes total for all gates

### Test Case 2: Gate Failure (Issues Found)

```
1. Complete requirements phase
2. Run GATE 1 → Find issues:
   - Missing edge cases
   - Ambiguous acceptance criteria
3. Fix issues
4. Re-run GATE 1 → Converge
5. Proceed to system design
...
```

**Expected:** Issues found, fixed, gate re-run, converge

### Test Case 3: Skip Gates (User Choice)

```
1. Complete requirements phase
2. Skip GATE 1 (user choice)
3. Proceed to system design
4. Complete system design
5. Run GATE 2 → Find issues:
   - Design doesn't support requirements
   - (Issues could have been caught in GATE 1)
6. Return to requirements phase
7. Fix requirements
8. Run GATE 1 (deferred)
9. Run GATE 2 again
...
```

**Expected:** Later gates catch earlier issues, more rework

---

## Success Metrics

### Gate Effectiveness
- **Issue Detection Rate:** 70%+ phases have issues found
- **Issue Prevention:** 60%+ issues caught before next phase
- **False Positive Rate:** <15% clean deliverables flagged

### Time Impact
- **Gate Time:** 10-20 minutes per gate (50-100 minutes total)
- **Rework Reduction:** 40%+ reduction in late-stage rework
- **Overall Time:** Net neutral or faster (due to rework reduction)

### Quality Improvement
- **Production Issues:** 50%+ reduction
- **Security Vulnerabilities:** 70%+ reduction
- **Requirement Misalignment:** 80%+ reduction

---

## Rollout Plan

### Week 2, Day 3: Initial Integration
- Add gate detection to windows-app-orchestrator
- Implement getPhaseReviewConfig()
- Add phase completion hooks
- Test GATE 1 (requirements)

### Week 2, Day 4: Full Integration
- Test all 5 gates
- Validate state tracking
- Test skip functionality
- End-to-end test

### Week 2, Day 5: Documentation
- Update windows-app-orchestrator README
- Create gate usage guide
- Document configuration options

### Week 3: Production
- Enable gates by default
- Monitor effectiveness
- Iterate based on feedback

---

## File Changes Required

### Modified Files
1. `windows-app/windows-app-orchestrator/SKILL.md`
   - Add gate detection rules
   - Add phase completion hooks
   - Add getPhaseReviewConfig()
   - Update workflow examples

2. `windows-app/windows-app-orchestrator/README.md`
   - Document 5 phase review gates
   - Add gate usage examples

3. `windows-app/windows-app-orchestrator/CHANGELOG.md`
   - Document gate addition
   - Version bump

### New Files
None (uses existing iterative-phase-review skill)

---

*Integration Guide Created: 2026-02-05*
*Ready for Implementation: Week 2, Day 3-4*
*Part of v4.0 Universal Skills Ecosystem - Learning Integration*
