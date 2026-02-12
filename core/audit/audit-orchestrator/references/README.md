# Audit Orchestrator - References

**Purpose:** Detailed documentation for audit-orchestrator implementation

---

## Reference Files

### 1. parallel-execution.md

**Complete parallel execution implementation:**
- Dependency graph and detection logic
- Topological sort algorithm (Kahn's algorithm)
- Sequential and parallel execution functions
- Batching with maxConcurrent limit
- Error handling patterns
- Performance metrics tracking
- Configuration options
- Testing examples
- Optimization tips

**Use for:** Implementing parallel audit execution, understanding dependency resolution, optimizing performance

---

### 2. complexity-assessment.md

**Battle-plan integration and complexity routing:**
- Complexity assessment function
- Complexity level definitions (trivial, simple, medium, complex)
- Battle-plan routing logic
- Monitoring integration (verify-evidence, detect-infinite-loop, manage-context)
- Configuration examples
- Full battle-plan workflow example

**Use for:** Understanding when to use battle-plan, implementing complexity assessment, configuring monitoring

---

### 3. workflow-examples.md

**Detailed execution traces:**
- Example 1: Web app pre-release (complex, battle-plan, convergence, parallel)
- Example 2: Content corpus quick check (simple, no battle-plan, parallel)
- Example 3: Manual audit selection (simple, parallel)
- Example 4: Error handling (audit failure recovery)
- Example 5: Custom configuration overrides
- Example 6: Resume from previous state

**Use for:** Understanding end-to-end workflows, debugging execution issues, training

---

## Quick Navigation

**Need to implement parallel execution?**
-> Start with `parallel-execution.md`

**Need to add new audit dependencies?**
-> See AUDIT_DEPENDENCIES in `parallel-execution.md`

**Need to understand complexity routing?**
-> See `complexity-assessment.md`

**Need to see full examples?**
-> See `workflow-examples.md`

**Need to integrate with battle-plan?**
-> See battle-plan section in `complexity-assessment.md`

---

## Implementation Checklist

When implementing audit-orchestrator:

- [ ] Read main SKILL.md for overview
- [ ] Implement dependency detection (parallel-execution.md)
- [ ] Implement topological sort (parallel-execution.md)
- [ ] Implement parallel execution with batching (parallel-execution.md)
- [ ] Add error handling for individual audit failures (parallel-execution.md)
- [ ] Implement complexity assessment (complexity-assessment.md)
- [ ] Integrate with battle-plan for medium/complex operations (complexity-assessment.md)
- [ ] Add configuration loading from corpus-config.json
- [ ] Add performance metrics tracking (parallel-execution.md)
- [ ] Test with workflow examples (workflow-examples.md)

---

*Part of audit-orchestrator v4.0*
*Parallel execution support added 2026-02-12*
