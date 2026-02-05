# Battle-Plan Orchestrator

**Category:** Core Learning - Orchestrators
**Purpose:** Master workflow for complex operations with learning-first approach
**Status:** Active (v2.1.0)

---

## Quick Reference

Use this skill for complex, multi-step operations requiring systematic planning and quality validation.

### Phases

1. **Clarification** - Understand the task (clarify-requirements)
2. **Knowledge Check** - Check pattern library for proven solutions
3. **Risk Assessment** - Run pre-mortem to anticipate failures
4. **Confirmation** - Get user approval before execution
5. **Execution** - Execute with monitoring (verify-evidence, detect-infinite-loop, manage-context)
5.5. **Iterative Phase Review** - Multi-methodology quality gate (NEW v2.1.0)
6. **Reflection** - Analyze errors with 5 Whys (error-reflection)
7. **Completion** - Declare done, block perfectionism (declare-complete)
8. **Pattern Update** - Update pattern library for future tasks

---

## When to Use

**Trigger Phrases:**
- "Run battle-plan"
- "Use learning workflow"
- Complex task detected automatically

**Context Indicators:**
- Task complexity >= medium
- Multi-step operation
- High-risk change
- Architectural decision
- User-facing feature

---

## Phase 5.5: Iterative Phase Review (NEW)

**Added in v2.1.0**

After Phase 5 (Execution) completes, if deliverables were produced, automatically run a multi-methodology quality review:

- **8 Review Methodologies:** Top-Down (Requirements, Architecture), Bottom-Up (Quality, Consistency), Lateral (Integration, Security, Performance, UX)
- **Random Selection:** No reuse within clean pass sequences
- **Fresh Perspective:** Context cleared between passes
- **3-Pass Convergence:** Requires 3 consecutive clean passes
- **Model:** Claude Opus 4.5 for highest quality
- **Time:** ~10-20 minutes for typical tasks

**Skip Condition:** Automatically skipped for pure research/exploration tasks with no deliverables.

---

## Key Principles

1. **Learn First:** Check pattern library before executing
2. **Think First:** Run pre-mortem before implementing
3. **Monitor During:** Use verify-evidence, detect-infinite-loop, manage-context
4. **Review After Execution:** Multi-methodology convergence (Phase 5.5)
5. **Reflect After:** Run error-reflection if issues occur
6. **Compound Learning:** Update pattern library for future tasks

---

## Workflow Diagram

```
User Request →
  CLARIFY (understand) →
  CHECK PATTERNS (learn from past) →
  PRE-MORTEM (anticipate failures) →
  CONFIRM (get approval) →
  EXECUTE (with monitoring) →
  REVIEW (multi-methodology convergence) →
  REFLECT (analyze results) →
  COMPLETE (declare done) →
  UPDATE PATTERNS (feed back to library)
```

---

## Files

- `SKILL.md` - Full documentation with all 9 phases
- `README.md` - This file (quick reference)
- `CHANGELOG.md` - Version history

---

## Version

**v2.1.0** (2026-02-05)
- Added Phase 5.5: Iterative Phase Review
- Enhanced workflow with quality gate after execution
- Full learning integration maintained

---

*Part of v4.0 Universal Skills Ecosystem - Learning Integration*
