---
name: windows-app-build
description: >
  Build, test, and package Windows applications. Includes iterative development
  workflow, regression prevention, automated validation, and delivery checklists.
  Condensed from windows-app-standards-modular (392KB → ~25KB). Use when: "start 
  coding", "implement feature", "fix bug", "create package", "ready to deliver".
---

# Windows Application Build Skill

**Purpose:** Write, test, validate, and package Windows applications  
**Version:** 4.0  
**Size:** ~25 KB (+ ~8 KB audit reference when needed)  
**Related Skills:** windows-app-requirements, windows-app-system-design, windows-app-ui-design

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

## Critical Patterns (MUST Follow)

### Batch Script Boilerplate

Every .bat file MUST start with:

```batch
@echo off
setlocal EnableDelayedExpansion
title [AppName] v[X.Y.Z] Build [YYDDD-HHMM]
cd /d "%~dp0"
```

**Why:** Without `cd /d "%~dp0"`, scripts fail when run from different directories.

### Auto-Elevation for Admin Scripts

Scripts requiring Administrator (hosts file, Caddy, ports 80/443) MUST auto-elevate:

```batch
@echo off
setlocal EnableDelayedExpansion
title [AppName] Setup (Administrator Required)
cd /d "%~dp0"

:: Check for Administrator privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting Administrator privileges...
    powershell -Command "Start-Process -Verb RunAs -FilePath '%~f0' -ArgumentList '%*'"
    exit /b
)

:: Rest of script runs as Administrator
echo Running with Administrator privileges...
```

**When to use auto-elevation:**

| Task | Requires Admin |
|------|----------------|
| Modify hosts file | Yes |
| Install Caddy as service | Yes |
| Bind to ports 80/443 | Yes |
| Create Windows service | Yes |
| Modify Program Files | Yes |
| Install to user directory | No |
| Run Python/venv | No |
| Start app on port 8008+ | No |

### Hosts File Modification Pattern

```batch
:: Auto-elevate first, then:
set "HOSTS_FILE=%SystemRoot%\System32\drivers\etc\hosts"
set "DOMAIN=pms.ucc-austin.org"
set "IP=192.168.0.132"

:: Check if entry already exists
findstr /C:"%DOMAIN%" "%HOSTS_FILE%" >nul 2>&1
if %errorlevel% equ 0 (
    echo Hosts entry already exists for %DOMAIN%
) else (
    echo Adding hosts entry: %IP% %DOMAIN%
    echo %IP%    %DOMAIN% >> "%HOSTS_FILE%"
    if %errorlevel% equ 0 (
        echo Successfully added hosts entry
    ) else (
        echo ERROR: Failed to modify hosts file
    )
)
```

### Session Cookie Access

```python
# WRONG - hardcoded
session_token = request.cookies.get("session_token")

# RIGHT - from settings
session_token = request.cookies.get(settings.SESSION_COOKIE_NAME)
```

### Template Configuration

Only ONE file creates Jinja2Templates - `templates_config.py`:

```python
from fastapi.templating import Jinja2Templates
from datetime import datetime
from app.config import get_settings
from app import auth

settings = get_settings()

templates = Jinja2Templates(directory="app/templates")
templates.env.globals.update({
    "app_name": settings.APP_NAME,
    "app_version": settings.APP_VERSION,
    "now": datetime.now,
    # Auth functions used in templates
    "can_manage_assets": auth.can_manage_assets,
    "can_approve_bookings": auth.can_approve_bookings,
    "is_admin": auth.is_admin,
})
```

All routes import: `from app.templates_config import templates`

**Rule:** Any function called in templates must be in `templates.env.globals`.

### Pydantic Settings

```python
class Settings(BaseSettings):
    # fields...
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # CRITICAL
```

### SessionMiddleware

```python
from starlette.middleware.sessions import SessionMiddleware

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie=settings.SESSION_COOKIE_NAME,
)
```

### Exception Handlers

```python
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    # Do NOT use Depends() - create manual session
    db = SessionLocal()
    try:
        user = get_user_from_session_manual(request, db)
    except:
        user = None
    finally:
        db.close()
    
    # Pass globals explicitly
    return templates.TemplateResponse(
        "errors/404.html",
        {
            "request": request,
            "user": user,
            "app_version": settings.APP_VERSION,
            "build_id": settings.BUILD_ID,
        },
        status_code=404
    )
```

