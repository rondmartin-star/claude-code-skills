# CorpusHub Integration Summary

**Date:** 2026-01-31
**Purpose:** Quick reference for how CorpusHub docs improved our v4.0 plan

---

## What We Learned

### 1. Production corpus-config.json Schema ✅

**Before (Our Draft):**
```json
{
  "name": "My Project",
  "type": "web-app",
  "artifacts": [ /* array */ ],
  "framework_terms": { /* flat */ }
}
```

**After (CorpusHub Production):**
```json
{
  "corpus": {
    "name": "My Corpus",
    "description": "...",
    "version": "1.0.0",
    "baseDir": "/absolute/path"
  },
  "artifacts": {
    "artifact-slug": { /* object keys */ }
  },
  "framework": {
    "categories": [ /* structured */ ]
  },
  "voice": { /* AI guidance */ },
  "roles": { /* granular permissions */ }
}
```

**Impact:** Use real schema in all templates and skills.

---

### 2. Multi-Methodology Audit (3-3-1 Rule) ✅

**Before (Our Draft):**
- Simple convergence: run audits until 3 clean passes
- No methodology distinction
- No time budgets

**After (CorpusHub Proven):**
```
3 Methodologies (Parallel):
├─ Technical (how it works)
├─ User (how it's experienced)
└─ Holistic (how it fits together)

×

3 Iterations (Minimum):
├─ Discovery (2-4h) - find 60-80% of issues
├─ Verification (1-2h) - catch gaps, find 20-30% more
└─ Stabilization (0.5-1h) - confirm 0 critical/high

×

1 User Validation (Essential):
└─ Real users, environment, workflows, data
```

**Proven Results:**
- F → A grade in 5 hours
- 23 issues found (vs. ~8 single method)
- $27,600+ savings
- ROI: 25x to 2,000x

**Impact:** Completely redesign convergence-engine with this methodology.

---

### 3. Bidirectional Architecture (Source Modes) ✅

**Before (Our Draft):**
- No concept of source modes
- Assumed all content in corpus

**After (CorpusHub Production):**

**Three Source Modes:**

1. **`source_of_truth = 'corpus'`**
   - For: Requirements, design docs, ADRs
   - Edit in CorpusHub only
   - Traditional file deleted or not created

2. **`source_of_truth = 'source'`**
   - For: Implementation code, config files
   - Edit in IDE (VS Code, etc.)
   - Corpus HTML auto-generated (read-only)
   - File watcher triggers regeneration

3. **`source_of_truth = 'bidirectional'`**
   - For: Documentation (README, guides, API docs)
   - Edit in EITHER location
   - Automatic bidirectional sync
   - File watcher temporarily disabled during sync

**Impact:** Create source-mode-manager skill to handle all three modes.

---

### 4. Corpus Detection API ✅

**Before (Our Draft):**
- No detection mechanism
- Just create corpus-config.json

**After (CorpusHub Production):**

**Full Detection API:**
```bash
GET /api/corpora/detect?path=/path
POST /api/corpora/validate
GET /api/corpora/registration-status?path=/path
GET /api/corpora/:slug/health
```

**CLI Tool:**
```bash
node scripts/detect-corpus.js /path/to/project
node scripts/detect-corpus.js /path/to/project --json
node scripts/detect-corpus.js --health corpus-slug
```

**Checks:**
- configExists, configValid
- isRegistered
- infrastructureExists, databaseExists
- bitCount, fileCount, edgeCount

**Impact:** corpus-init MUST use detection API before initializing.

---

## Key Changes to Our Plan

### 1. Updated Core Skills

