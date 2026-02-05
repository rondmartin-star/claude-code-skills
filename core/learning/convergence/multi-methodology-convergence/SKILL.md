---
name: multi-methodology-convergence
description: >
  Generic multi-methodology iterative convergence engine. Supports multiple modes
  (audit, phase-review, custom) with configurable methodologies. Implements 3-pass
  clean convergence with full learning integration (verify-evidence, detect-infinite-loop,
  manage-context, pattern-library). Use when: running audits, reviewing phases, or
  any multi-methodology quality convergence process.
---

# Multi-Methodology Convergence

**Purpose:** Generic convergence pattern for any multi-methodology quality process
**Size:** ~18 KB
**Type:** Core Pattern (Universal - Learning Integration)
**Modes:** audit, phase-review, custom (extensible)

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Run convergence" (with mode specification)
- "Run audit convergence" (audit mode)
- "Review this phase" (phase-review mode)
- "Converge until clean"

**Context Indicators:**
- Need iterative quality improvement
- Multiple perspectives needed (methodologies)
- Must reach clean state before proceeding
- Production readiness validation
- Phase transition quality gates

## ❌ DO NOT LOAD WHEN

- Single-pass check sufficient
- No need for convergence (one-time validation)
- Trivial operations

---

## Convergence Pattern Overview

**Core Concept:** Run multiple methodologies iteratively until 3 consecutive clean passes

**Methodology Selection:** Random selection from pool of 5-10 orthogonal approaches with priority constraint
- Each clean pass uses a different methodology
- Cannot reuse methodologies from previous clean passes
- Pool resets when consecutive clean count resets to 0
- **PRIORITY CONSTRAINT:** At least one functional/completeness or user-focused methodology must be selected in each clean sequence

**Generic Algorithm:**
```
WHILE consecutive_clean_passes < 3 AND iterations < max:
  1. Select random methodology with priority constraint:
     - If no priority methodology used yet in clean sequence, force priority selection
     - Otherwise random from unused methodologies
     - Cannot reuse methodologies from previous clean passes
  2. Execute selected methodology
  3. Verify results (with verify-evidence)
  4. If clean → increment counter, mark methodology as used
  5. If issues → reset counter, clear used methodologies, analyze and fix
  6. Monitor for infinite loops (detect-infinite-loop)
  7. Manage context (manage-context if needed)
DONE

Result: Converged (3 clean) OR Failed (max iterations)
```

**Supported Modes:**
- **audit:** Code quality convergence (technical/user/holistic)
- **phase-review:** Deliverable quality convergence (top-down/bottom-up/lateral)
- **custom:** Define your own methodologies

**Priority Constraint Rationale:**
The convergence engine ensures that at least one functional/completeness or user-focused methodology is always selected in each clean pass sequence. This guarantees that:
- **Functional completeness** is verified (does it work?)
- **User needs** are validated (does it solve the problem?)
- These fundamental concerns are never skipped in favor of only secondary concerns (performance, security, consistency, etc.)

Without this constraint, random selection could theoretically produce 3 clean passes using only secondary methodologies (e.g., performance, security, consistency), missing critical functional or user-focused validation.

---

## Configuration Interface

### Mode-Based Configuration (Recommended)

```javascript
await multiMethodologyConvergence.run({
  // Mode: uses preset configuration
  mode: 'audit' | 'phase-review' | 'custom',

  // Subject: what we're converging
  subject: {
    type: 'code' | 'deliverables' | 'architecture' | 'content',
    data: { /* mode-specific data */ }
  },

  // Optional overrides
  model: 'claude-opus-4-5',  // Override model
  convergence: {
    requiredCleanPasses: 3,   // Override clean passes
    maxIterations: 10          // Override max iterations
  }
});
```

### Full Custom Configuration

```javascript
await multiMethodologyConvergence.run({
  mode: 'custom',

  subject: {
    type: 'custom-type',
    data: { /* your data */ }
  },

  methodologies: [
    {
      name: 'methodology-1',
      description: 'What this checks',
      executor: async (subject) => {
        // Returns: { issues: [], evidence: [] }
      }
    },
    // ... 4-9 more methodologies (5-10 total recommended for diversity)
    // Each methodology should be orthogonal (different perspective/concern)
  ],

  verify: {
    clean: async (result) => {
      // Returns: boolean (true if clean)
    },
    evidence: [ /* verify-evidence requirements */ ]
  },

  fix: {
    executor: async (issues) => {
      // Fixes issues
      // Returns: { fixed: number }
    },
    backup: true | false
  },

  convergence: {
    requiredCleanPasses: 3,
    maxIterations: 10,
    clearContextBetweenPasses: false  // true = fresh context each pass
  },

  learning: {
    logToPatternLibrary: true,
    runErrorReflection: true,
    trackMetrics: true
  },

  model: null | 'claude-opus-4-5' | 'claude-sonnet-4-5'
});
```

