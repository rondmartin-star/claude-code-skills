---
name: svelte-component-generator
description: >
  Generate professional Svelte 5 components with TypeScript, Tailwind CSS, and WCAG AA
  accessibility. Three generation modes: requirements (AI-powered), design specs (guided),
  or templates (instant). Includes dependency graph system for parallel generation of
  multiple components. Triggers on: component generation requests, UI implementation.
---

# Svelte Component Generator

**Purpose:** Generate production-ready Svelte components with accessibility by default
**Size:** ~12 KB (intentionally minimal)
**Action:** Detect mode → Generate → Validate → Test

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Generate Svelte components"
- "Create Button component"
- "Build the login form"
- "Implement the design"
- "Generate components from design specs"
- "Create component library"

**Context Indicators:**
- User has design specs ready
- User mentions specific component names
- User wants to implement UI
- Request for Svelte/TypeScript/Tailwind components

## ❌ DO NOT LOAD WHEN

- Just designing UI specs (use windows-app-ui-design)
- Testing existing UI (use windows-app-ui-testing)
- No design specs available yet
- User wants requirements or data model
- Setting up design system (use design-system-manager)

---

## How This Works

```
┌─────────────────────────────────────────────────────────────────────┐
│  USER REQUEST: "Generate Button and Input components"               │
│       │                                                              │
│       ▼                                                              │
│  ┌─────────────────┐                                                │
│  │ Detect Mode     │                                                │
│  │ • Requirements  │ ◄── User provides requirements in natural lang │
│  │ • Design Specs  │ ◄── User has design doc ready                  │
│  │ • Templates     │ ◄── User requests standard component           │
│  └────────┬────────┘                                                │
│           │                                                          │
│           ▼                                                          │
│  ┌─────────────────┐     ┌─────────────────┐                       │
│  │ Build Dependency│────►│ Topological Sort│                       │
│  │ Graph           │     │ into Levels     │                       │
│  └─────────────────┘     └────────┬────────┘                       │
│                                   │                                  │
│                                   ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐        │
│  │ Generate Each Level in Parallel                         │        │
│  │  Level 1: [Button, Input, Select]      (3 concurrent)   │        │
│  │  Level 2: [Form]                        (depends on L1) │        │
│  │  Level 3: [LoginPage, RegisterPage]     (2 concurrent)  │        │
│  └─────────────────────────────────────────────────────────┘        │
│                                   │                                  │
│                                   ▼                                  │
│  ┌─────────────────┐     ┌─────────────────┐                       │
│  │ Validate Output │────►│ Run Tests       │                       │
│  │ • TypeScript    │     │ • Component     │                       │
│  │ • Accessibility │     │ • Accessibility │                       │
│  │ • Design Tokens │     │ • Visual        │                       │
│  └─────────────────┘     └─────────────────┘                       │
│                                                                      │
│  PERFORMANCE: 10 components in 6 min (vs 30 min sequential)        │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Three Generation Modes

| Mode | When | Process | Speed |
|------|------|---------|-------|
| **Requirements** | Natural language specs | AI-powered generation | 3-5 min |
| **Design Specs** | Design doc ready | Token-mapped generation | 1-2 min |
| **Templates** | Standard components | Template + customization | 30 sec |

**Examples:**
- Requirements: "Create a login form with email and password"
- Design Specs: Load from YAML/JSON design document
- Templates: "Create a standard Button component"

**See `references/component-templates.md` for 20+ available templates**

---

## Dependency Graph System

**Purpose:** Generate multiple components in parallel while respecting dependencies

### Building the Graph

```typescript
// Auto-detect dependencies from:
// 1. Import statements in design specs
// 2. Component composition in requirements
// 3. Explicit dependency declarations

const graph = {
  'Button': [],                          // No dependencies
  'Input': [],                           // No dependencies
  'Select': [],                          // No dependencies
  'Form': ['Button', 'Input', 'Select'], // Depends on form controls
  'Card': [],                            // No dependencies
  'LoginPage': ['Form', 'Card'],         // Depends on Form and Card
};
```

### Topological Sort

```typescript
// Sort into levels for parallel execution
const levels = [
  ['Button', 'Input', 'Select', 'Card'],  // L1: No deps (4 parallel)
  ['Form'],                                // L2: Depends on L1
  ['LoginPage']                            // L3: Depends on L2
];
```

### Parallel Generation

```typescript
for (const level of levels) {
  console.log(`→ Generating ${level.length} components in parallel...`);

  // Generate all components in this level concurrently
  await Promise.all(
    level.map(component => generateComponent(component))
  );
}

