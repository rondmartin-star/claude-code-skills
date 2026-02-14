# Accessibility Checks & WCAG AA/AAA Compliance

**Version:** 1.0.0
**Last Updated:** 2026-02-14

---

## Overview

Comprehensive accessibility validation using Axe-core and Lighthouse to ensure WCAG 2.1 Level AA/AAA compliance. All UI components must pass accessibility checks before deployment.

---

## WCAG 2.1 Levels

| Level | Description | Required |
|-------|-------------|----------|
| **A** | Basic accessibility | Minimum baseline |
| **AA** | Addresses major barriers | ✅ **Target** (industry standard) |
| **AAA** | Highest level | Optional (for critical apps) |

**Target:** WCAG 2.1 Level AA compliance (0 violations)

---

## Axe-core Integration

### Setup & Installation

```typescript
import { AxeBuilder } from '@axe-core/playwright';
import { test, expect } from '@playwright/test';

test('Homepage accessibility', async ({ page }) => {
  await page.goto('/');

  const accessibilityScanResults = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
    .analyze();

  expect(accessibilityScanResults.violations).toEqual([]);
});
```

### Tag-Based Scanning

```typescript
// WCAG 2.1 Level AA only
await new AxeBuilder({ page })
  .withTags(['wcag2aa', 'wcag21aa'])
  .analyze();

// WCAG 2.1 Level AAA
await new AxeBuilder({ page })
  .withTags(['wcag2aaa', 'wcag21aaa'])
  .analyze();

// Best practices (non-WCAG)
await new AxeBuilder({ page })
  .withTags(['best-practice'])
  .analyze();
```

### Exclude Elements

```typescript
// Skip third-party widgets
await new AxeBuilder({ page })
  .exclude('.third-party-widget')
  .exclude('#chat-embed')
  .analyze();
```

---

## WCAG AA Compliance Checks

### 1. Perceivable (4 Principles)

#### 1.1 Text Alternatives

**Rule:** All non-text content has text alternative

```typescript
// Check images have alt text
test('Images have alt text', async ({ page }) => {
  const results = await new AxeBuilder({ page })
    .withRules(['image-alt'])
    .analyze();

  expect(results.violations).toEqual([]);
});
```

**Fix:**
```svelte
<!-- ❌ Bad: Missing alt -->
<img src="logo.png" />

<!-- ✅ Good: Descriptive alt -->
<img src="logo.png" alt="Company Logo" />

<!-- ✅ Good: Decorative image -->
<img src="decoration.png" alt="" />
```

---

#### 1.2 Time-Based Media

**Rule:** Captions for audio/video content

```svelte
<!-- ✅ Video with captions -->
<video controls>
  <source src="video.mp4" type="video/mp4" />
  <track kind="captions" src="captions.vtt" srclang="en" label="English" />
</video>
```

---

#### 1.3 Adaptable

**Rule:** Content structure is programmatically determined

```typescript
// Check heading order
test('Headings have logical order', async ({ page }) => {
  const results = await new AxeBuilder({ page })
    .withRules(['heading-order'])
    .analyze();

  expect(results.violations).toEqual([]);
});
```

**Fix:**
```svelte
<!-- ❌ Bad: Skipped heading level -->
<h1>Page Title</h1>
<h3>Subsection</h3>

<!-- ✅ Good: Logical heading structure -->
<h1>Page Title</h1>
<h2>Section</h2>
<h3>Subsection</h3>
```

---

#### 1.4 Distinguishable

**Rule:** Color contrast 4.5:1 for normal text, 3:1 for large text

```typescript
// Check color contrast
test('Color contrast meets WCAG AA', async ({ page }) => {
  const results = await new AxeBuilder({ page })
    .withRules(['color-contrast'])
    .analyze();

  expect(results.violations).toEqual([]);
});
```

**Fix:**
```css
/* ❌ Bad: Insufficient contrast (2.5:1) */
color: #999999;
background: #ffffff;

/* ✅ Good: Sufficient contrast (4.6:1) */
color: #767676;
background: #ffffff;

/* ✅ Good: High contrast (7.0:1) */
color: #595959;
background: #ffffff;
```

**Color Contrast Calculator:**
```typescript
function getContrastRatio(fg: string, bg: string): number {
  const fgLum = getRelativeLuminance(fg);
  const bgLum = getRelativeLuminance(bg);
  const lighter = Math.max(fgLum, bgLum);
  const darker = Math.min(fgLum, bgLum);
  return (lighter + 0.05) / (darker + 0.05);
}

function getRelativeLuminance(hex: string): number {
  const rgb = hexToRgb(hex);
  const [r, g, b] = rgb.map(val => {
    const srgb = val / 255;
    return srgb <= 0.03928
      ? srgb / 12.92
      : Math.pow((srgb + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}
```

