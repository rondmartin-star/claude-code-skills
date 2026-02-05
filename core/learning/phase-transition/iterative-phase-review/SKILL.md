---
name: iterative-phase-review
description: >
  Convenient wrapper for phase transition quality reviews using multi-methodology
  convergence. Iteratively reviews phase deliverables with 8 orthogonal methodologies
  until achieving 3 consecutive clean passes. Uses Claude Opus 4.5 for highest quality.
  Use when: completing a development phase, transitioning between phases, validating
  phase deliverables before proceeding.
---

# Iterative Phase Review

**Purpose:** Phase transition quality gate with multi-methodology convergence
**Size:** ~8 KB
**Type:** Core Learning - Phase Transition
**Model:** Claude Opus 4.5 (highest quality reviews)
**Methodologies:** 8 orthogonal approaches (random selection)

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Review this phase"
- "Phase review"
- "Check phase deliverables"
- "Validate phase completion"
- "Phase transition review"
- "Ready to move to next phase"

**Context Indicators:**
- User completing a development phase
- User requesting phase validation
- Before phase transition in development workflow
- Integrated into battle-plan Phase 5.5
- Integrated into windows-app-orchestrator phase gates

## ❌ DO NOT LOAD WHEN

- Single-pass validation sufficient
- Early phase (not enough deliverables yet)
- User just wants quick status check

---

## Overview

**Purpose:** Ensure phase deliverables meet all requirements before proceeding

**How It Works:**
1. Randomly select methodology from pool of 8 (not used in current clean sequence)
2. Review phase deliverables with selected methodology
3. If clean → increment clean pass counter, mark methodology as used
4. If issues found → reset counter, clear used methodologies, fix issues
5. Repeat until 3 consecutive clean passes achieved
6. Context cleared between passes for fresh perspectives

**Model:** Claude Opus 4.5 for highest quality reviews

**Learning Integration:**
- verify-evidence: Validates review results
- detect-infinite-loop: Pivots after 3 failed fix attempts
- manage-context: Chunks work at 75% context usage
- error-reflection: Analyzes issues with 5 Whys
- pattern-library: Stores antipatterns and prevention measures

---

## 8 Orthogonal Review Methodologies

**Random selection ensures diverse perspectives. No reuse within clean pass sequences.**

### 1. Top-Down-Requirements
**Direction:** Requirements → Deliverables
**Focus:** Completeness check

**Questions:**
- Are all requirements addressed?
- Is each requirement traceable to deliverables?
- Are there missing requirements?
- Are deliverables sufficient for requirements?

**Example:**
```javascript
// Check requirements coverage
for (const req of requirements) {
  const coverage = findDeliverablesAddressing(req);
  if (coverage.length === 0) {
    issues.push({
      type: 'missing-requirement',
      requirement: req.id,
      description: `Requirement ${req.id} not addressed by any deliverable`
    });
  }
}
```

### 2. Top-Down-Architecture
**Direction:** Architecture → Implementation
**Focus:** Design alignment

**Questions:**
- Does implementation follow architecture?
- Are architectural decisions reflected in code?
- Are there deviations from planned architecture?
- Is the architecture actually implementable?

### 3. Bottom-Up-Quality
**Direction:** Code/Artifacts → Standards
**Focus:** Quality validation

**Questions:**
- Do artifacts meet quality standards?
- Is code well-structured and maintainable?
- Are tests comprehensive?
- Is documentation complete?

### 4. Bottom-Up-Consistency
**Direction:** Low-level → High-level
**Focus:** Internal consistency

**Questions:**
- Are naming conventions consistent?
- Are patterns used consistently?
- Are data structures consistent?
- Are APIs consistent?

### 5. Lateral-Integration
**Direction:** Across components
**Focus:** Component boundaries and interfaces

**Questions:**
- Do components integrate correctly?
- Are interfaces well-defined?
- Are dependencies managed properly?
- Are integration points tested?

### 6. Lateral-Security
**Direction:** Across concerns
**Focus:** Security architecture and implementation

**Questions:**
- Is authentication implemented correctly?
- Is authorization enforced?
- Are inputs validated?
- Are secrets managed securely?

