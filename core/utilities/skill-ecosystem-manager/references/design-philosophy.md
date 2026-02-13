# Skill Design Philosophy Reference

Load this file when making architectural decisions about skill ecosystems.

---

## Core Principles

### 1. Context is Precious

Every byte loaded into context reduces working space. Skills must earn their context usage.

**Implications:**
- Keep SKILL.md files small (< 15 KB)
- Load only what's needed for current task
- Move rarely-used content to references
- Orchestrators are intentionally minimal

### 2. Triggers Over Documentation

A skill that can't be found is useless. Clear triggers matter more than comprehensive docs.

**Implications:**
- Lead with trigger phrases
- Use explicit "LOAD WHEN" sections
- Include "DO NOT LOAD WHEN" anti-triggers
- Make triggers match natural user language

### 3. Tables Over Prose

Scannable tables beat paragraphs for quick reference.

**Good:**
```markdown
| Error | Cause | Fix |
|-------|-------|-----|
| 500 on save | Missing FK | Add venue_id |
```

**Bad:**
```markdown
When you encounter a 500 error while saving, this is typically
caused by a missing foreign key. To fix this, you should add
the venue_id field to your model...
```

### 4. Pointers Over Duplication

Reference other skills/files rather than duplicating content.

**Good:**
```markdown
**For detailed templates:**
/mnt/skills/user/skill-name/references/templates.md
```

**Bad:**
[Same 50-line template repeated in three skills]

### 5. Error-Driven Evolution

Skills improve through real-world usage, not speculation.

**Implications:**
- Start minimal, add based on actual errors
- Document errors that occur
- Integrate learnings back into skills
- Remove patterns that never trigger

### 6. Robust and Fool-Proof

Applications built with these skills must be robust and as fool-proof as possible. Users may have no technical background - it just needs to work.

**Implications:**
- Anticipate user mistakes and handle them gracefully
- Provide clear error messages with actionable guidance
- Use sensible defaults that work out of the box
- Auto-detect and auto-configure when possible
- Never assume technical knowledge from the user
- Test with non-technical users before delivery
- If something can fail silently, make it fail loudly instead

---

## Structural Patterns

### The 15KB Threshold

Why 15 KB for SKILL.md?

| Context Budget | Allocation |
|----------------|------------|
| ~100 KB | Typical working context |
| ~30 KB | System prompt + tools |
| ~20 KB | User conversation |
| ~15 KB | Skill guidance |
| ~35 KB | Working space for task |

At 15 KB per skill:
- 2 skills = 30 KB (comfortable)
- 3 skills = 45 KB (tight)
- 4+ skills = cramped

### Reference File Strategy

| Reference Type | When to Load |
|----------------|--------------|
| Templates | Creating new files |
| Patterns | Debugging specific issues |
| Checklists | Running audits |
| Examples | Learning new concepts |

**Key insight:** Most prompts need guidance, not templates. Keep guidance in SKILL.md, templates in references.

### Orchestrator Minimalism

Orchestrators should be:
- < 8 KB ideally
- Detection rules only
- No detailed procedures
- Fast to scan

**Orchestrator responsibilities:**
- ✓ Detect which skill to load
- ✓ Track phase/state
- ✓ Enforce transitions
- ✗ Contain domain knowledge
- ✗ Include detailed procedures

---

## Trigger Design

### Effective Triggers

Triggers should match how users naturally ask:

| Natural Language | Trigger |
|------------------|---------|
| "I want to build an app that..." | requirements skill |
| "Design the database" | system-design skill |
| "Fix this bug" | build skill |
| "Create a presentation" | pptx skill |

### Trigger Hierarchy

```
1. Explicit keywords: "requirements", "data model", "package"
2. Intent phrases: "I want to...", "help me..."
3. Context clues: existing code mentioned, file uploads
4. State file: recommended_skill field
5. Ask user: when uncertain
```

### Anti-Triggers

Equally important - when NOT to load:

```markdown
## ❌ DO NOT LOAD WHEN

- User has existing code (use build skill)
- User asking about unrelated topic
- Another skill explicitly requested
```

---

## Content Organization

### SKILL.md Structure

```
1. YAML frontmatter (name, description)
2. Title + metadata line
3. Trigger section (LOAD WHEN / DO NOT LOAD)
4. Core content (tables, rules, process)
5. Quick-fix error table
6. Checklist(s)
7. Pointers to references
```

### Reference File Structure

```
1. Title + load condition
2. Detailed content sections
3. Full templates
4. Extended examples
5. Complete checklists
```

### Cross-Skill References

When skills relate:

```markdown
**Related Skills:**
- [skill-a]: Use for [situation]
- [skill-b]: Handles [related topic]

**See also:**
/mnt/skills/user/[skill]/SKILL.md
```

---

## Ecosystem Patterns

### Linear Workflow

```
Phase A → Phase B → Phase C
   │          │          │
Skill A   Skill B    Skill C
```

- Each skill handles one phase
- Clear handoff points
- Orchestrator tracks progress

### Hub and Spoke

```
        ┌─── Skill B
        │
Skill A ├─── Skill C
(core)  │
        └─── Skill D
```

- Core skill always loaded
- Satellite skills for specific tasks
- No orchestrator needed

### Domain Grid

```
           Domain X    Domain Y    Domain Z
Phase 1   Skill X1    Skill Y1    Skill Z1
Phase 2   Skill X2    Skill Y2    Skill Z2
```

- Multiple orchestrators possible
- Skills can cross-reference
- Complex but powerful

---

## Quality Indicators

### Signs of a Good Skill

- [ ] SKILL.md < 15 KB
- [ ] Clear trigger phrases
- [ ] Tables for quick reference
- [ ] Pointers to details (not inline)
- [ ] Error table with real errors
- [ ] Actionable checklists
- [ ] README for documentation

### Signs of a Problem Skill

- [ ] SKILL.md > 20 KB → refactor
- [ ] No trigger section → add triggers
- [ ] Walls of prose → convert to tables
- [ ] Duplicated content → extract & reference
- [ ] No error table → add learnings
- [ ] Vague checklists → make specific
- [ ] No README → document

---

## Evolution Strategy

### Start Minimal

New skill should have:
1. Trigger section
2. Core guidance (1-2 pages)
3. One checklist
4. README

### Grow Through Usage

Add content when:
- Error occurs → add to error table
- User asks repeatedly → add guidance
- Pattern emerges → add to process

### Refactor When Needed

Split/consolidate when:
- Size exceeds threshold
- Natural boundaries emerge
- Usage patterns change

---

## Anti-Patterns

### Kitchen Sink Skill

**Problem:** One skill tries to cover everything  
**Solution:** Split into focused skills with orchestrator

### Template Dump

**Problem:** SKILL.md is 90% templates  
**Solution:** Move templates to references/

### Orphan References

**Problem:** References exist but SKILL.md doesn't point to them  
**Solution:** Add explicit pointers in SKILL.md

### Trigger Overlap

**Problem:** Multiple skills match same triggers  
**Solution:** Make triggers specific, use orchestrator

### Static Content

**Problem:** Skill never updated after creation  
**Solution:** Integrate learnings from usage

---

*End of Design Philosophy Reference*