---

## Mode Presets

### Audit Mode

**Purpose:** Code quality convergence (existing convergence-engine behavior)

**Methodology Pool (7 orthogonal approaches):**
1. **Technical-Security:** Security architecture, vulnerabilities, auth patterns
2. **Technical-Quality:** Code quality, maintainability, testability
3. **Technical-Performance:** Performance bottlenecks, optimization opportunities
4. **User-Accessibility:** Accessibility compliance, WCAG standards
5. **User-Experience:** UX patterns, usability, interaction flows
6. **Holistic-Consistency:** Naming, patterns, architectural consistency
7. **Holistic-Integration:** Navigation, API coherence, documentation completeness

**Selection:** Random (constraint: no reuse in current clean pass sequence)

**Configuration:**
```javascript
{
  mode: 'audit',
  subject: {
    type: 'code',
    data: { projectPath, audits: getApplicableAudits() }
  },
  // Methodologies auto-configured from audit preset
  // verify, fix auto-configured from audit preset
  convergence: {
    requiredCleanPasses: 3,
    clearContextBetweenPasses: false  // Keep audit context
  }
}
```

**When to use:** Pre-release validation, production readiness checks

---

### Phase-Review Mode

**Purpose:** Phase deliverable quality convergence

**Methodology Pool (8 orthogonal approaches):**
1. **Top-Down-Requirements:** Requirements → Deliverables (completeness check) ⭐ PRIORITY
2. **Top-Down-Architecture:** Architecture → Implementation (design alignment)
3. **Bottom-Up-Quality:** Code/Artifacts → Standards (quality validation)
4. **Bottom-Up-Consistency:** Low-level → High-level (internal consistency)
5. **Lateral-Integration:** Component interfaces and boundaries
6. **Lateral-Security:** Security architecture and implementation
7. **Lateral-Performance:** Performance characteristics and bottlenecks
8. **Lateral-UX:** User experience and interaction flows ⭐ PRIORITY

**Selection:** Random with constraint: At least one of methodologies 1 or 8 (functional/user-focused) must be selected in each pass. No reuse in current clean pass sequence.

**Configuration:**
```javascript
{
  mode: 'phase-review',
  subject: {
    type: 'deliverables',
    data: { phase, deliverables, requirements }
  },
  // Methodologies auto-configured from phase-review preset
  // verify, fix auto-configured from phase-review preset
  convergence: {
    requiredCleanPasses: 3,
    clearContextBetweenPasses: true  // Fresh review each pass
  },
  model: 'claude-opus-4-5'  // Use opus for high-quality reviews
}
```

**When to use:** Phase transitions in development flows, deliverable quality gates

---

## Generic Convergence Algorithm

