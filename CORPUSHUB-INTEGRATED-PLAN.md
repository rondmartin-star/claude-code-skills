# v4.0 Reorganization: CorpusHub Integration

**Date:** 2026-01-31
**Purpose:** Align skills ecosystem with actual CorpusHub implementation
**Status:** UPDATED - Based on CorpusHub production documentation

---

## Key Discoveries from CorpusHub Docs

### 1. Actual corpus-config.json Schema (Production)

Our original plan had a simplified schema. The **actual** CorpusHub schema is more sophisticated:

```json
{
  "corpus": {
    "name": "My Corpus",
    "description": "Brief description",
    "version": "1.0.0",
    "baseDir": "/absolute/path/to/corpus"
  },

  "artifacts": {
    "artifact-slug": {
      "path": "relative/path/from/baseDir",
      "label": "Human-readable label",
      "extensions": [".md", ".html"]
    }
  },

  "framework": {
    "categories": [
      {
        "id": "unique-id",
        "label": "Category Name",
        "terms": ["Canonical Term 1", "Canonical Term 2"],
        "canonicalSource": "artifact-type-slug",
        "matchMode": "case-insensitive" | "word-boundary" | "exact"
      }
    ]
  },

  "voice": {
    "promptFile": "path/to/system-prompt.md",
    "attributes": ["professional", "technical"],
    "avoid": ["jargon", "marketing speak"],
    "preferredTerms": {
      "Use This": "Not This"
    }
  },

  "roles": {
    "available": ["admin", "editor", "viewer", "pending"],
    "defaultRole": "pending",
    "aiAccess": ["admin", "editor"],
    "editAccess": ["admin", "editor"]
  },

  "consistency": {
    "enabled": true,
    "scanDirectories": ["docs/", "specifications/"]
  }
}
```

**Key Differences from Our Draft:**
- ✅ `artifacts` is an **object** (not array), keys are slugs
- ✅ `framework.categories` instead of flat `framework_terms`
- ✅ `matchMode` for term matching (case-insensitive, word-boundary, exact)
- ✅ `voice` section with AI guidance
- ✅ `roles` with granular permissions (aiAccess, editAccess)
- ✅ `consistency` configuration

### 2. Multi-Methodology Audit Framework (Proven)

CorpusHub has a **proven multi-methodology audit framework** (the "3-3-1 Rule"):

**3 Methodologies (Run in Parallel):**
1. **Technical/Internal** - Code, architecture, implementation
2. **User/External** - UX, flows, accessibility
3. **Holistic/Meta** - Documentation, completeness, consistency

**3 Iterations (Minimum):**
1. **Discovery** (2-4 hours) - Find 60-80% of issues, fix critical/high
2. **Verification** (1-2 hours) - Verify fixes, catch gaps, find 20-30% more
3. **Stabilization** (0.5-1 hour) - Final check, confirm 0 critical/high

**1 User Validation (Essential):**
- Real users, real environment, real workflows, real data
- **Critical:** Even after 3 clean iterations, user testing finds issues

**Proven Results:**
- CorpusHub Security Audit: F → A grade in 5 hours
- 23 issues found (vs. ~8 with single methodology)
- $27,600+ savings (pre-production fixes vs. post-production)
- ROI: 25x to 2,000x

**This is MORE sophisticated than our simple "3 clean passes" convergence.**

### 3. Bidirectional Architecture (Source Modes)

CorpusHub supports **three modes of source-of-truth**:

**Mode 1: `source_of_truth = 'corpus'`**
- Traditional file: None (or deleted)
- Corpus HTML: Source of truth
- Use for: Requirements, design docs, ADRs
- Edit in CorpusHub, store in corpus/ directory

**Mode 2: `source_of_truth = 'source'`**
- Traditional file: Source of truth (edited in IDE)
- Corpus HTML: Generated, read-only
- Use for: Implementation code, config files
- Edit in IDE, corpus HTML auto-regenerated
- File watcher detects changes, triggers regeneration

