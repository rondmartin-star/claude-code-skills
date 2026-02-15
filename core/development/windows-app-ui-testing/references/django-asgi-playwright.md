# Django ASGI + Playwright Async Testing

**Problem Solved:** `SynchronousOnlyOperation` errors when using Playwright with Django's ASGI server (Daphne)

**Version:** 1.0
**Last Updated:** 2026-02-14

---

## The Problem

### Symptom

```
django.core.exceptions.SynchronousOnlyOperation: You cannot call this from an
async context - use a thread or sync_to_async.
```

### Root Cause

**Mismatch between Playwright API and Django ASGI:**
- Playwright's **sync_api** expects synchronous execution
- Django **ASGI (Daphne)** runs in async event loop
- pytest-django's `live_server` fixture triggers synchronous database operations from async context

**Why This Happens:**
1. ASGI server (Daphne) creates async event loop
2. Playwright sync_api tries to perform sync operations
3. pytest-django attempts database setup synchronously
4. Async context violation → crash

---

## The Solution

### Use Playwright's Async API

**Key Changes:**
1. Switch from `playwright.sync_api` → `playwright.async_api`
2. Convert all test functions to async (`async def test_*`)
3. Add `await` to all Playwright operations
4. Configure pytest-asyncio for automatic async test detection
5. Create async Django test fixtures

---

## Complete Implementation

### 1. Install Dependencies

```bash
# Add to requirements.txt
playwright>=1.40.0
pytest-asyncio>=0.23.0
pytest-playwright>=0.4.0
pytest-django>=4.7.0
```

```bash
pip install playwright pytest-asyncio pytest-playwright pytest-django
npx playwright install chromium  # Or: playwright install
```

### 2. Configure pytest.ini

```ini
# pytest.ini
[pytest]
DJANGO_SETTINGS_MODULE = your_project.settings.development
python_files = test_*.py
python_classes = Test*
python_functions = test_*
testpaths = tests

addopts =
    --verbose
    --strict-markers
    --tb=short
    --reuse-db
    --nomigrations

# ✅ CRITICAL: Enable asyncio mode
asyncio_mode = auto

markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    asyncio: marks tests as async (auto-detected with asyncio_mode=auto)
```

### 3. Create Async Fixtures (tests/e2e/conftest.py)

```python
"""
Async fixtures for Playwright + Django ASGI testing.
© 2026 Pterodactyl Holdings LLC. All Rights Reserved.
"""

import asyncio
import pytest
import pytest_asyncio
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture(scope="session")
def event_loop():
    """
    Create event loop for entire test session.

    Required for async fixtures with session scope.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def browser():
    """
    Launch browser for entire test session.

    Reusing browser across tests speeds up execution.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,  # Set to False for debugging
            args=[
                '--disable-dev-shm-usage',  # Use /tmp instead of /dev/shm
                '--no-sandbox',
                '--disable-setuid-sandbox'
            ]
        )
        yield browser
        await browser.close()


@pytest_asyncio.fixture
async def context(browser: Browser):
    """
    Create new browser context for each test.

    Isolates cookies, storage, and session between tests.
    """
    context = await browser.new_context(
        viewport={'width': 1280, 'height': 720},
        ignore_https_errors=True
    )
    yield context
    await context.close()


@pytest_asyncio.fixture
async def page(context: BrowserContext):
    """
    Create new page for each test.

    Fresh page ensures clean state.
    """
    page = await context.new_page()
    yield page
    await page.close()


@pytest_asyncio.fixture
async def async_live_server(live_server):
    """
    Async wrapper for Django's live_server fixture.

    Provides server URL for Playwright navigation.
    """
    return live_server.url


@pytest_asyncio.fixture
async def test_user(db):
    """
    Create test user in database.

    Use @pytest.mark.django_db on test function.
    """
    user = User.objects.create_user(
        username='e2e_test_user',
        email='e2e@example.com',
        password='TestPassword123!',
        first_name='E2E',
        last_name='Test User'
    )
    return user


@pytest_asyncio.fixture
async def authenticated_page(page: Page, async_live_server: str, test_user: dict):
    """
    Create authenticated page by logging in test user.

    Reuses session for faster test execution.
    """
    # Navigate to login page
    await page.goto(f"{async_live_server}/auth/login/")

    # Fill login form
    await page.fill('input[name="username"]', test_user.username)
    await page.fill('input[name="password"]', 'TestPassword123!')

    # Submit and wait for redirect
    await page.click('button[type="submit"]')
    await page.wait_for_url(f"{async_live_server}/", timeout=5000)

    yield page
```

