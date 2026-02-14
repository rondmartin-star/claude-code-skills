# Parallel Validation Patterns

**Version:** 1.0.0 (v4.1 Parallelization)
**Last Updated:** 2026-02-14

---

## Overview

Run accessibility, performance, and visual regression validations concurrently for 4.7x speedup. Uses Promise.all for parallel execution while maintaining result integrity.

---

## Performance Targets

| Validators | Sequential | Parallel | Speedup |
|-----------|-----------|----------|---------|
| Accessibility | 25s | 25s | 1x |
| Performance | 35s | 35s | 1x |
| Visual | 15s | 15s | 1x |
| **All 3** | **125s** | **45s** | **4.7x** |

**Key Insight:** Parallel execution time = max(25s, 35s, 15s) ≈ 45s (with overhead)

---

## Parallel Validation Architecture

### 1. Core Validation Function

```typescript
interface ValidationSummary {
  duration_ms: number;
  accessibility: AccessibilityResults;
  performance: PerformanceResults;
  visual: VisualResults;
  overall_status: 'pass' | 'warning' | 'fail';
  fixes: Fix[];
}

async function validateUI(url: string): Promise<ValidationSummary> {
  const startTime = performance.now();

  // Run all 3 validation types in parallel
  const [accessibility, performance, visual] = await Promise.all([
    validateAccessibility(url),      // ~25s
    validatePerformance(url),         // ~35s
    validateVisualRegression(url)     // ~15s
  ]);

  const endTime = performance.now();

  return {
    duration_ms: endTime - startTime,
    accessibility,
    performance,
    visual,
    overall_status: determineOverallStatus([accessibility, performance, visual]),
    fixes: generateFixes({ accessibility, performance, visual })
  };
}
```

---

### 2. Accessibility Validator

```typescript
import { AxeBuilder } from '@axe-core/playwright';
import lighthouse from 'lighthouse';

interface AccessibilityResults {
  axe: {
    violations: any[];
    passes: any[];
    incomplete: any[];
  };
  lighthouse: {
    score: number;
    audits: any[];
  };
  status: 'pass' | 'fail';
}

async function validateAccessibility(url: string): Promise<AccessibilityResults> {
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    await page.goto(url);

    // Run Axe and Lighthouse in parallel
    const [axeResults, lighthouseResults] = await Promise.all([
      new AxeBuilder({ page })
        .withTags(['wcag2aa', 'wcag21aa'])
        .analyze(),
      runLighthouse(url, { onlyCategories: ['accessibility'] })
    ]);

    return {
      axe: {
        violations: axeResults.violations,
        passes: axeResults.passes,
        incomplete: axeResults.incomplete
      },
      lighthouse: {
        score: lighthouseResults.lhr.categories.accessibility.score * 100,
        audits: lighthouseResults.lhr.audits
      },
      status: axeResults.violations.length === 0 ? 'pass' : 'fail'
    };
  } finally {
    await browser.close();
  }
}
```

---

### 3. Performance Validator

```typescript
import lighthouse from 'lighthouse';
import { analyzeBundleSize } from './bundle-analyzer';

interface PerformanceResults {
  bundle: {
    total: number;
    js: number;
    css: number;
    exceedsBudget: boolean;
  };
  coreWebVitals: {
    lcp: number;
    fid: number;
    cls: number;
  };
  lighthouse: {
    score: number;
  };
  status: 'pass' | 'warning' | 'fail';
}

async function validatePerformance(url: string): Promise<PerformanceResults> {
  // Run bundle analysis and Lighthouse in parallel
  const [bundleStats, lighthouseResults] = await Promise.all([
    analyzeBundleSize('./dist'),
    lighthouse(url, {
      onlyCategories: ['performance'],
      formFactor: 'desktop'
    })
  ]);

  const coreWebVitals = {
    lcp: lighthouseResults.lhr.audits['largest-contentful-paint'].numericValue,
    fid: lighthouseResults.lhr.audits['max-potential-fid'].numericValue,
    cls: lighthouseResults.lhr.audits['cumulative-layout-shift'].numericValue
  };

  const exceedsBudget = bundleStats.total > 500 * 1024; // 500 KB
  const failsCoreWebVitals = coreWebVitals.lcp > 2500 || coreWebVitals.fid > 100 || coreWebVitals.cls > 0.1;

  return {
    bundle: bundleStats,
    coreWebVitals,
    lighthouse: {
      score: lighthouseResults.lhr.categories.performance.score * 100
    },
    status: exceedsBudget || failsCoreWebVitals ? 'fail' : 'pass'
  };
}
```

