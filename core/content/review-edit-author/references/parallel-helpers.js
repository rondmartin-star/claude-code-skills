/**
 * Parallel Helpers for Content Management
 *
 * Utilities for batch operations, chunking, queuing, and dependency management
 *
 * @module parallel-helpers
 * @version 1.0.0
 */

// ============================================================================
// Pattern 1: Batch Loading
// ============================================================================

/**
 * Load items in batches with parallel execution
 *
 * @param {Array} items - Items to load
 * @param {Function} loader - Async function to load each item
 * @param {Object} options - Configuration options
 * @returns {Object} Results with successful and failed items
 */
async function batchLoad(items, loader, options = {}) {
  const {
    batchSize = 10,
    delayBetween = 0,
    retryFailed = false,
    maxRetries = 3,
    onProgress = null
  } = options;

  const successful = [];
  const failed = [];

  for (let i = 0; i < items.length; i += batchSize) {
    const batch = items.slice(i, i + batchSize);

    const batchResults = await Promise.all(
      batch.map(async (item) => {
        try {
          const result = retryFailed
            ? await retryWithBackoff(() => loader(item), maxRetries)
            : await loader(item);
          return { item, result, success: true };
        } catch (error) {
          return { item, error: error.message, success: false };
        }
      })
    );

    // Separate successes and failures
    batchResults.forEach(r => {
      if (r.success) {
        successful.push(r);
      } else {
        failed.push(r);
      }
    });

    // Progress callback
    if (onProgress) {
      const progress = Math.min(i + batchSize, items.length);
      onProgress(progress, items.length);
    }

    // Delay between batches
    if (delayBetween > 0 && i + batchSize < items.length) {
      await delay(delayBetween);
    }
  }

  return { successful, failed, total: items.length };
}

// ============================================================================
// Pattern 2: Chunked Parallel Loading
// ============================================================================

/**
 * Load items in chunks with controlled concurrency
 *
 * @param {Array} items - Items to process
 * @param {Function} processor - Async function to process each item
 * @param {Object} options - Configuration options
 * @returns {Array} Results for all items
 */
async function chunkParallel(items, processor, options = {}) {
  const {
    chunkSize = 5,
    onProgress = null
  } = options;

  const results = [];

  for (let i = 0; i < items.length; i += chunkSize) {
    const chunk = items.slice(i, i + chunkSize);

    const chunkResults = await Promise.all(
      chunk.map(async (item) => {
        try {
          const result = await processor(item);
          return { item, result, success: true };
        } catch (error) {
          return { item, error: error.message, success: false };
        }
      })
    );

    results.push(...chunkResults);

    // Progress callback
    if (onProgress) {
      const progress = Math.min(i + chunkSize, items.length);
      onProgress(progress, items.length);
    }
  }

  return results;
}

/**
 * Create a rate limiter for controlled concurrency
 *
 * @param {Number} maxConcurrent - Maximum concurrent operations
 * @returns {Function} Rate-limited wrapper function
 */
function createRateLimiter(maxConcurrent) {
  let active = 0;
  const queue = [];

  return async function rateLimited(fn) {
    // Wait if at capacity
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

// ============================================================================
// Pattern 3: Queued Processing
// ============================================================================

/**
 * Process items through a queue with max concurrency
 *
 * @param {Array} items - Items to process
 * @param {Function} processor - Async function to process each item
 * @param {Object} options - Configuration options
 * @returns {Object} Results with completed, failed, and total counts
 */
async function processQueue(items, processor, options = {}) {
  const {
    maxConcurrent = 3,
    onProgress = null,
    onItemComplete = null
  } = options;

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
      pending.map(async (q) => {
        q.status = 'processing';

        try {
          q.result = await processor(q.item);
          q.status = 'complete';

          if (onItemComplete) {
            onItemComplete(q.item, q.result, null);
          }
        } catch (error) {
          q.error = error.message;
          q.status = 'failed';

          if (onItemComplete) {
            onItemComplete(q.item, null, error.message);
          }
        }
      })
    );

    // Progress callback
    if (onProgress) {
      const completed = queue.filter(q => q.status !== 'pending').length;
      onProgress(completed, queue.length);
    }
  }

  return {
    completed: queue.filter(q => q.status === 'complete'),
    failed: queue.filter(q => q.status === 'failed'),
    total: queue.length
  };
}

