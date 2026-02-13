---
name: windows-app-orchestrator
description: >
  ALWAYS LOAD THIS SKILL FIRST for Windows application development. Lightweight
  orchestrator (~4KB) that determines which specialized skills to load based on
  context. Manages project state, phase transitions, and skill coordination.
  Triggers on: ANY Windows application development request.
---

# Windows Application Orchestrator

**Purpose:** Coordinate skill loading to minimize context usage
**Size:** ~12 KB (intentionally minimal)
**Action:** Detect context → Load only needed skill(s) → Work → Update state

---

## How This Works

```
┌─────────────────────────────────────────────────────────────────────────┐
│  USER PROMPT                                                             │
│       │                                                                  │
│       ▼                                                                  │
│  ┌─────────────────┐                                                    │
│  │  ORCHESTRATOR   │ ◄── Always loaded first (~4KB)                     │
│  │  (this skill)   │                                                    │
│  └────────┬────────┘                                                    │
│           │                                                              │
│           ▼                                                              │
│  ┌─────────────────┐     ┌─────────────────┐                           │
│  │ Detect Phase/   │────►│ Load ONLY the   │                           │
│  │ Mode from       │     │ skill(s) needed │                           │
│  │ prompt + state  │     │ for this prompt │                           │
│  └─────────────────┘     └─────────────────┘                           │
│                                   │                                      │
│           ┌───────────────────────┼───────────────────────┐             │
│           ▼                       ▼                       ▼             │
│  ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐       │
│  │  REQUIREMENTS   │   │  SYSTEM-DESIGN  │   │     BUILD       │       │
│  │    (~8 KB)      │   │    (~12 KB)     │   │    (~25 KB)     │       │
│  └─────────────────┘   └─────────────────┘   └─────────────────┘       │
│                                                                          │
│  TOTAL CONTEXT: Orchestrator + 1-2 skills = 16-37 KB                    │
│  vs. Loading everything = 63+ KB                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Detection Guide

**See `references/routing-rules.md` for complete detection rules**

### Primary Skill Triggers

| User says... | Load skill... |
|-------------|---------------|
| "requirements", "user stories", "what should it do" | windows-app-requirements |
| "data model", "database schema", "entities" | windows-app-system-design |
| "UI", "pages", "screens", "workflows", "logo" | windows-app-ui-design |
| "code", "implement", "fix", "bug", "package" | windows-app-build |
| "OAuth", "Google login", "authentication" | authentication-patterns |
| "security", "XSS", "SQL injection", "CSRF" | secure-coding-patterns |
| "auto-start", "supervisor", "watchdog", "MSI" | windows-app-supervision |

### When Uncertain

Ask the user to clarify their current phase:
1. Defining requirements (what the app should do)
2. Designing the system (data model, architecture)
3. Designing the UI (pages, workflows)
4. Building/fixing/packaging (implementation)

---

## Skill Loading Paths

```python
# Core Windows App Skills
"/mnt/skills/user/windows-app-requirements/SKILL.md"      # ~8 KB
"/mnt/skills/user/windows-app-ui-design/SKILL.md"         # ~10 KB
"/mnt/skills/user/windows-app-system-design/SKILL.md"     # ~12 KB
"/mnt/skills/user/windows-app-build/SKILL.md"             # ~25 KB

