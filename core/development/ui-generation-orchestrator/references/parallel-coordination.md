# UI Generation Orchestrator: Parallel Coordination Patterns

**Version:** 1.0.0 (v4.1 Parallelization)
**Purpose:** Dependency-aware parallel component generation

---

## Overview

Generate multiple components concurrently while respecting dependencies and preventing conflicts. Based on v4.1 parallelization patterns from convergence system.

**Key Principles:**
1. **Independence:** Components with no dependencies generate in parallel
2. **Dependencies:** Respect component hierarchies (Button before Form)
3. **Conflicts:** Detect same-file edits, execute sequentially
4. **Performance:** 2-5x speedup for medium/complex operations

---

## Dependency Graph Construction

### Step 1: Extract Component Dependencies

```javascript
function buildDependencyGraph(components) {
  const graph = {};

  for (const component of components) {
    graph[component.name] = component.dependencies || [];
  }

  return graph;
}

// Example:
const components = [
  { name: 'Button', dependencies: [] },
  { name: 'Input', dependencies: [] },
  { name: 'Select', dependencies: [] },
  { name: 'Form', dependencies: ['Button', 'Input', 'Select'] },
  { name: 'Card', dependencies: [] },
  { name: 'LoginPage', dependencies: ['Form', 'Card'] },
  { name: 'DashboardPage', dependencies: ['Card'] }
];

const graph = buildDependencyGraph(components);
// Result:
// {
//   'Button': [],
//   'Input': [],
//   'Select': [],
//   'Form': ['Button', 'Input', 'Select'],
//   'Card': [],
//   'LoginPage': ['Form', 'Card'],
//   'DashboardPage': ['Card']
// }
```

### Step 2: Topological Sort

```javascript
function topologicalSort(graph) {
  const sorted = [];
  const visited = new Set();
  const visiting = new Set();

  function visit(node) {
    if (visited.has(node)) return;
    if (visiting.has(node)) {
      throw new Error(`Circular dependency detected: ${node}`);
    }

    visiting.add(node);

    const dependencies = graph[node] || [];
    for (const dep of dependencies) {
      visit(dep);
    }

    visiting.delete(node);
    visited.add(node);
    sorted.push(node);
  }

  for (const node in graph) {
    visit(node);
  }

  return sorted;
}

// Result: ['Button', 'Input', 'Select', 'Card', 'Form', 'LoginPage', 'DashboardPage']
```

### Step 3: Level-Based Grouping

```javascript
function groupIntoLevels(graph) {
  const levels = [];
  const nodeLevel = {};

  // Calculate level for each node
  function calculateLevel(node) {
    if (nodeLevel[node] !== undefined) return nodeLevel[node];

    const dependencies = graph[node] || [];
    if (dependencies.length === 0) {
      nodeLevel[node] = 0;
      return 0;
    }

    const maxDepLevel = Math.max(
      ...dependencies.map(dep => calculateLevel(dep))
    );
    nodeLevel[node] = maxDepLevel + 1;
    return maxDepLevel + 1;
  }

  // Calculate levels
  for (const node in graph) {
    calculateLevel(node);
  }

  // Group by level
  for (const node in nodeLevel) {
    const level = nodeLevel[node];
    if (!levels[level]) levels[level] = [];
    levels[level].push(node);
  }

  return levels;
}

// Result:
// [
//   ['Button', 'Input', 'Select', 'Card'],  // Level 0: No dependencies
//   ['Form'],                                // Level 1: Depends on level 0
//   ['LoginPage', 'DashboardPage']           // Level 2: Depends on level 1
// ]
```

---

## Parallel Execution

### Basic Parallel Pattern

```javascript
async function generateComponentsInParallel(components) {
  console.log(`→ Generating ${components.length} components in parallel...`);

  const results = await Promise.all(
    components.map(async (component) => {
      console.log(`  ├─ Generating ${component.name}...`);
      const result = await generateComponent(component);
      console.log(`  ├─ ✓ ${component.name} complete`);
      return result;
    })
  );

  console.log(`  └─ All ${components.length} components generated`);
  return results;
}
```

### Level-Based Parallel Pattern

```javascript
async function generateByLevels(graph) {
  const levels = groupIntoLevels(graph);

  console.log(`\n→ Dependency-aware generation (${levels.length} levels)...`);

  for (let i = 0; i < levels.length; i++) {
    const level = levels[i];
    console.log(`\nLevel ${i}: ${level.length} components (parallel)`);

    await generateComponentsInParallel(
      level.map(name => ({
        name,
        dependencies: graph[name]
      }))
    );
  }

  console.log(`\n✅ All levels complete`);
}

// Example output:
// → Dependency-aware generation (3 levels)...
//
// Level 0: 4 components (parallel)
//   ├─ Generating Button...
//   ├─ Generating Input...
//   ├─ Generating Select...
//   ├─ Generating Card...
//   ├─ ✓ Button complete
//   ├─ ✓ Input complete
//   ├─ ✓ Select complete
//   └─ ✓ Card complete
//
// Level 1: 1 components (parallel)
//   ├─ Generating Form...
//   └─ ✓ Form complete
//
// Level 2: 2 components (parallel)
//   ├─ Generating LoginPage...
//   ├─ Generating DashboardPage...
//   ├─ ✓ LoginPage complete
//   └─ ✓ DashboardPage complete
//
// ✅ All levels complete
```