### 4. Migrate Tests to Async API

#### Before (Sync API - BROKEN)

```python
"""
E2E tests using sync API - CAUSES ERRORS WITH ASGI
"""

import pytest
from playwright.sync_api import Page, expect  # ❌ sync_api


class TestAuthenticationFlow:
    def test_login_logout_flow(self, page: Page, live_server: str, test_user: dict):
        """Test: Login → Dashboard → Logout"""
        # ❌ This will crash with ASGI
        page.goto(f"{live_server}/auth/login/")
        page.fill('input[name="username"]', test_user["username"])
        page.click('button[type="submit"]')
        page.wait_for_url(f"{live_server}/", timeout=5000)
```

#### After (Async API - WORKS)

```python
"""
E2E tests using async API - WORKS WITH ASGI
"""

import pytest
from playwright.async_api import Page, expect  # ✅ async_api


class TestAuthenticationFlow:
    @pytest.mark.asyncio  # ✅ Mark as async (or use asyncio_mode=auto)
    @pytest.mark.django_db(transaction=True)  # ✅ Database access
    async def test_login_logout_flow(
        self,
        page: Page,
        async_live_server: str,
        test_user
    ):
        """Test: Login → Dashboard → Logout"""
        # ✅ All Playwright operations use await
        await page.goto(f"{async_live_server}/auth/login/")

        # Verify login page loaded
        await expect(page).to_have_title("Login")

        # Fill login form
        await page.fill('input[name="username"]', test_user.username)
        await page.fill('input[name="password"]', 'TestPassword123!')

        # Submit
        await page.click('button[type="submit"]')

        # Wait for redirect to dashboard
        await page.wait_for_url(f"{async_live_server}/", timeout=5000)

        # Verify dashboard loaded
        await expect(page.locator('.welcome-message')).to_be_visible()

        # Logout
        await page.click('a:has-text("Logout")')

        # Verify redirected to login
        await page.wait_for_url(f"{async_live_server}/auth/login/", timeout=5000)
```

### 5. Complete Test Examples

#### Example 1: Form Submission

```python
@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_create_event_form(authenticated_page: Page, async_live_server: str):
    """Test: Create Event → Verify Event Created"""
    page = authenticated_page

    # Navigate to events page
    await page.goto(f"{async_live_server}/service-director/events/")

    # Click "New Event" button
    await page.click('a:has-text("New Event")')

    # Wait for form to load
    await page.wait_for_selector('input[name="title"]')

    # Fill event form
    await page.fill('input[name="title"]', "E2E Test Service")
    await page.fill('input[name="date"]', "2026-12-25")
    await page.select_option('select[name="event_type_id"]', index=1)
    await page.fill('textarea[name="description"]', "Test event description")

    # Submit form
    await page.click('button[type="submit"]')

    # Verify redirect to event detail page
    await page.wait_for_url(f"{async_live_server}/service-director/events/*/", timeout=5000)

    # Verify event appears on page
    await expect(page.locator('h1:has-text("E2E Test Service")')).to_be_visible()
```

#### Example 2: Navigation Testing

