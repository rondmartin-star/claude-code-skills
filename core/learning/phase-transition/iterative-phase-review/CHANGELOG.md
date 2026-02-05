# Changelog - Iterative Phase Review

All notable changes to this skill will be documented in this file.

---

## [1.0.0] - 2026-02-05

### Added
- Initial release of iterative-phase-review skill
- Convenient wrapper for multi-methodology-convergence (phase-review mode)
- 8 orthogonal review methodologies:
  - Top-Down-Requirements (requirements → deliverables completeness)
  - Top-Down-Architecture (architecture → implementation alignment)
  - Bottom-Up-Quality (artifacts → standards quality validation)
  - Bottom-Up-Consistency (low-level → high-level consistency)
  - Lateral-Integration (component interfaces and boundaries)
  - Lateral-Security (security architecture and implementation)
  - Lateral-Performance (performance characteristics and bottlenecks)
  - Lateral-UX (user experience and interaction flows)
- Random methodology selection from pool (no reuse in clean sequences)
- Claude Opus 4.5 for highest quality reviews
- Context clearing between passes for fresh perspectives
- Full learning integration:
  - verify-evidence for review validation
  - detect-infinite-loop for pivot detection
  - manage-context for chunking long sessions
  - error-reflection for 5 Whys analysis
  - pattern-library for antipattern storage
- Phase-specific usage examples (requirements, design, build, deployment)
- Integration with battle-plan (Phase 5.5)
- Integration with windows-app-orchestrator (5 phase gates)

### Configuration
- Minimal config: phase, deliverables, requirements
- Optional convergence overrides (cleanPasses, maxIterations)
- Auto-configured for phase-review mode
- Context clearing enabled by default

### Documentation
- Complete SKILL.md with 8 methodology descriptions
- Quick reference README.md
- Version history CHANGELOG.md
- Usage examples for all development phases
- Integration point documentation

---

## Purpose and Design

### Why This Skill?

**Problem:** Phase transitions in development often skip rigorous quality validation
- Incomplete phases lead to rework in later phases
- Single-pass reviews miss issues from other perspectives
- Manual reviews inconsistent and time-consuming

**Solution:** Automated multi-methodology iterative review at phase gates
- 8 orthogonal methodologies ensure comprehensive coverage
- Random selection prevents pattern blindness
- Convergence to 3 clean passes ensures quality
- Claude Opus 4.5 provides highest quality analysis

### Design Principles

1. **Comprehensive Coverage**: 8 methodologies cover all quality dimensions
   - Top-down (requirements, architecture)
   - Bottom-up (quality, consistency)
   - Lateral (integration, security, performance, UX)

2. **Fresh Perspectives**: Context clearing between passes
   - Prevents confirmation bias
   - Each pass independent
   - No cumulative blindness

3. **Highest Quality**: Claude Opus 4.5 for all reviews
   - Best available model for quality analysis
   - Worth the cost at phase gates
   - Critical quality checkpoints

4. **Learning Integration**: Full pattern library integration
   - Compound learning from phase to phase
   - Antipatterns identified and prevented
   - Prevention measures applied in future phases

5. **Fool-Proof**: Sensible defaults, clear configuration
   - Minimal config required
   - Auto-detect phase type
   - Clear error messages

### Integration Strategy

**Battle-Plan Integration (Phase 5.5):**
- Inserted between Phase 5 (execution) and Phase 6 (verification)
- Reviews task deliverables before declaring complete
- Ensures quality before moving forward

**Windows App Orchestrator Integration:**
- 5 phase transition gates
- Each gate reviews phase-specific deliverables
- Prevents incomplete phases from proceeding

---

## Methodology Design

### Orthogonality

Each methodology provides unique perspective with minimal overlap:

**Top-Down**: Requirements and architecture perspective
- Requirements: Are we building the right thing?
- Architecture: Are we building it the right way?

**Bottom-Up**: Implementation and quality perspective
- Quality: Is it well-built?
- Consistency: Is it internally coherent?

**Lateral**: Cross-cutting concerns
- Integration: Do parts work together?
- Security: Is it secure?
- Performance: Is it fast enough?
- UX: Is it usable?

### Coverage Matrix

