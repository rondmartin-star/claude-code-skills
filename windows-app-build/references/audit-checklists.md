# Audit Checklists Reference

Consolidated inspection checklists for validating application packages. Load this file when running comprehensive audits before release.

---

## Quick Validation Commands

Run these FIRST before detailed audits:

```bash
# Import validation - must pass
python -c "from app.main import app; print('✓ Import validation passed')"

# Single Jinja2Templates
grep -r "Jinja2Templates(" app/ --include="*.py"
# Should only show templates_config.py

# No hardcoded options
grep -r "<option" app/templates/
# Should return nothing (or only "Loading...")

# No raw SQL without text()
grep -r "db.execute(" app/ --include="*.py"

# hashlib only in auth.py
grep -r "hashlib" app/ --include="*.py"

# Session cookie constant used everywhere
grep -r "session_token" app/routes/ --include="*.py"
# Should return ZERO results (use settings.SESSION_COOKIE_NAME)

# No "Coming Soon" placeholders
grep -ri "coming soon" app/templates/
# Should return ZERO results

# Check for variable shadowing common imports
grep -n "^\s*templates\s*=" app/routes/*.py
grep -n "^\s*settings\s*=" app/routes/*.py
# Review any matches - should not shadow imports

# Verify model columns match route parameters
# Manual review: compare Form() param names to model column names

# cd /d in all batch scripts
findstr /M "cd /d" *.bat scripts\*.bat
```

---

## Audit 1: Architecture & Code

```
═══════════════════════════════════════════════════════════════
MODEL LAYER
═══════════════════════════════════════════════════════════════
[ ] Models contain ONLY data structure (columns, relationships)
[ ] No business logic methods in models (@property OK)
[ ] All relationships have back_populates
[ ] Foreign keys have ondelete defined
[ ] Multi-tenant: relevant tables have venue/org FK
[ ] Seed data columns exist in model definition
[ ] Column names are consistent (not service_time vs time)

═══════════════════════════════════════════════════════════════
CONTROLLER - ROUTES
═══════════════════════════════════════════════════════════════
[ ] Routes are thin - delegate to services
[ ] Routes do NOT query database directly
[ ] All routers have explicit prefix
[ ] Form routes pass form={} to GET context
[ ] All routes use settings.SESSION_COOKIE_NAME (not hardcoded)
[ ] Route parameter names match model column names EXACTLY
[ ] No variable names that shadow imports (templates, settings)
[ ] Multi-entity routes accept optional venue_id parameter
[ ] Test API endpoints accept venue_id for multi-venue testing

═══════════════════════════════════════════════════════════════
SERVICE LAYER
═══════════════════════════════════════════════════════════════
[ ] All business logic in services
[ ] Services are HTTP-independent
[ ] Services raise exceptions for rule violations
[ ] SystemService has seed_database() method
[ ] Multi-tenant queries filter by venue/org ID
[ ] Integration services return ConnectionStatus/CommandResult
[ ] Naming conventions are consistent throughout

═══════════════════════════════════════════════════════════════
EXCEPTION HANDLERS
═══════════════════════════════════════════════════════════════
[ ] 404/500 handlers do NOT use Depends()
[ ] Handlers create manual database session
[ ] Handlers pass app_version, build_id explicitly
[ ] Error templates have version footer
```

---

## Audit 2: Templates & UI

```
═══════════════════════════════════════════════════════════════
TEMPLATE CONFIGURATION
═══════════════════════════════════════════════════════════════
[ ] templates_config.py exists
[ ] Only ONE Jinja2Templates() instantiation
[ ] now() in globals (for date formatting)
[ ] app_version, build_id in globals

═══════════════════════════════════════════════════════════════
NO HARDCODING
═══════════════════════════════════════════════════════════════
[ ] No <option> tags in templates (grep check)
[ ] All dropdowns load from /api/config/{key}
[ ] loadOptions() JavaScript function exists

═══════════════════════════════════════════════════════════════
FORM HANDLING
═══════════════════════════════════════════════════════════════
[ ] GET routes pass form={} in context
[ ] POST routes pass form data on validation error
[ ] Form field names match model columns EXACTLY
[ ] Required fields have validation
[ ] JS auto-populate sets .value not .placeholder

═══════════════════════════════════════════════════════════════
COMPLETENESS
═══════════════════════════════════════════════════════════════
[ ] No "Coming Soon" placeholders in templates
[ ] All CRUD operations implemented (create/read/update/delete)
[ ] Reorder functionality works with auto-save
[ ] All features in navigation are functional

═══════════════════════════════════════════════════════════════
MULTI-VENUE UI
═══════════════════════════════════════════════════════════════
[ ] Venue selector shown when multiple venues exist
[ ] Current venue displayed in header/breadcrumb
[ ] Venue ID passed to all relevant API calls
[ ] Test API endpoints include venue selector
```

