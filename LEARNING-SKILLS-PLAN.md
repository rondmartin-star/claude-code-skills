# Learning Skills Integration Plan

**Based on:** "Your AI has infinite knowledge and zero habits - here's the fix" by Elliot
**Date:** 2026-02-04
**Purpose:** Incorporate habit-building and learning mechanisms into v4.0 skills ecosystem

---

## Core Concepts from Article

### 1. Knowing That vs. Knowing How (Gilbert Ryle, 1949)

**Knowing That** (Declarative Knowledge):
- Facts, information, propositions
- Claude has infinite "knowing that"
- Can explain concepts, frameworks, best practices

**Knowing How** (Procedural Knowledge):
- Skills, habits, production rules
- What Claude lacks - automatic application
- Patterns ingrained through experience

**Key Insight:** *"Claude can tell you about pre-mortems, risk assessment, matching existing codebase patterns. But it doesn't DO these things automatically. The production rules don't exist."*

### 2. Skills as Production Rules for LLMs

**What Are Production Rules?**
- IF-THEN patterns that execute automatically
- Triggers that activate specific behaviors
- Build up through repetition and experience

**For Claude:**
- Skills should encode production rules
- Not just knowledge, but automatic habits
- Composable, sequenceable behaviors

### 3. The Pattern Library Approach

**Article's Solution:**
- Write down fixes for recurring mistakes
- Build a skill library over time
- Each skill = one production rule
- Combine skills for complex workflows

**Example from Article:**
```
battle-plan skill sequences:
1. rubber-duck (clarify scope)
2. pre-mortem (assess risks)
3. eta (estimate time)
4. you-sure (confirm before execution)
```

---

## Proposed Skills to Add

### Category: Learning & Adaptation

#### 1. **pre-mortem** (Already started - needs refinement)
**Purpose:** Anticipate failures before they happen
**Trigger:** Before starting complex tasks
**Process:**
- Imagine the task has failed completely
- Work backwards to identify what caused failure
- Generate preventive measures for high-risk items
- Create go/no-go recommendation

**Integration Points:**
- Before convergence Phase 1
- Before major refactorings
- Before architectural changes
- Part of task planning workflow

#### 2. **error-reflection**
**Purpose:** Self-analyze errors and extract learnings
**Trigger:** After errors, failures, or issues found
**Process:**
- Document what went wrong
- Identify root cause (not just symptoms)
- Categorize error type
- Extract pattern/antipattern
- Update pattern library
- Generate prevention rule

**Key Innovation:** Builds institutional memory from failures

**Storage Structure:**
```
.corpus/learning/
  errors/
    {timestamp}-{error-type}.json
  patterns/
    {category}/
      {pattern-name}.md
  antipatterns/
    {category}/
      {antipattern-name}.md
```

#### 3. **pattern-library**
**Purpose:** Maintain and apply learned patterns and antipatterns
**Trigger:** Before implementing solutions, after discovering new patterns
**Process:**
- Store successful patterns (what works)
- Store antipatterns (what fails)
- Tag by: technology, domain, task type
- Retrieve relevant patterns for current task
- Apply proven solutions automatically

**Pattern Structure:**
```json
{
  "name": "oauth-rate-limit-handling",
  "type": "pattern",
  "category": "authentication",
  "context": "Third-party OAuth provider integration",
  "problem": "Rate limits causing authentication failures",
  "solution": {
    "approach": "Caching layer + exponential backoff",
    "code": "...",
    "proven": true,
    "timesApplied": 5,
    "successRate": 100
  },
  "relatedAntipatterns": ["no-caching", "tight-polling"],
  "tags": ["oauth", "rate-limiting", "authentication", "third-party"]
}
```

#### 4. **rubber-duck**
**Purpose:** Clarify scope and requirements through explanation
**Trigger:** Before starting unclear tasks
**Process:**
- Explain task in plain language
- Identify assumptions
- List unknowns
- Generate clarifying questions
- Validate understanding with user