**core/corpus/** (4 → 6 skills):
- corpus-init (UPDATED: uses detection API)
- corpus-convert (UPDATED: uses detection API)
- corpus-detect (NEW: wrapper for API)
- corpus-config (UPDATED: validates real schema)
- source-mode-manager (NEW: handles 3 modes)
- corpus-orchestrator (existing)

**core/audit/** (3 → 4 groups):
- audit-orchestrator (existing)
- convergence-engine (UPDATED: 3-3-1 methodology)
- fix-planner (existing)
- methodologies/ (NEW: technical, user, holistic)
  - methodologies/technical/ (security-architecture, code-quality, performance-profiling)
  - methodologies/user/ (auth-flow-testing, ux-performance, accessibility)
  - methodologies/holistic/ (documentation, dependency-audit, consistency)

### 2. Updated Configuration Templates

**All templates now include:**
- Proper CorpusHub schema (corpus, artifacts as object, framework.categories)
- Source modes for each artifact type
- Voice section with AI guidance
- Roles with granular permissions (aiAccess, editAccess)
- Multi-methodology audit configuration with time budgets

**Example:** config/templates/web-app.json
```json
{
  "corpus": { "name": "...", "baseDir": "...", "version": "1.0.0" },
  "artifacts": {
    "source-code": { "sourceMode": "source" },
    "requirements": { "sourceMode": "corpus" },
    "documentation": { "sourceMode": "bidirectional" }
  },
  "audit": {
    "methodology": "multi-methodology-3-3-1",
    "convergence": {
      "methodologies": [
        { "name": "technical", "audits": [...] },
        { "name": "user", "audits": [...] },
        { "name": "holistic", "audits": [...] }
      ],
      "iterations": {
        "discovery": { "time_budget": "2-4h", "fix_priority": ["critical", "high"] },
        "verification": { "time_budget": "1-2h" },
        "stabilization": { "time_budget": "0.5-1h" }
      }
    }
  }
}
```

### 3. Updated Success Metrics

**Corpus Integration:**
- ✅ 100% schema compliance
- ✅ Detection API integration
- ✅ All 3 source modes supported
- ✅ Automatic registration

**Audit Methodology:**
- ✅ 3 methodologies per project
- ✅ Min 3 iterations + user validation
- ✅ Time budgets: 5-12 hours total
- ✅ Grade improvement: D/F → A/B
- ✅ ROI: >25x

---

## Implementation Impact

### Week 1 (UPDATED)
1. ~~Create simple corpus-init~~
2. **Create corpus-detect** (wrapper for CorpusHub API)
3. **Update corpus-init** (use detection, real schema, source modes)
4. **Study 3-3-1 methodology** for convergence-engine

### Week 2 (UPDATED)
5. **Create source-mode-manager** (handle 3 modes with file watchers)
6. **Rewrite convergence-engine** (3 methodologies × 3 iterations × 1 validation)
7. **Create methodology-specific audits** (9 total: 3 per methodology)
8. Test with real CorpusHub instance

### Week 3 (UPDATED)
9. **Update all config templates** (real schema, source modes, audit config)
10. **Create config examples** (from CorpusHub itself)
11. **Test bidirectional sync** (file watcher + SSE)
12. Integration testing

---

## Documentation Required

### New Documents (3)

1. **CORPUS-INTEGRATION-GUIDE.md**
   - CorpusHub detection API usage
   - Source modes explained (corpus, source, bidirectional)
   - File watcher patterns
   - Bidirectional sync implementation

2. **MULTI-METHODOLOGY-AUDIT-GUIDE.md**
   - 3-3-1 Rule detailed
   - Methodology selection by domain
   - Time budgets per phase
   - Success criteria and grading
   - Proven results (CorpusHub case study)

3. **CONFIG-SCHEMA-REFERENCE.md**
   - Complete corpus-config.json schema
   - All sections with examples
   - Validation rules
   - Migration guide from simplified schema

### Updated Documents (5)

1. **CLAUDE.md** - Add CorpusHub integration section
2. **REORGANIZATION-PLAN.md** - Update corpus-config schema
3. **AUDIT-SYSTEM-DESIGN.md** - Replace with 3-3-1 methodology
4. **REORGANIZATION-v4-SUMMARY.md** - Add CorpusHub integration
5. **STREAMLINED-INTEGRATION.md** - Add source modes

---

## Risks Mitigated

### Risk: Over-generalization
**Mitigation:** Use production-proven CorpusHub patterns, not invented ones.

### Risk: Invalid schema
**Mitigation:** All templates match CorpusHub production schema exactly.

### Risk: Weak audit methodology
**Mitigation:** Use proven 3-3-1 methodology with documented $27k+ savings.

### Risk: Missed edge cases
**Mitigation:** CorpusHub detection API handles all edge cases (partial init, broken config, etc.)

---

## Bottom Line

**Before Reading Docs:**
- Simple corpus-config.json (invented schema)
- Basic convergence (invented algorithm)
- No source mode concept
- No detection mechanism

**After Reading Docs:**
- Production CorpusHub schema (proven)
- Multi-methodology 3-3-1 (proven: F→A, 5hrs, $27k+ savings)
- Three source modes (production feature)
- Full detection API (production-ready)

**Impact:**
- ✅ No invented patterns - all production-proven
- ✅ Better audit methodology - 3x issue coverage
- ✅ More flexible - 3 source modes vs. 1
- ✅ Safer initialization - detect before init
- ✅ Higher confidence - based on real implementation

---

**Status:** INTEGRATION COMPLETE
**Next:** Update all planning docs and begin implementation
**Repository:** https://github.com/rondmartin-star/claude-code-skills

---

*Based on CorpusHub production documentation (C:\Program Files\CorpusHub\docs)*
*Key files: CORPUS-CONFIG-SCHEMA.md, AUDIT-METHODOLOGY-EXECUTIVE-SUMMARY.md, BIDIRECTIONAL-ARCHITECTURE.md, CORPUS-DETECTION.md*
