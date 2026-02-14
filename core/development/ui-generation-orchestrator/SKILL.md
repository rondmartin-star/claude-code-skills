---
name: ui-generation-orchestrator
description: >
  Coordinate UI generation operations by routing to specialized skills based on complexity.
  Lightweight orchestrator that determines whether to use svelte-component-generator directly
  or coordinate complex multi-component generation with parallelization. Triggers on: UI
  generation requests, component creation, design system implementation.
---

# UI Generation Orchestrator

**Purpose:** Coordinate UI generation to minimize context usage and maximize efficiency
**Size:** ~8 KB (intentionally minimal)
**Action:** Detect complexity → Load only needed skill(s) → Generate → Validate

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Generate UI components"
- "Create Svelte components"
- "Build the UI"
- "Implement the design system"
- "Generate components from design"
- "Create component library"

**Context Indicators:**
- User mentions UI generation
- User has design specs ready
- User wants to implement UI
- Discussion about components or design system

## ❌ DO NOT LOAD WHEN

- Just designing UI specs (use windows-app-ui-design)
- Testing existing UI (use windows-app-ui-testing)
- No design specs available yet
- User wants requirements or system design

---

## How This Works

```
┌─────────────────────────────────────────────────────────────────────┐
│  USER REQUEST: "Generate UI components"                             │
│       │                                                              │
│       ▼                                                              │
│  ┌─────────────────┐                                                │
│  │  ORCHESTRATOR   │ ◄── Always loaded first (~8KB)                 │
│  │  (this skill)   │                                                │
│  └────────┬────────┘                                                │
│           │                                                          │
│           ▼                                                          │
│  ┌─────────────────┐     ┌─────────────────┐                       │
│  │ Assess          │────►│ Load ONLY the   │                       │
│  │ Complexity      │     │ skill(s) needed │                       │
│  │                 │     │ for this request│                       │
│  └─────────────────┘     └─────────────────┘                       │
│                                   │                                  │
│           ┌───────────────────────┼───────────────────────┐         │
│           ▼                       ▼                       ▼         │
│  ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐   │
│  │  DIRECT         │   │  PARALLEL       │   │  BATTLE-PLAN    │   │
│  │  (1-5 comps)    │   │  (5-30 comps)   │   │  (30+ comps)    │   │
│  └─────────────────┘   └─────────────────┘   └─────────────────┘   │
│                                                                      │
│  TOTAL CONTEXT: Orchestrator + 1 skill = 8-20 KB                   │
│  vs. Loading everything = 50+ KB                                    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Quick Detection Guide

**See `references/routing-rules.md` for complete detection rules**

### Complexity Assessment

| Indicators | Complexity | Strategy |
|------------|-----------|----------|
| 1-5 components, no design system | **Trivial** | Direct generation |
| 5-10 components, basic tokens | **Simple** | Sequential generation |
| 10-30 components, design system | **Medium** | Parallel batching (5 concurrent) |
| 30+ components, full system | **Complex** | Battle-plan coordination |

### Routing Decision Tree

```
1. Load corpus-config.json from project root
2. Check for ui.framework configuration
3. Count components to generate
4. Assess design system complexity
5. Determine routing:
   ├─ Trivial/Simple → svelte-component-generator (direct)
   ├─ Medium → svelte-component-generator (parallel batch)
   └─ Complex → ui-battle-plan → svelte-component-generator

6. If parallel execution needed:
   → Build dependency graph
   → Topological sort into levels
   → Generate each level concurrently

7. If convergence requested:
   → Load convergence-engine
   → Run UI methodologies (Bottom-Up-UI-Components, etc.)
   → Achieve 3 clean passes
```

---

## Skill Loading Paths

```python
# Core UI Generation Skills
"/mnt/skills/core/development/svelte-component-generator/SKILL.md"    # ~12 KB
"/mnt/skills/core/development/design-system-manager/SKILL.md"         # ~10 KB
"/mnt/skills/core/development/ui-validation-suite/SKILL.md"           # ~14 KB

# Specialized Skills (load when relevant)
"/mnt/skills/core/development/windows-app-ui-design/SKILL.md"         # ~10 KB (design specs)
"/mnt/skills/core/development/windows-app-ui-testing/SKILL.md"        # ~14 KB (Playwright testing)
"/mnt/skills/core/utilities/ui-migration-manager/SKILL.md"            # ~12 KB (migration tooling)
```

**Rules:**
- Load at most 2 skills per prompt (usually just 1)
- Never load all skills simultaneously
- Prefer the most specific skill for the task
- Keep total context under 35 KB

---

## Quick Reference: When to Load Each Skill

### svelte-component-generator
**Load when user says:**
- "Generate Svelte components"
- "Create Button component"
- "Build the login form"
- "Implement the design"
- References specific component names

**Do NOT load when:** No design specs or unclear requirements

### design-system-manager
**Load when user says:**
- "Set up design system"
- "Create design tokens"
- "Generate Tailwind config"
- "Manage component library"
- "Validate design consistency"

**Do NOT load when:** Design system already configured

### ui-validation-suite
**Load when user says:**
- "Validate accessibility"
- "Check performance"
- "Run visual regression"
- "Test UI quality"
- "Ensure WCAG compliance"

**Do NOT load when:** No UI implementation exists yet

---

## Complexity Assessment Algorithm

**4 Key Indicators:**

1. **Component Count**
   - 1-5: Trivial
   - 5-10: Simple
   - 10-30: Medium
   - 30+: Complex

2. **Design System Presence**
   - No tokens: +0
   - Basic tokens: +1
   - Full system: +2

3. **Multiple Pages**
   - Single page: +0
   - 2-5 pages: +1
   - 6+ pages: +2

4. **Custom Components**
   - Standard only: +0
   - 1-3 custom: +1
   - 4+ custom: +2

**Scoring:**
```javascript
const score = componentCount +
              (hasDesignSystem ? designSystemComplexity : 0) +
              (multiplePages ? pageComplexity : 0) +
              (customComponents ? customComplexity : 0);

