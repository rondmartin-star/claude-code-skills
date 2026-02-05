# Iterative Phase Review

**Category:** Core Learning - Phase Transition
**Purpose:** Phase transition quality gate with multi-methodology convergence
**Model:** Claude Opus 4.5
**Status:** Active (v1.0.0)

---

## Quick Reference

Use this skill to review phase deliverables at development phase transitions. Iteratively reviews with 8 orthogonal methodologies until achieving 3 consecutive clean passes.

### Basic Usage

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
```

---

## 8 Review Methodologies

**Random selection, no reuse in clean pass sequences**

1. **Top-Down-Requirements** - Requirements → Deliverables (completeness)
2. **Top-Down-Architecture** - Architecture → Implementation (alignment)
3. **Bottom-Up-Quality** - Artifacts → Standards (quality)
4. **Bottom-Up-Consistency** - Low-level → High-level (consistency)
5. **Lateral-Integration** - Component interfaces and boundaries
6. **Lateral-Security** - Security architecture and implementation
7. **Lateral-Performance** - Performance characteristics
8. **Lateral-UX** - User experience and flows

---

## Convergence

- **3 consecutive clean passes** required
- **8 methodology pool** (random selection)
- **Context cleared** between passes (fresh perspective)
- **Claude Opus 4.5** for highest quality
- **Max 10 iterations** before timeout

---

## Integration Points

### Battle-Plan (Phase 5.5)
Automatically used after Phase 5 (execution), before Phase 6 (verification).

### Windows App Orchestrator
Used at 5 phase transition gates:
1. After requirements phase
2. After system design phase
3. After UI design phase
4. After build phase
5. After deployment phase

---

## Learning Integration

- **verify-evidence** - Validates review results
- **detect-infinite-loop** - Pivots after 3 failed attempts
- **manage-context** - Chunks work at 75% usage
- **error-reflection** - 5 Whys analysis
- **pattern-library** - Stores antipatterns

---

## Return Value

```javascript
{
  converged: boolean,      // true if 3 clean passes achieved
  passes: [],              // Pass details
  issues: [],              // All issues found
  issuesFixed: number,     // Total issues fixed
  cleanPasses: number,     // Consecutive clean passes
  monitoring: {
    loopsDetected: number, // Infinite loops prevented
    contextChunks: number  // Context chunks created
  }
}
```

---

## Implementation

This is a convenience wrapper around `multi-methodology-convergence` configured with:
- Mode: phase-review
- Model: claude-opus-4-5
- Context clearing: true (fresh reviews)
- Learning integration: full

---

## Files

- `SKILL.md` - Full documentation
- `README.md` - This file
- `CHANGELOG.md` - Version history

---

## Version

**v1.0.0** (2026-02-05)
- Initial release
- Wrapper for multi-methodology-convergence
- 8 orthogonal methodologies with random selection
- Full learning integration

---

*Part of v4.0 Universal Skills Ecosystem - Learning Integration*
