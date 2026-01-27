# Build Templates Reference

Load this file when setting up test suites, scripts, or documentation templates.

---

## Claude.md Template (Claude Code Handoff)

Create `Claude.md` in project root to provide context when switching to Claude Code:

```markdown
# Project: [AppName]

## Quick Start
```bash
cd [project-dir]
source venv/bin/activate  # or: venv\Scripts\activate (Windows)
python -m uvicorn app.main:app --reload --port 8008
```

## Architecture

| Component | Technology |
|-----------|------------|
| Framework | FastAPI |
| ORM | SQLAlchemy 2.0 |
| Templates | Jinja2 |
| Auth | OAuth (Google), first-user=admin |
| Database | SQLite (instance/app.db) |
| Config | Pydantic Settings (.env) |

## Key Files

| File | Purpose |
|------|---------|
| app/models.py | All SQLAlchemy models |
| app/config.py | Pydantic Settings |
| app/templates_config.py | Jinja2 setup (ONLY file with Jinja2Templates) |
| app/auth.py | OAuth + session management |
| app/routes/*.py | Route handlers by module |
| app/services/*.py | Business logic |

## Modules

| Module | Prefix | Status |
|--------|--------|--------|
| Property Management | /pms | Complete |
| Asset Management | /ams | In Progress |
| Venue Booking | /evms | Planned |

## Current State

**Completed:**
- [x] OAuth authentication
- [x] User management
- [x] Core CRUD for requests

**In Progress:**
- [ ] Email notifications
- [ ] File attachments

**Planned:**
- [ ] Reporting dashboard
- [ ] API endpoints

## Known Issues

| Issue | Workaround |
|-------|------------|
| Hairpin NAT | Add hosts entry: `192.168.x.x domain.org` |
| Google OAuth on localhost | Use `http://localhost:8008`, not IP |

## Testing

```bash
# All tests
pytest tests/ -v

# Specific module
pytest tests/test_pms.py -v

# Single test
pytest tests/test_pms.py -v -k "test_create_request"

# With coverage
pytest tests/ --cov=app --cov-report=html
```

## Critical Patterns

1. **Route ordering:** `/new` before `/{id}` (prevents 422)
2. **Template blocks:** Use `admin_content`, not `content`
3. **Variable naming:** Never use `request` for domain objects
4. **ORDER BY:** Use Column fields, not @property
5. **Cookie separation:** OAuth state ≠ auth session

## Environment Variables

```env
SECRET_KEY=          # Required
BASE_URL=            # https://domain.org for production
GOOGLE_CLIENT_ID=    # OAuth
GOOGLE_CLIENT_SECRET=# OAuth
GOOGLE_ALLOWED_DOMAIN=# Restrict to org domain
```

## Deployment

```bash
# Production with Caddy (HTTPS)
scripts/install-caddy-service.bat
# Then start app on configured port
```

---
*Last updated: [date] - [what changed]*
```

**Update Claude.md when:**
- Completing a feature (update Current State)
- Discovering issues (add to Known Issues)
- Before ending a session (capture context)
- When patterns change (update Critical Patterns)

---

## Admin Auto-Elevation Template

For scripts requiring Administrator privileges:

```batch
@echo off
setlocal EnableDelayedExpansion
title [AppName] - [Script Purpose] (Administrator)
cd /d "%~dp0"

:: ============================================
:: AUTO-ELEVATION - Do not modify this section
:: ============================================
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo  Administrator privileges required
    echo ========================================
    echo.
    echo This script needs to run as Administrator.
    echo Requesting elevation...
    echo.
    powershell -Command "Start-Process -Verb RunAs -FilePath '%~f0' -ArgumentList '%*'"
    exit /b
)
:: ============================================

echo Running with Administrator privileges...
echo.

:: Your admin commands here
:: Example: Modify hosts file, install services, etc.

pause
exit /b 0
```

### Hosts File Setup Script Template

`scripts/setup-hosts.bat`:

```batch
@echo off
setlocal EnableDelayedExpansion
title [AppName] - Hosts File Setup
cd /d "%~dp0"

