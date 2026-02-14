# Visual Regression Testing with Playwright

**Version:** 1.0.0
**Last Updated:** 2026-02-14

---

## Overview

Visual regression testing ensures UI components maintain pixel-perfect consistency across changes. Playwright screenshot comparison detects unintended visual changes with configurable thresholds.

---

## Playwright Setup

### Installation

```bash
npm install -D @playwright/test
npx playwright install
```

### playwright.config.ts

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:4173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure'
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] }
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] }
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] }
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] }
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 13'] }
    }
  ],
  webServer: {
    command: 'npm run preview',
    url: 'http://localhost:4173',
    reuseExistingServer: !process.env.CI
  }
});
```

---

## Basic Screenshot Testing

### Component Screenshot

```typescript
import { test, expect } from '@playwright/test';

test('Button visual regression', async ({ page }) => {
  await page.goto('/components/button');

  // Take screenshot of entire page
  await expect(page).toHaveScreenshot('button-page.png');

  // Take screenshot of specific element
  await expect(page.locator('.button-preview')).toHaveScreenshot('button.png');
});
```

### With Options

```typescript
test('Button with custom threshold', async ({ page }) => {
  await page.goto('/components/button');

  await expect(page.locator('.button')).toHaveScreenshot('button.png', {
    threshold: 0.001,        // 0.1% difference allowed
    maxDiffPixels: 100,      // Max 100 different pixels
    maxDiffPixelRatio: 0.01, // Max 1% pixels different
    animations: 'disabled',   // Disable CSS animations
    caret: 'hide'            // Hide text cursor
  });
});
```

---

## Baseline Management

### Generate Baselines

```bash
# Generate baselines for all tests
npx playwright test --update-snapshots

# Generate baselines for specific test
npx playwright test button.spec.ts --update-snapshots

# Generate baselines for specific project
npx playwright test --project=chromium --update-snapshots
```

### Baseline Storage

```
tests/
├── components/
│   └── button.spec.ts
└── components/
    └── button.spec.ts-snapshots/
        ├── button-chromium-darwin.png
        ├── button-firefox-darwin.png
        ├── button-webkit-darwin.png
        ├── button-Mobile-Chrome-darwin.png
        └── button-Mobile-Safari-darwin.png
```

**Platform-specific baselines:** Playwright generates separate baselines for each OS (darwin, linux, win32)

---

## Diff Detection

### Threshold Configuration

```typescript
// Global threshold in config
export default defineConfig({
  expect: {
    toHaveScreenshot: {
      threshold: 0.001, // 0.1% global threshold
      maxDiffPixels: 100
    }
  }
});

// Per-test override
test('Strict comparison', async ({ page }) => {
  await expect(page).toHaveScreenshot('strict.png', {
    threshold: 0 // No difference allowed
  });
});

test('Lenient comparison', async ({ page }) => {
  await expect(page).toHaveScreenshot('lenient.png', {
    threshold: 0.05 // 5% difference allowed (for animations, etc.)
  });
});
```

### Diff Pixel Ratio vs Threshold

| Option | Description | Use When |
|--------|-------------|----------|
| **threshold** | Per-pixel color difference (0-1) | Small color changes acceptable |
| **maxDiffPixels** | Absolute pixel count | Known diff area size |
| **maxDiffPixelRatio** | Percentage of total pixels (0-1) | Proportional to image size |

```typescript
test('Different diff strategies', async ({ page }) => {
  // Strategy 1: Per-pixel threshold
  await expect(page).toHaveScreenshot('threshold.png', {
    threshold: 0.01 // Allow 1% color difference per pixel
  });

  // Strategy 2: Max different pixels
  await expect(page).toHaveScreenshot('max-pixels.png', {
    maxDiffPixels: 50 // Allow up to 50 pixels to differ
  });

  // Strategy 3: Max diff pixel ratio
  await expect(page).toHaveScreenshot('max-ratio.png', {
    maxDiffPixelRatio: 0.001 // Allow 0.1% of pixels to differ
  });
});
```

---

## Responsive Testing

### Multiple Viewports

```typescript
const viewports = [
  { name: 'mobile', width: 375, height: 667 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'desktop', width: 1920, height: 1080 },
  { name: 'ultrawide', width: 3440, height: 1440 }
];

for (const viewport of viewports) {
  test(`Button ${viewport.name} visual regression`, async ({ page }) => {
    await page.setViewportSize(viewport);
    await page.goto('/components/button');

    await expect(page.locator('.button')).toHaveScreenshot(`button-${viewport.name}.png`);
  });
}
```

### Device Emulation

```typescript
import { test, expect, devices } from '@playwright/test';

