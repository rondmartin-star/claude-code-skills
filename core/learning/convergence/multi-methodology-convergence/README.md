# Multi-Methodology Convergence

**Category:** Core Learning - Convergence
**Purpose:** Generic multi-methodology iterative quality improvement with 3-pass convergence
**Status:** Active (v1.0.0)

---

## Quick Reference

Use this skill when you need iterative quality improvement with multiple review methodologies until achieving 3 consecutive clean passes.

### Common Use Cases

```javascript
// Audit convergence (code quality)
const result = await convergence.run({
  mode: 'audit',
  subject: { data: { projectPath: '/path/to/project' } }
});

// Phase review (deliverable quality)
const result = await convergence.run({
  mode: 'phase-review',
  subject: {
    data: {
      phase: { name: 'requirements', scope: [...] },
      deliverables: [...],
      requirements: [...]
    }
  }
});

// Custom convergence
const result = await convergence.run({
  mode: 'custom',
  subject: { type: 'architecture', data: {...} },
  methodologies: [
    { name: 'scalability', executor: reviewScalability },
    { name: 'security', executor: reviewSecurity },
    { name: 'maintainability', executor: reviewMaintainability }
  ],
  verify: {
    clean: async (result) => result.issues.length === 0
  },
  fix: {
    executor: async (issues) => await fixArchitecture(issues)
  }
});
```

---

## Modes

### audit
- **Subject:** Code and project files
- **Methodology Pool:** 7 approaches (technical-security, technical-quality, technical-performance, user-accessibility, user-experience, holistic-consistency, holistic-integration)
- **Selection:** Random (no reuse in clean sequence)
- **Context:** Preserved between passes
- **Use:** Pre-release code quality convergence

### phase-review
- **Subject:** Phase deliverables and artifacts
- **Methodology Pool:** 8 approaches (top-down-requirements, top-down-architecture, bottom-up-quality, bottom-up-consistency, lateral-integration, lateral-security, lateral-performance, lateral-ux)
- **Selection:** Random (no reuse in clean sequence)
- **Context:** Cleared between passes (fresh review)
- **Model:** claude-opus-4-5 (highest quality)
- **Use:** Phase transition quality gates

### custom
- **Subject:** User-defined
- **Methodologies:** User-defined
- **Configuration:** Full control
- **Use:** Any convergence scenario

---

## Convergence Requirements

- **3 consecutive clean passes** required
- **Different methodology per pass** (random selection from pool)
- **Pool of 5-10 orthogonal methodologies** (no reuse in clean sequence)
- **Max 10 iterations** before timeout
- **Learning integration** throughout

---

## Learning Skills Integration

- `verify-evidence` - Checkpoint validation
- `detect-infinite-loop` - Pivot after 3 failed attempts
- `manage-context` - Chunk work at 75% usage
- `pattern-library` - Store antipatterns
- `error-reflection` - 5 Whys analysis

---

## Backward Compatibility

Replaces `core/audit/convergence-engine`. Symlink maintained for transition period.

Old usage:
```javascript
await loadSkill('convergence-engine');
```

New usage (equivalent):
```javascript
await loadSkill('multi-methodology-convergence');
// OR
await convergence.run({ mode: 'audit', ... });
```

---

## Files

- `SKILL.md` - Main skill implementation
- `README.md` - This file (quick reference)
- `CHANGELOG.md` - Version history

---

## Version

**v1.0.0** (2026-02-05)
- Initial release
- Extracted from convergence-engine
- Added phase-review mode
- Added custom mode support
- Full learning skills integration

---

*Part of v4.0 Universal Skills Ecosystem*
