# Windows Application Development Skills

Complete development lifecycle for Windows applications - from requirements to production deployment.

**Category:** Windows-App
**Skills:** 6 (+ 3 security sub-category)
**Total Size:** ~64KB SKILL.md + ~173KB references

---

## Development Lifecycle

The Windows-App skills follow a structured workflow:

```
Requirements → System Design → UI Design → Build → Supervision
     ↓              ↓              ↓         ↓         ↓
 User Stories   Data Models    Pages     Code      Deploy
    NFRs        API Endpoints  Navigation  Tests   Service
```

---

## Skills in This Category

### windows-app-orchestrator (~12KB + 16KB ref)
**Phase:** All (coordinator)
**Purpose:** Determine which skill to load based on project phase

**When to use:**
- "I want to build an app..."
- Any Windows development request

**Key features:**
- Phase detection and routing
- State management across phases
- Multi-skill coordination
- Error recovery patterns

**References:**
- orchestration-patterns.md (16KB) - Phase transitions, state files, handoff protocols

**Related:** Always loads first, then routes to specialized skills

---

### windows-app-requirements (~8KB + 16KB ref)
**Phase:** Requirements
**Purpose:** Capture user intentions, write user stories, define acceptance criteria

**When to use:**
- "I need an app that..."
- "Write user stories for..."
- Starting a new project

**Key features:**
- User story template (Given-When-Then)
- Acceptance criteria patterns
- Non-functional requirements (NFRs)
- MoSCoW prioritization

**References:**
- requirements-templates.md (16KB) - Examples across 4 domains, NFR specifications

**Exit criteria:** User approves requirements, ready for design

---

### windows-app-system-design (~10KB)
**Phase:** System Design
**Purpose:** Design data models, API endpoints, choose architecture patterns

**When to use:**
- "Design the data model..."
- "Plan the API endpoints..."
- After requirements phase

**Key features:**
- Entity-relationship design
- FastAPI route planning
- Authentication strategy selection
- Technology stack decisions

**Exit criteria:** Data model complete, API endpoints defined

---

### windows-app-ui-design (~9KB)
**Phase:** UI Design
**Purpose:** Design pages, navigation flows, form specifications

**When to use:**
- "Design the UI..."
- "Create page layouts..."
- After system design phase

**Key features:**
- Page inventory
- Navigation flow mapping
- Form field specifications
- Template hierarchy

**Exit criteria:** All pages designed, navigation complete

---

### windows-app-build (~17KB + 124KB ref)
**Phase:** Build
**Purpose:** Implement features, fix bugs, run tests, validate, package

**When to use:**
- "Start coding..."
- "Implement this feature..."
- "Fix this bug..."
- After design phases complete

**Key features:**
- FastAPI/Jinja2 patterns
- Route ordering (critical)
- Session middleware setup
- Pre-delivery checklist (50 items)

**References:**
- audit-checklists.md (18KB) - 7-category validation
- security-patterns.md (19KB) - OAuth, CSRF, auth patterns
- templates.md (37KB) - Complete code examples
- deployment-patterns.md (7KB) - HTTPS, Caddy, network setup
- installer-patterns.md (13KB) - Batch scripts, auto-elevation
- error-catalog.md (29KB) - 36 errors with detailed fixes
- plugin-integration.md (5KB) - External skill coordination

**Exit criteria:** All tests pass, package created, ready to ship

---

### windows-app-supervision (~8KB + 33KB ref)
**Phase:** Supervision/Deployment
**Purpose:** Configure Windows service, health monitoring, create installers

**When to use:**
- "Create an installer..."
- "Set up Windows service..."
- "Configure auto-start..."
- After build complete

**Key features:**
- NSSM service configuration
- Health check implementation
- File watcher (auto-restart on changes)
- MSI packaging with WiX

**References:**
- supervision-patterns.md (17KB) - NSSM setup, health monitors, log rotation
- msi-patterns.md (16KB) - WiX templates, custom actions, upgrade patterns

