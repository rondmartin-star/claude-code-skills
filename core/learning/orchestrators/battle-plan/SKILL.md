---
name: battle-plan
description: >
  Master orchestrator for learning-first execution. Sequences all learning skills
  (clarify-requirements, pattern-library, pre-mortem, confirm-operation, execute with
  monitoring, error-reflection, declare-complete, pattern-update) to create complete
  feedback loop. Use when: complex tasks, multi-step operations, high-risk changes.
---

# Battle-Plan Orchestrator

**Purpose:** Master workflow for all complex operations (learning-first approach)
**Type:** Learning Orchestrator (Meta-Skill)
**Attribution:** Based on "Claude Skill Potions" by Elliot

---

## Attribution

**Article:** "Your AI has infinite knowledge and zero habits - here's the fix"
**Author:** Elliot
**Published:** January 28, 2026
**Source:** Medium

**Quote:** *"The battle-plan skill in my collection doesn't contain a massive monolithic procedure. It sequences other skills: rubber-duck (clarify scope), pre-mortem (assess risks), eta (estimate time), you-sure (confirm before execution). Each component skill does one thing. The orchestrator sequences them."*

**Philosophy:** "This is composable procedural knowledge — the same pattern that makes human expertise transferable and refinable."

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Run battle-plan"
- "Use learning workflow"
- Complex task detected automatically

**Context Indicators:**
- Task complexity >= medium
- Multi-step operation
- High-risk change
- Architectural decision
- User-facing feature

---

## Core Concept

**Traditional Workflow:**
```
User Request → Execute → Fix Errors → Done
```

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

**Key Principles:**
1. **Learn First:** Check pattern library before executing
2. **Think First:** Run pre-mortem before implementing
3. **Monitor During:** Use verify-evidence, detect-infinite-loop, manage-context
4. **Reflect After:** Run error-reflection if issues occur
5. **Compound Learning:** Update pattern library for future tasks

---

## Battle-Plan Phases

### Phase 1: Clarification

**Skill:** clarify-requirements

**Purpose:** Understand what we're actually building

**Process:**
1. Force plain language explanation
2. Identify hidden assumptions
3. List known vs. unknown
4. Generate clarifying questions
5. Get user answers

**Output:** Clear scope, validated assumptions, answered questions

**Example:**
```
User: "Add OAuth login"

CLARIFY-REQUIREMENTS:
→ Plain language: "Let users log in with Google/GitHub instead of password"
→ Assumptions identified:
  - Which provider? (UNKNOWN - need user answer)
  - Keep password auth? (UNKNOWN - need user answer)
→ Questions for user:
  1. Which OAuth provider(s)?
  2. Migrate existing users how?
  3. Keep password auth?

[User answers questions]

→ Scope clarified ✓
```

### Phase 2: Knowledge Check

**Skill:** pattern-library

**Purpose:** Learn from similar past tasks

**Process:**
1. Query pattern library
2. Find similar tasks
3. Retrieve proven patterns
4. Identify known antipatterns
5. Get recommendations

**Output:** Relevant patterns, antipatterns, recommendations

**Example:**
```
PATTERN-LIBRARY CHECK:

Found Patterns:
✓ oauth-token-caching (proven solution, 90% success rate)
✓ session-integration-pattern (used 5 times successfully)

Found Antipatterns:
⚠️ no-token-caching (seen 2 times, caused outages)
⚠️ direct-oauth-calls (rate limiting issues)

Recommendations:
1. Use oauth-token-caching pattern
2. Avoid direct OAuth API calls
3. Implement exponential backoff
```

### Phase 3: Risk Assessment

**Skill:** pre-mortem

**Purpose:** Anticipate failures before they happen

**Process:**
1. Imagine task has failed
2. Generate failure causes
3. Assess likelihood × impact
4. Create preventions
5. Generate go/no-go recommendation

**Output:** Risk assessment, preventions, go/no-go

