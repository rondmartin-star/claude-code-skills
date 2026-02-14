---
name: skill-ecosystem-manager
description: >
  Create, maintain, and improve skill ecosystems. Covers skill design philosophy,
  ecosystem architecture, error-driven improvement, and continuous refinement.
  Use when: creating new skills, refactoring existing skills, improving skills
  based on logged errors, or managing multi-skill workflows.
---

# Skill Ecosystem Manager

**Purpose:** Design and maintain high-quality skill ecosystems  
**Size:** ~12 KB (references: ~15 KB)  
**Philosophy:** Small skills, on-demand references, error-driven improvement

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Create a new skill for..."
- "Refactor this skill"
- "The skill is too large"
- "Improve skills based on these errors"
- "Document this workflow as a skill"
- "How should I structure this skill?"
- "Add learnings to the skill"

**Context Indicators:**
- User uploads ERROR-AND-FIXES-LOG.md
- User mentions skill size concerns
- User wants to capture repeatable workflows
- Discussion about skill organization
- Need to split a monolithic skill

## ❌ DO NOT LOAD WHEN

- Using skills (load the specific skill instead)
- General development work
- No skill creation/maintenance intent

---

## ⚡ Parallel Operations (v4.1)

**CRITICAL:** Every integration action MUST use parallel execution for 3-10x speedup.

| Operation | Sequential | Parallel | Speedup | Tasks |
|-----------|-----------|----------|---------|-------|
| Validate 10 skills | 7m | 45s | 9.3x | 10 |
| Create 5 skills | 8m | 2m | 4x | 5 |
| Refactor 15 skills | 45m | 8m | 5.6x | 15 |
| Apply learnings (20) | 30m | 5m | 6x | 20 |
| Quality check (30) | 25m | 4m | 6.3x | 30 |
| Test 12 skills | 18m | 4m | 4.5x | 12 |

### Quick Pattern: Launch All Tasks in Single Message

```
User: "Validate these 10 skills: corpus-init, corpus-convert,
       audit-orchestrator, convergence-engine, ..."

Claude: [Launches 10 Task tool calls in single message]
        Task 1: Validate corpus-init
        Task 2: Validate corpus-convert
        ...
        Task 10: Validate [skill]

        [45s later - all complete]

        Results: 9/10 passed, 1 failed (size violation)
```

### When to Parallelize

✅ **ALWAYS parallel:**
- Validating multiple skills (size, structure, frontmatter)
- Creating unrelated skills from templates
- Extracting references from multiple skills
- Applying error learnings to multiple skills
- Running quality checks across ecosystem
- Testing multiple skills
- Generating documentation

❌ **NEVER parallel:**
- Creating orchestrator + skills it routes to (dependency)
- Updating cross-references between skills (conflicts)
- Sequential workflow steps (order matters)

**For detailed patterns:** `references/parallel-operations.md`

---

## v4.1 Intelligent Parallelization Decision Framework

**When creating a new skill, decide if parallelization adds value:**

### ✅ Add Parallelization If:

- **Independent operations** - No dependencies between items
- **Batch/multiple items** - Commonly processes 10+ items
- **Proven speedup** - Expected > 2x performance improvement
- **Examples:** Batch CRUD, multi-platform publishing, parallel validation, concurrent analysis

### ❌ Skip Parallelization If:

- **Sequential workflow** - Step A must complete before step B
- **Single-item operations** - Primarily works with one item at a time
- **User interaction** - Requires human input (can't parallelize)
- **Data integrity** - Sequential processing ensures correctness
- **Planning/design** - Inherently sequential activities
- **Examples:** Status checks, configuration edits, user confirmation, workflow planning

### 🎯 Current Ecosystem State

**Total Skills:** 61 (v4.1 architecture)
**Parallelized:** 24 skills (39% - optimal coverage)
**Non-parallelized:** 37 skills (61% - intentionally sequential)

| Category | Parallelized | Total | % | Rationale |
|----------|--------------|-------|---|-----------|
| Audit | 9 | 12 | 75% | High-volume batch operations |
| Content | 3 | 4 | 75% | Multi-document workflows |
| Publishing | 2 | 2 | 100% | Multi-platform by design |
| Development | 5 | 14 | 36% | Only validation/generation |
| Corpus | 2 | 6 | 33% | Only multi-artifact ops |
| Utilities | 2 | 7 | 29% | Only integration/ecosystem |
| Learning | 2 | 13 | 15% | Mostly sequential planning |
| Core | 0 | 1 | 0% | Orchestrator delegates |

**Philosophy:** Intelligent parallelization where valuable, not universal coverage.

**See:** `references/parallelization-decision-guide.md` for detailed decision trees

---

## Core Design Philosophy

### The 15KB Rule

**SKILL.md files should stay under 15 KB.** This ensures:
- Fast loading into context
- Room for actual work
- Focused, scannable content

| Content Type | Location | Size Target |
|--------------|----------|-------------|
| Triggers & quick reference | SKILL.md | < 15 KB |
| Detailed templates | references/*.md | Any size |
| Code examples | references/*.md | Any size |
| Checklists & audits | references/*.md | Any size |

### Skill Anatomy

```
skill-name/
├── SKILL.md           # Core guidance (< 15 KB)
│   ├── Triggers       # When to load
│   ├── Quick tables   # Condensed reference
│   ├── Critical rules # Must-know items
│   └── Pointers       # Links to references
├── references/        # On-demand detail
│   ├── templates.md   # Detailed templates
│   ├── patterns.md    # Code patterns
│   └── checklists.md  # Validation lists
└── README.md          # Skill documentation
```

### What Goes Where

| In SKILL.md | In references/ |
|-------------|----------------|
| Trigger phrases | Full code templates |
| Decision tables | Extended examples |
| Critical rules (condensed) | Audit checklists with grep commands |
| Error quick-fix table | Detailed error documentation |
| Process overview | Step-by-step procedures |
| Pointers to references | CSS/script templates |

---

## Ecosystem Architecture

### Orchestrator Pattern

For multi-skill ecosystems, create a lightweight orchestrator:

```
ecosystem/
├── orchestrator/SKILL.md    # ~4-8 KB, always loaded first
├── skill-a/SKILL.md         # Phase/domain specific
├── skill-b/SKILL.md         # Phase/domain specific
└── skill-c/SKILL.md         # Phase/domain specific
```

**Orchestrator responsibilities:**
- Detect which skill to load from prompt
- Manage phase transitions
- Track project state
- Enforce exit gates between phases

### Skill Loading Rules

```
1. User prompt arrives
2. Orchestrator detects phase/intent
3. Load ONLY relevant skill(s)
4. Work with loaded skill
5. Load references ONLY when needed
6. Update state for next session
```

---

## Error-Driven Improvement

### Improvement Triggers

**Load this skill when you see:**

| Trigger | Action |
|---------|--------|
| User uploads ERROR-AND-FIXES-LOG.md | Extract patterns → Update skills |
| Same error occurs twice | Add to skill's error table |
| Validation step fails repeatedly | Add prevention to checklist |
| User says "the skill missed X" | Add X to skill coverage |
| Skill file exceeds 15 KB | Refactor to references |

### Error Integration Process

```
ERROR-AND-FIXES-LOG.md
        │
        ▼
┌─────────────────────┐
│ Extract Pattern     │
│ - Root cause        │
│ - Prevention        │
│ - Skill gap         │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ Categorize          │
│ - Which skill?      │
│ - Quick fix or deep?│
│ - New or existing?  │
└─────────────────────┘
        │
        ├─── Quick fix ──→ Add to error table in SKILL.md
        │                  (parallel if multiple skills)
        │
        └─── Deep pattern ──→ Add to references/*.md
                              (parallel if multiple skills)
```

**For multiple skills:** Use parallel execution (6x faster)
- 20 skills updated in 5m vs 30m sequential
- Launch one Task per skill in single message
- See `references/parallel-operations.md` Pattern 4

### Error Table Format (for SKILL.md)

Keep condensed in main skill:

```markdown
| Error | Cause | Fix |
|-------|-------|-----|
| [symptom] | [root cause] | [one-line fix] |
```

### Detailed Error Format (for references)

Full documentation in reference file:

```markdown
### Error N: [Title]
**Error**: [message]
**Symptoms**: [list]
**Root Cause**: [explanation]
**Fix**: [detailed steps]
**Prevention**: [checklist item]
**Added to skill**: [date]
```

---

## Skill Creation Checklist

Before creating a new skill:

- [ ] Is this a repeatable workflow? (not one-off)
- [ ] Will it be used across multiple projects?
- [ ] Can it fit in < 15 KB? (or needs references)
- [ ] Does it overlap with existing skills?
- [ ] What triggers should load it?
- [ ] **v4.1:** Does it need parallelization? (Use decision framework above)
- [ ] **v4.1:** Which parallelization pattern applies? (If parallelized)
- [ ] **v4.1:** Document why parallelization included/excluded

**For detailed templates and procedures:**
```
references/skill-templates.md (includes v4.1 template)
references/parallelization-decision-guide.md (decision trees)
```

---

## Skill Maintenance Checklist

Periodic review:

- [ ] Any skill over 15 KB? → Refactor to references (use parallel for multiple)
- [ ] New errors logged? → Integrate learnings (parallel across affected skills)
- [ ] User complaints? → Address gaps
- [ ] Overlapping content? → Consolidate
- [ ] Outdated patterns? → Update (parallel for multiple skills)

**For maintenance procedures:**
```
references/maintenance.md
```

**For parallel execution patterns:**
```
references/parallel-operations.md
```

---

## Quick Reference: Skill Sizing

| Skill Size | Action |
|------------|--------|
| < 10 KB | Ideal - room to grow |
| 10-15 KB | Good - monitor growth |
| 15-20 KB | Warning - plan refactor |
| > 20 KB | Refactor now - move detail to references |

---

## Cross-Skill Validation

When skills work together:

1. **Exit gates** - Each skill defines completion criteria
2. **Handoff data** - What transfers between skills
3. **Validation points** - Cross-check consistency
4. **State file** - Track progress across sessions

**Validate multiple skills concurrently:**
- Launch one validation Task per skill
- Aggregate results across all validators
- 9.3x speedup for 10 skills (45s vs 7m)
- See `references/parallel-operations.md` Pattern 1

---

## Performance Comparison

| Operation | Sequential | Parallel | Improvement |
|-----------|-----------|----------|-------------|
| Validate 30 skills | 21m | 51s | 25x faster |
| Create audit suite (5) | 8m | 2m | 4x faster |
| Refactor oversized (15) | 45m | 8m | 5.6x faster |
| Integrate errors (20) | 30m | 5m | 6x faster |
| Quality check ecosystem | 25m | 4m | 6.3x faster |

**Rule:** Always use parallel execution for multi-skill operations.

---

*End of Skill Ecosystem Manager*