# Specialized Skills (load alongside build when relevant)
"/mnt/skills/user/authentication-patterns/SKILL.md"       # ~4 KB
"/mnt/skills/user/secure-coding-patterns/SKILL.md"        # ~10 KB
"/mnt/skills/user/windows-app-supervision/SKILL.md"       # ~8 KB
```

**Rules:**
- Load at most 2 skills per prompt (usually just 1)
- Never load all skills simultaneously
- Prefer the most specific skill for the task
- Keep total context under 35 KB

---

## Quick Reference: When to Load Each Skill

### windows-app-requirements
**Load when user says:**
- "I want to build an app that..."
- "What should the system do?"
- "Help me define requirements"
- "Write user stories"
- "What features do I need?"

**Do NOT load when:** User has existing code or package

### windows-app-ui-design
**Load when user says:**
- "Design the UI"
- "What pages do I need?"
- "Plan the screens"
- "Document user workflows"
- "How will users interact with..."
- "Create a brand language"
- "Here's our logo"

**Do NOT load when:** Data model not yet defined

**Note:** This skill requests the organization's logo to establish brand colors, typography, and component styling. If no logo is available, a neutral palette is used.

### windows-app-system-design
**Load when user says:**
- "Design the data model"
- "Plan the architecture"
- "What entities do I need?"
- "How should I structure the database?"
- "Choose technologies"

**Do NOT load when:** Requirements not yet defined

### windows-app-build
**Load when user says:**
- "Start coding" / "Implement this"
- "Fix this bug" / "Something is broken"
- "Create the package" / "Ready to deliver"
- "Run tests" / "Validate the package"
- References specific files or code

**Do NOT load when:** No design work has been done

### windows-app-supervision (Process Management + MSI)
**Load when user says:**
- "Auto-start on boot" / "Start on reboot"
- "Add health checks" / "Watchdog"
- "Supervisor" / "Process manager" / "Daemon"
- "Build MSI" / "Create installer" / "WiX"
- "Restart on file change" / "Hot reload"

**Do NOT load when:** No working application yet

---

## Project State Management

**See `references/state-management.md` for:**
- Complete APP-STATE.yaml template
- Phase transition gates
- Automatic quality checks
- Session management

**Quick Start:**
1. Upload APP-STATE.yaml at session start
2. Orchestrator reads recommended_skill field
3. Load that skill automatically
4. Update state at session end

---

## Parallel Orchestration (v4.1)

**Performance Enhancement:** Run orchestration operations in parallel for 3-8x speedup

### When to Use Parallel Execution

**Quality Gates (4.7x faster):**
```
Run 5 checks in parallel (45s vs 3m 30s):
- Security audit
- Type checking
- Unit tests
- Integration tests
- Code linting
```

**Pre-Deployment (4.8x faster):**
```
Run 7 validations in parallel (1m 15s vs 6m):
- File existence
- Configuration validation
- Documentation check
- Forbidden files check
- Installation test
- Health check
- Cross-skill validation
```

**Multi-Skill Loading (4x faster):**
```
Load 3 skills in parallel (30s vs 2m):
- windows-app-build
- secure-coding-patterns
- authentication-patterns
```

### Example: Parallel Quality Gate

Before SHIP mode or after major changes:

```bash
# Launch 5 quality checks in single message
Task 1: Security audit (42s)
Task 2: Type checking (38s)
Task 3: Unit tests (45s)
Task 4: Integration tests (28s)
Task 5: Code linting (35s)

Total: 45s (slowest task)
Sequential: 3m 30s
Speedup: 4.7x
```

### Complete Patterns

See `references/parallel-orchestration.md` for:
- Parallel quality gate implementation
- Pre-deployment parallel validation
- Multi-skill coordination
- State operations parallelization
- Reference file concurrent loading
- Sub-agent coordination
- Performance metrics and optimization
- Error handling strategies

---

## Error Recovery

If the wrong skill was loaded or context is getting large:

1. **Note current progress** in state file
2. **Complete current task** if possible
3. **For next prompt**, explicitly state which skill is needed
4. **User can say:** "Just use the [skill-name] skill for this"

---

## Commands for Claude

When processing a Windows app development request:

```
1. READ this orchestrator skill (you're doing this now)
2. DETECT which phase/skill is needed (use Quick Detection Guide)
3. LOAD only that skill
4. WORK using the loaded skill's guidance
5. UPDATE state file at session end
6. RECOMMEND next skill for future sessions
```

**Context Budget:**
- Orchestrator: ~12 KB (always loaded)
- One skill: 8-25 KB
- Working space: Remaining context
- Target: Keep skill content under 35 KB total

---

## References

**Complete guides:**
1. **routing-rules.md** - Detailed detection rules and multi-skill scenarios
2. **state-management.md** - Phase transitions, state templates, quality gates
3. **parallel-orchestration.md** - Parallel execution patterns (v4.1, saves 60-70% time)

**Related Skills:**
- `windows-app-build` - Build, test, and package operations
- `audit-orchestrator` - Multi-audit parallel execution
- `skill-ecosystem-manager` - Parallel skill management

---

*End of Windows Application Orchestrator Skill*