```javascript
async function executeConvergence(config) {
  // Apply mode preset if specified
  if (config.mode && MODE_PRESETS[config.mode]) {
    config = applyModePreset(config);
  }

  const state = {
    passes: [],
    consecutiveClean: 0,
    issues: [],
    usedMethodologiesInCleanSequence: new Set(),  // Track used methodologies
    availableMethodologies: [...config.methodologies],  // Pool of methodologies
    totalIssuesFixed: 0,
    contextMonitor: initializeContextMonitor(),
    loopDetector: initializeLoopDetector()
  };

  // Set model if specified
  if (config.model) {
    setModel(config.model);
  }

  console.log(`\n═══ CONVERGENCE: ${config.mode || 'custom'} ═══`);
  console.log(`Subject: ${config.subject.type}`);
  console.log(`Methodologies: ${config.methodologies.map(m => m.name).join(', ')}`);
  console.log(`Required clean passes: ${config.convergence.requiredCleanPasses}`);
  console.log(`Model: ${config.model || 'default'}`);

  while (state.consecutiveClean < config.convergence.requiredCleanPasses
         && state.passes.length < config.convergence.maxIterations) {

    const passNumber = state.passes.length + 1;

    // Select random methodology (not used in current clean sequence)
    const unusedMethodologies = state.availableMethodologies.filter(
      m => !state.usedMethodologiesInCleanSequence.has(m.name)
    );

    // If all methodologies used, reset the pool (shouldn't happen with proper pool size)
    if (unusedMethodologies.length === 0) {
      console.log('⚠️ All methodologies exhausted, resetting pool');
      state.usedMethodologiesInCleanSequence.clear();
      unusedMethodologies.push(...state.availableMethodologies);
    }

    // CONSTRAINT: Ensure at least one functional/user-focused methodology in clean sequence
    // Check if any priority methodology has been used in current clean sequence
    const priorityMethodologies = config.methodologies.filter(m => m.priority === true);
    const priorityUsedInCleanSequence = Array.from(state.usedMethodologiesInCleanSequence).some(
      usedName => priorityMethodologies.some(pm => pm.name === usedName)
    );

    const unusedPriorityMethodologies = unusedMethodologies.filter(m =>
      priorityMethodologies.some(pm => pm.name === m.name)
    );

    // Force selection of priority methodology if:
    // 1. No priority methodology used yet in this clean sequence, AND
    // 2. Priority methodologies are still available
    let methodology;
    if (!priorityUsedInCleanSequence && unusedPriorityMethodologies.length > 0) {
      // Force priority methodology selection (functional/user-focused)
      const randomIndex = Math.floor(Math.random() * unusedPriorityMethodologies.length);
      methodology = unusedPriorityMethodologies[randomIndex];
      console.log('→ PRIORITY methodology selected (functional/user-focused required)');
    } else {
      // Random selection from all unused methodologies
      const randomIndex = Math.floor(Math.random() * unusedMethodologies.length);
      methodology = unusedMethodologies[randomIndex];
    }

    console.log(`\n--- Pass ${passNumber}: ${methodology.name} (random selection) ---`);
    console.log(`Description: ${methodology.description || '(no description)'}`);
    console.log(`Pool: ${state.availableMethodologies.length} total, ${unusedMethodologies.length} unused`);

    // manage-context integration: Check context usage
    if (state.contextMonitor.usage > 0.75) {
      console.log(`⚠️ Context usage high (${Math.round(state.contextMonitor.usage * 100)}%)`);
      const checkpoint = await manage_context.chunk_work({
        completed: {
          passes: state.passes,
          issuesFixed: state.totalIssuesFixed
        },
        remaining: `${config.convergence.requiredCleanPasses - state.consecutiveClean} clean passes needed`
      });
      console.log(`✓ Work chunked, checkpoint: ${checkpoint.path}`);
      state.contextMonitor.usage = 0.4;  // Reset
    }

    // Clear context if configured
    if (config.convergence.clearContextBetweenPasses) {
      await manage_context.clear_context({
        preserve: ['subject', 'methodologies', 'priorIssues']
      });
      console.log('✓ Context cleared for fresh review');
    }

    // Execute methodology
    const result = await methodology.executor(config.subject.data);

    // verify-evidence integration: Verify results are valid
    const resultsValid = await verify_evidence.check({
      claim: `${methodology.name} results are valid`,
      evidence: [
        "Methodology executed successfully",
        "No execution errors or timeouts",
        "Results format is valid"
      ]
    });

    if (!resultsValid.verified) {
      console.log(`⚠️ ${methodology.name} results verification failed`);
      state.passes.push({
        passNumber,
        methodology: methodology.name,
        isClean: false,
        issuesFound: 0,
        skipped: true,
        reason: 'Results verification failed'
      });
      continue;  // Skip to next iteration
    }

    // Verify if clean
    const isClean = await config.verify.clean(result);

    // verify-evidence integration: Confirm clean pass
    if (isClean && config.verify.evidence) {
      const cleanVerified = await verify_evidence.check({
        claim: `${config.mode || 'subject'} is clean`,
        evidence: config.verify.evidence
      });

      if (!cleanVerified.verified) {
        console.log('⚠️ Clean pass verification failed - treating as not clean');
        isClean = false;
      }
    }

    if (isClean) {
      state.consecutiveClean++;
      console.log(`✓ Clean pass ${state.consecutiveClean}/${config.convergence.requiredCleanPasses}`);

      // Mark methodology as used in this clean sequence
      state.usedMethodologiesInCleanSequence.add(methodology.name);
      console.log(`→ Methodology '${methodology.name}' marked as used`);
      console.log(`→ Clean sequence methodologies: [${Array.from(state.usedMethodologiesInCleanSequence).join(', ')}]`);

    } else {
      // Issues found - reset consecutive counter AND used methodologies
      console.log(`✗ Issues found: ${result.issues?.length || 0}`);
      state.consecutiveClean = 0;
      state.usedMethodologiesInCleanSequence.clear();  // Reset methodology tracking
      console.log(`→ Clean sequence reset - all methodologies available again`);
      state.issues.push(...(result.issues || []));

      // error-reflection integration
      if (config.learning.runErrorReflection && result.issues?.length > 0) {
        const reflection = await error_reflection.analyze(result.issues);

        // pattern-library integration
        if (config.learning.logToPatternLibrary) {
          await pattern_library.update({
            antipatterns: reflection.antipatterns,
            prevention: reflection.prevention_measures
          });
          console.log(`✓ Logged ${reflection.antipatterns.length} antipatterns to pattern library`);
        }
      }

      // Create backup if configured
      if (config.fix.backup) {
        await createBackup();
        console.log('✓ Backup created before fixes');
      }

      // Fix issues with detect-infinite-loop integration
      const fixResults = await fixIssuesWithLoopDetection(
        result.issues,
        config.fix.executor,
        state.loopDetector
      );

      state.totalIssuesFixed += fixResults.fixed;
      console.log(`✓ Fixed ${fixResults.fixed} issues`);

      if (fixResults.loopsDetected > 0) {
        console.log(`⚠️ ${fixResults.loopsDetected} infinite loops detected and pivoted`);
      }
    }

    state.passes.push({
      passNumber,
      methodology: methodology.name,
      isClean,
      issuesFound: result.issues?.length || 0
    });

    // Update context usage estimate
    state.contextMonitor.usage += 0.15;  // Estimate increase per pass
  }

  // Convergence result
  const converged = state.consecutiveClean >= config.convergence.requiredCleanPasses;

  console.log(`\n═══ CONVERGENCE ${converged ? 'COMPLETE ✓' : 'FAILED ✗'} ═══`);
  console.log(`Total passes: ${state.passes.length}`);
  console.log(`Issues found: ${state.issues.length}`);
  console.log(`Issues fixed: ${state.totalIssuesFixed}`);
  console.log(`Clean passes: ${state.consecutiveClean}/${config.convergence.requiredCleanPasses}`);
  console.log(`Infinite loops prevented: ${state.loopDetector.total_detections || 0}`);
  console.log(`Context chunks: ${state.contextMonitor.chunks || 0}`);

  return {
    converged,
    passes: state.passes,
    issues: state.issues,
    issuesFixed: state.totalIssuesFixed,
    cleanPasses: state.consecutiveClean,
    monitoring: {
      loopsDetected: state.loopDetector.total_detections || 0,
      contextChunks: state.contextMonitor.chunks || 0
    }
  };
}

/**
 * Fix issues with detect-infinite-loop integration
 */
async function fixIssuesWithLoopDetection(issues, fixExecutor, loopDetector) {
  let fixed = 0;
  let loopsDetected = 0;

  for (const issue of issues) {
    // detect-infinite-loop integration: Track fix attempts
    const fixSignature = getFixSignature(issue);
    loopDetector.record_attempt(fixSignature);

    if (loopDetector.is_stuck(fixSignature)) {
      console.log(`⚠️ INFINITE LOOP DETECTED: ${issue.description}`);
      console.log(`   Attempted ${loopDetector.count(fixSignature)} times`);

      // Generate alternatives
      const alternatives = await detect_infinite_loop.generate_alternatives({
        failed_approach: issue,
        attempts: loopDetector.count(fixSignature)
      });

      console.log(`   Pivoting to alternative approach...`);
      issue.alternative = alternatives[0];  // Use first alternative
      loopsDetected++;
    }

    // Apply fix (may be alternative if loop detected)
    const fixResult = await fixExecutor([issue]);

    // verify-evidence: Confirm fix applied
    const fixVerified = await verify_evidence.check({
      claim: `Fix applied for: ${issue.description}`,
      evidence: [
        "No errors during application",
        "Target modified",
        "Tests still passing"
      ]
    });

    if (fixVerified.verified) {
      fixed += fixResult.fixed || 0;
    } else {
      console.log(`⚠️ Fix verification failed: ${issue.description}`);
      // Don't count as fixed
    }
  }

  return { fixed, loopsDetected };
}

function getFixSignature(issue) {
  return `${issue.file || 'unknown'}:${issue.line || 0}:${issue.type || 'unknown'}`;
}
```

