# Comprehensive Learning Integration - Option C

**Date:** 2026-02-04
**Scope:** Full battle-plan integration across entire v4.0 ecosystem
**Philosophy:** Learning skills as foundational infrastructure, not add-on features

---

## Vision: Learning-First Architecture

**Current State:** Skills execute → maybe learn from errors
**Target State:** Learn → Plan → Execute → Reflect → Update → Compound

**Core Principle:** Every significant operation flows through battle-plan pattern

---

## Architecture Overview

### New Ecosystem Structure

```
v4.0 Learning-First Ecosystem
├── core/
│   ├── core-orchestrator/           ← ENHANCED: Routes through battle-plan
│   │
│   ├── learning/                    ← FOUNDATIONAL (not optional)
│   │   ├── orchestrators/           ← NEW: Battle-plan variants
│   │   │   ├── battle-plan/         # Master orchestrator
│   │   │   ├── corpus-battle-plan/  # Corpus operations variant
│   │   │   ├── audit-battle-plan/   # Audit operations variant
│   │   │   └── content-battle-plan/ # Content operations variant
│   │   │
│   │   ├── pre-execution/           ← BEFORE skills
│   │   │   ├── rubber-duck/         # Clarify scope
│   │   │   ├── pattern-library/     # Check known solutions
│   │   │   ├── pre-mortem/          # Anticipate failures
│   │   │   └── you-sure/            # Confirmation gate
│   │   │
│   │   ├── during-execution/        ← DURING skills
│   │   │   ├── prove-it/            # Demand evidence
│   │   │   ├── pivot/               # Detect infinite loops
│   │   │   └── dont-be-greedy/      # Context management
│   │   │
│   │   ├── post-execution/          ← AFTER skills
│   │   │   ├── error-reflection/    # Analyze failures
│   │   │   ├── ship-it/             # Declare done
│   │   │   └── pattern-update/      # Capture learnings
│   │   │
│   │   └── infrastructure/          ← SUPPORT
│   │       ├── pattern-library/     # Central pattern store
│   │       ├── metrics-tracker/     # Learning effectiveness
│   │       └── learning-config/     # Configuration
│   │
│   ├── corpus/
│   │   ├── corpus-orchestrator/     ← ENHANCED: Uses corpus-battle-plan
│   │   ├── corpus-init/             ← ENHANCED: Wrapped in battle-plan
│   │   ├── corpus-convert/          ← ENHANCED: Wrapped in battle-plan
│   │   └── ...
│   │
│   ├── audit/
│   │   ├── audit-orchestrator/      ← ENHANCED: Uses audit-battle-plan
│   │   ├── audits/                  ← ENHANCED: Each wrapped
│   │   ├── convergence-engine/      ← ENHANCED: Full battle-plan integration
│   │   └── fix-planner/             ← ENHANCED: Pattern-aware
│   │
│   ├── content/
│   │   ├── content-orchestrator/    ← ENHANCED: Uses content-battle-plan
│   │   └── ...
│   │
│   └── utilities/
│       └── ...                      ← OPTIONAL: Simple utilities skip battle-plan
```

### Execution Flow: Any Complex Task

```
User Request
    ↓
Core Orchestrator (detects complexity + category)
    ↓
[IF COMPLEX] → Battle-Plan Orchestrator
    ├─ 1. RUBBER-DUCK (clarify scope, resolve ambiguity)
    ├─ 2. PATTERN-LIBRARY (search for similar past tasks)
    │    └─ Returns: {patterns, antipatterns, recommendations}
    ├─ 3. PRE-MORTEM (imagine failure, using pattern insights)
    │    └─ Returns: {risks, preventions, goNoGo}
    ├─ 4. YOU-SURE (show plan, get user confirmation)
    │    └─ Returns: {approved, adjustments}
    │
    ├─ 5. EXECUTE (route to category orchestrator)
    │    ├─ Apply proven patterns automatically
    │    ├─ Monitor for known antipatterns
    │    ├─ PROVE-IT checkpoints during execution
    │    ├─ PIVOT if infinite loops detected
    │    └─ DONT-BE-GREEDY for context management
    │
    ├─ 6. POST-EXECUTION
    │    ├─ ERROR-REFLECTION (if errors/issues)
    │    │   └─ Extract patterns/antipatterns
    │    ├─ SHIP-IT (declare done, block perfectionism)
    │    └─ PATTERN-UPDATE (save learnings)
    │
    └─ 7. RETURN (with compound learning applied)
```

---

## Core Learning Skills (Expanded)

### Phase 1: Pre-Execution (Before)

#### 1. rubber-duck
**Trigger:** Before starting any task
**Purpose:** Force problem articulation, clarify scope

