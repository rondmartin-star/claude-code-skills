# Error Catalog

Comprehensive error reference with detailed explanations, symptoms, root causes, fixes, and prevention strategies. Load this when debugging specific errors or when the quick-fix table in SKILL.md isn't sufficient.

---

## Error Index by Category

### Configuration Errors (E001-E010)
- E001: requirements.txt not found
- E002: session_token undefined
- E003: SessionMiddleware must be installed
- E004: Jinja2Templates directory conflicts
- E005: Routes redirect to login randomly
- E006: Session lost on HTTPS
- E007: WatchFiles spam with --reload
- E008: Notifications not sent (test works)
- E009: Email links go to wrong portal
- E010: Dark mode shows white boxes

### Template & Global Errors (E011-E020)
- E011: 'now' is undefined
- E012: 'form' is undefined
- E013: 500 with blank footer
- E014: 'function' undefined in template
- E015: Template shows HTTP request not domain object
- E016: Admin sidebar missing
- E017: 'X' is invalid keyword for Model
- E018: 'int' object has no attribute 'X'
- E019: Form field empty despite JS
- E020: 500 after OAuth login

### Authentication & OAuth Errors (E021-E030)
- E021: Login always fails
- E022: Login loops back immediately
- E023: Google OAuth 400 private IP
- E024: Internal access shows router page
- E025: "Access denied" modifying hosts
- E026: Pydantic "Extra inputs not permitted"
- E027: AttributeError on model field
- E028: NoMatchFound for route name
- E029: Unexpected keyword argument
- E030: AttributeError / KeyError on name

### Routing & Database Errors (E031-E040)
- E031: 422 on /new endpoint
- E032: ORDER BY expected, got property
- E033: "no such column" after model change
- E034: "Coming Soon" in production
- E035: Drag/reorder not working
- E036: Multi-tenant features broken
- E037-E040: Reserved for future errors

---

## Configuration Errors

### E001: requirements.txt not found

**Error Message:** `FileNotFoundError: [Errno 2] No such file or directory: 'requirements.txt'`

**Symptoms:**
- INSTALL-AND-RUN.bat fails during `pip install -r requirements.txt`
- Works when requirements.txt is in current directory
- Fails when batch script run from different directory
- Venv activates successfully, but pip install fails

**Root Cause:**
Batch script doesn't change to script directory before running pip install. When user runs batch script from a different directory (e.g., double-click from Explorer), the working directory is wrong and requirements.txt can't be found.

**Fix:**
Add `cd /d "%~dp0"` at the beginning of the batch script (line 4, after setlocal):

```batch
@echo off
setlocal EnableDelayedExpansion
title AppName Installer
cd /d "%~dp0"
```

**Prevention:**
- ALL .bat files MUST include `cd /d "%~dp0"` after setlocal
- Run regression test: `findstr /M "cd /d" *.bat scripts\*.bat`
- Add to batch script template in references/installer-patterns.md

**Related Errors:** E007 (WatchFiles path issues)

---

### E002: session_token undefined

**Error Message:** `KeyError: 'session_token'` or `AttributeError: 'NoneType' object has no attribute 'get'`

**Symptoms:**
- Login works initially
- Random logouts during navigation
- Some routes work, others require re-login
- Inconsistent authentication state

**Root Cause:**
Cookie name hardcoded as `"session_token"` in some routes but uses `settings.SESSION_COOKIE_NAME` (which may be different, e.g., `"auth_session"`) in other routes. When cookie names don't match, authentication state is lost.

**Fix:**
Replace all hardcoded cookie name references with settings constant:

```python
# WRONG
session_token = request.cookies.get("session_token")

# RIGHT
session_token = request.cookies.get(settings.SESSION_COOKIE_NAME)
```

Search entire codebase for `"session_token"` string and replace with settings reference.

**Prevention:**
- NEVER hardcode cookie names
- Use settings.SESSION_COOKIE_NAME everywhere
- Add linter rule to detect hardcoded cookie strings
- Grep command: `grep -r '"session' app/ | grep -v "settings.SESSION"`

