# Playwright Testing Guide by Stack

**Quick reference for Playwright setup across different technology stacks**

**Version:** 1.0
**Last Updated:** 2026-02-14

---

## Stack Decision Tree

```
┌─────────────────────────────────────────────────────┐
│         Which stack are you testing?                │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Django + ASGI (Daphne/Uvicorn/Hypercorn)          │
│  → Use async API (playwright.async_api)            │
│  → See: django-asgi-playwright.md                  │
│                                                     │
│  Django + WSGI (Gunicorn/uWSGI)                    │
│  → Use sync or async API (both work)               │
│  → Prefer async for consistency                    │
│                                                     │
│  Node.js (Express/Next.js/Nest.js)                 │
│  → Use JavaScript/TypeScript API (always async)    │
│  → See: Node.js section below                      │
│                                                     │
│  .NET (ASP.NET Core/Blazor)                        │
│  → Use C# API (always async)                       │
│  → See: .NET section below                         │
│                                                     │
│  Ruby (Rails/Sinatra)                              │
│  → Use Ruby API                                    │
│  → See: Ruby section below                         │
│                                                     │
│  Static Sites (HTML/CSS/JS)                        │
│  → Use any API (JavaScript recommended)            │
│  → See: Static Sites section below                 │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Django

### ASGI (Daphne, Uvicorn, Hypercorn) ⚡ CRITICAL

**Must use async API** - sync API causes `SynchronousOnlyOperation` errors

**Installation:**
```bash
pip install playwright pytest-asyncio pytest-playwright pytest-django
playwright install chromium
```

**Configuration (pytest.ini):**
```ini
[pytest]
DJANGO_SETTINGS_MODULE = your_project.settings
asyncio_mode = auto  # ✅ CRITICAL
```

**Test Example:**
```python
import pytest
from playwright.async_api import Page, expect

@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_login(page: Page, async_live_server: str):
    await page.goto(f"{async_live_server}/auth/login/")
    await page.fill('[name="username"]', 'user')
    await page.fill('[name="password"]', 'pass')
    await page.click('button[type="submit"]')
    await expect(page).to_have_url(f"{async_live_server}/dashboard/")
```

**Complete Guide:** `django-asgi-playwright.md`

### WSGI (Gunicorn, uWSGI)

**Can use either API** - no async context issues with WSGI

**Recommendation:** Use async API for consistency with ASGI projects

**Test Example (sync API):**
```python
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.django_db
def test_login(page: Page, live_server):
    page.goto(f"{live_server.url}/auth/login/")
    page.fill('[name="username"]', 'user')
    page.click('button[type="submit"]')
    expect(page).to_have_url(f"{live_server.url}/dashboard/")
```

---

## Node.js

**Always async** - JavaScript/TypeScript is async-first

### Express.js

**Installation:**
```bash
npm install -D @playwright/test
npx playwright install chromium
```

**Configuration (playwright.config.js):**
```javascript
import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  use: {
    baseURL: 'http://localhost:3000',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure'
  },
  webServer: {
    command: 'npm run start',
    port: 3000,
    timeout: 120 * 1000,
    reuseExistingServer: !process.env.CI
  }
})
```

**Test Example:**
```javascript
import { test, expect } from '@playwright/test'

test('user login', async ({ page }) => {
  await page.goto('/auth/login')
  await page.fill('[name="email"]', 'user@example.com')
  await page.fill('[name="password"]', 'password123')
  await page.click('button[type="submit"]')
  await expect(page).toHaveURL('/dashboard')
})
```

### Next.js

**Built-in test mode:**
```javascript
// playwright.config.js
export default defineConfig({
  webServer: {
    command: 'npm run dev',
    port: 3000,
    reuseExistingServer: true
  }
})
```

**Test with Next.js routing:**
```javascript
test('navigation', async ({ page }) => {
  await page.goto('/')
  await page.click('a[href="/about"]')
  await expect(page).toHaveURL('/about')

  // Test dynamic routes
  await page.goto('/posts/1')
  await expect(page.locator('h1')).toContainText('Post Title')
})
```

### Nest.js

**Use E2E test module:**
```javascript
// test/e2e/app.e2e-spec.ts
import { test, expect } from '@playwright/test'

test.beforeAll(async () => {
  // Start Nest.js app
  const app = await createTestApp()
  await app.listen(3001)
})

