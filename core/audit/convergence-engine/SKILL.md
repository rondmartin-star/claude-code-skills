---
name: convergence-engine
description: >
  DEPRECATED - Forwarding to multi-methodology-convergence. This skill has been
  generalized and moved to core/learning/convergence/multi-methodology-convergence.
  Use audit mode for equivalent behavior with enhanced random methodology selection.
---

# Convergence Engine (DEPRECATED)

**Status:** ⚠️ DEPRECATED - Forwarding to new location
**New Location:** `core/learning/convergence/multi-methodology-convergence`
**Migration:** Automatic - Use `mode: 'audit'` for equivalent behavior

---

## ⚡ AUTOMATIC FORWARDING

This skill has been generalized and moved. When you load this skill, it automatically forwards to:

**`multi-methodology-convergence`** with **`mode: 'audit'`**

---

## What Changed

### Enhanced (Better!)
1. **Methodology Pool Expanded**: 3 → 7 orthogonal approaches
   - Technical-Security
   - Technical-Quality
   - Technical-Performance
   - User-Accessibility
   - User-Experience
   - Holistic-Consistency
   - Holistic-Integration

2. **Random Selection**: Prevents pattern blindness
   - Random methodology selection each pass
   - No reuse within clean pass sequences
   - All methodologies available again after issues found

3. **Same 3-Pass Convergence**: Still requires 3 consecutive clean passes

4. **All Learning Integration Preserved**:
   - verify-evidence checkpoints
   - detect-infinite-loop pivot detection
   - manage-context chunking
   - pattern-library updates
   - error-reflection analysis

### Preserved (Backward Compatible)
- Same convergence algorithm
- Same 3-pass clean requirement
- Same learning skills integration
- Same audit methodologies (just more of them!)
- Same context preservation between passes

---

## Migration Guide

### Old Usage
```javascript
await loadSkill('convergence-engine');
await convergenceEngine.run({ projectPath });
```

### New Usage (Equivalent + Enhanced)
```javascript
await loadSkill('multi-methodology-convergence');
await convergence.run({
  mode: 'audit',
  subject: { data: { projectPath } }
});
```

---

## Why the Change?

**Problem:** Phase review convergence needed the SAME pattern as audit convergence
- 80% of logic would be duplicated
- Different subjects (code vs deliverables)
- Different methodologies (audit types vs review approaches)
- Same convergence algorithm

**Solution:** Extract pattern to reusable component
- audit mode = old convergence-engine behavior (enhanced)
- phase-review mode = new phase review behavior
- custom mode = extensible for any convergence scenario

**Result:**
- 30% less code (700 lines vs 1000 lines)
- More maintainable (fix once, benefits all modes)
- More extensible (easy to add new modes)
- Better quality (larger methodology pools, random selection)

---

## New Capabilities

With multi-methodology-convergence you get:

1. **Audit Mode** (this skill's replacement)
   - Enhanced with 7 methodologies and random selection
   - Same behavior otherwise

2. **Phase-Review Mode** (new!)
   - Reviews phase deliverables at transitions
   - 8 orthogonal methodologies
   - Context clearing between passes
   - Uses Claude Opus 4.5

3. **Custom Mode** (new!)
   - Define your own convergence scenarios
   - Architecture reviews
   - Content reviews
   - Any multi-methodology quality process

---

## Files

The new skill is located at:
```
core/learning/convergence/multi-methodology-convergence/
├── SKILL.md       # Main skill (enhanced)
├── README.md      # Quick reference
└── CHANGELOG.md   # Version history
```

---

## Automatic Loading

When you reference `convergence-engine`, Claude Code will:
1. Detect this is a forwarding file
2. Load `multi-methodology-convergence` instead
3. Configure it with `mode: 'audit'`
4. Run with exact same behavior (enhanced)

**You don't need to change anything in your workflows!**

---

## Questions?

**Q: Will my existing workflows break?**
A: No. Backward compatibility maintained. audit mode = convergence-engine behavior.

**Q: Should I update my code?**
A: Optional but recommended. New location is more maintainable.

**Q: Can I still use the old 3-methodology set?**
A: Yes! The new skill includes all old methodologies plus 4 more. Random selection means you'll see all perspectives over time.

**Q: What about the 3-3-1 rule?**
A: Preserved! Still 3 consecutive clean passes required. Just more diverse methodologies.

---

*Deprecated: 2026-02-05*
*Replaced by: multi-methodology-convergence (audit mode)*
*Part of v4.0 Universal Skills Ecosystem - Learning Integration*