**Related Errors:** E005 (random login redirects), E006 (session lost on HTTPS)

---

### E003: SessionMiddleware must be installed

**Error Message:** `RuntimeError: SessionMiddleware must be installed to access request.session`

**Symptoms:**
- Application crashes on startup
- Any route accessing request.session fails
- Error appears immediately when session accessed
- Works locally, fails in production

**Root Cause:**
SessionMiddleware not added to FastAPI application, or added in wrong order. Middleware order matters - SessionMiddleware must be added before routes that use sessions.

**Fix:**
Add SessionMiddleware to main.py application setup:

```python
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie=settings.SESSION_COOKIE_NAME,
    max_age=settings.SESSION_MAX_AGE,
    https_only=settings.HTTPS_ONLY,
)
```

**Prevention:**
- SessionMiddleware MUST be first middleware added
- Verify in pre-delivery checklist
- Add to application template
- Grep check: `grep -n "SessionMiddleware" app/main.py`

**Related Errors:** E002 (session_token undefined)

---

### E004: Jinja2Templates directory conflicts

**Error Message:** `RuntimeError: Directory 'templates' must be unique for each Jinja2Templates instance`

**Symptoms:**
- Application crashes on startup
- Multiple templates instances detected
- Error mentions "templates" directory used multiple times
- Inconsistent template rendering

**Root Cause:**
Multiple Jinja2Templates instances created in different modules (e.g., main.py, routes modules), each pointing to same templates directory. Jinja2 requires unique directory per instance.

**Fix:**
Create single templates_config.py module with shared instance:

```python
# templates_config.py
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

# Add globals
templates.env.globals["now"] = datetime.now
templates.env.globals["app_version"] = settings.APP_VERSION
```

Import this instance everywhere templates needed:

```python
from app.templates_config import templates
```

**Prevention:**
- ONE templates instance per application
- Import from central config, never create new instances
- Add to application template
- Grep check: `grep -rn "Jinja2Templates" app/ | wc -l` (should be 1)

**Related Errors:** E011 ('now' undefined), E013 (blank footer)

---

### E005: Routes redirect to login randomly

**Error Message:** No explicit error, but unexpected redirects to login page

**Symptoms:**
- User logs in successfully
- Some pages work fine
- Other pages redirect to login without reason
- Inconsistent behavior across routes
- Session appears valid but auth fails

**Root Cause:**
Inconsistent cookie name usage across routes. Some routes check `settings.SESSION_COOKIE_NAME`, others check hardcoded `"session_token"`. When names don't match, auth check fails and redirects to login.

**Fix:**
1. Search for all cookie access: `grep -rn "cookies.get" app/`
2. Replace all hardcoded names with `settings.SESSION_COOKIE_NAME`
3. Verify auth.py uses correct cookie name
4. Test all routes after fix

**Prevention:**
- Use settings.SESSION_COOKIE_NAME everywhere
- Never hardcode cookie names
- Add pre-commit hook to detect hardcoded cookies
- Grep check: `grep -rn '"session' app/ | grep -v "settings.SESSION"`

**Related Errors:** E002 (session_token undefined), E022 (login loops)

---

### E006: Session lost on HTTPS

**Error Message:** No explicit error, but session not persisted

**Symptoms:**
- Login works on HTTP (localhost)
- Login fails on HTTPS (production)
- Session cookie not set in browser
- User logged out immediately after login
- Works on Chrome, fails on Firefox (or vice versa)

**Root Cause:**
Cookie `secure` flag not set to True for HTTPS. Browsers reject non-secure cookies on HTTPS connections for security reasons.

**Fix:**
Set `secure=True` in cookie configuration and SessionMiddleware:

```python
# In SessionMiddleware setup
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie=settings.SESSION_COOKIE_NAME,
    https_only=True,  # Set to True for HTTPS
)

# When setting cookies manually
response.set_cookie(
    key=settings.SESSION_COOKIE_NAME,
    value=token,
    secure=True,  # Required for HTTPS
    httponly=True,
    samesite="lax",
)
```