---

## Mode Preset Definitions

### Audit Mode Preset

```javascript
const AUDIT_MODE_PRESET = {
  methodologies: [
    {
      name: 'technical',
      description: 'How it\'s built (security, code-quality, performance)',
      priority: true,  // PRIORITY: Functional/completeness focused
      executor: async (data) => {
        const results = await runAudits(data, [
          'security-architecture',
          'code-quality',
          'performance'
        ]);
        return {
          issues: aggregateIssues(results),
          evidence: results.map(r => `${r.audit}: ${r.issues.length} issues`)
        };
      }
    },
    {
      name: 'user',
      description: 'How it\'s experienced (accessibility, ux)',
      priority: true,  // PRIORITY: User-focused
      executor: async (data) => {
        const results = await runAudits(data, [
          'accessibility',
          'ux-performance',
          'auth-flow-testing'
        ]);
        return {
          issues: aggregateIssues(results),
          evidence: results.map(r => `${r.audit}: ${r.issues.length} issues`)
        };
      }
    },
    {
      name: 'holistic',
      description: 'How it fits together (consistency, navigation, docs)',
      executor: async (data) => {
        const results = await runAudits(data, [
          'consistency',
          'navigation',
          'documentation',
          'dependency'
        ]);
        return {
          issues: aggregateIssues(results),
          evidence: results.map(r => `${r.audit}: ${r.issues.length} issues`)
        };
      }
    }
  ],

  verify: {
    clean: async (result) => {
      return result.issues.length === 0;
    },
    evidence: [
      "All 3 methodologies: 0 issues",
      "No critical or high issues",
      "All audits completed successfully"
    ]
  },

  fix: {
    executor: async (issues) => {
      const plan = await generateFixPlan(issues, {
        use_pattern_library: true,
        check_known_fixes: true
      });
      return await implementFixes(plan);
    },
    backup: true
  },

  convergence: {
    requiredCleanPasses: 3,
    maxIterations: 10,
    rotateMethodologies: true,
    clearContextBetweenPasses: false  // Keep audit context
  },

  learning: {
    logToPatternLibrary: true,
    runErrorReflection: true,
    trackMetrics: true
  }
};
```