// ============================================================================
// Pattern 4: Dependency-Aware Updates
// ============================================================================

/**
 * Detect dependencies between updates
 *
 * @param {Array} updates - Updates to analyze
 * @returns {Array} Dependency rules
 */
function detectDependencies(updates) {
  const dependencies = [];

  // Rule 1: Framework term changes before content updates
  const termChanges = updates.filter(u => u.type === 'term-change');
  const contentUpdates = updates.filter(u => u.type === 'content-update');

  if (termChanges.length > 0 && contentUpdates.length > 0) {
    dependencies.push({
      first: termChanges,
      then: contentUpdates,
      reason: 'Framework terms must propagate before content uses them'
    });
  }

  // Rule 2: Voice changes before AI generation
  const voiceChanges = updates.filter(u => u.type === 'voice-change');
  const aiGenerations = updates.filter(u => u.type === 'ai-generate');

  if (voiceChanges.length > 0 && aiGenerations.length > 0) {
    dependencies.push({
      first: voiceChanges,
      then: aiGenerations,
      reason: 'AI generation must use updated voice attributes'
    });
  }

  // Rule 3: Config changes before dependent operations
  const configChanges = updates.filter(u => u.type === 'config-change');
  const dependentOps = updates.filter(u =>
    ['content-update', 'ai-generate', 'term-change'].includes(u.type)
  );

  if (configChanges.length > 0 && dependentOps.length > 0) {
    dependencies.push({
      first: configChanges,
      then: dependentOps,
      reason: 'Configuration must be updated before operations use it'
    });
  }

  // Rule 4: Backups before deletions
  const deletions = updates.filter(u => u.type === 'delete');

  if (deletions.length > 0) {
    const nonDeletions = updates.filter(u => u.type !== 'delete');
    if (nonDeletions.length > 0) {
      dependencies.push({
        first: nonDeletions,
        then: deletions,
        reason: 'Deletions must happen last (after other operations)'
      });
    }
  }

  return dependencies;
}

/**
 * Perform topological sort on updates based on dependencies
 *
 * @param {Array} updates - Updates to sort
 * @param {Array} dependencies - Dependency rules
 * @returns {Array} Updates grouped by execution level
 */
function topologicalSort(updates, dependencies) {
  const levels = [];
  const processed = new Set();

  // Build dependency map
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
    // Find updates with all dependencies satisfied
    const ready = updates.filter(u => {
      if (processed.has(u)) return false;

      const deps = dependsOn.get(u) || [];
      return deps.every(d => processed.has(d));
    });

    if (ready.length === 0) {
      // Circular dependency or unreachable updates
      const remaining = updates.filter(u => !processed.has(u));
      throw new Error(
        `Circular dependency or unreachable updates: ${
          remaining.map(u => u.name || u.id).join(', ')
        }`
      );
    }

    levels.push(ready);
    ready.forEach(u => processed.add(u));
  }

  return levels;
}

/**
 * Execute updates with dependency awareness
 *
 * @param {Array} updates - Updates to execute
 * @param {Function} executor - Function to execute each update
 * @param {Object} options - Configuration options
 * @returns {Object} Execution results
 */
async function executeWithDependencies(updates, executor, options = {}) {
  const {
    onProgress = null,
    onLevelStart = null,
    onLevelComplete = null
  } = options;

  const dependencies = detectDependencies(updates);
  const levels = topologicalSort(updates, dependencies);

  const results = {
    levels: levels.length,
    completed: [],
    failed: [],
    total: updates.length
  };

  // Execute level by level
  for (let i = 0; i < levels.length; i++) {
    const level = levels[i];

    if (onLevelStart) {
      onLevelStart(i + 1, level.length);
    }

    // Execute all updates in this level in parallel
    const levelResults = await Promise.all(
      level.map(async (update) => {
        try {
          const result = await executor(update);
          return { update, result, success: true };
        } catch (error) {
          return { update, error: error.message, success: false };
        }
      })
    );

    // Collect results
    levelResults.forEach(r => {
      if (r.success) {
        results.completed.push(r);
      } else {
        results.failed.push(r);
      }
    });

    if (onLevelComplete) {
      onLevelComplete(i + 1, levelResults);
    }

    if (onProgress) {
      const totalProcessed = results.completed.length + results.failed.length;
      onProgress(totalProcessed, updates.length);
    }
  }

  return results;
}

