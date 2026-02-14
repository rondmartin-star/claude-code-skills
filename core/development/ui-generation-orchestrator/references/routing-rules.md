# UI Generation Orchestrator: Routing Rules

**Version:** 1.0.0
**Purpose:** Detailed complexity assessment and routing decision logic

---

## Complexity Indicators (4 Dimensions)

### 1. Component Count

| Range | Weight | Classification |
|-------|--------|----------------|
| 1-5 | 1-5 | Trivial |
| 6-10 | 6-10 | Simple |
| 11-30 | 11-30 | Medium |
| 31+ | 31+ | Complex |

### 2. Design System Complexity

| State | Weight | Description |
|-------|--------|-------------|
| None | 0 | No design tokens, using defaults |
| Basic | 5 | Colors and typography only |
| Intermediate | 10 | Colors, typography, spacing |
| Full | 15 | Complete system (colors, typography, spacing, shadows, borders, breakpoints) |

### 3. Page Complexity

| Pages | Weight | Description |
|-------|--------|-------------|
| 1 | 0 | Single page/view |
| 2-5 | 5 | Multiple related pages |
| 6+ | 10 | Complex multi-page application |

### 4. Custom Component Complexity

| Custom Components | Weight | Description |
|-------------------|--------|-------------|
| 0 | 0 | Using template library only |
| 1-3 | 3 | Few custom components |
| 4-10 | 7 | Moderate customization |
| 11+ | 12 | Heavy customization |

---

## Complexity Calculation

```javascript
function assessComplexity(request) {
  // Extract indicators
  const componentCount = request.components?.length || 0;
  const designSystemState = assessDesignSystem(request);
  const pageCount = request.pages?.length || 0;
  const customCount = countCustomComponents(request);

  // Calculate weights
  let score = componentCount;

  if (designSystemState === 'none') score += 0;
  else if (designSystemState === 'basic') score += 5;
  else if (designSystemState === 'intermediate') score += 10;
  else score += 15; // full

  if (pageCount === 1) score += 0;
  else if (pageCount <= 5) score += 5;
  else score += 10;

  if (customCount === 0) score += 0;
  else if (customCount <= 3) score += 3;
  else if (customCount <= 10) score += 7;
  else score += 12;

  // Classify
  if (score <= 5 || componentCount <= 5) return 'trivial';
  if (score <= 15 || componentCount <= 10) return 'simple';
  if (score <= 40 || componentCount <= 30) return 'medium';
  return 'complex';
}

function assessDesignSystem(request) {
  const config = request.config?.design_system;
  if (!config) return 'none';

  const hasColors = config.colors && Object.keys(config.colors).length > 0;
  const hasTypography = config.typography && Object.keys(config.typography).length > 0;
  const hasSpacing = config.spacing && config.spacing.scale;
  const hasShadows = config.shadows;
  const hasBorders = config.borderRadius;

  const count = [hasColors, hasTypography, hasSpacing, hasShadows, hasBorders]
    .filter(Boolean).length;

  if (count === 0) return 'none';
  if (count <= 2) return 'basic';
  if (count <= 3) return 'intermediate';
  return 'full';
}

function countCustomComponents(request) {
  if (!request.components) return 0;

  const templateComponents = [
    'Button', 'Input', 'Select', 'Checkbox', 'Radio', 'Toggle',
    'Card', 'Table', 'List', 'Badge', 'Avatar',
    'Modal', 'Alert', 'Toast', 'Tooltip',
    'Navbar', 'Sidebar', 'Tabs', 'Pagination'
  ];

  return request.components.filter(comp =>
    !templateComponents.includes(comp.name)
  ).length;
}
```

---

## Routing Decision Matrix

| Complexity | Strategy | Skill Loading | Parallelization | Monitoring |
|-----------|----------|---------------|-----------------|------------|
| **Trivial** | Direct | svelte-component-generator only | None | None |
| **Simple** | Sequential | svelte-component-generator only | None | None |
| **Medium** | Parallel Batch | svelte-component-generator + design-system-manager | 5 concurrent | Basic |
| **Complex** | Battle-Plan | ui-battle-plan → all skills | Dependency-aware | Full (verify-evidence, detect-infinite-loop, manage-context) |

