# Learning Skills

**Category:** Core / Learning
**Purpose:** Build procedural knowledge that compounds over time
**Inspired by:** "Your AI has infinite knowledge and zero habits" by Elliot

---

## The Problem

Claude has infinite **declarative knowledge** (knowing that) but lacks **procedural knowledge** (knowing how).

**Declarative Knowledge:** Facts, information, best practices
- Claude knows that you should do pre-mortems
- Claude knows that good engineers assess risks
- Claude knows about common antipatterns

**Procedural Knowledge:** Automatic habits, production rules
- Actually doing pre-mortems before starting
- Automatically detecting familiar failure modes
- Applying proven solutions without being asked

**Skills are production rules for LLMs** - they create the automatic behaviors that transform knowledge into expertise.

---

## The Solution: Learning Skills

Three core skills that create a feedback loop:

```
1. PRE-MORTEM (before)
   ↓ Anticipate failures, check pattern library

2. ERROR-REFLECTION (during/after)
   ↓ When errors occur, analyze and extract patterns

3. PATTERN-LIBRARY (continuous)
   ↓ Store patterns and antipatterns, feed back to pre-mortem

[LOOP BACK TO 1] - Compounds over time
```

---

## Skills in This Directory

### 1. pre-mortem

**Trigger:** Before starting complex tasks
**Purpose:** Anticipate failures before they happen

**Process:**
1. Imagine the task has failed completely
2. Generate failure causes (technical, process, assumptions, external)
3. Assess likelihood × impact for each risk
4. Create preventions, detections, mitigations
5. Generate go/no-go recommendation

**Key Feature:** Learns from past pre-mortems to get smarter

**Example:**
```
Task: Implement OAuth authentication

Pre-mortem identifies:
- Risk: OAuth provider rate limits (likelihood: 4, impact: 5)
- Prevention: Implement token caching
- Detection: Monitor OAuth request rate
- Mitigation: Fallback to local session store
```

### 2. error-reflection

**Trigger:** After errors, test failures, audit issues
**Purpose:** Build institutional memory from failures

**Process:**
1. Capture error context (what, when, where)
2. Identify root cause (5 Whys technique)
3. Categorize error type
4. Extract pattern or antipattern
5. Update pattern library
6. Generate prevention rule

**Key Feature:** "Failure paths save more time than success paths" - captures what NOT to do

**Example:**
```
Error: 429 Too Many Requests from OAuth provider

5 Whys Analysis:
1. Why failed? → Rate limits hit
2. Why hitting limits? → Request per user action
3. Why no caching? → Not implemented
4. Why not implemented? → Not in requirements
5. ROOT CAUSE: Pre-mortem didn't identify rate limits as risk

Creates antipattern: no-oauth-token-caching
Updates pre-mortem risk database
```

### 3. pattern-library

**Trigger:** Before starting tasks, after discovering patterns
**Purpose:** Store and retrieve proven solutions and known failures

**Storage:**
- **Patterns:** Successful solutions that work
- **Antipatterns:** Known failure modes to avoid

**Features:**
- Tag-based search
- Success rate tracking
- Auto-apply high-confidence patterns
- Suggest medium-confidence patterns
- Track pattern effectiveness over time

**Example:**
```javascript
// Before OAuth implementation
const patterns = await findRelevantPatterns({
  category: 'authentication',
  tags: ['oauth', 'third-party']
});

// Found: oauth-token-caching (90% success rate, used 5x)
// Found antipattern: no-token-caching (seen 2x, caused outages)

// Auto-applies proven pattern
// Warns about antipattern
```

---

## How They Work Together

### Scenario: Implementing OAuth Authentication

**1. User Request:**
```
"Implement OAuth authentication for login"
```

**2. Pre-Mortem Runs:**
```
Checking pattern library...
→ Found antipattern: no-oauth-token-caching (seen 2x, high severity)
→ Found pattern: oauth-token-caching (90% success, proven solution)

Running pre-mortem...
Top Risks:
1. OAuth rate limits (likelihood: 4, impact: 5, score: 20)
   - Prevention: Implement token caching (from pattern library)
   - Detection: Monitor OAuth request rate
   - Mitigation: Exponential backoff + fallback

2. Token expiration handling (likelihood: 3, impact: 4, score: 12)
   - Prevention: Track token TTL explicitly
   - Detection: Monitor auth failure rate
   - Mitigation: Automatic refresh before expiration

Recommendation: GO WITH CAUTION
Conditions: Implement oauth-token-caching pattern before launch
```

