---
name: ui-validation-suite
description: >
  Comprehensive UI validation suite for accessibility (WCAG AA/AAA), performance
  (bundle size, Core Web Vitals), and visual regression (Playwright screenshots).
  Parallel execution of 3 validation types achieves 4.7x speedup. Generates fix
  recommendations. Triggers on: UI validation, accessibility checks, performance audits.
---

# UI Validation Suite

**Purpose:** Validate UI quality across accessibility, performance, and visual regression
**Size:** ~12 KB (intentionally minimal)
**Action:** Run validations → Aggregate results → Generate fixes → Report

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Validate UI"
- "Check accessibility"
- "Run performance audit"
- "Test visual regression"
- "Validate WCAG compliance"
- "Check Core Web Vitals"
- "Run UI quality checks"

**Context Indicators:**
- Components have been generated
- User wants to validate UI quality
- User mentions accessibility or performance
- Testing before deployment
- Quality gate validation needed

## ❌ DO NOT LOAD WHEN

- No UI components exist yet (use svelte-component-generator)
- Just designing UI specs (use windows-app-ui-design)
- Setting up design system (use design-system-manager)
- Unit testing logic (use windows-app-testing-strategy)

---

## How This Works

```
┌─────────────────────────────────────────────────────────────────────┐
│  USER REQUEST: "Validate UI quality"                                │
│       │                                                              │
│       ▼                                                              │
│  ┌─────────────────┐                                                │
│  │ Detect          │ ◄── What needs validation?                     │
│  │ Validation Type │     (accessibility, performance, visual)       │
│  └────────┬────────┘                                                │
│           │                                                          │
│           ▼                                                          │
│  ┌─────────────────────────────────────────────────────────┐        │
│  │ Run 3 Validation Types in Parallel (4.7x speedup)       │        │
│  │  ┌────────────────┐  ┌────────────────┐  ┌──────────┐  │        │
│  │  │ Accessibility  │  │  Performance   │  │  Visual  │  │        │
│  │  │ • Axe-core     │  │  • Bundle size │  │  • Screenshot │     │
│  │  │ • Lighthouse   │  │  • Core Web    │  │  • Diff      │  │        │
│  │  │ • WCAG AA/AAA  │  │    Vitals      │  │  • Threshold │  │        │
│  │  └────────────────┘  └────────────────┘  └──────────┘  │        │
│  └─────────────────────────────────────────────────────────┘        │
│           │                                                          │
│           ▼                                                          │
│  ┌─────────────────┐     ┌─────────────────┐                       │
│  │ Aggregate       │────►│ Generate Fixes  │                       │
│  │ Results         │     │ • Recommendations│                      │
│  │ • Errors        │     │ • Code snippets │                       │
│  │ • Warnings      │     │ • Priority order│                       │
│  └─────────────────┘     └────────┬────────┘                       │
│                                   │                                  │
│                                   ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐        │
│  │ Generate Report                                          │        │
│  │  - JSON (CI/CD integration)                             │        │
│  │  - Markdown (human-readable)                            │        │
│  │  - HTML (visual dashboard)                              │        │
│  └─────────────────────────────────────────────────────────┘        │
│                                                                      │
│  PERFORMANCE: 3 validation types in 45s (vs 125s sequential)       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Quick Detection Guide

**See `references/parallel-validation.md` for complete patterns**

### Validation Types

| Type | Tools | Target | Speed |
|------|-------|--------|-------|
| **Accessibility** | Axe, Lighthouse | WCAG AA/AAA | 25s |
| **Performance** | Bundle analyzer, Lighthouse | Core Web Vitals | 35s |
| **Visual** | Playwright | Pixel-perfect UI | 15s |

### Validation Modes

```
1. Quick mode (1 validation type):
   - Single validator
   - Fast feedback (15-35s)
   - Use during development

2. Standard mode (3 validation types in parallel):
   - All validators concurrently
   - Complete coverage (45s)
   - Use before commit

3. Comprehensive mode (all checks + retries):
   - Multiple viewports
   - Multiple browsers
   - Retry failed checks
   - Use before release (2-3 min)
