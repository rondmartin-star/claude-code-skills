# Skill Templates Reference

Load this file when creating new skills or restructuring existing ones.

---

## SKILL.md Template

```markdown
---
name: [skill-name]
description: >
  [One paragraph describing what this skill does and when to use it.
  Include 2-3 trigger phrases. Keep under 280 characters.]
---

# [Skill Name]

**Purpose:** [One line]  
**Size:** ~[N] KB (references: ~[N] KB)  
**Related Skills:** [list or "none"]

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "[phrase 1]"
- "[phrase 2]"
- "[phrase 3]"

**Context Indicators:**
- [indicator 1]
- [indicator 2]

## ❌ DO NOT LOAD WHEN

- [anti-trigger 1]
- [anti-trigger 2]

---

## [Main Content Sections]

[Keep each section focused. Use tables for quick reference.]

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| data | data | data |

---

## Common Errors Quick Fix

| Error | Cause | Fix |
|-------|-------|-----|
| [error] | [cause] | [fix] |

---

## [Phase/Process] Checklist

Before proceeding:

- [ ] [item 1]
- [ ] [item 2]
- [ ] [item 3]

**For detailed [templates/patterns/examples]:**
\`\`\`
/mnt/skills/user/[skill-name]/references/[file].md
\`\`\`

---

*End of [Skill Name]*
```

---

## README.md Template

```markdown
# [Skill Name]

[One paragraph description of the skill's purpose and value.]

## Purpose

[Expanded description of what problems this skill solves.]

## When to Use

| Scenario | Use This Skill? |
|----------|-----------------|
| [scenario 1] | Yes |
| [scenario 2] | Yes |
| [scenario 3] | No - use [other skill] |

## Structure

\`\`\`
[skill-name]/
├── SKILL.md              # Core guidance (~[N] KB)
├── references/
│   └── [file].md         # [Description] (~[N] KB)
└── README.md             # This file
\`\`\`

## Related Skills

- **[skill-a]**: [relationship]
- **[skill-b]**: [relationship]

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | YYYY-MM-DD | Initial release |
```

---

## Reference File Template

```markdown
# [Topic] Reference

Load this file when [specific situation requiring detailed guidance].

---

## [Section 1]

[Detailed content, templates, or examples]

### [Subsection]

\`\`\`[language]
[code template or example]
\`\`\`

---

## [Section 2]

[More detailed content]

---

*End of [Topic] Reference*
```

---

## Orchestrator SKILL.md Template

```markdown
---
name: [ecosystem]-orchestrator
description: >
  ALWAYS LOAD THIS SKILL FIRST for [domain] work. Lightweight orchestrator
  (~[N]KB) that determines which specialized skills to load based on context.
  Manages project state, phase transitions, and skill coordination.
---

# [Ecosystem] Orchestrator

**Purpose:** Coordinate skill loading to minimize context usage  
**Size:** ~[N] KB (intentionally minimal)  
**Action:** Detect context → Load only needed skill(s) → Work → Update state

---

## How This Works

\`\`\`
USER PROMPT
    │
    ▼
ORCHESTRATOR (this skill, always loaded)
    │
    ▼
DETECT PHASE/MODE from prompt + state
    │
    ▼
LOAD ONLY the skill(s) needed
\`\`\`

---

## Skill Detection Rules

### Check for Explicit Indicators

| If prompt contains... | Load skill... |
|-----------------------|---------------|
| "[keywords]" | [skill-a] |
| "[keywords]" | [skill-b] |
| "[keywords]" | [skill-c] |

### Check for Project State

If state file provided, read `recommended_skill` field.

### When Uncertain

Ask the user which phase they're in.

---

## Skill Loading Paths

\`\`\`python
"/mnt/skills/user/[ecosystem]-[skill-a]/SKILL.md"
"/mnt/skills/user/[ecosystem]-[skill-b]/SKILL.md"
"/mnt/skills/user/[ecosystem]-[skill-c]/SKILL.md"
\`\`\`

**Rules:**
- Load at most 2 skills per prompt
- Never load all skills simultaneously
- Load references only when needed

---

## Phase Transitions

### [Phase A] → [Phase B]

**Exit Gate ([Phase A]):**
- [ ] [criterion 1]
- [ ] [criterion 2]

**Transition:** When user confirms, load [skill-b].

---

## Project State Template

\`\`\`yaml
project:
  name: "[Name]"
  version: "X.Y.Z"

current_phase: "[phase]"
completed_phases:
  phase_a: true|false
  phase_b: true|false

last_session:
  date: "YYYY-MM-DD"
  skill_used: "[skill]"
  summary: "[what was done]"

next_session:
  recommended_skill: "[skill]"
  focus: "[what to work on]"
\`\`\`

---

*End of [Ecosystem] Orchestrator*
```

---

## Ecosystem README.md Template

```markdown
# [Ecosystem Name] Skills

**Refactored from:** [original source] ([N] KB)  
**Total Size:** ~[N] KB combined ([N]% reduction)  
**Version:** [X.Y]

---

## Quick Start

**Always load the orchestrator first:**
\`\`\`
/mnt/skills/user/[ecosystem]-orchestrator/SKILL.md
\`\`\`

The orchestrator will determine which specialized skill to load.

---

## Skill Packages Overview

| Skill | Purpose | Size | When Loaded |
|-------|---------|------|-------------|
| **orchestrator** | Coordinate loading | ~[N] KB | **ALWAYS FIRST** |
| **[skill-a]** | [purpose] | ~[N] KB | "[trigger]" |
| **[skill-b]** | [purpose] | ~[N] KB | "[trigger]" |

---

## Context Budget

| Scenario | Skills Loaded | Approx Size |
|----------|---------------|-------------|
| [scenario 1] | orchestrator + [skill] | ~[N] KB |
| [scenario 2] | orchestrator + [skill] | ~[N] KB |
| **Loading everything** | all skills + refs | **~[N] KB** |

---

## Development Workflow

\`\`\`
[Phase A] → [Phase B] → [Phase C] → [Phase D]
    │           │            │           │
 [skill-a]  [skill-b]    [skill-c]   [skill-d]
\`\`\`

---

## Installation

Copy skill folders to:
\`\`\`
/mnt/skills/user/
├── [ecosystem]-orchestrator/
├── [ecosystem]-[skill-a]/
├── [ecosystem]-[skill-b]/
└── [ecosystem]-[skill-c]/
\`\`\`
```

---

## Description Field Best Practices

The YAML `description` field appears in skill listings. Make it count:

**Good:**
```yaml
description: >
  Create, maintain, and improve skill ecosystems. Covers skill design philosophy,
  ecosystem architecture, error-driven improvement, and continuous refinement.
  Use when: creating new skills, refactoring existing skills, improving skills
  based on logged errors, or managing multi-skill workflows.
```

**Bad:**
```yaml
description: A skill for managing skills.
```

**Formula:**
```
[What it does - 1 sentence]. [What it covers - list key areas].
Use when: [2-3 trigger scenarios].
```

---

*End of Skill Templates Reference*
