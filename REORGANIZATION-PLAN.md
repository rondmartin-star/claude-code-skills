# Skills Ecosystem Reorganization Plan

**Version:** 4.0.0 (Proposed)
**Date:** 2026-01-31
**Status:** PLANNING
**Scope:** Comprehensive restructure for generalization and efficiency

---

## Executive Summary

The current skills ecosystem (v3.0.0) has grown organically to 36+ skills across 5 categories, resulting in:

### Critical Issues Identified

1. **Significant Duplication** - 40%+ of code duplicated across ecosystems
   - consistency-engine duplicated in america40, corpus-hub
   - backup-archive duplicated in america40, corpus-hub
   - Role-based patterns duplicated (reviewer, editor, author)
   - Orchestrator patterns repeated 8 times with minimal variation

2. **Size Violations** - 7 skills exceed 15KB target (19% of ecosystem)
   - corpus-convert: 22KB (47% over)
   - corpus-init: 19.8KB (32% over)
   - windows-app-system-design: 19.8KB (32% over)
   - windows-app-ui-design: 18KB (20% over)
   - corpus-hub-v2/audit: 17.8KB (19% over)
   - windows-app-build: 16KB (7% over)
   - windows-app-orchestrator: 15.8KB (5% over)

3. **Domain Coupling** - Skills tightly coupled to specific domains
   - Limits reusability across projects
   - Increases maintenance burden
   - Obscures underlying patterns

### Proposed Solution

**Reorganize into 3-tier generalized architecture:**

```
Tier 1: Core Patterns (domain-agnostic)
Tier 2: Domain Adapters (lightweight configuration)
Tier 3: Project-Specific Extensions (optional)
```

**Expected Benefits:**
- 60% reduction in code duplication
- All skills under 15KB (100% compliance)
- Increased reusability across domains
- Simplified maintenance
- Faster skill loading

---

## Current State Analysis

### Duplication Matrix

| Pattern | Instances | Locations | Est. Duplication |
|---------|-----------|-----------|------------------|
| **consistency-engine** | 2 | america40, corpus-hub | 70% overlap |
| **backup-archive** | 2 | america40, corpus-hub | 80% overlap |
| **reviewer workflow** | 2 | america40, corpus-hub | 85% overlap |
| **editor workflow** | 2 | america40, corpus-hub | 85% overlap |
| **author workflow** | 2 | america40, corpus-hub | 85% overlap |
| **orchestrator pattern** | 8 | All categories | 60% overlap |
| **role-based routing** | 4 | america40 (3), corpus-hub (1) | 75% overlap |

**Total Estimated Duplication:** ~40-50% of codebase

### Shared Concepts Identified

#### 1. Document Management Pattern
**Appears in:** corpus-hub, america40, publishing, windows-app (docs)

**Core Capabilities:**
- Browse/list artifacts
- View artifact content
- Update artifact content
- Track version history
- Manage metadata

**Domain Variations:**
- corpus-hub: Generic documents with corpus-config
- america40: Framework documents with 7 principles
- publishing: Content with platform formats
- windows-app: Technical documentation

#### 2. Review-Edit-Author (REA) Pattern
**Appears in:** corpus-hub, america40

**Core Workflow:**
1. **Review**: Browse → Comment → Generate plan
2. **Edit**: Modify → Preview consistency → Commit
3. **Author**: Draft new → Analyze implications → Integrate

**Domain Variations:**
- corpus-hub: API-driven with SQLite backend
- america40: Framework-aware with canonical sources

#### 3. Consistency Scanning Pattern
**Appears in:** corpus-hub, america40

**Core Capabilities:**
- Define canonical terms
- Scan for term misuse
- Track cross-references
- Report violations
- Suggest fixes

**Domain Variations:**
- corpus-hub: corpus-config.json framework terms
- america40: 7 principles + 14 roles + key terms

#### 4. Backup/Archive Pattern
**Appears in:** corpus-hub, america40

