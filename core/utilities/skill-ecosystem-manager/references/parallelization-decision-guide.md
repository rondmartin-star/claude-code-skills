# Parallelization Decision Guide

**Purpose:** Determine if new skills should include parallelization
**Version:** v4.1.0
**Date:** 2026-02-14

---

## Quick Decision Tree

```
Creating new skill?
    │
    ├─ Does it process multiple items commonly? ─ No ──→ ❌ Skip parallelization
    │                                             Yes
    │                                              │
    ├─ Are operations independent? ────────────── No ──→ ❌ Skip parallelization
    │                                             Yes
    │                                              │
    ├─ Is typical volume > 10 items? ──────────── No ──→ 🤔 Evaluate case-by-case
    │                                             Yes
    │                                              │
    ├─ Will parallelization give > 2x speedup? ── No ──→ 🤔 Evaluate case-by-case
    │                                             Yes
    │                                              │
    └─────────────────────────────────────────────────→ ✅ Add parallelization
```

---

## Detailed Decision Criteria

### ✅ Strong Indicators for Parallelization

1. **Batch Operations**
   - Creating/updating/deleting multiple documents
   - Processing multiple files
   - Validating multiple configurations
   - **Example:** document-management bulk operations

2. **Multi-Platform Operations**
   - Publishing to blog, Twitter, LinkedIn simultaneously
   - Generating content for multiple formats
   - Syncing across multiple locations
   - **Example:** content-creation multi-platform generation

3. **Parallel Validation/Analysis**
   - Running multiple validators concurrently
   - Multiple methodologies analyzing same data
   - Independent quality checks
   - **Example:** audit-orchestrator 15 methodologies

4. **Concurrent Generation**
   - Generating multiple components
   - Creating multiple artifacts
   - Building multiple outputs
   - **Example:** svelte-component-generator batch creation

### ❌ Strong Indicators Against Parallelization

1. **Sequential Workflows**
   - Step 1 must complete before Step 2
   - Each step depends on previous result
   - State changes between steps
   - **Example:** corpus-init (setup sequence)

2. **User Interaction**
   - Waiting for user input
   - Confirmation dialogs
   - Interactive workflows
   - **Example:** confirm-operation skill

3. **Single-Item Focus**
   - Primarily works with one item
   - One configuration file
   - One status check
   - **Example:** corpus-detect (single status)

4. **Data Integrity Requirements**
   - Sequential processing ensures correctness
   - Transactional operations
   - Order matters for correctness
   - **Example:** backup-restore operations

5. **Planning/Design Activities**
   - Requirements gathering
   - Design decisions
   - Architecture planning
   - **Example:** windows-app-system-design

### 🤔 Evaluate Case-by-Case

1. **Orchestrators**
   - **Usually skip:** Orchestrators delegate to other skills
   - **Exception:** If orchestrator does its own processing
   - **Example:** audit-orchestrator parallelizes methodologies

2. **Export/Import Operations**
   - **Consider:** Volume and data dependencies
   - **High volume, independent:** Parallelize
   - **Data integrity critical:** Sequential
   - **Example:** corpus-export (delegates, no self-parallelization)

3. **Monitoring Skills**
   - **Depends:** What's being monitored
   - **Multiple independent monitors:** Parallelize
   - **Sequential checks:** Skip
   - **Example:** iterative-phase-review (parallel monitoring)

---

## Parallelization Patterns

### Pattern 1: Batch CRUD Operations

**Use For:** document-management, content management

**Implementation:**
```javascript
async function batchCreate(documents) {
  const results = await Promise.all(
    documents.map(doc => createDocument(doc))
  );
  return results;
}
```

**When to Use:**
- Common to create/update/delete 10+ items
- Operations are independent
- No cross-document dependencies

### Pattern 2: Multi-Platform Generation

**Use For:** Publishing, content creation

**Implementation:**
```javascript
async function generateMultiPlatform(content, platforms) {
  const outputs = await Promise.all(
    platforms.map(platform => formatFor Platform(content, platform))
  );
  return outputs;
}
```

**When to Use:**
- Generating for multiple targets (blog, social, etc.)
- Each platform format is independent
- Typical use case involves 2+ platforms

### Pattern 3: Parallel Validation

**Use For:** Audits, quality checks, testing

**Implementation:**
```javascript
async function parallelValidation(validators) {
  const results = await Promise.all(
    validators.map(v => v.validate())
  );
  return aggregateResults(results);
}
```

**When to Use:**
- Multiple independent checks
- Each validator is self-contained
- No validation dependencies

### Pattern 4: Concurrent Analysis

**Use For:** Convergence, multi-methodology audits

**Implementation:**
```javascript
async function concurrentAnalysis(methodologies) {
  const analyses = await Promise.all(
    methodologies.map(m => analyzeWith(m))
  );
  return mergeAnalyses(analyses);
}
```

**When to Use:**
- Multiple analysis approaches
- Each methodology independent
- Results can be aggregated

### Pattern 5: Model-Optimized Execution

**Use For:** Mixed operation types in any skill

**Implementation:**
```javascript
function selectModel(taskType) {
  const opusFor = ['user-facing', 'security-critical', 'complex-reasoning'];
  const sonnetFor = ['technical-analysis', 'repetitive-tasks', 'structured-output'];

  return opusFor.includes(taskType) ? 'opus' : 'sonnet';
}

async function optimizedExecution(tasks) {
  const grouped = groupByModel(tasks);
  const results = await Promise.all([
    executeWithModel(grouped.opus, 'opus'),
    executeWithModel(grouped.sonnet, 'sonnet')
  ]);
  return mergeResults(results);
}
```