// Performance:
// Sequential: 6 components × 3min = 18min
// Parallel: L1 (4 parallel) 3min + L2 (1) 3min + L3 (1) 3min = 9min
// Speedup: 2x
```

**See `references/parallel-coordination.md` for complete patterns**

---

## Component Structure

**Standard Pattern:**
1. TypeScript interface for props
2. Props with defaults using $props()
3. State management with $state()
4. Computed values with $derived()
5. Event handlers with type safety
6. Template with WCAG AA attributes
7. Minimal scoped styles (prefer Tailwind)

**Key Features:**
- ✅ TypeScript types | ✅ WCAG AA accessibility | ✅ Tailwind utilities
- ✅ Svelte 5 runes | ✅ Event handlers | ✅ JSDoc comments

**See `references/svelte-patterns.md` for complete component structure examples**

---

## Design Token Integration

**Process:**
1. Load design tokens from corpus-config.json
2. Map tokens to Tailwind CSS classes
3. Validate required tokens exist
4. Fall back to defaults if missing

**Token Sources:**
- `config.design_system.tokens.colors` → bg-*, text-*, border-*
- `config.design_system.tokens.spacing` → p-*, m-*, gap-*
- `config.design_system.tokens.typography` → text-*, font-*

**See `references/tailwind-integration.md` for complete token mapping**

---

## Accessibility (WCAG AA by Default)

**Required for all components:**
1. ✅ Semantic HTML (button, input, nav not div)
2. ✅ ARIA attributes (aria-label, aria-disabled, role)
3. ✅ Keyboard navigation (Tab, Enter, Space)
4. ✅ Focus management (focus-visible styles)
5. ✅ Color contrast (4.5:1 minimum for text)

**See `references/accessibility-guide.md` for complete WCAG AA patterns**

---

## File Organization

```
src/
├── lib/
│   └── components/
│       ├── forms/
│       │   ├── Button.svelte           # Generated component
│       │   ├── Input.svelte
│       │   ├── Select.svelte
│       │   └── Form.svelte
│       ├── layout/
│       │   ├── Card.svelte
│       │   ├── Container.svelte
│       │   └── Grid.svelte
│       ├── navigation/
│       │   ├── Navbar.svelte
│       │   └── Sidebar.svelte
│       └── index.ts                    # Auto-generated exports
├── routes/
│   ├── login/
│   │   └── +page.svelte                # Page using components
│   └── dashboard/
│       └── +page.svelte
└── app.css                             # Tailwind imports
```

**Auto-generated index.ts:**
```typescript
// Auto-generated by svelte-component-generator
export { default as Button } from './forms/Button.svelte';
export { default as Input } from './forms/Input.svelte';
export { default as Card } from './layout/Card.svelte';
// ... etc
```

---

## Validation & Testing

### Type Validation
```bash
# Ensure TypeScript compilation succeeds
tsc --noEmit
```

### Accessibility Validation
```typescript
// Auto-run Axe-core on generated components
import { axe } from 'axe-core';

const results = await axe.run(component);
if (results.violations.length > 0) {
  console.error('Accessibility violations:', results.violations);
}
```

### Component Tests
```typescript
// Auto-generate basic tests for each component
import { render } from '@testing-library/svelte';
import Button from './Button.svelte';

test('Button renders with props', () => {
  const { getByRole } = render(Button, {
    props: { variant: 'primary' }
  });
  expect(getByRole('button')).toBeInTheDocument();
});
```

---

## Performance Optimization

### Parallel Generation Benchmarks

| Components | Sequential | Parallel | Speedup |
|-----------|-----------|----------|---------|
| 5 simple | 15 min | 3 min | 5x |
| 10 medium | 30 min | 6 min | 5x |
| 20 complex | 60 min | 12 min | 5x |

**Key to Performance:**
1. Dependency graph prevents blocking
2. Concurrent generation within each level
3. Template mode for standard components
4. Batch token validation (not per-component)

---

## Commands for Claude

When processing component generation request:

```
1. READ corpus-config.json for design tokens
2. DETECT generation mode (requirements/specs/templates)
3. BUILD dependency graph if multiple components
4. GENERATE components level-by-level (parallel within level)
5. VALIDATE TypeScript types and accessibility
6. CREATE component tests
7. UPDATE index.ts exports
8. RECOMMEND next skill (ui-validation-suite if ready to test)
```

**Context Budget:**
- This skill: ~12 KB
- Component templates: Loaded on-demand from references/
- Working space: Remaining context
- Target: Generate 5-10 components per session

---

## Error Handling

| Error | Action |
|-------|--------|
| Missing design tokens | Warn + use defaults + suggest design-system-manager |
| Circular dependencies | Error + show cycle + request refactor |
| TypeScript errors | Show errors + auto-fix common issues |
| Invalid component name | Sanitize name + warn user |

---

## Integration with Ecosystem

### Called by ui-generation-orchestrator

```python
# Orchestrator routes to this skill
if complexity in ['trivial', 'simple']:
    load_skill("svelte-component-generator")
elif complexity == 'medium':
    load_skill("svelte-component-generator", mode="parallel")
```

### Calls to Related Skills

```python
# This skill may load:
load_skill("design-system-manager")  # If tokens not configured
load_skill("ui-validation-suite")    # After generation for validation
```

---

## References

**Complete guides:**
1. **svelte-patterns.md** - Svelte 5 patterns (runes, SSR, CSR)
2. **tailwind-integration.md** - Design token → Tailwind mapping
3. **component-templates.md** - 20+ reusable component templates
4. **accessibility-guide.md** - WCAG AA patterns and validation

**Related Skills:**
- `ui-generation-orchestrator` - Routes to this skill
- `design-system-manager` - Configure design tokens
- `ui-validation-suite` - Validate generated components
- `windows-app-ui-design` - Create design specs

---

*End of Svelte Component Generator Skill*