### Service Layer Pattern

```python
# services/item_service.py
class ItemService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_item(self, user_id: int, title: str) -> Item:
        # Business logic here
        item = Item(title=title, created_by_id=user_id)
        self.db.add(item)
        self.db.commit()
        return item

# routes/items.py - THIN controller
@router.post("/items/new")
async def create_item(
    request: Request,
    title: str = Form(...),
    db: Session = Depends(get_db),
    user: User = Depends(require_user)
):
    service = ItemService(db)
    item = service.create_item(user.id, title)
    return RedirectResponse(f"/items/{item.id}", status_code=303)
```

### Form Routes Pattern

```python
# GET - show form
@router.get("/items/new")
async def show_create_form(request: Request, user: User = Depends(require_user)):
    return templates.TemplateResponse(
        "items/form.html",
        {"request": request, "user": user, "form": {}, "mode": "create"}
    )

# POST - handle submission
@router.post("/items/new")
async def handle_create(
    request: Request,
    title: str = Form(...),
    db: Session = Depends(get_db),
    user: User = Depends(require_user)
):
    try:
        service = ItemService(db)
        item = service.create_item(user.id, title)
        return RedirectResponse(f"/items/{item.id}", status_code=303)
    except ValueError as e:
        return templates.TemplateResponse(
            "items/form.html",
            {"request": request, "user": user, "form": {"title": title}, "error": str(e), "mode": "create"}
        )
```

### Route Ordering (CRITICAL)

FastAPI matches routes in definition order. Static paths MUST come before dynamic paths:

```python
# CORRECT ORDER
@router.get("/items")              # 1. List
async def list_items(): ...

@router.get("/items/new")          # 2. Create (static)
async def create_form(): ...

@router.post("/items/new")         # 3. Create handler (static)
async def create(): ...

@router.get("/items/{id}")         # 4. Detail (dynamic - AFTER static)
async def view(): ...

@router.get("/items/{id}/edit")    # 5. Edit (dynamic sub-path)
async def edit_form(): ...
```

**Why:** If `/{id}` is before `/new`, FastAPI tries to convert "new" to integer → 422 error.

### Explicit Route Names

Always use `name=` parameter for routes referenced in templates:

```python
# WRONG - relies on auto-generated name
@router.get("/new")
async def new_request_form(): ...

# RIGHT - explicit name matches template url_for()
@router.get("/new", name="pms.new_request")
async def new_request_form(): ...
```

**Convention:** `{module}.{resource}_{action}` (e.g., `pms.request_list`, `ams.asset_detail`)

### HTTPS Cookie Security

Match cookie security to deployment:

```python
is_https = settings.BASE_URL.startswith("https://")

# In auth.py - create_session()
response.set_cookie(
    key=settings.SESSION_COOKIE_NAME,
    value=f"{user_id}:{token}",
    httponly=True,
    samesite="lax",
    secure=is_https,  # CRITICAL
    path="/"
)

# In main.py - SessionMiddleware
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie="app_oauth_state",
    https_only=is_https  # CRITICAL
)
```

### Model Field Name Verification

Always verify field names against model definitions:

```python
# models.py
class Booking(Base):
    start_time = Column(DateTime)  # Actual field name
    end_time = Column(DateTime)

# WRONG - field doesn't exist
bookings = query.order_by(Booking.start_datetime.desc())

# RIGHT - matches model definition
bookings = query.order_by(Booking.start_time.desc())
```

**Prevention:** Before using `Model.field_name` in routes/services, check models.py for exact name.

### Model Duplication/Copy Pattern

When copying model instances, ALWAYS read the model definition first:

```python
# Wrong - assumed names
new = Model(liturgical_season=src.liturgical_season)  # Wrong!

# Right - verified against model
new = Model(season=src.season)  # Actual field name
```

**Common name mistakes:** liturgical_season->season, sequence_order->sort_order, preacher->sermon_preacher

### Template URL Patterns (FastAPI)

Avoid Flask-style url_for() in FastAPI templates - use direct paths:

```html
<!-- Wrong --> <a href="{{ url_for('detail', id=x.id) }}">
<!-- Right --> <a href="/items/{{ x.id }}">
```

### Context-Aware Navigation

Navigation links should adapt based on authentication state:

```jinja2
{# Staff sees Dashboard, public sees Portal #}
{% if user %}
<a href="{{ url_for('dashboard.home') }}">Home</a>
{% else %}
<a href="{{ url_for('public.index') }}">Home</a>
{% endif %}

{# Staff actions link to admin pages #}
{% if user %}
<a href="{{ url_for('pms.new_request') }}">New Request</a>
{% else %}
<a href="{{ url_for('public.request_form') }}">Submit Request</a>
{% endif %}
```

**Pattern:** Use `{% if user %}` to switch between staff and public routes in shared templates.

### Template Variable Naming

**NEVER** use `request` as a variable name for domain objects. The HTTP Request object always occupies this name in Jinja2 context.

```python
# WRONG - shadows the HTTP request object
return templates.TemplateResponse(
    "requests/detail.html",
    {"request": request, "request": maint_request}  # Collision!
)

# RIGHT - use descriptive domain-specific name
return templates.TemplateResponse(
    "requests/detail.html",
    {"request": request, "maint_request": maint_request}
)
```

**Naming conventions for domain objects:**

| Domain | Variable Name |
|--------|---------------|
| Maintenance/Property Request | `maint_request`, `property_request` |
| Booking/Reservation | `booking`, `reservation` |
| Asset | `asset`, `equipment` |
| Venue/Room | `venue`, `room` |
| Service | `service`, `worship_service` |
| User | `target_user`, `staff_member` (not `user` if current user is also in context) |

### Template Block Names in Inheritance (CRITICAL)

When extending base templates with layout structure, use the correct nested block:

```jinja2
{# admin/base.html defines the structure #}
{% block content %}
<div class="row">
    <nav id="sidebar">...</nav>      {# SIDEBAR HERE #}
    <main>
        {% block admin_content %}{% endblock %}  {# CHILD CONTENT HERE #}
    </main>
</div>
{% endblock %}

{# WRONG - overwrites entire content block including sidebar #}
{% extends "admin/base.html" %}
{% block content %}
    <h1>My Page</h1>  {# Sidebar is gone! #}
{% endblock %}

{# RIGHT - uses nested block, preserves sidebar #}
{% extends "admin/base.html" %}
{% block admin_content %}
    <h1>My Page</h1>
{% endblock %}
```

**Rule:** Use the specific nested block (`admin_content`, `page_content`) not the outer `content` block.

**Verify:** `grep -l "{% block content %}" app/templates/admin/*.html` should only return base.html.

### SQLAlchemy ORDER BY - Columns Only

SQLAlchemy `order_by()` requires actual database columns, not Python `@property`:

```python
class User(Base):
    first_name = Column(String)  # Database column ✓
    last_name = Column(String)   # Database column ✓
    
    @property
    def display_name(self):      # Computed property ✗
        return f"{self.first_name} {self.last_name}"

# WRONG - property is not a column
users = db.query(User).order_by(User.display_name).all()

# RIGHT - use actual columns
users = db.query(User).order_by(User.first_name, User.last_name).all()
```

**Rule:** Only Column-defined attributes in `filter()`, `order_by()`, `group_by()`.

### Service Function Parameters

Always match exact parameter names when calling service functions:

```python
# Service signature
async def send_email(
    to_email: str,
    subject: str,
    html_content: str,  # <-- Actual name
) -> bool:

# WRONG
await send_email(to_email="x", subject="y", body="z")  # 'body' doesn't exist!

# RIGHT
await send_email(to_email="x", subject="y", html_content="z")
```

**Prevention:** Check function signature before calling; use IDE autocomplete.

### Email Service Database Settings (CRITICAL)

When calling `send_email()` from notification functions, MUST pass `db=db` to use database-configured SMTP settings:

```python
# WRONG - falls back to environment variables (often empty)
success, _ = await send_email(to_email, subject, html_content)

# RIGHT - uses database-configured SMTP settings
success, _ = await send_email(to_email, subject, html_content, db=db)
```

**Why this is insidious:** Test emails work (admin panel passes db), but notification emails fail silently (missing db). Hard to debug because SMTP "looks configured."

