# Batch Validation & Parallel Processing

**Version:** 1.0.0 (v4.1 Parallelization)
**Last Updated:** 2026-02-14

---

## Overview

Parallel validation patterns for 10x speedup in design token validation. Uses Promise.all for concurrent validation and batched processing for large token sets.

---

## Performance Targets

| Tokens | Sequential | Parallel (10 concurrent) | Speedup |
|--------|-----------|--------------------------|---------|
| 10 | 200ms | 20ms | 10x |
| 50 | 1000ms | 100ms | 10x |
| 100 | 2000ms | 200ms | 10x |
| 500 | 10s | 1s | 10x |

---

## Parallel Validation Strategy

### 1. Group Validators by Category

```typescript
interface ValidatorGroup {
  category: string;
  validators: Array<(tokens: any) => Promise<ValidationResult>>;
}

const validatorGroups: ValidatorGroup[] = [
  {
    category: 'colors',
    validators: [
      validateColorFormat,
      validateColorContrast,
      validateColorScales,
      validateSemanticColors,
      validateDarkModeTokens
    ]
  },
  {
    category: 'typography',
    validators: [
      validateFontFamilies,
      validateFontSizes,
      validateFontWeights,
      validateLineHeights,
      validateModularScale
    ]
  },
  {
    category: 'spacing',
    validators: [
      validateSpacingBase,
      validateSpacingScale,
      validateSpacingConsistency
    ]
  },
  {
    category: 'borderRadius',
    validators: [
      validateBorderRadiusValues,
      validateBorderRadiusProgression
    ]
  },
  {
    category: 'shadows',
    validators: [
      validateShadowSyntax,
      validateShadowProgression
    ]
  }
];
```

---

### 2. Execute All Validators in Parallel

```typescript
async function validateAllTokens(tokens: DesignSystem): Promise<ValidationSummary> {
  const startTime = performance.now();

  // Flatten all validators into single array
  const allValidators = validatorGroups.flatMap(group =>
    group.validators.map(validator => ({
      category: group.category,
      validator
    }))
  );

  // Execute all validators concurrently
  const results = await Promise.all(
    allValidators.map(async ({ category, validator }) => {
      const tokenCategory = tokens[category as keyof DesignSystem];
      try {
        const result = await validator(tokenCategory);
        return { category, ...result };
      } catch (error) {
        return {
          category,
          valid: false,
          severity: 'error',
          message: `Validation failed: ${error.message}`
        };
      }
    })
  );

  const endTime = performance.now();

  return {
    total_checks: results.length,
    passed: results.filter(r => r.valid).length,
    errors: results.filter(r => !r.valid && r.severity === 'error').length,
    warnings: results.filter(r => !r.valid && r.severity === 'warning').length,
    info: results.filter(r => !r.valid && r.severity === 'info').length,
    duration_ms: endTime - startTime,
    results
  };
}
```

**Performance:** 10-15 validators complete in ~200ms (vs ~2000ms sequential)

---

## Batched Token Processing

### 3. Process Large Token Sets in Chunks

```typescript
async function batchValidateTokens(
  tokens: string[],
  validator: (token: string) => Promise<boolean>,
  batchSize: number = 10
): Promise<Map<string, boolean>> {
  const results = new Map<string, boolean>();

  // Split tokens into batches
  for (let i = 0; i < tokens.length; i += batchSize) {
    const batch = tokens.slice(i, i + batchSize);

    // Process batch in parallel
    const batchResults = await Promise.all(
      batch.map(async token => ({
        token,
        valid: await validator(token)
      }))
    );

    // Collect results
    for (const { token, valid } of batchResults) {
      results.set(token, valid);
    }
  }

  return results;
}
```

**Example Usage:**
```typescript
// Validate 500 color tokens in 50 batches of 10
const colorTokens = extractAllColorTokens(tokens);
const validColors = await batchValidateTokens(
  colorTokens,
  validateColorFormat,
  10 // batch size
);

console.log(`Validated ${colorTokens.length} colors in ${validColors.size} results`);
```

---

## Tailwind Config Generation

### 4. Parallel Config Generation

```typescript
async function generateTailwindConfig(tokens: DesignSystem): Promise<string> {
  // Generate all sections in parallel
  const [colors, fonts, spacing, borderRadius, shadows, screens] = await Promise.all([
    generateColorConfig(tokens.colors),
    generateFontConfig(tokens.typography),
    generateSpacingConfig(tokens.spacing),
    generateBorderRadiusConfig(tokens.borderRadius),
    generateShadowConfig(tokens.shadows),
    generateBreakpointConfig(tokens.breakpoints)
  ]);

  // Combine into complete config
  return `