---

## Conflict Detection

### Problem: Same-File Edits

Multiple components might need to edit the same file (e.g., `index.ts` for barrel exports).

### Solution: Group by Target File

```javascript
function detectConflicts(components) {
  const byFile = components.reduce((groups, component) => {
    const file = component.targetFile || `${component.name}.svelte`;
    if (!groups[file]) groups[file] = [];
    groups[file].push(component);
    return groups;
  }, {});

  const independent = Object.entries(byFile).filter(([_, comps]) =>
    comps.length === 1
  );

  const conflicting = Object.entries(byFile).filter(([_, comps]) =>
    comps.length > 1
  );

  return { independent, conflicting };
}

// Example:
const components = [
  { name: 'Button', targetFile: 'Button.svelte' },
  { name: 'Input', targetFile: 'Input.svelte' },
  { name: 'BarrelExport1', targetFile: 'index.ts' },
  { name: 'BarrelExport2', targetFile: 'index.ts' }
];

const { independent, conflicting } = detectConflicts(components);
// independent: [['Button.svelte', [...]], ['Input.svelte', [...]]]
// conflicting: [['index.ts', [BarrelExport1, BarrelExport2]]]
```

### Two-Phase Execution

```javascript
async function generateWithConflictDetection(components) {
  const { independent, conflicting } = detectConflicts(components);

  console.log(`\n→ Analyzing ${components.length} components...`);
  console.log(`  Independent files: ${independent.length}`);
  console.log(`  Conflicting files: ${conflicting.length}`);

  let generated = 0;

  // Phase 1: Parallel generation for independent files
  if (independent.length > 0) {
    console.log(`\n→ Phase 1: Parallel generation (${independent.length} files)...`);

    const results = await Promise.all(
      independent.map(async ([file, [component]]) => {
        const result = await generateComponent(component);
        return result;
      })
    );

    generated += results.length;
    console.log(`  ✓ Phase 1 complete: ${results.length} components`);
  }

  // Phase 2: Sequential generation for conflicting files
  if (conflicting.length > 0) {
    console.log(`\n→ Phase 2: Sequential generation (${conflicting.length} files)...`);

    for (const [file, fileComponents] of conflicting) {
      console.log(`  Processing ${file} (${fileComponents.length} components)...`);

      for (const component of fileComponents) {
        await generateComponent(component);
        generated++;
      }

      console.log(`  ✓ ${file} complete`);
    }

    console.log(`  ✓ Phase 2 complete: ${conflicting.length} files`);
  }

  return { generated };
}
```

---

## Performance Optimization

### Concurrency Control

```javascript
async function generateWithConcurrencyLimit(components, maxConcurrent = 5) {
  const results = [];

  for (let i = 0; i < components.length; i += maxConcurrent) {
    const batch = components.slice(i, i + maxConcurrent);

    console.log(`\nBatch ${Math.floor(i / maxConcurrent) + 1}: ${batch.length} components`);

    const batchResults = await Promise.all(
      batch.map(component => generateComponent(component))
    );

    results.push(...batchResults);

    console.log(`  ✓ Batch complete: ${batchResults.length}/${components.length} total`);
  }

  return results;
}

// Example: 12 components with max 5 concurrent
// Batch 1: 5 components
//   ✓ Batch complete: 5/12 total
// Batch 2: 5 components
//   ✓ Batch complete: 10/12 total
// Batch 3: 2 components
//   ✓ Batch complete: 12/12 total
```

### Combined: Levels + Concurrency + Conflicts

```javascript
async function generateOptimized(graph, maxConcurrent = 5) {
  const levels = groupIntoLevels(graph);

  for (let i = 0; i < levels.length; i++) {
    const levelComponents = levels[i].map(name => ({
      name,
      dependencies: graph[name],
      targetFile: `${name}.svelte`
    }));

    console.log(`\n→ Level ${i}: ${levelComponents.length} components`);

    // Detect conflicts within this level
    const { independent, conflicting } = detectConflicts(levelComponents);

    // Phase 1: Parallel with concurrency limit
    if (independent.length > 0) {
      const independentComponents = independent.map(([_, [comp]]) => comp);
      await generateWithConcurrencyLimit(independentComponents, maxConcurrent);
    }

    // Phase 2: Sequential for conflicts
    if (conflicting.length > 0) {
      for (const [file, comps] of conflicting) {
        for (const comp of comps) {
          await generateComponent(comp);
        }
      }
    }
  }
}
```

---

## Real-World Example

### Scenario: Complete Venue Management UI

