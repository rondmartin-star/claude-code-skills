---
name: conversation-snapshot
description: >
  Create portable snapshots of chats or entire projects for seamless continuation
  in new contexts. Captures state, outputs, decisions, and learnings. Use when:
  approaching context limits, completing a work phase, archiving progress, or
  preparing to continue work in a new chat or project.
---

# Conversation Snapshot

**Purpose:** Preserve and transfer conversation/project state  
**Size:** ~8 KB (references: ~12 KB)  
**Output:** Portable package for seamless continuation

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Create a snapshot"
- "Save this conversation"
- "Package this chat for continuation"
- "Archive this project"
- "Prepare handoff package"
- "Context is getting long"
- "Before we hit the limit"

**Context Indicators:**
- Conversation approaching context limits
- Completing a major work phase
- Need to continue in new chat/project
- Archiving work for future reference
- Multiple files created that need preservation

## ❌ DO NOT LOAD WHEN

- Just starting a conversation
- Simple Q&A with no state to preserve
- No outputs or decisions to capture

---

## Core Principle: Distill Everything

**Snapshots must be lean.** Every byte counts when uploading to project knowledge or continuing in a new chat.

### Distillation Rules

| Instead of... | Write... |
|---------------|----------|
| Verbose explanations | Bullet points or tables |
| Full conversation replay | Key outcomes only |
| Every decision discussed | Only decisions that affect continuation |
| Complete error traces | Error → Cause → Fix → Prevention (one line each) |
| "We discussed X and decided Y because Z and W" | "**X:** Y (Z)" |

### What to Include

| Include | Exclude |
|---------|---------|
| Final decisions | Decision-making process |
| Current state | Historical states |
| Actionable next steps | Completed steps (unless context needed) |
| Patterns/learnings that apply going forward | One-time fixes |
| Files needed for continuation | Superseded file versions |
| Errors likely to recur | Errors already prevented |

### Size Targets

| Document | Target | Max |
|----------|--------|-----|
| SNAPSHOT.md (chat) | < 3 KB | 5 KB |
| CONTINUATION-PROMPT.md | < 1 KB | 2 KB |
| PROJECT-CONTEXT.md | < 2 KB | 4 KB |
| CONSOLIDATED-LEARNINGS.md | < 2 KB | 3 KB |
| ERROR-PREVENTION.md | < 1 KB | 2 KB |
| CURRENT-STATE.md | < 1 KB | 2 KB |
| OPEN-ITEMS.md | < 1 KB | 2 KB |

**Total project snapshot knowledge files: < 8 KB target**

---

## Snapshot Naming Convention

### Format

```
[type]-[scope]-[identifier]-[julian]-[time].zip
```

| Component | Description | Example |
|-----------|-------------|---------|
| **type** | `chat` or `project` | `chat` |
| **scope** | Project name (kebab-case) or `standalone` | `worship-av` |
| **identifier** | Chat topic or milestone (kebab-case, max 30 chars) | `vmix-integration` |
| **julian** | YYDDD (2-digit year + day of year) | `25366` (Dec 31, 2025) |
| **time** | HHMM (24-hour) | `1430` |

### Examples

**Chat Snapshots:**
```
chat-worship-av-vmix-integration-25366-1430.zip
chat-worship-av-ui-redesign-26002-0915.zip
chat-standalone-tax-analysis-26003-1100.zip
```

**Project Snapshots:**
```
project-worship-av-v1-complete-25366-2200.zip
project-skills-ecosystem-phase2-26003-1545.zip
```

### Julian Date Reference

| Month | Day 1 | Day 15 | Day 28/30/31 |
|-------|-------|--------|--------------|
| Jan | 001 | 015 | 031 |
| Feb | 032 | 046 | 059 |
| Mar | 060 | 074 | 090 |
| Apr | 091 | 105 | 120 |
| May | 121 | 135 | 151 |
| Jun | 152 | 166 | 181 |
| Jul | 182 | 196 | 212 |
| Aug | 213 | 227 | 243 |
| Sep | 244 | 258 | 273 |
| Oct | 274 | 288 | 304 |
| Nov | 305 | 319 | 334 |
| Dec | 335 | 349 | 365 |

*Add 1 to dates after Feb 28 in leap years*

### Naming Rules

1. **All lowercase** - No mixed case
2. **Kebab-case** - Use hyphens, not underscores or spaces
3. **Max 30 chars** for identifier - Truncate if longer
4. **No special characters** - Only a-z, 0-9, hyphens
5. **Standalone** - Use when chat is outside any project

---

## Snapshot Types

| Type | Scope | Use Case | Continuation |
|------|-------|----------|--------------|
| **Chat Snapshot** | Single conversation | Context limit, phase complete | New chat, same project |
| **Project Snapshot** | All project chats | Project complete, migration | New project |

---

## Chat Snapshot Process

### Step 1: Extract (Don't Summarize)

| Extract | Format |
|---------|--------|
| Purpose | 1 sentence |
| Decisions | Table: Decision \| Choice \| Why |
| Outputs | Table: File \| Status |
| Learnings | Bullets: [Learning]: [use] |
| Errors | Table: Error \| Fix \| Prevent |
| Open items | Q/I/T lists |
| Next steps | Numbered priorities |

