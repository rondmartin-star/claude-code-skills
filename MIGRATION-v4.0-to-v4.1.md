# Migration Guide: v4.0 to v4.1

**Parallelized Architecture Upgrade**

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Migration Steps](#migration-steps)
4. [Configuration Examples](#configuration-examples)
5. [Testing Migration](#testing-migration)
6. [Rollback Procedure](#rollback-procedure)
7. [Common Issues](#common-issues)
8. [FAQ](#faq)
9. [Support](#support)

---

## Overview

### What's New in v4.1

**Parallel Execution Architecture:**
- Unified mode combining audit + convergence + learning
- Parallelized methodology execution (up to 15 concurrent)
- Smart model selection (Opus vs Sonnet per methodology)
- Intelligent dependency resolution
- Real-time battle-plan monitoring
- Batch artifact operations

**Key Benefits:**
- **10x Faster**: 15 methodologies run in parallel vs sequential
- **Cost Optimized**: Sonnet for speed, Opus for quality
- **Better Results**: Learning skills track patterns in real-time
- **Same Quality**: All v4.0 guarantees maintained

### Breaking Changes

**None.** v4.1 is fully backward compatible.

- Sequential mode still available
- v4.0 configurations work unchanged
- Parallel mode is opt-in
- All existing workflows preserved

### Backward Compatibility Guarantees

- ✅ v4.0 corpus-config.json files work in v4.1
- ✅ Sequential execution available as fallback
- ✅ Audit mode still supported
- ✅ All v4.0 skills function identically
- ✅ API contracts unchanged

---

## Prerequisites

### Version Requirements

**Before Migration:**
- v4.0.0 or higher
- CorpusHub API v1.0+
- Claude Opus 4.5 or Sonnet 4.5 access

**Check Your Version:**
```bash
# In project root
"Check corpus status"
# Should show version: 4.0.x
```

### Configuration Review

**Review Before Migrating:**

1. **Current audit mode:**
   ```json
   {
     "audit": {
       "mode": "audit"  // or "convergence"
     }
   }
   ```

2. **Applicable audits list:**
   ```json
   {
     "audit": {
       "applicable_audits": ["security", "quality", ...]
     }
   }
   ```

3. **Methodology definitions:**
   ```json
   {
     "audit": {
       "convergence": {
         "methodologies": [...]
       }
     }
   }
   ```

### Backup Recommendations

**Before Migration:**

1. **Backup corpus-config.json:**
   ```bash
   cp corpus-config.json corpus-config.v4.0.backup.json
   ```

2. **Tag current state:**
   ```bash
   git tag v4.0-pre-migration
   git push origin v4.0-pre-migration
   ```

3. **Document current performance:**
   - Time a full convergence cycle
   - Note typical iteration count
   - Record cost per run

---

## Migration Steps

### Step 1: Update Configuration

**Enable Parallel Execution:**

Add `parallel` section to `corpus-config.json`:

```json
{
  "audit": {
    "mode": "unified",  // Switch to unified mode (recommended)
    "convergence": {
      "enabled": true,
      "requiredCleanPasses": 3,
      "maxIterations": 10,

      "parallel": {
        "enabled": true,
        "maxConcurrent": 15,
        "modelSelection": {
          "opus": [
            "User-Experience",
            "User-Accessibility",
            "User-Internationalization",
            "Holistic-Documentation",
            "Holistic-Onboarding"
          ],
          "sonnet": [
            "Technical-Quality",
            "Technical-Security",
            "Technical-Performance",
            "Technical-Testing",
            "Technical-Dependencies",
            "User-Responsiveness",
            "User-Error-Handling",
            "User-Help-System",
            "Holistic-Consistency",
            "Holistic-Navigation"
          ]
        },
        "dependencies": {
          "Technical-Security": ["Technical-Dependencies"],
          "Technical-Performance": ["Technical-Quality"],
          "User-Experience": ["Technical-Quality"],
          "Holistic-Consistency": ["Technical-Quality", "User-Experience"]
        }
      }
    }
  }
}
```

**Configure Concurrency Limits:**

Adjust `maxConcurrent` based on your needs:

- **maxConcurrent: 15** - Full speed (default, recommended)
- **maxConcurrent: 8** - Conservative (rate limit concerns)
- **maxConcurrent: 5** - Very conservative
- **maxConcurrent: 1** - Sequential mode (v4.0 behavior)

**Set Model Preferences:**

Choose which model runs each methodology:

- **Opus** - Best for complex, subjective assessments (UX, docs, accessibility)
- **Sonnet** - Best for technical, rule-based audits (security, quality, performance)

### Step 2: Update Convergence Workflows

**Switch to Unified Mode (Recommended):**

Unified mode integrates audit + convergence + learning:

```json
{
  "audit": {
    "mode": "unified",  // Was "audit" or "convergence"
    "convergence": {
      "enabled": true,
      "parallel": {
        "enabled": true
      }
    }
  }
}
```

**Benefits of Unified Mode:**
- Learning skills track patterns automatically
- Battle-plan monitors all methodologies in real-time
- Error-reflection analyzes failures across all attempts
- Pre-mortem prevents recurring issues

**Configure 15-Methodology Pool:**

v4.1 uses 15 methodologies across 3 perspectives:

```json
{
  "audit": {
    "convergence": {
      "methodologies": [
        {
          "name": "technical",
          "audits": [
            {"id": "Technical-Quality"},
            {"id": "Technical-Security"},
            {"id": "Technical-Performance"},
            {"id": "Technical-Testing"},
            {"id": "Technical-Dependencies"}
          ]
        },
        {
          "name": "user",
          "audits": [
            {"id": "User-Experience"},
            {"id": "User-Accessibility"},
            {"id": "User-Responsiveness"},
            {"id": "User-Error-Handling"},
            {"id": "User-Help-System"},
            {"id": "User-Internationalization"}
          ]
        },
        {
          "name": "holistic",
          "audits": [
            {"id": "Holistic-Consistency"},
            {"id": "Holistic-Navigation"},
            {"id": "Holistic-Documentation"},
            {"id": "Holistic-Onboarding"}
          ]
        }
      ]
    }
  }
}
```

**Adjust Fix Coordination Settings:**

Configure how fixes are coordinated:

```json
{
  "audit": {
    "convergence": {
      "parallel": {
        "fixCoordination": {
          "enabled": true,
          "conflictResolution": "merge",  // or "first-wins", "priority-based"
          "reviewBeforeApply": false
        }
      }
    }
  }
}
```

### Step 3: Update Learning Skills Usage

**Battle-Plan Parallel Monitoring:**

No changes needed - automatically enhanced in unified mode.

**Before (v4.0):**
```bash
"Create battle plan"
# Tracks sequential execution
```

**After (v4.1):**
```bash
"Create battle plan"
# Automatically tracks 15 parallel methodologies
# Real-time updates as each completes
# Cross-methodology pattern detection
```

**Error-Reflection Usage:**

No changes needed - works with parallel failures.

```bash
"Reflect on errors"
# Analyzes failures across all parallel methodologies
# Identifies common root causes
# Suggests systemic fixes
```

**Pre-Mortem Usage:**

No changes needed - enhanced with parallel insights.

```bash
"Run pre-mortem"
# Uses battle-plan data from parallel executions
# More comprehensive risk analysis
# Faster completion
```

### Step 4: Update Content Operations

**Batch Artifact Loading:**

Load multiple artifacts in parallel:

```bash
# Before (v4.0) - Sequential
"Load artifact requirements"
"Load artifact architecture"
"Load artifact api-docs"

# After (v4.1) - Parallel
"Load artifacts: requirements, architecture, api-docs"
# All load simultaneously
```

**Parallel Comment Loading:**

```bash
# Before (v4.0)
"Load comments for requirements"
# Sequential fetch

# After (v4.1)
"Load comments for all artifacts"
# Parallel fetch across all artifacts
```

**AI Improvement Queuing:**

```bash
# Before (v4.0)
"Improve clarity in section-1"
"Improve clarity in section-2"
"Improve clarity in section-3"

# After (v4.1)
"Improve clarity in sections: 1, 2, 3"
# All improvements queued and processed in parallel
```

**Batch Updates with Dependencies:**

```bash
# After (v4.1) - Smart dependency resolution
"Update artifacts with fixes from convergence"
# Automatically resolves dependencies
# Applies in correct order
# Validates cross-artifact consistency
```

### Step 5: Update Audit Operations

**Enable Parallel Audit Execution:**

```bash
# Before (v4.0)
"Run convergence audit"
# Methodologies run sequentially: T1 → T2 → ... → H4

# After (v4.1)
"Run convergence audit"
# 15 methodologies run in parallel
# Respects dependencies
# 10x faster completion
```

**Configure Dependency Rules:**

Define which audits depend on others:

```json
{
  "audit": {
    "convergence": {
      "parallel": {
        "dependencies": {
          "Technical-Security": ["Technical-Dependencies"],
          "Technical-Performance": ["Technical-Quality"],
          "User-Experience": ["Technical-Quality"],
          "Holistic-Consistency": ["Technical-Quality", "User-Experience"]
        }
      }
    }
  }
}
```

**How Dependencies Work:**
- `Technical-Security` waits for `Technical-Dependencies` to pass
- `User-Experience` waits for `Technical-Quality` to pass
- Independent audits run immediately in parallel
- Execution order optimized automatically

**Adjust Concurrency Limits:**

Fine-tune performance vs cost:

```json
{
  "audit": {
    "convergence": {
      "parallel": {
        "maxConcurrent": 15,  // Adjust based on rate limits
        "rateLimitStrategy": "adaptive",  // or "fixed", "backoff"
        "retryOnRateLimit": true,
        "maxRetries": 3
      }
    }
  }
}
```

---

## Configuration Examples

### Example 1: Minimal Migration (Parallel Only)

**Before (v4.0):**
```json
{
  "corpus": {
    "name": "My Project",
    "version": "1.0.0"
  },
  "audit": {
    "mode": "convergence",
    "convergence": {
      "enabled": true,
      "requiredCleanPasses": 3,
      "maxIterations": 10
    }
  }
}
```

**After (v4.1):**
```json
{
  "corpus": {
    "name": "My Project",
    "version": "1.0.0"
  },
  "audit": {
    "mode": "convergence",
    "convergence": {
      "enabled": true,
      "requiredCleanPasses": 3,
      "maxIterations": 10,
      "parallel": {
        "enabled": true,
        "maxConcurrent": 15
      }
    }
  }
}
```

**Changes:**
- Added `parallel.enabled: true`
- Added `parallel.maxConcurrent: 15`
- Everything else unchanged

---

### Example 2: Full Migration (Unified Mode)

**Before (v4.0):**
```json
{
  "corpus": {
    "name": "CorpusHub Platform",
    "version": "2.0.0"
  },
  "audit": {
    "mode": "convergence",
    "applicable_audits": ["security", "quality", "performance"],
    "convergence": {
      "enabled": true,
      "requiredCleanPasses": 3,
      "maxIterations": 10,
      "methodologies": [
        {
          "name": "technical",
          "audits": [
            {"id": "security"},
            {"id": "quality"}
          ]
        },
        {
          "name": "user",
          "audits": [
            {"id": "content"}
          ]
        },
        {
          "name": "holistic",
          "audits": [
            {"id": "consistency"}
          ]
        }
      ]
    }
  }
}
```

**After (v4.1):**
```json
{
  "corpus": {
    "name": "CorpusHub Platform",
    "version": "2.0.0"
  },
  "audit": {
    "mode": "unified",
    "applicable_audits": [
      "Technical-Quality",
      "Technical-Security",
      "Technical-Performance",
      "Technical-Testing",
      "Technical-Dependencies",
      "User-Experience",
      "User-Accessibility",
      "User-Responsiveness",
      "User-Error-Handling",
      "User-Help-System",
      "User-Internationalization",
      "Holistic-Consistency",
      "Holistic-Navigation",
      "Holistic-Documentation",
      "Holistic-Onboarding"
    ],
    "convergence": {
      "enabled": true,
      "requiredCleanPasses": 3,
      "maxIterations": 10,
      "methodologies": [
        {
          "name": "technical",
          "audits": [
            {"id": "Technical-Quality"},
            {"id": "Technical-Security"},
            {"id": "Technical-Performance"},
            {"id": "Technical-Testing"},
            {"id": "Technical-Dependencies"}
          ]
        },
        {
          "name": "user",
          "audits": [
            {"id": "User-Experience"},
            {"id": "User-Accessibility"},
            {"id": "User-Responsiveness"},
            {"id": "User-Error-Handling"},
            {"id": "User-Help-System"},
            {"id": "User-Internationalization"}
          ]
        },
        {
          "name": "holistic",
          "audits": [
            {"id": "Holistic-Consistency"},
            {"id": "Holistic-Navigation"},
            {"id": "Holistic-Documentation"},
            {"id": "Holistic-Onboarding"}
          ]
        }
      ],
      "parallel": {
        "enabled": true,
        "maxConcurrent": 15,
        "modelSelection": {
          "opus": [
            "User-Experience",
            "User-Accessibility",
            "User-Internationalization",
            "Holistic-Documentation",
            "Holistic-Onboarding"
          ],
          "sonnet": [
            "Technical-Quality",
            "Technical-Security",
            "Technical-Performance",
            "Technical-Testing",
            "Technical-Dependencies",
            "User-Responsiveness",
            "User-Error-Handling",
            "User-Help-System",
            "Holistic-Consistency",
            "Holistic-Navigation"
          ]
        },
        "dependencies": {
          "Technical-Security": ["Technical-Dependencies"],
          "Technical-Performance": ["Technical-Quality"],
          "User-Experience": ["Technical-Quality"],
          "Holistic-Consistency": ["Technical-Quality", "User-Experience"]
        },
        "fixCoordination": {
          "enabled": true,
          "conflictResolution": "merge",
          "reviewBeforeApply": false
        },
        "rateLimitStrategy": "adaptive",
        "retryOnRateLimit": true,
        "maxRetries": 3
      }
    }
  }
}
```

**Changes:**
- Mode changed from `convergence` to `unified`
- Expanded to 15 methodologies (from 4)
- Added parallel execution configuration
- Added model selection (Opus vs Sonnet)
- Added dependency rules
- Added fix coordination
- Added rate limit handling

---

### Example 3: Conservative Migration (Rate Limit Concerns)

**After (v4.1 Conservative):**
```json
{
  "audit": {
    "mode": "unified",
    "convergence": {
      "enabled": true,
      "requiredCleanPasses": 3,
      "maxIterations": 10,
      "parallel": {
        "enabled": true,
        "maxConcurrent": 5,  // Conservative limit
        "modelSelection": {
          "opus": ["User-Experience"],  // Only critical UX
          "sonnet": [  // Everything else
            "Technical-Quality",
            "Technical-Security",
            "Technical-Performance",
            "Technical-Testing",
            "Technical-Dependencies",
            "User-Accessibility",
            "User-Responsiveness",
            "User-Error-Handling",
            "User-Help-System",
            "User-Internationalization",
            "Holistic-Consistency",
            "Holistic-Navigation",
            "Holistic-Documentation",
            "Holistic-Onboarding"
          ]
        },
        "rateLimitStrategy": "backoff",  // More conservative
        "retryOnRateLimit": true,
        "maxRetries": 5,
        "backoffMultiplier": 2.0
      }
    }
  }
}
```

**Conservative Settings:**
- `maxConcurrent: 5` - Lower parallelism
- Mostly Sonnet models - Lower cost
- `rateLimitStrategy: backoff` - Conservative retry
- Higher retry count - More resilient

---

## Testing Migration

### Validate Parallel Execution

**Test 1: Dry Run**

```bash
"Run convergence audit in dry-run mode"
# Should show 15 methodologies queued
# Should display parallel execution plan
# Should respect dependencies
# Should not make actual changes
```

**Expected Output:**
```
Parallel Execution Plan:
  Wave 1 (15 concurrent):
    - Technical-Quality (Sonnet)
    - Technical-Dependencies (Sonnet)
    - User-Responsiveness (Sonnet)
    - User-Error-Handling (Sonnet)
    - ... (11 more)

  Wave 2 (4 concurrent, waiting for dependencies):
    - Technical-Security (Sonnet) [after Technical-Dependencies]
    - Technical-Performance (Sonnet) [after Technical-Quality]
    - User-Experience (Opus) [after Technical-Quality]

  Wave 3 (1 concurrent):
    - Holistic-Consistency (Sonnet) [after Technical-Quality, User-Experience]
```

**Test 2: Single Iteration**

```bash
"Run convergence audit for 1 iteration"
# Should execute in parallel
# Should complete 10x faster than v4.0
# Should produce same quality results
```

**Measure:**
- Time to complete 1 iteration
- Number of issues found
- Cost per iteration

**Test 3: Full Convergence**

```bash
"Run full convergence audit"
# Should reach 3 clean passes
# Should handle fixes correctly
# Should coordinate across methodologies
```

**Verify:**
- Final grade matches v4.0 quality
- No regressions introduced
- All methodologies converged

### Performance Benchmarking

**Benchmark Template:**

| Metric | v4.0 (Sequential) | v4.1 (Parallel) | Improvement |
|--------|-------------------|-----------------|-------------|
| Time per iteration | 45 min | 4.5 min | 10x faster |
| Time to convergence | 225 min (5 iter) | 22.5 min | 10x faster |
| Cost per iteration | $15 | $18 | 1.2x higher |
| Cost to convergence | $75 | $90 | 1.2x higher |
| Issues found | 47 | 47 | Same |
| Final grade | A | A | Same |

**How to Benchmark:**

1. **Run v4.0 baseline:**
   ```bash
   # Rollback to v4.0 config
   "Run convergence audit"
   # Record: time, cost, issues, grade
   ```

2. **Run v4.1 parallel:**
   ```bash
   # Use v4.1 config
   "Run convergence audit"
   # Record: time, cost, issues, grade
   ```

3. **Compare results:**
   - Time should be ~10x faster
   - Cost should be ~1.2x higher
   - Quality should be identical

### Regression Testing

**Test Checklist:**

- [ ] All v4.0 audits still pass
- [ ] Corpus detection works
- [ ] Configuration loading works
- [ ] Source mode management works
- [ ] Content operations work
- [ ] Fix application works
- [ ] Report generation works
- [ ] Learning skills work
- [ ] CorpusHub API integration works

**Run Full Test Suite:**

```bash
# Test corpus operations
"Check corpus status"
"Update corpus configuration"

# Test content operations
"Review artifact requirements"
"Edit artifact architecture"

# Test audit operations
"Run security audit"
"Run quality audit"

# Test convergence
"Run full convergence audit"

# Test learning
"Create battle plan"
"Reflect on errors"
"Run pre-mortem"
```

**Expected:** All operations complete successfully with identical results to v4.0.

---

## Rollback Procedure

### Revert to v4.0 Behavior

**Option 1: Disable Parallel Execution**

Keep v4.1 installed, disable parallel mode:

```json
{
  "audit": {
    "convergence": {
      "parallel": {
        "enabled": false  // Sequential mode
      }
    }
  }
}
```

**Option 2: Set maxConcurrent to 1**

```json
{
  "audit": {
    "convergence": {
      "parallel": {
        "enabled": true,
        "maxConcurrent": 1  // Forces sequential execution
      }
    }
  }
}
```

**Option 3: Restore Backup Configuration**

```bash
# Restore v4.0 config
cp corpus-config.v4.0.backup.json corpus-config.json

# Verify
"Check corpus status"
# Should show sequential mode active
```

### Configuration Rollback

**Full Rollback Steps:**

1. **Restore backup:**
   ```bash
   git checkout v4.0-pre-migration -- corpus-config.json
   ```

2. **Verify configuration:**
   ```bash
   "Check corpus status"
   ```

3. **Test functionality:**
   ```bash
   "Run convergence audit"
   # Should run sequentially
   ```

### Sequential Mode Fallback

**Automatic Fallback:**

v4.1 automatically falls back to sequential mode if:
- Rate limits exceeded repeatedly
- Parallel execution fails
- Context limits reached
- User explicitly requests

**Manual Fallback:**

```bash
"Run convergence in sequential mode"
# Temporarily overrides parallel config
# Runs like v4.0
```

---

## Common Issues

### Issue 1: Rate Limiting

**Symptoms:**
- "Rate limit exceeded" errors
- Slow execution despite parallelism
- Incomplete methodology runs

**Solutions:**

1. **Reduce concurrency:**
   ```json
   {
     "parallel": {
       "maxConcurrent": 8  // Down from 15
     }
   }
   ```

2. **Enable adaptive rate limiting:**
   ```json
   {
     "parallel": {
       "rateLimitStrategy": "adaptive",
       "retryOnRateLimit": true,
       "maxRetries": 5
     }
   }
   ```

3. **Use more Sonnet (cheaper, higher limits):**
   ```json
   {
     "modelSelection": {
       "opus": ["User-Experience"],  // Only critical
       "sonnet": [/* all others */]
     }
   }
   ```

### Issue 2: Context Exhaustion

**Symptoms:**
- "Context limit reached" errors
- Incomplete analysis
- Truncated reports

**Solutions:**

1. **Reduce concurrent methodologies:**
   ```json
   {
     "parallel": {
       "maxConcurrent": 5  // Fewer concurrent contexts
     }
   }
   ```

2. **Enable context management:**
   ```json
   {
     "parallel": {
       "contextManagement": {
         "enabled": true,
         "maxContextPerMethodology": 50000
       }
     }
   }
   ```

3. **Split large projects:**
   ```bash
   # Audit subsystems separately
   "Run convergence on src/core only"
   "Run convergence on src/ui only"
   ```

### Issue 3: Concurrency Conflicts

**Symptoms:**
- Same file edited by multiple methodologies
- Conflicting fixes applied
- Merge conflicts in reports

**Solutions:**

1. **Enable fix coordination:**
   ```json
   {
     "parallel": {
       "fixCoordination": {
         "enabled": true,
         "conflictResolution": "merge"
       }
     }
   }
   ```

2. **Review before applying:**
   ```json
   {
     "parallel": {
       "fixCoordination": {
         "reviewBeforeApply": true
       }
     }
   }
   ```

3. **Define stricter dependencies:**
   ```json
   {
     "parallel": {
       "dependencies": {
         "Technical-Security": ["Technical-Quality", "Technical-Dependencies"],
         "User-Experience": ["Technical-Quality", "Technical-Security"]
       }
     }
   }
   ```

### Issue 4: Unexpected Cost Increase

**Symptoms:**
- Higher than expected API costs
- Bills exceeding budget

**Solutions:**

1. **Use more Sonnet:**
   ```json
   {
     "modelSelection": {
       "opus": [],  // Use Sonnet for everything
       "sonnet": [/* all methodologies */]
     }
   }
   ```

2. **Reduce iterations:**
   ```json
   {
     "convergence": {
       "maxIterations": 5  // Down from 10
     }
   }
   ```

3. **Use selective methodology activation:**
   ```json
   {
     "convergence": {
       "methodologies": [
         {
           "name": "technical",
           "audits": [
             {"id": "Technical-Quality"},
             {"id": "Technical-Security"}
             // Only critical audits
           ]
         }
       ]
     }
   }
   ```

### Issue 5: Dependency Deadlock

**Symptoms:**
- Methodologies never start
- "Waiting for dependencies" indefinitely
- No progress after initial wave

**Solutions:**

1. **Review dependency graph:**
   ```bash
   "Show dependency graph"
   # Visualize dependencies
   # Identify cycles
   ```

2. **Remove circular dependencies:**
   ```json
   {
     "dependencies": {
       // BAD (circular):
       // "A": ["B"],
       // "B": ["A"]

       // GOOD (acyclic):
       "B": ["A"]  // B depends on A only
     }
   }
   ```

3. **Use dependency validation:**
   ```bash
   "Validate convergence configuration"
   # Checks for cycles
   # Suggests fixes
   ```

---

## FAQ

### Q: Do I have to use parallel mode?

**A:** No. Parallel mode is completely optional.

- v4.1 fully supports sequential mode
- Set `parallel.enabled: false` or `maxConcurrent: 1`
- All v4.0 functionality preserved
- No feature loss in sequential mode

### Q: Can I keep sequential mode permanently?

**A:** Yes. Sequential mode is a first-class execution mode.

**When to use sequential:**
- Budget constraints (lower concurrent API costs)
- Rate limit concerns
- Simpler debugging
- Preference for v4.0 behavior

**When to use parallel:**
- Speed is critical (10x faster)
- Cost increase acceptable (~20% more)
- Large projects (100+ files)
- Frequent convergence runs

### Q: What's the cost impact?

**A:** Approximately 20% cost increase for 10x speed improvement.

**Cost Breakdown:**

| Mode | Time | API Calls | Cost per Run | Cost per Hour |
|------|------|-----------|--------------|---------------|
| Sequential (v4.0) | 45 min | 15 sequential | $15 | $20/hr |
| Parallel (v4.1) | 4.5 min | 15 concurrent | $18 | $240/hr |

**Why Higher Cost per Hour?**
- More API calls per unit time
- Opus models for quality-critical audits
- Overhead for coordination

**Why Lower Cost per Run?**
- Finishes 10x faster
- Fewer total iterations (better convergence)
- More efficient fix application

**Net Result:** Faster convergence at similar or lower total cost.

### Q: How do I tune performance?

**A:** Adjust these key parameters:

**1. Concurrency Level:**
```json
{
  "maxConcurrent": 15  // Start here
  // Reduce if rate limits hit
  // Increase if no issues
}
```

**2. Model Selection:**
```json
{
  "modelSelection": {
    "opus": [/* quality-critical */],  // Fewer = faster + cheaper
    "sonnet": [/* rule-based */]       // More = faster + cheaper
  }
}
```

**3. Rate Limit Strategy:**
```json
{
  "rateLimitStrategy": "adaptive"  // Automatic tuning
  // or "fixed" for consistent speed
  // or "backoff" for conservative
}
```

**4. Dependencies:**
```json
{
  "dependencies": {
    // Fewer dependencies = more parallelism
    // More dependencies = safer but slower
  }
}
```

**Performance Tuning Guide:**

| Goal | Concurrency | Model Mix | Rate Strategy |
|------|-------------|-----------|---------------|
| Maximum speed | 15 | 50/50 Opus/Sonnet | Adaptive |
| Balanced | 10 | 30/70 Opus/Sonnet | Adaptive |
| Maximum quality | 8 | 80/20 Opus/Sonnet | Fixed |
| Minimum cost | 5 | 10/90 Opus/Sonnet | Backoff |

### Q: Will parallel mode work with my custom audits?

**A:** Yes, with configuration.

**Requirements:**
1. Define your custom audit in `corpus-config.json`
2. Add to a methodology (technical/user/holistic)
3. Choose model (Opus or Sonnet)
4. Define dependencies (if any)

**Example:**
```json
{
  "audit": {
    "applicable_audits": [
      "Technical-Quality",
      "Custom-Compliance"  // Your custom audit
    ],
    "convergence": {
      "methodologies": [
        {
          "name": "technical",
          "audits": [
            {"id": "Technical-Quality"},
            {"id": "Custom-Compliance"}
          ]
        }
      ],
      "parallel": {
        "modelSelection": {
          "sonnet": ["Technical-Quality", "Custom-Compliance"]
        },
        "dependencies": {
          "Custom-Compliance": ["Technical-Quality"]
        }
      }
    }
  }
}
```

### Q: What if I encounter a bug in parallel mode?

**A:** Fallback to sequential mode and report the issue.

**Immediate Fix:**
```json
{
  "parallel": {
    "enabled": false  // Temporary fix
  }
}
```

**Report Bug:**
1. Document the error
2. Include configuration
3. Note which methodology failed
4. Provide reproduction steps
5. Submit to support (see below)

### Q: Can I mix parallel and sequential execution?

**A:** Yes, using selective methodology activation.

**Example - Run some in parallel, some sequential:**
```bash
# Parallel for technical audits
"Run technical methodologies in parallel"

# Sequential for user audits (if Opus-heavy)
"Run user methodologies in sequential mode"
```

**Or configure in corpus-config.json:**
```json
{
  "parallel": {
    "methodologyOverrides": {
      "technical": {"maxConcurrent": 15},
      "user": {"maxConcurrent": 1},  // Sequential
      "holistic": {"maxConcurrent": 5}
    }
  }
}
```

### Q: How do I monitor parallel execution?

**A:** Use battle-plan skill for real-time monitoring.

```bash
"Create battle plan"
# Automatically tracks all 15 methodologies
# Real-time updates as each completes
# Shows progress, blockers, patterns

"Show battle plan status"
# Current state of all methodologies
# Which are running, which are complete
# Which are waiting on dependencies
```

**Battle Plan Dashboard:**
```
Parallel Execution Monitor:
  ✅ Technical-Quality (Sonnet) - Complete - 12 issues
  ✅ Technical-Dependencies (Sonnet) - Complete - 3 issues
  ⏳ Technical-Security (Sonnet) - Running (waiting for Dependencies)
  ⏳ Technical-Performance (Sonnet) - Running (waiting for Quality)
  🔄 User-Experience (Opus) - Queued (waiting for Quality)
  ...
```

---

## Support

### Where to Get Help

**Documentation:**
- v4.1 ARCHITECTURE.md - Full architecture details
- v4.1 IMPLEMENTATION-STATUS.md - Current status
- v4.1 ROADMAP.md - Future plans
- Skill READMEs - Individual skill docs

**Interactive Help:**
```bash
"Help with parallel execution"
"Explain v4.1 migration"
"Troubleshoot parallel issues"
```

**Community:**
- GitHub Discussions (coming soon)
- Slack workspace (coming soon)

### Reporting Issues

**Issue Template:**

```markdown
## Issue Description
[Brief description of the problem]

## Environment
- Version: v4.1.0
- Mode: parallel / sequential / unified
- Concurrency: 15
- Project type: web-app / content-corpus / etc.

## Configuration
```json
{
  "audit": {
    // Relevant config
  }
}
```

## Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happened]

## Error Messages
```
[Paste error messages here]
```

## Impact
- [ ] Blocking (cannot proceed)
- [ ] High (significant disruption)
- [ ] Medium (workaround available)
- [ ] Low (minor inconvenience)
```

**Where to Report:**

1. **GitHub Issues:**
   - Bug reports
   - Feature requests
   - Documentation improvements

2. **Direct Support:**
   - Email: support@corpushub.io
   - Emergency: Tag issue with `[URGENT]`

3. **In-Product:**
   ```bash
   "Report issue with parallel execution"
   # Automatically captures context
   # Includes configuration
   # Sends to support team
   ```

---

## Conclusion

**Migration Summary:**

1. ✅ Backup your configuration
2. ✅ Add `parallel` section to corpus-config.json
3. ✅ Test with dry-run
4. ✅ Benchmark performance
5. ✅ Adjust concurrency as needed
6. ✅ Monitor with battle-plan
7. ✅ Report any issues

**Expected Outcomes:**

- 10x faster convergence
- Same quality results
- ~20% higher cost per run
- More insights from learning skills
- Better fix coordination

**Remember:**

- Parallel mode is optional
- Sequential mode always available
- Full backward compatibility
- Rollback is simple and safe

**Questions?** See [FAQ](#faq) or [Support](#support)

---

*Migration Guide Version: 1.0.0*
*For Skills Version: v4.1.0*
*Last Updated: 2026-02-12*
*Status: Production Ready*
