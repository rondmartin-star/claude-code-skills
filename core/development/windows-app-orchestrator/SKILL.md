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
| "UI design", "pages", "screens", "workflows", "logo" | windows-app-ui-design |
| "generate UI", "create components", "Svelte", "design system" | ui-generation-orchestrator |
| "code", "implement", "fix", "bug", "package" | windows-app-build |
| "debug UI", "Playwright", "test UI", "pixel perfect" | windows-app-ui-testing |
| "test strategy", "coverage gaps", "test plan", "convergence" | windows-app-testing-strategy |
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
"/mnt/skills/user/windows-app-requirements/SKILL.md"         # ~8 KB
"/mnt/skills/user/windows-app-ui-design/SKILL.md"            # ~10 KB
"/mnt/skills/user/windows-app-system-design/SKILL.md"        # ~12 KB
"/mnt/skills/user/windows-app-build/SKILL.md"                # ~25 KB
"/mnt/skills/user/windows-app-ui-testing/SKILL.md"           # ~14 KB (Playwright)
"/mnt/skills/user/windows-app-testing-strategy/SKILL.md"     # ~14 KB (Convergence)

# UI Generation Skills (load when generating components)
"/mnt/skills/core/development/ui-generation-orchestrator/SKILL.md"    # ~12 KB
"/mnt/skills/core/development/svelte-component-generator/SKILL.md"    # ~12 KB
"/mnt/skills/core/development/design-system-manager/SKILL.md"         # ~10 KB

# Specialized Skills (load alongside build when relevant)
"/mnt/skills/user/authentication-patterns/SKILL.md"          # ~4 KB
"/mnt/skills/user/secure-coding-patterns/SKILL.md"           # ~10 KB
"/mnt/skills/user/windows-app-supervision/SKILL.md"          # ~8 KB
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

### windows-app-ui-testing
**Load when user says:**
- "Debug the UI" / "UI not matching design"
- "Pixel perfect" / "Fine-tune layout"
- "Test the interface" / "E2E tests"
- "Use Playwright" / "Open in browser"
- "Visual regression" / "Screenshot testing"

**Do NOT load when:** No UI implementation exists yet

**Key Insight:** Claude Code is bad at pixel-perfect UI when looking at code. Use Playwright to view the **rendered page** instead.

**Visual Iteration Workflow:**
```
"Spin out Playwright browser, open localhost and I'll guide you
from there in terms of UI improvements."
```

This workflow:
- Views rendered page (not code)
- Provides visual context
- Enables pixel-perfect iteration
- Catches layout issues invisible in code

### windows-app-testing-strategy
**Load when user says:**
- "Create test strategy" / "Test coverage plan"
- "Identify coverage gaps" / "Find untested code"
- "Improve test quality" / "Test convergence"
- "Parallel test execution" / "Speed up tests"
- "Test automation" / "CI/CD testing"

**Do NOT load when:** Writing individual tests (use windows-app-ui-testing)

**Key Features:**
- **Multi-methodology convergence:** 3 consecutive clean passes
- **Parallel execution:** 67% faster (120s → 40s)
- **Learning integration:** verify-evidence, detect-infinite-loop, error-reflection
- **Context optimization:** 69% token reduction
- **Automated gap detection:** Priority-based coverage analysis

**Proven Results:** Operations Hub test strategy
- 7 orthogonal methodologies
- Dependency-aware parallelization
- Pattern library for compound learning

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

## Troubleshooting Blockers: Three Strikes Rule

**Purpose:** Recognize hard blockers early to prevent wasted time on impossible workarounds

**The Problem:**
When encountering deployment blockers (permission errors, file locks, etc.), it's easy to spend 60+ minutes attempting 10+ different workarounds that all fail for the same root cause.

**The Solution: Three Strikes Rule**

```
Blocker encountered
    ↓
Try workaround #1
    ↓
Failed? → Try workaround #2
    ↓
Failed? → STOP and analyze
    ↓
Is this solvable without user action?
    ↓
YES → Try one more targeted approach
NO  → Document blocker, request user action, WAIT
```

