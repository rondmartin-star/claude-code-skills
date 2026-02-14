# Design Token Schema Reference

**Version:** 1.0.0
**Last Updated:** 2026-02-14

---

## Overview

Complete schema reference for design tokens in corpus-config.json. All tokens follow the v4.0 configuration-driven architecture.

---

## Required Token Categories

### 1. Colors

**Schema:**
```json
{
  "design_system": {
    "colors": {
      "primary": {
        "50": "#eff6ff",
        "100": "#dbeafe",
        "200": "#bfdbfe",
        "300": "#93c5fd",
        "400": "#60a5fa",
        "500": "#3b82f6",
        "600": "#2563eb",
        "700": "#1d4ed8",
        "800": "#1e40af",
        "900": "#1e3a8a",
        "950": "#172554"
      },
      "semantic": {
        "success": "#10b981",
        "warning": "#f59e0b",
        "error": "#ef4444",
        "info": "#3b82f6"
      },
      "neutral": {
        "50": "#f9fafb",
        "100": "#f3f4f6",
        ...
        "900": "#111827",
        "950": "#030712"
      }
    }
  }
}
```

**Validation Rules:**
- ✅ Format: Hex (#RRGGBB), RGB (rgb(r, g, b)), HSL (hsl(h, s%, l%))
- ✅ Primary scale: 11 values (50, 100, 200, ..., 900, 950)
- ✅ Neutral scale: 11 values (50, 100, 200, ..., 900, 950)
- ✅ Semantic colors: success, warning, error, info
- ✅ Contrast ratios: 4.5:1 minimum for text (WCAG AA)

**Color Scale Generation:**
```typescript
// Auto-generate from single value
const primary = generateColorScale('#3b82f6', {
  steps: 11,
  lightness: [95, 10], // 50 to 950
  saturation: [95, 90]
});
```

---

### 2. Typography

**Schema:**
```json
{
  "design_system": {
    "typography": {
      "fontFamilies": {
        "sans": ["Inter", "system-ui", "sans-serif"],
        "serif": ["Georgia", "serif"],
        "mono": ["Fira Code", "monospace"]
      },
      "fontSizes": {
        "xs": { "size": "0.75rem", "lineHeight": "1rem" },
        "sm": { "size": "0.875rem", "lineHeight": "1.25rem" },
        "base": { "size": "1rem", "lineHeight": "1.5rem" },
        "lg": { "size": "1.125rem", "lineHeight": "1.75rem" },
        "xl": { "size": "1.25rem", "lineHeight": "1.75rem" },
        "2xl": { "size": "1.5rem", "lineHeight": "2rem" },
        "3xl": { "size": "1.875rem", "lineHeight": "2.25rem" },
        "4xl": { "size": "2.25rem", "lineHeight": "2.5rem" }
      },
      "fontWeights": {
        "thin": "100",
        "light": "300",
        "normal": "400",
        "medium": "500",
        "semibold": "600",
        "bold": "700",
        "black": "900"
      }
    }
  }
}
```

**Validation Rules:**
- ✅ Font families: Valid system or web fonts
- ✅ Font sizes: Modular scale (1.2-1.5 ratio recommended)
- ✅ Line heights: 1.2-1.8 for readability
- ✅ Font weights: Valid CSS values (100-900)
- ✅ Size + line-height pairing for consistency

**Font Size Scale Validation:**
```typescript
// Validate modular scale ratio
const sizes = Object.values(fontSizes).map(s => parseFloat(s.size));
const ratios = sizes.slice(1).map((s, i) => s / sizes[i]);
const avgRatio = ratios.reduce((a, b) => a + b) / ratios.length;

if (avgRatio < 1.2 || avgRatio > 1.5) {
  console.warn(`Font size ratio ${avgRatio.toFixed(2)} outside recommended 1.2-1.5 range`);
}
```

---

### 3. Spacing

**Schema:**
```json
{
  "design_system": {
    "spacing": {
      "base": "4px",
      "scale": {
        "0": "0px",
        "px": "1px",
        "0.5": "2px",
        "1": "4px",
        "2": "8px",
        "3": "12px",
        "4": "16px",
        "5": "20px",
        "6": "24px",
        "8": "32px",
        "10": "40px",
        "12": "48px",
        "16": "64px",
        "20": "80px",
        "24": "96px",
        "32": "128px"
      }
    }
  }
}
```

**Validation Rules:**
- ✅ Base unit: 4px or 8px recommended
- ✅ Scale values: Multiples of base unit
- ✅ Progression: Logical sequence (1, 2, 3, 4, 5, 6, 8, 10, ...)
- ✅ Units: px, rem, or em

**Spacing Consistency Check:**
```typescript
// Validate spacing is multiples of base
const base = parseInt(spacing.base);
const invalidValues = Object.entries(spacing.scale)
  .filter(([key, value]) => {
    const val = parseInt(value);
    return val !== 0 && val !== 1 && val % base !== 0;
  });

if (invalidValues.length > 0) {
  console.warn('Spacing values not multiples of base:', invalidValues);
}
```

---

## Optional Token Categories

### 4. Border Radius

**Schema:**
```json
{
  "design_system": {
    "borderRadius": {
      "none": "0px",
      "sm": "0.125rem",
      "DEFAULT": "0.25rem",
      "md": "0.375rem",
      "lg": "0.5rem",
      "xl": "0.75rem",
      "2xl": "1rem",
      "3xl": "1.5rem",
      "full": "9999px"
    }
  }
}
```

**Validation Rules:**
- ✅ Valid CSS units (px, rem, em)
- ✅ Ascending values (sm < DEFAULT < md < lg)
- ✅ Special value: full (9999px for circles)

---

### 5. Shadows

**Schema:**
```json
{
  "design_system": {
    "shadows": {
      "sm": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
      "DEFAULT": "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)",
      "md": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
      "lg": "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)",
      "xl": "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)",
      "2xl": "0 25px 50px -12px rgb(0 0 0 / 0.25)",
      "inner": "inset 0 2px 4px 0 rgb(0 0 0 / 0.05)",
      "none": "0 0 #0000"
    }
  }
}
```

**Validation Rules:**
- ✅ Valid CSS box-shadow syntax
- ✅ Logical elevation (sm < md < lg < xl)
- ✅ Alpha transparency for soft shadows

---

### 6. Breakpoints

**Schema:**
```json
{
  "design_system": {
    "breakpoints": {
      "xs": "320px",
      "sm": "640px",
      "md": "768px",
      "lg": "1024px",
      "xl": "1280px",
      "2xl": "1536px"
    }
  }
}
```

**Validation Rules:**
- ✅ Ascending pixel values (xs < sm < md < lg)
- ✅ Mobile-first (smallest first)
- ✅ Common device breakpoints

---

## Validation Functions

### Color Validation

```typescript
function validateColorFormat(color: string): boolean {
  const hexRegex = /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/;
  const rgbRegex = /^rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)$/;
  const hslRegex = /^hsl\(\s*\d+\s*,\s*\d+%\s*,\s*\d+%\s*\)$/;

  return hexRegex.test(color) || rgbRegex.test(color) || hslRegex.test(color);
}

function validateColorContrast(fg: string, bg: string): number {
  const fgLum = getRelativeLuminance(fg);
  const bgLum = getRelativeLuminance(bg);
  const contrast = (Math.max(fgLum, bgLum) + 0.05) / (Math.min(fgLum, bgLum) + 0.05);
  return contrast; // WCAG AA requires 4.5:1 for normal text
}
```

### Typography Validation

```typescript
function validateFontFamily(family: string[]): boolean {
  // Check if at least one fallback font
  const genericFonts = ['serif', 'sans-serif', 'monospace', 'cursive', 'fantasy', 'system-ui'];
  return family.some(f => genericFonts.includes(f.toLowerCase()));
}

function validateModularScale(sizes: Record<string, any>): boolean {
  const values = Object.values(sizes).map(s => parseFloat(s.size));
  const ratios = values.slice(1).map((v, i) => v / values[i]);
  const avgRatio = ratios.reduce((a, b) => a + b) / ratios.length;
  return avgRatio >= 1.2 && avgRatio <= 1.5;
}
```

### Spacing Validation

```typescript
function validateSpacingScale(base: string, scale: Record<string, string>): string[] {
  const baseValue = parseInt(base);
  const errors = [];

  for (const [key, value] of Object.entries(scale)) {
    const val = parseInt(value);
    if (val !== 0 && val !== 1 && val % baseValue !== 0) {
      errors.push(`${key}: ${value} is not a multiple of base ${base}`);
    }
  }

  return errors;
}
```

---

## Complete Example

```json
{
  "design_system": {
    "version": "1.0.0",
    "colors": { /* required */ },
    "typography": { /* required */ },
    "spacing": { /* required */ },
    "borderRadius": { /* optional */ },
    "shadows": { /* optional */ },
    "breakpoints": { /* optional */ }
  }
}
```

---

## Token Usage in Components

### Tailwind CSS Mapping

| Token Category | Tailwind Utilities |
|----------------|-------------------|
| colors.primary | bg-primary-500, text-primary-600, border-primary-400 |
| colors.semantic | bg-success, text-error, border-warning |
| typography.fontSizes | text-xs, text-sm, text-base, text-lg |
| typography.fontWeights | font-thin, font-normal, font-bold |
| spacing.scale | p-4, m-2, gap-6, space-x-8 |
| borderRadius | rounded-sm, rounded-md, rounded-lg |
| shadows | shadow-sm, shadow-md, shadow-lg |
| breakpoints | sm:, md:, lg:, xl: |

---

*End of Token Schema Reference*
