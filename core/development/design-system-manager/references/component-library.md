# Component Library & Token Usage Tracking

**Version:** 1.0.0
**Last Updated:** 2026-02-14

---

## Overview

Track design token usage across components, identify unused tokens, and ensure consistency in component implementation.

---

## Token Usage Tracking

### Scan Components for Token References

```typescript
import { globby } from 'globby';
import fs from 'fs';

async function trackTokenUsage(componentsDir: string) {
  // Find all Svelte components
  const components = await globby(`${componentsDir}/**/*.svelte`);

  const usageMap = new Map<string, {
    count: number;
    components: string[];
  }>();

  for (const component of components) {
    const content = fs.readFileSync(component, 'utf8');

    // Extract Tailwind classes
    const classMatches = content.matchAll(/class(?::[\w-]+)?="([^"]+)"/g);

    for (const match of classMatches) {
      const classes = match[1].split(/\s+/);

      for (const cls of classes) {
        // Map Tailwind class to design token
        const token = mapClassToToken(cls);

        if (token) {
          if (!usageMap.has(token)) {
            usageMap.set(token, { count: 0, components: [] });
          }

          const usage = usageMap.get(token)!;
          usage.count++;
          if (!usage.components.includes(component)) {
            usage.components.push(component);
          }
        }
      }
    }
  }

  return usageMap;
}
```

---

## Tailwind Class to Token Mapping

### Color Tokens

```typescript
function mapColorClassToToken(cls: string): string | null {
  // bg-primary-500 → colors.primary.500
  const bgMatch = cls.match(/^bg-(\w+)-(\d+)$/);
  if (bgMatch) return `colors.${bgMatch[1]}.${bgMatch[2]}`;

  // text-success → colors.semantic.success
  const textSemanticMatch = cls.match(/^text-(success|warning|error|info)$/);
  if (textSemanticMatch) return `colors.semantic.${textSemanticMatch[1]}`;

  // border-neutral-200 → colors.neutral.200
  const borderMatch = cls.match(/^border-(\w+)-(\d+)$/);
  if (borderMatch) return `colors.${borderMatch[1]}.${borderMatch[2]}`;

  return null;
}
```

### Typography Tokens

```typescript
function mapTypographyClassToToken(cls: string): string | null {
  // text-xs → typography.fontSizes.xs
  const sizeMatch = cls.match(/^text-(xs|sm|base|lg|xl|2xl|3xl|4xl)$/);
  if (sizeMatch) return `typography.fontSizes.${sizeMatch[1]}`;

  // font-bold → typography.fontWeights.bold
  const weightMatch = cls.match(/^font-(thin|light|normal|medium|semibold|bold|black)$/);
  if (weightMatch) return `typography.fontWeights.${weightMatch[1]}`;

  // font-sans → typography.fontFamilies.sans
  const familyMatch = cls.match(/^font-(sans|serif|mono)$/);
  if (familyMatch) return `typography.fontFamilies.${familyMatch[1]}`;

  return null;
}
```

### Spacing Tokens

```typescript
function mapSpacingClassToToken(cls: string): string | null {
  // p-4 → spacing.scale.4
  const paddingMatch = cls.match(/^p[trblxy]?-(\d+\.?\d*)$/);
  if (paddingMatch) return `spacing.scale.${paddingMatch[1]}`;

  // m-2 → spacing.scale.2
  const marginMatch = cls.match(/^-?m[trblxy]?-(\d+\.?\d*)$/);
  if (marginMatch) return `spacing.scale.${marginMatch[1]}`;

  // gap-6 → spacing.scale.6
  const gapMatch = cls.match(/^gap-[xy]?-(\d+\.?\d*)$/);
  if (gapMatch) return `spacing.scale.${gapMatch[1]}`;

  // space-x-4 → spacing.scale.4
  const spaceMatch = cls.match(/^space-[xy]-(\d+\.?\d*)$/);
  if (spaceMatch) return `spacing.scale.${spaceMatch[1]}`;

  return null;
}
```

### Border Radius Tokens

```typescript
function mapBorderRadiusClassToToken(cls: string): string | null {
  // rounded-lg → borderRadius.lg
  const match = cls.match(/^rounded(?:-(\w+))?$/);
  if (match) {
    const key = match[1] || 'DEFAULT';
    return `borderRadius.${key}`;
  }

  return null;
}
```

### Shadow Tokens