---

### 2. Operable (4 Principles)

#### 2.1 Keyboard Accessible

**Rule:** All functionality available via keyboard

```typescript
// Check keyboard navigation
test('Interactive elements are keyboard accessible', async ({ page }) => {
  const results = await new AxeBuilder({ page })
    .withRules(['keyboard'])
    .analyze();

  expect(results.violations).toEqual([]);
});
```

**Fix:**
```svelte
<!-- ❌ Bad: div with click handler (not keyboard accessible) -->
<div on:click={handleClick}>Click me</div>

<!-- ✅ Good: button (keyboard accessible by default) -->
<button on:click={handleClick}>Click me</button>

<!-- ✅ Good: div with keyboard support -->
<div
  role="button"
  tabindex="0"
  on:click={handleClick}
  on:keydown={(e) => e.key === 'Enter' && handleClick()}
>
  Click me
</div>
```

---

#### 2.2 Enough Time

**Rule:** Users have enough time to read and use content

```svelte
<!-- ✅ Provide pause/stop for auto-updating content -->
<script>
  let isPaused = false;
  let slides = [...];
  let currentSlide = 0;

  function togglePause() {
    isPaused = !isPaused;
  }
</script>

<div class="carousel">
  <button on:click={togglePause}>
    {isPaused ? 'Play' : 'Pause'}
  </button>
  <img src={slides[currentSlide]} alt="Slide {currentSlide + 1}" />
</div>
```

---

#### 2.3 Seizures and Physical Reactions

**Rule:** No content flashes more than 3 times per second

```css
/* ❌ Bad: Rapid flashing animation */
@keyframes flash {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}
.element {
  animation: flash 0.1s infinite; /* 10 flashes/second */
}

/* ✅ Good: Slow, smooth animation */
@keyframes fade {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}
.element {
  animation: fade 2s ease-in-out; /* No rapid flashing */
}
```

---

#### 2.4 Navigable

**Rule:** Ways to help users navigate, find content

```typescript
// Check page has title
test('Page has descriptive title', async ({ page }) => {
  const results = await new AxeBuilder({ page })
    .withRules(['document-title'])
    .analyze();

  expect(results.violations).toEqual([]);
});
```

**Fix:**
```svelte
<!-- ✅ Descriptive page title -->
<svelte:head>
  <title>Login - MyApp</title>
</svelte:head>

<!-- ✅ Skip navigation link -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<main id="main-content">
  <!-- Page content -->
</main>
```

---

### 3. Understandable (3 Principles)

#### 3.1 Readable

**Rule:** Text content is readable and understandable

```svelte
<!-- ✅ Set language -->
<html lang="en">

<!-- ✅ Indicate language changes -->
<p>The French word for hello is <span lang="fr">bonjour</span>.</p>
```

---

#### 3.2 Predictable

**Rule:** Pages appear and operate in predictable ways

```svelte
<!-- ❌ Bad: Focus causes context change -->
<input on:focus={() => window.location = '/other-page'} />

<!-- ✅ Good: Focus does not change context -->
<input on:focus={() => showHelpText = true} />

<!-- ✅ Good: User initiates navigation -->
<button on:click={() => window.location = '/other-page'}>
  Go to other page
</button>
```

---

#### 3.3 Input Assistance

**Rule:** Help users avoid and correct mistakes

```svelte
<script>
  let email = '';
  let emailError = '';

  function validateEmail() {
    if (!email) {
      emailError = 'Email is required';
    } else if (!email.includes('@')) {
      emailError = 'Email must contain @';
    } else {
      emailError = '';
    }
  }
</script>

<!-- ✅ Form with validation -->
<form>
  <label for="email">Email</label>
  <input
    id="email"
    type="email"
    bind:value={email}
    on:blur={validateEmail}
    aria-invalid={emailError ? 'true' : 'false'}
    aria-describedby={emailError ? 'email-error' : undefined}
  />
  {#if emailError}
    <span id="email-error" role="alert">{emailError}</span>
  {/if}
</form>
```

---

### 4. Robust (1 Principle)

#### 4.1 Compatible

**Rule:** Content is compatible with assistive technologies

```typescript
// Check for valid ARIA attributes
test('ARIA attributes are valid', async ({ page }) => {
  const results = await new AxeBuilder({ page })
    .withRules(['aria-valid-attr', 'aria-valid-attr-value'])
    .analyze();

  expect(results.violations).toEqual([]);
});
```