**Process:**
1. Explain task in plain language
2. Identify assumptions being made
3. List what's known vs. unknown
4. Generate clarifying questions
5. Validate understanding with user

**Example:**
```
User: "Add OAuth login"

Rubber-duck:
- What we're building: Third-party OAuth authentication
- Assumptions:
  * Using OAuth 2.0 (not 1.0)
  * Provider is Google/GitHub/etc. (which one?)
  * Existing user system needs integration (or new?)
- Unknowns:
  * Which OAuth provider?
  * Session management strategy?
  * Mobile app support needed?
- Questions for user:
  1. Which OAuth provider(s)?
  2. Replace existing auth or supplement?
  3. What happens to existing users?
```

#### 2. pattern-library (check)
**Already created** - enhanced with category-specific collections

**Enhancements:**
```javascript
// Category-specific pattern collections
.corpus/learning/patterns/
├── corpus-operations/
│   ├── initialization.json
│   ├── conversion.json
│   └── configuration.json
├── audit-operations/
│   ├── code-quality-fixes.json
│   ├── security-fixes.json
│   └── performance-fixes.json
├── content-operations/
│   ├── newsletter-patterns.json
│   ├── blog-patterns.json
│   └── documentation-patterns.json
└── cross-cutting/
    ├── authentication.json
    ├── error-handling.json
    └── testing.json
```

#### 3. pre-mortem (anticipate)
**Already created** - enhanced with category-specific risk databases

**Enhancements:**
```javascript
// Category-specific risk databases
.corpus/learning/risks/
├── corpus-risks.json      // Common corpus operation failures
├── audit-risks.json       // Common audit/fix failures
├── content-risks.json     // Common content creation failures
└── integration-risks.json // Cross-cutting integration failures
```

#### 4. you-sure (confirmation gate)
**NEW SKILL**

**Trigger:** Before executing complex/destructive operations
**Purpose:** Pause, summarize, get explicit approval

**Process:**
1. Summarize what's about to happen
2. List potential impacts (files changed, data modified, etc.)
3. Show rollback options if available
4. Highlight risks from pre-mortem
5. Require explicit user confirmation

**Example:**
```
Ready to execute: Initialize new corpus

What will happen:
✓ Create .corpus/ directory structure
✓ Generate corpus-config.json with these settings:
  - Name: my-project
  - Type: application
  - Audits: code-quality, security
✓ Initialize empty pattern library
✓ Create backup infrastructure

Potential impacts:
⚠ Will create 15 files in current directory
⚠ Requires write permissions
⚠ Will initialize git hooks (if enabled)

Rollback option:
✓ Can delete .corpus/ directory to undo

Known risks (from pre-mortem):
⚠ Wrong directory (severity: medium)
  Prevention: Verified pwd = /correct/path ✓

Proceed? [Y/n]
```

### Phase 2: During Execution

#### 5. prove-it (evidence requirement)
**NEW SKILL**

**Trigger:** Before declaring something done/true
**Purpose:** Combat hallucination, demand evidence

**Process:**
1. Intercept declarative statements
2. Require evidence (file contents, test results, command output)
3. Verify claims against actual codebase/config
4. Flag uncertain statements
5. Provide confidence levels

**Integration Points:**
```javascript
// In any skill that makes claims
async function declareComplete(task, result) {
  // PROVE-IT checkpoint
  const evidence = await proveIt.verify({
    claim: "OAuth implementation complete",
    requiredEvidence: [
      "OAuth config file exists with provider settings",
      "OAuth routes defined in API",
      "Token caching implemented",
      "Tests pass for OAuth flow"
    ]
  });

  if (!evidence.verified) {
    throw new Error(`Cannot verify: ${evidence.missing.join(', ')}`);
  }

  return result;
}
```

**Example:**
```
Claude: "OAuth implementation is complete"

Prove-it: ❌ EVIDENCE REQUIRED
- [✓] OAuth config file exists (verified: src/config/oauth.js)
- [✓] Routes defined (verified: src/routes/auth.js)
- [✗] Token caching implemented (NOT FOUND: no cache module)
- [✗] Tests pass (NOT RUN: no test results)

Confidence: 40% (2/4 requirements verified)
Status: INCOMPLETE
```

#### 6. pivot (detect infinite loops)
**NEW SKILL**

**Trigger:** After repeated failures on same approach
**Purpose:** Force strategy change, prevent infinite loops

**Process:**
1. Monitor approach being used
2. Track failure count for same approach
3. After N failures (default: 3), trigger pivot
4. Generate alternative strategies
5. Force Claude to try different approach

