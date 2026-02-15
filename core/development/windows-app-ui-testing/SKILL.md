---
name: windows-app-ui-testing
description: >
  Playwright-powered UI testing, debugging, and visual iteration. Use for pixel-perfect
  UI work, end-to-end testing, visual regression, and browser automation. Load when:
  "debug UI", "test interface", "Playwright", "UI not matching design", "pixel perfect".
---

# Windows Application UI Testing Skill

**Purpose:** Visual-first UI testing and debugging with Playwright
**Version:** 1.0
**Size:** ~14 KB
**Related Skills:** windows-app-ui-design, windows-app-build

**Key Insight:** Claude Code is bad at pixel-perfect UI when looking at code. Use Playwright to look at the **rendered page** instead.

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Debug the UI" / "UI not matching design"
- "Pixel perfect" / "Fine-tune layout"
- "Test the interface" / "E2E tests"
- "Use Playwright" / "Open in browser"
- "Visual regression" / "Screenshot testing"
- "UI improvements" / "Iterate on design"

**Context Indicators:**
- User describes visual UI problems
- Need to verify UI behavior
- Building or debugging interface
- Implementing design specifications
- Creating automated tests

---

## ❌ DO NOT LOAD WHEN

- Writing backend logic (no UI component)
- Designing data models
- Working on API endpoints
- Pure code refactoring (no visual changes)

---

## Golden Rules

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   1. USE ASYNC API WITH DJANGO ASGI ⚡ CRITICAL            │
│      playwright.async_api (not sync_api) for Daphne        │
│                                                             │
│   2. LOOK AT THE PAGE, NOT THE CODE                        │
│      Use Playwright browser to see rendered UI             │
│                                                             │
│   3. ITERATE VISUALLY                                       │
│      Make change → View in browser → Adjust → Repeat       │
│                                                             │
│   4. SCREENSHOTS ARE TRUTH                                  │
│      Take screenshots to verify state                       │
│                                                             │
│   5. TEST END-TO-END FLOWS                                  │
│      Not just unit tests - real user journeys              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚠️ CRITICAL: Django ASGI + Playwright

**If using Django with ASGI (Daphne, Uvicorn, Hypercorn):**

❌ **DO NOT** use `playwright.sync_api` - causes `SynchronousOnlyOperation` errors
✅ **USE** `playwright.async_api` - works correctly with ASGI

**Quick Fix:**
```python
# ❌ WRONG (breaks with ASGI)
from playwright.sync_api import Page
def test_login(page: Page, live_server):
    page.goto(f"{live_server}/login/")

# ✅ CORRECT (works with ASGI)
from playwright.async_api import Page
@pytest.mark.asyncio
async def test_login(page: Page, async_live_server):
    await page.goto(f"{async_live_server}/login/")
```

**Complete Guide:** See `references/django-asgi-playwright.md`

---

## Quick Start

### 1. Load Playwright MCP

```bash
/plugin playwright
```

This enables:
- Stable Chrome browser connector
- UI testing and debugging
- Webpage interaction
- Headless mode (for CI/CD or VPS)
- Screenshot and video recording

### 2. Launch Browser for UI Iteration

**Standard workflow:**
```
Spin out an instance of Playwright browser, open http://localhost:3000
and I'll guide you from there in terms of UI improvements.
```

**Why this works:**
- Claude can see the rendered page
- Visual context beats code inspection
- Immediate feedback on changes
- Catches layout issues invisible in code

### 3. Visual Iteration Pattern

```
1. User describes UI issue
2. Open Playwright browser → localhost
3. Take screenshot of current state
4. Make CSS/HTML change
5. Refresh browser → view change
6. User provides feedback
7. Repeat until pixel-perfect
```

---

## Core Patterns

### Pattern 1: Pixel-Perfect UI Debugging

**Problem:** "The button is 2px too far left and the wrong shade of blue"

**Wrong Approach:**
```
Read CSS files → Guess which rule → Change → Hope it worked
```

