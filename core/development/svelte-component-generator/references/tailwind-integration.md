# Tailwind CSS Integration Reference

**Purpose:** Design token to Tailwind CSS mapping for component generation
**Version:** 1.0.0
**Date:** 2026-02-14

---

## Table of Contents

1. [Design Token Mapping](#design-token-mapping)
2. [Tailwind Configuration](#tailwind-configuration)
3. [Color System](#color-system)
4. [Typography](#typography)
5. [Spacing & Layout](#spacing--layout)
6. [Component Utilities](#component-utilities)
7. [Dark Mode](#dark-mode)

---

## Design Token Mapping

### Reading Tokens from corpus-config.json

```typescript
interface DesignSystemTokens {
  colors: {
    primary: string;
    secondary: string;
    danger: string;
    success: string;
    warning: string;
    info: string;
    gray: { [key: string]: string };
  };
  typography: {
    fontFamily: {
      sans: string;
      serif: string;
      mono: string;
    };
    fontSize: {
      xs: string;
      sm: string;
      base: string;
      lg: string;
      xl: string;
      '2xl': string;
      '3xl': string;
      '4xl': string;
    };
    fontWeight: {
      normal: number;
      medium: number;
      semibold: number;
      bold: number;
    };
  };
  spacing: {
    xs: string;
    sm: string;
    md: string;
    lg: string;
    xl: string;
    '2xl': string;
  };
  shadows: {
    sm: string;
    md: string;
    lg: string;
    xl: string;
  };
  borders: {
    radius: {
      none: string;
      sm: string;
      md: string;
      lg: string;
      full: string;
    };
    width: {
      thin: string;
      medium: string;
      thick: string;
    };
  };
}

// Load tokens from corpus-config.json
const config = await loadCorpusConfig();
const tokens = config.design_system?.tokens as DesignSystemTokens;
```

### Token to Tailwind Class Mapping

| Token Path | Tailwind Utility | Example |
|-----------|------------------|---------|
| `colors.primary` | `bg-primary-*`, `text-primary-*` | `bg-primary-600` |
| `typography.fontSize.base` | `text-base` | `text-base` |
| `spacing.md` | `p-*`, `m-*`, `gap-*` | `p-4` |
| `shadows.md` | `shadow-md` | `shadow-md` |
| `borders.radius.md` | `rounded-md` | `rounded-md` |

---

## Tailwind Configuration

### Auto-Generated tailwind.config.js

```javascript
// Auto-generated from corpus-config.json design tokens
import type { Config } from 'tailwindcss';

export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#EFF6FF',
          100: '#DBEAFE',
          200: '#BFDBFE',
          300: '#93C5FD',
          400: '#60A5FA',
          500: '#3B82F6',
          600: '#2563EB',  // Base primary color
          700: '#1D4ED8',
          800: '#1E40AF',
          900: '#1E3A8A',
          950: '#172554',
        },
        secondary: {
          // ... generated from tokens.colors.secondary
        },
        danger: {
          // ... generated from tokens.colors.danger
        },
        success: {
          // ... generated from tokens.colors.success
        },
        warning: {
          // ... generated from tokens.colors.warning
        },
        info: {
          // ... generated from tokens.colors.info
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        serif: ['Merriweather', 'Georgia', 'serif'],
        mono: ['Fira Code', 'monospace'],
      },
      fontSize: {
        xs: ['0.75rem', { lineHeight: '1rem' }],
        sm: ['0.875rem', { lineHeight: '1.25rem' }],
        base: ['1rem', { lineHeight: '1.5rem' }],
        lg: ['1.125rem', { lineHeight: '1.75rem' }],
        xl: ['1.25rem', { lineHeight: '1.75rem' }],
        '2xl': ['1.5rem', { lineHeight: '2rem' }],
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
        '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
      },
      spacing: {
        xs: '0.5rem',
        sm: '0.75rem',
        md: '1rem',
        lg: '1.5rem',
        xl: '2rem',
        '2xl': '3rem',
      },
      boxShadow: {
        sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
        md: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
        lg: '0 10px 15px -3px rgb(0 0 0 / 0.1)',
        xl: '0 20px 25px -5px rgb(0 0 0 / 0.1)',
      },
      borderRadius: {
        none: '0',
        sm: '0.125rem',
        md: '0.375rem',
        lg: '0.5rem',
        full: '9999px',
      },
    },
  },
  plugins: [],
} satisfies Config;
```

### Generating Config from Tokens

```typescript
function generateTailwindConfig(tokens: DesignSystemTokens): string {
  const config = {
    content: ['./src/**/*.{html,js,svelte,ts}'],
    theme: {
      extend: {
        colors: generateColorScale(tokens.colors),
        fontFamily: tokens.typography.fontFamily,
        fontSize: tokens.typography.fontSize,
        spacing: tokens.spacing,
        boxShadow: tokens.shadows,
        borderRadius: tokens.borders.radius,
      },
    },
    plugins: [],
  };

  return `import type { Config } from 'tailwindcss';\n\n` +
         `export default ${JSON.stringify(config, null, 2)} satisfies Config;`;
}

function generateColorScale(colors: any): Record<string, any> {
  const result: Record<string, any> = {};

  for (const [name, value] of Object.entries(colors)) {
    if (typeof value === 'string') {
      // Single color - generate full scale
      result[name] = generateShades(value);
    } else if (typeof value === 'object') {
      // Already a scale
      result[name] = value;
    }
  }

  return result;
}

function generateShades(baseColor: string): Record<number, string> {
  // Generate 50-950 shades from base color
  // Implementation uses color manipulation library (e.g., polished, chroma)
  return {
    50: lighten(baseColor, 0.95),
    100: lighten(baseColor, 0.90),
    200: lighten(baseColor, 0.80),
    300: lighten(baseColor, 0.60),
    400: lighten(baseColor, 0.30),
    500: baseColor,
    600: darken(baseColor, 0.10),
    700: darken(baseColor, 0.20),
    800: darken(baseColor, 0.30),
    900: darken(baseColor, 0.40),
    950: darken(baseColor, 0.50),
  };
}
```

---

## Color System

### Color Utilities

```svelte
<!-- Background Colors -->
<div class="bg-primary-600">Primary background</div>
<div class="bg-secondary-500">Secondary background</div>
<div class="bg-danger-600">Danger background</div>

<!-- Text Colors -->
<span class="text-primary-700">Primary text</span>
<span class="text-secondary-600">Secondary text</span>
<span class="text-danger-500">Danger text</span>

<!-- Border Colors -->
<div class="border border-primary-300">Primary border</div>
<div class="border-2 border-danger-400">Danger border</div>

<!-- Gradient Backgrounds -->
<div class="bg-gradient-to-r from-primary-500 to-secondary-500">
  Gradient background
</div>
```

### Color Composition Patterns

```svelte
<script lang="ts">
  let {
    variant = 'primary'
  } = $props<{
    variant?: 'primary' | 'secondary' | 'danger' | 'success';
  }>();

  const variantClasses = {
    primary: 'bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500',
    secondary: 'bg-secondary-600 text-white hover:bg-secondary-700 focus:ring-secondary-500',
    danger: 'bg-danger-600 text-white hover:bg-danger-700 focus:ring-danger-500',
    success: 'bg-success-600 text-white hover:bg-success-700 focus:ring-success-500',
  };

  let classes = $derived(variantClasses[variant]);
</script>

<button class={classes}>
  <slot />
</button>
```

### Semantic Color Mapping

| Semantic | Token | Tailwind Class | Usage |
|----------|-------|----------------|-------|
| Primary Action | `colors.primary` | `bg-primary-600` | Main buttons, links |
| Secondary Action | `colors.secondary` | `bg-secondary-600` | Secondary buttons |
| Destructive Action | `colors.danger` | `bg-danger-600` | Delete, remove actions |
| Success State | `colors.success` | `bg-success-600` | Success messages, checkmarks |
| Warning State | `colors.warning` | `bg-warning-600` | Warning messages |
| Info State | `colors.info` | `bg-info-600` | Info messages |

---

## Typography

### Font Family

```svelte
<!-- Sans-serif (default) -->
<p class="font-sans">This is sans-serif text</p>

<!-- Serif -->
<p class="font-serif">This is serif text</p>

<!-- Monospace -->
<code class="font-mono">This is monospace code</code>
```

### Font Size & Line Height

```svelte
<h1 class="text-4xl font-bold">Heading 1</h1>
<h2 class="text-3xl font-semibold">Heading 2</h2>
<h3 class="text-2xl font-semibold">Heading 3</h3>
<h4 class="text-xl font-medium">Heading 4</h4>
<h5 class="text-lg font-medium">Heading 5</h5>
<h6 class="text-base font-medium">Heading 6</h6>

<p class="text-base">Body text (16px)</p>
<p class="text-sm">Small text (14px)</p>
<p class="text-xs">Extra small text (12px)</p>
```

### Font Weight

```svelte
<p class="font-normal">Normal weight (400)</p>
<p class="font-medium">Medium weight (500)</p>
<p class="font-semibold">Semibold weight (600)</p>
<p class="font-bold">Bold weight (700)</p>
```

### Typography Component Pattern

```svelte
<script lang="ts">
  let {
    level = 'h1',
    size,
    weight,
    children
  } = $props<{
    level?: 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6';
    size?: 'xs' | 'sm' | 'base' | 'lg' | 'xl' | '2xl' | '3xl' | '4xl';
    weight?: 'normal' | 'medium' | 'semibold' | 'bold';
    children?: Snippet;
  }>();

  const defaultSizes = {
    h1: '4xl',
    h2: '3xl',
    h3: '2xl',
    h4: 'xl',
    h5: 'lg',
    h6: 'base',
  };

  const defaultWeights = {
    h1: 'bold',
    h2: 'semibold',
    h3: 'semibold',
    h4: 'medium',
    h5: 'medium',
    h6: 'medium',
  };

  let classes = $derived(`
    text-${size || defaultSizes[level]}
    font-${weight || defaultWeights[level]}
  `.trim().replace(/\s+/g, ' '));
</script>

<svelte:element this={level} class={classes}>
  {#if children}
    {@render children()}
  {:else}
    <slot />
  {/if}
</svelte:element>
```

---

## Spacing & Layout

### Padding & Margin

```svelte
<!-- Padding -->
<div class="p-md">Padding: 1rem (all sides)</div>
<div class="px-lg py-md">Padding: 1.5rem horizontal, 1rem vertical</div>
<div class="pt-xl pr-lg pb-md pl-sm">Individual padding</div>

<!-- Margin -->
<div class="m-md">Margin: 1rem (all sides)</div>
<div class="mx-auto">Margin: auto horizontal (center)</div>
<div class="mt-xl mb-lg">Margin: 2rem top, 1.5rem bottom</div>
```

### Gap (Flexbox & Grid)

```svelte
<!-- Flex Gap -->
<div class="flex gap-md">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>

<!-- Grid Gap -->
<div class="grid grid-cols-3 gap-lg">
  <div>Cell 1</div>
  <div>Cell 2</div>
  <div>Cell 3</div>
</div>
```

### Layout Components

```svelte
<!-- Container -->
<div class="container mx-auto px-4 max-w-7xl">
  <!-- Content -->
</div>

<!-- Stack (Vertical) -->
<div class="flex flex-col gap-md">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>

<!-- Stack (Horizontal) -->
<div class="flex flex-row gap-md items-center">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>

<!-- Grid -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-lg">
  <div>Card 1</div>
  <div>Card 2</div>
  <div>Card 3</div>
</div>
```

---

## Component Utilities

### Button Utilities

```svelte
<script lang="ts">
  const baseClasses = `
    inline-flex items-center justify-center
    font-medium rounded-md
    transition-colors duration-200
    focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2
    disabled:opacity-50 disabled:cursor-not-allowed
  `;

  const variantClasses = {
    primary: 'bg-primary-600 text-white hover:bg-primary-700 focus-visible:ring-primary-500',
    secondary: 'bg-secondary-600 text-white hover:bg-secondary-700 focus-visible:ring-secondary-500',
    outline: 'border-2 border-primary-600 text-primary-600 hover:bg-primary-50',
    ghost: 'text-primary-600 hover:bg-primary-50',
  };

  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };
</script>
```

### Input Utilities

```svelte
<script lang="ts">
  const baseClasses = `
    w-full rounded-md border border-gray-300
    px-3 py-2
    text-base text-gray-900 placeholder-gray-400
    focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500
    disabled:bg-gray-100 disabled:cursor-not-allowed
    transition-colors duration-200
  `;

  const errorClasses = `
    border-danger-500
    focus:ring-danger-500 focus:border-danger-500
  `;

  const successClasses = `
    border-success-500
    focus:ring-success-500 focus:border-success-500
  `;
</script>

<input
  type="text"
  class="{baseClasses} {hasError ? errorClasses : ''}"
  placeholder="Enter text"
/>
```

### Card Utilities

```svelte
<script lang="ts">
  const variantClasses = {
    elevated: 'bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow',
    outlined: 'bg-white rounded-lg border-2 border-gray-200',
    filled: 'bg-gray-100 rounded-lg',
  };
</script>

<div class="{variantClasses[variant]} p-6">
  <!-- Card content -->
</div>
```

---

## Dark Mode

### Dark Mode Configuration

```javascript
// tailwind.config.js
export default {
  darkMode: 'class', // or 'media'
  // ... rest of config
};
```

### Dark Mode Utilities

```svelte
<!-- Background colors with dark mode -->
<div class="bg-white dark:bg-gray-900">
  Content
</div>

<!-- Text colors with dark mode -->
<p class="text-gray-900 dark:text-gray-100">
  Text content
</p>

<!-- Border colors with dark mode -->
<div class="border border-gray-200 dark:border-gray-700">
  Bordered content
</div>
```

### Dark Mode Component Pattern

```svelte
<script lang="ts">
  let {
    variant = 'primary'
  } = $props<{
    variant?: 'primary' | 'secondary';
  }>();

  const variantClasses = {
    primary: `
      bg-primary-600 dark:bg-primary-500
      text-white
      hover:bg-primary-700 dark:hover:bg-primary-600
    `,
    secondary: `
      bg-white dark:bg-gray-800
      text-gray-900 dark:text-gray-100
      border border-gray-300 dark:border-gray-600
      hover:bg-gray-50 dark:hover:bg-gray-700
    `,
  };

  let classes = $derived(variantClasses[variant].trim().replace(/\s+/g, ' '));
</script>

<button class={classes}>
  <slot />
</button>
```

### Theme Toggle Component

```svelte
<script lang="ts">
  import { browser } from '$app/environment';
  import { onMount } from 'svelte';

  let theme = $state<'light' | 'dark'>('light');

  onMount(() => {
    // Read from localStorage or system preference
    const saved = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    theme = (saved as 'light' | 'dark') || (prefersDark ? 'dark' : 'light');
    applyTheme(theme);
  });

  function applyTheme(newTheme: 'light' | 'dark') {
    if (browser) {
      document.documentElement.classList.remove('light', 'dark');
      document.documentElement.classList.add(newTheme);
      localStorage.setItem('theme', newTheme);
    }
  }

  function toggleTheme() {
    theme = theme === 'light' ? 'dark' : 'light';
    applyTheme(theme);
  }
</script>

<button
  on:click={toggleTheme}
  class="p-2 rounded-md bg-gray-200 dark:bg-gray-700"
  aria-label="Toggle theme"
>
  {#if theme === 'light'}
    🌙 Dark Mode
  {:else}
    ☀️ Light Mode
  {/if}
</button>
```

---

## Responsive Design

### Breakpoint Utilities

```svelte
<!-- Responsive padding -->
<div class="p-4 md:p-6 lg:p-8">
  Responsive padding
</div>

<!-- Responsive grid -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
  <!-- Grid items -->
</div>

<!-- Responsive text size -->
<h1 class="text-2xl md:text-3xl lg:text-4xl">
  Responsive heading
</h1>

<!-- Responsive visibility -->
<div class="block md:hidden">Mobile only</div>
<div class="hidden md:block">Desktop only</div>
```

### Tailwind Breakpoints

| Breakpoint | Min Width | Usage |
|-----------|-----------|-------|
| `sm:` | 640px | Small tablets |
| `md:` | 768px | Tablets |
| `lg:` | 1024px | Laptops |
| `xl:` | 1280px | Desktops |
| `2xl:` | 1536px | Large desktops |

---

## Best Practices

1. **Use Design Tokens:** Always map from corpus-config.json tokens
2. **Compose Utilities:** Build complex styles from small utilities
3. **Avoid Arbitrary Values:** Prefer token-based values over arbitrary `[#3B82F6]`
4. **Dark Mode Support:** Include dark mode variants for all components
5. **Responsive by Default:** Consider mobile-first approach
6. **Consistent Spacing:** Use spacing tokens (xs, sm, md, lg, xl)
7. **Semantic Classes:** Use variant props, not direct Tailwind classes in templates

---

*Last Updated: 2026-02-14*
*Version: 1.0.0*
