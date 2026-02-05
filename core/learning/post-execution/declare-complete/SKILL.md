---
name: declare-complete
description: >
  Declares work "good enough" and blocks perfectionism loops. Checks definition of done,
  verifies minimum requirements met, prevents endless refinement suggestions, and clearly
  declares shippable status. Use when: work meets requirements, perfectionism starting, ready to ship.
---

# Declare Complete

**Purpose:** Block perfectionism loops, declare "good enough" and ship
**Type:** Learning Skill (Post-Execution / Completion Gate)
**Attribution:** Based on "Claude Skill Potions" by Elliot (ship-it skill)

---

## Attribution

**Article:** "Your AI has infinite knowledge and zero habits - here's the fix"
**Author:** Elliot
**Published:** January 28, 2026
**Source:** Medium

**Quote:** *"No definition of done. Perfectionism loops. 'We could also add...' 'It would be better if...' No clear declaration that something is shippable. Just endless refinement until the heat death of the universe."*

**Solution:** *"ship-it - Declares 'good enough,' blocks perfectionism"*

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Is this done?"
- "Ship it"
- "Good enough"
- When perfectionism starts

**Context Indicators:**
- Core requirements met
- Suggesting endless improvements
- "We could also add..." pattern emerging
- Task dragging on unnecessarily
- Diminishing returns on refinements

---

## Core Concept

**The Problem (from article):**
> "No definition of done. Perfectionism loops. 'We could also add...' 'It would be better if...' No clear declaration that something is shippable. Just endless refinement until the heat death of the universe."

**The Solution:**
1. Define "done" criteria upfront
2. Check against definition of done
3. Verify minimum requirements met
4. Block "we could also..." suggestions
5. Clearly declare SHIPPABLE status
6. Document what was NOT done (for future)

**Philosophy:**
- **Perfect is the enemy of good**
- **Ship fast, iterate based on feedback**
- **80/20 rule: 80% of value in 20% of work**
- **Done is better than perfect**

---

## Completion Process

### 1. Define "Done" Criteria

```javascript
function defineCompletionCriteria(task) {
  return {
    core: [
      // MUST have - blocking requirements
    ],
    important: [
      // SHOULD have - high value
    ],
    nice: [
      // COULD have - low priority
    ],
    threshold: {
      mustHave: 1.0,      // 100% of core requirements
      shouldHave: 0.8,    // 80% of important requirements
      couldHave: 0.0      // 0% of nice-to-haves required
    }
  };
}
```

**Example - OAuth Implementation:**
```javascript
{
  core: [
    "Users can log in with OAuth",
    "Tokens are cached to avoid rate limits",
    "Session management works",
    "Basic error handling exists",
    "No security vulnerabilities"
  ],
  important: [
    "Tests cover OAuth flow",
    "Handles token expiration",
    "Logs authentication events",
    "User-friendly error messages"
  ],
  nice: [
    "Social login button styling",
    "Remember me checkbox",
    "Login analytics dashboard",
    "Password recovery flow",
    "2FA integration",
    "Multiple OAuth providers"
  ],
  threshold: {
    mustHave: 1.0,    // All 5 core requirements
    shouldHave: 0.75, // 3 out of 4 important
    couldHave: 0.0    // None required
  }
}
```

### 2. Check Requirements Status

```javascript
async function checkRequirements(task, implementation) {
  const status = {
    core: [],
    important: [],
    nice: [],
    met: {core: 0, important: 0, nice: 0},
    total: {core: 0, important: 0, nice: 0}
  };

  // Check core requirements
  for (const req of task.criteria.core) {
    const met = await verifyRequirement(req, implementation);
    status.core.push({requirement: req, met});
    status.total.core++;
    if (met) status.met.core++;
  }

  // Check important requirements
  for (const req of task.criteria.important) {
    const met = await verifyRequirement(req, implementation);
    status.important.push({requirement: req, met});
    status.total.important++;
    if (met) status.met.important++;
  }

  // Check nice-to-haves (optional)
  for (const req of task.criteria.nice) {
    const met = await verifyRequirement(req, implementation);
    status.nice.push({requirement: req, met});
    status.total.nice++;
    if (met) status.met.nice++;
  }

  return status;
}
```

