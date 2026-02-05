# Option B: Multi-Methodology Convergence Implementation Plan

**Date:** 2026-02-04
**Approach:** Make audit convergence generic (rename to multi-methodology-convergence)
**Status:** 📋 READY FOR IMPLEMENTATION

---

## Approach: Enhance Existing Convergence Engine

Instead of creating a new convergence-pattern component, we'll:
1. Rename `convergence-engine` → `multi-methodology-convergence`
2. Make it generic to support multiple convergence types
3. Configure for specific use cases (audit, phase-review, etc.)

**Benefits over Option A (separate pattern):**
- Simpler architecture (1 component instead of 3)
- Leverage existing, proven convergence logic
- No need to refactor working audit convergence
- Just extend what works

---

## Architecture

### Before (Current)

```
convergence-engine
├─ Purpose: Audit convergence only
├─ 3-3-1 methodology (technical/user/holistic)
├─ GATE convergence for audits
└─ Pre-release validation
```

### After (Option B)

```
multi-methodology-convergence
├─ Purpose: Generic convergence for any subject
├─ Configurable methodologies
├─ Multiple convergence modes:
│   ├─ audit (existing)
│   ├─ phase-review (new)
│   └─ custom (extensible)
└─ Used by: audit-orchestrator, phase transitions, battle-plan
```

---

## Implementation Steps

### Step 1: Rename and Generalize

**File Changes:**
- Rename: `core/audit/convergence-engine/` → `core/learning/convergence/multi-methodology-convergence/`
- Update: All references to convergence-engine
- Move from audit category to learning category (more appropriate for general use)

**Code Changes:**

```javascript
// BEFORE (audit-specific)
async function runAuditConvergence(projectPath) {
  const audits = getApplicableAudits();
  const methodologies = ['technical', 'user', 'holistic'];
  // ... hardcoded for audits
}

// AFTER (generic)
async function runConvergence(config) {
  const {
    mode,           // 'audit' | 'phase-review' | 'custom'
    subject,        // What we're converging
    methodologies,  // How we check it
    verify,         // How we verify clean
    fix             // How we fix issues
  } = config;

  // Generic convergence logic
  // ...
}
```

---

### Step 2: Add Configuration System

**Configuration Interface:**

```javascript
const convergenceConfig = {
  // Mode: determines default behavior
  mode: 'audit' | 'phase-review' | 'custom',

  // Subject: what we're converging
  subject: {
    type: 'code' | 'deliverables' | 'architecture' | 'content',
    data: { /* mode-specific data */ }
  },

  // Methodologies: how we check it
  methodologies: [
    {
      name: 'methodology-1',
      description: 'What this methodology checks',
      executor: async (subject) => { /* returns issues */ }
    },
    {
      name: 'methodology-2',
      executor: async (subject) => { /* returns issues */ }
    },
    {
      name: 'methodology-3',
      executor: async (subject) => { /* returns issues */ }
    }
  ],

  // Verification: how we determine clean
  verify: {
    clean: async (result) => {
      // Returns true if clean, false if issues
    },
    evidence: [ /* verify-evidence requirements */ ]
  },

  // Fixing: how we resolve issues
  fix: {
    executor: async (issues) => {
      // Fixes issues, returns result
    },
    backup: true  // Create backup before fixing
  },

  // Convergence parameters
  convergence: {
    requiredCleanPasses: 3,
    maxIterations: 10,
    rotateMethodologies: true,
    clearContextBetweenPasses: false  // or true for phase reviews
  },

  // Learning integration
  learning: {
    logToPatternLibrary: true,
    runErrorReflection: true,
    trackMetrics: true
  },

  // Model configuration
  model: 'claude-opus-4-5'  // Optional: use specific model
};
```

---

### Step 3: Define Mode Presets

**Preset: audit**