---

## Routing Examples

### Example 1: Trivial (Score = 3)

**Request:**
```
"Generate a Button component"
```

**Analysis:**
- Component count: 1 (weight: 1)
- Design system: None (weight: 0)
- Pages: 1 (weight: 0)
- Custom: 0 (weight: 0)
- **Total Score: 1**

**Routing:** Trivial → Direct to svelte-component-generator

**Execution:**
```
Load: svelte-component-generator
Generate: Button.svelte
Validate: Type check only
Total time: ~3 minutes
```

---

### Example 2: Simple (Score = 12)

**Request:**
```
"Generate login form with email, password, and submit button"
```

**Analysis:**
- Component count: 3 (Button, Input, Input) (weight: 3)
- Design system: Basic (colors only) (weight: 5)
- Pages: 1 (LoginPage) (weight: 0)
- Custom: 1 (LoginForm) (weight: 3)
- **Total Score: 11**

**Routing:** Simple → Sequential generation

**Execution:**
```
Load: svelte-component-generator
Generate sequentially:
  1. Input.svelte (email)
  2. Input.svelte (password)
  3. Button.svelte (submit)
  4. LoginForm.svelte (composition)
Validate: Type check + accessibility
Total time: ~12 minutes
```

---

### Example 3: Medium (Score = 28)

**Request:**
```
"Generate complete venue management UI with list, detail, and form pages"
```

**Analysis:**
- Component count: 15 (weight: 15)
  - VenueCard, VenueList, VenueDetail, VenueForm
  - Button, Input, Select, Checkbox (×4)
  - Card, Table, Modal
- Design system: Intermediate (colors, typography, spacing) (weight: 10)
- Pages: 3 (List, Detail, Form) (weight: 5)
- Custom: 4 (VenueCard, VenueList, VenueDetail, VenueForm) (weight: 7)
- **Total Score: 37**

**Routing:** Medium → Parallel batch (5 concurrent)

**Execution:**
```
Load: svelte-component-generator + design-system-manager

Phase 1: Design tokens
  - Generate tailwind.config.js from design_system

Phase 2: Parallel component generation
  Level 1 (5 parallel): Button, Input, Select, Checkbox, Card
  Level 2 (3 parallel): Table, Modal, VenueCard
  Level 3 (2 parallel): VenueList, VenueDetail
  Level 4 (1 sequential): VenueForm

Phase 3: Validation
  - Accessibility audit
  - Token usage validation
  - Visual regression baselines

Total time: ~20 minutes (vs 45 minutes sequential)
Speedup: 2.25x
```

---

### Example 4: Complex (Score = 58)

**Request:**
```
"Generate complete application UI with authentication, venue management,
booking system, reporting, and admin dashboard"
```

**Analysis:**
- Component count: 40 (weight: 40)
- Design system: Full (all tokens) (weight: 15)
- Pages: 12 (weight: 10)
- Custom: 15 (weight: 12)
- **Total Score: 77**

**Routing:** Complex → Battle-plan coordination

**Execution:**
```
Load: ui-battle-plan

Phase 1: CLARIFY-REQUIREMENTS (clarify-requirements)
  - Confirm all pages needed
  - Verify design system completeness
  - Identify dependencies

Phase 2-3: PATTERN-LIBRARY + PRE-MORTEM (parallel)
  - Check for similar UI patterns
  - Anticipate component conflicts
  - Plan for accessibility issues

Phase 4: CONFIRM-OPERATION
  - User approves generation plan

Phase 5: EXECUTE (with monitoring)
  Load: svelte-component-generator + design-system-manager

  Design tokens setup
  Dependency graph with 7 levels
  Parallel generation (5 concurrent per level)

  Monitoring:
    - verify-evidence: Components match design
    - detect-infinite-loop: Stuck in refinement?
    - manage-context: Chunk large operations

Phase 6: ERROR-REFLECTION (if issues)
  - Analyze generation failures
  - Propose alternatives

Phase 7: DECLARE-COMPLETE
  - 40 components generated
  - All tests passing

Phase 8: PATTERN-UPDATE
  - Save successful patterns

Total time: ~2 hours (vs 5+ hours sequential/manual)
Speedup: 2.5x + quality improvement
```