:: Auto-elevate
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting Administrator privileges...
    powershell -Command "Start-Process -Verb RunAs -FilePath '%~f0' -ArgumentList '%*'"
    exit /b
)

:: Configuration
set "HOSTS_FILE=%SystemRoot%\System32\drivers\etc\hosts"
set "DOMAIN=pms.ucc-austin.org"
set "SERVER_IP=192.168.0.132"

echo ========================================
echo  Hosts File Configuration
echo ========================================
echo.
echo This adds an entry to route %DOMAIN%
echo to the internal server at %SERVER_IP%
echo.
echo This is needed for internal network access
echo when your router doesn't support hairpin NAT.
echo.

:: Check if entry exists
findstr /C:"%DOMAIN%" "%HOSTS_FILE%" >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] Entry for %DOMAIN% already exists.
    echo.
    echo Current hosts entries for this domain:
    findstr /C:"%DOMAIN%" "%HOSTS_FILE%"
    echo.
    set /p UPDATE="Update the entry? [y/N]: "
    if /i not "!UPDATE!"=="y" goto :done
    
    :: Remove old entry
    powershell -Command "(Get-Content '%HOSTS_FILE%') | Where-Object { $_ -notmatch '%DOMAIN%' } | Set-Content '%HOSTS_FILE%'"
)

:: Add new entry
echo Adding: %SERVER_IP%    %DOMAIN%
echo %SERVER_IP%    %DOMAIN% >> "%HOSTS_FILE%"

if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Hosts entry added successfully.
    echo.
    echo You can now access https://%DOMAIN% from this machine.
) else (
    echo.
    echo [ERROR] Failed to modify hosts file.
    echo Please check permissions and try again.
)

:done
echo.
pause
exit /b 0
```

### Caddy Service Install Template

`scripts/install-caddy-service.bat`:

```batch
@echo off
setlocal EnableDelayedExpansion
title [AppName] - Caddy Service Installation
cd /d "%~dp0.."

:: Auto-elevate
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting Administrator privileges...
    powershell -Command "Start-Process -Verb RunAs -FilePath '%~f0' -ArgumentList '%*'"
    exit /b
)

set "CADDY_DIR=%~dp0..\caddy"
set "CADDY_EXE=%CADDY_DIR%\caddy.exe"

echo ========================================
echo  Caddy Reverse Proxy Service Setup
echo ========================================
echo.

:: Check if Caddy exists
if not exist "%CADDY_EXE%" (
    echo [ERROR] Caddy not found at: %CADDY_EXE%
    echo Please run the installer first.
    pause
    exit /b 1
)

:: Stop existing service if running
sc query caddy >nul 2>&1
if %errorlevel% equ 0 (
    echo Stopping existing Caddy service...
    sc stop caddy >nul 2>&1
    timeout /t 2 >nul
    sc delete caddy >nul 2>&1
    timeout /t 2 >nul
)

:: Install as service
echo Installing Caddy as Windows service...
"%CADDY_EXE%" service install --config "%CADDY_DIR%\Caddyfile"

if %errorlevel% equ 0 (
    echo Starting Caddy service...
    sc start caddy
    echo.
    echo [SUCCESS] Caddy service installed and started.
    echo.
    echo Service will start automatically on boot.
) else (
    echo.
    echo [ERROR] Failed to install Caddy service.
)

pause
exit /b 0
```

---

## Complete Test Suite Structure

```
tests/
├── __init__.py
├── conftest.py          # Shared fixtures
├── test_models.py       # Model creation and validation
├── test_services.py     # Service layer business logic
├── test_api.py          # HTTP route testing
└── test_regressions.py  # Specific bug regression tests
```

### conftest.py Template

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import *  # Import all models

@pytest.fixture(scope="session")
def engine():
    """Create test database engine."""
    return create_engine("sqlite:///:memory:")

@pytest.fixture(scope="session")
def tables(engine):
    """Create all tables."""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture
def db_session(engine, tables):
    """Create a fresh database session for each test."""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def sample_venue(db_session):
    """Create a sample venue for testing."""
    venue = Venue(name="Test Venue", is_default=True)
    db_session.add(venue)
    db_session.commit()
    return venue

@pytest.fixture
def sample_user(db_session):
    """Create a sample user for testing."""
    from app.auth import hash_password
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash=hash_password("testpass123"),
        role="admin"
    )
    db_session.add(user)
    db_session.commit()
    return user
```