const mobileDevices = [
  devices['iPhone 13'],
  devices['iPhone 13 Pro'],
  devices['Pixel 5'],
  devices['Galaxy S9+']
];

for (const device of mobileDevices) {
  test(`Button on ${device.name}`, async ({ browser }) => {
    const context = await browser.newContext({
      ...device
    });
    const page = await context.newPage();

    await page.goto('/components/button');
    await expect(page.locator('.button')).toHaveScreenshot(`button-${device.name}.png`);

    await context.close();
  });
}
```

---

## Advanced Techniques

### Wait for Stability

```typescript
test('Wait for animations to complete', async ({ page }) => {
  await page.goto('/components/animated-button');

  // Wait for network idle
  await page.waitForLoadState('networkidle');

  // Wait for specific animation to complete
  await page.waitForFunction(() => {
    const button = document.querySelector('.button');
    return window.getComputedStyle(button).animationPlayState === 'idle';
  });

  await expect(page.locator('.button')).toHaveScreenshot('button-stable.png', {
    animations: 'disabled' // Disable remaining animations
  });
});
```

### Mask Dynamic Content

```typescript
test('Mask timestamps and dynamic content', async ({ page }) => {
  await page.goto('/dashboard');

  await expect(page).toHaveScreenshot('dashboard.png', {
    mask: [
      page.locator('.timestamp'),    // Hide timestamps
      page.locator('.live-counter'), // Hide counters
      page.locator('.user-avatar')   // Hide user images
    ]
  });
});
```

### Full Page Screenshots

```typescript
test('Full page screenshot', async ({ page }) => {
  await page.goto('/long-page');

  // Scroll to bottom to trigger lazy loading
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));

  // Wait for images to load
  await page.waitForLoadState('networkidle');

  await expect(page).toHaveScreenshot('full-page.png', {
    fullPage: true // Capture entire scrollable page
  });
});
```

---

## Component Testing

### Test Individual Components

```typescript
test.describe('Button Component', () => {
  test('Default variant', async ({ page }) => {
    await page.goto('/components/button');
    await expect(page.locator('.button.default')).toHaveScreenshot('button-default.png');
  });

  test('Primary variant', async ({ page }) => {
    await page.goto('/components/button');
    await expect(page.locator('.button.primary')).toHaveScreenshot('button-primary.png');
  });

  test('Secondary variant', async ({ page }) => {
    await page.goto('/components/button');
    await expect(page.locator('.button.secondary')).toHaveScreenshot('button-secondary.png');
  });

  test('Disabled state', async ({ page }) => {
    await page.goto('/components/button');
    await expect(page.locator('.button[disabled]')).toHaveScreenshot('button-disabled.png');
  });

  test('Loading state', async ({ page }) => {
    await page.goto('/components/button');
    await expect(page.locator('.button.loading')).toHaveScreenshot('button-loading.png', {
      animations: 'disabled' // Disable spinner animation
    });
  });
});
```

### Test Interactions

```typescript
test('Button hover state', async ({ page }) => {
  await page.goto('/components/button');

  const button = page.locator('.button');

  // Hover state
  await button.hover();
  await expect(button).toHaveScreenshot('button-hover.png');

  // Focus state
  await button.focus();
  await expect(button).toHaveScreenshot('button-focus.png');

  // Active state
  await button.click();
  await expect(button).toHaveScreenshot('button-active.png');
});
```

---

## Dark Mode Testing

```typescript
test.describe('Dark Mode', () => {
  test.use({ colorScheme: 'dark' });

  test('Button in dark mode', async ({ page }) => {
    await page.goto('/components/button');
    await expect(page.locator('.button')).toHaveScreenshot('button-dark.png');
  });
});

test.describe('Light Mode', () => {
  test.use({ colorScheme: 'light' });

  test('Button in light mode', async ({ page }) => {
    await page.goto('/components/button');
    await expect(page.locator('.button')).toHaveScreenshot('button-light.png');
  });
});
```

---

## CI/CD Integration

### GitHub Actions

```yaml
name: Visual Regression Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-node@v3
        with:
          node-version: 18

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      - name: Build
        run: npm run build

      - name: Run visual regression tests
        run: npm run test:visual

      - name: Upload test results
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30

      - name: Upload diffs
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: test-results/
          retention-days: 30