**Mode 3: `source_of_truth = 'bidirectional'`**
- Both traditional file AND corpus HTML editable
- Automatic bidirectional sync
- Use for: Documentation (README, guides, API docs)
- Edit either location, both stay in sync
- File watcher temporarily disabled during sync to prevent loops

**This pattern was NOT in our original plan - we need to incorporate it.**

### 4. Corpus Detection API (Production-Ready)

CorpusHub has a comprehensive **corpus detection utility**:

**API Endpoints:**
- `GET /api/corpora/detect?path=/path` - Detect corpus status
- `POST /api/corpora/validate` - Validate config without registering
- `GET /api/corpora/registration-status?path=/path` - Check registration
- `GET /api/corpora/:slug/health` - Comprehensive health check

**Detection Checks:**
- configExists, configValid, isRegistered
- infrastructureExists, databaseExists
- bitCount, fileCount, edgeCount
- Issues and suggestions

**CLI Tool:**
```bash
node scripts/detect-corpus.js /path/to/project
node scripts/detect-corpus.js /path/to/project --json
node scripts/detect-corpus.js --health corpus-slug
```

**This is production-ready and should be incorporated into corpus-init.**

---

## Updated Architecture: Aligned with CorpusHub

### Updated corpus-config.json Template

```json
{
  "corpus": {
    "name": "Project Name",
    "description": "Brief description",
    "version": "1.0.0",
    "baseDir": "/absolute/path/to/project"
  },

  "artifacts": {
    "source-code": {
      "path": "src",
      "label": "Source Code",
      "extensions": [".js", ".ts", ".py"],
      "sourceMode": "source"
    },
    "requirements": {
      "path": "docs/requirements",
      "label": "Requirements",
      "extensions": [".html", ".md"],
      "sourceMode": "corpus"
    },
    "documentation": {
      "path": "docs",
      "label": "Documentation",
      "extensions": [".md"],
      "sourceMode": "bidirectional"
    }
  },

  "framework": {
    "categories": [
      {
        "id": "core-concepts",
        "label": "Core Concepts",
        "terms": ["Authentication", "Authorization", "Session Management"],
        "canonicalSource": "requirements",
        "matchMode": "word-boundary"
      },
      {
        "id": "architecture",
        "label": "Architecture Patterns",
        "terms": ["MVC", "Repository Pattern", "Service Layer"],
        "matchMode": "case-insensitive"
      }
    ]
  },

  "voice": {
    "promptFile": "docs/system-prompt.md",
    "attributes": ["professional", "technical", "clear"],
    "avoid": ["jargon without explanation", "marketing speak"],
    "preferredTerms": {
      "OAuth 2.0 with cookie separation": "OAuth",
      "Parameterized queries": "SQL queries"
    }
  },

  "roles": {
    "available": ["admin", "editor", "reviewer", "viewer", "pending"],
    "defaultRole": "pending",
    "aiAccess": ["admin", "editor"],
    "editAccess": ["admin", "editor"]
  },

  "consistency": {
    "enabled": true,
    "scanDirectories": ["src/", "docs/", "requirements/"]
  },

  "audit": {
    "methodology": "multi-methodology-3-3-1",
    "applicable_audits": ["security", "quality", "performance"],
    "convergence": {
      "enabled": true,
      "methodologies": [
        {
          "name": "technical",
          "audits": ["security-architecture", "code-quality", "performance-profiling"]
        },
        {
          "name": "user",
          "audits": ["auth-flow-testing", "ux-performance", "accessibility"]
        },
        {
          "name": "holistic",
          "audits": ["documentation", "dependency-audit", "consistency"]
        }
      ],
      "iterations": {
        "minimum": 3,
        "max": 10,
        "discovery": {
          "time_budget": "2-4 hours",
          "fix_priority": ["critical", "high"]
        },
        "verification": {
          "time_budget": "1-2 hours",
          "fix_priority": ["medium", "high"]
        },
        "stabilization": {
          "time_budget": "0.5-1 hour",
          "success_criteria": {
            "critical": 0,
            "high": 0,
            "medium": "<3"
          }
        }
      },
      "user_validation": {
        "required": true,
        "tests": ["real_users", "real_environment", "real_workflows", "real_data"]
      }
    }
  }
}
```