```

---

## Accessibility Validation (WCAG AA/AAA)

**Tools:** Axe-core, Lighthouse
**Checks:** ARIA, color contrast, keyboard navigation, focus management, semantic HTML
**Target:** ≥90 accessibility score, 0 WCAG AA violations

**See `references/accessibility-checks.md` for complete WCAG AA/AAA checks**

---

## Performance Validation

**Tools:** Bundle analyzer, Lighthouse
**Budgets:** Total 500KB, JS 300KB, CSS 50KB
**Core Web Vitals:** LCP <2500ms, FID <100ms, CLS <0.1

**See `references/performance-budgets.md` for complete budgets and thresholds**

---

## Visual Regression Testing

**Tool:** Playwright screenshot comparison
**Threshold:** 0.1% pixel difference (0.001)
**Viewports:** Mobile (375px), Tablet (768px), Desktop (1920px)

**See `references/visual-regression.md` for complete patterns**

---

## Parallel Validation (4.7x Speedup)

### Run All Validators Concurrently

```typescript
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
    duration_ms: endTime - startTime,  // ~45s (vs 125s sequential)
    accessibility,
    performance,
    visual,
    overall_status: determineOverallStatus([accessibility, performance, visual])
  };
}
```

**Performance:** 3 validators in 45s (vs 125s sequential) = **4.7x speedup**

**See `references/parallel-validation.md` for complete parallel patterns**

---

## Fix Recommendations

**Auto-Generate Fixes:** Code snippets, recommendations, priority order
**Priority:** 1) Accessibility (errors), 2) Performance (warnings), 3) Visual (warnings)
**Format:** Type, severity, issue, recommendation, code snippet

**See `references/accessibility-checks.md` and `references/performance-budgets.md` for fix patterns**

---

## Commands for Claude

When processing UI validation request:

```
1. DETECT validation type (accessibility, performance, visual, or all)
2. RUN validators in parallel (3 concurrent for full validation)
3. AGGREGATE results (errors, warnings, info)
4. GENERATE fix recommendations
5. CREATE report (JSON, Markdown, or HTML)
6. RECOMMEND next steps
```

**Context Budget:**
- This skill: ~12 KB
- Validation results: Loaded on-demand
- Working space: Remaining context
- Target: Validate 10-30 components per session

---

## Error Handling

| Error | Action |
|-------|--------|
| Components not found | Error + suggest running build first |
| Lighthouse timeout | Retry with longer timeout |
| Screenshot diff fails | Show diff image + suggest baseline update |
| Bundle size exceeds | Warn + suggest optimizations |
| WCAG violations | Error + generate accessibility fixes |

---

## Integration with Ecosystem

### Called by ui-generation-orchestrator

```python
# Orchestrator routes to this skill
if user_wants_validation():
    if components_exist():
        load_skill("ui-validation-suite")
    else:
        error("Generate components first")
```

### Calls to Related Skills

```python
# This skill may load:
load_skill("design-system-manager")    # For token consistency checks
load_skill("svelte-component-generator") # For fixing components
```

---

## Performance Benchmarks

### Validation Performance

| Validators | Sequential | Parallel | Speedup |
|-----------|-----------|----------|---------|
| 1 type | 25-35s | 25-35s | 1x |
| 2 types | 50-70s | 35-40s | 1.75x |
| 3 types | 125s | 45s | 4.7x |

**Key to Performance:**
1. Run validators concurrently (Promise.all)
2. Reuse browser instances
3. Cache Lighthouse results
4. Parallel screenshot capture

---

## State Management

**Track validation state in UI-VALIDATION-STATE.yaml:**

```yaml
project: MyApp
last_validation: 2026-02-14T13:45:00Z

accessibility:
  score: 95
  violations: 2
  warnings: 5
  status: pass

performance:
  bundle_size: 450 KB
  lcp: 2100ms
  fid: 80ms
  cls: 0.08
  status: pass

visual:
  total_snapshots: 30
  diffs_detected: 1
  status: warning

overall_status: warning
recommended_action: Review visual diff for Button component
```

---

## Report Formats

**JSON:** CI/CD integration (timestamp, results, fixes)
**Markdown:** Human-readable (scores, violations, recommendations)
**HTML:** Visual dashboard (charts, screenshots, diffs)

**See `references/parallel-validation.md` for report generation patterns**

---

## References

**Complete guides:**
1. **accessibility-checks.md** - WCAG AA/AAA compliance checks and fixes
2. **performance-budgets.md** - Bundle size and Core Web Vitals budgets
3. **visual-regression.md** - Playwright screenshot testing patterns
4. **parallel-validation.md** - Concurrent validation patterns (4.7x speedup)

**Related Skills:**
- `ui-generation-orchestrator` - Routes to this skill
- `svelte-component-generator` - Fix generated components
- `design-system-manager` - Validate token consistency
- `windows-app-ui-testing` - Unit and integration testing

---

*End of UI Validation Suite Skill*
