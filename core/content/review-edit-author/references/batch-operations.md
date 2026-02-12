# Batch Operations Guide

**Purpose:** Comprehensive guide to parallelization patterns for content management
**Audience:** Developers implementing bulk operations
**Size:** ~5KB

---

## Overview

Batch operations enable processing multiple artifacts efficiently through:
- Parallel API calls with controlled concurrency
- Dependency-aware execution ordering
- Rate limiting and queue management
- Progress tracking and error recovery

---

## Pattern 1: Batch Loading

**Use Case:** Loading large numbers of artifacts (10+)

**Performance:**
- Sequential: 100 artifacts × 20ms = 2000ms
- Batch (size 10): 10 batches × 20ms = 200ms
- Speedup: 10x

### Implementation

```javascript
async function loadArtifactsBatch(artifactIds) {
  const BATCH_SIZE = 10;
  const artifacts = [];

  for (let i = 0; i < artifactIds.length; i += BATCH_SIZE) {
    const batch = artifactIds.slice(i, i + BATCH_SIZE);

    const batchResults = await Promise.all(
      batch.map(id =>
        fetch(`http://localhost:3000/api/artifacts/${id}`)
          .then(r => r.json())
          .catch(err => ({
            id,
            error: err.message
          }))
      )
    );

    artifacts.push(...batchResults);

    // Progress tracking
    const progress = Math.min(i + BATCH_SIZE, artifactIds.length);
    console.log(`Loaded ${progress}/${artifactIds.length} artifacts`);
  }

  // Separate successes from failures
  const successful = artifacts.filter(a => !a.error);
  const failed = artifacts.filter(a => a.error);

  return { successful, failed };
}
```

### Configuration

```javascript
const BATCH_CONFIG = {
  size: 10,              // Items per batch
  delayBetween: 0,       // Ms delay between batches (optional)
  retryFailed: true,     // Retry failed items
  maxRetries: 3          // Max retry attempts
};
```

---

## Pattern 2: Chunked Parallel Loading

**Use Case:** Loading related data with rate limits (comments, versions)

**Performance:**
- Sequential: 50 artifacts × 30ms = 1500ms
- Chunked (size 5): 10 chunks × 30ms = 300ms
- Speedup: 5x

### Implementation

```javascript
async function loadCommentsChunked(artifacts) {
  const CHUNK_SIZE = 5; // Rate limit: 5 concurrent
  const results = [];

  for (let i = 0; i < artifacts.length; i += CHUNK_SIZE) {
    const chunk = artifacts.slice(i, i + CHUNK_SIZE);

    await Promise.all(
      chunk.map(async artifact => {
        try {
          const response = await fetch(
            `http://localhost:3000/api/comments/${artifact.type}/${artifact.name}`
          );
          artifact.comments = await response.json();
          results.push({ artifact, success: true });
        } catch (error) {
          artifact.comments = [];
          results.push({
            artifact,
            success: false,
            error: error.message
          });
        }
      })
    );

    console.log(`Loaded comments: ${Math.min(i + CHUNK_SIZE, artifacts.length)}/${artifacts.length}`);
  }

  return results;
}
```

### Rate Limiting

```javascript
function createRateLimiter(maxConcurrent) {
  let active = 0;
  const queue = [];

  return async function rateLimited(fn) {
    while (active >= maxConcurrent) {
      await new Promise(resolve => queue.push(resolve));
    }

    active++;
    try {
      return await fn();
    } finally {
      active--;
      const next = queue.shift();
      if (next) next();
    }
  };
}