### Blocker Type Recognition

After 2-3 failed attempts (10 minutes max), categorize the blocker:

| Blocker Type | Characteristics | Time Limit | Resolution |
|--------------|----------------|------------|------------|
| **Permission** | "Access denied" errors | 1-2 attempts | User action required |
| **File Lock** | "In use by another process" | 2-3 attempts | Kill process or reboot |
| **Configuration** | Settings mismatch | 15-30 min | Code change |
| **Environment** | System-level issue | Recognize immediately | System change or user action |
| **Logic** | Code bug | No limit | Fix and test |

### Hard Blocker Decision Tree

**After 2nd failed workaround:**

1. **Analyze WHY it failed:**
   - Permission issue → Requires elevated access
   - File lock issue → Requires process termination
   - Configuration issue → Requires code change
   - Environment issue → Requires system change

2. **Check if root cause category changed:**
   - Same category? → STOP, request user action
   - Different category? → One more targeted attempt

3. **Avoid circular troubleshooting:**
   - DO NOT try different ports if database is locked (same DB = same lock)
   - DO NOT try to delete files in use (will always fail)
   - DO NOT repeat kill commands with different flags (permission is permission)

### Communication Pattern During Troubleshooting

**DO NOT provide running commentary of each attempt.**

Instead:
1. **First message:** "Investigating [issue]. Will update when resolved or blocked."
2. **Investigation:** Work silently through diagnostic tree (2-3 attempts max)
3. **Blocker hit:** "Found blocker: [description]. Need you to: [specific action]"
4. **Resolution:** "Fixed. Here's what happened and what I changed."

### Example: Database Lock Blocker

**Wrong Approach (60 minutes wasted):**
1. Try `taskkill /F /PID` → Access denied
2. Try `WMIC process` → Access denied
3. Try different port → Same database = same lock
4. Try to delete WAL files → In use
5. Try to rename WAL files → In use
6. Try checkpoint WAL → Lock returns
7. Try disable app initialization → Still needs DB
8. Try skip migrations → Can't skip
9. Try simple WSGI → Same django.setup()
10. Try 5+ more workarounds... (all fail)

**Correct Approach (5 minutes):**
1. Try `taskkill /F /PID` → Access denied (Attempt 1)
2. Try `WMIC process` → Access denied (Attempt 2)
3. **STOP** - Recognize as **permission-based blocker**
4. Provide clear user action:
   ```
   HARD BLOCKER: Zombie process requires manual termination

   ACTION REQUIRED:
   1. Open Task Manager (Ctrl+Shift+Esc)
   2. Find Python process PID 330108
   3. Right-click → End Task
   4. Restart server

   This cannot be automated due to Windows process permissions.
   ```

### Windows-Specific Gotchas

**Remember these Windows behaviors:**
- File locking is more aggressive than Unix
- Process permissions are more complex (SYSTEM vs User vs Admin)
- `taskkill` has different permissions than Task Manager
- Task Manager has elevated privileges that CLI doesn't
- SQLite WAL mode creates persistent shared memory locks

### Success Metrics

**Green Flags (Keep Doing):**
- ✓ Recognize blocker type after 2-3 attempts
- ✓ Stop when root cause category doesn't change
- ✓ Provide clear user action instead of continuing
- ✓ Silent investigation with clear results

**Red Flags (Stop Doing):**
- ✗ Persisting past 3 failures in same category
- ✗ Not recognizing permission-based blockers
- ✗ Attempting same category of solution repeatedly
- ✗ Excessive status updates during debugging

### Time Impact

**Example from Operations Hub v0.6.0 deployment:**
- OAuth debugging: 45 min ✓ (appropriate)
- Zombie process identification: 10 min ✓ (appropriate)
- Failed workaround attempts: 60 min ✗ (wasted)
- **Efficiency loss:** 42% of time on impossible workarounds

**With Three Strikes Rule:**
- OAuth debugging: 45 min
- Zombie process identification: 10 min
- Failed workaround attempts: 5 min ✓ (stopped early)
- **Total time saved:** 55 minutes

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
