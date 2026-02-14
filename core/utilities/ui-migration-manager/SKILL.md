---
name: ui-migration-manager
description: >
  Migrate existing UIs from Bootstrap/Jinja2 to Tailwind/Svelte with automated conversion,
  parity validation, and safe rollback. Handles pre-migration assessment, token mapping,
  template conversion, visual regression testing, and blue-green deployment. Triggers on:
  UI migration, framework modernization, template conversion.
---

# UI Migration Manager

**Purpose:** Safe, validated migration from legacy UI frameworks to modern stack
**Size:** ~11 KB (intentionally minimal)
**Action:** Assess → Convert → Validate → Deploy → Monitor

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Migrate UI to Svelte"
- "Convert from Bootstrap to Tailwind"
- "Modernize UI framework"
- "Migrate templates to Svelte"
- "Convert Jinja2 templates"
- "Plan UI migration"

**Context Indicators:**
- Existing Bootstrap + Jinja2 codebase
- User wants to modernize UI
- Migration planning needed
- Framework upgrade discussion

## ❌ DO NOT LOAD WHEN

- Building new UI from scratch (use svelte-component-generator)
- No existing UI to migrate
- Just validating current UI (use ui-validation-suite)
- Design system setup (use design-system-manager)

---

## How This Works

```
┌─────────────────────────────────────────────────────────────────────┐
│  USER REQUEST: "Migrate UI from Bootstrap/Jinja2 to Tailwind/Svelte"│
│       │                                                              │
│       ▼                                                              │
│  ┌─────────────────┐                                                │
│  │ Phase 1:        │ ◄── Analyze existing codebase                  │
│  │ Assessment      │     Count components, identify patterns        │
│  └────────┬────────┘                                                │
│           │                                                          │
│           ▼                                                          │
│  ┌─────────────────┐                                                │
│  │ Phase 2:        │ ◄── Bootstrap → Tailwind                       │
│  │ Token Conversion│     Map colors, spacing, typography            │
│  └────────┬────────┘                                                │
│           │                                                          │
│           ▼                                                          │
│  ┌─────────────────┐                                                │
│  │ Phase 3:        │ ◄── Jinja2 → Svelte                            │
│  │ Template Convert│     Convert syntax, props, logic               │
│  └────────┬────────┘                                                │
│           │                                                          │
│           ▼                                                          │
│  ┌─────────────────┐                                                │
│  │ Phase 4:        │ ◄── Visual + Functional testing                │
│  │ Parity Validation│    Screenshot comparison, E2E tests           │
│  └────────┬────────┘                                                │
│           │                                                          │
│           ▼                                                          │
│  ┌─────────────────┐     ┌─────────────────┐                       │
│  │ Phase 5:        │────►│ Rollback Ready  │                       │
│  │ Blue-Green      │     │ if Issues Found │                       │
│  │ Deployment      │     └─────────────────┘                       │
│  └─────────────────┘                                                │
│                                                                      │
│  SAFETY: Zero-downtime cutover with instant rollback capability    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Migration Phases

### Phase 1: Pre-Migration Assessment

**Objective:** Understand scope and identify risks

```typescript
interface AssessmentReport {
  components: {
    total: number;
    byType: Record<string, number>;
    complexity: 'low' | 'medium' | 'high';
  };
  dependencies: {
    bootstrap_version: string;
    jinja2_version: string;
    custom_components: number;
  };
  risks: Risk[];
  estimated_effort: string;
  recommended_approach: 'big-bang' | 'incremental' | 'parallel';
}
```

**See `references/bootstrap-to-tailwind.md` for component inventory**

---

### Phase 2: Token Conversion (Bootstrap → Tailwind)

**Objective:** Map design tokens to preserve visual consistency

```typescript
interface TokenMapping {
  colors: Record<string, string>;      // primary → colors.primary.500
  spacing: Record<string, string>;     // p-3 → p-4
  typography: Record<string, string>;  // h1 → text-4xl
  breakpoints: Record<string, string>; // sm → sm:
}
```

**Common Mappings:**
- Bootstrap `primary` → Tailwind `colors.primary.500`
- Bootstrap `p-3` (1rem) → Tailwind `p-4` (1rem)
- Bootstrap `h1` → Tailwind `text-4xl font-bold`

**See `references/bootstrap-to-tailwind.md` for complete mapping**

---

### Phase 3: Template Conversion (Jinja2 → Svelte)

**Objective:** Convert template syntax while preserving logic

**Conversion Patterns:**

| Jinja2 | Svelte |
|--------|--------|
| `{{ variable }}` | `{variable}` |
| `{% if condition %}` | `{#if condition}` |
| `{% for item in items %}` | `{#each items as item}` |
| `{% block content %}` | `<slot name="content">` |

**See `references/jinja2-to-svelte.md` for complete conversion guide**

---

### Phase 4: Parity Validation

**Objective:** Ensure migrated UI matches original

**Validation Types:**

1. **Visual Parity** (Playwright screenshot comparison)
   - Capture baseline screenshots of original UI
   - Compare new UI screenshots pixel-by-pixel
   - Threshold: <0.5% difference allowed

2. **Functional Parity** (E2E testing)
   - All user flows work identically
   - Forms submit correctly
   - Navigation works
   - Data displays correctly

3. **Performance Parity**
   - Bundle size ≤ original (target: 30% smaller)
   - LCP ≤ original (target: 20% faster)
   - Lighthouse score ≥ original

**See `references/parity-validation.md` for validation strategies**

---

### Phase 5: Blue-Green Deployment

**Objective:** Zero-downtime cutover with instant rollback

**Strategy:**

```
1. Deploy new UI (Svelte) to "green" environment
2. Route 5% traffic to green (canary)
3. Monitor metrics (errors, performance, user satisfaction)
4. If successful: Gradually increase to 100%
5. If issues: Instant rollback to "blue" (original)
```

**See `references/rollback-strategy.md` for deployment patterns**

---

## Migration Approaches

### Approach 1: Big Bang (Fast, Risky)

**Timeline:** 1-2 weeks
**Risk:** High
**Use When:** Small codebase (<20 components)

```
Week 1: Convert all components
Week 2: Validate + deploy
```

---

### Approach 2: Incremental (Moderate, Safer)

**Timeline:** 4-8 weeks
**Risk:** Medium
**Use When:** Medium codebase (20-50 components)

```
Week 1-2: Critical pages (login, dashboard)
Week 3-4: Secondary pages
Week 5-6: Admin pages
Week 7-8: Validation + full cutover
```

---

### Approach 3: Parallel (Slow, Safest)

**Timeline:** 8-12 weeks
**Risk:** Low
**Use When:** Large codebase (50+ components)

```
Weeks 1-8: Build new UI alongside old
Weeks 9-10: Feature parity validation
Weeks 11-12: Gradual traffic migration
```

---

## Automated Conversion Tools

### Bootstrap Class Converter

```typescript
function convertBootstrapToTailwind(html: string): string {
  const classMap = {
    'container': 'container mx-auto px-4',
    'row': 'flex flex-wrap -mx-4',
    'col-md-6': 'md:w-1/2 px-4',
    'btn btn-primary': 'px-4 py-2 bg-primary-500 text-white rounded hover:bg-primary-600',
    'form-control': 'w-full px-3 py-2 border border-gray-300 rounded',
    // ... 100+ mappings
  };

  let converted = html;
  for (const [bootstrap, tailwind] of Object.entries(classMap)) {
    converted = converted.replace(new RegExp(`class="${bootstrap}"`, 'g'), `class="${tailwind}"`);
  }

  return converted;
}
```

**See `references/bootstrap-to-tailwind.md` for complete class mappings**

---

### Jinja2 Template Converter

```typescript
function convertJinja2ToSvelte(template: string): string {
  let svelte = template;

  // Variables
  svelte = svelte.replace(/\{\{\s*(\w+)\s*\}\}/g, '{$1}');

  // If statements
  svelte = svelte.replace(/\{%\s*if\s+(.+?)\s*%\}/g, '{#if $1}');
  svelte = svelte.replace(/\{%\s*endif\s*%\}/g, '{/if}');

  // For loops
  svelte = svelte.replace(/\{%\s*for\s+(\w+)\s+in\s+(\w+)\s*%\}/g, '{#each $2 as $1}');
  svelte = svelte.replace(/\{%\s*endfor\s*%\}/g, '{/each}');

  // Blocks → Slots
  svelte = svelte.replace(/\{%\s*block\s+(\w+)\s*%\}/g, '<slot name="$1">');
  svelte = svelte.replace(/\{%\s*endblock\s*%\}/g, '</slot>');

  return svelte;
}
```

**See `references/jinja2-to-svelte.md` for complete conversion patterns**

---

## Parity Testing

### Visual Regression Test

```typescript
import { test, expect } from '@playwright/test';

test('Homepage visual parity', async ({ page }) => {
  // Capture original (Jinja2 + Bootstrap)
  await page.goto('http://localhost:5000/');
  const original = await page.screenshot();

  // Capture new (Svelte + Tailwind)
  await page.goto('http://localhost:4173/');
  const migrated = await page.screenshot();

  // Compare
  expect(migrated).toMatchSnapshot(original, {
    threshold: 0.005 // 0.5% difference allowed
  });
});
```

---

### Functional Parity Test

```typescript
test('Login flow parity', async ({ page }) => {
  await page.goto('http://localhost:4173/login');

  // Same user flow as original
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'password123');
  await page.click('button[type="submit"]');

  // Same outcome as original
  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('h1')).toContainText('Dashboard');
});
```

---

## Rollback Strategy

### Blue-Green Setup

```nginx
# Blue (original): port 5000
upstream blue {
  server localhost:5000;
}

# Green (new): port 4173
upstream green {
  server localhost:4173;
}

# Traffic split (configurable)
server {
  listen 80;

  location / {
    # Route traffic based on cookie or percentage
    if ($cookie_ui_version = "new") {
      proxy_pass http://green;
    }
    proxy_pass http://blue; # Default to original
  }
}
```

### Instant Rollback

```bash
# If issues detected, instant rollback
curl -X POST http://admin/rollback
# → All traffic back to blue (original) immediately
```

**See `references/rollback-strategy.md` for deployment automation**

---

## Commands for Claude

When processing migration request:

```
1. READ existing codebase (Bootstrap + Jinja2 files)
2. ASSESS scope and complexity
3. RECOMMEND migration approach (big-bang vs incremental vs parallel)
4. CONVERT tokens (Bootstrap → Tailwind)
5. CONVERT templates (Jinja2 → Svelte)
6. VALIDATE parity (visual + functional)
7. DEPLOY with blue-green strategy
8. MONITOR and rollback if needed
```

**Context Budget:**
- This skill: ~11 KB
- Conversion tools: Loaded on-demand from references/
- Working space: Remaining context
- Target: Migrate 10-20 components per session

---

## Error Handling

| Error | Action |
|-------|--------|
| Component not found | Warn + skip |
| Conversion fails | Manual review + fallback |
| Parity test fails | Show diff + block deployment |
| Deployment error | Instant rollback to original |

---

## Integration with Ecosystem

### Called by ui-generation-orchestrator

```python
# Orchestrator routes to this skill
if user_wants_migration():
    if has_legacy_ui():
        load_skill("ui-migration-manager")
    else:
        error("No legacy UI to migrate")
```

### Calls to Related Skills

```python
# This skill may load:
load_skill("design-system-manager")    # For token setup
load_skill("svelte-component-generator") # For new components
load_skill("ui-validation-suite")      # For parity validation
```

---

## Performance Expectations

### Conversion Speed

| Components | Manual | Automated | Speedup |
|-----------|--------|-----------|---------|
| 10 | 20 hours | 2 hours | 10x |
| 50 | 100 hours | 10 hours | 10x |
| 100 | 200 hours | 20 hours | 10x |

**Key Insight:** Automated conversion handles 90% of work, 10% requires manual review

---

## Success Metrics

**Visual Parity:** ≥99.5% pixel match
**Functional Parity:** 100% user flows work
**Performance:** ≥20% improvement in LCP, ≥30% smaller bundle
**Zero Downtime:** <1 second rollback time
**User Satisfaction:** ≥95% positive feedback

---

## References

**Complete guides:**
1. **bootstrap-to-tailwind.md** - Complete class mapping and token conversion
2. **jinja2-to-svelte.md** - Template syntax conversion patterns
3. **parity-validation.md** - Visual and functional testing strategies
4. **rollback-strategy.md** - Blue-green deployment and safe rollback

**Related Skills:**
- `ui-generation-orchestrator` - Routes to this skill
- `svelte-component-generator` - Generates new components
- `design-system-manager` - Manages design tokens
- `ui-validation-suite` - Validates migrated UI

---

*End of UI Migration Manager Skill*