```javascript
const auditModePreset = {
  mode: 'audit',
  subject: {
    type: 'code',
    data: { projectPath, audits: getApplicableAudits() }
  },
  methodologies: [
    {
      name: 'technical',
      description: 'How it\'s built',
      executor: async (data) => runAudits(data, ['security', 'code-quality', 'performance'])
    },
    {
      name: 'user',
      description: 'How it\'s experienced',
      executor: async (data) => runAudits(data, ['accessibility', 'ux-performance'])
    },
    {
      name: 'holistic',
      description: 'How it fits together',
      executor: async (data) => runAudits(data, ['consistency', 'navigation', 'documentation'])
    }
  ],
  verify: {
    clean: async (result) => result.issues.length === 0,
    evidence: [
      "All 3 methodologies: 0 issues",
      "No critical or high issues",
      "All audits completed successfully"
    ]
  },
  fix: {
    executor: async (issues) => {
      const plan = await generateFixPlan(issues);
      return await implementFixes(plan);
    },
    backup: true
  },
  convergence: {
    requiredCleanPasses: 3,
    maxIterations: 10,
    clearContextBetweenPasses: false  // Keep audit context
  }
};
```

**Preset: phase-review**

```javascript
const phaseReviewModePreset = {
  mode: 'phase-review',
  subject: {
    type: 'deliverables',
    data: { phase, deliverables, requirements }
  },
  methodologies: [
    {
      name: 'top-down',
      description: 'Requirements → Implementation',
      executor: async (data) => reviewTopDown(data.phase, data.deliverables)
    },
    {
      name: 'bottom-up',
      description: 'Implementation → Quality',
      executor: async (data) => reviewBottomUp(data.deliverables)
    },
    {
      name: 'lateral',
      description: 'Cross-cutting concerns',
      executor: async (data) => reviewLateral(data.phase, data.deliverables)
    }
  ],
  verify: {
    clean: async (result) => {
      return await verify_evidence.check({
        claim: `Phase ${data.phase.name} is complete`,
        evidence: result.evidence
      });
    },
    evidence: [
      "All requirements met",
      "All deliverables complete",
      "No inconsistencies",
      "Ready for next phase"
    ]
  },
  fix: {
    executor: async (issues) => fixPhaseIssues(phase, deliverables, issues),
    backup: false  // Phase work is iterative, no need for backup
  },
  convergence: {
    requiredCleanPasses: 3,
    maxIterations: 10,
    clearContextBetweenPasses: true  // Fresh review each pass
  },
  model: 'claude-opus-4-5'  // Use opus for high-quality reviews
};
```

---

### Step 4: Generic Convergence Algorithm

**Enhanced Algorithm (supports all modes):**

```javascript
async function executeConvergence(config) {
  // Apply mode preset if specified
  if (config.mode && !config.methodologies) {
    config = applyModePreset(config);
  }

  const state = {
    passes: [],
    consecutiveClean: 0,
    issues: [],
    currentMethodologyIndex: 0,
    totalIssuesFixed: 0
  };

  // Set model if specified
  if (config.model) {
    setModel(config.model);
  }

  console.log(`\n═══ CONVERGENCE: ${config.mode || 'custom'} ═══`);
  console.log(`Subject: ${config.subject.type}`);
  console.log(`Methodologies: ${config.methodologies.map(m => m.name).join(', ')}`);
  console.log(`Required clean passes: ${config.convergence.requiredCleanPasses}`);

  while (state.consecutiveClean < config.convergence.requiredCleanPasses
         && state.passes.length < config.convergence.maxIterations) {

    const passNumber = state.passes.length + 1;
    const methodology = config.methodologies[state.currentMethodologyIndex];

    console.log(`\n--- Pass ${passNumber}: ${methodology.name} ---`);
    console.log(`Description: ${methodology.description}`);

    // Clear context if configured
    if (config.convergence.clearContextBetweenPasses) {
      await manage_context.clear_context({
        preserve: ['subject', 'methodologies', 'priorIssues']
      });
      console.log('✓ Context cleared for fresh review');
    }

    // Execute methodology
    const result = await methodology.executor(config.subject.data);

    // Verify if clean
    const isClean = await config.verify.clean(result);

    // verify-evidence integration
    if (isClean && config.verify.evidence) {
      const evidenceVerified = await verify_evidence.check({
        claim: `${config.mode} is clean`,
        evidence: config.verify.evidence
      });

      if (!evidenceVerified) {
        console.log('⚠️  Evidence verification failed - treating as not clean');
        isClean = false;
      }
    }

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

      // error-reflection integration
      if (config.learning.runErrorReflection) {
        const reflection = await error_reflection.analyze(result.issues);

        // pattern-library integration
        if (config.learning.logToPatternLibrary) {
          await pattern_library.update({
            antipatterns: reflection.antipatterns,
            prevention: reflection.prevention_measures
          });
        }
      }

      // Create backup if configured
      if (config.fix.backup) {
        await createBackup();
      }

      // Fix issues
      const fixResult = await config.fix.executor(result.issues);
      state.totalIssuesFixed += fixResult.fixed || 0;

      console.log(`✓ Fixed ${fixResult.fixed} issues`);
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

  console.log(`\n═══ CONVERGENCE ${converged ? 'COMPLETE ✓' : 'FAILED ✗'} ═══`);
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

## Usage Examples

### Usage 1: Audit Convergence (Existing Behavior)

```javascript
// Simple API - uses audit mode preset
const result = await multiMethodologyConvergence.run({
  mode: 'audit',
  subject: { data: { projectPath: '/path/to/project' } }
});