**Example Check:**
```
Requirement Status:

CORE (MUST HAVE) - 5/5 met (100%) ✓
  ✓ Users can log in with OAuth
  ✓ Tokens are cached to avoid rate limits
  ✓ Session management works
  ✓ Basic error handling exists
  ✓ No security vulnerabilities

IMPORTANT (SHOULD HAVE) - 3/4 met (75%) ✓
  ✓ Tests cover OAuth flow
  ✓ Handles token expiration
  ✓ Logs authentication events
  ✗ User-friendly error messages (generic errors shown)

NICE (COULD HAVE) - 1/6 met (17%)
  ✗ Social login button styling
  ✗ Remember me checkbox
  ✗ Login analytics dashboard
  ✗ Password recovery flow
  ✗ 2FA integration
  ✓ Multiple OAuth providers (Google + GitHub)

OVERALL: 9/15 total requirements (60%)
SHIPPABLE: ✓ YES (meets thresholds)
```

### 3. Calculate Shippability

```javascript
function calculateShippability(status, thresholds) {
  const corePercentage = status.met.core / status.total.core;
  const importantPercentage = status.met.important / status.total.important;
  const nicePercentage = status.met.nice / status.total.nice;

  const meetsCore = corePercentage >= thresholds.mustHave;
  const meetsImportant = importantPercentage >= thresholds.shouldHave;
  const meetsNice = nicePercentage >= thresholds.couldHave;

  const isShippable = meetsCore && meetsImportant && meetsNice;

  return {
    isShippable,
    percentages: {core: corePercentage, important: importantPercentage, nice: nicePercentage},
    thresholdsMet: {core: meetsCore, important: meetsImportant, nice: meetsNice},
    confidence: calculateConfidence(corePercentage, importantPercentage),
    blockers: identifyBlockers(status, thresholds)
  };
}

function calculateConfidence(corePercentage, importantPercentage) {
  // Weighted confidence (core requirements weighted more)
  const confidence = (corePercentage * 0.7) + (importantPercentage * 0.3);

  if (confidence >= 0.95) return 'VERY HIGH';
  if (confidence >= 0.85) return 'HIGH';
  if (confidence >= 0.75) return 'MEDIUM';
  return 'LOW';
}
```

**Example Calculation:**
```
Shippability Analysis:

Core Requirements: 100% (5/5) ✓ MEETS THRESHOLD (100% required)
Important Requirements: 75% (3/4) ✓ MEETS THRESHOLD (75% required)
Nice-to-Haves: 17% (1/6) ✓ MEETS THRESHOLD (0% required)

Overall Confidence: HIGH (87.5%)
  = (100% × 0.7) + (75% × 0.3)
  = 70% + 22.5%
  = 92.5%

Status: ✓ SHIPPABLE
Blockers: None
```

### 4. Block Perfectionism

```javascript
async function blockPerfectionism(shippability) {
  if (!shippability.isShippable) {
    // Not shippable yet - don't block
    return {blocked: false, reason: "Requirements not met"};
  }

  // Shippable - block further "improvements"
  console.log("\n" + "=".repeat(60));
  console.log("⚠️ PERFECTIONISM BLOCKER ACTIVATED");
  console.log("=".repeat(60));

  console.log("\nThis implementation is SHIPPABLE.");
  console.log(`Confidence: ${shippability.confidence}`);
  console.log(`Core requirements: ${shippability.percentages.core * 100}%`);
  console.log(`Important requirements: ${shippability.percentages.important * 100}%`);

  console.log("\n🚫 BLOCKING additional 'improvements':");
  console.log("  - 'We could also add...'");
  console.log("  - 'It would be better if...'");
  console.log("  - 'What about also...'");
  console.log("  - 'Should we...'");

  console.log("\n✓ SHIP IT AS IS");
  console.log("  - Meets all core requirements");
  console.log("  - Meets important requirements threshold");
  console.log("  - Additional features can be added LATER");
  console.log("  - Get user feedback before over-engineering");

  console.log("\n💡 REMEMBER:");
  console.log("  - Perfect is the enemy of good");
  console.log("  - Done is better than perfect");
  console.log("  - Ship fast, iterate based on feedback");
  console.log("  - 80% of value comes from 20% of work");

  console.log("\n" + "=".repeat(60) + "\n");

  return {
    blocked: true,
    reason: "Implementation is shippable - perfectionism not allowed"
  };
}
```