### Updated Core Patterns

#### core/corpus/ (UPDATED)

```
core/corpus/
├── corpus-init/                # Initialize new corpus
│   └── SKILL.md               # Uses detection API, creates proper schema
│
├── corpus-convert/            # Convert existing project
│   └── SKILL.md              # Detects existing infrastructure
│
├── corpus-detect/             # Corpus detection (NEW)
│   └── SKILL.md              # Wrapper for CorpusHub detection API
│
├── corpus-config/             # Configuration management
│   └── SKILL.md              # Validate and manage corpus-config.json
│
├── source-mode-manager/       # Manage source modes (NEW)
│   └── SKILL.md              # Handle corpus/source/bidirectional modes
│
└── corpus-orchestrator/       # Route corpus operations
    └── SKILL.md              # Detect intent, load appropriate skill
```

#### core/audit/ (UPDATED with 3-3-1 Rule)

```
core/audit/
├── audit-orchestrator/         # Route to applicable audits
│   └── SKILL.md               # Project type detection, routing
│
├── convergence-engine/         # Multi-methodology 3-3-1 (UPDATED)
│   └── SKILL.md               # 3 methodologies × 3 iterations × 1 validation
│
├── fix-planner/               # Generate and execute fix plans
│   └── SKILL.md              # Auto-fix strategies
│
└── methodologies/             # Audit methodologies (NEW)
    ├── technical/             # Technical/Internal perspective
    │   ├── security-architecture/
    │   ├── code-quality/
    │   └── performance-profiling/
    │
    ├── user/                  # User/External perspective
    │   ├── auth-flow-testing/
    │   ├── ux-performance/
    │   └── accessibility/
    │
    └── holistic/              # Holistic/Meta perspective
        ├── documentation/
        ├── dependency-audit/
        └── consistency/
```

---

## Updated Convergence Algorithm (3-3-1 Rule)