**Integration:**
```javascript
async function executeWithPivot(task, approach) {
  const attempts = [];

  while (true) {
    const result = await tryApproach(task, approach);

    if (result.success) {
      return result;
    }

    attempts.push({approach, error: result.error});

    // PIVOT checkpoint
    if (pivot.shouldPivot(attempts)) {
      console.log("⚠️ Pivot triggered: Tried same approach 3 times");
      console.log("Failed approach:", approach.description);

      const alternatives = await pivot.generateAlternatives({
        failedAttempts: attempts,
        task: task
      });

      console.log("Alternative strategies:");
      alternatives.forEach((alt, i) => {
        console.log(`${i + 1}. ${alt.description}`);
      });

      // Force strategy change
      approach = alternatives[0];
      console.log(`Pivoting to: ${approach.description}`);
    }
  }
}
```

**Example:**
```
Attempt 1: Install dependency via npm install
→ Failed: Network timeout

Attempt 2: Install dependency via npm install
→ Failed: Network timeout

Attempt 3: Install dependency via npm install
→ Failed: Network timeout

⚠️ PIVOT TRIGGERED: Same approach failed 3 times

Failed approach: "npm install directly"

Alternative strategies:
1. Check for cached package in ~/.npm
2. Try yarn instead of npm
3. Download package manually from registry
4. Use different registry (npmmirror, etc.)

Pivoting to: Check for cached package in ~/.npm
```

#### 7. dont-be-greedy (context management)
**NEW SKILL**

**Trigger:** During long sessions, before context limit
**Purpose:** Protect context window, chunk data, summarize

**Process:**
1. Monitor context usage (token count)
2. Before hitting limit, trigger chunking
3. Summarize completed work
4. Write summaries to files
5. Clear detailed context, keep summaries

**Integration:**
```javascript
async function executeLongTask(task) {
  const contextManager = new DontBeGreedy({
    maxTokens: 180000,  // Leave buffer
    chunkSize: 50000
  });

  while (task.hasMoreWork()) {
    // Check context before continuing
    if (contextManager.shouldChunk()) {
      console.log("⚠️ Context usage high, chunking work...");

      const summary = await contextManager.summarize({
        completed: task.completedWork,
        remaining: task.remainingWork
      });

      await contextManager.writeCheckpoint({
        summary: summary,
        state: task.state,
        path: '.corpus/learning/checkpoints/'
      });

      console.log("✓ Checkpoint saved, context cleared");
    }

    await task.doNextChunk();
  }
}
```

### Phase 3: Post-Execution (After)

#### 8. error-reflection (analyze)
**Already created** - enhanced with cross-skill integration

#### 9. ship-it (declare done)
**NEW SKILL**

**Trigger:** When work is "good enough"
**Purpose:** Block perfectionism loops, declare done

**Process:**
1. Check against definition of done
2. Verify minimum requirements met
3. Block "we could also add..." suggestions
4. Declare shippable status
5. Document what was NOT done (for future)

**Integration:**
```javascript
async function completeTask(task, result) {
  // Check definition of done
  const requirements = task.requirements;
  const met = requirements.filter(r => result.satisfies(r));

  if (met.length >= requirements.length * 0.8) {  // 80% threshold
    // SHIP-IT checkpoint
    await shipIt.declare({
      task: task,
      requirementsMet: met,
      requirementsDeferred: requirements.filter(r => !result.satisfies(r))
    });

    console.log("✓ SHIP IT: Requirements met, task complete");
    console.log(`  Met: ${met.length}/${requirements.length}`);

    // Block perfectionism
    console.log("\n⚠️ Blocking perfectionism:");
    console.log("  - Additional features can be added later");
    console.log("  - Current implementation is shippable");
    console.log("  - Perfect is the enemy of good");

    return result;
  }

  throw new Error(`Requirements not met: ${met.length}/${requirements.length}`);
}
```

**Example:**
```
OAuth Implementation Status:

Requirements Met (4/5):
✓ User can log in with OAuth
✓ Tokens are cached
✓ Session management works
✓ Basic error handling

Requirements Deferred (1/5):
⚠ 2FA integration (future enhancement)

SHIP IT: 80% threshold met (4/5)

⚠️ Blocking perfectionism loop:
  Claude suggested: "We could also add..."
  - Social login buttons styling
  - Remember me checkbox
  - Login analytics
  - Password recovery flow

  → These can be added later
  → Current implementation is shippable
  → Don't let perfect be the enemy of good

Status: ✓ SHIPPED
```

#### 10. pattern-update (capture)
**Part of pattern-library** - automatic update after execution

---

## Battle-Plan Orchestrators

### 1. Master Battle-Plan