**Rule:** Every `send_email()` call in notification functions must include `db=db`.

### Database Migration for New Model Columns

When adding new columns to SQLAlchemy models, existing databases need ALTER TABLE:

```python
# After adding to models.py:
subscribe_all_requests = Column(Boolean, default=False, nullable=False)

# Run this to add column to existing database:
import sqlite3
conn = sqlite3.connect('instance/app.db')
cursor = conn.cursor()
cursor.execute('ALTER TABLE users ADD COLUMN subscribe_all_requests BOOLEAN DEFAULT 0 NOT NULL')
conn.commit()
conn.close()
```

**Symptom:** `sqlite3.OperationalError: no such column: users.new_column`

**Prevention:** After adding model columns, always run migration before testing.

### Recipient-Aware Email Links

Notification emails should link staff to admin pages, public users to public portal:

```python
def is_staff_user(db: Session, email: str) -> bool:
    """Check if email belongs to active staff user."""
    from app.models import User
    user = db.query(User).filter(
        User.email == email.lower(),
        User.is_active == True
    ).first()
    return user is not None

def get_request_url_for_recipient(db, request, email: str) -> str:
    """Return admin URL for staff, public URL for others."""
    if is_staff_user(db, email):
        return f"{settings.BASE_URL}/admin/requests/{request.id}"
    return f"{settings.BASE_URL}/requests/view/{request.request_number}"
```

**Usage:** Build email content per-recipient, not once for all:

```python
# WRONG - same link for everyone
html = f'<a href="{get_public_url(request)}">View</a>'
for email in recipients:
    send_email(email, subject, html, db=db)

# RIGHT - customized link per recipient
for email in recipients:
    url = get_request_url_for_recipient(db, request, email)
    html = f'<a href="{url}">View</a>'
    send_email(email, subject, html, db=db)
```

### Dark Mode CSS (Bootstrap 5.3)

Use `bg-body-secondary` instead of `bg-light` for dark mode support:

```html
<!-- WRONG - stays light in dark mode -->
<div class="p-3 bg-light rounded">Content</div>

<!-- RIGHT - adapts to dark mode -->
<div class="p-3 bg-body-secondary rounded">Content</div>
```

**Rule:** Replace all `bg-light` with `bg-body-secondary` in templates.

### View/Edit Page Card Consistency

View and Edit pages for the same entity should have consistent card ordering:

1. **Common cards first** (appear on both pages)
2. **Page-specific cards after** (only on View or Edit)

```
View Page:              Edit Page:
├── Submitter Info      ├── Submitter Info     (common)
├── Email Notifications ├── Email Notifications (common)
├── Vendor Assignment   ├── [form fields]      (edit-specific)
├── Quick Actions
└── Status History      (view-specific)
```

**Rule:** When adding cards, maintain ordering parity between View and Edit templates.

### Verify Exact Names (Universal Principle)

**Always verify exact names before using them.** This applies to:

| Context | Common Mistakes | Prevention |
|---------|-----------------|------------|
| Model fields | `start_datetime` vs `start_time` | Check models.py |
| Service params | `body` vs `html_content` | Check function signature |
| Template vars | `request` vs `maint_request` | Check route context |
| Property vs Column | `display_name` vs `first_name` | Check if @property or Column |
| Audit log fields | `details` vs `new_value` | Check AuditLog model |

**Rule:** When you assume a name, you're often wrong. Take 5 seconds to verify.

```python
# Before writing this:
booking.start_datetime  # Are you SURE it's not start_time?
send_email(body=...)    # Are you SURE it's not html_content?
User.display_name       # Are you SURE it's a Column, not @property?
```

### Claude.md for Claude Code Handoff

Maintain a `Claude.md` file in the application root to facilitate switching to Claude Code for implementation, testing, debugging, and extension.