```javascript
async function multiMethodologyConvergence(projectConfig) {
  const results = {
    convergenceCycles: [],
    finalStatus: null
  };

  let convergenceCycle = 0;
  let userValidationClean = false;
  const maxCycles = 5; // Max convergence → user test cycles

  // OUTER LOOP: Convergence → User Validation cycles
  while (!userValidationClean && convergenceCycle < maxCycles) {
    convergenceCycle++;

    const cycle = {
      cycleNumber: convergenceCycle,
      automatedConvergence: null,
      userValidation: null
    };

    console.log(`\n=== Convergence Cycle ${convergenceCycle} ===`);

    // ============================================
    // PHASE 1: AUTOMATED CONVERGENCE (Gate)
    // ============================================
    console.log('\nPhase 1: Automated Convergence');

    const automatedResult = await runAutomatedConvergence(projectConfig);
    cycle.automatedConvergence = automatedResult;

    if (automatedResult.status !== 'CONVERGED') {
      // Failed to converge with automated audits
      cycle.userValidation = { skipped: true, reason: 'Automated convergence failed' };
      results.convergenceCycles.push(cycle);
      results.finalStatus = 'FAILED - Automated convergence incomplete';
      break;
    }

    console.log('✓ Automated convergence complete (3 clean passes)');

    // ============================================
    // PHASE 2: USER VALIDATION (After clean system)
    // ============================================
    console.log('\nPhase 2: User Validation (testing clean system)');

    const userResult = await runUserValidation(projectConfig);
    cycle.userValidation = userResult;

    if (userResult.issues.length === 0) {
      // SUCCESS: Both automated and user validation clean
      userValidationClean = true;
      console.log('✓ User validation clean');
      results.finalStatus = 'PRODUCTION READY';
    } else {
      // User found issues - back to automated convergence
      console.warn(`⚠ User validation found ${userResult.issues.length} issues`);
      console.log('→ Returning to automated convergence...');
    }

    results.convergenceCycles.push(cycle);
  }

  if (convergenceCycle >= maxCycles && !userValidationClean) {
    results.finalStatus = 'MAX CYCLES - Manual review required';
  }

  return results;
}

/**
 * Run automated convergence until 3 consecutive clean passes
 * This is the GATE before user testing
 */
async function runAutomatedConvergence(projectConfig) {
  const convergenceResult = {
    iterations: [],
    status: null,
    consecutiveCleanPasses: 0
  };

  // Load 3 methodologies based on project type
  const methodologies = selectMethodologies(projectConfig.type);

  let iteration = 0;
  let consecutiveCleanPasses = 0;
  const maxIterations = projectConfig.audit.convergence.iterations.max || 10;

  // INNER LOOP: Automated audit iterations
  while (consecutiveCleanPasses < 3 && iteration < maxIterations) {
    iteration++;

    const iterationResult = {
      number: iteration,
      phase: iteration === 1 ? 'discovery' : iteration === 2 ? 'verification' : 'stabilization',
      methodologyResults: [],
      totalIssues: 0,
      fixesApplied: 0
    };

    console.log(`  Iteration ${iteration} (${iterationResult.phase})...`);

    // Run all 3 methodologies in parallel
    const methodologyPromises = methodologies.map(async (methodology) => {
      const audits = projectConfig.audit.convergence.methodologies
        .find(m => m.name === methodology).audits;

      const auditsResults = [];
      for (const audit of audits) {
        const result = await runAudit(audit, projectConfig);
        auditsResults.push(result);
      }

      return {
        methodology,
        audits: auditsResults,
        issues: auditsResults.flatMap(r => r.issues)
      };
    });

    const methodologyResults = await Promise.all(methodologyPromises);
    iterationResult.methodologyResults = methodologyResults;

    // Aggregate all issues
    const allIssues = methodologyResults.flatMap(m => m.issues);
    iterationResult.totalIssues = allIssues.length;

    // Check if clean
    if (allIssues.length === 0) {
      consecutiveCleanPasses++;
      iterationResult.status = `Clean pass ${consecutiveCleanPasses}/3`;
      convergenceResult.iterations.push(iterationResult);
      console.log(`  ✓ Clean pass ${consecutiveCleanPasses}/3`);
      continue;
    } else {
      consecutiveCleanPasses = 0; // Reset on any issues
      console.log(`  Found ${allIssues.length} issues`);
    }

    // Prioritize based on phase
    const fixPriority = projectConfig.audit.convergence.iterations[
      iterationResult.phase
    ].fix_priority;

    const issuesToFix = prioritizeIssues(allIssues, fixPriority);

    // Generate fix plan
    const plan = await generateFixPlan(issuesToFix);

    // Get user approval for fixes (optional)
    if (projectConfig.audit.convergence.approval_required) {
      const approved = await getUserApproval(plan);
      if (!approved) {
        iterationResult.status = 'User aborted';
        convergenceResult.iterations.push(iterationResult);
        convergenceResult.status = 'ABORTED';
        return convergenceResult;
      }
    }

    // Implement fixes
    const fixResults = await implementFixes(plan);
    iterationResult.fixesApplied = fixResults.successful;
    iterationResult.fixesFailed = fixResults.failed;
    console.log(`  Fixed ${fixResults.successful}/${issuesToFix.length} issues`);

    convergenceResult.iterations.push(iterationResult);
  }

  // Determine convergence status
  if (consecutiveCleanPasses >= 3) {
    convergenceResult.status = 'CONVERGED';
    convergenceResult.consecutiveCleanPasses = 3;
  } else if (iteration >= maxIterations) {
    convergenceResult.status = 'MAX ITERATIONS';
  }

  return convergenceResult;
}

function selectMethodologies(projectType) {
  const methodologyMap = {
    'web-app': ['technical', 'user', 'holistic'],
    'content-corpus': ['holistic', 'user', 'technical'],
    'framework-docs': ['holistic', 'technical', 'user'],
    'windows-app': ['technical', 'user', 'holistic']
  };

  return methodologyMap[projectType] || ['technical', 'user', 'holistic'];
}
```