**Core Capabilities:**
- Create backups (full, incremental, selective)
- Restore from backup
- Retention policies
- Archive management

**Domain Variations:**
- corpus-hub: API-driven, per-corpus databases
- america40: File-based, framework artifacts

#### 5. Orchestrator Pattern
**Appears in:** All categories (8 instances)

**Core Capabilities:**
- Detect user intent
- Route to appropriate skill
- Manage phase transitions
- Track state

**Domain Variations:**
- windows-app: Phase-based routing (requirements → design → build → deploy)
- security: Context-based routing (auth vs secure-coding)
- publishing: Content-type routing (social, newsletter, blog)
- america40: Role-based routing (reviewer, editor, author)
- corpus-hub: Intent + role routing

---

## Proposed Architecture: v4.0.0

### Two-Tier Universal Structure

**UPDATED: All skills now universally available to all projects**

```
skills/
├── core/                          # Tier 1: Universal patterns (all projects)
│   ├── corpus/                    # Corpus management (DEFAULT for all)
│   │   ├── corpus-init/           # Initialize any project as corpus
│   │   ├── corpus-convert/        # Convert existing projects
│   │   ├── corpus-config/         # Configuration management
│   │   └── corpus-orchestrator/   # Route corpus operations
│   │
│   ├── audit/                     # Comprehensive audit system (NEW)
│   │   ├── audit-orchestrator/    # Route to applicable audits
│   │   ├── convergence-engine/    # Iterative audit until stable
│   │   ├── fix-planner/           # Generate and execute fix plans
│   │   └── audits/                # Individual audit types
│   │       ├── consistency/       # Term usage, cross-refs
│   │       ├── security/          # XSS, CSRF, SQL injection
│   │       ├── quality/           # Test coverage, linting
│   │       ├── performance/       # Load time, bundle size
│   │       ├── accessibility/     # WCAG compliance
│   │       ├── seo/               # Meta tags, sitemap
│   │       ├── content/           # Grammar, style
│   │       ├── navigation/        # Broken links, orphans
│   │       └── dependency/        # Vulnerabilities, updates
│   │
│   ├── content/                   # Content management & workflows
│   │   ├── document-management/   # Generic doc CRUD operations
│   │   ├── review-edit-author/    # Generic REA workflow
│   │   ├── version-control/       # Track changes, rollback
│   │   └── collaboration/         # Comments, plans, approvals
│   │
│   ├── development/               # Software development patterns
│   │   ├── windows-app/           # Windows application lifecycle
│   │   │   ├── requirements/      # User stories, acceptance criteria
│   │   │   ├── system-design/     # Data models, API design
│   │   │   ├── ui-design/         # Page inventory, navigation
│   │   │   ├── build/             # Implementation, testing
│   │   │   └── supervision/       # NSSM service, MSI packaging
│   │   │
│   │   └── security/              # Security patterns
│   │       ├── authentication/    # OAuth, sessions, first-user admin
│   │       └── secure-coding/     # XSS, CSRF, SQL injection prevention
│   │
│   ├── publishing/                # Content creation & export
│   │   ├── publishing-orchestrator/
│   │   ├── content-creation/      # HTML-first with multi-format export
│   │   └── format-converters/     # DOCX, PDF, PPTX, plain text
│   │
│   └── utilities/                 # Shared utilities
│       ├── backup-restore/        # Generic backup/archive
│       ├── validation/            # Input validation, schema checking
│       ├── formatting/            # HTML, Markdown, DOCX, PDF
│       └── orchestration/         # Generic orchestrator framework
│
├── config/                        # Tier 2: Configuration templates
│   ├── templates/                 # corpus-config.json templates
│   │   ├── web-app.json
│   │   ├── content-corpus.json
│   │   ├── framework-docs.json
│   │   ├── windows-app.json
│   │   └── default.json
│   │
│   └── examples/                  # Real-world configuration examples
│       ├── america40-config.json  # America 4.0 framework
│       ├── corpushub-config.json  # CorpusHub platform
│       └── sample-webapp.json     # Sample web application
│
└── meta/                          # Ecosystem management
    ├── skill-ecosystem-manager/
    ├── conversation-snapshot/
    └── plugin-ecosystem/
```