### 7. Lateral-Performance
**Direction:** Across concerns
**Focus:** Performance characteristics

**Questions:**
- Are there performance bottlenecks?
- Is resource usage appropriate?
- Are queries optimized?
- Is caching used effectively?

### 8. Lateral-UX
**Direction:** Across features
**Focus:** User experience and interaction flows

**Questions:**
- Is the UX consistent?
- Are interactions intuitive?
- Is error handling user-friendly?
- Are workflows efficient?

---

## Usage

### Basic Usage (Auto-Configure)

```javascript
const phaseReview = await loadSkill('iterative-phase-review');

const result = await phaseReview.run({
  phase: {
    name: 'requirements',
    scope: ['user stories', 'acceptance criteria', 'data models']
  },
  deliverables: [
    { type: 'user-story', path: 'docs/user-stories.md' },
    { type: 'acceptance-criteria', path: 'docs/acceptance.md' },
    { type: 'data-model', path: 'docs/data-model.md' }
  ],
  requirements: [
    { id: 'REQ-001', description: 'User authentication' },
    { id: 'REQ-002', description: 'Profile management' }
  ]
});

// Result:
// {
//   converged: true,
//   passes: [...],  // All pass details
//   issues: [...],  // All issues found
//   issuesFixed: 12,
//   cleanPasses: 3  // Consecutive clean passes achieved
// }
```

### With Custom Configuration

```javascript
const result = await phaseReview.run({
  phase: { name: 'build', scope: ['implementation', 'tests'] },
  deliverables: [...],
  requirements: [...],

  // Override defaults
  convergence: {
    requiredCleanPasses: 3,  // Default
    maxIterations: 15         // Override max (default: 10)
  }
});
```

---

## Phase-Specific Usage

### Requirements Phase

```javascript
await phaseReview.run({
  phase: {
    name: 'requirements',
    scope: ['user stories', 'acceptance criteria', 'data models']
  },
  deliverables: [
    { type: 'user-story', path: 'docs/user-stories.md' },
    { type: 'acceptance-criteria', path: 'docs/acceptance.md' },
    { type: 'data-model', path: 'docs/data-model.md' }
  ],
  requirements: extractedRequirements
});
```

**Focus Areas:**
- Completeness (all stakeholder needs captured)
- Clarity (unambiguous requirements)
- Testability (acceptance criteria defined)
- Feasibility (requirements achievable)

### System Design Phase

```javascript
await phaseReview.run({
  phase: {
    name: 'system-design',
    scope: ['data models', 'API design', 'architecture']
  },
  deliverables: [
    { type: 'data-model', path: 'design/data-model.md' },
    { type: 'api-spec', path: 'design/api-spec.yaml' },
    { type: 'architecture', path: 'design/architecture.md' }
  ],
  requirements: phaseRequirements
});
```

**Focus Areas:**
- Alignment with requirements
- Scalability and performance considerations
- Security architecture
- API consistency and usability

### UI Design Phase

```javascript
await phaseReview.run({
  phase: {
    name: 'ui-design',
    scope: ['page inventory', 'navigation flows', 'forms']
  },
  deliverables: [
    { type: 'page-inventory', path: 'design/pages.md' },
    { type: 'navigation', path: 'design/navigation.md' },
    { type: 'forms', path: 'design/forms.md' }
  ],
  requirements: uiRequirements
});
```

**Focus Areas:**
- UX consistency
- Accessibility considerations
- Navigation flows
- Form validation

### Build Phase

```javascript
await phaseReview.run({
  phase: {
    name: 'build',
    scope: ['implementation', 'tests', 'documentation']
  },
  deliverables: [
    { type: 'code', path: 'src/' },
    { type: 'tests', path: 'tests/' },
    { type: 'docs', path: 'docs/' }
  ],
  requirements: implementationRequirements
});
```

**Focus Areas:**
- Code quality and maintainability
- Test coverage
- Security implementation
- Performance optimization

### Deployment Phase

```javascript
await phaseReview.run({
  phase: {
    name: 'deployment',
    scope: ['service config', 'health checks', 'installer']
  },
  deliverables: [
    { type: 'service-config', path: 'deployment/nssm-config.json' },
    { type: 'health-checks', path: 'src/health/' },
    { type: 'installer', path: 'installer/' }
  ],
  requirements: deploymentRequirements
});
```

