---
name: windows-app-build
description: >
  Build, test, and package Windows applications. Includes iterative development
  workflow, regression prevention, automated validation, and delivery checklists.
  Condensed from windows-app-standards-modular (392KB → 17KB + references). Use when: "start
  coding", "implement feature", "fix bug", "create package", "ready to deliver".
---

# Windows Application Build Skill

**Purpose:** Write, test, validate, and package Windows applications
**Version:** 4.1
**Size:** ~17 KB (+ ~102 KB references when needed)
**Related Skills:** windows-app-requirements, windows-app-system-design, windows-app-ui-design, security-patterns-orchestrator

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Start coding" / "Let's implement"
- "Fix this bug" / "Something is broken"
- "Create the package" / "Ready to deliver"
- "Run tests" / "Validate"
- "Add this feature to the existing app"
- "Here's the baseline package"
- "Update the application"

**Context Indicators:**
- User provides existing code/package
- User references specific files
- Discussion is about implementation details
- User reports an error or bug
- User wants to deliver/package
- Design phases are complete

## ❌ DO NOT LOAD WHEN

- User is defining what the app should do (use requirements skill)
- User is designing data model (use system-design skill)
- User is planning UI without code (use ui-design skill)
- No design work has been done yet

**Exception:** For quick fixes to existing packages, load build skill directly.

---

## Golden Rule

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   NEVER REBUILD FROM SCRATCH                                │
│   ALWAYS ITERATE ON THE BASELINE                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

If user requests "rebuild", "refactor everything", or "create new version":
1. Ask for the golden baseline package
2. Ask what specific changes are needed
3. Make ONLY those changes


## Fool-Proof Principle

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   USERS MAY HAVE NO TECHNICAL BACKGROUND                    │
│   IT JUST NEEDS TO WORK                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

Applications must be robust and fool-proof:
- Anticipate user mistakes and handle them gracefully
- Provide clear error messages with actionable guidance
- Use sensible defaults that work out of the box
- Auto-detect and auto-configure when possible
- If something can fail silently, make it fail loudly instead

---

## Three Modes

| Mode | Trigger | Action |
|------|---------|--------|
| **ADD** | New feature request | Add files to existing package |
| **FIX** | Bug report | Patch specific files |
| **SHIP** | Ready to deliver | Validate and package |

### Mode: ADD (New Feature)
- [ ] Load existing package first
- [ ] Create only new files needed
- [ ] Register new routes in main.py
- [ ] Add tests for new feature
- [ ] Update CHANGELOG.md

### Mode: FIX (Bug/Regression)
- [ ] Identify affected file(s)
- [ ] Make minimal change to fix
- [ ] Add regression test
- [ ] Update ERROR-AND-FIXES-LOG.md
- [ ] Update build ID

### Mode: SHIP (Package Delivery)
- [ ] Run pre-delivery checklist (below)
- [ ] Run all audits
- [ ] Verify no forbidden files in ZIP
- [ ] Test installation on clean path

---

## Critical Patterns (Quick Reference)

**Note:** Full code examples and detailed patterns are in reference files. This section provides quick reminders only.

### Batch Script Patterns
- **Boilerplate:** Every .bat must have `@echo off`, `setlocal`, `cd /d "%~dp0"` → `references/installer-patterns.md#batch-boilerplate`
- **Auto-Elevation:** Admin tasks must auto-elevate with `net session` check → `references/installer-patterns.md#auto-elevation`
- **Hosts File:** Use findstr check before adding entries → `references/installer-patterns.md#hosts-file`

### Python/FastAPI Patterns
- **Session Cookie:** Use `settings.SESSION_COOKIE_NAME`, never hardcode `"session_token"`
- **Template Config:** ONE file (`templates_config.py`) creates Jinja2Templates, all globals there
- **Pydantic Settings:** Add `extra = "ignore"` to Config class
- **SessionMiddleware:** Add first in middleware stack, with `secret_key` and `session_cookie`
- **Exception Handlers:** Pass `app_version` explicitly (no Depends() in error handlers)
- **Service Layer:** Thin controllers, business logic in services (ItemService, BookingService)
- **Form Routes:** GET passes empty `form={}`, POST passes form data back on error

### Route Patterns (CRITICAL)
- **Route Ordering:** Static (`/new`) BEFORE dynamic (`/{id}`) or 422 errors occur
- **Explicit Names:** Use `name="module.action"` for routes referenced in templates
- **HTTPS Cookies:** Set `secure=True` when `BASE_URL` starts with `https://`
- **Model Fields:** Verify field names in models.py before using in queries (common: `start_datetime` vs `start_time`)

### Template Patterns
- **URL Generation:** Use direct paths `/items/{{ x.id }}` not `url_for()`
- **Context Navigation:** Adapt links based on `user` state (staff vs public)
- **Admin Templates:** Use `{% block admin_content %}` not `{% block content %}`
- **Variable Names:** Never name domain objects `request` (shadows FastAPI Request)

### Database Patterns
- **ORDER BY:** Use Column fields only, not @property decorated methods
- **Model Copying:** Read model definition first, verify exact field names
- **Migrations:** Run ALTER TABLE after model changes, document in CHANGELOG.md