### Phase-Review Mode Preset

```javascript
const PHASE_REVIEW_MODE_PRESET = {
  methodologies: [
    {
      name: 'top-down',
      description: 'Requirements → Implementation (completeness)',
      priority: true,  // PRIORITY: Functional/completeness focused
      executor: async (data) => {
        const issues = [];
        const { phase, deliverables, requirements } = data;

        // Check all requirements are met
        for (const req of requirements) {
          const met = await checkRequirementMet(req, deliverables);
          if (!met) {
            issues.push({
              type: 'missing-requirement',
              description: `Requirement not met: ${req.description}`,
              file: phase.name,
              severity: 'high'
            });
          }
        }

        // Check deliverable completeness
        for (const deliverable of deliverables) {
          const complete = await checkDeliverableComplete(deliverable);
          if (!complete) {
            issues.push({
              type: 'incomplete-deliverable',
              description: `Deliverable incomplete: ${deliverable.name}`,
              file: deliverable.path,
              severity: 'medium'
            });
          }
        }

        return {
          issues,
          evidence: [
            `${requirements.length} requirements checked`,
            `${deliverables.length} deliverables reviewed`,
            `${issues.length} issues found`
          ]
        };
      }
    },
    {
      name: 'bottom-up',
      description: 'Implementation → Quality (consistency)',
      executor: async (data) => {
        const issues = [];
        const { deliverables } = data;

        // Check internal consistency of each deliverable
        for (const deliverable of deliverables) {
          const consistencyIssues = await checkInternalConsistency(deliverable);
          issues.push(...consistencyIssues);
        }

        // Check cross-deliverable consistency
        const crossIssues = await checkCrossDeliverableConsistency(deliverables);
        issues.push(...crossIssues);

        return {
          issues,
          evidence: [
            `${deliverables.length} deliverables checked for consistency`,
            `${issues.length} issues found`
          ]
        };
      }
    },
    {
      name: 'lateral',
      description: 'Cross-cutting concerns (integration, ux)',
      priority: true,  // PRIORITY: User-focused (includes UX review)
      executor: async (data) => {
        const issues = [];
        const { phase, deliverables } = data;

        // Check integration points
        const integrationIssues = await checkIntegrationPoints(deliverables);
        issues.push(...integrationIssues);

        // Check architectural alignment
        const archIssues = await checkArchitecturalAlignment(phase, deliverables);
        issues.push(...archIssues);

        // Check security/performance/ux implications
        const crossCuttingIssues = await checkCrossCuttingConcerns(deliverables);
        issues.push(...crossCuttingIssues);

        return {
          issues,
          evidence: [
            `Integration points checked`,
            `Architectural alignment verified`,
            `Cross-cutting concerns reviewed`,
            `${issues.length} issues found`
          ]
        };
      }
    }
  ],

  verify: {
    clean: async (result) => {
      return result.issues.length === 0;
    },
    evidence: [
      "All requirements met",
      "All deliverables complete",
      "No inconsistencies found",
      "Ready for next phase"
    ]
  },

  fix: {
    executor: async (issues) => {
      return await fixPhaseIssues(issues);
    },
    backup: false  // Phase work is iterative, no backup needed
  },

  convergence: {
    requiredCleanPasses: 3,
    maxIterations: 10,
    rotateMethodologies: true,
    clearContextBetweenPasses: true  // Fresh review each pass
  },

  learning: {
    logToPatternLibrary: true,
    runErrorReflection: true,
    trackMetrics: true
  }
};
```