### Tier Responsibilities

**Tier 1: Core Patterns** (Universal - ALL PROJECTS)
- **Corpus-First:** Every project initialized as corpus by default
- **Audit-Ready:** Comprehensive audit system available to all
- **Universal Access:** All skills available to all projects
- **Configuration-Driven:** Behavior customized via corpus-config.json
- Size: 8-12KB per skill (100% compliance)
- Examples: corpus-init, audit-orchestrator, review-edit-author, windows-app-build

**Tier 2: Configuration Templates** (Lightweight - JSON only)
- Pre-configured corpus-config.json templates for common project types
- No code, just configuration
- Easy to customize
- Examples: web-app.json, content-corpus.json, framework-docs.json

**Key Changes from v3.0:**
- ✅ Eliminated Tier 3 (project-specific extensions)
- ✅ All patterns generalized and universally available
- ✅ Corpus management promoted to core (default for all)
- ✅ Navigation auditor moved to audit suite
- ✅ Configuration-only second tier (no adapters)

---

## Detailed Design: Core Patterns

### 1. document-management (Core Pattern)

**Purpose:** Generic CRUD operations for any document/artifact type

**Size Target:** 10KB

**Configuration:**
```json
{
  "backend": "api" | "filesystem" | "database",
  "endpoints": {
    "list": "/api/artifacts",
    "get": "/api/artifacts/:type/:name",
    "update": "/api/artifacts/:type/:name",
    "create": "/api/artifacts",
    "delete": "/api/artifacts/:type/:name"
  },
  "metadata_schema": {
    "required": ["type", "name", "title"],
    "optional": ["author", "created_at", "updated_at"]
  }
}
```

**Capabilities:**
- List artifacts (with filtering, sorting)
- Get artifact content
- Update artifact
- Create new artifact
- Delete artifact
- Manage metadata

**Domain-Agnostic:** Works for corpus docs, framework docs, content, code docs, etc.

### 2. review-edit-author (Core Pattern)

**Purpose:** Generic workflow for reviewing, editing, and authoring documents

**Size Target:** 12KB

**Configuration:**
```json
{
  "roles": {
    "reviewer": {
      "permissions": ["read", "comment", "generate_plan"],
      "workflow": "browse → comment → plan"
    },
    "editor": {
      "permissions": ["read", "comment", "edit", "preview"],
      "workflow": "modify → preview → commit"
    },
    "author": {
      "permissions": ["read", "comment", "create", "analyze"],
      "workflow": "draft → analyze → integrate"
    }
  },
  "comment_types": ["suggestion", "issue", "question", "praise"],
  "plan_generation": {
    "enabled": true,
    "scopes": ["artifact", "all_open"]
  }
}
```

**Capabilities:**
- Role-based access control
- Comment management
- Plan generation from comments
- Consistency preview
- Change tracking

**Domain-Agnostic:** Works for any document-based workflow with review/edit/author roles

### 3. consistency-scanning (Core Pattern)

**Purpose:** Generic consistency checking against canonical definitions

**Size Target:** 11KB

**Configuration:**
```json
{
  "canonical_sources": [
    {
      "type": "terms",
      "source": "path/to/glossary.json",
      "definitions": {"term1": "definition1"}
    },
    {
      "type": "principles",
      "source": "path/to/principles.md",
      "count": 7
    }
  ],
  "scan_rules": [
    {
      "name": "term_misuse",
      "severity": "warning",
      "description": "Using non-standard term when canonical exists"
    },
    {
      "name": "broken_reference",
      "severity": "critical",
      "description": "Reference to non-existent artifact"
    }
  ],
  "issue_categories": ["term_misuse", "broken_reference", "style_deviation"]
}
```