**Focus Areas:**
- Deployment readiness
- Health check coverage
- Monitoring and logging
- Rollback capabilities

---

## Implementation

**Note:** This is a convenience wrapper around `multi-methodology-convergence`

```javascript
async function run(config) {
  // Load multi-methodology-convergence
  const convergence = await loadSkill('multi-methodology-convergence');

  // Configure for phase-review mode
  return await convergence.run({
    mode: 'phase-review',

    subject: {
      type: 'deliverables',
      data: {
        phase: config.phase,
        deliverables: config.deliverables,
        requirements: config.requirements
      }
    },

    // Use opus for highest quality reviews
    model: 'claude-opus-4-5',

    // Convergence settings
    convergence: {
      requiredCleanPasses: config.convergence?.requiredCleanPasses || 3,
      maxIterations: config.convergence?.maxIterations || 10,
      clearContextBetweenPasses: true  // Fresh review each pass
    },

    // Learning integration enabled
    learning: {
      logToPatternLibrary: true,
      runErrorReflection: true,
      trackMetrics: true
    }
  });
}
```

---

## Integration Points

### Battle-Plan Integration (Phase 5.5)

Used automatically in battle-plan after Phase 5 (execution), before Phase 6 (verification).

```javascript
// In battle-plan orchestrator
PHASE 5: EXECUTION
  → Execute task
  → Task complete

PHASE 5.5: ITERATIVE PHASE REVIEW (NEW)
  → Load iterative-phase-review
  → Review phase deliverables
  → Converge until 3 clean passes
  → Log learnings to pattern library

PHASE 6: VERIFICATION
  → Run verify-evidence on final state
  → Confirm completion
```

### Windows App Orchestrator Integration

Used at 5 phase transition gates:

```javascript
// In windows-app-orchestrator
Phase 1: Requirements
  → Complete requirements
  → GATE 1: iterative-phase-review
    - Review user stories, acceptance criteria, data models
    - Converge until clean
  → Proceed to System Design

Phase 2: System Design
  → Complete design
  → GATE 2: iterative-phase-review
    - Review data models, API specs, architecture
    - Converge until clean
  → Proceed to UI Design

Phase 3: UI Design
  → Complete UI design
  → GATE 3: iterative-phase-review
    - Review pages, navigation, forms
    - Converge until clean
  → Proceed to Build

Phase 4: Build
  → Complete implementation
  → GATE 4: iterative-phase-review
    - Review code, tests, documentation
    - Converge until clean
  → Proceed to Deployment

Phase 5: Deployment (Supervision)
  → Complete deployment setup
  → GATE 5: iterative-phase-review
    - Review service config, health checks, installer
    - Converge until clean
  → Production Ready
```

---

## Convergence Behavior

### Convergence Requirements
- **3 consecutive clean passes** required
- **8 methodology pool** (random selection)
- **No methodology reuse** within clean pass sequences
- **Max 10 iterations** before timeout

### Example Convergence Flow

```
═══ PHASE REVIEW: requirements ═══

Pass 1: Top-Down-Requirements (random selection)
  → Found 3 issues (missing requirements)
  ✗ Issues found, fixing...
  → Fixed 3 issues
  → Clean sequence reset

Pass 2: Lateral-Integration (random selection)
  → Found 2 issues (interface mismatches)
  ✗ Issues found, fixing...
  → Fixed 2 issues
  → Clean sequence reset

Pass 3: Bottom-Up-Consistency (random selection)
  → All checks passed
  ✓ Clean pass 1/3
  → Methodology 'Bottom-Up-Consistency' marked as used

Pass 4: Lateral-UX (random selection)
  → All checks passed
  ✓ Clean pass 2/3
  → Methodology 'Lateral-UX' marked as used

Pass 5: Top-Down-Architecture (random selection)
  → All checks passed
  ✓ Clean pass 3/3
  → Methodology 'Top-Down-Architecture' marked as used

═══ CONVERGENCE COMPLETE ✓ ═══
Total passes: 5
Issues found: 5
Issues fixed: 5
Clean passes: 3/3
Methodologies used in final sequence: [Bottom-Up-Consistency, Lateral-UX, Top-Down-Architecture]
```