// Usage
const limiter = createRateLimiter(5);
const results = await Promise.all(
  artifacts.map(a => limiter(() => loadComments(a)))
);
```

---

## Pattern 3: Queued Processing

**Use Case:** AI operations, expensive computations

**Performance:**
- Controls concurrency
- Respects API rate limits
- Provides progress tracking

### Implementation

```javascript
async function processQueue(items, processor, maxConcurrent = 3) {
  const queue = items.map(item => ({
    item,
    status: 'pending',
    result: null,
    error: null
  }));

  while (queue.some(q => q.status === 'pending')) {
    const pending = queue
      .filter(q => q.status === 'pending')
      .slice(0, maxConcurrent);

    await Promise.all(
      pending.map(async q => {
        q.status = 'processing';
        console.log(`Processing: ${q.item.name || q.item.id}`);

        try {
          q.result = await processor(q.item);
          q.status = 'complete';
          console.log(`✓ Complete: ${q.item.name || q.item.id}`);
        } catch (error) {
          q.error = error.message;
          q.status = 'failed';
          console.log(`✗ Failed: ${q.item.name || q.item.id} - ${error.message}`);
        }
      })
    );
  }

  return {
    completed: queue.filter(q => q.status === 'complete'),
    failed: queue.filter(q => q.status === 'failed'),
    total: queue.length
  };
}
```

### AI Batch Processing

```javascript
async function batchAIImprove(artifacts, improvementType = 'clarity') {
  const processor = async (artifact) => {
    const response = await fetch('http://localhost:3000/api/ai/improve', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        artifact_type: artifact.type,
        artifact_name: artifact.name,
        improvement_type: improvementType,
        context: 'Batch improvement'
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  };

  const result = await processQueue(artifacts, processor, 3);

  console.log(`\nBatch AI Improvement Results:`);
  console.log(`  Completed: ${result.completed.length}`);
  console.log(`  Failed: ${result.failed.length}`);
  console.log(`  Total: ${result.total}`);

  return result;
}
```

---

## Pattern 4: Dependency-Aware Updates

**Use Case:** Multiple update types with execution order constraints

**Prevents:**
- Race conditions
- Ordering issues
- Inconsistent state

### Dependency Detection

```javascript
function detectDependencies(updates) {
  const dependencies = [];

  // Rule: Framework term changes before content updates
  const termChanges = updates.filter(u => u.type === 'term-change');
  const contentUpdates = updates.filter(u => u.type === 'content-update');

  if (termChanges.length > 0 && contentUpdates.length > 0) {
    dependencies.push({
      first: termChanges,
      then: contentUpdates,
      reason: 'Framework terms must propagate before content uses them'
    });
  }

  // Rule: Voice changes before AI generation
  const voiceChanges = updates.filter(u => u.type === 'voice-change');
  const aiGenerations = updates.filter(u => u.type === 'ai-generate');

  if (voiceChanges.length > 0 && aiGenerations.length > 0) {
    dependencies.push({
      first: voiceChanges,
      then: aiGenerations,
      reason: 'AI generation must use updated voice attributes'
    });
  }

  // Rule: Backups before deletions
  const deletions = updates.filter(u => u.type === 'delete');

  if (deletions.length > 0) {
    dependencies.push({
      first: [],
      then: deletions,
      reason: 'Deletions must happen last (after backups)'
    });
  }

  return dependencies;
}
```

### Topological Sort

```javascript
function topologicalSort(updates, dependencies) {
  const levels = [];
  const processed = new Set();

  // Build dependency graph
  const dependsOn = new Map();
  updates.forEach(u => dependsOn.set(u, []));

  dependencies.forEach(dep => {
    dep.then.forEach(u => {
      if (!dependsOn.has(u)) dependsOn.set(u, []);
      dependsOn.get(u).push(...dep.first);
    });
  });

  // Extract levels
  while (processed.size < updates.length) {
    const ready = updates.filter(u => {
      if (processed.has(u)) return false;

      const deps = dependsOn.get(u) || [];
      return deps.every(d => processed.has(d));
    });

    if (ready.length === 0) {
      const remaining = updates.filter(u => !processed.has(u));
      throw new Error(
        `Circular dependency detected: ${remaining.map(u => u.name).join(', ')}`
      );
    }

    levels.push(ready);
    ready.forEach(u => processed.add(u));
  }

  return levels;
}
```

### Execution with Dependencies

```javascript
async function executeWithDependencies(updates) {
  const dependencies = detectDependencies(updates);
  const levels = topologicalSort(updates, dependencies);

  console.log(`Executing ${updates.length} updates in ${levels.length} levels`);

  // Display execution plan
  levels.forEach((level, i) => {
    console.log(`Level ${i + 1}: ${level.length} updates (parallel)`);
    level.forEach(u => console.log(`  - ${u.type}: ${u.name || u.id}`));
  });

  // Execute level by level
  for (let i = 0; i < levels.length; i++) {
    const level = levels[i];
    console.log(`\nExecuting Level ${i + 1}...`);

    await Promise.all(
      level.map(async update => {
        await executeUpdate(update);
        console.log(`  ✓ ${update.type}: ${update.name || update.id}`);
      })
    );
  }

  console.log('\nAll updates executed successfully');
}

async function executeUpdate(update) {
  switch (update.type) {
    case 'term-change':
      return await updateFrameworkTerm(update.termId, update.newValue);
    case 'content-update':
      return await updateArtifact(update.artifactId, update.content);
    case 'voice-change':
      return await updateVoiceAttribute(update.attribute, update.value);
    case 'ai-generate':
      return await generateContent(update.artifactId, update.prompt);
    case 'delete':
      return await deleteArtifact(update.artifactId);
    default:
      throw new Error(`Unknown update type: ${update.type}`);
  }
}
```

---

## Error Recovery

### Retry Strategy

```javascript
async function retryWithBackoff(fn, maxRetries = 3, baseDelay = 1000) {
  let lastError;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      if (attempt < maxRetries - 1) {
        const delay = baseDelay * Math.pow(2, attempt);
        console.log(`Retry ${attempt + 1}/${maxRetries} after ${delay}ms`);
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }

  throw lastError;
}
```

### Checkpoint System

```javascript
class BatchProcessor {
  constructor() {
    this.checkpoint = null;
  }

  async processBatch(items, processor) {
    const results = [];

    for (let i = 0; i < items.length; i++) {
      try {
        const result = await processor(items[i]);
        results.push({ item: items[i], result, success: true });

        // Save checkpoint every 10 items
        if (i % 10 === 0) {
          this.checkpoint = { position: i, results };
        }
      } catch (error) {
        results.push({ item: items[i], error: error.message, success: false });
      }
    }

    return results;
  }

  async resume(items, processor) {
    if (!this.checkpoint) {
      return await this.processBatch(items, processor);
    }

    const remaining = items.slice(this.checkpoint.position);
    const newResults = await this.processBatch(remaining, processor);

    return [...this.checkpoint.results, ...newResults];
  }
}
```

---

## Best Practices

### 1. Choose Appropriate Batch Size
- API calls: 10 items
- Comments/versions: 5 items (rate limit)
- AI operations: 3 items (expensive)

### 2. Always Handle Errors
- Catch individual failures
- Don't fail entire batch
- Return both successes and failures

### 3. Provide Progress Feedback
- Log batch/chunk progress
- Show completion percentage
- Indicate remaining items

### 4. Respect Rate Limits
- Use controlled concurrency
- Add delays if needed
- Monitor API responses

### 5. Test Dependency Logic
- Verify topological sort
- Check for circular dependencies
- Test with various update combinations

---

*End of Batch Operations Guide*
*Part of review-edit-author skill*
*Updated: 2026-02-12*