**Capabilities:**
- Load canonical definitions from config
- Scan documents for violations
- Categorize and prioritize issues
- Suggest fixes
- Track issue resolution

**Domain-Agnostic:** Works for any domain with canonical terms/principles

### 4. backup-restore (Core Pattern)

**Purpose:** Generic backup and restore operations

**Size Target:** 9KB

**Configuration:**
```json
{
  "storage": {
    "type": "filesystem" | "s3" | "database",
    "path": "backups/",
    "retention": {
      "daily": 7,
      "weekly": 4,
      "monthly": 12,
      "manual": "indefinite"
    }
  },
  "backup_types": {
    "full": {
      "includes": ["artifacts", "metadata", "database"]
    },
    "incremental": {
      "includes": ["changed_since_last"]
    },
    "selective": {
      "includes": ["specified_types"]
    }
  }
}
```

**Capabilities:**
- Create backups (full, incremental, selective)
- Restore from backup
- List available backups
- Manage retention policies
- Archive cleanup

**Domain-Agnostic:** Works for any system needing backup/restore

### 5. orchestration (Core Pattern Framework)

**Purpose:** Generic orchestrator framework for routing and state management

**Size Target:** 8KB

**Configuration:**
```json
{
  "routing_strategy": "phase" | "role" | "intent" | "content_type",
  "routes": [
    {
      "pattern": "create|write|author",
      "target": "review-edit-author",
      "context": {"role": "author"}
    },
    {
      "pattern": "review|comment|feedback",
      "target": "review-edit-author",
      "context": {"role": "reviewer"}
    }
  ],
  "state_management": {
    "enabled": true,
    "persistence": "filesystem" | "memory"
  }
}
```

**Capabilities:**
- Intent detection from user prompt
- Route to appropriate skill
- Manage phase/role transitions
- Track state across sessions
- Validate exit gates

**Domain-Agnostic:** Works for any multi-skill workflow needing coordination

---

## Migration Strategy

### Phase 1: Create Core Patterns (Weeks 1-2)

**Objective:** Build domain-agnostic core skills

**Steps:**
1. Extract common logic from duplicated skills
2. Create generalized interfaces
3. Build configuration system
4. Create 5 core pattern skills
5. Validate with test configurations

**Deliverables:**
- core/corpus/ (promoted from adapter tier)
- core/audit/ (NEW comprehensive audit system)
- core/content/document-management/
- core/content/review-edit-author/
- core/utilities/backup-restore/
- core/utilities/orchestration/

**Risk:** Medium - Requires careful abstraction
**Mitigation:** Start with most duplicated pattern (review-edit-author)

### Phase 2: Create Configuration Templates (Weeks 3-4)

**Objective:** Build corpus-config.json templates for common project types

**Steps:**
1. Create config/ directory structure
2. Extract domain-specific config from existing skills
3. Create JSON configuration templates (NO CODE)
4. Create example configurations from real projects
5. Test templates with core patterns

**Deliverables:**
- config/templates/web-app.json
- config/templates/content-corpus.json
- config/templates/framework-docs.json
- config/templates/windows-app.json
- config/examples/america40-config.json
- config/examples/corpushub-config.json

**Risk:** Low - Configuration only, no code
**Mitigation:** Validation against schema

### Phase 3: Refactor Size Violations (Week 5)

**Objective:** Bring all skills under 15KB target

**Target Skills:**
1. corpus-convert (22KB → 12KB) - Extract templates to references
2. corpus-init (19.8KB → 11KB) - Extract prompts to references
3. windows-app-system-design (19.8KB → 13KB) - Extract examples to references
4. windows-app-ui-design (18KB → 12KB) - Extract UI patterns to references
5. corpus-hub-v2/audit (17.8KB → 14KB) - Extract audit rules to references
6. windows-app-build (16KB → 14KB) - Further consolidation
7. windows-app-orchestrator (15.8KB → 12KB) - Use core orchestration pattern