---

## Audit 3: Scripts & Windows

```
═══════════════════════════════════════════════════════════════
BATCH SCRIPT HEADERS
═══════════════════════════════════════════════════════════════
Every .bat file must have:
[ ] Line 1: @echo off
[ ] Line 2: setlocal EnableDelayedExpansion
[ ] Line 3: title [AppName] vX.Y.Z Build YYDDD-HHMM
[ ] Line 4: cd /d "%~dp0" (or cd /d "%APP_DIR%")

═══════════════════════════════════════════════════════════════
REQUIRED SCRIPTS
═══════════════════════════════════════════════════════════════
[ ] INSTALL-AND-RUN.bat - Root level
[ ] UPDATE.bat - Root level
[ ] scripts/run.bat
[ ] scripts/run-tests.bat
[ ] scripts/backup.bat
[ ] scripts/config_crypto.py

═══════════════════════════════════════════════════════════════
SCRIPT CONTENT
═══════════════════════════════════════════════════════════════
[ ] Use python -m pip (not bare pip)
[ ] Use !errorlevel! (not %errorlevel%)
[ ] Development: --reload-dir app
[ ] Production: NO --reload flag
```

---

## Audit 4: Database & Configuration

```
═══════════════════════════════════════════════════════════════
PYDANTIC SETTINGS
═══════════════════════════════════════════════════════════════
[ ] Settings class has extra="ignore"
[ ] All Optional fields have = None default
[ ] SECRET_KEY is required (no default)
[ ] SESSION_COOKIE_NAME defined
[ ] APP_VERSION defined
[ ] BUILD_ID defined

═══════════════════════════════════════════════════════════════
SQLALCHEMY
═══════════════════════════════════════════════════════════════
[ ] Raw SQL wrapped in text()
[ ] Single SessionLocal factory
[ ] Proper session cleanup in routes

═══════════════════════════════════════════════════════════════
CONFIGURATION OPTIONS
═══════════════════════════════════════════════════════════════
[ ] SystemSetting model exists
[ ] DEFAULT_OPTIONS in config_options.py
[ ] /api/config/{key} endpoints exist
```

---

## Audit 5: Security

```
═══════════════════════════════════════════════════════════════
AUTHENTICATION
═══════════════════════════════════════════════════════════════
[ ] auth.py has hash_password() and verify_password()
[ ] Only auth.py imports hashlib
[ ] Session cookies: httponly=True, samesite="lax"
[ ] SessionMiddleware installed with secret_key

═══════════════════════════════════════════════════════════════
DATA PROTECTION
═══════════════════════════════════════════════════════════════
[ ] No secrets in source code
[ ] .env not in package
[ ] No | safe on user data in templates
[ ] config_crypto.py for encrypted configs
```

---

## Audit 6: Documentation & Testing

```
═══════════════════════════════════════════════════════════════
REQUIRED DOCUMENTATION
═══════════════════════════════════════════════════════════════
[ ] README.md - Overview and quick start
[ ] INSTALL.md - Detailed installation
[ ] CHANGELOG.md - Version history
[ ] .env.example - All variables documented
[ ] ERROR-AND-FIXES-LOG.md - Bug tracking with prevention notes
[ ] AUDIT-REPORT.md - Pre-release audit results

═══════════════════════════════════════════════════════════════
TESTING
═══════════════════════════════════════════════════════════════
[ ] pytest.ini exists
[ ] tests/conftest.py with fixtures
[ ] tests/test_models.py - Model creation tests
[ ] tests/test_services.py - Business logic tests
[ ] tests/test_api.py - Route/endpoint tests
[ ] tests/test_regressions.py - Bug regression tests
[ ] All tests pass: python -m pytest
[ ] Tests run during installation

═══════════════════════════════════════════════════════════════
HEALTH CHECK
═══════════════════════════════════════════════════════════════
[ ] scripts/health-check.bat exists
[ ] Checks Python installation
[ ] Checks virtual environment
[ ] Checks dependencies installed
[ ] Checks application import
[ ] Checks database exists
[ ] Runs test suite
[ ] Returns error count as exit code
```

---

## Audit 7: Package Release