| Methodology | Requirements | Architecture | Implementation | Quality | Integration |
|-------------|--------------|--------------|----------------|---------|-------------|
| Top-Down-Requirements | ✓ Primary | | | | |
| Top-Down-Architecture | | ✓ Primary | ✓ Secondary | | |
| Bottom-Up-Quality | | | ✓ Secondary | ✓ Primary | |
| Bottom-Up-Consistency | | | ✓ Primary | ✓ Secondary | |
| Lateral-Integration | | ✓ Secondary | | | ✓ Primary |
| Lateral-Security | ✓ Secondary | ✓ Secondary | ✓ Primary | | ✓ Secondary |
| Lateral-Performance | | ✓ Secondary | ✓ Primary | | |
| Lateral-UX | ✓ Secondary | | ✓ Primary | | ✓ Secondary |

**Result:** Every quality dimension covered by at least 2 methodologies (redundancy)

---

## Usage Patterns

### Pattern 1: Windows App Development (5 Gates)

```
Phase 1: Requirements
  → Complete requirements deliverables
  → GATE 1: iterative-phase-review
    - Validate user stories, acceptance criteria, data models
    - Converge until 3 clean passes
  → Proceed to System Design

Phase 2: System Design
  → Complete design deliverables
  → GATE 2: iterative-phase-review
    - Validate data models, API specs, architecture
    - Converge until 3 clean passes
  → Proceed to UI Design

Phase 3: UI Design
  → Complete UI deliverables
  → GATE 3: iterative-phase-review
    - Validate pages, navigation, forms
    - Converge until 3 clean passes
  → Proceed to Build

Phase 4: Build
  → Complete implementation
  → GATE 4: iterative-phase-review
    - Validate code, tests, documentation
    - Converge until 3 clean passes
  → Proceed to Deployment

Phase 5: Deployment
  → Complete deployment setup
  → GATE 5: iterative-phase-review
    - Validate service config, health checks, installer
    - Converge until 3 clean passes
  → Production Ready
```

### Pattern 2: Battle-Plan Task Execution

```
Battle-Plan Phases:
  1. Clarify requirements
  2. Check pattern library
  3. Pre-mortem risks
  4. Confirm with user
  5. Execute task
  → 5.5. ITERATIVE PHASE REVIEW (NEW)
    - Review task deliverables
    - Converge until 3 clean passes
    - Log learnings to pattern library
  6. Verification (verify-evidence)
  7. Declare complete
  8. Update patterns
```

---

## Future Enhancements

### Under Consideration
- [ ] Phase-specific methodology pools (e.g., requirements phase uses subset)
- [ ] Adaptive convergence (adjust cleanPasses based on phase criticality)
- [ ] Cross-phase consistency checks (reference previous phase deliverables)
- [ ] Automated deliverable discovery (detect from file system)
- [ ] Integration with project management tools (Jira, Linear)

### Not Planned
- Parallel methodology execution (defeats purpose of random selection)
- Automatic phase transition (requires human approval)
- Skip convergence option (defeats purpose of quality gate)

---

## Metrics

**Expected Performance:**
- Convergence rate: 80%+ within 10 iterations
- Average passes to convergence: 5-7
- Issues found per phase: 5-15 (early phases), 1-5 (later phases)
- Time per pass: 2-5 minutes (depends on deliverable complexity)
- Total review time: 10-35 minutes per phase

**Learning Effectiveness:**
- Antipatterns identified: 1-3 per phase
- Prevention measures: 2-5 per phase
- Pattern library growth: Compound over multiple phases
- Issue recurrence: Should decrease with pattern library maturity

---

## Attribution

**Concept:** Elliot's "Claude Skill Potions" article (January 28, 2026)
- Compound learning and institutional memory
- Multi-methodology convergence pattern

**Enhancement:** Random methodology selection (February 5, 2026)
- User-requested feature
- Prevents pattern blindness

**Integration:** Phase transition quality gates (February 5, 2026)
- Battle-plan Phase 5.5
- Windows app orchestrator phase gates

---

*Part of v4.0 Universal Skills Ecosystem - Learning Integration*
*Wrapper for: multi-methodology-convergence (phase-review mode)*