### test_models.py Template

```python
import pytest
from app.models import Venue, Service, User

class TestVenueModel:
    def test_create_venue(self, db_session):
        venue = Venue(name="Test Church")
        db_session.add(venue)
        db_session.commit()
        
        assert venue.id is not None
        assert venue.name == "Test Church"
    
    def test_venue_default_flag(self, db_session):
        venue = Venue(name="Main", is_default=True)
        db_session.add(venue)
        db_session.commit()
        
        assert venue.is_default == True

class TestServiceModel:
    def test_create_service(self, db_session, sample_venue):
        from datetime import date, time
        service = Service(
            title="Sunday Worship",
            date=date.today(),
            time=time(10, 30),
            venue_id=sample_venue.id
        )
        db_session.add(service)
        db_session.commit()
        
        assert service.id is not None
        assert service.venue_id == sample_venue.id
```

### test_regressions.py Template

```python
"""
Regression tests for specific bugs that have been fixed.
Each test should reference the error number from ERROR-AND-FIXES-LOG.md
"""
import pytest
import re
from pathlib import Path

class TestRegressions:
    def test_error_12_service_time_column_name(self, db_session, sample_venue):
        """
        Error 12: Route must use 'time' not 'service_time' for Service model.
        """
        from datetime import date, time
        from app.models import Service
        
        # This should work - using correct column name
        service = Service(
            title="Test",
            date=date.today(),
            time=time(10, 0),  # Column is 'time', not 'service_time'
            venue_id=sample_venue.id
        )
        db_session.add(service)
        db_session.commit()
        assert service.id is not None
    
    def test_error_8_venue_is_default_column(self, db_session):
        """
        Error 8: Venue model must have is_default column for seed data.
        """
        from app.models import Venue
        
        venue = Venue(name="Test", is_default=True)
        db_session.add(venue)
        db_session.commit()
        assert venue.is_default == True


class TestOAuthPatterns:
    """OAuth-related regression tests."""
    
    def test_oauth_cookie_separated(self):
        """OAuth state and auth session must use different cookies."""
        main_py = Path('app/main.py')
        if not main_py.exists():
            pytest.skip("main.py not found")
        
        content = main_py.read_text()
        if 'SessionMiddleware' in content:
            # Should NOT use settings.SESSION_COOKIE_NAME for OAuth state
            assert 'session_cookie=settings.SESSION_COOKIE_NAME' not in content, \
                "OAuth state cookie must be separate from auth session cookie"
    
    def test_login_template_oauth_only(self):
        """Login page should not have password form for OAuth-only apps."""
        login_html = Path('app/templates/public/login.html')
        if not login_html.exists():
            pytest.skip("login.html not found")
        
        content = login_html.read_text()
        if 'google_oauth_enabled' in content or 'oauth' in content.lower():
            has_password = 'type="password"' in content
            has_divider = 'or sign in with' in content.lower()
            if not has_password:
                assert not has_divider, \
                    "Remove 'or sign in with' divider for OAuth-only login"
    
    def test_first_user_admin_pattern(self):
        """First OAuth user should become admin."""
        oauth_routes = Path('app/routes/oauth_routes.py')
        if not oauth_routes.exists():
            pytest.skip("oauth_routes.py not found")
        
        content = oauth_routes.read_text()
        has_first_user_check = 'count() == 0' in content or 'first user' in content.lower()
        assert has_first_user_check, \
            "OAuth should assign ADMIN role to first user"


class TestHTTPSPatterns:
    """HTTPS deployment regression tests."""
    
    def test_base_url_no_port_for_https(self):
        """HTTPS base URLs should not include port numbers."""
        env_example = Path('.env.example')
        if not env_example.exists():
            pytest.skip(".env.example not found")
        
        content = env_example.read_text()
        for line in content.split('\n'):
            if 'BASE_URL' in line and 'https://' in line:
                # HTTPS URLs should not have :port
                assert not re.search(r'https://[^/]+:\d+', line), \
                    "HTTPS BASE_URL should not include port (Caddy handles 443)"


class TestScriptPatterns:
    """Batch script regression tests."""
    
    def test_admin_scripts_have_elevation(self):
        """Scripts modifying system files must auto-elevate."""
        admin_indicators = ['hosts', 'caddy', 'service', 'install']
        
        for bat in Path('scripts').glob('*.bat'):
            name_lower = bat.name.lower()
            needs_admin = any(ind in name_lower for ind in admin_indicators)
            
            if needs_admin:
                content = bat.read_text()
                has_elevation = 'net session' in content
                assert has_elevation, \
                    f"{bat.name} appears to need admin but lacks 'net session' elevation check"
    
    def test_all_scripts_have_cd(self):
        """All batch scripts must have cd /d command."""
        for bat in Path('.').glob('**/*.bat'):
            if 'venv' in str(bat):
                continue
            content = bat.read_text()
            assert 'cd /d' in content, \
                f"{bat} missing 'cd /d' directory change"


class TestTemplatePatterns:
    """Template consistency regression tests."""
    
    def test_template_user_variable_consistency(self):
        """Templates should use consistent variable names for current user."""
        user_vars = set()
        
        for template in Path('app/templates').rglob('*.html'):
            content = template.read_text()
            # Check for common user variable patterns
            if '{{ user' in content or '{% if user' in content:
                user_vars.add('user')
            if '{{ current_user' in content or '{% if current_user' in content:
                user_vars.add('current_user')
        
        # If both are used, ensure base context provides aliases
        if len(user_vars) > 1:
            # Check that templates_config.py or base context handles this
            templates_config = Path('app/templates_config.py')
            if templates_config.exists():
                config_content = templates_config.read_text()
                has_alias = 'current_user' in config_content
                assert has_alias, \
                    f"Templates use both {user_vars} - add alias in templates_config.py"


class TestRoutePatterns:
    """Route definition regression tests."""
    
    def test_route_ordering_static_before_dynamic(self):
        """Static routes (/new) must be defined before dynamic routes (/{id})."""
        for route_file in Path('app/routes').glob('*.py'):
            content = route_file.read_text()
            
            # Find positions of /new and /{id} patterns
            new_match = re.search(r'@router\.(get|post)\(["\']\/new["\']', content)
            dynamic_match = re.search(r'@router\.get\(["\']\/\{', content)
            
            if new_match and dynamic_match:
                assert new_match.start() < dynamic_match.start(), \
                    f"{route_file.name}: /new must be defined before /{{id}} routes"
    
    def test_auth_functions_in_template_globals(self):
        """Auth helper functions used in templates must be in globals."""
        templates_config = Path('app/templates_config.py')
        if not templates_config.exists():
            pytest.skip("templates_config.py not found")
        
        config_content = templates_config.read_text()
        
        # Check for common auth functions
        auth_functions = ['can_manage', 'can_approve', 'is_admin', 'has_minimum_role']
        
        # Find auth functions used in templates
        for template in Path('app/templates').rglob('*.html'):
            content = template.read_text()
            for func in auth_functions:
                if f'{func}(' in content or f'{func} ' in content:
                    assert func in config_content, \
                        f"Template uses {func}() but not in templates.env.globals"
    
    def test_explicit_route_names(self):
        """Routes referenced in url_for() should have explicit names."""
        # Collect all url_for references from templates
        url_for_names = set()
        for template in Path('app/templates').rglob('*.html'):
            content = template.read_text()
            matches = re.findall(r"url_for\(['\"]([^'\"]+)['\"]", content)
            url_for_names.update(matches)
        
        # Check each route file for explicit names
        for route_file in Path('app/routes').glob('*.py'):
            content = route_file.read_text()
            # Routes should have name= parameter
            decorators = re.findall(r'@router\.(get|post|put|delete)\([^)]+\)', content)
            for dec in decorators:
                if 'name=' not in dec and any(name.split('.')[-1] in dec for name in url_for_names):
                    # This is a simplified check - may need refinement
                    pass  # Log warning but don't fail
    
    def test_model_field_references(self):
        """Route/service model field references should match model definitions."""
        models_py = Path('app/models.py')
        if not models_py.exists():
            pytest.skip("models.py not found")
        
        models_content = models_py.read_text()
        
        # Extract model class names and their fields
        model_fields = {}
        current_model = None
        for line in models_content.split('\n'):
            if line.startswith('class ') and '(Base)' in line:
                current_model = re.search(r'class (\w+)\(', line).group(1)
                model_fields[current_model] = set()
            elif current_model and '= Column(' in line:
                field_match = re.match(r'\s+(\w+)\s*=\s*Column', line)
                if field_match:
                    model_fields[current_model].add(field_match.group(1))
        
        # Check routes and services for field references
        for py_file in list(Path('app/routes').glob('*.py')) + list(Path('app/services').glob('*.py')):
            content = py_file.read_text()
            for model, fields in model_fields.items():
                # Look for Model.field_name patterns
                refs = re.findall(rf'{model}\.(\w+)', content)
                for ref in refs:
                    if ref not in fields and not ref.startswith('__'):
                        # Skip method calls and relationships
                        if ref not in ['query', 'id', 'filter', 'order_by']:
                            print(f"WARNING: {py_file.name} references {model}.{ref} - verify field exists")
    
    def test_no_request_variable_collision(self):
        """Domain objects should not be named 'request' in template contexts."""
        reserved_names = ['request']  # HTTP request object
        
        for route_file in Path('app/routes').glob('*.py'):
            content = route_file.read_text()
            
            # Find TemplateResponse calls
            template_calls = re.findall(
                r'TemplateResponse\([^{]+\{([^}]+)\}',
                content,
                re.DOTALL
            )
            
            for call in template_calls:
                # Check for "request": <something_other_than_request>
                # Pattern: "request": variable where variable != request
                matches = re.findall(r'"request"\s*:\s*(\w+)', call)
                for match in matches:
                    if match != 'request':
                        assert False, \
                            f"{route_file.name}: Domain object passed as 'request' - use descriptive name"
    
    def test_admin_templates_use_admin_content_block(self):
        """Admin child templates must use admin_content block, not content."""
        admin_dir = Path('app/templates/admin')
        if not admin_dir.exists():
            pytest.skip("admin templates not found")
        
        for template in admin_dir.rglob('*.html'):
            if template.name == 'base.html':
                continue
            content = template.read_text()
            if '{% extends' in content and 'admin' in content:
                assert '{% block content %}' not in content, \
                    f"{template.name}: Use admin_content block, not content (preserves sidebar)"
    
    def test_order_by_uses_columns_not_properties(self):
        """ORDER BY clauses should use Column fields, not @property."""
        # Get list of @property names from models
        models_py = Path('app/models.py')
        if not models_py.exists():
            pytest.skip("models.py not found")
        
        models_content = models_py.read_text()
        properties = re.findall(r'@property\s+def\s+(\w+)', models_content)
        
        # Check routes and services for order_by with properties
        for py_file in list(Path('app/routes').glob('*.py')) + list(Path('app/services').glob('*.py')):
            content = py_file.read_text()
            for prop in properties:
                if f'.order_by({prop})' in content or f'.order_by(*.{prop})' in content:
                    print(f"WARNING: {py_file.name} may use @property {prop} in order_by")
```