// ============================================================================
// Error Recovery Utilities
// ============================================================================

/**
 * Retry a function with exponential backoff
 *
 * @param {Function} fn - Async function to retry
 * @param {Number} maxRetries - Maximum retry attempts
 * @param {Number} baseDelay - Base delay in ms
 * @returns {Promise} Result of successful execution
 */
async function retryWithBackoff(fn, maxRetries = 3, baseDelay = 1000) {
  let lastError;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;

      if (attempt < maxRetries - 1) {
        const delay = baseDelay * Math.pow(2, attempt);
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }

  throw lastError;
}

/**
 * Checkpoint-based batch processor
 */
class CheckpointProcessor {
  constructor() {
    this.checkpoint = null;
    this.checkpointInterval = 10; // Save every 10 items
  }

  /**
   * Process items with checkpointing
   *
   * @param {Array} items - Items to process
   * @param {Function} processor - Processing function
   * @returns {Array} Results
   */
  async process(items, processor) {
    const results = [];

    for (let i = 0; i < items.length; i++) {
      try {
        const result = await processor(items[i]);
        results.push({ item: items[i], result, success: true });
      } catch (error) {
        results.push({
          item: items[i],
          error: error.message,
          success: false
        });
      }

      // Save checkpoint
      if (i % this.checkpointInterval === 0) {
        this.checkpoint = { position: i, results: [...results] };
      }
    }

    this.checkpoint = null; // Clear after successful completion
    return results;
  }

  /**
   * Resume processing from last checkpoint
   *
   * @param {Array} items - Original items
   * @param {Function} processor - Processing function
   * @returns {Array} Combined results
   */
  async resume(items, processor) {
    if (!this.checkpoint) {
      return await this.process(items, processor);
    }

    const { position, results: previousResults } = this.checkpoint;
    const remaining = items.slice(position + 1);

    const newResults = await this.process(remaining, processor);

    return [...previousResults, ...newResults];
  }

  /**
   * Clear checkpoint
   */
  clearCheckpoint() {
    this.checkpoint = null;
  }

  /**
   * Get checkpoint status
   */
  getCheckpoint() {
    return this.checkpoint;
  }
}

// ============================================================================
// Utility Functions
// ============================================================================

/**
 * Delay execution
 *
 * @param {Number} ms - Milliseconds to delay
 * @returns {Promise} Resolves after delay
 */
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Group items by a key
 *
 * @param {Array} items - Items to group
 * @param {Function} keyFn - Function to extract key
 * @returns {Map} Grouped items
 */
function groupBy(items, keyFn) {
  const groups = new Map();

  items.forEach(item => {
    const key = keyFn(item);
    if (!groups.has(key)) {
      groups.set(key, []);
    }
    groups.get(key).push(item);
  });

  return groups;
}

/**
 * Partition items into chunks
 *
 * @param {Array} items - Items to partition
 * @param {Number} size - Chunk size
 * @returns {Array} Array of chunks
 */
function partition(items, size) {
  const chunks = [];

  for (let i = 0; i < items.length; i += size) {
    chunks.push(items.slice(i, i + size));
  }

  return chunks;
}

// ============================================================================
// Exports
// ============================================================================

module.exports = {
  // Pattern 1: Batch Loading
  batchLoad,

  // Pattern 2: Chunked Parallel
  chunkParallel,
  createRateLimiter,

  // Pattern 3: Queued Processing
  processQueue,

  // Pattern 4: Dependency-Aware
  detectDependencies,
  topologicalSort,
  executeWithDependencies,

  // Error Recovery
  retryWithBackoff,
  CheckpointProcessor,

  // Utilities
  delay,
  groupBy,
  partition
};
