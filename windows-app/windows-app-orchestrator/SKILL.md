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
**Size:** ~4 KB (intentionally minimal)  
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

## Skill Detection Rules

### STEP 1: Check for Explicit Phase Indicators

| If prompt contains... | Load skill... |
|-----------------------|---------------|
| "requirements", "user stories", "what should it do" | requirements |
| "data model", "database schema", "entities" | system-design |
| "UI", "pages", "screens", "workflows", "navigation" | ui-design |
| "logo", "brand", "colors", "styling" | ui-design |
| "OAuth", "Google login", "authentication", "login page" | authentication-patterns |
| "HTTPS", "SSL", "Caddy", "production deployment" | build (HTTPS section) |
| "code", "implement", "fix", "bug", "package", "deliver" | build |
| "form", "file upload", "user input", "CSRF" | build + secure-coding-patterns |
| "security", "XSS", "SQL injection", "authentication" | build + secure-coding-patterns |
| "audit", "check consistency", "verify codebase" | codebase-audit |
| "bulletproof", "pre-commit", "CI/CD", "type checking" | bulletproof-codebase |
| "protect database", "backup verification", "error monitoring" | bulletproof-codebase |
| "auto-start", "boot", "reboot", "supervisor", "health check", "watchdog" | supervision |
| "MSI", "installer", "WiX", "build package", "create installer" | supervision (MSI section) |

### STEP 2: Check for Project State File

If user uploads or references a state file (e.g., `APP-STATE.yaml`):
- Read the `recommended_mode` field
- Load the appropriate skill for that mode

### STEP 3: Infer from Context

| Context Clues | Likely Phase | Load |
|---------------|--------------|------|
| No existing code mentioned | Early phase | requirements |
| Discussing "what" not "how" | Requirements | requirements |
| Discussing structure/architecture | Design | system-design |
| Discussing user interaction | UI Design | ui-design |
| Has existing package/baseline | Implementation | build |
| Mentions specific files/bugs | Fix mode | build |
| "Ready to deliver" | Ship mode | build |

### STEP 4: When Uncertain

Ask the user:
> "I want to load only the skills needed for this task. Are you:
> 1. Defining requirements (what the app should do)
> 2. Designing the system (data model, architecture)
> 3. Designing the UI (pages, workflows)
> 4. Building/fixing/packaging (implementation)
> 
> Or tell me what you're working on and I'll determine the right skill."

---

## Skill Loading Commands

When you determine which skill to load, use these paths:

```python
# Load ONE of these based on detected phase:
"~/.claude/skills/windows-app/windows-app-requirements/SKILL.md"      # ~8 KB
"~/.claude/skills/windows-app/windows-app-ui-design/SKILL.md"         # ~10 KB
"~/.claude/skills/windows-app/windows-app-system-design/SKILL.md"     # ~12 KB
"~/.claude/skills/windows-app/windows-app-build/SKILL.md"             # ~17 KB

# Specialized skills (load alongside build when relevant):
"~/.claude/skills/windows-app/security/security-patterns-orchestrator/SKILL.md"  # ~7 KB (routes to auth/secure)
"~/.claude/skills/windows-app/windows-app-supervision/SKILL.md"       # ~8 KB

# Quality & Protection skills (from plugins):
"~/.claude/plugins/codebase-audit/skills/codebase-audit/SKILL.md"              # ~12 KB
"~/.claude/plugins/bulletproof-codebase/skills/bulletproof-orchestrator/SKILL.md"  # ~8 KB
"~/.claude/plugins/bulletproof-codebase/skills/pre-commit-hooks/SKILL.md"      # ~6 KB
"~/.claude/plugins/bulletproof-codebase/skills/ci-cd-pipeline/SKILL.md"        # ~8 KB
"~/.claude/plugins/bulletproof-codebase/skills/type-checking/SKILL.md"         # ~8 KB
"~/.claude/plugins/bulletproof-codebase/skills/database-protection/SKILL.md"   # ~10 KB
"~/.claude/plugins/bulletproof-codebase/skills/error-monitoring/SKILL.md"      # ~12 KB

# Only load audit reference when running audits:
"~/.claude/skills/windows-app/windows-app-build/references/audit-checklists.md"  # ~18 KB
```

**Rules:**
- Load at most 2 skills per prompt (usually just 1)
- Never load all skills simultaneously
- Prefer the most specific skill for the task
- Load authentication-patterns WITH build when implementing OAuth

---

## Phase Transitions

### Requirements → System Design
**Exit Gate (Requirements):**
- [ ] Problem statement documented
- [ ] User roles defined with permissions
- [ ] All P0 user stories have acceptance criteria
- [ ] User approved requirements

**Transition:** When user confirms requirements, load system-design skill.

### System Design → UI Design
**Exit Gate (System Design):**
- [ ] All entities defined with attributes
- [ ] Relationships documented
- [ ] Technology stack selected
- [ ] User approved data model

**Transition:** When user confirms system design, load ui-design skill.

### UI Design → Build
**Exit Gate (UI Design):**
- [ ] Page inventory complete
- [ ] Role workflows documented
- [ ] Form specifications defined
- [ ] User approved UI design

**Transition:** When user confirms UI design, load build skill.

### Build Modes (Internal)
The build skill has its own modes (ADD/FIX/SHIP) - no skill transition needed.

---

## Automatic Quality Checks

### When to Auto-Run Audit