#### 5. **you-sure** (Confirmation Gate)
**Purpose:** Pause before potentially destructive/major changes
**Trigger:** Before irreversible operations
**Process:**
- Summarize what's about to happen
- List potential impacts
- Show rollback options
- Require explicit confirmation
- Create backup/checkpoint if confirmed

**Triggers:**
- Database migrations
- Mass file deletions
- Dependency major version upgrades
- Production deployments
- Breaking API changes

#### 6. **prove-it** (Evidence Requirement)
**Purpose:** Combat hallucination with evidence requirement
**Trigger:** When making factual claims
**Process:**
- Require source for claims
- Check against codebase/docs/config
- Verify assumptions with tests
- Flag uncertain statements
- Provide confidence levels

---

## Integration with Existing Skills

### Convergence Engine Updates

**Current Flow:**
```
Discovery → Verification → Stabilization → GATE → User Validation
```

**Enhanced Flow:**
```
1. Pre-Mortem (anticipate failures)
2. Discovery (run audits)
3. Error Reflection (analyze failures)
4. Pattern Application (use proven fixes)
5. Verification
6. Stabilization
7. GATE (3 clean passes)
8. User Validation
```

### Audit System Integration

**After each audit:**
1. Run audit (find issues)
2. **Error Reflection** (understand why issues exist)
3. Generate fixes
4. **Pattern Library** (check for proven solutions)
5. Apply fixes
6. Verify
7. **Update Pattern Library** if new pattern discovered

### Task Execution Wrapper

**Before any complex task:**
```javascript
async function executeTaskWithLearning(task) {
  // 1. Check pattern library for similar tasks
  const patterns = await patternLibrary.findRelevant(task);

  // 2. Run pre-mortem
  const preMortem = await runPreMortem(task, patterns);

  if (preMortem.goNoGo.decision === 'NO GO') {
    return { blocked: true, preMortem };
  }

  // 3. Apply proven patterns
  task.applyPatterns(patterns);

  // 4. Execute with monitoring
  const result = await executeTaskMonitored(task);

  // 5. If errors, reflect and learn
  if (result.errors) {
    await errorReflection.analyze(result.errors);
    await patternLibrary.updateAntipatterns(result.errors);
  }

  // 6. If success, record pattern
  if (result.success && result.novel) {
    await patternLibrary.recordSuccess(task, result);
  }

  return result;
}
```

---

## Feedback Loop Architecture

```
┌──────────────────────────────────────────────┐
│                                              │
│  1. PRE-MORTEM                               │
│     ↓ (anticipate failures)                  │
│  2. EXECUTE TASK                             │
│     ↓ (with monitoring)                      │
│  3. DETECT ISSUES/ERRORS                     │
│     ↓                                        │
│  4. ERROR REFLECTION                         │
│     ↓ (analyze root cause)                   │
│  5. EXTRACT PATTERN/ANTIPATTERN              │
│     ↓                                        │
│  6. UPDATE PATTERN LIBRARY                   │
│     ↓                                        │
│  7. PATTERN LIBRARY                          │
│     ↓ (feeds back to pre-mortem)             │
│  [BACK TO 1] ─────────────────────────────────┘
```

**Key Points:**
- Each iteration improves future performance
- Patterns compound over time
- Antipatterns prevent repeat mistakes
- Pre-mortem becomes smarter with more data

---

## Storage & Retrieval System

### Directory Structure

```
.corpus/learning/
  ├── pre-mortems/
  │   ├── index.json
  │   └── {task-slug}-{timestamp}.json
  ├── errors/
  │   ├── index.json
  │   └── {timestamp}-{error-type}.json
  ├── patterns/
  │   ├── index.json
  │   ├── authentication/
  │   ├── database/
  │   ├── api/
  │   └── ...
  ├── antipatterns/
  │   ├── index.json
  │   ├── authentication/
  │   ├── database/
  │   └── ...
  └── metrics/
      └── effectiveness.json
```

### Corpus Config Integration