**When to Use:**
- Skill has both user-facing and technical operations
- Cost/performance optimization matters
- Can batch by model type

---

## Real-World Examples

### Example 1: document-management (PARALLELIZED)

**Decision:**
- ✅ Processes multiple documents
- ✅ Independent operations
- ✅ Typical volume > 10 (bulk operations)
- ✅ 3-10x speedup

**Pattern:** Pattern 1 (Batch CRUD)

**Rationale:** Users commonly create, delete, or update multiple documents. Each operation is independent.

### Example 2: corpus-init (NOT PARALLELIZED)

**Decision:**
- ❌ Sequential workflow (create structure → configure → validate)
- ❌ Each step depends on previous
- ❌ Single corpus initialization

**Rationale:** Setup must happen in specific order. No benefit from parallelization.

### Example 3: content-creation (PARALLELIZED)

**Decision:**
- ✅ Multi-platform by design
- ✅ Independent format generation
- ✅ Typical use: 2-5 platforms
- ✅ 3-5x speedup

**Pattern:** Pattern 2 (Multi-Platform)

**Rationale:** Primary use case is "publish to blog AND Twitter AND LinkedIn." Perfect for parallelization.

### Example 4: corpus-detect (NOT PARALLELIZED)

**Decision:**
- ❌ Single status check
- ❌ One corpus at a time
- ❌ Fast enough (<1s)

**Rationale:** Checking status of one corpus. Parallelization overhead > benefit.

### Example 5: audit-orchestrator (PARALLELIZED)

**Decision:**
- ✅ Runs 15 methodologies
- ✅ Each methodology independent
- ✅ High volume (always 15)
- ✅ 40-50% speedup proven

**Pattern:** Pattern 3 + Pattern 4 (Validation + Analysis)

**Rationale:** Running 15 methodologies sequentially takes 5-10 minutes. Parallel reduces to 2-5 minutes. Production-proven.

---

## How to Document Decision

In every skill SKILL.md, include either:

### If Parallelized:

```markdown
## v4.1 Parallelization

**Decision:** ✅ Parallelized

**Rationale:**
- [Why parallelization makes sense]
- [Expected use case with multiple items]
- [Performance benefit]

**Parallel Capabilities:**
- [Specific operation 1]
- [Specific operation 2]

**Performance:**
| Operation | Sequential | Parallel | Speedup |
|-----------|-----------|----------|---------|
| [Operation] | [Time] | [Time] | [X]x |

**Pattern:** [Pattern name from this guide]

**See:** `core/references/parallelization-patterns.md`
```

### If Not Parallelized:

```markdown
## v4.1 Parallelization

**Decision:** ❌ Not Parallelized

**Rationale:**
- [Why this skill is sequential]
- [Why parallelization doesn't apply]

**Example:** [Specific workflow showing sequential nature]
```

---

## Performance Expectations

### Typical Speedups by Pattern

| Pattern | Items | Sequential | Parallel | Speedup |
|---------|-------|-----------|----------|---------|
| Batch CRUD | 10 | 5m | 1m | 5x |
| Batch CRUD | 50 | 25m | 5m | 5x |
| Multi-platform | 3 | 3m | 1m | 3x |
| Multi-platform | 5 | 5m | 1m | 5x |
| Validation | 5 | 2.5m | 30s | 5x |
| Validation | 15 | 7.5m | 1m | 7.5x |
| Analysis | 7 | 10m | 5m | 2x |
| Analysis | 15 | 20m | 10m | 2x |

**Rule of thumb:** Expect 2-10x speedup depending on:
- Number of parallel items (more = better)
- Item processing time (longer = better)
- Parallelization overhead (lower = better)

---

## Common Mistakes

### ❌ Mistake 1: Parallelizing Sequential Workflows

```javascript
// WRONG - Steps are dependent
async function wrongParallel() {
  const [step1, step2, step3] = await Promise.all([
    initializeProject(),  // step2 needs step1
    configureProject(),   // step3 needs step2
    validateProject()
  ]);
}

// CORRECT - Sequential
async function correctSequential() {
  await initializeProject();
  await configureProject();
  await validateProject();
}
```

### ❌ Mistake 2: Parallelizing Low-Volume Operations

```javascript
// WRONG - Overhead > benefit for 1-2 items
async function wrongLowVolume() {
  const [doc] = await Promise.all([
    createDocument(singleDoc)  // Just use await directly
  ]);
}

// CORRECT - Direct for single item
async function correctSingleItem() {
  const doc = await createDocument(singleDoc);
}
```

### ❌ Mistake 3: Parallelizing Data-Dependent Operations

```javascript
// WRONG - Each backup depends on previous state
async function wrongBackup() {
  const backups = await Promise.all(
    files.map(f => createBackup(f))  // Order matters!
  ]);
}

// CORRECT - Sequential ensures integrity
async function correctBackup() {
  const backups = [];
  for (const file of files) {
    backups.push(await createBackup(file));
  }
}
```

---

## Ecosystem Evolution

### Current State (v4.1)

- **24/61 skills parallelized** (39%)
- **37/61 skills intentionally sequential** (61%)
- **Optimal coverage** for current use cases

### Future Additions

When creating new skills:
1. Use this decision guide
2. Default to NO parallelization
3. Add only if clear benefit
4. Document decision either way

**Philosophy:** Intelligent parallelization > Universal parallelization

---

**Last Updated:** 2026-02-14
**Version:** v4.1.0
**Status:** Production guide for all new skills