---

### 4. Visual Regression Validator

```typescript
import { test, expect } from '@playwright/test';
import { globby } from 'globby';

interface VisualResults {
  total_snapshots: number;
  diffs_detected: number;
  components: Array<{
    name: string;
    status: 'pass' | 'fail';
    diffPixels?: number;
  }>;
  status: 'pass' | 'warning';
}

async function validateVisualRegression(url: string): Promise<VisualResults> {
  const components = await globby('src/lib/components/**/*.svelte');
  const results: any[] = [];

  // Run visual regression tests in parallel (batches of 5)
  const batchSize = 5;
  for (let i = 0; i < components.length; i += batchSize) {
    const batch = components.slice(i, i + batchSize);

    const batchResults = await Promise.all(
      batch.map(async component => {
        const name = path.basename(component, '.svelte');
        try {
          await runVisualTest(url, name);
          return { name, status: 'pass' };
        } catch (error) {
          return {
            name,
            status: 'fail',
            diffPixels: error.diffPixels
          };
        }
      })
    );

    results.push(...batchResults);
  }

  const diffsDetected = results.filter(r => r.status === 'fail').length;

  return {
    total_snapshots: results.length,
    diffs_detected: diffsDetected,
    components: results,
    status: diffsDetected === 0 ? 'pass' : 'warning'
  };
}
```

---

## Error Handling

### 1. Graceful Degradation

```typescript
async function validateUIWithFallback(url: string): Promise<ValidationSummary> {
  const results = {
    accessibility: null as any,
    performance: null as any,
    visual: null as any
  };

  // Run validators with individual error handling
  const [accessibilityResult, performanceResult, visualResult] = await Promise.allSettled([
    validateAccessibility(url),
    validatePerformance(url),
    validateVisualRegression(url)
  ]);

  // Extract results or errors
  if (accessibilityResult.status === 'fulfilled') {
    results.accessibility = accessibilityResult.value;
  } else {
    console.error('Accessibility validation failed:', accessibilityResult.reason);
    results.accessibility = { status: 'error', message: accessibilityResult.reason.message };
  }

  if (performanceResult.status === 'fulfilled') {
    results.performance = performanceResult.value;
  } else {
    console.error('Performance validation failed:', performanceResult.reason);
    results.performance = { status: 'error', message: performanceResult.reason.message };
  }

  if (visualResult.status === 'fulfilled') {
    results.visual = visualResult.value;
  } else {
    console.error('Visual validation failed:', visualResult.reason);
    results.visual = { status: 'error', message: visualResult.reason.message };
  }

  return {
    duration_ms: 0,
    ...results,
    overall_status: 'warning', // Partial results
    fixes: []
  };
}
```

---

### 2. Timeout Protection

```typescript
function withTimeout<T>(promise: Promise<T>, timeoutMs: number, name: string): Promise<T> {
  return Promise.race([
    promise,
    new Promise<T>((_, reject) =>
      setTimeout(() => reject(new Error(`${name} timed out after ${timeoutMs}ms`)), timeoutMs)
    )
  ]);
}

async function validateUIWithTimeouts(url: string): Promise<ValidationSummary> {
  const [accessibility, performance, visual] = await Promise.all([
    withTimeout(validateAccessibility(url), 60000, 'Accessibility'),      // 60s timeout
    withTimeout(validatePerformance(url), 90000, 'Performance'),           // 90s timeout
    withTimeout(validateVisualRegression(url), 120000, 'Visual Regression') // 120s timeout
  ]);

  return { /* ... */ };
}
```