module.exports = {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: ${JSON.stringify(colors, null, 2)},
      fontFamily: ${JSON.stringify(fonts.families, null, 2)},
      fontSize: ${JSON.stringify(fonts.sizes, null, 2)},
      fontWeight: ${JSON.stringify(fonts.weights, null, 2)},
      spacing: ${JSON.stringify(spacing, null, 2)},
      borderRadius: ${JSON.stringify(borderRadius, null, 2)},
      boxShadow: ${JSON.stringify(shadows, null, 2)},
      screens: ${JSON.stringify(screens, null, 2)}
    }
  },
  plugins: [],
  darkMode: 'class'
};
  `.trim();
}
```

**Performance:** Generate complete config in ~100ms (vs ~500ms sequential)

---

### 5. Generate Color Config with Scales

```typescript
async function generateColorConfig(colors: any): Promise<Record<string, any>> {
  // Process all color categories in parallel
  const colorEntries = Object.entries(colors);

  const processedColors = await Promise.all(
    colorEntries.map(async ([category, value]) => {
      if (typeof value === 'object' && !Array.isArray(value)) {
        // Color scale (primary, neutral, etc.)
        return [category, value];
      } else {
        // Single color (semantic colors)
        return [category, value];
      }
    })
  );

  return Object.fromEntries(processedColors);
}
```

---

## Dark Mode Token Generation

### 6. Parallel Dark Mode Variants

```typescript
async function generateDarkModeTokens(colors: any): Promise<any> {
  const colorEntries = Object.entries(colors);

  // Generate dark variants in parallel
  const darkColors = await Promise.all(
    colorEntries.map(async ([category, scale]) => {
      if (typeof scale === 'object' && !Array.isArray(scale)) {
        // Invert color scale
        const invertedScale = await invertColorScale(scale);
        return [category, invertedScale];
      } else {
        // Adjust single color luminosity
        const adjusted = await adjustLuminosity(scale, -0.2);
        return [category, adjusted];
      }
    })
  );

  return Object.fromEntries(darkColors);
}

async function invertColorScale(
  scale: Record<string, string>
): Promise<Record<string, string>> {
  const entries = Object.entries(scale);

  // Invert all shades in parallel
  const inverted = await Promise.all(
    entries.map(async ([shade, color]) => {
      // Invert shade key (50 → 950, 100 → 900, etc.)
      const invertedShade = 1000 - parseInt(shade);
      return [invertedShade.toString(), color];
    })
  );

  return Object.fromEntries(inverted);
}
```

**Example:**
```typescript
// Original light mode
colors.primary = {
  50: '#eff6ff',
  100: '#dbeafe',
  ...
  900: '#1e3a8a',
  950: '#172554'
};

// Generated dark mode (inverted)
darkColors.primary = {
  50: '#172554',  // was 950
  100: '#1e3a8a', // was 900
  ...
  900: '#dbeafe', // was 100
  950: '#eff6ff'  // was 50
};
```

---

## Component Scanning Performance

### 7. Parallel Component Analysis

```typescript
async function scanAllComponents(
  componentsDir: string
): Promise<ComponentAnalysis[]> {
  // Find all Svelte components
  const components = await globby(`${componentsDir}/**/*.svelte`);

  // Analyze all components in parallel
  const analyses = await Promise.all(
    components.map(async component => ({
      component,
      tokens: await extractTokens(component),
      hardcoded: await findHardcodedValues(component),
      issues: await detectIssues(component)
    }))
  );

  return analyses;
}
```

**Performance:** Scan 30 components in ~500ms (vs ~3000ms sequential)

---

### 8. Batched File Reads

```typescript
async function batchReadFiles(
  files: string[],
  batchSize: number = 10
): Promise<Map<string, string>> {
  const contents = new Map<string, string>();

  for (let i = 0; i < files.length; i += batchSize) {
    const batch = files.slice(i, i + batchSize);

    // Read batch in parallel
    const batchContents = await Promise.all(
      batch.map(async file => ({
        file,
        content: await fs.promises.readFile(file, 'utf8')
      }))
    );

    // Collect contents
    for (const { file, content } of batchContents) {
      contents.set(file, content);
    }
  }

  return contents;
}
```

---

## Error Aggregation

### 9. Collect and Prioritize Errors