**Exit criteria:** Service installed, health checks working, production deployed

---

## Security Sub-Category

See [security/README.md](security/README.md) for details on:
- security-patterns-orchestrator
- authentication-patterns
- secure-coding-patterns

---

## Common Workflows

### Workflow 1: New Application (Full Lifecycle)

```
1. Requirements Phase
   User: "I want to build a property management system"
   → windows-app-requirements
   → Define user stories, NFRs
   → User approves

2. System Design Phase
   → windows-app-system-design
   → Model entities (Property, Booking, Guest)
   → Define API endpoints
   → Choose OAuth authentication

3. UI Design Phase
   → windows-app-ui-design
   → Design pages (dashboard, properties, bookings)
   → Map navigation flow
   → Specify forms

4. Build Phase
   → windows-app-build
   → Implement routes and models
   → security-patterns-orchestrator (for OAuth)
   → Run tests
   → Create package

5. Deployment Phase
   → windows-app-supervision
   → Install as Windows service
   → Configure health checks
   → Deploy to production
```

### Workflow 2: Add Feature to Existing App

```
User: "Add guest check-in/check-out functionality"
→ windows-app-build (skip to implementation)
→ Implement new routes
→ Add tests
→ Update package
```

### Workflow 3: Fix Bug

```
User: "Login redirects back to login page"
→ windows-app-build
→ Check ERROR-AND-FIXES-LOG.md (Error #5: Cookie name collision)
→ Fix: Separate OAuth state cookie from session cookie
→ Add regression test
→ Update build ID
```

### Workflow 4: Security Enhancement

```
User: "Add CSRF protection to all forms"
→ windows-app-build
→ security-patterns-orchestrator
→ secure-coding-patterns
→ Implement CSRF tokens
→ Validate with security checklist
```

---

## Phase Transition Rules

### When to Skip Phases

**Skip to Build if:**
- User provides existing code
- Quick bug fix needed
- Design already complete

**Skip to Supervision if:**
- Application built, just need deployment
- Only packaging/service setup needed

### When to Go Back

**Return to Requirements if:**
- Major feature addition
- Scope change
- New user stories needed

**Return to Design if:**
- New entities needed
- API structure change
- Major refactoring planned

---

## Best Practices

### Golden Rule: Never Rebuild

**ALWAYS:**
- Iterate on existing baseline
- Make minimal changes
- Preserve working state
- Track changes in CHANGELOG.md

**NEVER:**
- Rebuild from scratch
- "Refactor everything"
- Delete working code without backup

### Critical Patterns

1. **Route Ordering:** Static (`/new`) before dynamic (`/{id}`)
2. **Session Cookie:** Never hardcode "session_token", use settings.SESSION_COOKIE_NAME
3. **OAuth State:** Separate cookie from auth cookie (different names)
4. **Template Config:** ONE file creates Jinja2Templates
5. **Batch Scripts:** Always `cd /d "%~dp0"` at top

### Size Management

- **Build skill:** 17KB (condensed from 40KB)
- **Reference files:** Load only when needed
- **Keep SKILL.md focused:** Essential patterns only
- **Detailed examples:** In reference files

---

## Validation

### Pre-Delivery Checklist

Run before SHIP mode:

- [ ] All batch scripts have proper headers
- [ ] No hardcoded cookie names
- [ ] Only ONE Jinja2Templates instance
- [ ] Route ordering correct (/new before /{id})
- [ ] All tests pass
- [ ] Build ID updated
- [ ] CHANGELOG.md current

### Quick Audits

```bash
# Session cookie check
grep -rn '"session' app/ | grep -v "settings.SESSION"

# Route ordering check
grep -n "@router" app/routes/*.py

# Batch script check
findstr /M "cd /d" *.bat
```

---

## Related Skills

- **authentication-patterns** - OAuth implementation
- **secure-coding-patterns** - Security validation
- **navigation-auditor** - Navigation verification
- **conversation-snapshot** - Project state preservation

---

*Windows-App Category - Complete Development Lifecycle*