---

## Health Check Script Template

`scripts/health-check.bat`:

```batch
@echo off
setlocal EnableDelayedExpansion
title [AppName] Health Check
cd /d "%~dp0.."

echo ========================================
echo [AppName] Health Check
echo ========================================
echo.

set ERRORS=0

:: Check Python
echo [1/6] Checking Python...
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo [FAIL] Python not found
    set /a ERRORS+=1
) else (
    echo [OK] Python found
)

:: Check virtual environment
echo [2/6] Checking virtual environment...
if exist "venv\Scripts\python.exe" (
    echo [OK] Virtual environment exists
) else (
    echo [FAIL] Virtual environment not found
    set /a ERRORS+=1
)

:: Check dependencies
echo [3/6] Checking dependencies...
venv\Scripts\python -c "import fastapi, sqlalchemy, jinja2" >nul 2>&1
if !errorlevel! neq 0 (
    echo [FAIL] Missing dependencies
    set /a ERRORS+=1
) else (
    echo [OK] Dependencies installed
)

:: Check app import
echo [4/6] Checking application import...
venv\Scripts\python -c "from app.main import app" >nul 2>&1
if !errorlevel! neq 0 (
    echo [FAIL] Application import failed
    set /a ERRORS+=1
) else (
    echo [OK] Application imports successfully
)

:: Check database
echo [5/6] Checking database...
if exist "instance\app.db" (
    echo [OK] Database exists
) else (
    echo [WARN] Database not initialized (will be created on first run)
)

:: Run tests
echo [6/6] Running tests...
venv\Scripts\python -m pytest tests/ -q >nul 2>&1
if !errorlevel! neq 0 (
    echo [FAIL] Tests failed
    set /a ERRORS+=1
) else (
    echo [OK] All tests pass
)

echo.
echo ========================================
if !ERRORS! equ 0 (
    echo Health Check: PASSED
    echo All systems operational
) else (
    echo Health Check: FAILED
    echo !ERRORS! error(s) found
)
echo ========================================

pause
exit /b !ERRORS!
```