**Correct Approach:**
```javascript
// 1. Open browser and inspect
await page.goto('http://localhost:3000')
await page.screenshot({ path: 'before.png' })

// 2. User describes exact issue
// "Submit button should be 12px from right edge, color #007BFF"

// 3. Make targeted CSS change in code editor
// button { margin-right: 12px; background-color: #007BFF; }

// 4. Refresh and verify
await page.reload()
await page.screenshot({ path: 'after.png' })

// 5. Compare visually
```

### Pattern 2: End-to-End User Flows

**Django ASGI Projects (Python):**
```python
import pytest
from playwright.async_api import Page, expect

@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_user_registration_flow(page: Page, async_live_server: str):
    """User registration flow"""
    await page.goto(f'{async_live_server}/register')

    # Fill form
    await page.fill('[name="email"]', 'test@example.com')
    await page.fill('[name="password"]', 'SecurePass123!')
    await page.click('button[type="submit"]')

    # Verify redirect and success
    await expect(page).to_have_url(f'{async_live_server}/dashboard/')
    await expect(page.locator('.welcome-message')).to_be_visible()
```

**JavaScript/Node Projects:**
```javascript
// User registration flow
test('user registration flow', async ({ page }) => {
  await page.goto('http://localhost:3000/register')

  // Fill form
  await page.fill('[name="email"]', 'test@example.com')
  await page.fill('[name="password"]', 'SecurePass123!')
  await page.click('button[type="submit"]')

  // Verify redirect and success
  await expect(page).toHaveURL(/.*dashboard/)
  await expect(page.locator('.welcome-message')).toBeVisible()
})
```

### Pattern 3: Visual Regression Testing

**Catch unintended UI changes:**
```javascript
import { test, expect } from '@playwright/test'

test('homepage matches baseline', async ({ page }) => {
  await page.goto('http://localhost:3000')

  // Take screenshot
  await expect(page).toHaveScreenshot('homepage.png', {
    maxDiffPixels: 100  // Allow small rendering differences
  })
})

// Playwright will:
// 1. First run: Save baseline screenshot
// 2. Future runs: Compare to baseline
// 3. Fail if visual diff exceeds threshold
```

### Pattern 4: Responsive Testing

**Verify across viewports:**
```javascript
const viewports = [
  { name: 'mobile', width: 375, height: 667 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'desktop', width: 1920, height: 1080 }
]

for (const viewport of viewports) {
  test(`layout on ${viewport.name}`, async ({ page }) => {
    await page.setViewportSize(viewport)
    await page.goto('http://localhost:3000')

    // Test critical elements are visible
    await expect(page.locator('.main-nav')).toBeVisible()
    await expect(page.locator('.content')).toBeVisible()

    await page.screenshot({
      path: `screenshots/${viewport.name}.png`,
      fullPage: true
    })
  })
}
```

### Pattern 5: Interaction Testing

**Verify dynamic behavior:**
```javascript
test('dropdown menu interaction', async ({ page }) => {
  await page.goto('http://localhost:3000')

  // Menu should be hidden initially
  await expect(page.locator('.dropdown-menu')).not.toBeVisible()

  // Click trigger
  await page.click('.dropdown-trigger')

  // Menu should appear
  await expect(page.locator('.dropdown-menu')).toBeVisible()

  // Click outside
  await page.click('body')

  // Menu should hide
  await expect(page.locator('.dropdown-menu')).not.toBeVisible()
})
```

---

## Memory-Efficient Patterns

**Problem:** Playwright can consume 4-8GB RAM during Docker container rebuilds.

### Solution 1: Headless Mode (Saves ~500MB)

```javascript
const browser = await playwright.chromium.launch({
  headless: true,  // No GUI
  args: [
    '--disable-dev-shm-usage',  // Use /tmp instead of /dev/shm
    '--no-sandbox',             // Required on some VPS
    '--disable-setuid-sandbox'
  ]
})
```

### Solution 2: Resource Limits

```javascript
const context = await browser.newContext({
  viewport: { width: 1280, height: 720 },
  ignoreHTTPSErrors: true,

  // Disable heavy features
  javaScriptEnabled: true,  // Keep JS
  hasTouch: false,          // Disable touch simulation
  isMobile: false,          // Disable mobile emulation

  // Reduce cache
  serviceWorkers: 'block',
  offline: false
})
```