### 5. Declare Shippable Status

```javascript
async function declareShippable(task, status, shippability) {
  const declaration = {
    task: task.description,
    status: 'SHIPPABLE',
    timestamp: new Date().toISOString(),
    confidence: shippability.confidence,
    summary: {
      requirementsMet: status.met.core + status.met.important + status.met.nice,
      requirementsTotal: status.total.core + status.total.important + status.total.nice,
      coreComplete: `${status.met.core}/${status.total.core}`,
      importantComplete: `${status.met.important}/${status.total.important}`,
      niceComplete: `${status.met.nice}/${status.total.nice}`
    },
    deferred: status.core.filter(r => !r.met)
                    .concat(status.important.filter(r => !r.met))
                    .concat(status.nice.filter(r => !r.met))
                    .map(r => r.requirement),
    nextRelease: suggestNextRelease(status)
  };

  // Log declaration
  await logShipDeclaration(declaration);

  // Display to user
  console.log("\n" + "╔" + "═".repeat(58) + "╗");
  console.log("║" + " ".repeat(20) + "🚀 SHIP IT 🚀" + " ".repeat(26) + "║");
  console.log("╚" + "═".repeat(58) + "╝\n");

  console.log(`Task: ${task.description}`);
  console.log(`Status: ${declaration.status}`);
  console.log(`Confidence: ${declaration.confidence}\n`);

  console.log("Requirements Met:");
  console.log(`  Core: ${declaration.summary.coreComplete} (100%)`);
  console.log(`  Important: ${declaration.summary.importantComplete} (${Math.round(status.met.important / status.total.important * 100)}%)`);
  console.log(`  Nice-to-have: ${declaration.summary.niceComplete} (${Math.round(status.met.nice / status.total.nice * 100)}%)\n`);

  if (declaration.deferred.length > 0) {
    console.log("Deferred to Future Releases:");
    declaration.deferred.forEach((req, i) => {
      console.log(`  ${i + 1}. ${req}`);
    });
    console.log();
  }

  console.log("✓ This implementation is production-ready");
  console.log("✓ Ship it and gather user feedback");
  console.log("✓ Iterate based on actual usage\n");

  return declaration;
}
```

**Example Declaration:**
```
╔══════════════════════════════════════════════════════════╗
║                    🚀 SHIP IT 🚀                          ║
╚══════════════════════════════════════════════════════════╝

Task: Implement OAuth authentication
Status: SHIPPABLE
Confidence: HIGH

Requirements Met:
  Core: 5/5 (100%)
  Important: 3/4 (75%)
  Nice-to-have: 1/6 (17%)

Deferred to Future Releases:
  1. User-friendly error messages
  2. Social login button styling
  3. Remember me checkbox
  4. Login analytics dashboard
  5. Password recovery flow
  6. 2FA integration

✓ This implementation is production-ready
✓ Ship it and gather user feedback
✓ Iterate based on actual usage
```

### 6. Document What's NOT Done

```javascript
async function documentDeferred(declaration) {
  const futureWork = {
    version: 'v1.0',
    released: new Date().toISOString(),
    deferred: declaration.deferred.map(req => ({
      feature: req,
      category: categorizeRequirement(req),
      priority: assessPriority(req),
      effort: estimateEffort(req),
      reason: "Deferred post-MVP for user feedback"
    })),
    suggestedRoadmap: generateRoadmap(declaration.deferred)
  };

  await writeFile('.corpus/learning/future-work.json', JSON.stringify(futureWork, null, 2));

  console.log("✓ Future work documented in .corpus/learning/future-work.json");

  return futureWork;
}
```

---

## Integration with Battle-Plan

**Position:** Post-Execution (Phase 7) - After work complete

