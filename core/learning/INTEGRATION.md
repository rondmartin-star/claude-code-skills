# Learning Skills Integration Guide

**Purpose:** Lightweight integration of learning skills into existing v4.0 ecosystem
**Philosophy:** "Start with failure modes you actually hit" - Elliot

---

## Core Learning Loop

```
┌─────────────────────────────────────────┐
│  1. PRE-MORTEM (before task)            │
│     → Check pattern library             │
│     → Identify known antipatterns       │
│     → Apply proven solutions            │
│     → Anticipate new risks              │
├─────────────────────────────────────────┤
│  2. EXECUTE TASK                        │
│     → With pattern-informed approach    │
│     → Monitoring for known antipatterns │
├─────────────────────────────────────────┤
│  3. ERROR REFLECTION (if errors)        │
│     → Analyze root cause                │
│     → Extract pattern/antipattern       │
│     → Update pattern library            │
├─────────────────────────────────────────┤
│  4. PATTERN LIBRARY UPDATED             │
│     → Feeds back to pre-mortem          │
│     → Compounds learning over time      │
└─────────────────────────────────────────┘
```

---

## Convergence Engine Integration

### Enhanced Workflow

**Before:**
```
Discovery → Verification → Stabilization → GATE → User Validation
```

**After (with Learning):**
```
Pattern Check → Pre-Mortem → Discovery → Error Reflection →
Verification → Stabilization → GATE → Pattern Update → User Validation
```

### Minimal Integration Points

**1. Before Phase 1 - Check Patterns**
```javascript
// In convergence-engine/SKILL.md
async function runPhase1WithLearning(config) {
  // Check pattern library for similar tasks
  const patterns = await checkPatternLibrary({
    category: 'code-quality',
    tags: config.audits
  });

  if (patterns.antipatterns.length > 0) {
    console.log("⚠️ Known antipatterns detected - adding to pre-mortem");
  }

  // Run pre-mortem with pattern insights
  const preMortem = await runPreMortem({
    task: config.task,
    knownAntipatterns: patterns.antipatterns,
    provenPatterns: patterns.patterns
  });

  // Continue with normal Phase 1
  return await runDiscoveryPhase(config);
}
```

**2. After Issues Found - Error Reflection**
```javascript
// In convergence-engine/SKILL.md
async function handleIssuesWithLearning(issues) {
  // Normal issue handling
  const fixes = await generateFixes(issues);

  // Reflect on patterns
  for (const issue of issues) {
    // Check if this is a known antipattern
    const knownAntipattern = await checkAntipattern(issue);

    if (knownAntipattern) {
      console.log(`Known issue: ${knownAntipattern.name}`);
      // Apply known fix
      await applyPattern(knownAntipattern.relatedPatterns[0]);
    } else {
      // New issue - reflect
      await errorReflection.analyze(issue);
    }
  }

  return fixes;
}
```

**3. After Success - Pattern Capture**
```javascript
// In convergence-engine/SKILL.md
async function onConvergenceSuccess(result) {
  // If we discovered a new solution approach
  if (result.novel && result.effective) {
    await patternLibrary.savePattern({
      category: 'code-quality',
      problem: result.initialState,
      solution: result.approach,
      metrics: result.metrics
    });

    console.log("✓ New pattern saved to library");
  }
}
```

---

## Storage: Lightweight and Efficient

### Directory Structure

```
.corpus/learning/           # Learning data (keep lightweight)
├── patterns.json          # Single file for all patterns (start simple)
├── antipatterns.json      # Single file for all antipatterns
├── pre-mortems/           # Pre-mortem reports (last 100)
│   └── recent/
└── metrics.json           # Effectiveness tracking
```

**Why not elaborate directory structure?**
- Start simple, evolve based on actual usage
- Single JSON files easier to search initially
- Can split by category later if needed
- Keeps ecosystem fast and lean

### Minimal Configuration

```json
{
  "learning": {
    "enabled": true,
    "autoPatternCheck": true,
    "autoErrorReflection": true,
    "storage": {
      "path": ".corpus/learning",
      "maxPreMortems": 100,
      "maxPatternsInMemory": 50
    },
    "thresholds": {
      "autoApplyConfidence": 0.8,
      "suggestConfidence": 0.5
    }
  }
}
```

