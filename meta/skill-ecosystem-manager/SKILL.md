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
        │
        └─── Deep pattern ──→ Add to references/*.md
```

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

**For detailed templates and procedures:**
```
~/.claude/skills/meta/skill-ecosystem-manager/references/skill-templates.md
```

---

## Skill Maintenance Checklist

Periodic review:

- [ ] Any skill over 15 KB? → Refactor to references
- [ ] New errors logged? → Integrate learnings
- [ ] User complaints? → Address gaps
- [ ] Overlapping content? → Consolidate
- [ ] Outdated patterns? → Update

**For maintenance procedures:**
```
~/.claude/skills/meta/skill-ecosystem-manager/references/maintenance.md
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

---

*End of Skill Ecosystem Manager*