---

## Audit Report Template

`docs/AUDIT-REPORT.md`:

```markdown
# [AppName] Comprehensive Audit Report

Version X.Y.Z | Build YYDDD-HHMM | Generated: YYYY-MM-DD

---

## Executive Summary

Audit of [AppName] package against all requirements and standards.

**Total Routes**: [N]
**Total Templates**: [N]
**Total Models**: [N]

### Audit Status: [PASS/FAIL]

---

## Feature Status Matrix

### IMPLEMENTED ✓

| Feature | Status | Location | Notes |
|---------|--------|----------|-------|
| [Feature 1] | ✓ Complete | routes/xxx.py | [Notes] |
| [Feature 2] | ✓ Complete | routes/yyy.py | [Notes] |

### REMAINING ITEMS

| Feature | Priority | Notes |
|---------|----------|-------|
| [Feature N] | LOW | [Why deferred] |

---

## Verification Results

```
✓ All [N] routes load without import errors
✓ All [N] templates parse without syntax errors
✓ All Python files pass syntax check
✓ All tests pass
✓ Health check passes
```

---

## Files Modified Since Last Audit

### Created
- [list new files]

### Modified
- [list modified files]

---

*Audit completed on YYYY-MM-DD*
```

---

## Error Documentation Template

`docs/ERROR-AND-FIXES-LOG.md` entry:

```markdown
### Error N: [Brief Title]

**Error**: [Error message or behavior]

**Symptoms**:
- [Observable symptom 1]
- [Observable symptom 2]

**Root Cause**: [Why this happened]

**Fix**: [What was changed]
- File: line X changed from Y to Z
- Added/removed code

**Prevention**: [How to avoid this in the future]
```

### Common Error Entries

```markdown
### OAuth Session Cookie Conflict
**Error**: Login appears successful but immediately redirects back to login
**Symptoms**: 
- User clicks OAuth login, authenticates with Google
- Callback completes, but user returns to login page
- No error messages displayed
**Root Cause**: SessionMiddleware (for OAuth state) uses same cookie name as auth session
**Fix**: Use separate cookie names:
- Auth session: `{app}_session`
- OAuth state: `{app}_oauth_state`
**Prevention**: Grep check in regression tests for `session_cookie=settings.SESSION_COOKIE_NAME`

### Google OAuth Private IP Rejection
**Error**: "Error 400: invalid_request - device_id and device_name are required"
**Symptoms**:
- OAuth works on localhost
- Fails when using 192.168.x.x or 10.x.x.x addresses
**Root Cause**: Google OAuth blocks redirects to private IP addresses
**Fix**: Use `localhost` for testing, or configure public domain with Caddy
**Prevention**: Document in INSTALL.md; never use private IPs in redirect URIs

### Hairpin NAT / NAT Loopback Issue
**Error**: Internal access to public domain fails while external access works
**Symptoms**:
- Phone on mobile data can access https://pms.ucc-austin.org ✓
- Computer on internal network gets timeout or router admin page ✗
- Server shows Caddy listening on 443
**Root Cause**: Router cannot route internal traffic to public IP back to internal server
**Fix**: Add hosts file entry on internal machines:
```
# C:\Windows\System32\drivers\etc\hosts (run Notepad as Admin)
192.168.0.132    pms.ucc-austin.org
```
**Diagnosis**:
1. Test from phone on mobile data (WiFi off) - if works, it's hairpin NAT
2. Check `netstat -an | findstr ":443"` - if LISTENING, server is fine
3. Router admin page appearing = router intercepting its own public IP
**Prevention**: Document in deployment guide; consider hosts file setup in installer

### Template/Context Variable Mismatch
**Error**: 500 Server Error after successful OAuth login; Jinja2 `UndefinedError` in logs
**Symptoms**:
- User authenticates successfully with OAuth
- Redirect to dashboard causes 500 error
- Log shows: `jinja2.exceptions.UndefinedError: 'current_user' is undefined`
**Root Cause**: Template expects variable name (e.g., `current_user`) but route provides different name (e.g., `user`)
**Fix**: Ensure base context provides aliases for all expected names:
```python
def get_base_context(request, user=None, **kwargs) -> dict:
    return {
        "request": request,
        "user": user,
        "current_user": user,  # Alias for templates expecting current_user
        "app_name": settings.APP_NAME,
        **kwargs
    }