**Components:**
```javascript
const components = [
  // Level 0: Base components (no dependencies)
  { name: 'Button', deps: [] },
  { name: 'Input', deps: [] },
  { name: 'Select', deps: [] },
  { name: 'Checkbox', deps: [] },
  { name: 'Card', deps: [] },
  { name: 'Table', deps: [] },
  { name: 'Modal', deps: [] },

  // Level 1: Composite components (depend on base)
  { name: 'VenueCard', deps: ['Card', 'Button'] },
  { name: 'VenueForm', deps: ['Input', 'Select', 'Checkbox', 'Button'] },
  { name: 'VenueTable', deps: ['Table', 'Button'] },
  { name: 'DeleteModal', deps: ['Modal', 'Button'] },

  // Level 2: Page components (depend on composites)
  { name: 'VenueList', deps: ['VenueCard', 'VenueTable', 'Button'] },
  { name: 'VenueDetail', deps: ['VenueCard', 'Button', 'DeleteModal'] },
  { name: 'VenueFormPage', deps: ['VenueForm'] },

  // Level 3: App composition
  { name: 'VenueManagement', deps: ['VenueList', 'VenueDetail', 'VenueFormPage'] }
];
```

**Execution Plan:**
```
Level 0: 7 components (parallel, max 5 concurrent)
  Batch 1: Button, Input, Select, Checkbox, Card (5 parallel)
  Batch 2: Table, Modal (2 parallel)
  Time: ~3 minutes

Level 1: 4 components (parallel, max 5 concurrent)
  Batch 1: VenueCard, VenueForm, VenueTable, DeleteModal (4 parallel)
  Time: ~3 minutes

Level 2: 3 components (parallel, max 5 concurrent)
  Batch 1: VenueList, VenueDetail, VenueFormPage (3 parallel)
  Time: ~3 minutes

Level 3: 1 component (sequential)
  VenueManagement
  Time: ~3 minutes

Total: ~12 minutes
Sequential would be: 15 components × 3min = 45 minutes
Speedup: 3.75x
```

---

## Integration with Convergence

### Monitoring During Parallel Execution

```javascript
async function generateWithMonitoring(components) {
  const levels = groupIntoLevels(buildDependencyGraph(components));

  for (const level of levels) {
    // Generate components in parallel
    const results = await Promise.all(
      level.map(async (component) => {
        const generated = await generateComponent(component);

        // Verify evidence (from convergence system)
        const verified = await verifyEvidence({
          claim: `${component.name} generated correctly`,
          evidence: [
            'File created',
            'TypeScript compiles',
            'No accessibility violations',
            'Uses design tokens'
          ]
        });

        if (!verified) {
          console.warn(`⚠️  ${component.name} verification failed`);
        }

        return { generated, verified };
      })
    );

    // Check for infinite loops (regenerating same component)
    const signatures = results.map(r => getComponentSignature(r));
    const duplicates = findDuplicates(signatures);

    if (duplicates.length > 0) {
      console.warn('⚠️  Infinite loop detected, stopping generation');
      break;
    }
  }
}
```

---

## Error Handling

### Parallel Execution Errors

```javascript
async function generateWithErrorHandling(components) {
  const results = await Promise.allSettled(
    components.map(component => generateComponent(component))
  );

  const succeeded = results.filter(r => r.status === 'fulfilled');
  const failed = results.filter(r => r.status === 'rejected');

  console.log(`✅ Succeeded: ${succeeded.length}`);
  console.log(`❌ Failed: ${failed.length}`);

  if (failed.length > 0) {
    console.log('\nFailed components:');
    failed.forEach((result, index) => {
      console.log(`  - ${components[index].name}: ${result.reason}`);
    });

    // Retry failed components sequentially
    console.log('\n→ Retrying failed components...');
    for (const index of failed.map((_, i) => i)) {
      try {
        await generateComponent(components[index]);
        console.log(`  ✓ ${components[index].name} succeeded on retry`);
      } catch (error) {
        console.log(`  ✗ ${components[index].name} failed again: ${error.message}`);
      }
    }
  }

  return { succeeded: succeeded.length, failed: failed.length };
}
```

---

## Performance Metrics

### Expected Speedups

| Components | Levels | Concurrent/Level | Sequential Time | Parallel Time | Speedup |
|-----------|--------|------------------|-----------------|---------------|---------|
| 5 | 1 | 5 | 15 min | 15 min | 1x |
| 10 | 2 | 5 | 30 min | 12 min | 2.5x |
| 20 | 3 | 5-7 | 60 min | 21 min | 2.9x |
| 30 | 4 | 5-10 | 90 min | 30 min | 3x |
| 50 | 5 | 10 | 150 min | 45 min | 3.3x |

### Diminishing Returns

```
Speedup diminishes with:
- More dependencies (fewer parallel opportunities)
- More conflicting files (sequential execution required)
- Higher concurrency (coordination overhead)

Optimal concurrency: 5-10 components
Beyond 10: Marginal gains, increased complexity
```

---

*End of Parallel Coordination Patterns*