```

### Update Baselines in CI

```yaml
- name: Update baselines on main
  if: github.ref == 'refs/heads/main' && failure()
  run: |
    npm run test:visual -- --update-snapshots
    git config user.name "GitHub Actions"
    git config user.email "actions@github.com"
    git add tests/**/*-snapshots/
    git commit -m "Update visual regression baselines"
    git push
```

---

## Diff Analysis

### View Diffs Locally

```bash
# Run tests (failures generate diffs)
npx playwright test

# Open HTML report with diffs
npx playwright show-report
```

### Diff Output Structure

```
test-results/
└── components-button-spec-ts-button-visual-regression-chromium/
    ├── button-actual.png       # Current screenshot
    ├── button-expected.png     # Baseline screenshot
    └── button-diff.png         # Diff highlighting changes
```

### Programmatic Diff Access

```typescript
import { test, expect } from '@playwright/test';
import fs from 'fs';

test('Capture diff for analysis', async ({ page }) => {
  await page.goto('/components/button');

  try {
    await expect(page.locator('.button')).toHaveScreenshot('button.png');
  } catch (error) {
    // Read diff image
    const diffPath = 'test-results/.../button-diff.png';
    if (fs.existsSync(diffPath)) {
      const diff = fs.readFileSync(diffPath);
      // Analyze or upload diff
      await uploadDiff(diff);
    }
    throw error;
  }
});
```

---

## Best Practices

### 1. Stable Selectors

```typescript
// ❌ Bad: Brittle selector
await expect(page.locator('div > div > button')).toHaveScreenshot();

// ✅ Good: Semantic selector
await expect(page.locator('[data-testid="submit-button"]')).toHaveScreenshot();

// ✅ Good: Accessible selector
await expect(page.getByRole('button', { name: 'Submit' })).toHaveScreenshot();
```

### 2. Isolate Components

```typescript
// ❌ Bad: Full page screenshot (flaky due to dynamic content)
await expect(page).toHaveScreenshot('dashboard.png');

// ✅ Good: Component-level screenshot
await expect(page.locator('.dashboard-metrics')).toHaveScreenshot('metrics.png');
```

### 3. Disable Animations

```typescript
// Global CSS to disable animations
test.beforeEach(async ({ page }) => {
  await page.addStyleTag({
    content: `
      *, *::before, *::after {
        animation-duration: 0s !important;
        transition-duration: 0s !important;
      }
    `
  });
});
```

### 4. Consistent Test Data

```typescript
// ❌ Bad: Random data (causes flaky tests)
const data = generateRandomData();

// ✅ Good: Fixed test data
const data = {
  name: 'Test User',
  email: 'test@example.com',
  avatar: 'test-avatar.png'
};
```

### 5. Appropriate Thresholds

```typescript
// Static content: Strict threshold
await expect(page.locator('.logo')).toHaveScreenshot('logo.png', {
  threshold: 0
});

// Charts/graphs: Lenient threshold
await expect(page.locator('.chart')).toHaveScreenshot('chart.png', {
  threshold: 0.05 // 5% difference allowed
});

// Anti-aliasing differences: Moderate threshold
await expect(page.locator('.diagonal-line')).toHaveScreenshot('line.png', {
  threshold: 0.01 // 1% difference allowed
});
```

---

## Parallel Execution

```typescript
// Run tests in parallel
export default defineConfig({
  fullyParallel: true,
  workers: 4 // 4 parallel workers
});

// Or limit parallelism for screenshots
export default defineConfig({
  workers: process.env.CI ? 1 : 4 // Serial in CI for consistency
});
```

---

## Performance Optimization

### Reuse Browser Context

```typescript
import { test as base } from '@playwright/test';

const test = base.extend({
  context: async ({ browser }, use) => {
    // Reuse context across tests in same file
    const context = await browser.newContext();
    await use(context);
    await context.close();
  }
});

test('Test 1', async ({ page }) => {
  // Uses shared context
});

test('Test 2', async ({ page }) => {
  // Uses shared context
});
```

### Screenshot Caching

```typescript
const screenshotCache = new Map();

test('Cached baseline', async ({ page }) => {
  const cacheKey = 'button-default';

  if (!screenshotCache.has(cacheKey)) {
    await page.goto('/components/button');
    const screenshot = await page.locator('.button').screenshot();
    screenshotCache.set(cacheKey, screenshot);
  }

  // Use cached screenshot for comparison
  const baseline = screenshotCache.get(cacheKey);
  // Compare with current screenshot
});
```

---

*End of Visual Regression Reference*