```python
@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_module_navigation(authenticated_page: Page, async_live_server: str):
    """Test: Navigate through all modules"""
    page = authenticated_page

    modules = [
        {'name': 'PMS', 'url': '/pms/'},
        {'name': 'Service Director', 'url': '/service-director/'},
        {'name': 'HVAC Director', 'url': '/hvac/'},
        {'name': 'Finance Director', 'url': '/finance/'},
        {'name': 'Time Logging', 'url': '/time-logging/'}
    ]

    for module in modules:
        # Click module link in sidebar
        await page.click(f'a:has-text("{module["name"]}")')

        # Verify navigation
        await page.wait_for_url(f"{async_live_server}{module['url']}*", timeout=5000)

        # Verify page loaded (no 404/500)
        await expect(page.locator('h1')).to_be_visible()
```

#### Example 3: Screenshot Testing

```python
@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_dashboard_visual_regression(authenticated_page: Page, async_live_server: str):
    """Test: Dashboard matches baseline screenshot"""
    page = authenticated_page

    await page.goto(f"{async_live_server}/")

    # Wait for dynamic content to load
    await page.wait_for_load_state('networkidle')

    # Take screenshot and compare to baseline
    await expect(page).to_have_screenshot(
        'dashboard.png',
        max_diff_pixels=100,  # Allow small rendering differences
        full_page=True
    )
```

#### Example 4: Error Handling

```python
@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_404_error_page(page: Page, async_live_server: str):
    """Test: 404 page displays correctly"""
    # Navigate to non-existent page
    await page.goto(f"{async_live_server}/nonexistent-page/")

    # Verify 404 page elements
    await expect(page.locator('h1:has-text("404")')).to_be_visible()
    await expect(page.locator('a:has-text("Return to Dashboard")')).to_be_visible()

    # Click return link
    await page.click('a:has-text("Return to Dashboard")')

    # Verify redirected to dashboard
    await page.wait_for_url(f"{async_live_server}/", timeout=5000)
```

---

## Debugging Tips

### 1. Enable Headed Mode

```python
# tests/e2e/conftest.py
@pytest_asyncio.fixture(scope="session")
async def browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,  # ✅ See browser window
            slow_mo=500      # ✅ Slow down actions (ms)
        )
        yield browser
        await browser.close()
```

### 2. Take Screenshots on Failure

```python
@pytest_asyncio.fixture
async def page(context: BrowserContext, request):
    page = await context.new_page()
    yield page

    # Take screenshot on test failure
    if request.node.rep_call.failed:
        await page.screenshot(path=f'screenshots/failure-{request.node.name}.png')

    await page.close()
```

### 3. Console Logging

```python
@pytest.mark.asyncio
async def test_with_console_logging(page: Page):
    # Capture console messages
    messages = []
    page.on('console', lambda msg: messages.append(f"{msg.type}: {msg.text}"))

    await page.goto('http://localhost:8000')

    # Print console messages
    for msg in messages:
        print(msg)
```

### 4. Network Monitoring

```python
@pytest.mark.asyncio
async def test_with_network_monitoring(page: Page):
    # Monitor network requests
    async def log_request(request):
        print(f"→ {request.method} {request.url}")

    async def log_response(response):
        print(f"← {response.status} {response.url}")

    page.on('request', log_request)
    page.on('response', log_response)

    await page.goto('http://localhost:8000')
```

---

## Performance Optimization

### 1. Reuse Browser Instance

```python
# ✅ GOOD: Session-scoped browser
@pytest_asyncio.fixture(scope="session")
async def browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        yield browser
        await browser.close()

# ❌ BAD: Function-scoped browser (slow)
@pytest_asyncio.fixture
async def browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        yield browser
        await browser.close()
```

**Speedup:** 10x faster (5s → 0.5s per test)

### 2. Parallel Test Execution

```bash
# Run tests in parallel (4 workers)
pytest tests/e2e -n 4
```

**Requires:** `pip install pytest-xdist`

### 3. Selective Test Running

```bash
# Run only critical E2E tests
pytest tests/e2e -m "critical"

# Skip slow tests
pytest tests/e2e -m "not slow"
```

---

## Integration with Convergence Engine