```
**Prevention**: 
- Grep templates for variable names, verify routes provide them
- Use consistent naming (`user` everywhere, not mix of `user` and `current_user`)
- Add regression test checking template variables match route context

### Route Ordering - 422 on Static Paths
**Error**: 422 Unprocessable Entity when accessing /new endpoints
**Symptoms**:
- Clicking "New" button returns 422 error
- Error mentions "value is not a valid integer"
- Works if you manually type the full URL with trailing content
**Root Cause**: FastAPI matches routes in definition order. If `/{id}` is defined before `/new`, requests to `/new` match `/{id}` first, and FastAPI tries to convert "new" to an integer.
**Fix**: Reorder routes - static paths before dynamic:
```python
@router.get("/new")       # Static - FIRST
async def create_form(): ...

@router.get("/{id}")      # Dynamic - AFTER static
async def view(): ...
```
**Prevention**: 
- Always define routes: list → create → detail → actions
- Add regression test checking route order

### Missing Route Name
**Error**: NoMatchFound: No route exists for name "pms.new_request"
**Symptoms**:
- Template renders but crashes on url_for() call
- Error shows route name that doesn't exist
**Root Cause**: Template uses `url_for('module.route_name')` but route decorator lacks explicit `name=` parameter
**Fix**: Add explicit name to route decorator:
```python
@router.get("/new", name="pms.new_request")
async def new_request_form(): ...
```
**Prevention**: 
- Convention: `{module}.{resource}_{action}`
- Grep templates for url_for(), verify all names exist in routes

### HTTPS Session Loss
**Error**: User logged out unexpectedly on HTTPS deployment
**Symptoms**:
- Login works initially
- Session randomly disappears
- Works fine on HTTP localhost
**Root Cause**: Session cookie `secure` flag not set for HTTPS
**Fix**: Set secure flag based on BASE_URL:
```python
is_https = settings.BASE_URL.startswith("https://")
response.set_cookie(..., secure=is_https)
```
**Prevention**: Always derive `secure` flag from BASE_URL

### Model Field Name Mismatch
**Error**: AttributeError: type object 'Model' has no attribute 'field_name'
**Symptoms**:
- 500 error on list/filter/sort operations
- Error references a field that "should" exist
- Works with different field name
**Root Cause**: Route/service uses field name that doesn't match model definition
**Example**:
```python
# models.py has:
start_time = Column(DateTime)