```markdown
# Project: [App Name]

## Quick Start
cd [project-dir] && source venv/bin/activate && python -m uvicorn app.main:app --reload

## Architecture
- Framework: FastAPI + SQLAlchemy 2.0 + Jinja2
- Auth: OAuth-only (Google), first-user=admin
- Database: SQLite (instance/app.db)

## Key Files
- app/models.py - All SQLAlchemy models
- app/config.py - Pydantic Settings
- app/templates_config.py - Jinja2 setup (ONE file)
- app/auth.py - OAuth + session management

## Current State
- [x] Core CRUD for [Module]
- [ ] Email notifications
- [ ] Reporting

## Known Issues
- Hairpin NAT requires hosts file entry for internal access

## Testing
pytest tests/ -v
pytest tests/test_[module].py -v -k "test_name"

## Critical Patterns
- Route ordering: /new before /{id}
- Template blocks: use admin_content, not content
- Never name domain objects "request"
```

**When to update Claude.md:**
- After completing a feature
- When discovering issues/workarounds
- Before ending a session
- When patterns change

**Benefits:**
- Claude Code starts with full context
- No re-explaining architecture decisions
- Known issues don't get re-discovered
- Testing commands ready to use

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
- [ ] Route ordering: `/new` before `/{id}` in all route files
- [ ] Template auth functions registered in `templates.env.globals`
- [ ] All `url_for()` routes have explicit `name=` parameter
- [ ] No domain objects named `request` (use `maint_request`, `booking`, etc.)
- [ ] Admin templates use `{% block admin_content %}` not `{% block content %}`
- [ ] ORDER BY clauses use Column fields, not @property attributes

### Navigation Checks
- [ ] All new features have navigation links to reach them
- [ ] Settings sub-features have links in appropriate settings tab
- [ ] CLAUDE.md Navigation Registry is current
- [ ] Navigation tests pass: `pytest tests/test_navigation.py -v`
- [ ] No "hidden features" (route + template exists but no UI link)

### Security Checks
- [ ] No `|safe` filter on user-generated content
- [ ] All POST/PUT/DELETE routes have authentication checks
- [ ] No secrets in code (grep for API_KEY, PASSWORD, SECRET)
- [ ] All POST forms have CSRF tokens
- [ ] File uploads validate extension AND MIME type
- [ ] No raw SQL queries with user input
- [ ] Sensitive settings use encryption (SENSITIVE_SETTINGS list)
- [ ] .env.example documents all required env vars
- [ ] No production secrets in .env.example
- [ ] Config values match between code defaults and .env.example

### Name Verification (verify against source)
- [ ] Model field names match models.py exactly
- [ ] Service function calls use exact parameter names
- [ ] Template variable names don't collide with reserved names

### Documentation
- [ ] Claude.md exists in project root (for Claude Code handoff)
- [ ] Claude.md has current state, known issues, critical patterns

---

## Quick Audits (Essential Checks)

### Architecture Audit
```bash
# Models should not have business methods
grep -n "def " app/models.py | grep -v "__\|property"

# Routes should not query database directly (minimize)
grep -rn "db.query\|\.filter\|\.all()" app/routes/

# Services should exist
ls app/services/
```

### Template Audit
```bash
# Single Jinja2Templates instance
grep -r "Jinja2Templates(" app/ --include="*.py"
# Should only show templates_config.py

# No hardcoded options
grep -r "<option" app/templates/
# Should return nothing (or only "Loading...")
```

### Script Audit
```bash
# All scripts have cd /d
findstr /M "cd /d" *.bat scripts\*.bat
# ALL .bat files should appear

# Admin scripts have elevation
findstr /M "net session" scripts\*.bat
# Should show: setup-hosts.bat, install-*.bat, etc.
```

### Security Audit
```bash
# Only auth.py has hashlib
grep -r "import hashlib" app/ --include="*.py"
# Should only show auth.py

# Session cookie constant used
grep -r "session_token" app/routes/ --include="*.py"
# Should return ZERO results
```

---

## Common Errors Quick Fix

