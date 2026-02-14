# Design Consistency Rules & Validation

**Version:** 1.0.0
**Last Updated:** 2026-02-14

---

## Overview

Comprehensive consistency rules for design tokens and component implementation. All rules enforce WCAG AA accessibility standards and modern design best practices.

---

## Severity Levels

| Severity | Symbol | Meaning | Action |
|----------|--------|---------|--------|
| **Error** | ❌ | Blocks deployment | Must fix before release |
| **Warning** | ⚠️ | Reduces quality | Should fix soon |
| **Info** | 🟡 | Best practice | Optional improvement |

---

## Color Consistency Rules

### Rule 1: Color Contrast (WCAG AA)

**Severity:** ❌ Error
**Rule:** All text must have 4.5:1 contrast ratio (3:1 for large text 18pt+)

```typescript
function validateColorContrast(
  foreground: string,
  background: string,
  fontSize: number
): ValidationResult {
  const contrast = calculateContrast(foreground, background);
  const minContrast = fontSize >= 18 ? 3.0 : 4.5;

  if (contrast < minContrast) {
    return {
      valid: false,
      severity: 'error',
      message: `Contrast ${contrast.toFixed(2)}:1 fails WCAG AA (requires ${minContrast}:1)`,
      fix: `Increase contrast by darkening foreground or lightening background`
    };
  }

  return { valid: true };
}
```

**Common Violations:**
- Light gray text on white background
- Primary color text on light backgrounds
- Semantic colors without sufficient contrast

**Fix Strategies:**
- Use darker shades for text (600-900 range)
- Use lighter backgrounds (50-200 range)
- Test with Lighthouse or Axe DevTools

---

### Rule 2: Color Scale Consistency

**Severity:** ⚠️ Warning
**Rule:** Color scales should have 11 values (50, 100, 200, ..., 900, 950)

```typescript
function validateColorScale(scale: Record<string, string>): ValidationResult {
  const expectedShades = ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900', '950'];
  const actualShades = Object.keys(scale);
  const missingShades = expectedShades.filter(s => !actualShades.includes(s));

  if (missingShades.length > 0) {
    return {
      valid: false,
      severity: 'warning',
      message: `Missing shades: ${missingShades.join(', ')}`,
      fix: `Add missing shades to color scale`
    };
  }

  return { valid: true };
}
```

**Benefits of Complete Scales:**
- More flexibility in component styling
- Consistent visual hierarchy
- Better dark mode support

---

### Rule 3: Semantic Color Consistency

**Severity:** ❌ Error
**Rule:** Must include success, warning, error, info semantic colors

```typescript
function validateSemanticColors(semantic: Record<string, string>): ValidationResult {
  const required = ['success', 'warning', 'error', 'info'];
  const missing = required.filter(key => !semantic[key]);

  if (missing.length > 0) {
    return {
      valid: false,
      severity: 'error',
      message: `Missing semantic colors: ${missing.join(', ')}`,
      fix: `Add required semantic colors (success: green, warning: orange, error: red, info: blue)`
    };
  }

  return { valid: true };
}
```