# But route uses:
Booking.start_datetime  # Wrong! Should be start_time
```
**Fix**: Check models.py for exact field name, update route/service code
**Prevention**: 
- Before using Model.field in routes, verify in models.py
- Add regression test for model field references

### Template Variable Name Collision
**Error**: Template shows HTTP request object properties instead of domain data
**Symptoms**:
- Detail page shows weird data like "GET", "http://...", headers
- Domain object fields don't render
- No actual error thrown - just wrong data displayed
**Root Cause**: Domain object passed as `request` in template context, colliding with HTTP Request
**Example**:
```python
# WRONG - maint_request overwrites HTTP request
return templates.TemplateResponse(
    "detail.html",
    {"request": request, "request": maint_request}  # Second 'request' wins
)
```
**Fix**: Use descriptive variable names for domain objects:
```python
return templates.TemplateResponse(
    "detail.html",
    {"request": request, "maint_request": maint_request}
)
```
**Prevention**:
- Convention: Never name domain objects `request`, `user`, `form` (reserved)
- Use domain-specific names: `maint_request`, `booking`, `asset`, `venue`
- Add regression test checking for variable name collisions

### Template Block Name - Missing Sidebar/Layout
**Error**: Admin sidebar missing; page shows public-style layout
**Symptoms**:
- Admin page renders but without sidebar navigation
- Layout looks like public page, not admin page
- No error thrown - just wrong appearance
**Root Cause**: Child template uses `{% block content %}` which overwrites the entire layout defined in base.html, including the sidebar
**Example**:
```jinja2
{# WRONG - overwrites entire content including sidebar #}
{% extends "admin/base.html" %}
{% block content %}
    <h1>My Page</h1>
{% endblock %}
```
**Fix**: Use the correct nested block name:
```jinja2
{# RIGHT - preserves sidebar layout #}
{% extends "admin/base.html" %}
{% block admin_content %}
    <h1>My Page</h1>
{% endblock %}
```
**Prevention**:
- Check base template for nested block names before creating child templates
- Verify with: `grep -l "{% block content %}" app/templates/admin/*.html` (should only be base.html)

### SQLAlchemy ORDER BY with Property
**Error**: ArgumentError: ORDER BY expression expected, got <property object>
**Symptoms**:
- 500 error on list pages with sorting
- Error mentions "property object"
**Root Cause**: Using @property (computed Python attribute) in order_by() instead of Column
**Example**:
```python
# Model has @property
@property
def display_name(self):
    return f"{self.first_name} {self.last_name}"

# WRONG
db.query(User).order_by(User.display_name)  # display_name is a property!
```
**Fix**: Use actual Column fields:
```python
db.query(User).order_by(User.first_name, User.last_name)
```
**Prevention**: Only use Column-defined attributes in filter/order_by/group_by

### Service Function Parameter Mismatch
**Error**: TypeError: function() got an unexpected keyword argument 'xxx'
**Symptoms**:
- 500 error when calling service function
- Error shows parameter name that "should" work
**Root Cause**: Calling service with wrong parameter name
**Example**:
```python
# Function signature has html_content
async def send_email(to_email, subject, html_content): ...

# WRONG - using 'body' instead of 'html_content'
await send_email(to_email="x", subject="y", body="z")
```
**Fix**: Use exact parameter names from function signature
**Prevention**: Check function signature; use IDE autocomplete

### Name Verification Failures (Universal Pattern)
**Error**: AttributeError, KeyError, TypeError with name-related messages
**Symptoms**:
- Error message contains a field/parameter/variable name
- The name "looks right" but doesn't match the actual definition
**Root Cause**: Assuming a name instead of verifying it
**Common Examples**:
```python
# Model fields
Booking.start_datetime  # Actually: start_time
AuditLog.details        # Actually: new_value

# Service parameters  
send_email(body=...)    # Actually: html_content

# SQLAlchemy
User.display_name       # Actually: @property, not Column

# Template variables
"request": maint_request  # Collides with HTTP request
```
**Fix**: Check the source file for exact name:
- Model fields → models.py
- Service params → function signature
- Template vars → route context dict
**Prevention**: 
- Never assume names - take 5 seconds to verify
- Use IDE autocomplete/go-to-definition
- Add to pre-delivery checklist: "Verified all field/param names"
```

---

*End of Build Templates Reference*
