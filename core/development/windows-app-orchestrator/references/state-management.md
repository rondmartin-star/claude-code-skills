# Project State Management

## State File Template

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

## State File Usage

**At Session Start:**
1. If state file provided → Read and load recommended skill
2. If no state file → Detect from prompt or ask user

**At Session End:**
1. Update state file with session summary
2. Set recommended_skill for next session
3. Note any pending items

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
1. Run tests to verify
2. Run quick audit automatically
3. If issues found → report and offer to fix
4. If clean → Restart server using: scripts\restart-server.bat -bg
5. Verify changes work in browser (check /health endpoint)

Before SHIP Mode:
1. Run full audit (all 5 agents in parallel)
2. Verify bulletproof setup exists
3. Run all tests
4. Generate audit report
5. Only proceed if all checks pass

After Bug Fix (FIX Mode):
1. Run targeted audit on affected files
2. Run tests to verify fix
3. Restart server: powershell -ExecutionPolicy Bypass -File scripts\restart-server.ps1 -Background
4. Verify fix via /health endpoint and browser test
5. Add regression test suggestion

Server Restart Command (reliable):
  powershell -ExecutionPolicy Bypass -File scripts\restart-server.ps1 -Background
  - Kills by port (not process name)
  - Waits for port release
  - Verifies /health after start
```