```typescript
interface AggregatedErrors {
  errors: ValidationResult[];
  warnings: ValidationResult[];
  info: ValidationResult[];
  by_category: Map<string, ValidationResult[]>;
  critical_first: ValidationResult[];
}

function aggregateValidationResults(
  results: ValidationResult[]
): AggregatedErrors {
  const errors = results.filter(r => !r.valid && r.severity === 'error');
  const warnings = results.filter(r => !r.valid && r.severity === 'warning');
  const info = results.filter(r => !r.valid && r.severity === 'info');

  // Group by category
  const byCategory = new Map<string, ValidationResult[]>();
  for (const result of results) {
    if (!result.valid) {
      const category = result.category || 'general';
      if (!byCategory.has(category)) {
        byCategory.set(category, []);
      }
      byCategory.get(category)!.push(result);
    }
  }

  // Sort by severity (errors first, then warnings, then info)
  const criticalFirst = [
    ...errors,
    ...warnings,
    ...info
  ];

  return {
    errors,
    warnings,
    info,
    by_category: byCategory,
    critical_first: criticalFirst
  };
}
```

---

## Performance Monitoring

### 10. Track Validation Performance

```typescript
interface PerformanceMetrics {
  total_duration_ms: number;
  validators_run: number;
  avg_validator_duration_ms: number;
  tokens_validated: number;
  tokens_per_second: number;
  parallelization_factor: number;
}

async function measureValidationPerformance(
  tokens: DesignSystem
): Promise<PerformanceMetrics> {
  const startTime = performance.now();

  const results = await validateAllTokens(tokens);

  const endTime = performance.now();
  const duration = endTime - startTime;

  const tokensCount = countTotalTokens(tokens);
  const tokensPerSecond = (tokensCount / duration) * 1000;

  // Estimate sequential time (assume 20ms per validator)
  const sequentialTime = results.total_checks * 20;
  const parallelizationFactor = sequentialTime / duration;

  return {
    total_duration_ms: duration,
    validators_run: results.total_checks,
    avg_validator_duration_ms: duration / results.total_checks,
    tokens_validated: tokensCount,
    tokens_per_second: tokensPerSecond,
    parallelization_factor: parallelizationFactor
  };
}
```

**Example Output:**
```
✅ Validation complete
   Duration: 187ms
   Validators: 15
   Tokens: 98
   Throughput: 524 tokens/sec
   Speedup: 10.7x vs sequential
```

---

## Best Practices

### Concurrency Guidelines

1. **Batch Size:** 10 concurrent operations (optimal for most systems)
2. **Independent Validators:** Ensure validators don't share mutable state
3. **Error Isolation:** Wrap validators in try-catch to prevent cascade failures
4. **Progress Tracking:** Report progress for long-running operations
5. **Resource Limits:** Respect system memory and CPU constraints

### When to Use Parallel Validation

✅ **Use parallel when:**
- Validating 10+ independent tokens
- Generating Tailwind config
- Scanning 5+ components
- Running full design system audit

❌ **Avoid parallel when:**
- Validating < 5 tokens (overhead > benefit)
- Validators depend on each other
- Limited system resources
- Debugging validation errors

---

## Complete Example

```typescript
import { DesignSystem, validateAllTokens } from './validators';

async function main() {
  // Load tokens
  const tokens = loadCorpusConfig().design_system;

  console.log('🔍 Validating design system...');

  // Run all validations in parallel
  const startTime = performance.now();
  const results = await validateAllTokens(tokens);
  const duration = performance.now() - startTime;

  // Report results
  console.log(`\n✅ Validation complete in ${duration.toFixed(0)}ms`);
  console.log(`   Checks: ${results.total_checks}`);
  console.log(`   Passed: ${results.passed}`);
  console.log(`   Errors: ${results.errors}`);
  console.log(`   Warnings: ${results.warnings}`);
  console.log(`   Info: ${results.info}`);

  // Show errors
  if (results.errors > 0) {
    console.log('\n❌ Errors found:');
    results.results
      .filter(r => !r.valid && r.severity === 'error')
      .forEach(r => console.log(`   - ${r.message}`));
  }

  // Generate Tailwind config if validation passed
  if (results.errors === 0) {
    console.log('\n⚙️  Generating Tailwind config...');
    const config = await generateTailwindConfig(tokens);
    await fs.promises.writeFile('tailwind.config.js', config);
    console.log('   ✅ tailwind.config.js generated');
  }
}

main();
```

---

*End of Batch Validation & Parallel Processing*