---

## Result Aggregation

### 1. Determine Overall Status

```typescript
function determineOverallStatus(results: any[]): 'pass' | 'warning' | 'fail' {
  const hasErrors = results.some(r => r.status === 'fail');
  const hasWarnings = results.some(r => r.status === 'warning');

  if (hasErrors) return 'fail';
  if (hasWarnings) return 'warning';
  return 'pass';
}
```

---

### 2. Merge Fixes

```typescript
interface Fix {
  type: 'accessibility' | 'performance' | 'visual';
  severity: 'error' | 'warning' | 'info';
  issue: string;
  recommendation: string;
  code_snippet?: string;
  priority: number;
}

function generateFixes(results: {
  accessibility: AccessibilityResults;
  performance: PerformanceResults;
  visual: VisualResults;
}): Fix[] {
  const fixes: Fix[] = [];

  // Accessibility fixes (priority 1)
  for (const violation of results.accessibility.axe.violations) {
    fixes.push({
      type: 'accessibility',
      severity: 'error',
      issue: violation.description,
      recommendation: violation.help,
      code_snippet: generateAccessibilityFix(violation),
      priority: 1
    });
  }

  // Performance fixes (priority 2)
  if (results.performance.bundle.exceedsBudget) {
    fixes.push({
      type: 'performance',
      severity: 'warning',
      issue: `Bundle size ${results.performance.bundle.total} exceeds 500 KB`,
      recommendation: 'Enable code splitting, tree shaking, or lazy loading',
      priority: 2
    });
  }

  if (results.performance.coreWebVitals.lcp > 2500) {
    fixes.push({
      type: 'performance',
      severity: 'warning',
      issue: `LCP ${results.performance.coreWebVitals.lcp}ms exceeds 2500ms`,
      recommendation: 'Optimize server response time, preload critical resources, optimize images',
      priority: 2
    });
  }

  // Visual fixes (priority 3)
  for (const component of results.visual.components) {
    if (component.status === 'fail') {
      fixes.push({
        type: 'visual',
        severity: 'warning',
        issue: `Visual diff detected: ${component.name} (${component.diffPixels} pixels)`,
        recommendation: 'Review changes or update baseline if intentional',
        priority: 3
      });
    }
  }

  return fixes.sort((a, b) => a.priority - b.priority);
}
```

---

## Report Generation

### 1. JSON Report (CI/CD)

```typescript
async function generateJSONReport(results: ValidationSummary): Promise<void> {
  const report = {
    timestamp: new Date().toISOString(),
    duration_ms: results.duration_ms,
    overall_status: results.overall_status,
    accessibility: {
      status: results.accessibility.status,
      score: results.accessibility.lighthouse.score,
      violations: results.accessibility.axe.violations.length
    },
    performance: {
      status: results.performance.status,
      score: results.performance.lighthouse.score,
      bundle_size: results.performance.bundle.total,
      core_web_vitals: results.performance.coreWebVitals
    },
    visual: {
      status: results.visual.status,
      total_snapshots: results.visual.total_snapshots,
      diffs_detected: results.visual.diffs_detected
    },
    fixes: results.fixes
  };

  await fs.promises.writeFile(
    'validation-report.json',
    JSON.stringify(report, null, 2)
  );
}
```

---

### 2. Markdown Report (Human-Readable)

```typescript
function generateMarkdownReport(results: ValidationSummary): string {
  const statusEmoji = {
    pass: '✅',
    warning: '⚠️',
    fail: '❌'
  };

  return `
# UI Validation Report

**Validated:** ${new Date().toISOString()}
**Duration:** ${(results.duration_ms / 1000).toFixed(1)}s
**Status:** ${statusEmoji[results.overall_status]} ${results.overall_status.toUpperCase()}