### Solution 3: Cleanup After Tests

```javascript
test.afterEach(async ({ page, context }) => {
  // Close page
  await page.close()

  // Clear cookies/storage
  await context.clearCookies()
  await context.clearPermissions()
})

test.afterAll(async ({ browser }) => {
  // Close browser
  await browser.close()

  // Force garbage collection (if available)
  if (global.gc) global.gc()
})
```

### Solution 4: Prompt Memory Awareness

On constrained VPS (4GB RAM):
```
I only have 4GB RAM on this VPS, so use Playwright in headless mode
with minimal resource usage. Don't run multiple browsers simultaneously.
```

---

## Token-Optimized Test Generation

**Problem:** Generating 50 test cases can consume 20k+ tokens.

### Solution 1: Template-Based Generation

**Reusable test template:**
```javascript
function createFormTest(formName, fields, submitUrl, successUrl) {
  return test(`${formName} form submission`, async ({ page }) => {
    await page.goto(submitUrl)

    for (const [fieldName, value] of Object.entries(fields)) {
      await page.fill(`[name="${fieldName}"]`, value)
    }

    await page.click('button[type="submit"]')
    await expect(page).toHaveURL(successUrl)
  })
}

// Generate 10 tests with 1 template (saves ~15k tokens)
createFormTest('login', { email: 'user@example.com', password: 'pass' }, '/login', '/dashboard')
createFormTest('signup', { email: 'new@example.com', password: 'pass', name: 'User' }, '/signup', '/welcome')
// ... 8 more
```

### Solution 2: Parametrized Tests

```javascript
const testCases = [
  { role: 'admin', canDelete: true },
  { role: 'editor', canDelete: false },
  { role: 'viewer', canDelete: false }
]

testCases.forEach(({ role, canDelete }) => {
  test(`${role} delete permissions`, async ({ page }) => {
    await loginAs(page, role)
    const deleteBtn = page.locator('.delete-button')

    if (canDelete) {
      await expect(deleteBtn).toBeVisible()
    } else {
      await expect(deleteBtn).not.toBeVisible()
    }
  })
})
```

### Solution 3: Data-Driven Testing

```javascript
// tests/data/scenarios.json
[
  {
    "name": "Valid login",
    "input": { "email": "user@example.com", "password": "correct" },
    "expected": { "url": "/dashboard", "message": "Welcome" }
  },
  {
    "name": "Invalid password",
    "input": { "email": "user@example.com", "password": "wrong" },
    "expected": { "error": "Invalid credentials" }
  }
]

// tests/login.spec.js
const scenarios = require('./data/scenarios.json')

scenarios.forEach(scenario => {
  test(scenario.name, async ({ page }) => {
    await page.goto('/login')
    await page.fill('[name="email"]', scenario.input.email)
    await page.fill('[name="password"]', scenario.input.password)
    await page.click('button[type="submit"]')

    if (scenario.expected.url) {
      await expect(page).toHaveURL(scenario.expected.url)
    }
    if (scenario.expected.error) {
      await expect(page.locator('.error')).toContainText(scenario.expected.error)
    }
  })
})
```

---

## Common UI Debugging Workflows

### Workflow 1: "The Layout is Broken"

```javascript
// 1. Open browser and take screenshots
await page.goto('http://localhost:3000')
await page.screenshot({ path: 'desktop.png' })

await page.setViewportSize({ width: 375, height: 667 })
await page.screenshot({ path: 'mobile.png' })

// 2. Inspect computed styles
const element = await page.locator('.broken-layout')
const styles = await element.evaluate(el => {
  const computed = window.getComputedStyle(el)
  return {
    display: computed.display,
    flexDirection: computed.flexDirection,
    justifyContent: computed.justifyContent,
    alignItems: computed.alignItems,
    width: computed.width,
    height: computed.height
  }
})
console.log('Computed styles:', styles)

// 3. Make targeted fix in CSS
// 4. Refresh and verify
await page.reload()
await page.screenshot({ path: 'fixed.png' })
```

### Workflow 2: "Button Not Clickable"