**Example:**
```
PRE-MORTEM:

Top Risks:
1. OAuth rate limits (likelihood: 4, impact: 5, score: 20)
   Prevention: Implement token caching

2. Session compatibility (likelihood: 3, impact: 4, score: 12)
   Prevention: Test session integration early

Recommendation: GO WITH CAUTION
Conditions: Implement oauth-token-caching before launch
```

### Phase 4: Confirmation

**Skill:** confirm-operation

**Purpose:** Get user approval before proceeding

**Process:**
1. Summarize what will happen
2. List potential impacts
3. Show rollback options
4. Highlight risks
5. Require explicit confirmation

**Output:** User confirmation or cancellation

**Example:**
```
CONFIRM-OPERATION:

About to implement:
- OAuth authentication (Google + GitHub)
- Token caching with Redis
- Session integration

Impacts:
- 4 new files created
- Database migration required
- Session system modified

Risks (from pre-mortem):
⚠️ Rate limits (mitigated by caching)
⚠️ Session compatibility (will test early)

Rollback: Available (database migration reversible)

Proceed? [Y/n]
```

### Phase 5: Execution (with Monitoring)

**Skills:** verify-evidence, detect-infinite-loop, manage-context

**Purpose:** Execute with continuous monitoring and safety

**Sub-phases:**
```
5a. Apply proven patterns (from pattern library)
5b. Execute implementation
5c. VERIFY-EVIDENCE checkpoints
5d. DETECT-INFINITE-LOOP if stuck
5e. MANAGE-CONTEXT if usage high
```

**Example:**
```
EXECUTE:

Applying pattern: oauth-token-caching
├─ Implement OAuth config ✓
│  [VERIFY-EVIDENCE: Config file exists ✓]
│
├─ Implement OAuth routes ✓
│  [VERIFY-EVIDENCE: Routes defined ✓]
│
├─ Implement token caching
│  Attempt 1: npm install redis → Failed (network timeout)
│  Attempt 2: npm install redis → Failed (network timeout)
│  Attempt 3: npm install redis → Failed (network timeout)
│  [DETECT-INFINITE-LOOP: Pivoting to yarn ✓]
│  Attempt 4: yarn add redis → Success ✓
│
├─ Integrate with sessions ✓
│  [VERIFY-EVIDENCE: Tests pass ✓]
│
└─ [MANAGE-CONTEXT: 75% usage, continue]
```

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

### Phase 6: Reflection

**Skill:** error-reflection (if errors occurred)

**Purpose:** Analyze failures, extract learnings

**Process:**
1. Identify errors that occurred
2. Run 5 Whys analysis
3. Categorize error types
4. Extract patterns/antipatterns
5. Update pattern library

**Output:** Root causes, new patterns/antipatterns

**Example:**
```
ERROR-REFLECTION:

Error: npm install kept timing out

5 Whys Analysis:
1. Why timeout? → Network issues
2. Why network issues? → Corporate proxy
3. Why proxy blocking? → npm registry on blocklist
4. Why not detected earlier? → Pre-mortem didn't check network
5. ROOT CAUSE: Pre-mortem risk database missing "network connectivity" risks

New Antipattern Created:
- Name: assume-network-works
- Prevention: Always check network/proxy before package install
- Added to pattern library ✓
```

### Phase 7: Completion

**Skill:** declare-complete

**Purpose:** Declare done, block perfectionism

**Process:**
1. Check definition of done
2. Verify requirements met
3. Calculate shippability
4. Block perfectionism
5. Declare SHIPPABLE
6. Document deferred work

**Output:** Ship decision, deferred features

**Example:**
```
DECLARE-COMPLETE:

Requirements Met:
- Core: 5/5 (100%) ✓
- Important: 3/4 (75%) ✓
- Nice-to-have: 1/6 (17%)

Status: ✓ SHIPPABLE

⚠️ BLOCKING PERFECTIONISM:
- "We could also add 2FA..." → Deferred to v2.0
- "What about analytics?" → Deferred to v2.0

🚀 SHIP IT
```

### Phase 8: Pattern Update

**Skill:** pattern-library (update mode)

**Purpose:** Save learnings for future tasks