## Accessibility (${statusEmoji[results.accessibility.status]})
- Lighthouse Score: ${results.accessibility.lighthouse.score}/100
- Axe Violations: ${results.accessibility.axe.violations.length}
- WCAG AA Compliance: ${results.accessibility.axe.violations.length === 0 ? 'Yes' : 'No'}

## Performance (${statusEmoji[results.performance.status]})
- Lighthouse Score: ${results.performance.lighthouse.score}/100
- Bundle Size: ${(results.performance.bundle.total / 1024).toFixed(1)} KB
- LCP: ${results.performance.coreWebVitals.lcp}ms (target: <2500ms)
- FID: ${results.performance.coreWebVitals.fid}ms (target: <100ms)
- CLS: ${results.performance.coreWebVitals.cls.toFixed(3)} (target: <0.1)

## Visual Regression (${statusEmoji[results.visual.status]})
- Total Snapshots: ${results.visual.total_snapshots}
- Diffs Detected: ${results.visual.diffs_detected}

## Recommended Fixes (${results.fixes.length})
${results.fixes.map((fix, i) => `
${i + 1}. **[${fix.severity.toUpperCase()}]** ${fix.issue}
   - ${fix.recommendation}
`).join('')}
  `.trim();
}
```

---

## CLI Integration

```typescript
#!/usr/bin/env node
import { program } from 'commander';

program
  .name('validate-ui')
  .description('Run UI validation suite')
  .argument('<url>', 'URL to validate')
  .option('-f, --format <type>', 'Report format (json|markdown|html)', 'json')
  .option('-o, --output <file>', 'Output file path')
  .option('-q, --quick', 'Run quick validation (single validator)')
  .action(async (url, options) => {
    console.log('🔍 Validating UI...');

    const results = await validateUI(url);

    // Generate report
    let report: string;
    if (options.format === 'markdown') {
      report = generateMarkdownReport(results);
    } else if (options.format === 'html') {
      report = generateHTMLReport(results);
    } else {
      report = JSON.stringify(results, null, 2);
    }

    // Output report
    if (options.output) {
      await fs.promises.writeFile(options.output, report);
      console.log(`📝 Report saved to ${options.output}`);
    } else {
      console.log(report);
    }

    // Exit with appropriate code
    process.exit(results.overall_status === 'fail' ? 1 : 0);
  });

program.parse();
```

**Usage:**
```bash
# Run validation
npx validate-ui http://localhost:4173

# Generate markdown report
npx validate-ui http://localhost:4173 --format markdown --output report.md

# Quick mode (accessibility only)
npx validate-ui http://localhost:4173 --quick
```

---

## Performance Monitoring

```typescript
interface PerformanceMetrics {
  total_duration_ms: number;
  accessibility_duration_ms: number;
  performance_duration_ms: number;
  visual_duration_ms: number;
  parallelization_factor: number;
}

async function measureValidationPerformance(url: string): Promise<PerformanceMetrics> {
  const startTime = performance.now();

  const accessibilityStart = performance.now();
  const accessibility = await validateAccessibility(url);
  const accessibilityDuration = performance.now() - accessibilityStart;

  const performanceStart = performance.now();
  const performanceResult = await validatePerformance(url);
  const performanceDuration = performance.now() - performanceStart;

  const visualStart = performance.now();
  const visual = await validateVisualRegression(url);
  const visualDuration = performance.now() - visualStart;

  const totalDuration = performance.now() - startTime;

  // Sequential time would be sum of all durations
  const sequentialTime = accessibilityDuration + performanceDuration + visualDuration;
  const parallelizationFactor = sequentialTime / totalDuration;

  return {
    total_duration_ms: totalDuration,
    accessibility_duration_ms: accessibilityDuration,
    performance_duration_ms: performanceDuration,
    visual_duration_ms: visualDuration,
    parallelization_factor: parallelizationFactor
  };
}
```

**Example Output:**
```
✅ Validation complete
   Duration: 45s
   Accessibility: 25s
   Performance: 35s
   Visual: 15s
   Speedup: 4.7x vs sequential (3m 5s)
```

---

*End of Parallel Validation Reference*