test('API endpoint', async ({ page }) => {
  await page.goto('http://localhost:3001')
  await expect(page.locator('.welcome')).toBeVisible()
})
```

---

## .NET (C#)

**Installation:**
```bash
dotnet add package Microsoft.Playwright.NUnit
playwright install chromium
```

**Test Example (NUnit):**
```csharp
using Microsoft.Playwright;
using Microsoft.Playwright.NUnit;
using NUnit.Framework;

[TestFixture]
public class LoginTests : PageTest
{
    [Test]
    public async Task UserCanLogin()
    {
        await Page.GotoAsync("http://localhost:5000/auth/login");
        await Page.FillAsync("[name='email']", "user@example.com");
        await Page.FillAsync("[name='password']", "password123");
        await Page.ClickAsync("button[type='submit']");
        await Expect(Page).ToHaveURLAsync("http://localhost:5000/dashboard");
    }
}
```

**Test Example (xUnit):**
```csharp
using Microsoft.Playwright;
using Xunit;

public class LoginTests : IAsyncLifetime
{
    private IPlaywright _playwright;
    private IBrowser _browser;
    private IPage _page;

    public async Task InitializeAsync()
    {
        _playwright = await Playwright.CreateAsync();
        _browser = await _playwright.Chromium.LaunchAsync();
        _page = await _browser.NewPageAsync();
    }

    [Fact]
    public async Task UserCanLogin()
    {
        await _page.GotoAsync("http://localhost:5000/auth/login");
        await _page.FillAsync("[name='email']", "user@example.com");
        await _page.ClickAsync("button[type='submit']");
        await Expect(_page).ToHaveURLAsync("http://localhost:5000/dashboard");
    }

    public async Task DisposeAsync()
    {
        await _browser.CloseAsync();
        _playwright.Dispose();
    }
}
```

---

## Ruby

**Installation:**
```bash
gem install playwright-ruby-client
playwright install chromium
```

**Test Example (RSpec):**
```ruby
require 'playwright'

RSpec.describe 'User Login' do
  before(:each) do
    @playwright = Playwright.create(playwright_cli_executable_path: 'npx playwright')
    @browser = @playwright.chromium.launch(headless: true)
    @page = @browser.new_page
  end

  after(:each) do
    @browser.close
    @playwright.stop
  end

  it 'allows user to login' do
    @page.goto('http://localhost:3000/auth/login')
    @page.fill('[name="email"]', 'user@example.com')
    @page.fill('[name="password"]', 'password123')
    @page.click('button[type="submit"]')
    expect(@page.url).to include('/dashboard')
  end
end
```

**Test Example (Minitest):**
```ruby
require 'minitest/autorun'
require 'playwright'

class LoginTest < Minitest::Test
  def setup
    @playwright = Playwright.create
    @browser = @playwright.chromium.launch
    @page = @browser.new_page
  end

  def teardown
    @browser.close
    @playwright.stop
  end

  def test_user_can_login
    @page.goto('http://localhost:3000/auth/login')
    @page.fill('[name="email"]', 'user@example.com')
    @page.click('button[type="submit"]')
    assert @page.url.include?('/dashboard')
  end
end
```

---

## Static Sites (HTML/CSS/JS)

**No server needed - test files directly:**

```javascript
import { test, expect } from '@playwright/test'

test('homepage loads', async ({ page }) => {
  // Test local file
  await page.goto('file:///path/to/index.html')
  await expect(page.locator('h1')).toContainText('Welcome')
})

test('homepage loads from server', async ({ page }) => {
  // Or use Python http.server, Live Server, etc.
  await page.goto('http://localhost:8000')
  await expect(page.locator('h1')).toBeVisible()
})
```

**Start simple server:**
```bash
# Python
python -m http.server 8000

# Node.js
npx http-server -p 8000

# Or use VS Code Live Server extension
```

---

## Common Patterns Across All Stacks

### 1. Wait for Elements

```javascript
// JavaScript/TypeScript
await page.waitForSelector('.element')
await page.waitForLoadState('networkidle')

// Python (async)
await page.wait_for_selector('.element')
await page.wait_for_load_state('networkidle')

// C#
await Page.WaitForSelectorAsync(".element");
await Page.WaitForLoadStateAsync(LoadState.NetworkIdle);

// Ruby
@page.wait_for_selector('.element')
@page.wait_for_load_state('networkidle')
```

### 2. Assertions

```javascript
// JavaScript
await expect(page).toHaveURL('/dashboard')
await expect(page.locator('h1')).toBeVisible()

