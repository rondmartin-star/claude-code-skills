# Streamlined Audit Integration Plan

**Date:** 2026-01-31
**Purpose:** Show how audit orchestrator integrates seamlessly into universal skills ecosystem
**Repository:** https://github.com/rondmartin-star/claude-code-skills

---

## Integration Philosophy

**Every project is audit-ready from day one:**
1. Project initialized with corpus-config.json (corpus-first)
2. Audit configuration auto-generated based on project type
3. Audits run on-demand or automatically at milestones
4. Convergence available when production-ready
5. All integrated through unified skill loading

---

## Unified Skill Loading Pattern

### Single Entry Point: Project Context

```
User works on ANY project
    ↓
Claude detects corpus-config.json
    ↓
Loads project configuration
    ↓
Makes ALL skills available automatically
    ├─ Corpus management
    ├─ Content workflows (review-edit-author)
    ├─ Development patterns (if applicable)
    ├─ Publishing (if applicable)
    └─ Audit orchestrator (always available)
```

**No explicit skill loading needed** - everything contextual

---

## Project Initialization Flow

### Step 1: Auto-Initialize (Happens Once)

```
User: "Initialize this project"
    ↓
corpus-init detects project type
    ↓
Creates corpus-config.json with:
    ├─ Project metadata
    ├─ Artifact definitions
    ├─ Framework terms (if applicable)
    ├─ Audit configuration (auto-selected)
    └─ Role definitions
    ↓
Creates .corpus/ directory
    ├─ database.sqlite
    ├─ backups/
    └─ audit-logs/
    ↓
Project is now:
    ✓ Corpus-enabled
    ✓ Audit-ready
    ✓ All skills available
```

### Step 2: Natural Workflow Integration

**During Development:**
```
User: "Review this document"
→ Loads review-edit-author (reviewer mode)
→ Comments tracked in .corpus/database.sqlite
→ Generates plans automatically

User: "Edit chapter 3"
→ Loads review-edit-author (editor mode)
→ Checks consistency on save
→ Tracks version history

User: "Create new section"
→ Loads review-edit-author (author mode)
→ Analyzes framework alignment
→ Suggests canonical terms
```

**At Milestones:**
```
User: "Quick quality check"
→ Loads audit-orchestrator (single-run mode)
→ Runs applicable audits
→ Reports issues
→ Suggests fixes

User: "Pre-release validation"
→ Loads audit-orchestrator (convergence mode)
→ Iterates until 3 clean passes
→ Marks project PRODUCTION READY
```

**Continuous:**
```
Automatic triggers (configured):
→ On git commit: Run quick audits
→ On merge to main: Run full audit suite
→ On tag creation: Run convergence audit
→ Daily: Run consistency audit
```

---

## Configuration-Driven Integration

### Single Configuration File

**corpus-config.json controls everything:**

```json
{
  "name": "My Project",
  "type": "web-app",

  // Artifacts define what to manage
  "artifacts": [
    {
      "type": "source-code",
      "location": "src/**/*.js",
      "audit_types": ["security", "quality"]
    },
    {
      "type": "documentation",
      "location": "docs/**/*.md",
      "audit_types": ["content", "navigation"]
    }
  ],

  // Framework terms for consistency
  "framework_terms": {
    "terms": {
      "User Authentication": "OAuth 2.0 with cookie separation",
      "Database Access": "Parameterized queries only"
    }
  },

  // Roles define permissions
  "roles": [
    {"name": "reviewer", "permissions": ["read", "comment"]},
    {"name": "editor", "permissions": ["read", "edit"]},
    {"name": "author", "permissions": ["read", "create"]}
  ],

  // Audits auto-configured
  "audit_config": {
    "applicable_audits": ["security", "quality", "content", "navigation"],
    "auto_run_on": ["commit", "merge", "tag"],
    "convergence": {
      "enabled_for": ["tag"],
      "max_iterations": 10,
      "required_clean_passes": 3
    }
  },

  // Workflow integration
  "workflow": {
    "on_save": ["validate", "consistency_check"],
    "on_comment": ["track_in_database"],
    "on_plan_generate": ["backup_first"],
    "on_audit_fail": ["create_issue_list"]
  }
}
```

**Result:** Entire project behavior controlled from one file