---

## Integration Points Updated

### 1. corpus-init → CorpusHub Detection API

```javascript
// core/corpus/corpus-init/implementation.js

async function initializeCorpus(projectPath) {
  // Use CorpusHub detection API
  const detectionResponse = await fetch(
    `http://localhost:3000/api/corpora/detect?path=${encodeURIComponent(projectPath)}`
  );

  const status = await detectionResponse.json();

  if (status.isCorpusEnabled) {
    console.log(`⚠️  Corpus already enabled: ${status.config.name}`);

    const choice = await askUser('What would you like to do?', [
      'Update configuration',
      'Re-initialize (overwrites)',
      'Cancel'
    ]);

    if (choice === 'Cancel') return;
    if (choice === 'Update configuration') {
      // Open config editor
      return await editCorpusConfig(projectPath);
    }
  }

  // Auto-detect project type
  const projectType = await detectProjectType(projectPath);

  // Load template
  const template = await loadConfigTemplate(projectType);

  // Customize template
  template.corpus.name = await detectProjectName(projectPath);
  template.corpus.baseDir = path.resolve(projectPath);
  template.artifacts = await detectArtifacts(projectPath);

  // Write corpus-config.json
  await writeConfig(projectPath, template);

  // Register with CorpusHub
  await registerCorpus(template);

  // Create infrastructure
  await createCorpusInfrastructure(projectPath, template);

  console.log('✅ Corpus initialized successfully');
  console.log(`   Name: ${template.corpus.name}`);
  console.log(`   Artifacts: ${Object.keys(template.artifacts).length} types`);
}
```

### 2. Source Mode Manager (NEW)

```javascript
// core/corpus/source-mode-manager/implementation.js

async function setupSourceMode(artifactType, config) {
  const artifact = config.artifacts[artifactType];
  const sourceMode = artifact.sourceMode || 'bidirectional';

  switch (sourceMode) {
    case 'corpus':
      // Corpus is source of truth
      await setupCorpusSourceMode(artifactType, config);
      break;

    case 'source':
      // Traditional file is source of truth
      await setupSourceSourceMode(artifactType, config);
      break;

    case 'bidirectional':
      // Both stay in sync
      await setupBidirectionalMode(artifactType, config);
      break;
  }
}

async function setupBidirectionalMode(artifactType, config) {
  const artifact = config.artifacts[artifactType];
  const traditionalPath = path.join(config.corpus.baseDir, artifact.path);
  const corpusPath = path.join(config.corpus.baseDir, 'corpus', artifactType);

  // Set up file watcher
  const watcher = chokidar.watch(traditionalPath, {
    ignored: /^\./,
    persistent: true
  });

  watcher.on('change', async (filePath) => {
    console.log(`Traditional file changed: ${filePath}`);

    // Regenerate corpus HTML
    await convertToCorpusHTML(filePath, corpusPath);

    // Notify CorpusHub clients via SSE
    await notifyClients({
      type: 'bit_updated',
      artifactType,
      path: filePath
    });
  });

  // Set up corpus save handler
  app.post('/api/artifacts/:type/:name', async (req, res) => {
    const { type, name } = req.params;
    const { content } = req.body;

    // Save corpus HTML
    await saveCorpusHTML(type, name, content);

    // Convert back to traditional file
    watcher.unwatch(traditionalPath); // Prevent loop
    await convertFromCorpusHTML(content, traditionalPath);
    await wait(1000); // Wait for file system
    watcher.add(traditionalPath); // Re-enable

    res.json({ success: true });
  });
}
```

### 3. Multi-Methodology Audit Configuration

```json
// config/templates/web-app.json