---

## Special Cases

### Case 1: Design Specs Available

**Detection:**
```
User has completed windows-app-ui-design phase
Design specs exist in docs/design/
```

**Routing:**
```
Load: design-system-manager first
  → Extract tokens from design specs
  → Generate corpus-config.json design_system section

Then: ui-generation-orchestrator
  → Assess complexity with design system context
  → Route to svelte-component-generator
```

### Case 2: Migration from Jinja2

**Detection:**
```
templates/ directory exists with .html files
User mentions "migrate" or "convert"
```

**Routing:**
```
Load: ui-migration-manager
  → Assess existing templates
  → Convert Bootstrap → Tailwind
  → Convert Jinja2 → Svelte
  → Validate parity

NOT: ui-generation-orchestrator (different workflow)
```

### Case 3: Only Design System Needed

**Detection:**
```
User says "set up design tokens" or "create Tailwind config"
No component generation mentioned
```

**Routing:**
```
Direct to: design-system-manager
Skip: ui-generation-orchestrator (no components to generate)
```

### Case 4: Validation Only

**Detection:**
```
Components already exist
User wants to validate accessibility/performance
```

**Routing:**
```
Direct to: ui-validation-suite
Skip: ui-generation-orchestrator (no generation needed)
```

---

## Multi-Skill Coordination

### When to Load Multiple Skills in Parallel

**Scenario 1: Design System + Component Generation**
```
User: "Set up design system and generate initial components"

Load in parallel:
  - design-system-manager (generate tokens + Tailwind config)
  - svelte-component-generator (wait for tokens, then generate)

Dependencies: Component generation waits for design system completion
```

**Scenario 2: Generation + Validation**
```
User: "Generate components and validate accessibility"

Sequential:
  1. svelte-component-generator (generate all components)
  2. ui-validation-suite (validate after generation complete)

NOT parallel: Validation requires components to exist
```

---

## Performance Metrics

### Expected Timing by Complexity

| Complexity | Components | Sequential Time | Parallel Time | Speedup |
|-----------|-----------|-----------------|---------------|---------|
| Trivial | 1-5 | 3-15 min | 3-15 min | 1x |
| Simple | 5-10 | 15-30 min | 15-30 min | 1x |
| Medium | 10-30 | 30-90 min | 12-35 min | 2.5x |
| Complex | 30+ | 90-300 min | 30-120 min | 3x |

### Parallel Efficiency

```
Speedup = Sequential Time / Parallel Time

Amdahl's Law applies:
- Dependency-free components: Near-linear speedup
- Dependencies present: Reduced speedup
- Same-file conflicts: Sequential execution required

Practical speedups:
- 5 concurrent (medium): 2-2.5x
- 10 concurrent (complex): 2.5-3.5x
- Diminishing returns beyond 10 concurrent
```

---

## Error Handling

### Routing Errors

**Problem:** Can't determine complexity

**Solution:**
```
Ask user:
  - How many components?
  - Do you have design tokens?
  - How many pages?

Default to: Simple (safe choice)
```

**Problem:** Multiple routing options

**Solution:**
```
Prefer simplest that works:
  Trivial > Simple > Medium > Complex

Don't over-engineer for edge cases
```

**Problem:** Missing dependencies

**Solution:**
```
Check for:
  - Design specs (windows-app-ui-design output)
  - Design tokens (design_system config)
  - Component dependencies (parent components)

If missing: Load prerequisite skill first
```

---

*End of Routing Rules Reference*