---

## Streamlined Skill Organization

### Flat, Discoverable Structure

```
core/
├── audit/                          # All audit-related
│   ├── orchestrator/               # Main entry (11KB)
│   ├── convergence/               # Iterative workflow (12KB)
│   ├── fix-planner/               # Auto-fix (10KB)
│   └── types/                     # Individual audits
│       ├── consistency/           # (9KB)
│       ├── security/              # (11KB)
│       ├── quality/               # (10KB)
│       ├── performance/           # (10KB)
│       ├── accessibility/         # (9KB)
│       ├── seo/                   # (8KB)
│       ├── content/               # (9KB)
│       ├── navigation/            # (8KB)
│       └── dependency/            # (9KB)
│
├── corpus/                         # Corpus management
│   ├── init/                      # Initialize (11KB)
│   ├── convert/                   # Convert existing (12KB)
│   ├── config/                    # Configuration mgmt (8KB)
│   └── orchestrator/              # Route corpus ops (9KB)
│
├── content/                        # Content workflows
│   ├── review-edit-author/        # REA pattern (12KB)
│   ├── document-management/       # CRUD ops (10KB)
│   ├── version-control/           # History (9KB)
│   └── collaboration/             # Comments, plans (10KB)
│
├── development/                    # Dev patterns
│   ├── windows-app/               # Windows lifecycle
│   └── security/                  # Security patterns
│
├── publishing/                     # Publishing
│   └── content-creation/          # Multi-format (14KB)
│
└── utilities/                      # Shared
    ├── backup-restore/            # Backup (9KB)
    ├── validation/                # Validation (8KB)
    └── orchestration/             # Generic routing (8KB)
```

**Total:** ~25 skills, all <15KB, all universally available

---

## Auto-Loading Logic

### Smart Context Detection

```javascript
function loadSkillsForProject(projectPath) {
  // Always load corpus management
  const skills = ['corpus-orchestrator'];

  // Load project config
  const config = readCorpusConfig(projectPath);

  // Auto-load based on project type
  if (config.type === 'web-app') {
    skills.push('development/windows-app/orchestrator');
    skills.push('development/security/orchestrator');
  }

  if (config.type === 'content-corpus') {
    skills.push('content/review-edit-author');
    skills.push('publishing/content-creation');
  }

  // Audit always available, but load specific types
  skills.push('audit/orchestrator');

  // Load on-demand based on user action
  addEventListener('user_intent', (intent) => {
    if (intent.includes('audit')) {
      loadSkill('audit/orchestrator');
    }
    if (intent.includes('review')) {
      loadSkill('content/review-edit-author', {mode: 'reviewer'});
    }
    if (intent.includes('edit')) {
      loadSkill('content/review-edit-author', {mode: 'editor'});
    }
  });

  return skills;
}
```

---

## Workflow Examples (Streamlined)

### Example 1: New Project Start to Production

```
Day 1: Initialize
User: "Initialize this web app project"
→ corpus-init creates corpus-config.json
→ Detects: type = "web-app", has src/, docs/, package.json
→ Auto-configures: security, quality, performance audits
→ Creates .corpus/ directory
→ Project ready

Day 2-30: Development
User: "Add OAuth login"
→ development/security/authentication loads
→ Implements OAuth with cookie separation
→ Auto-saves to version control
→ Consistency check runs (terms tracked)

User: "Review the login flow"
→ content/review-edit-author (reviewer mode) loads
→ User adds comments
→ Stored in .corpus/database.sqlite

User: "Generate plan from comments"
→ Plan generated automatically
→ User approves
→ Fixes implemented
→ Comments marked resolved

Day 31: Pre-release
User: "Run convergence audit for production"
→ audit/orchestrator loads
→ Runs: security, quality, performance, accessibility, seo, navigation, dependency
→ Iteration 1: 34 issues → auto-fix → 32 successful
→ Iteration 2: 2 issues → auto-fix → 2 successful
→ Iteration 3-5: 0 issues (3 clean passes)
→ PRODUCTION READY ✓

Day 32: Deploy
User: "Deploy to production"
→ development/windows-app/supervision loads
→ Creates MSI installer
→ Sets up NSSM service
→ Health checks configured
→ Deployed ✓
```