if (score <= 5 || componentCount <= 5) return 'trivial';
if (score <= 10 || componentCount <= 10) return 'simple';
if (score <= 20 || componentCount <= 30) return 'medium';
return 'complex';
```

---

## Parallel Coordination (v4.1)

**Purpose:** Generate multiple independent components simultaneously for faster results

**Performance Gains:**
- 10 independent components: 30min → 6min (5x speedup)
- Dependency-aware: Respect component hierarchies
- Conflict detection: Sequential for same-file edits

### Dependency Graph Example

```javascript
// Build dependency graph
const graph = {
  'Button': [],                          // No dependencies
  'Input': [],                           // No dependencies
  'Select': [],                          // No dependencies
  'Form': ['Button', 'Input', 'Select'], // Depends on form controls
  'Card': [],                            // No dependencies
  'LoginPage': ['Form', 'Card'],         // Depends on Form and Card
  'DashboardPage': ['Card']              // Depends on Card
};

// Topological sort into levels
const levels = [
  ['Button', 'Input', 'Select', 'Card'],  // L1: No dependencies (parallel)
  ['Form'],                                // L2: Depends on L1
  ['LoginPage', 'DashboardPage']           // L3: Depends on L2 (parallel)
];

// Generate each level in parallel
for (const level of levels) {
  console.log(`→ Generating ${level.length} components in parallel...`);
  await Promise.all(
    level.map(component => generateComponent(component))
  );
}

// Performance:
// Sequential: 7 components × 3min = 21min
// Parallel: L1 (4 parallel) 3min + L2 (1) 3min + L3 (2 parallel) 3min = 9min
// Speedup: 2.3x
```

**See `references/parallel-coordination.md` for complete patterns**

---

## Integration with Existing System

### Called by windows-app-orchestrator

```python
# In windows-app-orchestrator routing logic
if user_mentions_ui_generation():
    if has_design_specs():
        load_skill("ui-generation-orchestrator")
    else:
        load_skill("windows-app-ui-design")
```

### Calls to Specialized Skills

```python
# ui-generation-orchestrator routing
complexity = assess_complexity(request)

if complexity == 'trivial' or complexity == 'simple':
    load_skill("svelte-component-generator")
elif complexity == 'medium':
    load_skill("svelte-component-generator", mode="parallel")
else:  # complex
    load_skill("ui-battle-plan")
    # battle-plan loads svelte-component-generator with monitoring
```

---

## State Management

**Track generation progress in UI-STATE.yaml:**

```yaml
project: MyApp
phase: ui-generation
status: in_progress

components:
  generated: 12
  total: 30
  current_level: 2

design_system:
  tokens_configured: true
  tailwind_config_generated: true

validation:
  accessibility: pending
  performance: pending
  visual_regression: pending

recommended_next_skill: svelte-component-generator
```

---

## Error Recovery

If wrong skill loaded or context getting large:

1. **Note current progress** in UI-STATE.yaml
2. **Complete current component** if possible
3. **For next prompt**, explicitly state which skill needed
4. **User can say:** "Just use the svelte-component-generator skill"

---

## Commands for Claude

When processing UI generation request:

```
1. READ this orchestrator skill (you're doing this now)
2. ASSESS complexity using 4 indicators
3. LOAD only the needed skill(s)
4. GENERATE components with appropriate strategy
5. VALIDATE with ui-validation-suite
6. UPDATE UI-STATE.yaml
7. RECOMMEND next skill for future prompts
```

**Context Budget:**
- Orchestrator: ~8 KB (always loaded)
- One skill: 10-14 KB
- Working space: Remaining context
- Target: Keep skill content under 30 KB total

---

## References

**Complete guides:**
1. **routing-rules.md** - Detailed detection rules and complexity assessment
2. **parallel-coordination.md** - Dependency-aware parallel generation patterns (v4.1)

**Related Skills:**
- `svelte-component-generator` - AI-powered component generation
- `design-system-manager` - Design tokens and consistency
- `ui-validation-suite` - Accessibility, performance, visual regression
- `windows-app-orchestrator` - Parent orchestrator that routes to this skill

---

*End of UI Generation Orchestrator Skill*