```typescript
function mapShadowClassToToken(cls: string): string | null {
  // shadow-md → shadows.md
  const match = cls.match(/^shadow(?:-(\w+))?$/);
  if (match) {
    const key = match[1] || 'DEFAULT';
    return `shadows.${key}`;
  }

  return null;
}
```

### Complete Mapping Function

```typescript
function mapClassToToken(cls: string): string | null {
  return (
    mapColorClassToToken(cls) ||
    mapTypographyClassToToken(cls) ||
    mapSpacingClassToToken(cls) ||
    mapBorderRadiusClassToToken(cls) ||
    mapShadowClassToToken(cls)
  );
}
```

---

## Unused Token Detection

```typescript
function findUnusedTokens(
  tokens: DesignSystem,
  usageMap: Map<string, any>
): string[] {
  const unusedTokens: string[] = [];

  // Check color tokens
  for (const [category, colors] of Object.entries(tokens.colors)) {
    if (typeof colors === 'object') {
      for (const shade in colors) {
        const tokenPath = `colors.${category}.${shade}`;
        if (!usageMap.has(tokenPath)) {
          unusedTokens.push(tokenPath);
        }
      }
    }
  }

  // Check typography tokens
  for (const size in tokens.typography.fontSizes) {
    const tokenPath = `typography.fontSizes.${size}`;
    if (!usageMap.has(tokenPath)) {
      unusedTokens.push(tokenPath);
    }
  }

  // Check spacing tokens
  for (const key in tokens.spacing.scale) {
    const tokenPath = `spacing.scale.${key}`;
    if (!usageMap.has(tokenPath)) {
      unusedTokens.push(tokenPath);
    }
  }

  // Check border radius tokens
  for (const key in tokens.borderRadius) {
    const tokenPath = `borderRadius.${key}`;
    if (!usageMap.has(tokenPath)) {
      unusedTokens.push(tokenPath);
    }
  }

  // Check shadow tokens
  for (const key in tokens.shadows) {
    const tokenPath = `shadows.${key}`;
    if (!usageMap.has(tokenPath)) {
      unusedTokens.push(tokenPath);
    }
  }

  return unusedTokens;
}
```

---

## Usage Coverage Report

```typescript
interface CoverageReport {
  total_tokens: number;
  used_tokens: number;
  unused_tokens: number;
  coverage_percentage: number;
  total_components: number;
  components_using_tokens: number;
  token_usage_breakdown: {
    colors: { total: number; used: number; coverage: number };
    typography: { total: number; used: number; coverage: number };
    spacing: { total: number; used: number; coverage: number };
    borderRadius: { total: number; used: number; coverage: number };
    shadows: { total: number; used: number; coverage: number };
  };
  most_used_tokens: Array<{ token: string; count: number }>;
  unused_tokens: string[];
}

async function generateCoverageReport(
  tokens: DesignSystem,
  componentsDir: string
): Promise<CoverageReport> {
  const usageMap = await trackTokenUsage(componentsDir);
  const unusedTokens = findUnusedTokens(tokens, usageMap);

  // Calculate coverage
  const totalTokens = countTotalTokens(tokens);
  const usedTokens = usageMap.size;
  const coverage = (usedTokens / totalTokens) * 100;

  // Find most used tokens
  const mostUsed = Array.from(usageMap.entries())
    .sort((a, b) => b[1].count - a[1].count)
    .slice(0, 10)
    .map(([token, usage]) => ({ token, count: usage.count }));

  return {
    total_tokens: totalTokens,
    used_tokens: usedTokens,
    unused_tokens: unusedTokens.length,
    coverage_percentage: coverage,
    total_components: /* count */,
    components_using_tokens: /* count */,
    token_usage_breakdown: /* calculate */,
    most_used_tokens: mostUsed,
    unused_tokens: unusedTokens
  };
}
```

---

## Component Token Audit

### Per-Component Analysis