{
  "audit": {
    "methodology": "multi-methodology-3-3-1",
    "convergence": {
      "enabled": true,
      "methodologies": [
        {
          "name": "technical",
          "description": "How it works - code, architecture, implementation",
          "audits": [
            {
              "id": "security-architecture",
              "config": {
                "checks": ["https", "oauth", "csrf", "xss", "sql_injection"]
              }
            },
            {
              "id": "code-quality",
              "config": {
                "min_coverage": 80,
                "max_complexity": 10
              }
            },
            {
              "id": "performance-profiling",
              "config": {
                "max_bundle_kb": 500,
                "max_load_ms": 3000
              }
            }
          ]
        },
        {
          "name": "user",
          "description": "How it's experienced - UX, flows, accessibility",
          "audits": [
            {
              "id": "auth-flow-testing",
              "config": {
                "test_scenarios": ["login", "logout", "signup", "password_reset"]
              }
            },
            {
              "id": "ux-performance",
              "config": {
                "metrics": ["lcp", "fid", "cls"],
                "thresholds": {"lcp": 2500, "fid": 100, "cls": 0.1}
              }
            },
            {
              "id": "accessibility",
              "config": {
                "wcag_level": "AA",
                "tools": ["axe", "lighthouse"]
              }
            }
          ]
        },
        {
          "name": "holistic",
          "description": "How it fits together - docs, completeness, consistency",
          "audits": [
            {
              "id": "documentation",
              "config": {
                "required": ["README", "API_DOCS", "DEPLOYMENT_GUIDE"]
              }
            },
            {
              "id": "dependency-audit",
              "config": {
                "tools": ["npm_audit", "snyk"]
              }
            },
            {
              "id": "consistency",
              "config": {
                "canonical_source": "corpus-config.json",
                "scan_directories": ["src/", "docs/"]
              }
            }
          ]
        }
      ]
    }
  }
}
```

---

## Updated Migration Plan

### Phase 1: Core Patterns (Weeks 1-2) - UPDATED

**Deliverables:**
- ✅ core/corpus/corpus-init/ (with CorpusHub detection API)
- ✅ core/corpus/corpus-detect/ (wrapper for detection API)
- ✅ core/corpus/source-mode-manager/ (bidirectional architecture)
- ✅ core/audit/convergence-engine/ (3-3-1 methodology)
- core/content/review-edit-author/
- core/utilities/backup-restore/

**Updated corpus-init:**
- Use `/api/corpora/detect` before initialization
- Generate proper corpus-config.json with all sections
- Support source modes (corpus, source, bidirectional)
- Register with CorpusHub after creation

**Updated convergence-engine:**
- Implement 3 methodologies (technical, user, holistic)
- 3 iterations minimum (discovery, verification, stabilization)
- Required user validation after convergence
- Time budgets per phase
- Cross-methodology issue correlation

### Phase 2: Configuration Templates (Weeks 3-4) - UPDATED

**Deliverables:**
- config/templates/web-app.json (with 3-3-1 audit config)
- config/templates/content-corpus.json
- config/templates/framework-docs.json
- config/templates/windows-app.json
- config/examples/corpushub-config.json (real example from CorpusHub)

**Template Structure:**
- Proper `corpus`, `artifacts`, `framework`, `voice`, `roles` sections
- Artifact definitions with `sourceMode`
- Framework categories with `matchMode`
- Multi-methodology audit configuration
- Time budgets and success criteria

---

## Success Metrics (Updated)

### Corpus Integration

| Metric | Target | Validation |
|--------|--------|------------|
| **Schema Compliance** | 100% | All configs use proper CorpusHub schema |
| **Detection Integration** | 100% | corpus-init uses /api/corpora/detect |
| **Source Modes** | 3 supported | corpus, source, bidirectional |
| **Registration** | Automatic | Auto-register after init |

### Audit Methodology

| Metric | Target | Validation |
|--------|--------|------------|
| **Methodologies** | 3 per project | technical, user, holistic |
| **Iterations** | Min 3 | discovery, verification, stabilization |
| **User Validation** | Required | Can't skip |
| **Time Budget** | 5-12 hours | Configurable per phase |
| **Grade Improvement** | D/F → A/B | Measured |
| **ROI** | >25x | Cost of pre-prod vs. post-prod fixes |

---

## Documentation Updates Required

### New Documents

1. **CORPUS-INTEGRATION-GUIDE.md**
   - How to use CorpusHub detection API
   - Source modes explained
   - Bidirectional sync patterns

2. **MULTI-METHODOLOGY-AUDIT-GUIDE.md**
   - 3-3-1 Rule explained
   - Selecting methodologies by domain
   - Time budgets and success criteria
   - Proven results and case studies

3. **CONFIG-SCHEMA-REFERENCE.md**
   - Complete corpus-config.json schema
   - All sections with examples
   - Validation rules
   - Migration from simplified schema

### Updated Documents

1. **CLAUDE.md** - Add CorpusHub integration
2. **REORGANIZATION-PLAN.md** - Update with real schema
3. **AUDIT-SYSTEM-DESIGN.md** - Update with 3-3-1 methodology

---

## Questions Resolved

### Q: How should corpus-config.json be structured?
**A:** Use the CorpusHub production schema with proper sections: corpus, artifacts (as object), framework (with categories), voice, roles, consistency, audit.

### Q: How many iterations for convergence?
**A:** Minimum 3 (discovery, verification, stabilization) + required user validation. Max 10 configurable.

### Q: What audit methodologies?
**A:** 3 complementary perspectives - technical (how it works), user (how it's experienced), holistic (how it fits together). Run in parallel.

### Q: How to handle documentation that needs both IDE and CorpusHub editing?
**A:** Use `sourceMode: 'bidirectional'` with file watchers and temporary unwatching to prevent loops.

### Q: Should we check if corpus already exists before init?
**A:** Yes, always use `/api/corpora/detect` endpoint before initialization.

---

## Implementation Priority (Updated)

### Week 1
1. ✅ Study CorpusHub docs (DONE)
2. Update config templates with real schema
3. Create corpus-detect skill (API wrapper)
4. Update corpus-init to use detection API

### Week 2
5. Implement source-mode-manager
6. Update convergence-engine with 3-3-1 methodology
7. Create methodology-specific audit skills
8. Test with real CorpusHub instance

### Week 3
9. Create all config templates
10. Validate against CorpusHub
11. Test bidirectional sync
12. Integration testing

---

## Next Steps

1. **Update all planning documents** with CorpusHub integration
2. **Create config templates** using real schema
3. **Build corpus-detect** skill
4. **Update corpus-init** with detection API
5. **Implement 3-3-1 convergence** engine
6. **Test with CorpusHub** production instance

---

**Status:** UPDATED WITH CORPUSHUB INTEGRATION
**Next Milestone:** Implement corpus-detect and update corpus-init
**Repository:** https://github.com/rondmartin-star/claude-code-skills

---

*Aligned with CorpusHub production documentation (2026-01-31)*
*Based on: CORPUS-CONFIG-SCHEMA.md, AUDIT-METHODOLOGY-EXECUTIVE-SUMMARY.md, BIDIRECTIONAL-ARCHITECTURE.md, CORPUS-DETECTION.md*