**Prevention:**
- Always set `secure=True` for production (HTTPS)
- Use environment variable: `HTTPS_ONLY=true` in production
- Test on actual HTTPS before deployment
- Add to deployment checklist

**Related Errors:** E022 (login loops on HTTPS)

---

### E007: WatchFiles spam with --reload

**Error Message:** No error, but console spammed with WatchFiles messages

**Symptoms:**
- Development server works fine
- Console filled with "WatchFiles detected change" messages
- Files in venv/ or .git/ triggering reloads
- Slow reload times
- Console difficult to read

**Root Cause:**
Using bare `--reload` flag watches entire directory tree, including venv/, .git/, __pycache__/. Every file change (including pip installs) triggers reload.

**Fix:**
Use `--reload-dir app` to watch only application directory:

```bash
python -m uvicorn app.main:app --reload --reload-dir app
```

Or in INSTALL-AND-RUN.bat:
```batch
start /B python -m uvicorn app.main:app --reload --reload-dir app --port !PORT!
```

**Prevention:**
- Always use `--reload-dir app` in development
- Add to batch script template
- Document in development workflow
- Update INSTALL-AND-RUN.bat template

**Related Errors:** None directly related

---

### E008: Notifications not sent (test works)

**Error Message:** No error, but emails silently not sent

**Symptoms:**
- Email test function works (`send_test_email()`)
- Actual notifications not sent in production
- No error logged
- Email appears to send (no exception)
- Database shows notification as "sent"

**Root Cause:**
Missing `db=db` parameter in `send_email()` call. Email function requires database session to log email history, but some calls don't pass it. Without db session, email isn't actually sent (fails silently).

**Fix:**
Pass `db=db` to ALL `send_email()` calls:

```python
# WRONG
send_email(
    to=user.email,
    subject="Subject",
    body="Body"
)

# RIGHT
send_email(
    to=user.email,
    subject="Subject",
    body="Body",
    db=db  # Required!
)
```

Search codebase: `grep -rn "send_email(" app/ | grep -v "db=db"`

**Prevention:**
- Make `db` a required parameter (not optional)
- Add type hints to catch missing parameter
- Grep check in pre-commit hook
- Add to security checklist (email delivery critical)

**Related Errors:** E009 (wrong portal links in emails)

---

### E009: Email links go to wrong portal

**Error Message:** No error, but email links incorrect

**Symptoms:**
- Emails sent successfully
- Links in email go to wrong domain
- Admin emails have tenant portal links
- Tenant emails have admin portal links
- Links work, but go to wrong place

**Root Cause:**
Using static `settings.BASE_URL` instead of recipient-specific URL. Admin portal and tenant portal have different base URLs (e.g., `admin.example.com` vs `portal.example.com`).

**Fix:**
Use `get_request_url_for_recipient()` helper function that determines correct base URL based on recipient role:

```python
# WRONG
reset_link = f"{settings.BASE_URL}/reset-password?token={token}"

# RIGHT
base_url = get_request_url_for_recipient(user)
reset_link = f"{base_url}/reset-password?token={token}"
```

**Prevention:**
- NEVER use static BASE_URL in email links
- Always use recipient-specific URL function
- Add to email template checklist
- Grep check: `grep -rn "BASE_URL" app/ | grep "email"`

**Related Errors:** E008 (emails not sent)

---

### E010: Dark mode shows white boxes

**Error Message:** No error, but visual styling broken

**Symptoms:**
- Light mode looks correct
- Dark mode has white boxes instead of dark backgrounds
- Text invisible on white backgrounds in dark mode
- Bootstrap components ignore dark mode
- Custom elements styled correctly, Bootstrap elements broken

