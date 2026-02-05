# Changelog - Multi-Methodology Convergence

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-02-05

### Added
- Initial release of multi-methodology-convergence skill
- Generic convergence pattern extracted from convergence-engine
- Mode-based configuration system (audit, phase-review, custom)
- **Enhanced methodology selection**: Random selection from pool of 5-10 orthogonal approaches
- **Constraint-based selection**: No methodology reuse within clean pass sequences
- **Pool reset**: Methodology tracking clears when consecutive clean count resets to 0
- Full learning skills integration:
  - verify-evidence for checkpoint validation
  - detect-infinite-loop for pivot detection
  - manage-context for chunking long sessions
  - error-reflection for issue analysis
  - pattern-library for antipattern storage

### Audit Mode
- 7 orthogonal methodology pool:
  - Technical-Security (security architecture, vulnerabilities, auth)
  - Technical-Quality (code quality, maintainability, testability)
  - Technical-Performance (performance bottlenecks, optimization)
  - User-Accessibility (WCAG compliance, accessibility standards)
  - User-Experience (UX patterns, usability, interaction flows)
  - Holistic-Consistency (naming, patterns, architectural consistency)
  - Holistic-Integration (navigation, API coherence, documentation)
- Context preservation between passes
- Backward compatible with convergence-engine

### Phase-Review Mode
- 8 orthogonal methodology pool:
  - Top-Down-Requirements (requirements → deliverables completeness)
  - Top-Down-Architecture (architecture → implementation alignment)
  - Bottom-Up-Quality (code/artifacts → standards validation)
  - Bottom-Up-Consistency (low-level → high-level consistency)
  - Lateral-Integration (component interfaces and boundaries)
  - Lateral-Security (security architecture and implementation)
  - Lateral-Performance (performance characteristics and bottlenecks)
  - Lateral-UX (user experience and interaction flows)
- Context clearing between passes (fresh review)
- Claude Opus 4.5 model for highest quality reviews

### Custom Mode
- User-defined subject and methodologies
- Full configuration control
- Extensible for any convergence scenario

### Technical
- State tracking for used methodologies in clean sequences
- Random selection algorithm with constraint enforcement
- Pool exhaustion protection (reset if all methodologies used)
- Monitoring statistics (loops detected, context chunks)
- Backward compatibility symlink support

---

## Design Decisions

### Random Selection with Pool
**Decision:** Use random selection from 5-10 methodology pool instead of fixed rotation

**Rationale:**
- More diverse perspectives prevent pattern blindness
- Random selection reduces confirmation bias
- Larger pool provides orthogonal coverage
- Constraint (no reuse in clean sequence) ensures variety while allowing eventual reuse

**Implementation:**
```javascript
// Track used methodologies in current clean sequence
state.usedMethodologiesInCleanSequence = new Set();

// Select random from unused methodologies
const unusedMethodologies = pool.filter(
  m => !state.usedMethodologiesInCleanSequence.has(m.name)
);
const methodology = unusedMethodologies[randomIndex];

// On clean pass: mark as used
state.usedMethodologiesInCleanSequence.add(methodology.name);

// On issues found: reset tracking
state.usedMethodologiesInCleanSequence.clear();
```

### Orthogonal Methodology Design
**Decision:** Design methodologies to be orthogonal (non-overlapping perspectives)

**Examples:**
- Audit: Technical vs User vs Holistic (different stakeholder views)
- Phase Review: Top-Down vs Bottom-Up vs Lateral (different traversal directions)

**Benefit:** Each methodology provides unique insights, minimal redundancy

---

## Migration from convergence-engine

### Breaking Changes
None. Full backward compatibility maintained via:
- audit mode preserves exact convergence-engine behavior (enhanced with random selection)
- Symlink at old location during transition period
- Old API still works

### Enhancements
1. **Expanded methodology pools**: 3 → 7 (audit) and 3 → 8 (phase-review)
2. **Random selection**: Prevents methodology pattern blindness
3. **No reuse constraint**: Ensures diverse perspectives in clean sequences
4. **Mode system**: Enables new convergence use cases (phase-review, custom)

### Migration Path
```javascript
// Old (convergence-engine)
await loadSkill('convergence-engine');
await convergenceEngine.run({ projectPath });

// New (equivalent behavior with enhancements)
await loadSkill('multi-methodology-convergence');
await convergence.run({
  mode: 'audit',
  subject: { data: { projectPath } }
});
```

---

## Future Enhancements

### Under Consideration
- [ ] Methodology effectiveness tracking (which methodologies find most issues)
- [ ] Adaptive pool sizing based on subject complexity
- [ ] Inter-methodology dependency hints
- [ ] Parallel methodology execution for faster convergence
- [ ] Custom methodology pool per project (project-specific perspectives)

### Not Planned
- Automatic methodology generation (requires human expertise for orthogonal design)
- Methodology ordering hints (defeats purpose of random selection)

---

## Attribution

**Inspiration:** Elliot's "Claude Skill Potions" article (January 28, 2026)
- Concept: Compound learning and institutional memory
- Pattern: Convergence-based quality improvement

**Enhancement:** Random pool selection (February 5, 2026)
- Requested by: User feedback during implementation
- Rationale: More diverse perspectives, reduced pattern blindness

---

*Part of v4.0 Universal Skills Ecosystem - Learning Integration*