**File:** `core/learning/orchestrators/battle-plan/SKILL.md`

```markdown
---
name: battle-plan
description: >
  Master orchestrator for learning-first execution. Sequences pre-execution
  (rubber-duck, pattern-library, pre-mortem, you-sure), execution (with monitoring),
  and post-execution (error-reflection, ship-it, pattern-update) phases.
---

# Battle-Plan Orchestrator

**Purpose:** Standard workflow wrapper for all complex operations
**Pattern:** Learn → Plan → Execute → Reflect → Compound

## Execution Sequence

### Phase 1: Clarification (rubber-duck)
- Force problem articulation
- Identify assumptions
- Generate clarifying questions
- Validate understanding

### Phase 2: Knowledge Check (pattern-library)
- Search for similar past tasks
- Retrieve proven patterns
- Identify known antipatterns
- Get recommendations

### Phase 3: Risk Assessment (pre-mortem)
- Imagine task has failed
- Generate failure causes
- Assess likelihood × impact
- Create preventions

### Phase 4: Confirmation (you-sure)
- Summarize plan
- Show impacts
- Highlight risks
- Get user approval

### Phase 5: Execution (monitored)
- Apply proven patterns
- Monitor for antipatterns
- PROVE-IT checkpoints
- PIVOT if needed
- DONT-BE-GREEDY context management

### Phase 6: Reflection (error-reflection)
- IF errors: Analyze root cause
- Extract patterns/antipatterns
- Update pattern library

### Phase 7: Completion (ship-it)
- Check definition of done
- Block perfectionism
- Declare shippable

### Phase 8: Learning Update (pattern-update)
- Save new patterns
- Update metrics
- Feed back to pattern library

## Configuration

```json
{
  "battlePlan": {
    "phases": {
      "rubberDuck": true,
      "patternCheck": true,
      "preMortem": "auto",  // auto, manual, off
      "confirmation": "complex",  // always, complex, never
      "monitoring": true,
      "reflection": true,
      "shipIt": true,
      "patternUpdate": true
    },
    "thresholds": {
      "complexityForPreMortem": "medium",
      "complexityForConfirmation": "high",
      "pivotAfterFailures": 3,
      "contextChunkThreshold": 0.8
    }
  }
}
```
```

### 2. Corpus Battle-Plan

**File:** `core/learning/orchestrators/corpus-battle-plan/SKILL.md`

**Specializations:**
- Pattern library focuses on corpus-operations category
- Pre-mortem uses corpus-specific risk database
- Common corpus antipatterns pre-loaded
- Prove-it checks corpus structure

**Example Flow:**
```
"Initialize new corpus" →
├─ RUBBER-DUCK
│  Q: What type of corpus? (application, documentation, framework)
│  Q: Where should it be initialized? (verify path)
│  Q: What audits needed? (code-quality, security, etc.)
│
├─ PATTERN-LIBRARY (corpus-operations)
│  Found: corpus-init-best-practices (applied 15x, 93% success)
│  Found antipattern: wrong-directory-init (seen 3x, high severity)
│
├─ PRE-MORTEM (corpus-specific risks)
│  Risk #1: Wrong directory (likelihood: 3, impact: 4, score: 12)
│    Prevention: Verify pwd, ask user to confirm
│  Risk #2: Missing dependencies (likelihood: 2, impact: 3, score: 6)
│    Prevention: Check for required tools
│
├─ YOU-SURE
│  About to initialize corpus in: /correct/path
│  Will create: .corpus/ structure
│  Proceed? [Y/n]
│
├─ EXECUTE (corpus-init)
│  Applying pattern: corpus-init-best-practices
│  ✓ Created .corpus/
│  ✓ Generated corpus-config.json
│  ✓ Initialized pattern library
│  ✓ Created audit infrastructure
│
├─ PROVE-IT
│  [✓] .corpus/ directory exists
│  [✓] corpus-config.json valid
│  [✓] All required subdirectories present
│  Confidence: 100% - VERIFIED
│
├─ SHIP-IT
│  Requirements met (5/5)
│  Status: COMPLETE
│
└─ PATTERN-UPDATE
   Updated: corpus-init-best-practices (16 applications, 93.75% success)
```

### 3. Audit Battle-Plan

**File:** `core/learning/orchestrators/audit-battle-plan/SKILL.md`

**Specializations:**
- Pattern library focuses on audit-operations and fix patterns
- Pre-mortem anticipates common audit failures
- Prove-it verifies fixes actually work
- Integration with convergence-engine