```
═══════════════════════════════════════════════════════════════
PACKAGE CONTENTS
═══════════════════════════════════════════════════════════════
Must Include:
[ ] INSTALL-AND-RUN.bat
[ ] UPDATE.bat
[ ] requirements.txt
[ ] .env.example
[ ] README.md, CHANGELOG.md
[ ] app/ (all Python files)
[ ] scripts/ (all batch files)
[ ] tests/ (test files)

Must NOT Include:
[ ] instance/app.db
[ ] .env (with secrets)
[ ] venv/
[ ] __pycache__/
[ ] .git/
[ ] *.pyc

═══════════════════════════════════════════════════════════════
NAMING
═══════════════════════════════════════════════════════════════
ZIP: [Org]-[App]-v[X.Y.Z]-[YYDDD][HHMM].zip
Internal folder: [Org]-[App]/ (NO VERSION)

═══════════════════════════════════════════════════════════════
INSTALLATION TEST
═══════════════════════════════════════════════════════════════
[ ] Extract to clean directory
[ ] Run INSTALL-AND-RUN.bat
[ ] No DLL errors
[ ] No ModuleNotFoundError
[ ] Automated tests pass
[ ] Application starts
[ ] Login works
```

---

## Audit 8: Integration Validation

```
═══════════════════════════════════════════════════════════════
DATABASE SCHEMA SYNC
═══════════════════════════════════════════════════════════════
[ ] All model columns exist in production database
[ ] Column types match (String vs Text, Integer vs BigInteger)
[ ] Foreign keys exist and reference valid tables
[ ] Indexes defined in model exist in database
[ ] No orphan columns in database (removed from model)

Run schema validation:
python -c "from app.models import *; from app.database import engine; from sqlalchemy import inspect; ..."

═══════════════════════════════════════════════════════════════
MODEL ATTRIBUTE ACCESS
═══════════════════════════════════════════════════════════════
[ ] All model.field references use correct field names
[ ] No typos in common fields (expiry vs expiration, date vs datetime)
[ ] Relationship names match model definitions
[ ] Enum values used correctly (Status.ACTIVE not "active")

Check for common errors:
grep -rn "\.next_maintenance_date" app/ --include="*.py"  # Should be .next_maintenance
grep -rn "\.warranty_expiration" app/ --include="*.py"    # Should be .warranty_expiry

═══════════════════════════════════════════════════════════════
TEMPLATE INHERITANCE
═══════════════════════════════════════════════════════════════
[ ] Child templates use correct parent block names
[ ] Admin templates use admin_content (NOT content)
[ ] JavaScript uses extra_js (NOT scripts)
[ ] Page titles use page_title block
[ ] All {% block X %} have matching {% endblock %}

Check for wrong blocks:
grep -rn "{% block content %}" app/templates/admin/ --include="*.html"  # Should be empty
grep -rn "{% block scripts %}" app/templates/admin/ --include="*.html"  # Should be empty

═══════════════════════════════════════════════════════════════
FRONTEND DEPENDENCIES
═══════════════════════════════════════════════════════════════
[ ] All JavaScript libraries used are loaded in templates
[ ] CDN URLs use specific versions (not "latest")
[ ] JavaScript files load AFTER their dependencies
[ ] No duplicate library loads
[ ] Development vs production CDN URLs correct

Check library loading:
grep -rn "new Chart" app/static/js/ --include="*.js"  # Find usage
grep -rn "chart.js" app/templates/base.html            # Verify CDN
```

---

## Error Prevention Quick Reference

| Always Do This | Prevents |
|----------------|----------|
| `cd /d "%APP_DIR%"` in scripts | "No module named 'app'" |
| `form={}` in GET route context | "'form' is undefined" |
| `"now": datetime.now` in globals | "'now' is undefined" |
| `text()` wrapper for raw SQL | SQLAlchemy 2.0 warnings |
| `extra="ignore"` in Settings | Pydantic validation errors |
| Delete instance/app.db before packaging | Stale database |
| `settings.SESSION_COOKIE_NAME` constant | Session failures |
| Test on clean Windows | Missing DLL errors |
| Route param names = model column names | "invalid keyword argument" |
| Distinct variable names (not `templates=`) | "'int' has no attribute" |
| Seed data columns exist in model | "invalid keyword argument" |
| JS `.value =` not `.placeholder =` | Empty form fields |
| No "Coming Soon" in templates | Incomplete features shipped |
| Complete CRUD before delivery | Non-functional UI |
| Multi-venue design from start | Expensive refactoring later |
| Consistent naming conventions | Confusion and bugs |
| Health check before release | Deployment failures |

---

## Common Issues Quick Reference

| Issue | Cause | Solution |
|-------|-------|----------|
| "No module named 'app'" | Wrong working directory | Add `cd /d "%APP_DIR%"` before Python |
| Template not found | Wrong path in route | Check template path matches file location |
| 422 Unprocessable Entity | Form field mismatch | Align HTML names with Form() params |
| Session not working | Cookie name mismatch | Use SESSION_COOKIE_NAME constant |
| Database locked | Multiple connections | Close other processes accessing db |
| 500 on create/update | Column name mismatch | Match route params to model columns |
| Variable shadows import | `templates = count` | Use distinct names like `template_count` |
| Multi-venue broken | Single-tenant design | Add venue_id FK and filter queries |

---

*End of Audit Checklists Reference*