**Root Cause:**
Using deprecated Bootstrap class `bg-light` which is always light (doesn't respond to dark mode). Bootstrap 5.3+ uses theme-aware classes like `bg-body-secondary`.

**Fix:**
Replace `bg-light` with theme-aware class:

```html
<!-- WRONG -->
<div class="card bg-light">

<!-- RIGHT -->
<div class="card bg-body-secondary">
```

Search and replace: `grep -rn "bg-light" templates/`

**Prevention:**
- Use theme-aware Bootstrap classes
- Test dark mode before delivery
- Add to UI checklist
- Bootstrap 5.3+ theme documentation

**Related Errors:** None directly related

---

## Template & Global Errors

### E011: 'now' is undefined

**Error Message:** `UndefinedError: 'now' is undefined`

**Symptoms:**
- Templates render correctly most times
- Error appears in templates using {{ now }}
- Timestamp display missing
- Footer shows error or blank space
- Inconsistent - works in some templates, fails in others

**Root Cause:**
`now` function not added to Jinja2 templates globals. Templates expect `now` to be available (for displaying timestamps), but it's not registered.

**Fix:**
Add `now` to templates configuration globals:

```python
# In templates_config.py
from datetime import datetime
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
templates.env.globals["now"] = datetime.now  # Add this line
```

**Prevention:**
- Add all global functions in templates_config.py
- Use central templates instance (see E004)
- Test all templates in development
- Add to application template

**Related Errors:** E013 (blank footer), E015 (function undefined)

---

### E012: 'form' is undefined

**Error Message:** `UndefinedError: 'form' is undefined`

**Symptoms:**
- POST routes work (form submission)
- GET routes fail (initial page load)
- Error appears when loading form page
- Form renders on POST but not GET
- Works after submission, fails on first visit

**Root Cause:**
Template expects `form` in context, but GET route doesn't provide it. POST routes create form from request, but GET routes must explicitly pass empty form.

**Fix:**
Pass empty form dict in GET route:

```python
# WRONG
@router.get("/items/new")
async def new_item(request: Request):
    return templates.TemplateResponse("items/new.html", {
        "request": request
    })

# RIGHT
@router.get("/items/new")
async def new_item(request: Request):
    return templates.TemplateResponse("items/new.html", {
        "request": request,
        "form": {}  # Add empty form for GET
    })
```

**Prevention:**
- Always pass `form={}` in GET routes with forms
- Template should handle missing form gracefully
- Add to route template
- Grep check: `grep -rn "TemplateResponse" app/ | grep "new.html"`

**Related Errors:** E019 (form field empty)

---

### E013: 500 with blank footer

**Error Message:** `UndefinedError` or blank space in footer

**Symptoms:**
- Page loads partially
- Footer shows blank space or error
- Error handler catches exception but footer broken
- Content displays but footer missing
- Inconsistent - some pages work, error pages fail

**Root Cause:**
Error handler template doesn't have access to global variables (like `app_version`) that footer expects. Error handler creates separate template context without globals.

**Fix:**
Pass globals explicitly in error handler:

```python
# In error handler
return templates.TemplateResponse(
    "error.html",
    {
        "request": request,
        "error": error,
        "app_version": settings.APP_VERSION,  # Explicit pass
        "now": datetime.now,
    },
    status_code=500
)
```

Or ensure templates_config.py globals are set (see E011).

**Prevention:**
- Use templates_config.py with globals
- Test error pages specifically
- Add to testing checklist
- Verify footer renders on all page types

**Related Errors:** E011 ('now' undefined)

---

### E015: Template shows HTTP request not domain object

**Error Message:** No error, but template displays wrong data

**Symptoms:**
- Template shows Request object properties instead of domain object
- Variables display as `<Request object>` in HTML
- Template iteration shows Request attributes
- Data looks correct in debugger, wrong in template
- Confusing variable names in code

**Root Cause:**
Variable named `request` shadows the FastAPI Request object in template context. When domain object named `request` (e.g., maintenance request), template accesses HTTP Request instead.

**Fix:**
Use descriptive variable names, never generic `request`:

```python
# WRONG
maint_request = get_maintenance_request(id)
return templates.TemplateResponse("view.html", {
    "request": maint_request  # Shadows FastAPI Request!
})

# RIGHT
maint_request = get_maintenance_request(id)
return templates.TemplateResponse("view.html", {
    "request": request,  # FastAPI Request
    "maint_request": maint_request  # Domain object
})
```

**Prevention:**
- NEVER name variables `request` in templates
- Use descriptive names: `booking`, `maint_request`, `order`
- Add linter rule
- Code review checklist item

**Related Errors:** E018 ('int' object has no attribute)

---

### E016: Admin sidebar missing

**Error Message:** No error, but admin sidebar not rendered

**Symptoms:**
- Admin pages load
- Sidebar navigation missing
- Content displays correctly
- Sidebar shows on non-admin pages
- Template inheritance seems broken

**Root Cause:**
Template uses wrong block name. Admin layout expects `{% block admin_content %}`, but template uses `{% block content %}` (standard layout block).

**Fix:**
Use correct block name in admin templates:

```html
<!-- WRONG -->
{% extends "base.html" %}
{% block content %}
  <!-- Admin content here -->
{% endblock %}

<!-- RIGHT -->
{% extends "admin_base.html" %}
{% block admin_content %}
  <!-- Admin content here -->
{% endblock %}
```

**Prevention:**
- Use correct base template for each section
- Admin pages extend `admin_base.html`
- Tenant pages extend `base.html`
- Document template hierarchy

**Related Errors:** None directly related

---

## Authentication & OAuth Errors

### E021: Login always fails

**Error Message:** `Invalid credentials` or password check fails

**Symptoms:**
- Correct credentials rejected
- Login form validation passes
- Database has user with correct email
- Password hash check always returns false
- Test users can't login

**Root Cause:**
Duplicate `hash_password()` function in multiple files (e.g., both `auth.py` and `routes/users.py`). Registration uses one hash function, login uses different hash function. Hashes don't match even for correct password.

**Fix:**
Remove duplicate hash functions, use only `auth.py`:

```python
# Delete duplicate in routes/users.py
# Keep only in auth.py

from app.auth import hash_password, verify_password

# Use auth.py functions everywhere
```

Search for duplicates: `grep -rn "def hash_password" app/`

**Prevention:**
- ONE auth module for all auth functions
- Import from auth.py, never redefine
- Add to code review checklist
- Grep check for duplicate functions

**Related Errors:** E022 (login loops)

---

### E022: Login loops back immediately

**Error Message:** No error, but endless login loop

**Symptoms:**
- User enters credentials
- Login appears successful (brief flash)
- Immediately redirected back to login
- No session cookie set
- OAuth flow completes but doesn't persist

**Root Cause:**
OAuth state cookie and auth session cookie have same name. OAuth uses cookie for CSRF protection, auth uses cookie for session. When names conflict, auth cookie is overwritten by OAuth state cookie, losing authentication.

**Fix:**
Use separate cookie names:

```python
# settings.py
SESSION_COOKIE_NAME = "auth_session"  # Auth cookie
OAUTH_STATE_COOKIE_NAME = "oauth_state"  # OAuth CSRF cookie

# Verify they're different
assert SESSION_COOKIE_NAME != OAUTH_STATE_COOKIE_NAME
```

**Prevention:**
- ALWAYS use different cookie names for OAuth and auth
- Document in authentication-patterns
- Add to OAuth implementation checklist
- Test OAuth flow thoroughly

**Related Errors:** E002 (session_token undefined), E023 (OAuth 400)

---

### E023: Google OAuth 400 private IP

**Error Message:** `OAuth error: invalid_request` or `400 Bad Request`

**Symptoms:**
- OAuth works on localhost
- OAuth fails on private IP (192.168.x.x)
- Google OAuth rejects redirect URI
- "redirect_uri_mismatch" error
- Works with public domain, fails with IP

**Root Cause:**
Google OAuth rejects private IP addresses (192.168.x.x, 10.x.x.x) as redirect URIs for security reasons. Only allows localhost, 127.0.0.1, or public domains.

**Fix:**
Use localhost for testing, public domain for production:

```python
# Development (local testing)
BASE_URL = "http://localhost:8008"

# Production (public domain)
BASE_URL = "https://app.example.com"

# NOT ALLOWED by Google
BASE_URL = "http://192.168.1.100:8008"  # Will fail
```

**Prevention:**
- Use localhost for local development
- Use public domain for production
- Configure OAuth redirect URIs correctly in Google Console
- Document in authentication-patterns

**Related Errors:** E024 (internal access issues)

---

### E024: Internal access shows router page

**Error Message:** No error, but shows router admin page

**Symptoms:**
- External access works (mobile data)
- Internal access shows router page
- URL correct, DNS correct
- Happens after HTTPS setup
- Only affects internal network users

**Root Cause:**
Hairpin NAT not supported by router. When internal client accesses public IP, router doesn't loop traffic back internally. Instead shows router admin interface on port 443.

**Fix:**
Add hosts file entry for internal users:

```
# Add to C:\Windows\System32\drivers\etc\hosts (requires admin)
192.168.1.100    app.example.com
```

This bypasses DNS and routes to internal IP directly.

**Prevention:**
- Document hosts file workaround
- Add to deployment checklist
- Test from internal network
- Provide batch script for hosts file update

**Related Errors:** E025 (access denied modifying hosts)

---

### E025: "Access denied" modifying hosts

**Error Message:** `Access is denied` when running hosts file batch script

**Symptoms:**
- Batch script runs
- Fails at hosts file modification
- "Access denied" error
- Script doesn't elevate to admin
- Manually works as admin

**Root Cause:**
Batch script missing auto-elevation pattern. Hosts file modification requires Administrator privileges, but script runs as normal user.

**Fix:**
Add auto-elevation to batch script:

```batch
@echo off
setlocal EnableDelayedExpansion

:: Check for Administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting Administrator privileges...
    powershell -Command "Start-Process -Verb RunAs -FilePath '%~f0'"
    exit /b
)

:: Now running as admin, proceed with hosts modification
```

**Prevention:**
- ALL scripts modifying hosts MUST auto-elevate
- Use auto-elevation template from installer-patterns.md
- Test as normal user
- Add to batch script template

**Related Errors:** E024 (hairpin NAT workaround)

---

## Routing & Database Errors

### E031: 422 on /new endpoint

**Error Message:** `422 Unprocessable Entity` when accessing /items/new

**Symptoms:**
- /items/new returns 422 error
- /items/{id} works fine
- URL looks correct
- FastAPI treats "new" as {id} parameter
- Other routes work normally

**Root Cause:**
Route ordering wrong. FastAPI matches routes in order defined. If `/{id}` route defined before `/new` route, FastAPI matches "new" as an ID parameter and fails validation (expects integer, gets string).

**Fix:**
Define static routes (`/new`) BEFORE parameterized routes (`/{id}`):

```python
# WRONG ORDER
@router.get("/{id}")
async def get_item(id: int):
    ...

@router.get("/new")  # Never reached! "new" matches /{id}
async def new_item():
    ...

# RIGHT ORDER
@router.get("/new")  # Static route first
async def new_item():
    ...

@router.get("/{id}")  # Parameterized route after
async def get_item(id: int):
    ...
```

**Prevention:**
- Always define static routes before parameterized routes
- Document route ordering rules
- Add to code review checklist
- Grep check: Verify /new before /{id} in all routers

**Related Errors:** None directly related

---

### E032: ORDER BY expected, got property

**Error Message:** `AttributeError: ORDER BY expression expected, got property`

**Symptoms:**
- Query with ORDER BY fails
- Works without ORDER BY
- Model has @property decorator
- Trying to sort by calculated field
- SQLAlchemy query error

**Root Cause:**
Attempting to use `@property` decorated method in SQLAlchemy ORDER BY clause. SQLAlchemy ORDER BY requires actual Column objects, not Python properties.

**Fix:**
Use actual column fields for ORDER BY:

```python
# Model with property
class Item(Base):
    __tablename__ = "items"
    name = Column(String)
    price = Column(Float)

    @property
    def display_name(self):
        return f"{self.name} (${self.price})"

# WRONG - can't order by property
items = session.query(Item).order_by(Item.display_name).all()

# RIGHT - order by actual column
items = session.query(Item).order_by(Item.name).all()
```

**Prevention:**
- Only use Column fields in ORDER BY
- Properties are for display/calculation only
- Add type hints to distinguish
- Document in data model patterns

**Related Errors:** E027 (AttributeError on model field)

---

### E033: "no such column" after model change

**Error Message:** `OperationalError: no such column: items.new_field`

**Symptoms:**
- Model updated with new field
- Code references new field
- Database query fails
- SQLite database doesn't have column
- Works on fresh database

**Root Cause:**
Added field to Python model but didn't run database migration. Existing database lacks the new column.

**Fix:**
Run ALTER TABLE to add column:

```sql
-- For SQLite
ALTER TABLE items ADD COLUMN new_field TEXT;

-- Or in Python
from sqlalchemy import text
with engine.begin() as conn:
    conn.execute(text("ALTER TABLE items ADD COLUMN new_field TEXT"))
```

**Prevention:**
- Create migration script for schema changes
- Document migration in CHANGELOG.md
- Test on production-like database
- Add to deployment checklist

**Related Errors:** None directly related

---

## Implementation Errors

### E034: "Coming Soon" in production

**Error Message:** No error, but placeholder text visible

**Symptoms:**
- "Coming Soon" text in production
- Feature partially implemented
- Broken links to unfinished features
- Users report missing functionality
- Incomplete CRUD operations

**Root Cause:**
Shipped application with incomplete features. Implemented UI without backend, or backend without UI.

**Fix:**
Complete ALL features before shipping:

1. Hide unfinished features (remove from navigation)
2. OR complete the feature fully
3. OR mark clearly as "Beta" with warning

**Prevention:**
- NEVER ship with "Coming Soon" placeholders
- Complete features end-to-end before adding to navigation
- Use feature flags for partial features
- Pre-delivery audit checklist

**Related Errors:** E035 (drag/reorder not working)

---

### E035: Drag/reorder not working

**Error Message:** No error, but drag-drop doesn't persist

**Symptoms:**
- Drag-drop UI works visually
- Order resets on page refresh
- No save button visible
- Dragging items doesn't persist
- Looks complete but doesn't function

**Root Cause:**
Incomplete CRUD implementation. Implemented drag-drop UI (front-end) without reorder endpoint (back-end) or auto-save logic.

**Fix:**
Implement complete reorder functionality:

1. Create reorder endpoint
2. Add auto-save on drag-drop
3. Show save confirmation
4. Test persistence

```python
@router.post("/reorder")
async def reorder_items(order: List[int], db: Session):
    for index, item_id in enumerate(order):
        item = db.query(Item).get(item_id)
        item.sort_order = index
    db.commit()
    return {"status": "ok"}
```

**Prevention:**
- Complete BOTH front-end AND back-end for features
- Test all CRUD operations
- Verify persistence in database
- Add to feature completion checklist

**Related Errors:** E034 ("Coming Soon" in production)

---

### E036: Multi-tenant features broken

**Error Message:** Various - data leaks between tenants

**Symptoms:**
- User sees data from other organizations
- Data isolation broken
- Queries return all organizations' data
- Filters don't work consistently
- Security violation

**Root Cause:**
Application designed as single-tenant initially, then multi-tenant features added without proper data isolation. Queries don't filter by organization ID consistently.

**Fix:**
Redesign from start for multi-tenancy:

1. Add organization_id to ALL tables
2. Add organization filter to ALL queries
3. Use middleware to auto-filter
4. Verify data isolation with tests

**Prevention:**
- Design for multi-tenant from day ONE
- NEVER add multi-tenant as afterthought
- Test data isolation thoroughly
- Implement tenant middleware early

**Related Errors:** None directly related (serious design issue)

---

## Reserved Error Numbers

**E037-E040:** Reserved for future common errors

As new errors are encountered and patterns emerge, they will be documented here with the same format:
- Error message
- Symptoms
- Root cause
- Fix
- Prevention
- Related errors

---

*End of Error Catalog*