**Example Flow:**
```
"Run code quality audit" →
├─ PATTERN-LIBRARY (audit-operations)
│  Found: eslint-common-fixes (124 patterns)
│  Found: typescript-strict-mode-migration (proven pattern)
│
├─ PRE-MORTEM (audit-specific risks)
│  Risk: Config conflicts (likelihood: 3, impact: 3)
│  Risk: Breaking changes from fixes (likelihood: 4, impact: 4)
│
├─ EXECUTE (audit-orchestrator → code-quality)
│  Running: ESLint, Prettier, TypeScript
│  Issues found: 23
│
│  Applying known patterns for common issues:
│  ✓ unused-vars (pattern: prefix-with-underscore)
│  ✓ prefer-const (pattern: auto-fix-safe)
│
│  Novel issues: 3 (need manual review)
│
├─ CONVERGENCE-ENGINE (for novel issues)
│  [Full battle-plan integration here too]
│  Phase 1: Discovery
│  Phase 2: Generate fixes
│  Phase 3: Verify fixes
│  GATE: 3 clean passes
│
├─ PROVE-IT
│  [✓] All audits pass
│  [✓] No new issues introduced
│  [✓] Tests still pass
│  Confidence: 100% - VERIFIED
│
└─ PATTERN-UPDATE
   New pattern: handle-specific-eslint-rule (novel issue solved)
   Updated: eslint-common-fixes (125 patterns now)
```

### 4. Content Battle-Plan

**File:** `core/learning/orchestrators/content-battle-plan/SKILL.md`

**Specializations:**
- Pattern library for content structures (newsletter, blog, docs)
- Pre-mortem for content quality risks
- Prove-it for content validation (links, formatting)

---

## Enhanced Core Orchestrator

**File:** `core/core-orchestrator/SKILL.md`

**Updated Flow:**

```markdown
## Orchestration Flow

### 1. Analyze Request
- Detect category (corpus, audit, content, utility)
- Assess complexity (trivial, simple, medium, complex)
- Determine if battle-plan needed

### 2. Route Through Battle-Plan (if complex)

**Complexity Assessment:**
```javascript
function assessComplexity(request) {
  const indicators = {
    multiStep: request.steps?.length > 3,
    architectural: request.type === 'architecture',
    destructive: request.destructive === true,
    newTechnology: request.involves?.newTech,
    userFacing: request.userImpact === 'high',
    criticalPath: request.blocking?.length > 0
  };

  const score = Object.values(indicators).filter(Boolean).length;

  if (score >= 4) return 'complex';
  if (score >= 2) return 'medium';
  if (score >= 1) return 'simple';
  return 'trivial';
}
```

**Routing Decision:**
```javascript
async function route(request) {
  const category = detectCategory(request);
  const complexity = assessComplexity(request);

  // Trivial: Skip battle-plan
  if (complexity === 'trivial') {
    return await routeDirect(category, request);
  }

  // Simple: Optional battle-plan (pattern-check only)
  if (complexity === 'simple') {
    return await routeWithPatternCheck(category, request);
  }

  // Medium/Complex: Full battle-plan
  const battlePlan = selectBattlePlan(category);
  return await battlePlan.execute(request);
}

function selectBattlePlan(category) {
  switch(category) {
    case 'corpus': return corpusBattlePlan;
    case 'audit': return auditBattlePlan;
    case 'content': return contentBattlePlan;
    default: return masterBattlePlan;
  }
}
```

### 3. Execute Through Category Orchestrator
- Category orchestrator receives request from battle-plan
- Category orchestrator routes to specialized skill
- Specialized skill executes with battle-plan monitoring

### 4. Return Results
- Battle-plan completes post-execution phase
- Results returned to user
- Learning updates applied
```

---

## Enhanced Convergence Engine

**File:** `core/audit/convergence-engine/SKILL.md`

**Full Battle-Plan Integration:**