---

## Return Value

```javascript
{
  // Convergence result
  converged: boolean,  // true if 3 clean passes achieved

  // Pass details
  passes: [
    {
      passNumber: 1,
      methodology: 'Top-Down-Requirements',
      isClean: false,
      issuesFound: 3
    },
    // ... more passes
  ],

  // Issue tracking
  issues: [
    {
      type: 'missing-requirement',
      severity: 'high',
      description: 'Requirement REQ-003 not addressed',
      fix: 'Add user story for password reset'
    },
    // ... more issues
  ],

  // Fix statistics
  issuesFixed: 5,
  cleanPasses: 3,

  // Monitoring
  monitoring: {
    loopsDetected: 0,  // Infinite loops prevented
    contextChunks: 0   // Context chunks created
  }
}
```

---

## Learning Integration Details

### verify-evidence
**When:** After each methodology execution
**Purpose:** Validate review results are legitimate
**Example:**
```javascript
claim: "Top-Down-Requirements review is valid"
evidence: [
  "All requirements checked",
  "No execution errors",
  "Results format valid"
]
```

### detect-infinite-loop
**When:** During issue fixing
**Purpose:** Prevent repeated failed fix attempts
**Behavior:**
- Track fix attempts per issue
- After 3 failed attempts → pivot strategy
- Escalate to user if pivot fails

### manage-context
**When:** Context usage > 75%
**Purpose:** Chunk work to prevent degradation
**Behavior:**
- Create checkpoint with current state
- Reset context usage
- Continue from checkpoint

**Also:** Clear context between passes for fresh reviews

### error-reflection
**When:** Issues found
**Purpose:** Analyze root causes
**Output:**
- Antipatterns identified
- Root causes (5 Whys analysis)
- Prevention measures

### pattern-library
**When:** After error-reflection
**Purpose:** Store learnings for compound learning
**Storage:**
- Antipatterns: `.corpus/learning/antipatterns/phase-review/`
- Prevention: Measures to avoid issues in future

---

## Configuration

### Minimal Configuration
```javascript
{
  phase: { name: 'requirements', scope: [...] },
  deliverables: [...],
  requirements: [...]
}
```

### Full Configuration
```javascript
{
  phase: {
    name: 'requirements',
    scope: ['user stories', 'acceptance criteria', 'data models'],
    dependencies: ['stakeholder interviews completed']
  },

  deliverables: [
    {
      type: 'user-story',
      path: 'docs/user-stories.md',
      required: true
    },
    // ... more deliverables
  ],

  requirements: [
    {
      id: 'REQ-001',
      description: 'User authentication',
      priority: 'high',
      source: 'stakeholder interview'
    },
    // ... more requirements
  ],

  convergence: {
    requiredCleanPasses: 3,   // Override
    maxIterations: 15          // Override
  }
}
```

---

## Best Practices

### 1. Complete Phases Before Review
Don't trigger review until phase is genuinely complete. Incomplete phases will fail review repeatedly.

### 2. Provide Comprehensive Deliverables
Include all relevant deliverables for accurate review. Missing deliverables = incomplete requirements coverage.

### 3. Define Clear Requirements
Well-defined requirements enable better top-down reviews. Ambiguous requirements → ambiguous reviews.

### 4. Let Convergence Complete
Trust the 3-pass convergence. Don't interrupt or skip. Each methodology provides unique insights.

### 5. Review Pattern Library
After convergence, check pattern library for learnings. Apply prevention measures to future phases.

---

## Files

**Location:** `core/learning/phase-transition/iterative-phase-review/`

**Files:**
- `SKILL.md` - This file
- `README.md` - Quick reference
- `CHANGELOG.md` - Version history

---

## Version

**v1.0.0** (2026-02-05)
- Initial release
- Wrapper for multi-methodology-convergence (phase-review mode)
- 8 orthogonal methodologies
- Random selection with no-reuse constraint
- Claude Opus 4.5 for highest quality
- Full learning integration

---

*Part of v4.0 Universal Skills Ecosystem - Learning Integration*
*Uses: multi-methodology-convergence (phase-review mode)*