**Recommended Colors:**
- Success: Green (#10b981 or similar)
- Warning: Orange/Amber (#f59e0b or similar)
- Error: Red (#ef4444 or similar)
- Info: Blue (#3b82f6 or similar)

---

### Rule 4: No Hardcoded Colors

**Severity:** ⚠️ Warning
**Rule:** Components should use design tokens, not hardcoded hex/rgb values

```typescript
function detectHardcodedColors(component: string): ValidationResult {
  const content = fs.readFileSync(component, 'utf8');
  const hardcodedColors: string[] = [];

  // Find hardcoded colors in style blocks
  const styleMatches = content.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/g);
  for (const match of styleMatches) {
    const styleContent = match[1];
    const colorMatches = styleContent.matchAll(/(color|background|border)[^;]*:\s*(#[0-9a-f]{3,6}|rgb\([^)]+\))/gi);
    for (const colorMatch of colorMatches) {
      hardcodedColors.push(colorMatch[2]);
    }
  }

  if (hardcodedColors.length > 0) {
    return {
      valid: false,
      severity: 'warning',
      message: `Found ${hardcodedColors.length} hardcoded colors`,
      locations: hardcodedColors,
      fix: `Replace with Tailwind classes or CSS variables`
    };
  }

  return { valid: true };
}
```

---

## Typography Consistency Rules

### Rule 5: Modular Font Scale

**Severity:** 🟡 Info
**Rule:** Font sizes should follow modular scale (1.2-1.5 ratio)

```typescript
function validateModularScale(fontSizes: Record<string, any>): ValidationResult {
  const sizes = Object.values(fontSizes)
    .map(s => parseFloat(s.size))
    .sort((a, b) => a - b);

  const ratios = sizes.slice(1).map((size, i) => size / sizes[i]);
  const avgRatio = ratios.reduce((a, b) => a + b) / ratios.length;

  if (avgRatio < 1.2 || avgRatio > 1.5) {
    return {
      valid: false,
      severity: 'info',
      message: `Font scale ratio ${avgRatio.toFixed(2)} outside recommended 1.2-1.5 range`,
      fix: `Adjust font sizes to maintain consistent ratio`
    };
  }

  return { valid: true };
}
```

**Recommended Ratios:**
- 1.2 (Minor Third) - Subtle, conservative
- 1.25 (Major Third) - Balanced
- 1.333 (Perfect Fourth) - Distinct
- 1.5 (Perfect Fifth) - Dramatic

---

### Rule 6: Line Height Consistency

**Severity:** ⚠️ Warning
**Rule:** Line heights should be 1.2-1.8 for readability

```typescript
function validateLineHeights(fontSizes: Record<string, any>): ValidationResult {
  const issues: string[] = [];

  for (const [key, value] of Object.entries(fontSizes)) {
    const size = parseFloat(value.size);
    const lineHeight = parseFloat(value.lineHeight);
    const ratio = lineHeight / size;

    if (ratio < 1.2 || ratio > 1.8) {
      issues.push(`${key}: line-height ${lineHeight} / font-size ${size} = ${ratio.toFixed(2)} (should be 1.2-1.8)`);
    }
  }

  if (issues.length > 0) {
    return {
      valid: false,
      severity: 'warning',
      message: `Line height ratios outside recommended range`,
      locations: issues,
      fix: `Adjust line heights to 1.2-1.8 × font size`
    };
  }

  return { valid: true };
}
```

---

### Rule 7: Font Family Fallbacks

**Severity:** ❌ Error
**Rule:** All font families must include generic fallback

```typescript
function validateFontFallbacks(fontFamilies: Record<string, string[]>): ValidationResult {
  const genericFonts = ['serif', 'sans-serif', 'monospace', 'cursive', 'fantasy', 'system-ui'];
  const issues: string[] = [];

  for (const [key, family] of Object.entries(fontFamilies)) {
    const hasGenericFallback = family.some(f =>
      genericFonts.includes(f.toLowerCase().trim())
    );

    if (!hasGenericFallback) {
      issues.push(`${key}: ${family.join(', ')}`);
    }
  }

  if (issues.length > 0) {
    return {
      valid: false,
      severity: 'error',
      message: `Font families missing generic fallback`,
      locations: issues,
      fix: `Add generic fallback (serif, sans-serif, or monospace) to end of font stack`
    };
  }

  return { valid: true };
}
```

---

## Spacing Consistency Rules

### Rule 8: Spacing Scale Base

**Severity:** ⚠️ Warning
**Rule:** Spacing should use 4px or 8px base unit

```typescript
function validateSpacingBase(spacing: { base: string }): ValidationResult {
  const base = parseInt(spacing.base);

  if (base !== 4 && base !== 8) {
    return {
      valid: false,
      severity: 'warning',
      message: `Spacing base ${base}px is not 4px or 8px`,
      fix: `Use 4px (common) or 8px (Material Design) for better consistency`
    };
  }

  return { valid: true };
}
```

---

### Rule 9: Spacing Multiples

**Severity:** ⚠️ Warning
**Rule:** All spacing values should be multiples of base unit

```typescript
function validateSpacingMultiples(spacing: { base: string; scale: Record<string, string> }): ValidationResult {
  const base = parseInt(spacing.base);
  const issues: string[] = [];

  for (const [key, value] of Object.entries(spacing.scale)) {
    const val = parseInt(value);

    // Skip special values (0, 1px)
    if (val === 0 || val === 1) continue;

    if (val % base !== 0) {
      issues.push(`${key}: ${value} is not a multiple of ${base}px`);
    }
  }

  if (issues.length > 0) {
    return {
      valid: false,
      severity: 'warning',
      message: `Spacing values not multiples of base unit`,
      locations: issues,
      fix: `Adjust values to multiples of ${base}px`
    };
  }

  return { valid: true };
}
```

---

### Rule 10: No Hardcoded Spacing

**Severity:** ⚠️ Warning
**Rule:** Components should use spacing tokens, not hardcoded px values

```typescript
function detectHardcodedSpacing(component: string): ValidationResult {
  const content = fs.readFileSync(component, 'utf8');
  const hardcodedSpacing: string[] = [];

  // Find hardcoded spacing in style blocks
  const styleMatches = content.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/g);
  for (const match of styleMatches) {
    const styleContent = match[1];
    const spacingMatches = styleContent.matchAll(/(padding|margin|gap)[^;]*:\s*(\d+px)/gi);
    for (const spacingMatch of spacingMatches) {
      hardcodedSpacing.push(`${spacingMatch[1]}: ${spacingMatch[2]}`);
    }
  }

  if (hardcodedSpacing.length > 0) {
    return {
      valid: false,
      severity: 'warning',
      message: `Found ${hardcodedSpacing.length} hardcoded spacing values`,
      locations: hardcodedSpacing,
      fix: `Replace with Tailwind spacing classes (p-4, m-2, etc.)`
    };
  }

  return { valid: true };
}
```

---

## Border & Shadow Consistency Rules

### Rule 11: Border Radius Progression

**Severity:** 🟡 Info
**Rule:** Border radius values should increase logically

```typescript
function validateBorderRadiusProgression(borderRadius: Record<string, string>): ValidationResult {
  const entries = Object.entries(borderRadius)
    .filter(([key]) => key !== 'full' && key !== 'none')
    .map(([key, value]) => ({ key, value: parseFloat(value) }))
    .sort((a, b) => a.value - b.value);

  const issues: string[] = [];

  for (let i = 1; i < entries.length; i++) {
    const prev = entries[i - 1];
    const curr = entries[i];

    if (curr.value <= prev.value) {
      issues.push(`${curr.key} (${curr.value}) should be > ${prev.key} (${prev.value})`);
    }
  }

  if (issues.length > 0) {
    return {
      valid: false,
      severity: 'info',
      message: `Border radius values not in ascending order`,
      locations: issues,
      fix: `Ensure sm < DEFAULT < md < lg < xl progression`
    };
  }

  return { valid: true };
}
```

---

### Rule 12: Shadow Depth Progression

**Severity:** 🟡 Info
**Rule:** Shadow blur and spread should increase with elevation

```typescript
function validateShadowProgression(shadows: Record<string, string>): ValidationResult {
  // Extract blur radius from shadow definitions
  const entries = Object.entries(shadows)
    .filter(([key]) => key !== 'none' && key !== 'inner')
    .map(([key, value]) => {
      const blurMatch = value.match(/\s(\d+)px\s/);
      const blur = blurMatch ? parseInt(blurMatch[1]) : 0;
      return { key, blur };
    })
    .sort((a, b) => {
      const order = ['sm', 'DEFAULT', 'md', 'lg', 'xl', '2xl'];
      return order.indexOf(a.key) - order.indexOf(b.key);
    });

  const issues: string[] = [];

  for (let i = 1; i < entries.length; i++) {
    const prev = entries[i - 1];
    const curr = entries[i];

    if (curr.blur <= prev.blur) {
      issues.push(`${curr.key} blur (${curr.blur}px) should be > ${prev.key} blur (${prev.blur}px)`);
    }
  }

  if (issues.length > 0) {
    return {
      valid: false,
      severity: 'info',
      message: `Shadow blur not increasing with elevation`,
      locations: issues,
      fix: `Ensure sm < md < lg < xl shadow blur progression`
    };
  }

  return { valid: true };
}
```

---

## Component API Consistency Rules

### Rule 13: Consistent Prop Naming

**Severity:** 🟡 Info
**Rule:** Similar props should use consistent naming across components

**Common Patterns:**
- `variant` not `type` or `kind`
- `size` not `scale` or `dimension`
- `disabled` not `isDisabled` or `enabled`
- `loading` not `isLoading` or `busy`
- `onClick` not `handleClick` or `onPress`

```typescript
function validatePropNaming(components: string[]): ValidationResult {
  const propPatterns = {
    variant: ['type', 'kind', 'style'],
    size: ['scale', 'dimension'],
    disabled: ['isDisabled', 'enabled'],
    loading: ['isLoading', 'busy']
  };

  const issues: string[] = [];

  for (const component of components) {
    const content = fs.readFileSync(component, 'utf8');

    for (const [preferred, alternatives] of Object.entries(propPatterns)) {
      for (const alt of alternatives) {
        if (content.includes(`export let ${alt}`)) {
          issues.push(`${component}: Use "${preferred}" instead of "${alt}"`);
        }
      }
    }
  }

  if (issues.length > 0) {
    return {
      valid: false,
      severity: 'info',
      message: `Inconsistent prop naming detected`,
      locations: issues,
      fix: `Rename props to follow consistent patterns`
    };
  }

  return { valid: true };
}
```

---

## Validation Summary

### Run All Consistency Checks

```typescript
async function validateDesignConsistency(
  tokens: DesignSystem,
  componentsDir: string
): Promise<ValidationSummary> {
  const results = await Promise.all([
    // Color rules
    validateColorContrast(tokens.colors),
    validateColorScale(tokens.colors.primary),
    validateSemanticColors(tokens.colors.semantic),

    // Typography rules
    validateModularScale(tokens.typography.fontSizes),
    validateLineHeights(tokens.typography.fontSizes),
    validateFontFallbacks(tokens.typography.fontFamilies),

    // Spacing rules
    validateSpacingBase(tokens.spacing),
    validateSpacingMultiples(tokens.spacing),

    // Border & shadow rules
    validateBorderRadiusProgression(tokens.borderRadius),
    validateShadowProgression(tokens.shadows),

    // Component rules
    detectHardcodedColors(componentsDir),
    detectHardcodedSpacing(componentsDir),
    validatePropNaming(componentsDir)
  ]);

  const errors = results.filter(r => !r.valid && r.severity === 'error');
  const warnings = results.filter(r => !r.valid && r.severity === 'warning');
  const info = results.filter(r => !r.valid && r.severity === 'info');

  return {
    total_checks: results.length,
    passed: results.filter(r => r.valid).length,
    errors: errors.length,
    warnings: warnings.length,
    info: info.length,
    results: results
  };
}
```

---

*End of Design Consistency Rules*