```markdown
## Enhanced Convergence Flow

### Pre-Convergence (Battle-Plan Phase 1-4)
Already handled by audit-battle-plan before convergence starts

### Phase 1: Discovery (with monitoring)
```javascript
async function runPhase1WithMonitoring(config) {
  const issues = [];

  for (const audit of config.audits) {
    const result = await runAudit(audit);
    issues.push(...result.issues);

    // DONT-BE-GREEDY checkpoint
    if (contextManager.shouldChunk()) {
      await saveCheckpoint({issues, audit, progress: 'phase1-partial'});
    }
  }

  // Check pattern library for known issues
  for (const issue of issues) {
    const knownPattern = await patternLibrary.findFixPattern(issue);
    if (knownPattern && knownPattern.proven) {
      issue.suggestedFix = knownPattern;
    }
  }

  return issues;
}
```

### Phase 2: Fix Planning (pattern-aware)
```javascript
async function planFixes(issues) {
  const fixes = [];

  for (const issue of issues) {
    if (issue.suggestedFix) {
      // Apply known pattern
      console.log(`Applying proven pattern: ${issue.suggestedFix.name}`);
      fixes.push(issue.suggestedFix);
    } else {
      // Generate new fix
      const fix = await generateFix(issue);
      fixes.push(fix);
    }

    // PIVOT checkpoint (if same issue keeps failing)
    if (pivot.shouldPivot(issue.attempts)) {
      const alternative = await pivot.generateAlternative(issue);
      fixes.push(alternative);
    }
  }

  return fixes;
}
```

### Phase 3: Verification (with prove-it)
```javascript
async function verifyFixes(fixes) {
  for (const fix of fixes) {
    await applyFix(fix);

    // PROVE-IT checkpoint
    const evidence = await proveIt.verify({
      claim: `Fix for ${fix.issue} successful`,
      requiredEvidence: [
        "Audit passes for this issue",
        "No new issues introduced",
        "Related tests pass"
      ]
    });

    if (!evidence.verified) {
      console.log(`⚠️ Fix not verified: ${evidence.missing.join(', ')}`);
      fix.status = 'unverified';
    }
  }

  return fixes.filter(f => f.status !== 'unverified');
}
```

### GATE (with ship-it)
```javascript
async function runGate() {
  let cleanPasses = 0;

  while (cleanPasses < 3) {
    const issues = await runAllAudits();

    if (issues.length === 0) {
      cleanPasses++;
      console.log(`✓ Clean pass ${cleanPasses}/3`);
    } else {
      cleanPasses = 0;
      console.log(`⚠️ Issues found, resetting GATE counter`);
      await handleIssues(issues);
    }

    // PIVOT if stuck
    if (attempts > 10) {
      await pivot.escalate("GATE not converging");
    }
  }

  // SHIP-IT checkpoint
  await shipIt.declare({
    task: "convergence",
    status: "complete",
    cleanPasses: 3
  });

  return {converged: true, cleanPasses: 3};
}
```

### Post-Convergence (Battle-Plan Phase 6-8)
Handled by audit-battle-plan after convergence completes
```

---

## Storage Structure (Enhanced)

```
.corpus/
├── config.json
│
├── learning/                        # Learning infrastructure
│   ├── patterns/                    # Category-organized patterns
│   │   ├── index.json
│   │   ├── corpus-operations/
│   │   │   ├── initialization.json
│   │   │   ├── conversion.json
│   │   │   └── configuration.json
│   │   ├── audit-operations/
│   │   │   ├── code-quality-fixes.json
│   │   │   ├── security-fixes.json
│   │   │   └── convergence-patterns.json
│   │   ├── content-operations/
│   │   │   └── ...
│   │   └── cross-cutting/
│   │       ├── authentication.json
│   │       ├── error-handling.json
│   │       └── testing.json
│   │
│   ├── antipatterns/                # Category-organized antipatterns
│   │   ├── index.json
│   │   ├── corpus-operations/
│   │   ├── audit-operations/
│   │   ├── content-operations/
│   │   └── cross-cutting/
│   │
│   ├── risks/                       # Pre-mortem risk databases
│   │   ├── corpus-risks.json
│   │   ├── audit-risks.json
│   │   ├── content-risks.json
│   │   └── integration-risks.json
│   │
│   ├── pre-mortems/                 # Pre-mortem reports
│   │   ├── recent/                  # Last 100
│   │   └── archive/                 # Older ones
│   │
│   ├── battle-plan-results/         # Battle-plan execution logs
│   │   └── recent/
│   │
│   ├── checkpoints/                 # Context checkpoints (dont-be-greedy)
│   │   └── recent/
│   │
│   └── metrics/
│       ├── effectiveness.json       # Learning effectiveness
│       ├── pattern-usage.json       # Pattern application stats
│       └── error-reduction.json     # Error trends
│
├── audits/                          # Existing
├── backups/                         # Existing
└── ...
```

---

## Implementation Roadmap

### Phase 1: Core Learning Skills (2-3 days)

**Completed:**
- [x] pre-mortem
- [x] error-reflection
- [x] pattern-library

**Remaining:**
- [ ] rubber-duck
- [ ] you-sure
- [ ] prove-it
- [ ] pivot
- [ ] dont-be-greedy
- [ ] ship-it
- [ ] pattern-update (enhance existing pattern-library)

### Phase 2: Battle-Plan Orchestrators (2-3 days)

- [ ] battle-plan (master)
- [ ] corpus-battle-plan
- [ ] audit-battle-plan
- [ ] content-battle-plan

### Phase 3: Core Orchestrator Integration (1 day)

