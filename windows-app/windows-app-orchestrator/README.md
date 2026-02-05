# Windows App Orchestrator

**Category:** Windows Application Development
**Purpose:** Coordinate skill loading to minimize context usage
**Status:** Active (v2.0.0)

---

## Quick Reference

ALWAYS LOAD THIS SKILL FIRST for Windows application development. Determines which specialized skills to load based on context.

### Skills Coordinated

1. **windows-app-requirements** - User stories & acceptance criteria
2. **windows-app-system-design** - Data models, API design, architecture
3. **windows-app-ui-design** - Pages, navigation, forms
4. **windows-app-build** - Implementation, testing, packaging
5. **windows-app-supervision** - NSSM service, health checks, MSI installer

### Security Skills

- **security-patterns-orchestrator** - Routes to authentication or secure coding patterns
- **authentication-patterns** - OAuth-first authentication
- **secure-coding-patterns** - XSS, CSRF, SQL injection prevention

---

## Phase Review Gates (NEW in v2.0.0)

5 quality gates at development phase transitions:

| Gate | Trigger | Review Focus |
|------|---------|--------------|
| GATE 1 | After Requirements | Completeness, clarity, testability |
| GATE 2 | After System Design | Architecture alignment, scalability |
| GATE 3 | After UI Design | UX consistency, navigation flows |
| GATE 4 | After Build | Code quality, security, performance |
| GATE 5 | After Supervision | Deployment readiness, monitoring |

**How Gates Work:**
- Complete phase deliverables
- Automatic gate prompt appears
- Choose: run now, skip, or defer
- Multi-methodology review (8 approaches)
- Converge until 3 clean passes
- Gate passed: Proceed to next phase

**Time Impact:** 10-20 minutes per gate (50-100 minutes total)

---

## Detection Logic

### Phase Detection

Orchestrator analyzes user prompt and loads appropriate skill:

- "requirements", "user stories" → windows-app-requirements
- "data model", "entities" → windows-app-system-design
- "UI", "pages", "screens" → windows-app-ui-design
- "code", "implement", "fix" → windows-app-build
- "auto-start", "health check" → windows-app-supervision

### Gate Detection

- "review requirements", "requirements gate" → Run GATE 1
- "review design", "design gate" → Run GATE 2
- "review UI", "UI gate" → Run GATE 3
- "review build", "build gate" → Run GATE 4
- "review deployment", "supervision gate" → Run GATE 5

---

## State Management

Track project state with APP-STATE.yaml:

```yaml
project:
  name: "[Application Name]"
  version: "X.Y.Z"

current_phase: "requirements|system-design|ui-design|build"

phases:
  requirements:
    complete: true
    gate:
      passed: true
      date: '2026-02-05'
      issues_found: 5
      issues_fixed: 5
```

---

## Context Optimization

**Without Orchestrator:** Load all skills (~63+ KB)
**With Orchestrator:** Load only needed skills (16-37 KB)

**Savings:** 40-75% context reduction

---

## Files

- `SKILL.md` - Full orchestrator logic with all detection rules
- `README.md` - This file (quick reference)
- `CHANGELOG.md` - Version history

---

## Version

**v2.0.0** (2026-02-05)
- Added 5 Phase Review Gates
- Enhanced phase completion workflow
- Integrated with iterative-phase-review skill
- State tracking for gate passage

---

*Part of v4.0 Universal Skills Ecosystem - Windows Application Development*