```json
{
  "learning": {
    "enabled": true,
    "preMortem": {
      "autoRun": true,
      "minComplexity": "medium",
      "requireConfirmation": true
    },
    "errorReflection": {
      "autoCapture": true,
      "categorizeErrors": true,
      "extractPatterns": true
    },
    "patternLibrary": {
      "autoApply": true,
      "minConfidence": 0.7,
      "similarityThreshold": 0.8
    },
    "storage": {
      "path": ".corpus/learning",
      "maxPreMortems": 100,
      "maxErrors": 500,
      "retentionDays": 365
    }
  }
}
```

---

## Skill Composition Patterns

### Example: Secure Authentication Implementation

```javascript
// Orchestrator skill that composes learning skills
const authImplementation = {
  name: "implement-secure-auth",
  sequence: [
    {
      skill: "rubber-duck",
      purpose: "clarify requirements"
    },
    {
      skill: "pattern-library",
      action: "findRelevant",
      query: { tags: ["authentication", "oauth", "security"] }
    },
    {
      skill: "pre-mortem",
      context: "oauth implementation",
      applyLearnings: true
    },
    {
      skill: "you-sure",
      message: "Ready to implement OAuth with preventive measures?"
    },
    {
      skill: "implement",
      applyPatterns: true
    },
    {
      skill: "prove-it",
      verify: ["oauth-flow", "token-storage", "rate-limiting"]
    },
    {
      skill: "convergence-engine",
      audits: ["security", "quality"]
    },
    {
      skill: "error-reflection",
      if: "errors found",
      updateLibrary: true
    }
  ]
};
```

---

## Success Metrics

### Pattern Library Growth
- Patterns added per week
- Antipatterns identified
- Pattern reuse rate
- Success rate of applied patterns

### Error Reduction
- Repeat error rate (should decrease)
- Time to resolution (should decrease)
- Pre-mortem accuracy (should increase)

### Productivity Impact
- Tasks blocked by pre-mortem (preventing failures)
- Tasks accelerated by pattern application
- Reduction in trial-and-error iterations

---

## Implementation Phases

### Phase 1: Core Learning Skills (Week 1)
- [x] pre-mortem (partially complete)
- [ ] error-reflection
- [ ] pattern-library
- [ ] rubber-duck

### Phase 2: Safety & Verification (Week 2)
- [ ] you-sure
- [ ] prove-it
- [ ] Integration with convergence-engine

### Phase 3: Composition & Orchestration (Week 3)
- [ ] Update existing orchestrators to use learning skills
- [ ] Create composite skills (like battle-plan)
- [ ] Add automatic triggers

### Phase 4: Refinement & Optimization (Week 4)
- [ ] Tune pattern matching algorithms
- [ ] Optimize storage and retrieval
- [ ] Add metrics and dashboards
- [ ] User feedback integration

---

## Open Questions

1. **Pattern Similarity Matching:**
   - How to determine if two tasks are similar enough to apply same pattern?
   - Use embedding similarity? Keyword matching? Both?

2. **Pattern Confidence Scoring:**
   - How to weigh: times applied, success rate, recency, context match?
   - When to suggest pattern vs. auto-apply?

3. **Error Categorization:**
   - What taxonomy of errors? (syntax, logic, architecture, security, etc.)
   - How granular?

4. **Pre-Mortem Integration:**
   - Always run automatically? Or only for certain task types?
   - How to avoid analysis paralysis?

5. **Cross-Project Learning:**
   - Should patterns be corpus-specific or shared globally?
   - How to handle privacy/sensitive info in patterns?

---

## References

- Article: "Your AI has infinite knowledge and zero habits" by Elliot
- Gilbert Ryle's "The Concept of Mind" (1949)
- Elliot's GitHub: Claude Skill Potions
- Current v4.0 Architecture (ARCHITECTURE-v4.md)

---

## Next Steps

**Immediate:**
1. Review this plan with user
2. Refine pre-mortem skill (already started)
3. Design pattern library schema
4. Create error-reflection skill

**Discussion Points:**
- Is this the right approach?
- Any missing skills?
- Priority order of implementation?
- Integration concerns?