- [ ] Add complexity assessment
- [ ] Add battle-plan routing logic
- [ ] Update existing orchestration flows

### Phase 4: Category Orchestrator Enhancement (2 days)

- [ ] Update corpus-orchestrator (or create if doesn't exist)
- [ ] Update audit-orchestrator
- [ ] Update content-orchestrator
- [ ] Keep utilities lightweight (optional battle-plan)

### Phase 5: Convergence Engine Integration (1 day)

- [ ] Add battle-plan monitoring hooks
- [ ] Pattern-aware fix planning
- [ ] Prove-it verification
- [ ] Pivot detection

### Phase 6: Specialized Skill Wrapping (1-2 days)

- [ ] Wrap corpus-init in battle-plan
- [ ] Wrap corpus-convert in battle-plan
- [ ] Wrap individual audits in monitoring
- [ ] Wrap content-creation in battle-plan

### Phase 7: Storage & Infrastructure (1 day)

- [ ] Create category-organized pattern directories
- [ ] Initialize risk databases
- [ ] Set up battle-plan logging
- [ ] Create checkpoint infrastructure

### Phase 8: Configuration & Testing (2 days)

- [ ] Create comprehensive config schema
- [ ] Test battle-plan flows end-to-end
- [ ] Validate pattern library queries
- [ ] Test complexity assessment

### Phase 9: Documentation (1 day)

- [ ] Update ARCHITECTURE-v4.md
- [ ] Create battle-plan usage guide
- [ ] Document pattern library structure
- [ ] Write migration guide for existing corpora

**Total Estimated Time: 12-16 days**

---

## Configuration Schema (Complete)

```json
{
  "corpus": {
    "name": "my-project",
    "type": "application"
  },

  "learning": {
    "enabled": true,
    "mode": "full",  // minimal, standard, full

    "battlePlan": {
      "enabled": true,
      "defaultVariant": "auto",  // auto-select based on category

      "phases": {
        "rubberDuck": {
          "enabled": true,
          "auto": false  // Manual invocation
        },
        "patternCheck": {
          "enabled": true,
          "auto": true,
          "categories": ["all"]  // or specific categories
        },
        "preMortem": {
          "enabled": true,
          "auto": "complexity",  // always, complexity, manual, off
          "threshold": "medium"
        },
        "confirmation": {
          "enabled": true,
          "auto": "complexity",  // always, complexity, manual, off
          "threshold": "high"
        },
        "monitoring": {
          "enabled": true,
          "proveIt": true,
          "pivot": true,
          "dontBeGreedy": true
        },
        "reflection": {
          "enabled": true,
          "auto": true
        },
        "shipIt": {
          "enabled": true,
          "threshold": 0.8  // 80% of requirements
        },
        "patternUpdate": {
          "enabled": true,
          "auto": true
        }
      },

      "thresholds": {
        "complexity": {
          "trivial": {"maxSteps": 1, "maxTime": "5min"},
          "simple": {"maxSteps": 3, "maxTime": "30min"},
          "medium": {"maxSteps": 5, "maxTime": "2hr"},
          "complex": {"minSteps": 6}
        },
        "pivot": {
          "afterFailures": 3,
          "generateAlternatives": 3
        },
        "context": {
          "chunkAt": 0.8,  // 80% of max tokens
          "checkpointInterval": 50000  // tokens
        },
        "shipIt": {
          "requirementThreshold": 0.8
        }
      }
    },

    "patternLibrary": {
      "enabled": true,
      "path": ".corpus/learning/patterns",
      "categories": [
        "corpus-operations",
        "audit-operations",
        "content-operations",
        "cross-cutting"
      ],
      "autoApply": {
        "enabled": true,
        "confidenceThreshold": 0.8,
        "minApplications": 3
      },
      "suggest": {
        "enabled": true,
        "confidenceThreshold": 0.5
      }
    },

    "antipatternDetection": {
      "enabled": true,
      "path": ".corpus/learning/antipatterns",
      "warnOnMatch": true,
      "blockOnCritical": false  // Just warn, don't block
    },

    "errorReflection": {
      "enabled": true,
      "auto": true,
      "categories": [
        "technical",
        "architectural",
        "security",
        "process",
        "assumptions",
        "external"
      ],
      "extractPatterns": true,
      "updateLibrary": true
    },

    "preMortem": {
      "enabled": true,
      "riskDatabases": [
        ".corpus/learning/risks/corpus-risks.json",
        ".corpus/learning/risks/audit-risks.json",
        ".corpus/learning/risks/content-risks.json"
      ],
      "riskThresholds": {
        "critical": 20,
        "high": 15,
        "medium": 9,
        "low": 0
      }
    },

    "storage": {
      "path": ".corpus/learning",
      "retention": {
        "preMortems": 100,
        "battlePlanResults": 50,
        "checkpoints": 20
      },
      "archive": {
        "enabled": true,
        "afterDays": 90
      }
    },

    "metrics": {
      "enabled": true,
      "track": [
        "pattern-usage",
        "error-reduction",
        "convergence-improvement",
        "time-saved"
      ]
    }
  }
}
```

---

## Benefits of Full Integration

### 1. True Institutional Memory
- Every operation builds on past learnings
- Patterns compound automatically
- Antipatterns prevented before they occur
- Cross-project knowledge sharing (optional)

### 2. Consistent Quality
- Pre-mortem prevents predictable failures
- Proven patterns applied automatically
- Error reflection ensures mistakes aren't repeated
- Ship-it prevents over-engineering

### 3. Adaptive Intelligence
- Pivot prevents infinite loops
- Prove-it prevents hallucination
- Dont-be-greedy manages context
- Pattern library gets smarter over time

### 4. User Confidence
- You-sure gives explicit control
- Rubber-duck clarifies intent
- Prove-it provides evidence
- Ship-it declares clear completion

### 5. Ecosystem Synergy
- Convergence engine learns fix patterns
- Corpus operations learn initialization patterns
- Content creation learns structure patterns
- All categories feed central pattern library

---

## Migration Strategy

### For Existing Corpora

**Step 1: Add learning infrastructure**
```bash
cd /path/to/existing/corpus
mkdir -p .corpus/learning/{patterns,antipatterns,risks,pre-mortems,battle-plan-results,checkpoints,metrics}

# Initialize empty pattern libraries
echo '[]' > .corpus/learning/patterns/corpus-operations/initialization.json
echo '[]' > .corpus/learning/antipatterns/corpus-operations/initialization.json
# ... etc for all categories
```

**Step 2: Seed with initial patterns**
```bash
# Use corpus-convert with battle-plan
"Convert this existing project to use battle-plan architecture"

# Battle-plan will:
# - Analyze existing structure
# - Generate initial patterns based on current setup
# - Identify potential antipatterns
# - Create risk database from current issues
```

**Step 3: Enable gradually**
```json
{
  "learning": {
    "enabled": true,
    "mode": "standard",  // Start with standard, not full
    "battlePlan": {
      "phases": {
        "patternCheck": {"enabled": true, "auto": true},
        "preMortem": {"enabled": true, "auto": "manual"},  // Manual at first
        "monitoring": {"enabled": true},
        "reflection": {"enabled": true, "auto": true}
      }
    }
  }
}
```

**Step 4: Validate and expand**
- Run a few operations manually with battle-plan
- Verify patterns are captured correctly
- Adjust thresholds based on actual usage
- Gradually enable more automation

### For New Corpora

**Automatic:** corpus-init with battle-plan enabled creates full structure

---

## Success Criteria (Full Integration)

### Short-term (1 month)
- [ ] 50+ patterns captured across all categories
- [ ] 20+ antipatterns identified
- [ ] 10+ pre-mortems completed successfully
- [ ] 5+ errors prevented by antipattern detection
- [ ] Battle-plan flows smoothly for all complexity levels

### Medium-term (3 months)
- [ ] 200+ patterns, 50+ antipatterns
- [ ] Pattern reuse rate >40%
- [ ] Repeat error rate down 60%
- [ ] Convergence iterations reduced 30%
- [ ] Pre-mortem blocks 15+ potential failures

### Long-term (6 months)
- [ ] 500+ patterns across all categories
- [ ] Pattern success rate >85%
- [ ] Institutional knowledge evident in all operations
- [ ] New projects benefit immediately from pattern library
- [ ] Cross-corpus pattern sharing productive

---

## Next Steps

**Ready for your approval to:**

1. Create remaining 6 learning skills (rubber-duck, you-sure, prove-it, pivot, dont-be-greedy, ship-it)
2. Create 4 battle-plan orchestrators (master + 3 category variants)
3. Enhance core-orchestrator with battle-plan routing
4. Update category orchestrators
5. Enhance convergence-engine with full monitoring
6. Create storage infrastructure
7. Test end-to-end flows
8. Document migration path

**Estimated: 12-16 days for full implementation**

**Questions:**
1. Proceed with full Option C implementation?
2. Any category-specific requirements I'm missing?
3. Should pattern library be corpus-specific or shared globally?
4. Any specific antipatterns you want seeded initially?

---

*End of Comprehensive Learning Integration Plan*
*"Every significant operation flows through battle-plan pattern"*