// Python
await expect(page).to_have_url('/dashboard')
await expect(page.locator('h1')).to_be_visible()

// C#
await Expect(Page).ToHaveURLAsync("/dashboard");
await Expect(Page.Locator("h1")).ToBeVisibleAsync();

// Ruby
expect(@page.url).to include('/dashboard')
expect(@page.locator('h1')).to be_visible
```

### 3. Screenshots

```javascript
// JavaScript
await page.screenshot({ path: 'screenshot.png' })

// Python
await page.screenshot(path='screenshot.png')

// C#
await Page.ScreenshotAsync(new() { Path = "screenshot.png" });

// Ruby
@page.screenshot(path: 'screenshot.png')
```

### 4. Network Interception

```javascript
// JavaScript
await page.route('**/api/data', route => {
  route.fulfill({ json: { status: 'mocked' } })
})

// Python
await page.route('**/api/data', lambda route: route.fulfill(json={'status': 'mocked'}))

// C#
await Page.RouteAsync("**/api/data", route =>
{
    route.FulfillAsync(new() { Json = new { status = "mocked" } });
});

// Ruby
@page.route('**/api/data') do |route|
  route.fulfill(json: { status: 'mocked' })
end
```

---

## CI/CD Integration

### GitHub Actions

```yaml
name: E2E Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      # Node.js
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npm test

      # Python
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt
      - run: playwright install --with-deps
      - run: pytest tests/e2e

      # .NET
      - uses: actions/setup-dotnet@v3
      - run: dotnet test

      # Ruby
      - uses: ruby/setup-ruby@v1
      - run: bundle install
      - run: playwright install --with-deps
      - run: rspec spec/e2e

      # Upload artifacts on failure
      - uses: actions/upload-artifact@v3
        if: failure()
        with:
          name: test-results
          path: test-results/
```

---

## Performance Tips (All Stacks)

### 1. Reuse Browser Contexts

```javascript
// Create once, reuse for all tests
const browser = await playwright.chromium.launch()
const context = await browser.newContext()

// Each test gets fresh page
const page = await context.newPage()
```

### 2. Parallel Execution

```bash
# JavaScript
npx playwright test --workers=4

# Python
pytest tests/e2e -n 4  # Requires pytest-xdist

# .NET
dotnet test --parallel

# Ruby
parallel_rspec spec/e2e
```

### 3. Headless Mode

```javascript
// All stacks support headless mode
const browser = await playwright.chromium.launch({ headless: true })
```

---

## Debugging Tips (All Stacks)

### 1. Headed Mode (See Browser)

```javascript
// JavaScript
await playwright.chromium.launch({ headless: false })

// Python
await p.chromium.launch(headless=False)

// C#
await Playwright.Chromium.LaunchAsync(new() { Headless = false });

// Ruby
@playwright.chromium.launch(headless: false)
```

### 2. Slow Motion

```javascript
await playwright.chromium.launch({ slowMo: 500 })  // 500ms delay
```

### 3. Inspector

```bash
# JavaScript
PWDEBUG=1 npx playwright test

# Python
PWDEBUG=1 pytest tests/e2e

# .NET
PWDEBUG=1 dotnet test

# Ruby
PWDEBUG=1 rspec spec/e2e
```

---

## Summary: Key Differences by Stack

| Stack | API Style | Async Required | Test Framework | Notes |
|-------|-----------|----------------|----------------|-------|
| Django ASGI | Python async | ✅ YES | pytest-asyncio | Must use async_api |
| Django WSGI | Python sync/async | ❌ No | pytest-django | Either works |
| Node.js | JavaScript | ✅ YES | @playwright/test | Always async |
| .NET | C# | ✅ YES | NUnit/xUnit/MSTest | Always async |
| Ruby | Ruby | ❌ No | RSpec/Minitest | Sync by default |
| Static | Any | Depends | Any | Use what you prefer |

---

## Quick Reference by Stack

**Django ASGI:** Read `django-asgi-playwright.md`
**Node.js:** Use `@playwright/test` package
**.NET:** Use `Microsoft.Playwright.NUnit` or `Microsoft.Playwright.MSTest`
**Ruby:** Use `playwright-ruby-client` gem
**Static Sites:** Use JavaScript API with local server

---

*End of Playwright Stack Guide*