```javascript
// 1. Verify element exists
const button = page.locator('button.submit')
await expect(button).toBeVisible()

// 2. Check if obscured
const boundingBox = await button.boundingBox()
console.log('Button position:', boundingBox)

// 3. Check for overlapping elements
const elementAtPoint = await page.evaluate(({ x, y }) => {
  const el = document.elementFromPoint(x, y)
  return {
    tag: el.tagName,
    class: el.className,
    id: el.id
  }
}, { x: boundingBox.x, y: boundingBox.y })
console.log('Element at button position:', elementAtPoint)

// 4. Try scrolling into view
await button.scrollIntoViewIfNeeded()
await button.click()
```

### Workflow 3: "Animation Not Working"

```javascript
// 1. Verify CSS animation exists
const element = page.locator('.animated-element')
const animationName = await element.evaluate(el =>
  window.getComputedStyle(el).animationName
)
console.log('Animation name:', animationName)  // Should not be 'none'

// 2. Record video to see actual behavior
const context = await browser.newContext({
  recordVideo: { dir: 'videos/' }
})
const page = await context.newPage()

await page.goto('http://localhost:3000')
await page.click('.trigger-animation')
await page.waitForTimeout(3000)  // Let animation complete

await context.close()  // Video saved to videos/
```

### Workflow 4: "Form Validation Not Showing"

```javascript
// 1. Fill form with invalid data
await page.fill('[name="email"]', 'invalid-email')
await page.click('button[type="submit"]')

// 2. Check for validation message
const errorMessage = page.locator('.error-message')
await expect(errorMessage).toBeVisible()
await expect(errorMessage).toContainText('Invalid email')

// 3. If not showing, debug:
const formHtml = await page.locator('form').innerHTML()
console.log('Form HTML:', formHtml)

const jsErrors = []
page.on('pageerror', error => jsErrors.push(error.message))
await page.reload()
console.log('JavaScript errors:', jsErrors)
```

---

## Integration with Build Workflow

### Pre-Commit Hook (Run UI Tests)

```javascript
// .husky/pre-commit
#!/bin/sh
npm run test:ui -- --grep "@critical"
```

### CI/CD Pipeline

```yaml
# .github/workflows/ui-tests.yml
name: UI Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npm run test:ui

      # Upload screenshots on failure
      - uses: actions/upload-artifact@v3
        if: failure()
        with:
          name: playwright-screenshots
          path: test-results/
```

### VPS Deployment (Headless Testing)

```bash
# Install Playwright on VPS
npm install -D @playwright/test
npx playwright install --with-deps chromium

# Run tests in headless mode
PLAYWRIGHT_HEADLESS=1 npm run test:ui
```

---

## Checklist: Before Declaring UI Complete

- [ ] Viewed in Playwright browser (not just code)
- [ ] Tested on mobile viewport (375px)
- [ ] Tested on tablet viewport (768px)
- [ ] Tested on desktop viewport (1920px)
- [ ] All interactive elements work (click, hover, focus)
- [ ] Forms validate correctly
- [ ] Error messages display
- [ ] Loading states show
- [ ] Animations run smoothly
- [ ] No console errors
- [ ] Accessibility basics (keyboard navigation, ARIA)
- [ ] Matches design mockup (screenshot comparison)

---

## References

**Complete guides:**
1. **playwright-stack-guide.md** - Quick reference for all stacks (Django, Node.js, .NET, Ruby)
2. **django-asgi-playwright.md** ⚡ Django ASGI + async Playwright (CRITICAL)
3. **playwright-patterns.md** - Common testing patterns and examples
4. **visual-regression.md** - Screenshot testing and diff workflows
5. **memory-optimization.md** - Resource-efficient browser automation
6. **ci-cd-integration.md** - Automated testing pipelines
7. **debugging-workflows.md** - Step-by-step troubleshooting guides

---

## Integration with Other Skills

**windows-app-ui-design:**
- Design creates mockups
- UI Testing verifies implementation matches design
- Provides visual feedback loop

**windows-app-build:**
- Build implements features
- UI Testing verifies features work end-to-end
- Catches regressions before deployment

**windows-app-orchestrator:**
- Routes UI-related requests to this skill
- Coordinates test execution in quality gates

---

*End of Windows Application UI Testing Skill*