// OR explicit configuration
const result = await multiMethodologyConvergence.run({
  mode: 'audit',
  subject: {
    type: 'code',
    data: {
      projectPath: '/path/to/project',
      audits: ['security', 'quality', 'performance']
    }
  },
  // methodologies, verify, fix auto-applied from audit preset
});
```

### Usage 2: Phase Review (New Behavior)

```javascript
// Simple API - uses phase-review mode preset
const result = await multiMethodologyConvergence.run({
  mode: 'phase-review',
  subject: {
    data: {
      phase: { name: 'requirements', scope: [...] },
      deliverables: [...]
    }
  }
});

// OR explicit configuration
const result = await multiMethodologyConvergence.run({
  mode: 'phase-review',
  subject: {
    type: 'deliverables',
    data: { phase, deliverables, requirements }
  },
  model: 'claude-opus-4-5',  // Override to use opus
  // methodologies, verify, fix auto-applied from phase-review preset
});
```

### Usage 3: Custom Convergence (Extensible)

```javascript
// Completely custom configuration
const result = await multiMethodologyConvergence.run({
  mode: 'custom',
  subject: {
    type: 'architecture',
    data: { architecture, requirements, constraints }
  },
  methodologies: [
    { name: 'scalability', executor: reviewScalability },
    { name: 'security', executor: reviewSecurityArchitecture },
    { name: 'maintainability', executor: reviewMaintainability }
  ],
  verify: {
    clean: async (result) => result.issues.length === 0
  },
  fix: {
    executor: async (issues) => updateArchitecture(issues)
  },
  convergence: {
    requiredCleanPasses: 3,
    maxIterations: 10
  }
});
```

---

## File Structure

### New Location

```
core/learning/convergence/multi-methodology-convergence/
├── SKILL.md                          # Main skill (~15KB)
├── README.md                         # Quick reference
├── CHANGELOG.md                      # Version history
├── references/
│   ├── audit-mode.md                 # Audit convergence details
│   ├── phase-review-mode.md          # Phase review details
│   ├── custom-modes.md               # How to create custom modes
│   └── methodology-design.md         # Designing methodologies
└── examples/
    ├── audit-convergence-example.md
    ├── phase-review-example.md
    └── custom-convergence-example.md
```

### Migration Path

**Old references:**
```javascript
const convergence = await loadSkill('convergence-engine');
```

**New references:**
```javascript
const convergence = await loadSkill('multi-methodology-convergence');
```

**Backward compatibility:** Keep symlink for transition period
```bash
ln -s core/learning/convergence/multi-methodology-convergence \
      core/audit/convergence-engine
```

---

## Integration Points

### 1. Audit Orchestrator

**File:** `core/audit/audit-orchestrator/SKILL.md`

**Change:**
```javascript
// BEFORE
const convergence = await loadSkill('convergence-engine');
await convergence.run(projectPath);

// AFTER
const convergence = await loadSkill('multi-methodology-convergence');
await convergence.run({
  mode: 'audit',
  subject: { data: { projectPath } }
});
```

### 2. Battle-Plan Phase Transitions

**File:** `core/learning/orchestrators/battle-plan/SKILL.md`

**Add Phase 5.5:**
```javascript
// After PHASE 5: EXECUTION
console.log('\n═══ PHASE 5.5: PHASE REVIEW ═══');

const convergence = await loadSkill('multi-methodology-convergence');
const reviewResult = await convergence.run({
  mode: 'phase-review',
  subject: {
    data: {
      phase: { name: 'execution', deliverables: [...] },
      deliverables: result.phases.execution
    }
  }
});