### Example 2: Framework Documentation Maintenance

```
Ongoing: Content Management
User: "Review America 4.0 specifications"
→ Detects existing corpus-config.json (type: framework-docs)
→ content/review-edit-author (reviewer mode) loads
→ Canonical sources auto-loaded (7 principles, 14 roles)
→ User navigates and comments

User: "Check consistency"
→ audit/types/consistency loads automatically
→ Scans for term misuse
→ Finds 3 instances of non-canonical terms
→ Suggests corrections
→ Auto-fix applied

Weekly: Quality Check
Automatic trigger (configured)
→ audit/orchestrator runs (single-run mode)
→ Consistency + content + navigation audits
→ Results saved to .corpus/audit-logs/
→ Issues tracked

Quarterly: Full Validation
User: "Run full convergence audit"
→ audit/orchestrator (convergence mode)
→ Iterates until 3 clean passes
→ Framework verified ✓
```

### Example 3: Minimal Friction - Just Works

```
User: "I have a project at /path/to/project"
→ Claude checks for corpus-config.json
→ Not found → "Initialize as corpus-enabled? [Y/n]"
→ User: Y
→ corpus-init runs, detects type, configures
→ Done

User: "Review chapter 3"
→ content/review-edit-author loads (reviewer mode)
→ User works naturally
→ Everything tracked automatically

User: "Is this production ready?"
→ audit/orchestrator loads
→ Runs applicable audits
→ Reports: "12 issues found. Run convergence audit? [Y/n]"
→ User: Y
→ Converges to production ready
→ Done

// NO EXPLICIT SKILL MANAGEMENT NEEDED
// NO CONFIGURATION TWEAKING
// JUST WORKS
```

---

## Integration Points

### 1. Corpus ↔ Audit

```
corpus-config.json
    ↓
Defines artifacts and audit types
    ↓
audit/orchestrator reads config
    ↓
Runs applicable audits on artifacts
    ↓
Results saved to .corpus/audit-logs/
    ↓
Issues tracked in .corpus/database.sqlite
```

### 2. Content Workflows ↔ Audit

```
review-edit-author generates plans
    ↓
Plans trigger consistency audit
    ↓
Audit finds additional issues
    ↓
Issues added to plan
    ↓
Plan implemented
    ↓
Re-audit validates fixes
```

### 3. Development ↔ Audit

```
windows-app/build writes code
    ↓
Auto-triggers security audit
    ↓
Audit finds XSS vulnerability
    ↓
fix-planner generates fix
    ↓
Fix applied automatically
    ↓
Re-audit confirms fixed
```

### 4. All Skills ↔ Backup

```
Before any modification:
    ↓
utilities/backup-restore creates backup
    ↓
Modification attempted
    ↓
If fails: automatic rollback
    ↓
If succeeds: backup retained per policy
```

---

## Key Simplifications

### Before (v3.0)
```
- User needs to know which skill to load
- Manual coordination between skills
- Separate systems (corpus, audit, content)
- Configuration scattered across skills
- Audits run manually, not integrated
```

### After (v4.0)
```
✓ Auto-detection and loading
✓ Skills coordinate automatically
✓ Unified system (everything integrated)
✓ Single configuration file
✓ Audits triggered automatically or on-demand
```

---

## Technical Implementation

### Unified Skill Loader