---

## Usage Examples

### Example 1: Audit Convergence

```javascript
// Load skill
const convergence = await loadSkill('multi-methodology-convergence');

// Run audit convergence (simple API)
const result = await convergence.run({
  mode: 'audit',
  subject: {
    data: { projectPath: '/path/to/project' }
  }
});

if (result.converged) {
  console.log('✓ Audit convergence complete - production ready');
  console.log(`  Fixed ${result.issuesFixed} issues in ${result.passes.length} passes`);
} else {
  console.log('✗ Audit convergence failed - manual review required');
}
```

### Example 2: Phase Review

```javascript
// Load skill
const convergence = await loadSkill('multi-methodology-convergence');

// Run phase review (with opus model for high quality)
const result = await convergence.run({
  mode: 'phase-review',
  subject: {
    data: {
      phase: { name: 'requirements', scope: [...] },
      deliverables: [...],
      requirements: [...]
    }
  },
  model: 'claude-opus-4-5'  // Override to use opus
});

if (result.converged) {
  console.log('✓ Phase review complete - proceeding to next phase');
} else {
  console.log('✗ Phase review issues remain');
}
```

### Example 3: Custom Convergence

```javascript
const result = await convergence.run({
  mode: 'custom',
  subject: {
    type: 'architecture',
    data: { architecture, requirements, constraints }
  },
  methodologies: [
    {
      name: 'scalability',
      executor: async (data) => reviewScalability(data.architecture)
    },
    {
      name: 'security',
      executor: async (data) => reviewSecurity(data.architecture)
    },
    {
      name: 'maintainability',
      executor: async (data) => reviewMaintainability(data.architecture)
    }
  ],
  verify: {
    clean: async (result) => result.issues.length === 0
  },
  fix: {
    executor: async (issues) => updateArchitecture(issues)
  }
});
```

---

## Configuration

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

## Backward Compatibility

**For existing convergence-engine users:**

```javascript
// Old way (still works via symlink)
const convergence = await loadSkill('convergence-engine');
await convergence.run(projectPath);

// New way (explicit mode)
const convergence = await loadSkill('multi-methodology-convergence');
await convergence.run({
  mode: 'audit',
  subject: { data: { projectPath } }
});
```

**Symlink:** `core/audit/convergence-engine` → `core/learning/convergence/multi-methodology-convergence`

---

*End of Multi-Methodology Convergence*
*Part of v4.0.0 Universal Skills Ecosystem*
*Category: Learning / Convergence*
*Supports: audit, phase-review, custom modes*
*Learning Integration: verify-evidence, detect-infinite-loop, manage-context, pattern-library*