---

## Usage Patterns

### Pattern 1: Start of Complex Task

```bash
# User: "Implement OAuth authentication"

# System automatically:
1. Checks pattern library
   → Found: oauth-token-caching (90% success rate)
   → Found antipattern: no-token-caching (seen 2x)

2. Runs pre-mortem
   → Adds rate-limiting risk (from antipattern history)
   → Suggests token caching (from pattern library)

3. Executes with informed approach
4. Captures success as refined pattern
```

### Pattern 2: Error Occurs During Development

```bash
# Error: 429 Too Many Requests from OAuth provider

# System automatically:
1. Error reflection analyzes
   → Root cause: No token caching
   → Matches antipattern: no-token-caching

2. Suggests proven fix
   → Apply pattern: oauth-token-caching

3. Updates antipattern metrics
   → Occurrences: 3 (was 2)
   → Prevention: Add to pre-mortem risks
```

### Pattern 3: Convergence Engine Run

```bash
# User: "Run convergence engine"

# Enhanced flow:
1. Pre-check: Query pattern library for code-quality patterns
2. Pre-mortem: Anticipate common issues based on history
3. Discovery: Run audits
4. Reflection: Analyze any issues found
5. Fixes: Apply proven patterns where available
6. Verification: Standard verification
7. Stabilization: Standard stabilization
8. Update: Save any new patterns discovered
9. GATE: 3 clean passes
```

---

## Performance Considerations

### Keep It Fast

**Pattern queries:**
- In-memory index of patterns (load on startup)
- Simple tag matching (O(n) acceptable for <1000 patterns)
- Lazy load full pattern details only when needed

**Storage:**
- JSON files (easy to read, edit, version control)
- Append-only for new patterns (no file rewrites)
- Periodic cleanup of old pre-mortems

**Memory:**
- Max 50 patterns in memory
- Stream read/write for large operations
- Don't load all pre-mortems at once

### When to Skip Learning

**Skip pattern check if:**
- Trivial task (< 5 min estimated)
- User explicitly says "quick fix"
- No patterns exist for category yet

**Skip error reflection if:**
- Syntax errors (too basic)
- User is experimenting ("trying things out")
- Task marked as "learning/experimental"

---

## Integration Checklist

- [ ] Add pattern check to convergence-engine Phase 1
- [ ] Add error reflection to convergence-engine issue handling
- [ ] Add pattern capture to convergence-engine success path
- [ ] Create .corpus/learning directory structure
- [ ] Initialize empty patterns.json and antipatterns.json
- [ ] Add learning config to corpus-config schema
- [ ] Update convergence-engine SKILL.md with learning hooks
- [ ] Test full loop: pattern → pre-mortem → execute → reflect → update

---

## Metrics to Track

**Pattern Library Growth:**
- Patterns added per week
- Antipatterns identified
- Pattern reuse rate

**Error Reduction:**
- Repeat error rate (should decrease)
- Time to resolution (should decrease)
- Pre-mortem accuracy (should increase)

**Productivity Impact:**
- Tasks accelerated by pattern application
- Errors prevented by antipattern detection
- Time saved vs. baseline

---

## Migration Path

**Phase 1 (Current):**
- Create core 3 learning skills (pre-mortem, error-reflection, pattern-library)
- Lightweight integration with convergence-engine
- Simple JSON storage

**Phase 2 (After validation):**
- Add additional skills based on actual failure modes hit
- Enhance pattern matching (embeddings for semantic search)
- Add metrics dashboard

**Phase 3 (If needed):**
- Cross-project pattern sharing (optional)
- Pattern marketplace (optional)
- Advanced orchestration (only if complexity warrants)

---

## Article Wisdom

*"The sweet spot in January 2026: I use about five skills regularly. That feels like the right amount — enough to cover the failure modes that actually burn me, not so many that I'm managing a system instead of doing work."* - Elliot

**Applied to v4.0:**
- Core 3: pre-mortem, error-reflection, pattern-library
- Add 2-3 more based on real usage (don't pre-optimize)
- Keep integration lightweight
- Focus on compound learning, not automation complexity

---

*End of Integration Guide*
*Keep it simple. Make it useful. Let it compound.*