| Error | Cause | Fix |
|-------|-------|-----|
| "requirements.txt not found" | Missing `cd /d` | Add to batch script line 4 |
| "session_token undefined" | Hardcoded name | Use settings.SESSION_COOKIE_NAME |
| "'now' is undefined" | Missing global | Add to templates_config.py |
| "'form' is undefined" | GET route missing form | Pass `form={}` in context |
| "Jinja2Templates directory" | Multiple instances | Use single templates_config.py |
| "Extra inputs not permitted" | Pydantic strict | Add `extra = "ignore"` |
| "SessionMiddleware must be installed" | Missing middleware | Add to main.py |
| 500 with blank footer | Error handler missing globals | Pass app_version explicitly |
| Login always fails | Duplicate hash_password | Only use auth.py |
| WatchFiles spam | Bare --reload | Use `--reload-dir app` |
| "'X' is invalid keyword for Model" | Route param ≠ model column | Use exact model column names |
| "'int' object has no attribute 'X'" | Variable shadows import | Use distinct variable names |
| Routes redirect to login randomly | Inconsistent cookie name | SESSION_COOKIE_NAME everywhere |
| Form field empty despite JS | JS sets placeholder not value | Set `.value` in auto-populate |
| "Coming Soon" in production | Incomplete feature shipped | Complete ALL features first |
| Drag/reorder not working | Incomplete CRUD | Implement reorder + auto-save |
| Multi-tenant features broken | Single-tenant design | Design for multi-tenant from start |
| Login loops back immediately | OAuth cookie = auth cookie | Use separate cookie names |
| Google OAuth 400 private IP | OAuth rejects 192.168.x.x | Use localhost or public domain |
| Internal access shows router page | Hairpin NAT not supported | Add hosts file entry |
| "Access denied" modifying hosts | Script not elevated | Add auto-elevation pattern |
| 500 after OAuth login | Template expects `current_user`, route passes `user` | Use consistent naming or aliases |
| 422 on /new endpoint | Route ordering wrong | Move /new routes before /{id} routes |
| 'function' undefined in template | Missing global | Add function to templates.env.globals |
| NoMatchFound for route name | Missing name param | Add `name=` to route decorator |
| AttributeError on model field | Wrong field name | Check models.py for exact name |
| Session lost on HTTPS | Cookie not secure | Set `secure=True` for HTTPS |
| Template shows HTTP request not domain object | Variable named `request` | Use descriptive name: `maint_request`, `booking` |
| Admin sidebar missing | Wrong block name | Use `{% block admin_content %}` not `{% block content %}` |
| ORDER BY expected, got property | @property in order_by | Use actual Column fields, not properties |
| Unexpected keyword argument | Wrong param name | Check service function signature |
| AttributeError / KeyError on name | Assumed wrong name | Verify exact name in source file |
| Notifications not sent (test works) | Missing db=db in send_email() | Pass `db=db` to all send_email calls |
| "no such column" after model change | Missing DB migration | Run `ALTER TABLE x ADD COLUMN y` |
| Email links go to wrong portal | Static public URL | Use `get_request_url_for_recipient()` |
| Dark mode shows white boxes | Using `bg-light` class | Replace with `bg-body-secondary` |

---

## HTTPS Production Deployment

### Caddy Auto-Setup Pattern

```batch
REM After BASE_URL prompt in INSTALL-AND-RUN.bat:
echo !BASE_URL! | findstr "^https://" >nul
if !errorlevel! equ 0 (
    echo HTTPS detected - configuring Caddy reverse proxy...
    call :setup_caddy
)
```

### Base URL Rules

| Scenario | BASE_URL Format |
|----------|-----------------|
| Local testing | `http://localhost:8008` |
| Production HTTPS | `https://pms.ucc-austin.org` (no port) |

**HTTPS URLs must NOT include port** - Caddy handles 443 automatically.

### Network Deployment Checklist

Before declaring HTTPS deployment complete:

**Router:**
- [ ] Port 80 forwarded (Let's Encrypt validation)
- [ ] Port 443 forwarded (HTTPS traffic)
- [ ] Router admin NOT on port 443

**DNS:**
- [ ] A record → public IP (`nslookup {domain}`)

**Server:**
- [ ] Caddy listening (`netstat -an | findstr ":443"`)
- [ ] App on configured port
- [ ] Firewall allows Caddy

### Hairpin NAT Workaround

**Symptom:** External works, internal fails or shows router page.

**Fix:** Add to `C:\Windows\System32\drivers\etc\hosts`:
```
192.168.0.132    pms.ucc-austin.org
```

**Test sequence:** Phone on mobile data first → if works, internal fail = hairpin NAT.

---

## Installer Smart Defaults

Configure organization-specific defaults in INSTALL-AND-RUN.bat:

| Setting | Pattern | Example |
|---------|---------|---------|
| Response filename | `{AppName}_install_response.enc` | `UCC-PMS_install_response.enc` |
| Server port | Non-default | `8008` (not 8000) |
| Base URL | Public HTTPS | `https://pms.ucc-austin.org` |
| OAuth domain | Org domain | `ucc-austin.org` |
| SMTP sender | Service account | `PropertyManager@ucc-austin.org` |

### Directory Auto-Creation

When accepting file paths, create directories automatically:

```batch
REM Extract directory from user-provided path and create if needed
for %%F in ("!USER_PATH!") do set "DIR_PATH=%%~dpF"
if not "!DIR_PATH!"=="" if not exist "!DIR_PATH!" (
    mkdir "!DIR_PATH!" 2>nul
    if !errorlevel! equ 0 echo Created directory: !DIR_PATH!
)
```

### Response File Path Handling

```batch
set "DEFAULT_RESPONSE=%USERPROFILE%\Documents\%APP_NAME%_install_response.enc"
set /p RESPONSE_PATH="Response file path [%DEFAULT_RESPONSE%]: "
if "!RESPONSE_PATH!"=="" set "RESPONSE_PATH=%DEFAULT_RESPONSE%"

REM Auto-create directory for response file
for %%F in ("!RESPONSE_PATH!") do set "RESP_DIR=%%~dpF"
if not "!RESP_DIR!"=="" if not exist "!RESP_DIR!" mkdir "!RESP_DIR!" 2>nul
```

---

## Error Documentation Format

Document bugs in `docs/ERROR-AND-FIXES-LOG.md`:

```markdown
### Error N: [Brief Title]
**Error**: [message]
**Symptoms**: [observable issues]
**Root Cause**: [why]
**Fix**: [what changed]
**Prevention**: [how to avoid]
```

**For detailed example entries and templates:**
```
/mnt/skills/user/windows-app-build/references/templates.md
```

---

## Test Suite Structure

```
tests/
├── conftest.py          # Shared fixtures
├── test_models.py       # Model validation
├── test_services.py     # Business logic
├── test_api.py          # Route testing
└── test_regressions.py  # Bug regression tests
```

**For complete test file templates:**
```
/mnt/skills/user/windows-app-build/references/templates.md
```

---

## Health Check & Audit

Before release:
1. Run `scripts/health-check.bat` (checks Python, venv, deps, import, tests)
2. Generate `docs/AUDIT-REPORT.md` with feature status matrix
3. Verify all tests pass

**For script and report templates:**
```
/mnt/skills/user/windows-app-build/references/templates.md
```

---

## Real-World Error Patterns

These patterns come from actual production issues:

| Pattern | Wrong | Right |
|---------|-------|-------|
| Variable shadows import | `templates = db.query().count()` | `template_count = db.query().count()` |
| Route param ≠ model column | `service_time=Form(...)` for `time` column | Match exactly: `time=Form(...)` |
| JS auto-populate | `.placeholder = value` | `.value = value` |
| Multi-tenant query | `db.query(X).first()` | `db.query(X).filter(X.venue_id == id).first()` |

---

## Regression Prevention

### After Every Fix

1. Add test to `tests/test_regressions.py`
2. Document in `docs/ERROR-AND-FIXES-LOG.md`
3. Test must fail without fix, pass with fix

### Key Regression Tests

```python
def test_batch_scripts_have_directory_change():
    """All .bat files must have cd /d command."""
    for bat in Path('.').glob('**/*.bat'):
        assert 'cd /d' in bat.read_text()

def test_session_cookie_not_hardcoded():
    """No hardcoded session_token in routes."""
    for py in Path('app/routes').glob('*.py'):
        assert 'session_token' not in py.read_text()

def test_single_jinja2templates():
    """Only templates_config.py creates Jinja2Templates."""
    count = 0
    for py in Path('app').rglob('*.py'):
        if 'Jinja2Templates(' in py.read_text():
            count += 1
    assert count == 1
```

---

## Testing Requirements

### Automated Testing at Installation

Tests MUST run during INSTALL-AND-RUN.bat:

```batch
echo Running automated test suite...
python -m pytest tests/ -v --tb=short > "%TEST_LOG%" 2>&1
if !errorlevel! neq 0 (
    echo WARNING: SOME TESTS FAILED
    set /p CONTINUE="Continue anyway? [y/N]: "
    if /i not "!CONTINUE!"=="y" exit /b 1
)
```

### Test Categories

| Category | Files | Purpose |
|----------|-------|---------|
| Unit | test_models.py, test_services.py | Core logic |
| API | test_api.py | Endpoint contracts |
| Integration | test_workflows.py | End-to-end flows |
| Regressions | test_regressions.py | Never remove |

### UI Test Button

Admin settings page MUST include:

```html
<button onclick="runTests('quick')">Quick Validation</button>
<button onclick="runTests('full')">Full Validation</button>
```

---

## Package Naming

```
ZIP: [Org]-[App]-v[X.Y.Z]-[YYDDD][HHMM].zip
Internal folder: [Org]-[App]/ (NO VERSION in folder name)

Example: UCC-PMS-v9.0.1-260021430.zip containing UCC-PMS/
```

**Golden Baseline:** `[App]-GOLDEN-BASELINE.zip`

---

## Version Numbering

```
v[Major].[Minor].[Patch] Build [YYDDD]-[HHMM]

Major: Breaking changes
Minor: New features
Patch: Bug fixes

YYDDD: Year (2 digit) + Day of year (3 digit)
HHMM: Hour + Minute (24h)

Example: v9.0.1 Build 26002-1430 = January 2, 2026 at 2:30 PM
```

---

## Directory Structure

```
[AppName]/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py            # SACRED
│   ├── auth.py              # SACRED
│   ├── templates_config.py  # SACRED
│   ├── database.py
│   ├── models.py
│   ├── ontology.py
│   ├── routes/
│   ├── services/
│   ├── templates/
│   └── static/
├── scripts/
│   ├── run.bat
│   ├── run-tests.bat
│   ├── backup.bat
│   └── config_crypto.py
├── tests/
│   ├── conftest.py
│   ├── test_regressions.py
│   └── test_*.py
├── docs/
│   └── ERROR-AND-FIXES-LOG.md
├── instance/                 # Runtime (not in package)
├── INSTALL-AND-RUN.bat
├── UPDATE.bat
├── README.md
├── INSTALL.md
├── CHANGELOG.md
├── requirements.txt
├── pytest.ini
└── .env.example
```

---

## Session Workflow

### Starting a Session

1. **Receive:** Golden baseline ZIP + State file
2. **Review:** State file for context
3. **Clarify:** What specific changes needed
4. **Determine:** Mode (ADD, FIX, or SHIP)

### During a Session

1. Extract baseline to working directory
2. Make only requested changes
3. Test affected functionality
4. Run regression tests

### Ending a Session

1. Update CHANGELOG.md
2. Update state file
3. Run pre-delivery checklist
4. Package excluding forbidden files
5. Deliver with summary

### State File Template

```yaml
# APP-STATE.yaml
version: "X.Y.Z"
build: "YYDDD-HHMM"
last_verified: "YYYY-MM-DD"
mode_used: "ADD|FIX|SHIP"

changes_made:
  - "Description of change"

files_modified:
  - "path/to/file.py"

tests_passing: N
regression_tests: N
known_issues: []

next_session:
  recommended_mode: "ADD|FIX|SHIP"
  focus: "What to work on"
```

---

## Forbidden Actions

| Action | Why | Do Instead |
|--------|-----|------------|
| Rebuild from scratch | Loses fixes | Iterate on baseline |
| Create .bat without boilerplate | Regressions | Copy from existing |
| Hardcode cookie names | Session failures | Use settings constant |
| Create multiple Jinja2Templates | Template errors | Import from templates_config |
| Deliver without checklist | Defects | Run 20-item check |
| Skip regression tests | Reintroduce bugs | Run tests every delivery |
| Ship "Coming Soon" | Incomplete features | Complete all features |

---

## Emergency: Something Broke

1. **Don't rebuild** - find the specific broken file
2. Check ERROR-AND-FIXES-LOG.md
3. Run `pytest tests/test_regressions.py -v`
4. Fix the specific issue
5. Add new regression test

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
```python
# Only load when running full audits
"/mnt/skills/user/windows-app-build/references/audit-checklists.md"
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

*End of Windows Application Build Skill*