### Step 2: Distill

Ask for each item: **"Does this affect continuation?"**
- Yes → Include (condensed)
- No → Exclude

### Step 3: Format

- Tables over prose
- One line per item
- No redundancy
- Target: SNAPSHOT.md < 3 KB

### Step 4: Package

```
chat-[project]-[id]-[YYDDD]-[HHMM]/
├── SNAPSHOT.md          # < 3 KB
├── CONTINUATION-PROMPT.md # < 1 KB
└── outputs/
```

---

## Project Snapshot Process

### Step 1: Enumerate Chats

Use `recent_chats` tool to list all project conversations.

### Step 2: Extract & Deduplicate

From all chats, extract:
- Decisions (keep latest if evolved)
- Learnings (merge similar)
- Errors (combine into prevention guide)
- Final outputs only

### Step 3: Distill to Targets

| File | Target | Contains |
|------|--------|----------|
| PROJECT-CONTEXT.md | < 2 KB | Purpose, decisions, architecture |
| CONSOLIDATED-LEARNINGS.md | < 2 KB | Patterns, do/don't |
| ERROR-PREVENTION.md | < 1 KB | Errors, checks |
| CURRENT-STATE.md | < 1 KB | Progress, blockers |
| OPEN-ITEMS.md | < 1 KB | Q/I/T, decisions needed |
| **Total Knowledge** | **< 8 KB** | |

### Step 4: Package

```
project-[name]-[milestone]-[YYDDD]-[HHMM]/
├── 1-UPLOAD-TO-PROJECT-KNOWLEDGE/  # < 8 KB total
├── 2-SET-PROJECT-INSTRUCTIONS/
├── 3-USE-IN-FIRST-CHAT/
├── 4-REFERENCE-OUTPUTS/
├── 5-ARCHIVE/
└── README.md
```

---

## Snapshot Document Structure

### SNAPSHOT.md Contents

| Section | Content |
|---------|---------|
| Header | Generated date, project, reason |
| Summary | Goal, accomplishments, state |
| Decisions | Table with rationale |
| Outputs | Files with status |
| Learnings | Patterns discovered |
| Errors | Fixed issues + prevention |
| Open Items | Questions, issues, tasks |
| Next Steps | Prioritized actions |
| Continuation | How to resume |

### CONTINUATION-PROMPT.md Contents

| Section | Content |
|---------|---------|
| Context | 2-3 sentence summary |
| Decisions | Do not revisit these |
| Files | What's attached |
| Next Steps | What to do first |

**For full templates:**
```
~/.claude/skills/meta/conversation-snapshot/references/templates.md
```

---

## Continuation Prompt Format

The `CONTINUATION-PROMPT.md` must be self-contained for copy-paste:

1. Brief context (2-3 sentences)
2. Key decisions (don't revisit)
3. Files to reference
4. Immediate next steps
5. Request to confirm and proceed

---

## When to Snapshot

| Trigger | Snapshot Type | Urgency |
|---------|---------------|---------|
| "Context getting long" warning | Chat | High |
| Major phase completed | Chat | Medium |
| Before risky operation | Chat | Medium |
| Project milestone reached | Project | Medium |
| Moving to new project | Project | High |
| Archiving completed work | Either | Low |

---

## Snapshot Checklist

Before finalizing:

- [ ] **Size check:** Each file under target?
- [ ] **Tables over prose:** Converted explanations to tables?
- [ ] **No redundancy:** Same info not in multiple files?
- [ ] **Continuation-only:** Excluded historical-only content?
- [ ] **Decisions condensed:** "[Topic]: [Choice] ([Why])" format?
- [ ] **Prompt standalone:** Works without reading other files?
- [ ] **Files listed:** All outputs accounted for?

---

## Package Structures

### Chat Snapshot
```
chat-[project]-[identifier]-[YYDDD]-[HHMM]/
├── SNAPSHOT.md
├── CONTINUATION-PROMPT.md
├── ERROR-AND-FIXES-LOG.md (if any)
└── outputs/
```

### Project Snapshot
```
project-[name]-[milestone]-[YYDDD]-[HHMM]/
├── 1-UPLOAD-TO-PROJECT-KNOWLEDGE/
│   ├── PROJECT-CONTEXT.md
│   ├── CONSOLIDATED-LEARNINGS.md
│   └── ERROR-PREVENTION.md
├── 2-SET-PROJECT-INSTRUCTIONS/
│   └── instructions.md
├── 3-USE-IN-FIRST-CHAT/
│   ├── CONTINUATION-PROMPT.md
│   ├── CURRENT-STATE.md
│   └── OPEN-ITEMS.md
├── 4-REFERENCE-OUTPUTS/
├── 5-ARCHIVE/
│   ├── CHAT-SUMMARIES.md
│   └── FULL-SNAPSHOT.md
└── README.md
```

**For document templates:**
```
~/.claude/skills/meta/conversation-snapshot/references/templates.md
```

---

## Integration with Skills

If project uses skill ecosystem:

1. **Note active skills** in snapshot
2. **Include skill state files** (e.g., APP-STATE.yaml)
3. **Reference skill versions** used
4. **Capture skill-specific learnings** for feedback

---

*End of Conversation Snapshot Skill*
