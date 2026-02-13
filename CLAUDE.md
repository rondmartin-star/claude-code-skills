# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Claude Code Skills Ecosystem

**Project:** Claude Code Skills Library
**Type:** Meta-Project (Skill Management System)
**Version:** 4.1.0
**Owner:** Pterodactyl Holdings, LLC
**Status:** Production (v4.1 Parallelization In Production)

---

## v4.0 Universal Architecture

**Major Change:** Migrated from project-specific skills to **universal, configuration-driven patterns**.

### Two-Tier Structure

**Tier 1: Core Patterns (Universal)**
- All skills available to all projects
- Configuration-driven behavior via `corpus-config.json`
- No project-specific code
- Located in `core/` directory

**Tier 2: Configuration Templates**
- Lightweight JSON templates
- Define project-specific behavior
- Located in `config/templates/` and `config/examples/`
- Applied to universal skills

**No Tier 3**: Eliminated project-specific extensions (v3.0's america40/, corpus-hub/, etc.)

---

## Repository Structure (v4.0)

```
skills/
├── CLAUDE.md                        # This file (v4.1.0)
├── README.md                        # Ecosystem overview
├── IMPLEMENTATION-STATUS.md         # v4.0 migration progress
├── PARALLELIZATION-GUIDE.md         # v4.1 parallelization patterns
├── MIGRATION-v4.0-to-v4.1.md        # v4.1 migration guide
├── RELEASE-NOTES-v4.1.md            # v4.1 release notes
├── tools/                           # Validation utilities
│   ├── quick_validate.py            # Validate SKILL.md
│   └── package_skill.py             # Package for distribution
│
├── core/                            # TIER 1: Universal Skills
│   ├── corpus/                      # Corpus Management (6 skills)
│   │   ├── corpus-detect/           # Status detection via API
│   │   ├── corpus-init/             # Initialize new corpus
│   │   ├── corpus-convert/          # Convert existing projects
│   │   ├── corpus-config/           # Configuration management
│   │   ├── source-mode-manager/     # 3 source modes (corpus/source/bidirectional)
│   │   └── corpus-orchestrator/     # Route corpus operations
│   │
│   ├── audit/                       # Audit System (12 skills)
│   │   ├── audit-orchestrator/      # Route to applicable audits
│   │   ├── convergence-engine/      # Multi-methodology 3-3-1
│   │   ├── fix-planner/             # Generate & execute fix plans
│   │   └── audits/                  # Audit Types
│   │       ├── consistency/         # Framework term validation
│   │       ├── navigation/          # Link & structure validation
│   │       ├── security/            # Vulnerability scanning
│   │       ├── content/             # Grammar, readability, voice
│   │       ├── quality/             # Code quality, coverage (WIP)
│   │       ├── performance/         # Load time, bundle size (WIP)
│   │       ├── accessibility/       # WCAG compliance (WIP)
│   │       ├── seo/                 # Meta tags, sitemap (WIP)
│   │       └── dependency/          # Vulnerabilities, licenses (WIP)
│   │
│   ├── content/                     # Content Management (4 skills)
│   │   ├── review-edit-author/      # Universal role-based content ops
│   │   │   └── references/
│   │   │       ├── batch-operations.md       # Batch patterns (v4.1)
│   │   │       └── parallel-helpers.js       # Utilities (v4.1)
│   │   ├── document-management/     # CRUD operations (WIP)
│   │   ├── version-control/         # Track changes, rollback (WIP)
│   │   └── collaboration/           # Comments, plans, approvals (WIP)
│   │
│   ├── learning/                    # Learning Skills (v4.1)
│   │   └── convergence/
│   │       └── multi-methodology-convergence/
│   │           ├── parallel-executor.md      # Sub-agent patterns (v4.1)
│   │           └── fix-coordinator.md        # Conflict detection (v4.1)
│   │
│   ├── development/                 # Development Tools (3 skills)
│   │   ├── windows-app/             # Windows app lifecycle (WIP)
│   │   ├── windows-app-packaging/   # MSI installer creation
│   │   └── security/                # Security patterns (WIP)
│   │
│   ├── publishing/                  # Publishing (2 skills)
│   │   ├── publishing-orchestrator/ # Content creation routing (WIP)
│   │   └── content-creation/        # Multi-platform publishing (WIP)
│   │
│   └── utilities/                   # Utilities (4 skills)
│       ├── backup-restore/          # Backup & archive (WIP)
│       ├── validation/              # Input & schema validation (WIP)
│       ├── formatting/              # Format conversion (WIP)
│       └── orchestration/           # Generic routing (WIP)
│
├── config/                          # TIER 2: Configuration
│   ├── templates/                   # Pre-built templates
│   │   ├── web-app.json             # Full-stack web applications
│   │   ├── content-corpus.json      # Documentation repositories
│   │   ├── framework-docs.json      # Framework documentation
│   │   ├── windows-app.json         # Windows desktop apps
│   │   └── default.json             # Minimal generic template
│   │
│   └── examples/                    # Real project examples
│       ├── corpushub-config.json    # CorpusHub platform config
│       └── america40-config.json    # America 4.0 framework config
│
└── [legacy]/                        # v3.0 project-specific (being migrated)
    ├── meta/
    ├── windows-app/
    ├── publishing/
    ├── america40/
    └── corpus-hub/
```

---

## v4.1 Universal Parallelization (2026-02-12)

**Major Enhancement:** Ecosystem-wide parallelization for 40-50% performance improvement.

### Three-Tier Parallel Architecture

**Tier 1: Convergence Parallelization**
- Unified 15-methodology pool (7 audit + 8 phase-review merged)
- Parallel execution of ALL 15 methodologies per pass
- Model-optimized (6 Opus for user/security, 9 Sonnet for technical)
- Context optimization (30% context, 70% analysis budget)
- Parallel fix application with conflict detection

**Tier 2: Learning Skills Parallelization**
- Battle-plan Phase 2+3 parallel (pattern check + pre-mortem)
- Phase 5 parallel monitoring (verify-evidence, detect-infinite-loop, manage-context)
- Error-reflection 3-phase parallel analysis (2.6x speedup)
- Pre-mortem 6-category parallel generation (6x speedup)

**Tier 3: Content Management Parallelization**
- Batch artifact loading (10x speedup)
- Chunked parallel comment loading (5x speedup)
- Queued AI improvements (3x speedup)
- Dependency-aware batch updates

### Performance Improvements

| System | Before | After | Improvement |
|--------|--------|-------|-------------|
| Convergence (7 audits) | 5-10 min | 2-5 min | 40-50% faster |
| Learning monitoring | 90ms/step | 30ms/step | 67% faster |
| Content batch ops | Sequential | Parallel | 3-10x faster |
| Token usage | Baseline | Optimized | 69% reduction |

### Real-World Results

**CorpusHub Production:**
- F→A grade in 5 hours, $27k+ value delivered
- 40% faster deployments (8-10h → 5-6h)
- 63% cost reduction ($1200 → $450 per cycle)

### See Also

- `PARALLELIZATION-GUIDE.md` - Comprehensive parallelization patterns
- `MIGRATION-v4.0-to-v4.1.md` - Migration guide
- `RELEASE-NOTES-v4.1.md` - Release notes

---

## Core Concepts (v4.0)

### Corpus-First Approach

**Every project is corpus-enabled by default.**

A corpus is a project with:
- `corpus-config.json` at root
- Structured artifacts (code, docs, specs, etc.)
- Framework terms for consistency
- Voice attributes for AI guidance
- Role-based permissions
- Audit configuration

**Initialization:**
```bash
# New project
"Initialize this as a corpus"  → loads corpus-init

# Existing project
"Convert this to corpus"  → loads corpus-convert
```

### Source Modes

Every artifact has a **source mode** defining editing workflow:

| Mode | Edited In | Source of Truth | Use For |
|------|-----------|-----------------|---------|
| **corpus** | CorpusHub only | CorpusHub HTML | Requirements, design docs, ADRs |
| **source** | IDE (VS Code) | Files in repo | Code, config files, tests |
| **bidirectional** | Either location | Synced both ways | Documentation, guides, API docs |

**Configuration:**
```json
{
  "artifacts": {
    "source-code": {
      "path": "src",
      "sourceMode": "source"
    },
    "requirements": {
      "path": "docs/requirements",
      "sourceMode": "corpus"
    },
    "documentation": {
      "path": "docs",
      "sourceMode": "bidirectional"
    }
  }
}
```

### Multi-Methodology 3-3-1 Convergence

**Three Methodologies:**
1. **Technical** - How it works (code, architecture)
2. **User** - How it's experienced (UX, flows, accessibility)
3. **Holistic** - How it fits together (docs, consistency, completeness)

**Three Iterations:**
1. Discovery (find issues)
2. Verification (confirm fixes)
3. Stabilization (ensure stability)

**One User Validation:**
- Real users test the system
- In production environment
- With actual data

**Two-Phase Workflow:**
1. **Automated Convergence** (GATE) - Must pass 3 consecutive clean automated passes
2. **User Validation** (Clean System) - Users test only after automation succeeds

**Proven Results:** CorpusHub went from F→A grade in 5 hours, $27k+ value delivered

---

## Configuration Schema (corpus-config.json)

### Complete Structure

```json
{
  "corpus": {
    "name": "Project Name",
    "description": "Project description",
    "version": "1.0.0",
    "baseDir": "/absolute/path"
  },

  "artifacts": {
    "artifact-slug": {
      "path": "relative/path",
      "label": "Display Label",
      "extensions": [".ext"],
      "sourceMode": "corpus|source|bidirectional"
    }
  },

  "framework": {
    "categories": [{
      "id": "category-id",
      "label": "Category Label",
      "terms": ["Term 1", "Term 2"],
      "canonicalSource": "artifact-slug",
      "matchMode": "word-boundary|case-insensitive|exact"
    }]
  },

  "voice": {
    "promptFile": "path/to/prompt.md",
    "attributes": ["professional", "clear"],
    "avoid": ["jargon", "ambiguity"],
    "preferredTerms": {}
  },

  "roles": {
    "available": ["admin", "editor", "author", "reviewer", "viewer", "pending"],
    "defaultRole": "pending",
    "aiAccess": ["admin", "editor", "author"],
    "editAccess": ["admin", "editor", "author"]
  },

  "audit": {
    "methodology": "multi-methodology-3-3-1",
    "applicable_audits": ["security", "quality", "content"],
    "convergence": {
      "enabled": true,
      "automated": {
        "max_iterations": 10,
        "required_clean_passes": 3
      },
      "user_validation": {
        "required": true,
        "after_automated_convergence": true,
        "min_testers": 2
      },
      "methodologies": [
        {
          "name": "technical",
          "audits": [{"id": "security"}, {"id": "quality"}]
        },
        {
          "name": "user",
          "audits": [{"id": "content"}, {"id": "accessibility"}]
        },
        {
          "name": "holistic",
          "audits": [{"id": "consistency"}, {"id": "navigation"}]
        }
      ]
    }
  }
}
```

See `config/templates/` for complete working examples.

---

## Common Development Tasks

### Validate Skills

```bash
# Check SKILL.md frontmatter
python tools/quick_validate.py core/corpus/corpus-init

# Verify all skills under 15KB
find core/ -name "SKILL.md" -exec wc -c {} \; | awk '$1 > 15360'
```

### Work with Corpus

```bash
# Initialize new project
"Initialize this as a corpus"

# Convert existing project
"Convert this to corpus"

# Check status
"Check corpus status"

# Update config
"Update corpus configuration"
```

### Run Audits

```bash
# Run all applicable audits
"Run convergence audit"

# Specific audit
"Run security audit"
"Check content quality"
"Validate consistency"
```

### Content Management

```bash
# Review mode (read-only + comments)
"Review this document"
"Add comment to section"

# Editor mode (modify + AI)
"Edit this artifact"
"Improve clarity with AI"

# Author mode (create new)
"Create new draft"
"Generate content with AI"
```

### Run Parallel Convergence

```bash
# Run unified mode (all 15 methodologies in parallel)
"Run convergence in unified mode"

# Configure concurrency
"Update convergence config for 10 concurrent methodologies"

# Check parallel performance
"Show convergence performance metrics"
```

---

## Skill Loading Patterns

### Entry Points

**Corpus Operations:**
- "Initialize corpus" → `corpus-init`
- "Convert to corpus" → `corpus-convert`
- "Check status" → `corpus-detect`
- "Update config" → `corpus-config`
- Ambiguous → `corpus-orchestrator` routes

**Audit Operations:**
- "Run audit" → `audit-orchestrator` routes
- "Start convergence" → `convergence-engine`
- Specific audit → Direct load (e.g., `security`, `content`)

**Content Operations:**
- "Review content" → `review-edit-author` (reviewer mode)
- "Edit content" → `review-edit-author` (editor mode)
- "Create content" → `review-edit-author` (author mode)

### Orchestrator Routing

**corpus-orchestrator:**
```
├─ Not enabled → Setup
│  ├─ New project → corpus-init
│  └─ Existing → corpus-convert
└─ Enabled → Manage
   ├─ Status → corpus-detect
   ├─ Config → corpus-config
   └─ Sync → source-mode-manager
```

**audit-orchestrator:**
```
├─ Convergence mode → convergence-engine
└─ Single audit → Route by project type
   ├─ web-app → [security, quality, performance, ...]
   ├─ content-corpus → [consistency, content, navigation]
   └─ framework-docs → [consistency, content, navigation]
```

---

## Key Design Principles

### Universal Availability
Every skill works with every project type via configuration.

### Configuration-Driven
Behavior determined by corpus-config.json, not hardcoded logic.

### CorpusHub Integration
All skills integrate with CorpusHub production API at `http://localhost:3000`.

### Size Optimization
- Target: <15KB per SKILL.md
- Detailed content in `references/` subdirectories
- Current: 100% compliance (14 skills, all under 15KB)

### Fool-Proof Design
- Sensible defaults
- Auto-detection
- Clear error messages
- Designed for all skill levels

---

## Migration Status (v3.0 → v4.0)

**Current Status:** 50% Complete (Phase 1, Week 1)

**Completed:**
- ✅ Planning & Documentation (100%)
- ✅ Core Corpus Skills (6/6 - 100%)
- ✅ Critical Audit Skills (7/12 - 58%)
- ✅ Config Templates (5/6 - 83%)
- ✅ review-edit-author (consolidates 6 old skills)

**In Progress:**
- ⏳ Remaining Audit Skills (5/12)
- ⏳ Content Management (3/4)
- ⏳ Development & Publishing (4 skills)
- ⏳ Utilities (4 skills)
- ⏳ Documentation (7 docs)

See `IMPLEMENTATION-STATUS.md` for detailed progress.

---

## Version History

### v4.1.0 (2026-02-12) - Universal Parallelization

**Major Enhancement:**
- Ecosystem-wide parallelization (convergence, learning, content)
- 40-50% performance improvement
- 69% token reduction (learning skills)
- 3-10x speedup (content operations)

**New Features:**
- 15-methodology unified convergence pool
- Parallel fix application with conflict detection
- Battle-plan parallel phases (Phase 2+3, Phase 5)
- Batch content operations
- Model-optimized execution (6 Opus, 9 Sonnet)

**Documentation:**
- PARALLELIZATION-GUIDE.md (57KB comprehensive guide)
- parallel-executor.md, fix-coordinator.md
- batch-operations.md, parallel-helpers.js

**Performance (Real-world):**
- CorpusHub: F→A grade in 5 hours, $27k+ value
- 40% faster deployments (8-10h → 5-6h)
- 63% cost reduction ($1200 → $450 per cycle)

**Total Files Modified:** 10 core skills + 9 new files

### v4.0.0 (2026-01-31) - Universal Architecture

**Major Reorganization:**
- Two-tier universal architecture (core + config)
- Corpus-first approach (every project corpus-enabled)
- Multi-methodology 3-3-1 convergence
- Source modes (corpus/source/bidirectional)
- Configuration-driven behavior

**New Skills (14 implemented):**
- 6 corpus management skills
- 7 audit skills (+ 5 WIP)
- 1 universal content management skill

**Total Skills (Projected):** 27 core skills
**Current Status:** 14 complete, 13 WIP

### v3.0.0 (2026-01-31) - Multi-Ecosystem Expansion

**Added:**
- America 4.0 framework (7+ skills)
- CorpusHub platform (10+ skills)
- 5 major categories

**Total Skills:** 36+ across 5 categories

### v2.0.0 (2026-01-27) - Comprehensive Restructure

**Changes:**
- Flat → 3-tier structure
- Security orchestrator
- Publishing orchestrator
- Size optimization

**Total Skills:** 15

### v1.0.0 (2026-01-20) - Initial Version

**Initial Release:** 13 skills in flat structure

---

## License

Proprietary - Pterodactyl Holdings, LLC

---

*Last Updated: 2026-02-12*
*Version: 4.1.0*
*Branch: main*
*Status: Production - v4.1 Parallelization Complete*