**3. Implementation:**
```
Applying pattern: oauth-token-caching
- Redis cache with token TTL
- Refresh 5 min before expiration
- Exponential backoff on errors

Implementation successful ✓
```

**4. If Error Occurred:**
```
Error: Token expired but still in cache

Error Reflection:
→ Root cause: TTL calculation bug (used seconds instead of milliseconds)
→ Category: Implementation error
→ Pattern update: Add test case for TTL edge cases
→ Antipattern: Saved as "ttl-unit-mismatch"

Updated pattern library:
- oauth-token-caching: Added edge case documentation
- New antipattern: ttl-unit-mismatch (with prevention rule)
```

**5. Next Time:**
```
Pre-mortem now includes:
- Rate limiting risk (from pattern history)
- TTL handling risk (from error reflection)
- Unit conversion risk (from antipattern library)

Pattern library suggests:
- oauth-token-caching with edge case tests
- Explicit unit handling in TTL calculations

Institutional memory has grown ✓
```

---

## Storage Structure

### Lightweight Design

```
.corpus/learning/
├── patterns.json              # All patterns (start simple)
├── antipatterns.json          # All antipatterns
├── pre-mortems/               # Recent pre-mortem reports
│   └── recent/
└── metrics.json               # Effectiveness tracking
```

**Why JSON?**
- Easy to read and edit
- Version control friendly
- Fast for <1000 patterns
- Can split by category later if needed

### Pattern Format

```json
{
  "name": "oauth-token-caching",
  "type": "pattern",
  "category": "authentication",
  "context": "Third-party OAuth with rate limits",
  "problem": "Frequent token requests hitting limits",
  "solution": {
    "approach": "Cache tokens with TTL",
    "implementation": "Redis with expiration",
    "benefits": ["95% fewer API calls", "No rate limit errors"],
    "tradeoffs": ["Requires Redis", "Cache invalidation complexity"]
  },
  "metrics": {
    "proven": true,
    "timesApplied": 5,
    "successRate": 1.0
  },
  "tags": ["oauth", "caching", "rate-limiting"]
}
```

### Antipattern Format

```json
{
  "name": "no-oauth-token-caching",
  "type": "antipattern",
  "category": "authentication",
  "problem": "Making OAuth request on every user action",
  "symptoms": ["429 errors", "Slow auth", "Intermittent failures"],
  "consequences": {
    "severity": "high",
    "userImpact": "Cannot log in",
    "businessImpact": "Service unavailable"
  },
  "prevention": {
    "rule": "Always cache OAuth tokens",
    "implementation": "Use oauth-token-caching pattern"
  },
  "metrics": {
    "occurrences": 2,
    "preventedBy": "pre-mortem"
  }
}
```

---

## Integration with Convergence Engine

### Before (Simple)

```
Discovery → Verification → Stabilization → GATE
```

### After (With Learning)

```
Pattern Check → Pre-Mortem →
Discovery → Error Reflection →
Verification → Stabilization →
GATE → Pattern Update
```

### Minimal Integration Points

**1. Before Phase 1:**
- Check pattern library for similar tasks
- Run pre-mortem with pattern insights

**2. During Issue Handling:**
- Run error reflection on issues
- Check for known antipatterns
- Apply proven fixes

**3. After Success:**
- Save new patterns discovered
- Update existing pattern metrics

---

## Usage Guide

### Manual Invocation

```bash
# Run pre-mortem before complex task
"Run a pre-mortem on implementing OAuth"

# Analyze an error
"Analyze this error and extract patterns"

# Check pattern library
"Do we have patterns for authentication?"
```

### Automatic Invocation

**Pre-mortem runs automatically when:**
- Task complexity is high
- Task involves multiple steps
- Task is architectural change
- Task involves new technology

**Error reflection runs automatically when:**
- Errors occur during execution
- Tests fail
- Audits find issues
- Convergence engine detects problems

**Pattern library is checked automatically when:**
- Starting any non-trivial task
- Pre-mortem is running
- Error reflection completes

---

## Configuration