```typescript
interface ComponentTokenAudit {
  component: string;
  tokens_used: string[];
  hardcoded_values: string[];
  issues: Array<{
    type: 'hardcoded-color' | 'hardcoded-spacing' | 'missing-token';
    location: string;
    value: string;
    recommendation: string;
  }>;
}

function auditComponent(component: string, tokens: DesignSystem): ComponentTokenAudit {
  const content = fs.readFileSync(component, 'utf8');
  const tokensUsed: string[] = [];
  const hardcodedValues: string[] = [];
  const issues: any[] = [];

  // Find Tailwind classes
  const classMatches = content.matchAll(/class(?::[\w-]+)?="([^"]+)"/g);
  for (const match of classMatches) {
    const classes = match[1].split(/\s+/);
    for (const cls of classes) {
      const token = mapClassToToken(cls);
      if (token) {
        tokensUsed.push(token);
      }
    }
  }

  // Find hardcoded colors in style blocks
  const colorMatches = content.matchAll(/(?:color|background|border):\s*(#[0-9a-f]{3,6})/gi);
  for (const match of colorMatches) {
    hardcodedValues.push(match[1]);
    issues.push({
      type: 'hardcoded-color',
      location: component,
      value: match[1],
      recommendation: 'Replace with design token from colors.*'
    });
  }

  // Find hardcoded spacing in style blocks
  const spacingMatches = content.matchAll(/(padding|margin|gap):\s*(\d+px)/gi);
  for (const match of spacingMatches) {
    hardcodedValues.push(match[2]);
    issues.push({
      type: 'hardcoded-spacing',
      location: component,
      value: match[2],
      recommendation: 'Replace with design token from spacing.scale'
    });
  }

  return {
    component,
    tokens_used: tokensUsed,
    hardcoded_values: hardcodedValues,
    issues
  };
}
```

---

## Batch Component Auditing

```typescript
async function auditAllComponents(
  componentsDir: string,
  tokens: DesignSystem
): Promise<ComponentTokenAudit[]> {
  const components = await globby(`${componentsDir}/**/*.svelte`);

  // Batch audit in parallel (10 concurrent)
  const audits = await Promise.all(
    components.map(component => auditComponent(component, tokens))
  );

  return audits;
}
```

---

## Recommendations Engine

```typescript
interface TokenRecommendation {
  component: string;
  current_value: string;
  recommended_token: string;
  confidence: number; // 0-1
}

function recommendTokenReplacement(
  hardcodedValue: string,
  tokens: DesignSystem
): TokenRecommendation | null {
  // Color replacement
  if (hardcodedValue.match(/^#[0-9a-f]{3,6}$/i)) {
    const closestToken = findClosestColor(hardcodedValue, tokens.colors);
    return {
      component: /* context */,
      current_value: hardcodedValue,
      recommended_token: closestToken.path,
      confidence: closestToken.similarity
    };
  }

  // Spacing replacement
  if (hardcodedValue.match(/^\d+px$/)) {
    const closestSpacing = findClosestSpacing(hardcodedValue, tokens.spacing);
    return {
      component: /* context */,
      current_value: hardcodedValue,
      recommended_token: closestSpacing.path,
      confidence: closestSpacing.similarity
    };
  }

  return null;
}
```

---

## Export Formats

### JSON Report

```json
{
  "timestamp": "2026-02-14T13:30:00Z",
  "total_tokens": 98,
  "used_tokens": 85,
  "unused_tokens": 13,
  "coverage_percentage": 86.7,
  "total_components": 30,
  "components_using_tokens": 28,
  "most_used_tokens": [
    { "token": "colors.primary.500", "count": 45 },
    { "token": "spacing.scale.4", "count": 38 },
    { "token": "typography.fontSizes.base", "count": 32 }
  ],
  "unused_tokens": [
    "colors.primary.950",
    "spacing.scale.32",
    "shadows.2xl"
  ],
  "issues": [
    {
      "component": "Button.svelte",
      "type": "hardcoded-color",
      "value": "#3b82f6",
      "recommendation": "Use colors.primary.500"
    }
  ]
}
```

### Markdown Report

```markdown
# Design Token Usage Report

**Generated:** 2026-02-14 13:30:00
**Coverage:** 86.7% (85/98 tokens used)

## Summary

- Total Tokens: 98
- Used Tokens: 85
- Unused Tokens: 13
- Total Components: 30
- Components Using Tokens: 28

## Most Used Tokens

1. `colors.primary.500` - 45 uses
2. `spacing.scale.4` - 38 uses
3. `typography.fontSizes.base` - 32 uses

## Unused Tokens

- `colors.primary.950`
- `spacing.scale.32`
- `shadows.2xl`

## Issues Found

### Button.svelte
- **Hardcoded color:** `#3b82f6`
- **Recommendation:** Use `colors.primary.500`
```

---

*End of Component Library & Token Usage Tracking*