### Security Patterns
- **OAuth:** State cookie ≠ auth cookie (different names) → Load `security-patterns-orchestrator` for OAuth implementation
- **Form Security:** CSRF tokens, server-side validation → Load `secure-coding-patterns` for forms
- **File Upload:** Extension whitelist, MIME validation, UUID filenames → Load `secure-coding-patterns`

**For detailed code examples, templates, and full explanations:**
```
~/.claude/skills/windows-app/windows-app-build/references/templates.md
~/.claude/skills/windows-app/windows-app-build/references/security-patterns.md
~/.claude/skills/windows-app/windows-app-build/references/installer-patterns.md
```

---

## Top 10 Critical Errors (Quick Fix)

| Error | Cause | Fix |
|-------|-------|-----|
| "requirements.txt not found" | Missing `cd /d` in .bat | Add `cd /d "%~dp0"` at line 4 |
| "session_token undefined" | Hardcoded cookie name | Use `settings.SESSION_COOKIE_NAME` everywhere |
| "SessionMiddleware must be installed" | Missing middleware | Add SessionMiddleware to main.py first |
| 422 on /new endpoint | Route order wrong | Define `/new` before `/{id}` |
| Login loops back immediately | OAuth cookie = auth cookie | Use separate cookie names |
| Google OAuth 400 private IP | Private IP in redirect_uri | Use localhost or public domain |
| "no such column" after model change | No DB migration | Run ALTER TABLE to add column |
| Internal access shows router page | Hairpin NAT not supported | Add hosts file entry for internal IP |
| Drag/reorder not working | Incomplete CRUD | Implement reorder endpoint + auto-save |
| Multi-tenant data leaks | Single-tenant design | Redesign with org_id filtering from start |

**For complete error catalog with 36+ errors (symptoms, root causes, prevention):**
```
~/.claude/skills/windows-app/windows-app-build/references/error-catalog.md
```

**Error catalog includes:** E001-E036 with full documentation (error message, symptoms, root cause, fix, prevention, related errors)

---

## Pre-Delivery Checklist (50 Items)

### Files Must Exist
- [ ] INSTALL-AND-RUN.bat
- [ ] UPDATE.bat
- [ ] scripts/run.bat
- [ ] scripts/run-tests.bat
- [ ] scripts/backup.bat
- [ ] scripts/config_crypto.py
- [ ] README.md
- [ ] INSTALL.md
- [ ] CHANGELOG.md
- [ ] .env.example
- [ ] pytest.ini
- [ ] tests/conftest.py

### Files Must NOT Exist in Package
- [ ] instance/app.db
- [ ] .env (only .env.example)
- [ ] venv/
- [ ] __pycache__/

### Code Patterns (grep checks)
- [ ] All .bat files have `cd /d "%~dp0"` or `cd /d "%APP_DIR%"`
- [ ] No hardcoded "session_token" (use SESSION_COOKIE_NAME)
- [ ] Only ONE file has `Jinja2Templates(`
- [ ] Only auth.py has password hashing
- [ ] Admin scripts have `net session` elevation check

### Authentication Checks (if OAuth enabled)
- [ ] Login page has no password form (OAuth-only)
- [ ] OAuth state cookie ≠ auth session cookie
- [ ] First user gets ADMIN role automatically
- [ ] GOOGLE_ALLOWED_DOMAIN is set in .env.example

### HTTPS/Production Checks (if applicable)
- [ ] BASE_URL uses `https://` for production
- [ ] HTTPS BASE_URL has no port number
- [ ] Response filename includes app name
- [ ] Cookies have `secure=True` when HTTPS

### Route/Template Checks
- [ ] /new routes defined BEFORE /{id} routes
- [ ] All route names use `module.action` convention
- [ ] All templates extend correct base (admin_base vs base)
- [ ] No domain objects named `request` in template context

### Database Checks
- [ ] All ORDER BY use Column fields, not @property
- [ ] All model field names verified in models.py
- [ ] Database migrations documented in CHANGELOG.md

### Security Checks
- [ ] No secrets in code (use encrypted response file)
- [ ] CSRF tokens in all POST forms
- [ ] Input validation server-side
- [ ] File uploads have extension whitelist
- [ ] Email links use recipient-specific URLs

### Testing Checks
- [ ] All tests pass: `pytest tests/ -v`
- [ ] Regression tests exist for fixed bugs
- [ ] Test coverage > 70% for critical paths

### Documentation Checks
- [ ] README has installation instructions
- [ ] CHANGELOG documents all changes since last version
- [ ] ERROR-AND-FIXES-LOG has recent bugs documented
- [ ] .env.example has all required variables
- [ ] Claude.md updated with current state

**For deployment-specific checklists (HTTPS, network, certificates):**
```
~/.claude/skills/windows-app/windows-app-build/references/deployment-patterns.md
```

---

## Quick Audit Commands

Run these grep commands before delivery:

```bash
# Batch script check
findstr /M "cd /d" *.bat scripts\*.bat

# Session cookie check
grep -rn '"session' app/ | grep -v "settings.SESSION"

# Template instances check
grep -rn "Jinja2Templates" app/ | wc -l  # Should be 1

# Route ordering check
grep -n "@router" app/routes/*.py  # Verify /new before /{id}

# Model field usage check
grep -rn "\.start_datetime" app/  # Check if field actually exists in model
```

**For complete 7-category audit with detailed grep commands:**
```
~/.claude/skills/windows-app/windows-app-build/references/audit-checklists.md
```

---

## Test Suite Structure

```
tests/
├── conftest.py          # Shared fixtures
├── test_models.py       # Model validation
├── test_services.py     # Business logic
├── test_routes.py       # Route/controller tests
├── test_auth.py         # OAuth, sessions, permissions
├── test_templates.py    # Template rendering
└── test_regressions.py  # Previously fixed bugs
```

**Testing commands:**
```bash
# All tests
pytest tests/ -v

# Specific module
pytest tests/test_services.py -v

# Specific test
pytest tests/test_auth.py -v -k "test_first_user_admin"

# With coverage
pytest tests/ --cov=app --cov-report=term-missing
```

---

## Session Workflow

### Starting a Session
1. User provides package or describes feature
2. Determine mode (ADD, FIX, or SHIP)
3. Load existing baseline (if ADD/FIX)
4. Make changes
5. Test changes
6. Update build ID

### Build ID Format
`YYDDD-HHMM` (e.g., `26027-1442` = 2026, day 27, 14:42)

**Update in:** `app/config.py` → `BUILD_ID = "YYDDD-HHMM"`

### During Development
- [ ] Run tests frequently: `pytest tests/ -v`
- [ ] Check routes with `curl` or browser
- [ ] Verify database changes
- [ ] Test error scenarios
- [ ] Check logs for warnings

### Before Ending Session
- [ ] All tests pass
- [ ] CHANGELOG.md updated
- [ ] Build ID incremented
- [ ] README.md reflects changes
- [ ] Claude.md documents new patterns/issues

---

## Regression Prevention

**When fixing bugs:**
1. **Don't rebuild** - find the specific broken file
2. Check ERROR-AND-FIXES-LOG.md
3. Run `pytest tests/test_regressions.py -v`
4. Fix the specific issue
5. Add new regression test

**Regression test template:**
```python
def test_regression_issue_N():
    """Regression: [Brief description of original bug]

    Fixed in build YYDDD-HHMM
    Root cause: [Why it happened]
    """
    # Test that verifies bug doesn't reoccur
    ...
```

---

## Full Audit Reference

For detailed audits, use these 7 categories:

1. **Architecture & Code** - MVC, services, routes
2. **Templates & UI** - Jinja2, forms, options
3. **Scripts & Windows** - Batch files, paths
4. **Database & Config** - Models, settings
5. **Security** - Auth, encryption
6. **Documentation & Testing** - Docs, tests
7. **Package Release** - Final verification

Each audit has specific grep commands and checklists. Run all audits before major releases.

**Load audit reference when:**
```
~/.claude/skills/windows-app/windows-app-build/references/audit-checklists.md
```

---

## Cross-Skill Validation (Build Phase)

Before SHIP mode, validate against other skills:

### From Requirements
- [ ] All P0 user stories are implemented
- [ ] Acceptance criteria can be demonstrated
- [ ] NFRs are met (performance, security, usability)

### From System Design
- [ ] All entities exist in models.py
- [ ] All API endpoints are implemented
- [ ] Authentication works as designed
- [ ] Backup/restore functions exist

### From UI Design
- [ ] All pages from inventory exist
- [ ] All forms match specifications
- [ ] Navigation matches design
- [ ] Help system is functional

**If cross-skill validation fails:**
1. Document the gap
2. Either implement the missing piece (ADD mode)
3. Or update the design documents to match reality

---

## Reference Files

| File | Purpose | Load When |
|------|---------|-----------|
| **audit-checklists.md** | 7-category validation checklists | SHIP mode, major releases |
| **security-patterns.md** | OAuth, CSRF, auth patterns | Implementing authentication/security |
| **templates.md** | Full code templates for all patterns | Need complete working examples |
| **deployment-patterns.md** | HTTPS, Caddy, network setup, troubleshooting | Deploying to production with HTTPS |
| **installer-patterns.md** | Batch scripts, MSI, auto-elevation | Creating installers, batch files |
| **error-catalog.md** | 36+ errors with full documentation | Debugging specific errors, E001-E036 |
| **plugin-integration.md** | Bulletproof, audit, other plugins | Integrating external skills/plugins |

**All references located at:**
```
~/.claude/skills/windows-app/windows-app-build/references/
```

---

## Delivery Statement

**When delivering a package, ALWAYS state:**

> "I have verified this package contains:
> - [X] All required batch scripts with proper headers
> - [X] All documentation files
> - [X] Test files with actual tests
> - [X] No database or environment files
> - [X] All patterns verified
>
> The package is ready for installation."

**If ANY item cannot be verified, DO NOT DELIVER. Fix first.**

---

*End of Windows Application Build Skill - v4.1*