### E2E Audit for Multi-Methodology Convergence

```python
# common/convergence/audits/e2e_audit.py
"""
E2E Audit for Multi-Methodology Convergence
"""

import asyncio
import pytest
from pathlib import Path


class E2EAudit:
    """Run E2E tests as part of convergence quality assurance."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.test_dir = project_root / 'tests' / 'e2e'

    async def run_audit(self) -> dict:
        """
        Run all E2E tests and return results.

        Returns:
            {
                'passed': bool,
                'total_tests': int,
                'passed_tests': int,
                'failed_tests': int,
                'issues': List[dict]
            }
        """
        # Run pytest programmatically
        exit_code = pytest.main([
            str(self.test_dir),
            '--tb=short',
            '--quiet',
            '-v'
        ])

        passed = exit_code == 0

        # Parse results (simplified)
        return {
            'methodology': 'E2E-User-Flows',
            'passed': passed,
            'issues_found': [] if passed else ['E2E tests failed'],
            'severity': 'high' if not passed else None
        }
```

---

## Migration Checklist

### From Sync to Async Playwright

- [ ] Install `playwright` and `pytest-asyncio`
- [ ] Add `asyncio_mode = auto` to `pytest.ini`
- [ ] Create `tests/e2e/conftest.py` with async fixtures
- [ ] Change imports: `playwright.sync_api` → `playwright.async_api`
- [ ] Convert test functions: `def test_*` → `async def test_*`
- [ ] Add `@pytest.mark.asyncio` decorator (or rely on auto-detection)
- [ ] Add `@pytest.mark.django_db(transaction=True)` for database access
- [ ] Add `await` to all Playwright operations
- [ ] Update fixture usage: `live_server` → `async_live_server`
- [ ] Run tests: `pytest tests/e2e -v`
- [ ] Verify 0 skipped tests (all passing)

---

## Common Errors & Solutions

### Error 1: "RuntimeError: There is no current event loop"

**Cause:** Missing event loop fixture

**Solution:**
```python
# tests/e2e/conftest.py
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
```

### Error 2: "SynchronousOnlyOperation" Still Occurring

**Cause:** Forgot `await` on Playwright operation

**Solution:** Add `await` to all Playwright calls:
```python
# ❌ WRONG
page.goto('http://localhost:8000')

# ✅ CORRECT
await page.goto('http://localhost:8000')
```

### Error 3: "fixture 'page' not found"

**Cause:** Async fixtures not registered

**Solution:** Use `pytest_asyncio.fixture` instead of `pytest.fixture`:
```python
import pytest_asyncio

@pytest_asyncio.fixture
async def page(context):
    page = await context.new_page()
    yield page
    await page.close()
```

### Error 4: Tests Hang Forever

**Cause:** Missing `await` or timeout too long

**Solution:**
1. Check all Playwright calls have `await`
2. Add reasonable timeouts:
```python
await page.goto(url, timeout=10000)  # 10 second timeout
await page.wait_for_selector('.element', timeout=5000)
```

---

## References

**Official Documentation:**
- [Playwright Python Async API](https://playwright.dev/python/docs/api/class-playwright)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [Django ASGI](https://docs.djangoproject.com/en/5.1/topics/async/)

**Related Skills:**
- `windows-app-ui-testing` - Main UI testing skill
- `windows-app-testing-strategy` - Test strategy and convergence
- `convergence-engine` - Multi-methodology quality assurance

---

## Summary

**Problem:** Playwright sync API + Django ASGI = `SynchronousOnlyOperation` errors

**Solution:**
1. Use Playwright's `async_api` instead of `sync_api`
2. Convert all tests to async functions
3. Add `await` to all Playwright operations
4. Configure pytest-asyncio with `asyncio_mode = auto`
5. Create async fixtures for Django testing

**Result:** All E2E tests pass with Django ASGI (Daphne), enabling automated browser testing in production environment.

---

*End of Django ASGI + Playwright Async Testing Reference*