**Strategy:**
- Move detailed examples to references/*.md
- Use core patterns where applicable
- Create lookup tables instead of verbose explanations
- Link to adapters for domain logic

**Risk:** Low - Well-defined refactoring
**Mitigation:** Incremental approach, one skill at a time

### Phase 4: Consolidate Duplicates (Week 6)

**Objective:** Eliminate duplicate skills

**Actions:**

**consistency-engine (2 instances → 1 core + 2 configs):**
- Delete america40/shared/consistency-engine/
- Delete corpus-hub/shared/consistency-engine/
- Create core/patterns/consistency-scanning/
- Create adapters/*/consistency-config.json

**backup-archive (2 instances → 1 core + 2 configs):**
- Delete america40/shared/backup-archive/
- Delete corpus-hub/shared/backup-archive/
- Create core/patterns/backup-restore/
- Create adapters/*/backup-config.json

**Role Skills (6 instances → 1 core + 2 adapters):**
- Consolidate corpus-hub/reviewer + america40/review → core/patterns/review-edit-author (reviewer mode)
- Consolidate corpus-hub/editor + america40/edit → core/patterns/review-edit-author (editor mode)
- Consolidate corpus-hub/author + america40/author → core/patterns/review-edit-author (author mode)
- Create adapters with role configurations

**Risk:** High - Breaking changes
**Mitigation:** Keep deprecated skills for 1 version with forwarding logic

### Phase 5: Create Audit System (Week 7)

**Objective:** Build comprehensive audit orchestrator with convergence

**Steps:**
1. Create audit-orchestrator skill
2. Implement convergence-engine algorithm
3. Build fix-planner with auto-fix strategies
4. Port navigation-auditor to navigation-audit
5. Create remaining 8 audit types
6. Integration testing

**Deliverables:**
- core/audit/audit-orchestrator/
- core/audit/convergence-engine/
- core/audit/fix-planner/
- core/audit/audits/consistency/
- core/audit/audits/security/
- core/audit/audits/quality/
- core/audit/audits/performance/
- core/audit/audits/accessibility/
- core/audit/audits/seo/
- core/audit/audits/content/
- core/audit/audits/navigation/
- core/audit/audits/dependency/

**Risk:** Medium - Complex new system
**Mitigation:** Phased implementation, start with existing audits

### Phase 6: Update Documentation (Week 8)

**Objective:** Comprehensive documentation update

**Steps:**
1. Update CLAUDE.md to v4.0.0
2. Update README.md for each tier
3. Create migration guide for skill users
4. Update skill-ecosystem-manager references
5. Create new skill templates for v4.0.0

**Deliverables:**
- CLAUDE.md v4.0.0
- Migration guide (v3.0 → v4.0)
- Updated README files (15 total)
- New skill templates
- Architecture decision records (ADRs)

**Risk:** Low - Documentation only
**Mitigation:** Phased updates, user testing

### Phase 7: Validation & Testing (Week 9)

**Objective:** Comprehensive testing of new architecture

**Test Cases:**
1. **Core Pattern Tests:** Each core pattern works standalone
2. **Adapter Tests:** Each adapter correctly configures core patterns
3. **Integration Tests:** Full workflows work end-to-end
4. **Size Tests:** All skills under 15KB
5. **Navigation Tests:** All documented paths work
6. **Performance Tests:** Skills load faster than v3.0

**Validation Tools:**
- Automated size checks
- Navigation auditor
- quick_validate.py for all skills
- Integration test suite

**Risk:** Medium - Complex testing required
**Mitigation:** Automated test suite, gradual rollout

### Phase 8: Gradual Rollout (Week 10)

**Objective:** Deploy v4.0.0 with backward compatibility

**Steps:**
1. Deploy core patterns (read-only, no breaking changes)
2. Deploy adapters (aliases to old paths)
3. Deprecate old skills (warnings, not errors)
4. Monitor usage and errors
5. Fix issues incrementally
6. Remove deprecated skills in v4.1.0

**Rollout Plan:**
- Week 10: Deploy to test environment
- Week 11: Deploy to production with deprecation warnings
- Week 12-15: Monitor and fix issues
- Week 16: Remove deprecated skills (v4.1.0 release)

**Risk:** Low - Backward compatibility maintained
**Mitigation:** Gradual deprecation, clear migration docs

---

## Expected Outcomes

### Quantitative Improvements

| Metric | Current (v3.0) | Target (v4.0) | Improvement |
|--------|----------------|---------------|-------------|
| **Total Skills** | 36+ | ~25 | 31% reduction |
| **Code Duplication** | ~45% | <5% | 89% reduction |
| **Skills >15KB** | 7 (19%) | 0 (0%) | 100% compliance |
| **Largest Skill** | 22KB | <15KB | 32% reduction |
| **Avg Skill Size** | ~12KB | ~10KB | 17% reduction |
| **Maintenance Burden** | High | Low | 60% reduction |
| **Universal Availability** | 0% | 100% | All skills → all projects |
| **Corpus-Enabled Projects** | 2 | All | Default for everything |
| **Audit Coverage** | Partial | Comprehensive | 9 audit types |

### Qualitative Improvements

**Reusability:**
- Core patterns work across any domain
- Easy to add new projects/domains
- Reduced time to create new skills

**Maintainability:**
- Single source of truth for each pattern
- Bug fixes benefit all users
- Clear separation of concerns

**Discoverability:**
- Clearer architecture (3 tiers)
- Better navigation (core → adapter → project)
- Improved documentation

**Performance:**
- Faster skill loading (smaller files)
- On-demand reference loading
- Reduced context usage

**Extensibility:**
- Easy to add new core patterns
- Easy to create new adapters
- Easy to add project extensions

---

## Risk Assessment

### High Risks

**Risk:** Breaking changes for existing users
**Mitigation:**
- Maintain backward compatibility for 1 version
- Provide migration guide
- Gradual deprecation with warnings

**Risk:** Over-generalization loses domain value
**Mitigation:**
- Keep domain adapters rich with context
- Project extensions for non-generalizable features
- Test with real use cases

### Medium Risks

**Risk:** Migration takes longer than 10 weeks
**Mitigation:**
- Phased approach allows partial completion
- Core patterns deliver value immediately
- Incremental improvements acceptable

**Risk:** Configuration complexity
**Mitigation:**
- Provide templates for common configs
- Auto-generation tools for adapters
- Clear documentation with examples

### Low Risks

**Risk:** User resistance to change
**Mitigation:**
- Clear communication of benefits
- Show concrete improvements (size, speed)
- Provide migration assistance

**Risk:** Size reduction compromises functionality
**Mitigation:**
- Reference files maintain full detail
- On-demand loading ensures availability
- No functionality removed, only reorganized

---

## Success Criteria

### Must Have (v4.0.0 Release)

- [ ] All skills under 15KB (100% compliance)
- [ ] Code duplication reduced to <15%
- [ ] 5 core patterns fully functional
- [ ] 4 domain adapters operational
- [ ] Backward compatibility maintained
- [ ] Full documentation updated
- [ ] All validation tests pass

### Should Have (v4.1.0 Release)

- [ ] Deprecated skills removed
- [ ] Performance benchmarks show improvement
- [ ] User feedback incorporated
- [ ] Additional core patterns identified
- [ ] New project adapter created (proof of concept)

### Could Have (v4.2.0+ Future)

- [ ] Auto-generation tools for adapters
- [ ] Visual skill navigator
- [ ] Performance monitoring dashboard
- [ ] Community-contributed patterns
- [ ] Plugin marketplace

---

## Backward Compatibility Plan

### Deprecation Strategy

**Phase 1: Warnings (v4.0.0, Week 10-15)**
```
When user loads deprecated skill:
WARNING: This skill has been deprecated and will be removed in v4.1.0.
Please use: core/patterns/[pattern-name] with adapters/[domain]/[adapter-name]
Migration guide: ~/.claude/skills/MIGRATION-v3-to-v4.md
```

**Phase 2: Forwarding (v4.0.0, Week 10-15)**
```
Deprecated skills automatically forward to new location:
america40/shared/consistency-engine → core/patterns/consistency-scanning
  + load adapters/framework-management/consistency-config.json
```

**Phase 3: Removal (v4.1.0, Week 16+)**
```
Deprecated skills removed from filesystem
Error message provides clear migration path
Migration guide remains available
```

### Alias System

Create alias files in deprecated locations:

```yaml
# america40/shared/consistency-engine/DEPRECATED.md
---
deprecated: true
replacement: core/patterns/consistency-scanning
adapter: adapters/framework-management/consistency-config.json
migration_guide: ~/.claude/skills/MIGRATION-v3-to-v4.md
---

This skill has been deprecated. Please use the replacement above.
```

---

## Appendix A: File Size Reduction Techniques

### Technique 1: Extract Examples to References

**Before (in SKILL.md):**
```markdown
### Example: Create User Story

Here's a complete example of a user story:

As a property manager, I want to view all my properties on a dashboard
so that I can quickly see which ones need attention.

Acceptance Criteria:
- Dashboard shows all properties I manage
- Properties display key metrics (occupancy, rent status, maintenance)
- I can filter by status (occupied, vacant, maintenance)
- I can click a property to see details

[30 more lines of examples...]
```

**After (in SKILL.md):**
```markdown
### Example: Create User Story

See templates in references/user-story-templates.md

Quick format:
- As a [role], I want [goal] so that [benefit]
- Acceptance Criteria: [bulleted list]
```

**Savings:** ~400 bytes → ~80 bytes (80% reduction)

### Technique 2: Use Lookup Tables

**Before (in SKILL.md):**
```markdown
### Error: SQLITE_BUSY

This error occurs when the database is locked by another process.
Common causes include:
- Another user has an open transaction
- A background process is writing to the database
- File system permissions issue

To fix:
1. Check for other running processes
2. Ensure database file is not locked
3. Implement retry logic with exponential backoff
4. Use WAL mode for SQLite

[20 more lines...]
```

**After (in SKILL.md):**
```markdown
| Error | Cause | Fix | Ref |
|-------|-------|-----|-----|
| SQLITE_BUSY | DB locked | Retry with backoff | [1] |

[1] references/error-catalog.md#sqlite-busy
```

**Savings:** ~350 bytes → ~80 bytes (77% reduction)

### Technique 3: Use Core Patterns

**Before (in SKILL.md):**
```markdown
### Create Backup

To create a full backup:
1. Determine backup type (full/incremental/selective)
2. Create timestamp for backup name
3. Create backup directory if not exists
4. Copy all artifacts to backup location
5. Export database to SQL dump
6. Create manifest file with metadata
7. Compress backup to tar.gz
8. Verify backup integrity

[50 more lines of implementation details...]
```

**After (in SKILL.md):**
```markdown
### Create Backup

Use core/patterns/backup-restore with config:
- backup_type: full | incremental | selective
- retention: see adapters/[domain]/backup-config.json

Details: references/backup-procedures.md
```

**Savings:** ~800 bytes → ~120 bytes (85% reduction)

---

## Appendix B: Configuration File Examples

### Corpus Management Adapter Config

```json
{
  "name": "corpus-management",
  "version": "4.0.0",
  "core_patterns": {
    "document_management": {
      "backend": "api",
      "base_url": "http://localhost:3000",
      "endpoints": {
        "list": "/api/artifacts",
        "get": "/api/artifacts/:type/:name",
        "update": "/api/artifacts/:type/:name",
        "create": "/api/artifacts",
        "delete": "/api/artifacts/:type/:name"
      }
    },
    "review_edit_author": {
      "roles": ["reviewer", "editor", "author", "admin"],
      "comment_types": ["suggestion", "issue", "question", "praise"],
      "plan_generation": true
    },
    "consistency_scanning": {
      "canonical_source": "corpus-config.json",
      "term_key": "framework_terms",
      "issue_categories": ["term_misuse", "broken_reference", "style_deviation"]
    },
    "backup_restore": {
      "storage_type": "filesystem",
      "path": "data/backups/",
      "retention": {
        "daily": 7,
        "weekly": 4,
        "monthly": 12
      }
    }
  },
  "project_extensions": [
    "projects/corpushub/plugin-system",
    "projects/corpushub/multi-corpus-support"
  ]
}
```

### Framework Management Adapter Config

```json
{
  "name": "framework-management",
  "version": "4.0.0",
  "core_patterns": {
    "document_management": {
      "backend": "filesystem",
      "base_path": "G:/My Drive/Projects/America40",
      "artifact_types": ["specification", "marketing", "publication"]
    },
    "review_edit_author": {
      "roles": ["reviewer", "editor", "author"],
      "workflow": "browse → comment → plan → implement"
    },
    "consistency_scanning": {
      "canonical_sources": [
        {
          "type": "principles",
          "path": "03-specifications/v1.0/america40.comprehensive-framework-synthesis-streamlined.md",
          "count": 7
        },
        {
          "type": "roles",
          "path": "03-specifications/v1.0/america40.stakeholder-roles.md",
          "count": 14
        },
        {
          "type": "terms",
          "terms": ["Variable Geometry", "Curated Failure", "Attractor Theory"]
        }
      ]
    }
  },
  "project_extensions": [
    "projects/america40/webapp-integration",
    "projects/america40/canonical-sources"
  ]
}
```

---

## Appendix C: Next Steps

### Immediate Actions (This Week)

1. **Get User Approval** on reorganization plan
2. **Create Working Branch** for v4.0.0 development
3. **Set Up Project Tracking** (milestones, issues)
4. **Identify Phase 1 Team** (if applicable)

### Week 1-2 Focus

1. **Start with Most Duplicated Pattern:** review-edit-author
   - Extract from corpus-hub/reviewer, corpus-hub/editor, corpus-hub/author
   - Extract from america40/review, america40/edit, america40/author
   - Create core/patterns/review-edit-author/
   - Test with both domains

2. **Create Configuration System:**
   - Design JSON schema for adapter configs
   - Build config loader utility
   - Create validation for configs

3. **Build Foundation:**
   - Create core/ directory structure
   - Create adapters/ directory structure
   - Create projects/ directory structure
   - Update .gitignore if needed

### Success Metrics (Weekly Check-ins)

- **Week 1:** review-edit-author core pattern complete, tested
- **Week 2:** All 5 core patterns complete
- **Week 3-4:** All 4 adapters complete
- **Week 5:** All size violations fixed
- **Week 6:** All duplicates consolidated
- **Week 7:** Project extensions migrated
- **Week 8:** Documentation complete
- **Week 9:** All tests passing
- **Week 10:** v4.0.0 deployed with backward compatibility

---

## Questions for Discussion

1. **Timeline:** Is 10 weeks realistic? Can we extend to 12-15 weeks?
2. **Breaking Changes:** Acceptable to break backward compatibility in v4.1.0 (after 4-6 week deprecation)?
3. **Priorities:** Are there skills we should migrate first? Last?
4. **Resources:** Do we need additional help for testing/validation?
5. **Scope:** Should we include corpus-hub-v2 or defer to v4.1.0?
6. **Extensions:** Are there other domains we should plan for (future-proofing)?

---

**End of Reorganization Plan**
**Status:** AWAITING APPROVAL
**Next Step:** Review and discussion