| Build Mode | Trigger | Audit Type |
|------------|---------|------------|
| ADD | After completing a feature | Quick (models + routes) |
| FIX | After applying a fix | Targeted (affected component) |
| SHIP | Before packaging | Full (all 5 components) |

### When to Suggest Bulletproof Setup

| Condition | Suggestion |
|-----------|------------|
| New project (no .pre-commit-config.yaml) | "Set up pre-commit hooks?" |
| No CI pipeline (.github/workflows/) | "Add CI/CD pipeline?" |
| No type checking (mypy.ini) | "Enable type checking?" |
| No backup scripts | "Add database protection?" |
| No health endpoint | "Add error monitoring?" |

### Automatic Actions

```
After Feature Completion (ADD Mode):
1. Run quick audit automatically
2. If issues found → report and offer to fix
3. If clean → continue

Before SHIP Mode:
1. Run full audit (all 5 agents in parallel)
2. Verify bulletproof setup exists
3. Run all tests
4. Generate audit report
5. Only proceed if all checks pass

After Bug Fix (FIX Mode):
1. Run targeted audit on affected files
2. Verify fix doesn't introduce new issues
3. Add regression test suggestion
```

---

## Project State Management

### State File Template

```yaml
# [APP-NAME]-STATE.yaml
# Upload this file at the start of each session

project:
  name: "[Application Name]"
  version: "X.Y.Z"
  build: "YYDDD-HHMM"

current_phase: "requirements|system-design|ui-design|build"
build_mode: "ADD|FIX|SHIP"  # Only if current_phase is "build"

completed_phases:
  requirements: true|false
  system_design: true|false
  ui_design: true|false

last_session:
  date: "YYYY-MM-DD"
  skill_used: "[skill name]"
  summary: "[What was accomplished]"

next_session:
  recommended_skill: "[skill name]"
  focus: "[What to work on]"

known_issues: []

files_to_review: []
```

### State File Usage

**At Session Start:**
1. If state file provided → Read and load recommended skill
2. If no state file → Detect from prompt or ask user

**At Session End:**
1. Update state file with session summary
2. Set recommended_skill for next session
3. Note any pending items

---

## Multi-Skill Scenarios

Some tasks may require content from multiple skills:

| Scenario | Skills to Load | Notes |
|----------|----------------|-------|
| "Design data model and plan pages" | system-design + ui-design | Design phases often overlap |
| "Implement feature from scratch" | requirements (briefly) + build | Capture intent, then implement |
| "Fix authentication bug" | build only | Auth patterns are in build |
| "Add new entity and UI" | system-design + build | Design then implement |

**When loading multiple skills:**
- Load the primary skill fully
- Reference specific sections from secondary skill
- Keep total context under 40 KB

---

## Quick Reference: Skill Triggers

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

### codebase-audit (Quality Verification)
**Load when user says:**
- "Audit the system" / "Check for inconsistencies"
- "Verify codebase" / "Run audit"
- "Make sure docs match code"
- After completing significant changes (auto-suggest)
- Before SHIP mode (auto-run)

**Do NOT load when:** Just starting requirements phase

### bulletproof-codebase (Protection Setup)
**Load when user says:**
- "Bulletproof the codebase" / "Make it robust"
- "Add pre-commit hooks" / "Set up CI/CD"
- "Add type checking" / "Enable mypy"
- "Protect the database" / "Add backup verification"
- "Add error monitoring" / "Set up alerting"
- New project without protection (auto-suggest)

**Do NOT load when:** Already has all protections set up

### windows-app-supervision (Process Management + MSI)
**Load when user says:**
- "Auto-start on boot" / "Start on reboot"
- "Add health checks" / "Watchdog"
- "Supervisor" / "Process manager" / "Daemon"
- "Application didn't start after reboot"
- "Restart on file change" / "Hot reload supervision"
- "Build MSI" / "Create installer" / "WiX"
- "Build after commit" / "Automated builds"

**Do NOT load when:** No working application yet, or Linux/macOS deployment

---

## Error Recovery

If the wrong skill was loaded or context is getting large:

1. **Note current progress** in state file
2. **Complete current task** if possible
3. **For next prompt**, explicitly state which skill is needed
4. **User can say:** "Just use the [skill-name] skill for this"

---

## Validation Across Skills

Each skill has its own exit gate checklist. The orchestrator ensures:

1. **Phase transitions** only happen after exit gate passes
2. **Build skill** contains detailed coding/audit validation
3. **Cross-references** are maintained (e.g., UI must cover all user stories)

### Cross-Skill Validation Points

| Checkpoint | Validates |
|------------|-----------|
| Requirements → System Design | All user stories map to entities |
| System Design → UI Design | All entities have UI representation |
| UI Design → Build | All pages have route specifications |
| Build (SHIP) → Delivery | All audits pass |

---

## Commands for Claude

When processing a Windows app development request:

```
1. READ this orchestrator skill (you're doing this now)
2. DETECT which phase/skill is needed (use rules above)
3. LOAD only that skill using view tool
4. WORK using the loaded skill's guidance
5. UPDATE state file at session end
6. RECOMMEND next skill for future sessions
```

**Context Budget:**
- Orchestrator: ~4 KB (always loaded)
- One skill: 8-25 KB
- Working space: Remaining context
- Target: Keep skill content under 35 KB total

---

*End of Windows Application Orchestrator Skill*