```javascript
class SkillLoader {
  constructor(projectPath) {
    this.projectPath = projectPath;
    this.config = this.loadConfig();
    this.loadedSkills = new Map();
  }

  loadConfig() {
    const configPath = path.join(this.projectPath, 'corpus-config.json');
    if (!exists(configPath)) {
      // Auto-initialize
      return this.initialize();
    }
    return readJSON(configPath);
  }

  initialize() {
    // Run corpus-init
    const init = require('core/corpus/init');
    return init.run(this.projectPath);
  }

  async handleUserIntent(intent) {
    // Parse intent
    const action = this.detectAction(intent);

    // Load appropriate skill
    switch(action) {
      case 'review':
        return this.loadSkill('content/review-edit-author', {mode: 'reviewer'});
      case 'edit':
        return this.loadSkill('content/review-edit-author', {mode: 'editor'});
      case 'author':
        return this.loadSkill('content/review-edit-author', {mode: 'author'});
      case 'audit':
        return this.loadSkill('audit/orchestrator');
      case 'audit_convergence':
        return this.loadSkill('audit/orchestrator', {mode: 'convergence'});
      // ... more cases
    }
  }

  loadSkill(skillPath, options = {}) {
    // Check if already loaded
    if (this.loadedSkills.has(skillPath)) {
      return this.loadedSkills.get(skillPath);
    }

    // Load skill
    const skill = require(`core/${skillPath}`);

    // Configure from corpus-config.json
    skill.configure(this.config, options);

    // Cache
    this.loadedSkills.set(skillPath, skill);

    return skill;
  }

  async onTrigger(trigger, data) {
    // Handle automatic triggers
    const triggers = this.config.workflow[trigger] || [];

    for (const action of triggers) {
      await this.executeAction(action, data);
    }
  }
}

// Usage
const loader = new SkillLoader('/path/to/project');

// User says: "Review chapter 3"
await loader.handleUserIntent("Review chapter 3");

// Automatic trigger on save
await loader.onTrigger('on_save', {file: 'chapter-3.md'});
```

---

## Migration from v3.0

### Automatic Migration

```bash
# User has v3.0 project
/project
├── america40/
│   └── shared/
│       ├── consistency-engine/
│       └── backup-archive/

# Run migration
User: "Migrate to v4.0"

# Migration tool:
1. Detects v3.0 structure
2. Creates corpus-config.json
3. Moves data to .corpus/
4. Updates references
5. Creates forwarding from old to new
6. Validates migration
7. Done

# Result
/project
├── corpus-config.json         # NEW
├── .corpus/                   # NEW
│   ├── database.sqlite
│   └── backups/
├── america40/                 # Unchanged
│   └── shared/
│       ├── consistency-engine/  # Now forwards to core/audit/types/consistency
│       └── backup-archive/      # Now forwards to core/utilities/backup-restore
```

---

## Performance Optimization

### Lazy Loading

Only load skills when needed:

```javascript
// Initial load: Just config
const config = readCorpusConfig();  // <1ms

// User action triggers load
User: "Review chapter 3"
→ Load review-edit-author ONLY      // ~50ms
→ Don't load audit, publishing, etc.

// Later action
User: "Run audit"
→ Load audit/orchestrator ONLY      // ~50ms
→ Load specific audit types on-demand
```

### Skill Size Targets

All skills <15KB = Fast loading:
- 15KB SKILL.md ~ 50-100ms load time
- Reference files loaded on-demand
- Total context usage optimized

### Caching

```javascript
// Skills loaded once, cached
const cache = new Map();

function loadSkill(path) {
  if (cache.has(path)) {
    return cache.get(path);  // <1ms
  }
  const skill = require(path);  // ~50ms
  cache.set(path, skill);
  return skill;
}
```

---

## User Experience Goals

### Invisible Integration

**User never thinks about:**
- Which skill to load
- How skills coordinate
- Where data is stored
- When audits run
- How configuration works

**User just:**
- Works on their project naturally
- Gets suggestions and validations
- Approves fixes when needed
- Sees "PRODUCTION READY" when done

### Progressive Disclosure

**Level 1: Just Works**
```
User: "Initialize project"
→ Done
User: "Review this"
→ Done
User: "Is it ready?"
→ "Yes, production ready"
```

**Level 2: Some Control**
```
User: "Run only security audit"
→ Specific audit runs
User: "Don't auto-fix, just report"
→ Configuration respected
```

**Level 3: Full Control**
```
User edits corpus-config.json
→ Full customization
User: "Run convergence with 15 iterations"
→ Override defaults
```

---

## Success Criteria (Integration)

- [ ] User can initialize any project in <10 seconds
- [ ] All skills available without explicit loading
- [ ] Single configuration file controls everything
- [ ] Automatic triggers work reliably
- [ ] Convergence audit runs to completion
- [ ] Zero configuration needed for defaults
- [ ] Migration from v3.0 is automatic
- [ ] Performance: <100ms skill loading
- [ ] User experience: "just works"

---

**Status:** Integration Plan Complete
**Next:** Implement unified skill loader
**Repository:** https://github.com/rondmartin-star/claude-code-skills