**Process:**
1. If successful and novel → save as pattern
2. If errors occurred → save as antipattern
3. Update metrics for applied patterns
4. Feed back to pattern library

**Output:** Updated pattern library

**Example:**
```
PATTERN-UPDATE:

New Pattern Saved:
- Name: oauth-with-proxy-detection
- Category: authentication
- Solution: Check network before OAuth setup
- Success rate: 100% (1 application)

Updated Pattern:
- oauth-token-caching (6 applications now, 91.7% success)

Updated Antipattern:
- assume-network-works (3 occurrences now)

✓ Pattern library updated
```

---

## Battle-Plan Execution Flow

```javascript
async function executeBattlePlan(userRequest, config = {}) {
  const result = {
    phases: {},
    success: false,
    learnings: []
  };

  try {
    // Phase 1: Clarification
    console.log("═══ PHASE 1: CLARIFICATION ═══");
    result.phases.clarification = await clarifyRequirements.analyze(userRequest);

    if (result.phases.clarification.validation.readyToProceed === false) {
      // Need more info from user
      await askUserQuestions(result.phases.clarification.questions.critical);
      // Re-analyze with answers
      result.phases.clarification = await clarifyRequirements.analyze(userRequest);
    }

    // Phase 2: Knowledge Check
    console.log("\n═══ PHASE 2: KNOWLEDGE CHECK ═══");
    result.phases.patternCheck = await patternLibrary.findRelevant({
      description: result.phases.clarification.explanation.plainLanguage,
      category: detectCategory(userRequest)
    });

    if (result.phases.patternCheck.antipatterns.length > 0) {
      console.log("⚠️ Known antipatterns detected");
      result.phases.patternCheck.antipatterns.forEach(ap => {
        console.log(`  - ${ap.name}: ${ap.problem}`);
      });
    }

    // Phase 3: Risk Assessment
    console.log("\n═══ PHASE 3: RISK ASSESSMENT ═══");
    result.phases.preMortem = await preMortem.run({
      task: result.phases.clarification,
      knownAntipatterns: result.phases.patternCheck.antipatterns,
      provenPatterns: result.phases.patternCheck.patterns
    });

    if (result.phases.preMortem.goNoGo.decision === "NO GO") {
      console.log("⚠️ Pre-mortem recommends not proceeding");
      console.log(result.phases.preMortem.goNoGo.reasoning);

      if (!config.forceProced) {
        throw new Error("Pre-mortem blocked execution");
      }
    }

    // Phase 4: Confirmation
    console.log("\n═══ PHASE 4: CONFIRMATION ═══");
    const confirmation = await confirmOperation.confirm({
      operation: userRequest,
      summary: result.phases.clarification.explanation,
      impacts: result.phases.preMortem.topRisks,
      patterns: result.phases.patternCheck.patterns
    });

    if (!confirmation.confirmed) {
      throw new Error("User cancelled operation");
    }

    // Phase 5: Execution (with monitoring)
    console.log("\n═══ PHASE 5: EXECUTION ═══");

    // Apply proven patterns
    if (result.phases.patternCheck.patterns.length > 0) {
      console.log("Applying proven patterns:");
      result.phases.patternCheck.patterns.forEach(p => {
        console.log(`  - ${p.name} (${p.metrics.successRate * 100}% success)`);
      });
    }

    // Execute with monitoring
    result.phases.execution = await executeWithMonitoring({
      task: userRequest,
      clarification: result.phases.clarification,
      patterns: result.phases.patternCheck.patterns,
      preventions: result.phases.preMortem.preventiveMeasures,
      monitors: [verifyEvidence, detectInfiniteLoop, manageContext]
    });

    // Phase 6: Reflection (if errors)
    if (result.phases.execution.errors.length > 0) {
      console.log("\n═══ PHASE 6: ERROR REFLECTION ═══");
      result.phases.reflection = await errorReflection.analyze(
        result.phases.execution.errors
      );

      result.learnings.push(...result.phases.reflection.patterns);
      result.learnings.push(...result.phases.reflection.antipatterns);
    }

    // Phase 7: Completion
    console.log("\n═══ PHASE 7: DECLARE COMPLETE ═══");
    result.phases.completion = await declareComplete.check({
      task: userRequest,
      implementation: result.phases.execution.result,
      criteria: result.phases.clarification.validation.requirements
    });

    if (result.phases.completion.isShippable) {
      await declareComplete.ship(result.phases.completion);
    } else {
      console.log("⚠️ Not yet shippable:");
      console.log(result.phases.completion.blockers);
    }

    // Phase 8: Pattern Update
    console.log("\n═══ PHASE 8: PATTERN UPDATE ═══");
    result.phases.patternUpdate = await patternLibrary.update({
      task: userRequest,
      result: result.phases.execution.result,
      learnings: result.learnings,
      success: result.phases.completion.isShippable
    });

    result.success = result.phases.completion.isShippable;

  } catch (error) {
    console.error("Battle-plan execution failed:", error);
    result.error = error;
    result.success = false;

    // Still try to capture learnings
    if (error.errors) {
      const reflection = await errorReflection.analyze(error.errors);
      result.learnings.push(...reflection.patterns);
      result.learnings.push(...reflection.antipatterns);
      await patternLibrary.update({task: userRequest, learnings: result.learnings});
    }
  }

  return result;
}
```