**Flow:**
```
Battle-Plan:
├─ CLARIFY-REQUIREMENTS ✓
├─ PATTERN-LIBRARY ✓
├─ PRE-MORTEM ✓
├─ CONFIRM-OPERATION ✓
├─ EXECUTE ✓
├─ VERIFY-EVIDENCE ✓
├─ ERROR-REFLECTION (if errors) ✓
│
├─ DECLARE-COMPLETE (you are here)
│  ├─ Check definition of done
│  ├─ Verify requirements met
│  ├─ Calculate shippability
│  ├─ Block perfectionism
│  ├─ Declare SHIPPABLE
│  └─ Document deferred work
│
└─ PATTERN-UPDATE ✓
```

**Triggers:**
- All core requirements met
- Important requirements threshold met
- No critical blockers
- Quality gates passed (tests, audits, etc.)

---

## Perfectionism Detection Patterns

```javascript
const perfectionismPatterns = [
  /we could also add/i,
  /it would be better if/i,
  /what about also/i,
  /should we also/i,
  /might want to consider/i,
  /while we're at it/i,
  /as long as we're/i,
  /one more thing/i
];

function detectPerfectionism(statement) {
  return perfectionismPatterns.some(pattern => pattern.test(statement));
}
```

**When detected:**
```
Claude: "We could also add a login analytics dashboard..."

[DECLARE-COMPLETE intercepted]

⚠️ PERFECTIONISM DETECTED

The statement "We could also add..." indicates perfectionism.

Current status:
- Core requirements: 100% ✓
- Important requirements: 75% ✓
- Implementation is SHIPPABLE

🚫 Additional features can be added in v2.0
✓ Ship current implementation first
✓ Get user feedback before adding analytics

Blocked: "login analytics dashboard" (nice-to-have)
Reason: Not required for MVP, defer to future release
```

---

## Configuration

```json
{
  "declareComplete": {
    "enabled": true,
    "strictMode": true,  // Enforce thresholds strictly
    "thresholds": {
      "core": 1.0,       // 100% of core requirements
      "important": 0.75, // 75% of important requirements
      "nice": 0.0        // 0% of nice-to-haves required
    },
    "perfectionism": {
      "blockSuggestions": true,
      "allowUserOverride": true,
      "showPhilosophy": true  // Show "perfect is enemy of good"
    },
    "documentation": {
      "recordDeclaration": true,
      "documentDeferred": true,
      "createRoadmap": true
    }
  }
}
```

---

## Benefits

**Prevents:**
- Endless refinement loops
- Feature creep
- Analysis paralysis
- Over-engineering

**Provides:**
- Clear completion criteria
- Objective shippability assessment
- Documented future work
- Confidence in shipping

**Enables:**
- Faster shipping
- Feedback-driven development
- Iterative improvement
- Focus on core value

---

## Philosophy Reminders

**Perfect is the enemy of good** (Voltaire)
- Striving for perfection often prevents shipping good work

**Done is better than perfect**
- Shipping imperfect work allows learning and iteration

**80/20 Rule** (Pareto Principle)
- 80% of value comes from 20% of work
- Don't spend 80% of time on 20% of value

**Ship fast, iterate based on feedback**
- Real user feedback > hypothetical improvements
- Users will tell you what actually matters

**MVP Philosophy**
- Minimum Viable Product first
- Add features based on usage, not speculation

---

## Quick Reference

**Check if shippable:**
```javascript
const status = await checkRequirements(task, implementation);
const shippability = calculateShippability(status, task.criteria.threshold);

if (shippability.isShippable) {
  await blockPerfectionism(shippability);
  await declareShippable(task, status, shippability);
}
```

**Manually declare complete:**
```javascript
await declareComplete.ship({
  task: "OAuth implementation",
  requirementsMet: [list of met requirements],
  deferredFeatures: [list of deferred features]
});
```

---

*End of Declare-Complete*
*Part of v4.0.0 Universal Skills Ecosystem*
*Category: Learning / Post-Execution (Completion Gate)*
*Attribution: Based on "ship-it" skill from Claude Skill Potions by Elliot*
*"Perfect is the enemy of good - ship it!"*