**Fix:**
```svelte
<!-- ❌ Bad: Invalid ARIA -->
<div role="button" aria-pressed="yes">Toggle</div>

<!-- ✅ Good: Valid ARIA -->
<div role="button" aria-pressed="true" tabindex="0">Toggle</div>

<!-- ✅ Better: Use semantic HTML -->
<button aria-pressed="true">Toggle</button>
```

---

## Lighthouse Accessibility Audit

### Run Lighthouse

```typescript
import lighthouse from 'lighthouse';
import * as chromeLauncher from 'chrome-launcher';

async function runLighthouseAccessibility(url: string) {
  const chrome = await chromeLauncher.launch({ chromeFlags: ['--headless'] });

  const result = await lighthouse(url, {
    port: chrome.port,
    onlyCategories: ['accessibility']
  });

  await chrome.kill();

  return {
    score: result.lhr.categories.accessibility.score * 100,
    audits: result.lhr.audits
  };
}
```

### Interpret Scores

| Score | Grade | Status |
|-------|-------|--------|
| 90-100 | ✅ Pass | Deploy ready |
| 50-89 | ⚠️ Warning | Fix issues |
| 0-49 | ❌ Fail | Block deployment |

---

## Common Accessibility Violations & Fixes

### 1. Missing Alt Text

```svelte
<!-- ❌ Violation -->
<img src="chart.png" />

<!-- ✅ Fix -->
<img src="chart.png" alt="Sales chart showing 30% growth in Q4" />
```

---

### 2. Low Color Contrast

```css
/* ❌ Violation (3.1:1 ratio) */
.text { color: #959595; background: #ffffff; }

/* ✅ Fix (4.6:1 ratio) */
.text { color: #767676; background: #ffffff; }
```

---

### 3. Missing Form Labels

```svelte
<!-- ❌ Violation -->
<input type="text" placeholder="Enter name" />

<!-- ✅ Fix: Visible label -->
<label for="name">Name</label>
<input id="name" type="text" />

<!-- ✅ Fix: Aria-label for icon-only inputs -->
<input type="search" aria-label="Search" />
```

---

### 4. Non-Descriptive Link Text

```svelte
<!-- ❌ Violation -->
<a href="/article">Click here</a>

<!-- ✅ Fix -->
<a href="/article">Read the full article about accessibility</a>
```

---

### 5. Missing Heading Structure

```svelte
<!-- ❌ Violation: Skipped heading -->
<h1>Page Title</h1>
<h3>Section Title</h3>

<!-- ✅ Fix: Logical structure -->
<h1>Page Title</h1>
<h2>Section Title</h2>
```

---

### 6. Buttons Without Accessible Names

```svelte
<!-- ❌ Violation: Icon-only button -->
<button><Icon name="close" /></button>

<!-- ✅ Fix: aria-label -->
<button aria-label="Close dialog"><Icon name="close" /></button>

<!-- ✅ Fix: Visually hidden text -->
<button>
  <span class="sr-only">Close dialog</span>
  <Icon name="close" />
</button>
```

---

## Automated Testing Suite

### Complete Test Suite

```typescript
import { test, expect } from '@playwright/test';
import { AxeBuilder } from '@axe-core/playwright';

// Test all pages for accessibility
const pages = ['/', '/about', '/contact', '/products'];

for (const url of pages) {
  test(`${url} meets WCAG AA`, async ({ page }) => {
    await page.goto(url);

    const results = await new AxeBuilder({ page })
      .withTags(['wcag2aa', 'wcag21aa'])
      .analyze();

    expect(results.violations).toEqual([]);
  });
}

// Test specific components
test('Button component is accessible', async ({ page }) => {
  await page.goto('/components/button');

  const results = await new AxeBuilder({ page })
    .include('.button-preview')
    .analyze();

  expect(results.violations).toEqual([]);
});

// Keyboard navigation test
test('Modal can be closed with Escape key', async ({ page }) => {
  await page.goto('/components/modal');
  await page.click('button:text("Open Modal")');

  // Press Escape
  await page.keyboard.press('Escape');

  // Modal should be closed
  await expect(page.locator('.modal')).not.toBeVisible();
});
```

---

## CI/CD Integration

### GitHub Actions

```yaml
name: Accessibility Tests

on: [push, pull_request]

jobs:
  a11y:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm run build
      - run: npm run test:a11y
      - name: Upload Axe results
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: axe-results
          path: test-results/
```

---

*End of Accessibility Checks Reference*
