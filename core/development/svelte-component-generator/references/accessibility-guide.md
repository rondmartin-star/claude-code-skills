# Accessibility Guide (WCAG AA)

**Purpose:** Complete guide to WCAG AA accessibility for Svelte components
**Version:** 1.0.0
**Date:** 2026-02-14

---

## Table of Contents

1. [WCAG AA Overview](#wcag-aa-overview)
2. [Semantic HTML](#semantic-html)
3. [ARIA Attributes](#aria-attributes)
4. [Keyboard Navigation](#keyboard-navigation)
5. [Focus Management](#focus-management)
6. [Color Contrast](#color-contrast)
7. [Screen Readers](#screen-readers)
8. [Validation Tools](#validation-tools)

---

## WCAG AA Overview

**WCAG 2.1 Level AA** is the industry standard for web accessibility. It ensures:
- Content is perceivable
- Interface is operable
- Information is understandable
- Implementation is robust

### Key Requirements

| Category | Requirement | Level |
|----------|------------|-------|
| **Text Contrast** | 4.5:1 for normal text, 3:1 for large text | AA |
| **Interactive Elements** | Keyboard accessible | AA |
| **Focus Indicators** | Visible focus on all interactive elements | AA |
| **Form Labels** | All inputs have associated labels | AA |
| **Error Identification** | Errors clearly identified and described | AA |
| **Resize Text** | Text can be resized to 200% without loss | AA |

---

## Semantic HTML

### Use Semantic Elements

**Always prefer semantic HTML over divs with roles:**

```svelte
<!-- ✅ GOOD: Semantic HTML -->
<button onclick={handleClick}>Click me</button>
<input type="text" placeholder="Enter email" />
<nav><ul><li><a href="/home">Home</a></li></ul></nav>
<main><article>Content</article></main>
<footer>Footer content</footer>

<!-- ❌ BAD: Non-semantic with ARIA -->
<div role="button" onclick={handleClick}>Click me</div>
<div role="textbox" contenteditable>Enter email</div>
<div role="navigation"><div role="list"><div role="listitem">...</div></div></div>
```

### HTML5 Landmark Elements

```svelte
<!-- Page Structure -->
<header>
  <h1>Site Title</h1>
  <nav>
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/about">About</a></li>
    </ul>
  </nav>
</header>

<main>
  <article>
    <h2>Article Title</h2>
    <section>
      <h3>Section Heading</h3>
      <p>Content...</p>
    </section>
  </article>

  <aside>
    <h3>Related Content</h3>
    <ul>
      <li>Link 1</li>
      <li>Link 2</li>
    </ul>
  </aside>
</main>

<footer>
  <p>&copy; 2026 Company Name</p>
</footer>
```

### Heading Hierarchy

```svelte
<!-- ✅ GOOD: Proper hierarchy -->
<h1>Page Title</h1>
  <h2>Section</h2>
    <h3>Subsection</h3>
    <h3>Another Subsection</h3>
  <h2>Another Section</h2>

<!-- ❌ BAD: Skipped levels -->
<h1>Page Title</h1>
  <h3>Skipped h2!</h3>
  <h2>Out of order</h2>
```

---

## ARIA Attributes

### When to Use ARIA

**First Rule of ARIA:** Don't use ARIA if semantic HTML works.

**Use ARIA when:**
1. Semantic HTML doesn't exist (e.g., tabs, accordions)
2. Enhancing semantic HTML (e.g., aria-expanded on button)
3. Providing screen reader context

### Common ARIA Attributes

#### aria-label

```svelte
<!-- When visual label is missing or inadequate -->
<button aria-label="Close dialog">×</button>
<button aria-label="Search">
  <svg><!-- Search icon --></svg>
</button>
```

#### aria-labelledby & aria-describedby

```svelte
<!-- Associate element with text elsewhere -->
<div role="dialog" aria-labelledby="dialog-title" aria-describedby="dialog-desc">
  <h2 id="dialog-title">Confirm Delete</h2>
  <p id="dialog-desc">Are you sure you want to delete this item?</p>
  <button>Cancel</button>
  <button>Delete</button>
</div>
```

#### aria-hidden

```svelte
<!-- Hide decorative elements from screen readers -->
<div class="decorative-icon" aria-hidden="true">
  <svg><!-- Decorative only --></svg>
</div>

<!-- But provide text alternative -->
<button>
  <svg aria-hidden="true"><!-- Icon --></svg>
  <span class="sr-only">Save</span>
</button>
```

#### aria-expanded, aria-controls

```svelte
<script lang="ts">
  let isOpen = $state(false);
</script>

<button
  aria-expanded={isOpen}
  aria-controls="dropdown-menu"
  on:click={() => isOpen = !isOpen}
>
  Menu
</button>

{#if isOpen}
  <ul id="dropdown-menu" role="menu">
    <li role="menuitem">Item 1</li>
    <li role="menuitem">Item 2</li>
  </ul>
{/if}
```

#### aria-live

```svelte
<!-- Announce dynamic content changes -->
<div aria-live="polite" aria-atomic="true">
  {#if loading}
    Loading...
  {:else if error}
    Error: {error.message}
  {:else}
    {data.length} items loaded
  {/if}
</div>

<!-- Urgent announcements -->
<div aria-live="assertive" role="alert">
  {errorMessage}
</div>
```

#### aria-disabled vs disabled

```svelte
<!-- ✅ Use disabled for form controls -->
<button disabled={isDisabled}>Submit</button>
<input type="text" disabled={isDisabled} />

<!-- Use aria-disabled when need to keep focusable -->
<div
  role="button"
  aria-disabled={isDisabled}
  tabindex={isDisabled ? -1 : 0}
>
  Custom Button
</div>
```

### ARIA Roles

#### Interactive Roles

```svelte
<!-- Tabs -->
<div role="tablist">
  <button role="tab" aria-selected="true" aria-controls="panel-1">Tab 1</button>
  <button role="tab" aria-selected="false" aria-controls="panel-2">Tab 2</button>
</div>
<div role="tabpanel" id="panel-1">Content 1</div>
<div role="tabpanel" id="panel-2" hidden>Content 2</div>

<!-- Accordion -->
<div>
  <button
    aria-expanded={isOpen}
    aria-controls="section-1"
  >
    Section Title
  </button>
  {#if isOpen}
    <div id="section-1" role="region">
      Section content
    </div>
  {/if}
</div>

<!-- Menu -->
<div role="menu">
  <button role="menuitem">Action 1</button>
  <button role="menuitem">Action 2</button>
</div>
```

---

## Keyboard Navigation

### Tab Order

```svelte
<!-- Focusable elements in DOM order -->
<button tabindex="0">First (default)</button>
<a href="/page" tabindex="0">Second (default)</a>
<input type="text" tabindex="0" /> <!-- Third (default) -->

<!-- Skip focusable elements -->
<div tabindex="-1">Not in tab order</div>

<!-- ❌ NEVER: Positive tabindex creates confusion -->
<button tabindex="1">Don't do this</button>
<button tabindex="2">Or this</button>
```

### Keyboard Event Handlers

```svelte
<script lang="ts">
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      handleClick();
    }

    if (event.key === 'Escape') {
      handleClose();
    }

    // Arrow key navigation
    if (event.key === 'ArrowDown') {
      focusNext();
    }
    if (event.key === 'ArrowUp') {
      focusPrevious();
    }
  }
</script>

<div
  role="button"
  tabindex="0"
  on:keydown={handleKeydown}
  on:click={handleClick}
>
  Custom Interactive Element
</div>
```

### Common Keyboard Patterns

| Component | Keys | Action |
|-----------|------|--------|
| **Button** | Enter, Space | Activate |
| **Link** | Enter | Navigate |
| **Checkbox** | Space | Toggle |
| **Radio** | Arrow keys | Move selection |
| **Dropdown** | Arrow Down/Up | Navigate items |
| **Dialog** | Escape | Close |
| **Tabs** | Arrow Left/Right | Switch tabs |
| **Menu** | Arrow Down/Up | Navigate items |

### Skip Links

```svelte
<!-- Allow keyboard users to skip navigation -->
<a href="#main-content" class="skip-link">
  Skip to main content
</a>

<header>
  <nav><!-- Navigation --></nav>
</header>

<main id="main-content" tabindex="-1">
  <!-- Main content -->
</main>

<style>
  .skip-link {
    position: absolute;
    left: -9999px;
    top: 0;
  }

  .skip-link:focus {
    left: 0;
    background: #000;
    color: #fff;
    padding: 0.5rem 1rem;
    z-index: 1000;
  }
</style>
```

---

## Focus Management

### Visible Focus Indicators

```svelte
<style>
  /* Default focus (fallback) */
  button:focus {
    outline: 2px solid #3B82F6;
    outline-offset: 2px;
  }

  /* Modern focus-visible (keyboard only) */
  button:focus-visible {
    outline: 2px solid #3B82F6;
    outline-offset: 2px;
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.3);
  }

  /* Remove focus for mouse users (if focus-visible supported) */
  button:focus:not(:focus-visible) {
    outline: none;
  }
</style>

<!-- Tailwind approach -->
<button class="
  focus:outline-none
  focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2
">
  Click me
</button>
```

### Focus Trapping (Modals)

```svelte
<script lang="ts">
  import { onMount } from 'svelte';

  let {
    isOpen = $bindable(false)
  } = $props();

  let dialogElement: HTMLElement;
  let previouslyFocused: HTMLElement | null = null;

  $effect(() => {
    if (isOpen) {
      previouslyFocused = document.activeElement as HTMLElement;

      // Focus first focusable element
      const focusable = dialogElement.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );

      if (focusable.length > 0) {
        (focusable[0] as HTMLElement).focus();
      }

      // Trap focus
      document.addEventListener('keydown', handleKeydown);

      return () => {
        document.removeEventListener('keydown', handleKeydown);
        previouslyFocused?.focus();
      };
    }
  });

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Tab') {
      trapFocus(event);
    } else if (event.key === 'Escape') {
      isOpen = false;
    }
  }

  function trapFocus(event: KeyboardEvent) {
    const focusable = Array.from(
      dialogElement.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      )
    ) as HTMLElement[];

    const firstFocusable = focusable[0];
    const lastFocusable = focusable[focusable.length - 1];

    if (event.shiftKey) {
      // Shift + Tab
      if (document.activeElement === firstFocusable) {
        lastFocusable.focus();
        event.preventDefault();
      }
    } else {
      // Tab
      if (document.activeElement === lastFocusable) {
        firstFocusable.focus();
        event.preventDefault();
      }
    }
  }
</script>

{#if isOpen}
  <div
    bind:this={dialogElement}
    role="dialog"
    aria-modal="true"
    aria-labelledby="dialog-title"
  >
    <!-- Dialog content -->
  </div>
{/if}
```

---

## Color Contrast

### WCAG AA Requirements

| Text Size | Minimum Contrast Ratio |
|-----------|----------------------|
| Normal text (<18pt) | 4.5:1 |
| Large text (≥18pt or ≥14pt bold) | 3:1 |
| UI components | 3:1 |

### Testing Contrast

```typescript
// Simple contrast ratio calculator
function getLuminance(r: number, g: number, b: number): number {
  const [rs, gs, bs] = [r, g, b].map(c => {
    c = c / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
}

function getContrastRatio(color1: string, color2: string): number {
  const lum1 = getLuminance(...hexToRgb(color1));
  const lum2 = getLuminance(...hexToRgb(color2));
  const brightest = Math.max(lum1, lum2);
  const darkest = Math.min(lum1, lum2);
  return (brightest + 0.05) / (darkest + 0.05);
}

// Example
const ratio = getContrastRatio('#FFFFFF', '#3B82F6');
console.log(`Contrast ratio: ${ratio.toFixed(2)}:1`);

if (ratio >= 4.5) {
  console.log('✅ Passes WCAG AA for normal text');
} else if (ratio >= 3.0) {
  console.log('⚠️ Passes AA for large text only');
} else {
  console.log('❌ Fails WCAG AA');
}
```

### Safe Color Combinations

```svelte
<!-- Text on Backgrounds -->
<div class="bg-white text-gray-900"><!-- 21:1 ✅ --></div>
<div class="bg-gray-900 text-white"><!-- 21:1 ✅ --></div>
<div class="bg-primary-600 text-white"><!-- Check specific primary color --></div>

<!-- Links -->
<a href="#" class="text-blue-600 underline"><!-- Underline ensures visibility --></a>

<!-- Buttons -->
<button class="bg-primary-600 text-white"><!-- Ensure 4.5:1 contrast --></button>

<!-- Focus Indicators -->
<button class="focus-visible:ring-2 focus-visible:ring-primary-500">
  <!-- Ring must contrast with both button and background -->
</button>
```

---

## Screen Readers

### Screen Reader Only Text

```svelte
<!-- Utility class for screen reader only text -->
<style>
  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
  }
</style>

<button>
  <svg aria-hidden="true"><!-- Icon --></svg>
  <span class="sr-only">Delete item</span>
</button>

<!-- Tailwind equivalent -->
<button>
  <svg aria-hidden="true"><!-- Icon --></svg>
  <span class="sr-only">Delete item</span>
</button>
```

### Meaningful Link Text

```svelte
<!-- ❌ BAD: Generic link text -->
<a href="/article">Click here</a>
<a href="/article">Read more</a>

<!-- ✅ GOOD: Descriptive link text -->
<a href="/article">Read the full article about accessibility</a>

<!-- ✅ GOOD: Context provided -->
<article>
  <h2>Article Title</h2>
  <p>Summary...</p>
  <a href="/article">Read more about Article Title</a>
</article>

<!-- ✅ GOOD: Screen reader only context -->
<a href="/article">
  Read more
  <span class="sr-only">about accessibility best practices</span>
</a>
```

### Form Labels

```svelte
<!-- ✅ Explicit label -->
<label for="email">Email Address</label>
<input type="email" id="email" name="email" />

<!-- ✅ Implicit label (less preferred) -->
<label>
  Email Address
  <input type="email" name="email" />
</label>

<!-- ✅ aria-label (when visual label not desired) -->
<input
  type="search"
  aria-label="Search products"
  placeholder="Search..."
/>

<!-- ✅ aria-labelledby (label is elsewhere) -->
<h2 id="contact-heading">Contact Information</h2>
<form aria-labelledby="contact-heading">
  <!-- Form fields -->
</form>
```

### Error Messages

```svelte
<script lang="ts">
  let email = $state('');
  let error = $state('');
  let errorId = 'email-error';

  function validate() {
    if (!email.includes('@')) {
      error = 'Please enter a valid email address';
    } else {
      error = '';
    }
  }
</script>

<label for="email">Email Address</label>
<input
  type="email"
  id="email"
  bind:value={email}
  on:blur={validate}
  aria-invalid={!!error}
  aria-describedby={error ? errorId : undefined}
  class="{error ? 'border-danger-500' : 'border-gray-300'}"
/>

{#if error}
  <p id={errorId} class="text-danger-600 text-sm mt-1" role="alert">
    {error}
  </p>
{/if}
```

---

## Validation Tools

### Automated Testing

#### Axe-core (Recommended)

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig({
  plugins: [svelte()],
  test: {
    environment: 'jsdom',
  },
});

// Button.test.ts
import { render } from '@testing-library/svelte';
import { axe, toHaveNoViolations } from 'jest-axe';
import Button from './Button.svelte';

expect.extend(toHaveNoViolations);

test('Button has no accessibility violations', async () => {
  const { container } = render(Button, {
    props: { children: 'Click me' }
  });

  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

#### Playwright (E2E)

```typescript
// e2e/accessibility.spec.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('Homepage should not have accessibility violations', async ({ page }) => {
  await page.goto('/');

  const accessibilityScanResults = await new AxeBuilder({ page }).analyze();

  expect(accessibilityScanResults.violations).toEqual([]);
});

test('Check specific component', async ({ page }) => {
  await page.goto('/components/button');

  const accessibilityScanResults = await new AxeBuilder({ page })
    .include('#button-demo')
    .analyze();

  expect(accessibilityScanResults.violations).toEqual([]);
});
```

### Manual Testing

#### Keyboard Testing Checklist

- [ ] All interactive elements reachable via Tab
- [ ] Tab order logical and intuitive
- [ ] Enter/Space activate buttons
- [ ] Escape closes modals/dropdowns
- [ ] Arrow keys navigate lists/menus
- [ ] Focus visible on all elements
- [ ] No keyboard traps

#### Screen Reader Testing

**Test with:**
- **Windows:** NVDA (free), JAWS (paid)
- **macOS:** VoiceOver (built-in)
- **Linux:** Orca (free)

**What to test:**
- [ ] All content is announced
- [ ] Headings structure makes sense
- [ ] Form labels are clear
- [ ] Buttons/links have meaningful text
- [ ] Error messages are announced
- [ ] Dynamic content changes announced
- [ ] Images have alt text

#### Browser DevTools

**Chrome DevTools:**
1. Open DevTools (F12)
2. Go to Lighthouse tab
3. Select "Accessibility" category
4. Run audit

**Firefox Accessibility Inspector:**
1. Open DevTools (F12)
2. Go to Accessibility tab
3. Check for issues

---

## Accessibility Checklist

### Per Component

- [ ] Uses semantic HTML where possible
- [ ] Includes ARIA attributes only when needed
- [ ] All interactive elements keyboard accessible
- [ ] Focus indicators visible and clear
- [ ] Text contrast meets WCAG AA (4.5:1)
- [ ] Screen reader text provided where needed
- [ ] Error states clearly communicated
- [ ] Tested with keyboard only
- [ ] Tested with screen reader
- [ ] Passes automated accessibility tests

### Application-Wide

- [ ] Heading hierarchy logical (h1 → h2 → h3)
- [ ] Skip links provided
- [ ] Page title descriptive
- [ ] Language attribute set on <html>
- [ ] Forms have clear labels and error messages
- [ ] Color not used as only means of conveying information
- [ ] Text can be resized to 200%
- [ ] No flashing content (seizure risk)
- [ ] Sufficient time provided for reading/using content

---

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [MDN Web Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
- [WebAIM](https://webaim.org/)
- [A11y Project](https://www.a11yproject.com/)
- [Axe DevTools](https://www.deque.com/axe/devtools/)

---

*Last Updated: 2026-02-14*
*Version: 1.0.0*