---

## Integration with Core Orchestrator

**Core orchestrator routing:**
```javascript
async function routeRequest(userRequest) {
  const complexity = assessComplexity(userRequest);
  const category = detectCategory(userRequest);

  // Trivial: Skip battle-plan
  if (complexity === 'trivial') {
    return await routeDirect(category, userRequest);
  }

  // Simple: Pattern-check only
  if (complexity === 'simple') {
    return await routeWithPatternCheck(category, userRequest);
  }

  // Medium/Complex: Full battle-plan
  const variant = selectBattlePlanVariant(category);
  return await variant.execute(userRequest);
}
```

---

## Configuration

```json
{
  "battlePlan": {
    "enabled": true,
    "phases": {
      "clarification": {"enabled": true, "auto": false},
      "patternCheck": {"enabled": true, "auto": true},
      "preMortem": {"enabled": true, "auto": "complexity"},
      "confirmation": {"enabled": true, "auto": "complexity"},
      "monitoring": {"enabled": true, "auto": true},
      "reflection": {"enabled": true, "auto": true},
      "completion": {"enabled": true, "auto": true},
      "patternUpdate": {"enabled": true, "auto": true}
    },
    "thresholds": {
      "complexityForPreMortem": "medium",
      "complexityForConfirmation": "high",
      "autoApplyPatterns": 0.8
    },
    "monitoring": {
      "verifyEvidence": true,
      "detectInfiniteLoop": true,
      "manageContext": true
    }
  }
}
```

---

## Benefits

**Before Battle-Plan:**
- Jump straight to implementation
- Repeat same mistakes
- No risk assessment
- Quality degrades over time

**With Battle-Plan:**
- Understand requirements first
- Learn from past tasks
- Anticipate failures
- Monitor execution
- Reflect on errors
- Compound learning

**Compound Learning Effect:**
```
Task 1: Discover oauth-token-caching works
Task 2: Pre-mortem suggests it for similar task
Task 3: Auto-applies with 90% confidence
Task N: Institutional expertise in OAuth
```

---

## Quick Reference

**Run battle-plan manually:**
```javascript
const result = await battlePlan.execute({
  description: "Implement OAuth authentication",
  complexity: "high",
  category: "authentication"
});
```

**Check if battle-plan should run:**
```javascript
if (battlePlan.shouldRun(task)) {
  return await battlePlan.execute(task);
} else {
  return await directExecution(task);
}
```

---

*End of Battle-Plan Orchestrator*
*Part of v4.0.0 Universal Skills Ecosystem*
*Category: Learning Orchestrators*
*Attribution: Based on Claude Skill Potions by Elliot*
*"Composable procedural knowledge that compounds over time"*