Add to `corpus-config.json`:

```json
{
  "learning": {
    "enabled": true,
    "autoPatternCheck": true,
    "autoPreMortem": true,
    "autoErrorReflection": true,
    "storage": {
      "path": ".corpus/learning",
      "maxPreMortems": 100
    },
    "thresholds": {
      "autoApplyConfidence": 0.8,
      "suggestConfidence": 0.5
    }
  }
}
```

---

## Metrics Tracked

### Pattern Library Growth
- Total patterns
- Total antipatterns
- Patterns added per week
- Pattern reuse rate

### Error Reduction
- Repeat error rate (should decrease)
- Time to resolution (should decrease)
- Pre-mortem accuracy (should increase)
- Errors prevented by antipattern detection

### Productivity Impact
- Tasks accelerated by patterns
- Time saved by avoiding antipatterns
- Implementation speed increase

---

## Design Philosophy

### From the Article

**"Start with failure modes you actually hit"**
- Don't create patterns for hypothetical problems
- Build based on real errors encountered
- Iterate based on actual usage

**"Failure paths save more time than success paths"**
- Antipatterns more valuable than patterns
- Knowing what NOT to do is crucial
- Failed approaches documented thoroughly

**"Five skills regularly used is the sweet spot"**
- Don't over-engineer
- Keep it simple and useful
- Focus on compound learning

**"You're not building an AI employee"**
- Skills encode procedural knowledge
- Not about full automation
- About making expertise reusable

---

## Future Enhancements

### Phase 1 (Current)
- [x] Core 3 learning skills
- [x] Simple JSON storage
- [ ] Integration with convergence-engine
- [ ] Basic metrics tracking

### Phase 2 (After Validation)
- [ ] Add 2-3 more skills based on actual failure modes
- [ ] Enhanced pattern matching (semantic search)
- [ ] Metrics dashboard
- [ ] Cross-skill orchestration

### Phase 3 (If Needed)
- [ ] Cross-project pattern sharing
- [ ] Advanced analytics
- [ ] Pattern recommendations based on codebase analysis

---

## Quick Start

1. **Initialize Learning Directory:**
   ```bash
   mkdir -p .corpus/learning/pre-mortems/recent
   echo '[]' > .corpus/learning/patterns.json
   echo '[]' > .corpus/learning/antipatterns.json
   echo '{}' > .corpus/learning/metrics.json
   ```

2. **Run Your First Pre-Mortem:**
   ```
   "Run a pre-mortem on implementing user authentication"
   ```

3. **Capture Your First Error:**
   ```
   "Analyze this error: [error details]"
   ```

4. **Check Pattern Library:**
   ```
   "What patterns do we have for authentication?"
   ```

5. **Watch It Compound:**
   - Each pre-mortem gets smarter with more data
   - Each error captured prevents future repeats
   - Each pattern applied accelerates development

---

## Key Concepts

**Production Rules:** IF-THEN patterns that execute automatically
- IF starting OAuth implementation → THEN check for rate-limiting antipatterns
- IF 429 error detected → THEN apply token-caching pattern

**Declarative → Procedural:** Transform knowledge into habits
- Claude KNOWS about pre-mortems → Claude DOES pre-mortems automatically
- Claude KNOWS about antipatterns → Claude AVOIDS them proactively

**Compound Learning:** Knowledge builds on itself
- Session 1: Discover oauth-token-caching works
- Session 2: Pre-mortem suggests oauth-token-caching for similar task
- Session 3: Pattern applied automatically with 90% confidence
- Session N: Institutional expertise in OAuth implementations

---

## References

**Article:** "Your AI has infinite knowledge and zero habits - here's the fix" by Elliot
**Date:** January 28, 2026
**Source:** Medium

**Key Citations:**
- Gilbert Ryle's "The Concept of Mind" (1949)
- Knowing that vs. knowing how
- Production rules for LLMs
- Composable procedural knowledge
- Failed attempts documentation
- Self-improving CLAUDE.md pattern

**Elliot's GitHub:** Claude Skill Potions

---

*"Every correction becomes a permanent lesson. Your procedural knowledge layer gets smarter through use."* - Elliot

---

*Part of v4.0.0 Universal Skills Ecosystem*
*Transforms infinite knowledge into reliable expertise*