if (!reviewResult.converged) {
  console.log('⚠️  Phase review did not converge');
  // Handle non-convergence
}
```

### 3. Windows App Orchestrator

**File:** `windows-app/windows-app-orchestrator/SKILL.md`

**Add after each phase:**
```javascript
// After Phase 1: Requirements
const convergence = await loadSkill('multi-methodology-convergence');
const review = await convergence.run({
  mode: 'phase-review',
  subject: {
    data: {
      phase: { name: 'requirements', scope: [...] },
      deliverables: requirementsOutput
    }
  }
});

if (review.converged) {
  console.log('→ Proceeding to Phase 2: System Design');
} else {
  console.log('⚠️  Requirements review failed - manual review needed');
}
```

---

## Configuration Files

### Global Config

**File:** `.corpus/learning/config.json`

```json
{
  "multiMethodologyConvergence": {
    "defaults": {
      "requiredCleanPasses": 3,
      "maxIterations": 10,
      "rotateMethodologies": true
    },
    "modes": {
      "audit": {
        "clearContextBetweenPasses": false,
        "model": null
      },
      "phase-review": {
        "clearContextBetweenPasses": true,
        "model": "claude-opus-4-5"
      }
    },
    "learning": {
      "logToPatternLibrary": true,
      "runErrorReflection": true,
      "trackMetrics": true
    }
  }
}
```

---

## Benefits Summary

### vs Option A (Separate Pattern)

| Aspect | Option A | Option B |
|--------|----------|----------|
| **Components** | 3 (pattern + 2 uses) | 1 (multi-methodology) |
| **Code** | ~700 lines | ~600 lines |
| **Refactoring** | Required (audit) | Optional (audit) |
| **Testing** | 3 components | 1 component |
| **Learning curve** | Medium | Low |
| **Backward compat** | Breaks existing | Maintains existing |

**Winner:** Option B (simpler, less refactoring, backward compatible)

---

## Implementation Timeline

### Week 1: Core Enhancement

**Days 1-2:** Generalize convergence-engine
- Add configuration system
- Support multiple modes
- Keep audit mode working

**Days 3-4:** Create mode presets
- Audit mode (existing behavior)
- Phase-review mode (new)
- Test both modes

**Day 5:** Move and rename
- Move to core/learning/convergence/
- Rename to multi-methodology-convergence
- Create backward-compat symlink
- Update all references

### Week 2: Integration

**Days 1-2:** Battle-plan integration
- Add Phase 5.5
- Test phase reviews
- Document integration

**Days 3-4:** Windows app integration
- Add phase review gates
- Test all 5 phases
- Collect antipatterns

**Day 5:** Documentation
- Update SKILL.md files
- Update CLAUDE.md
- Create migration guide

---

## Migration Checklist

- [ ] Generalize convergence-engine code
- [ ] Add configuration system
- [ ] Create audit mode preset
- [ ] Create phase-review mode preset
- [ ] Test audit mode (existing behavior preserved)
- [ ] Test phase-review mode (new behavior works)
- [ ] Move to core/learning/convergence/
- [ ] Rename to multi-methodology-convergence
- [ ] Create backward-compat symlink
- [ ] Update audit-orchestrator references
- [ ] Add Phase 5.5 to battle-plan
- [ ] Add phase reviews to windows-app-orchestrator
- [ ] Test end-to-end flows
- [ ] Update documentation
- [ ] Create migration guide
- [ ] Remove symlink after transition period

---

## Success Criteria

### Week 1 (Core)

- ✓ multi-methodology-convergence created
- ✓ Audit mode works (existing behavior)
- ✓ Phase-review mode works (new behavior)
- ✓ All tests pass

### Week 2 (Integration)

- ✓ Battle-plan Phase 5.5 working
- ✓ Windows app phase reviews working
- ✓ Pattern library capturing antipatterns
- ✓ Documentation complete

### Month 1 (Validation)

- ✓ 20+ antipatterns captured from phase reviews
- ✓ 95%+ of issues caught before next phase
- ✓ Zero major rework in later phases
- ✓ Developer confidence: high

---

*End of Option B Implementation Plan*
*Status: 📋 READY TO IMPLEMENT*
*Approach: Enhance existing convergence-engine, rename to multi-methodology-convergence*
*Benefits: Simpler, less refactoring, backward compatible*
