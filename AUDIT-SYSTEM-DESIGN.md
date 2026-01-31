# Audit System Design: Orchestrator + Convergence

**Version:** 4.0.0 (Proposed)
**Date:** 2026-01-31
**Status:** DESIGN SPECIFICATION
**Type:** Core Pattern

---

## Overview

A comprehensive audit system with convergence capability that runs multiple audit types, identifies issues, plans fixes, implements solutions, and repeats until the project reaches a stable clean state (3 consecutive clean passes).

**Purpose:** Late-stage quality assurance for production-ready applications and content

**Use Cases:**
- Pre-release quality checks
- Production readiness audits
- Content publication validation
- Framework compliance verification
- Security hardening
- Performance optimization

---

## Architecture

```
core/patterns/audit-system/
├── audit-orchestrator/             # Main entry point
│   └── SKILL.md                    # Routes to audit types, manages convergence
│
├── audits/                         # Individual audit types
│   ├── consistency-audit/          # Term usage, cross-references
│   ├── security-audit/             # XSS, CSRF, SQL injection, OAuth
│   ├── quality-audit/              # Code quality, test coverage
│   ├── performance-audit/          # Load time, bundle size, queries
│   ├── accessibility-audit/        # WCAG compliance, ARIA
│   ├── seo-audit/                  # Meta tags, structure, sitemap
│   ├── content-audit/              # Grammar, style, formatting
│   ├── navigation-audit/           # Broken links, unreachable pages
│   └── dependency-audit/           # Outdated packages, vulnerabilities
│
├── convergence-engine/             # Convergence algorithm
│   └── SKILL.md                    # Run audits until stable
│
└── fix-planner/                    # Issue → plan → implementation
    └── SKILL.md                    # Generate and execute fix plans
```

---

## Audit Orchestrator

### Purpose

Routes to appropriate audit types based on project context and coordinates convergence workflow.

### Detection Logic

```javascript
function detectApplicableAudits(projectType, phase) {
  const audits = [];

  // All projects get these
  audits.push('consistency-audit', 'navigation-audit');

  // Project-type specific
  if (projectType === 'web-app') {
    audits.push('security-audit', 'performance-audit', 'accessibility-audit', 'seo-audit');
  }

  if (projectType === 'content-corpus') {
    audits.push('content-audit', 'consistency-audit');
  }

  if (projectType === 'framework-docs') {
    audits.push('content-audit', 'consistency-audit', 'navigation-audit');
  }

  if (projectType === 'windows-app') {
    audits.push('security-audit', 'quality-audit', 'dependency-audit');
  }

  // Phase-specific
  if (phase === 'pre-release') {
    audits.push(...allAudits); // Run everything
  }

  return audits;
}
```

### Routing Matrix

| Project Type | Audits |
|--------------|--------|
| **Web Application** | security, performance, accessibility, seo, quality, navigation, dependency |
| **Content Corpus** | consistency, content, navigation |
| **Framework Docs** | consistency, content, navigation |
| **Windows Application** | security, quality, dependency |
| **Publishing Content** | content, seo, accessibility |

---

## Convergence Engine

### Purpose

Iteratively run audits → identify issues → plan fixes → implement → verify until system reaches stable state.

### Convergence Algorithm

```
CONVERGENCE_WORKFLOW:

  Initialize:
    convergence_cycle = 0
    max_cycles = 5
    production_ready = false

  # OUTER LOOP: Convergence → User Validation cycles
  While NOT production_ready AND convergence_cycle < max_cycles:
    convergence_cycle++

    # ============================================
    # PHASE 1: AUTOMATED CONVERGENCE (GATE)
    # ============================================
    # Don't waste user time on detectable issues
    # Converge to 3 consecutive clean automated passes

    consecutive_clean_passes = 0
    max_iterations = 10
    iteration = 0

    While consecutive_clean_passes < 3 AND iteration < max_iterations:
      iteration++

      # Run all applicable audits
      audit_results = run_all_audits(project)

      # Classify issues
      issues = classify_issues(audit_results)

      # Check if clean
      if issues.count == 0:
        consecutive_clean_passes++
        continue
      else:
        consecutive_clean_passes = 0  # Reset

      # Prioritize and fix
      prioritized = prioritize_issues(issues)
      plan = generate_fix_plan(prioritized)

      # Optional approval gate
      if require_approval:
        approved = await user_approval(plan)
        if not approved:
          ABORT

      # Implement fixes
      results = implement_fixes(plan)
      log_iteration(iteration, issues, results)

    # Check automated convergence status
    if consecutive_clean_passes < 3:
      status = "AUTOMATED CONVERGENCE FAILED"
      ABORT

    log("✓ Automated convergence complete (3 clean passes)")

    # ============================================
    # PHASE 2: USER VALIDATION (CLEAN SYSTEM)
    # ============================================
    # Now that automation is clean, get real user testing
    # Users focus on UX, edge cases, integration issues

    user_results = run_user_validation(project)

    if user_results.issues.count == 0:
      production_ready = true
      status = "PRODUCTION READY"
      log("✓ User validation clean - PRODUCTION READY")
    else:
      log("⚠ User found {user_results.issues.count} issues")
      log("→ Returning to automated convergence...")
      # Back to PHASE 1 (automated convergence)

  # Final status
  if production_ready:
    status = "PRODUCTION READY"
  elif convergence_cycle >= max_cycles:
    status = "MAX CYCLES - Manual Review Required"

  generate_final_report(status, convergence_cycle, all_logs)
```

### Convergence Criteria

**Success:** 3 consecutive clean passes
- Pass 1: No new issues found
- Pass 2: Still no issues (confirms Pass 1 wasn't false positive)
- Pass 3: Stable state confirmed → **PRODUCTION READY**

**Failure Modes:**
- **Max Iterations (10):** System not converging, manual review needed
- **User Abort:** User intervention required
- **Critical Blocker:** Unfixable issue detected

### Safety Mechanisms

1. **Max Iterations:** Prevent infinite loops (default: 10)
2. **User Approval:** Optional approval gates for each fix plan
3. **Rollback Capability:** Backup before each fix implementation
4. **Issue Tracking:** Log all issues and fixes for audit trail
5. **Progress Monitoring:** Real-time status updates

---

## Individual Audit Types

### 1. Consistency Audit

**Purpose:** Verify term usage, cross-references, canonical definitions

**Checks:**
- Term misuse (non-standard terms used)
- Broken cross-references
- Definition inconsistencies
- Style guide violations

**Inputs:**
- Canonical sources (corpus-config.json or framework definitions)
- All documents/artifacts

**Outputs:**
```json
{
  "audit_type": "consistency",
  "issues": [
    {
      "severity": "critical",
      "category": "term_misuse",
      "location": "chapter-3.md:42",
      "found": "industrial policy",
      "expected": "strategic industrial investment",
      "fix": "Replace with canonical term"
    }
  ]
}
```

### 2. Security Audit

**Purpose:** Identify security vulnerabilities

**Checks:**
- XSS vulnerabilities (unescaped user input)
- CSRF protection missing
- SQL injection risks
- Insecure authentication
- Exposed secrets/credentials
- HTTPS not enforced
- Weak password policies
- Missing security headers

**Inputs:**
- Source code (all files)
- Configuration files
- Environment variables

**Outputs:**
```json
{
  "audit_type": "security",
  "issues": [
    {
      "severity": "critical",
      "category": "xss",
      "location": "views/profile.ejs:23",
      "vulnerability": "User input not escaped",
      "fix": "Use <%- name %> → <%= name %>"
    }
  ]
}
```

### 3. Quality Audit

**Purpose:** Code quality and testing validation

**Checks:**
- Test coverage < 80%
- Linting errors
- Code complexity (cyclomatic complexity)
- Dead code
- Duplicate code
- Missing documentation

**Inputs:**
- Source code
- Test files
- Coverage reports

**Outputs:**
```json
{
  "audit_type": "quality",
  "issues": [
    {
      "severity": "warning",
      "category": "coverage",
      "location": "src/auth.js",
      "coverage": "45%",
      "threshold": "80%",
      "fix": "Add tests for untested functions"
    }
  ]
}
```

### 4. Performance Audit

**Purpose:** Performance bottlenecks and optimization

**Checks:**
- Page load time > 3s
- Bundle size > 500KB
- Unoptimized images
- Missing caching headers
- N+1 query problems
- Memory leaks

**Inputs:**
- Build output
- Network requests
- Database queries

**Outputs:**
```json
{
  "audit_type": "performance",
  "issues": [
    {
      "severity": "warning",
      "category": "bundle_size",
      "location": "dist/main.js",
      "size": "847KB",
      "threshold": "500KB",
      "fix": "Enable code splitting, tree shaking"
    }
  ]
}
```

### 5. Accessibility Audit

**Purpose:** WCAG 2.1 AA compliance

**Checks:**
- Missing alt text on images
- Insufficient color contrast
- Missing ARIA labels
- Keyboard navigation issues
- Missing skip links
- Form labels missing

**Inputs:**
- HTML files
- CSS stylesheets

**Outputs:**
```json
{
  "audit_type": "accessibility",
  "issues": [
    {
      "severity": "critical",
      "category": "alt_text",
      "location": "index.html:45",
      "element": "<img src='logo.png'>",
      "fix": "Add alt='Company Logo'"
    }
  ]
}
```

### 6. SEO Audit

**Purpose:** Search engine optimization validation

**Checks:**
- Missing meta description
- Missing title tags
- Missing sitemap.xml
- Missing robots.txt
- Broken canonical URLs
- Missing Open Graph tags

**Inputs:**
- HTML files
- Site structure

**Outputs:**
```json
{
  "audit_type": "seo",
  "issues": [
    {
      "severity": "warning",
      "category": "meta",
      "location": "about.html",
      "missing": "meta description",
      "fix": "Add <meta name='description' content='...'>"
    }
  ]
}
```

### 7. Content Audit

**Purpose:** Content quality validation

**Checks:**
- Grammar and spelling errors
- Style guide compliance
- Broken formatting
- Missing sections (required structure)
- Readability score < threshold

**Inputs:**
- Content files (markdown, HTML, etc.)
- Style guide configuration

**Outputs:**
```json
{
  "audit_type": "content",
  "issues": [
    {
      "severity": "info",
      "category": "grammar",
      "location": "chapter-1.md:23",
      "error": "Their vs They're",
      "fix": "Replace 'their' with 'they're'"
    }
  ]
}
```

### 8. Navigation Audit

**Purpose:** Navigation structure and link validation

**Checks:**
- Broken internal links
- Broken external links
- Orphaned pages (unreachable)
- Circular navigation loops
- Missing breadcrumbs
- Inconsistent navigation structure

**Inputs:**
- All pages/artifacts
- Navigation configuration

**Outputs:**
```json
{
  "audit_type": "navigation",
  "issues": [
    {
      "severity": "critical",
      "category": "broken_link",
      "location": "docs/api.md:12",
      "link": "/docs/auth.md",
      "status": "404",
      "fix": "Update link to /docs/authentication.md"
    }
  ]
}
```

### 9. Dependency Audit

**Purpose:** Dependency security and freshness

**Checks:**
- Known vulnerabilities (npm audit, Snyk)
- Outdated packages
- License compliance
- Unused dependencies

**Inputs:**
- package.json, requirements.txt, etc.
- Lock files

**Outputs:**
```json
{
  "audit_type": "dependency",
  "issues": [
    {
      "severity": "critical",
      "category": "vulnerability",
      "package": "lodash@4.17.15",
      "cve": "CVE-2021-23337",
      "fix": "Update to lodash@4.17.21"
    }
  ]
}
```

---

## Fix Planner

### Purpose

Converts audit issues into actionable fix plans and implements them.

### Plan Generation

```javascript
function generateFixPlan(issues) {
  const plan = {
    id: generatePlanId(),
    timestamp: Date.now(),
    issues_count: issues.length,
    fixes: []
  };

  // Group issues by file/location
  const grouped = groupByLocation(issues);

  for (const [location, locationIssues] of grouped) {
    const fix = {
      location: location,
      issues: locationIssues,
      actions: [],
      estimated_risk: calculateRisk(locationIssues),
      backup_required: true
    };

    // Generate fix actions
    for (const issue of locationIssues) {
      const action = determineFixAction(issue);
      fix.actions.push(action);
    }

    plan.fixes.push(fix);
  }

  // Prioritize fixes (critical first)
  plan.fixes.sort((a, b) =>
    getPriority(b.issues) - getPriority(a.issues)
  );

  return plan;
}
```

### Fix Implementation

```javascript
async function implementFixes(plan) {
  const results = {
    plan_id: plan.id,
    fixes_attempted: 0,
    fixes_successful: 0,
    fixes_failed: 0,
    errors: []
  };

  for (const fix of plan.fixes) {
    results.fixes_attempted++;

    try {
      // Create backup
      if (fix.backup_required) {
        await createBackup(fix.location);
      }

      // Execute fix actions
      for (const action of fix.actions) {
        await executeFix(action);
      }

      // Verify fix
      const verified = await verifyFix(fix);

      if (verified) {
        results.fixes_successful++;
      } else {
        results.fixes_failed++;
        results.errors.push({
          location: fix.location,
          error: "Fix verification failed"
        });

        // Rollback
        await rollback(fix.location);
      }

    } catch (error) {
      results.fixes_failed++;
      results.errors.push({
        location: fix.location,
        error: error.message
      });

      // Rollback on error
      await rollback(fix.location);
    }
  }

  return results;
}
```

### Automatic Fix Strategies

| Issue Type | Fix Strategy | Automation Level |
|------------|--------------|------------------|
| **Term misuse** | Replace with canonical term | Fully automatic |
| **Broken link** | Update to correct path | Fully automatic |
| **Missing alt text** | Generate descriptive alt text | AI-assisted |
| **Security (XSS)** | Escape user input | Fully automatic |
| **Missing meta tag** | Add required meta tag | Template-based |
| **Outdated dependency** | Update to latest secure version | Fully automatic |
| **Code formatting** | Run prettier/eslint --fix | Fully automatic |
| **Grammar error** | Suggest correction | User approval required |
| **Performance issue** | Suggest optimization | User approval required |

---

## Corpus-First Approach

### Why Corpus as Default

**Traceability:**
- Every artifact tracked in corpus-config.json
- Full version history
- Comment and plan tracking
- Consistency scanning built-in

**Content Management:**
- Centralized metadata
- Cross-reference management
- Framework term enforcement
- Multi-role collaboration

**Audit Integration:**
- All audits corpus-aware
- Canonical source integration
- Automatic issue tracking
- Fix plan persistence

### Default Project Structure

All projects now initialized as corpus-enabled by default:

```
project-root/
├── corpus-config.json          # Created automatically
│   ├── artifacts: [...]        # Auto-detected
│   ├── framework_terms: {...}  # Empty initially
│   ├── voice: {...}            # Default template
│   └── roles: [...]            # Default: reviewer, editor, author, admin
│
├── .corpus/                    # Corpus metadata
│   ├── database.sqlite         # Comments, plans, history
│   ├── backups/               # Automatic backups
│   └── audit-logs/            # Convergence audit logs
│
├── [project files...]          # Actual project content
│
└── README.md                   # Auto-generated with corpus info
```

### corpus-config.json Template

```json
{
  "name": "Project Name",
  "slug": "project-name",
  "version": "1.0.0",
  "type": "web-app" | "content-corpus" | "framework-docs" | "windows-app",

  "artifacts": [
    {
      "type": "source-code",
      "location": "src/**/*.js",
      "editable": true,
      "audit_types": ["security", "quality", "performance"]
    },
    {
      "type": "documentation",
      "location": "docs/**/*.md",
      "editable": true,
      "audit_types": ["content", "navigation", "consistency"]
    }
  ],

  "framework_terms": {
    "canonical_sources": [],
    "terms": {}
  },

  "voice": {
    "tone": "professional",
    "audience": "developers",
    "style_guide": "default"
  },

  "roles": [
    {
      "name": "reviewer",
      "permissions": ["read", "comment", "generate_plan"]
    },
    {
      "name": "editor",
      "permissions": ["read", "comment", "edit", "preview"]
    },
    {
      "name": "author",
      "permissions": ["read", "comment", "create", "analyze"]
    },
    {
      "name": "admin",
      "permissions": ["all"]
    }
  ],

  "audit_config": {
    "auto_run": false,
    "convergence": {
      "enabled": false,
      "max_iterations": 10,
      "required_clean_passes": 3,
      "approval_required": true
    },
    "applicable_audits": [
      "consistency",
      "navigation",
      "security",
      "quality"
    ]
  }
}
```

### Auto-Detection Logic

```javascript
function initializeCorpus(projectPath) {
  const config = {
    name: detectProjectName(projectPath),
    slug: slugify(projectPath),
    type: detectProjectType(projectPath),
    artifacts: []
  };

  // Auto-detect artifacts
  if (exists(projectPath + '/src')) {
    config.artifacts.push({
      type: 'source-code',
      location: 'src/**/*',
      editable: true
    });
  }

  if (exists(projectPath + '/docs')) {
    config.artifacts.push({
      type: 'documentation',
      location: 'docs/**/*.md',
      editable: true
    });
  }

  // Detect project type
  if (exists(projectPath + '/package.json')) {
    const pkg = readJSON(projectPath + '/package.json');
    if (pkg.dependencies?.express) {
      config.type = 'web-app';
    }
  }

  // Set applicable audits based on type
  config.audit_config.applicable_audits =
    detectApplicableAudits(config.type);

  return config;
}
```

---

## Integration with Reorganization Plan

### Updated Core Patterns (Tier 1)

```
core/patterns/
├── audit-system/               # NEW: Comprehensive audit orchestrator
│   ├── audit-orchestrator/
│   ├── convergence-engine/
│   ├── fix-planner/
│   └── audits/
│       ├── consistency-audit/
│       ├── security-audit/
│       ├── quality-audit/
│       ├── performance-audit/
│       ├── accessibility-audit/
│       ├── seo-audit/
│       ├── content-audit/
│       ├── navigation-audit/
│       └── dependency-audit/
│
├── corpus-management/          # PROMOTED: From adapter to core pattern
│   ├── corpus-init/            # Auto-initialize any project
│   ├── corpus-convert/         # Convert existing projects
│   ├── corpus-config/          # Configuration management
│   └── corpus-adapter/         # Domain-specific adapters
│
├── document-management/        # Existing
├── review-edit-author/         # Existing
├── consistency-scanning/       # NOW: Part of audit-system
├── backup-restore/             # Existing
└── orchestration/              # Existing
```

### Updated Architecture

**Corpus-First Principle:**
- All projects initialized with corpus-config.json by default
- All core patterns are corpus-aware
- Audit system integrates with corpus metadata
- Traceability built into every operation

---

## Usage Examples

### Example 1: Pre-Release Convergence Audit

```bash
# User initiates convergence audit
"Run convergence audit for pre-release"

→ audit-orchestrator loads
→ Detects project type: web-app
→ Loads applicable audits: security, performance, accessibility, seo, quality, navigation, dependency, consistency
→ Starts convergence-engine

Iteration 1:
  - Run all 8 audits
  - Found 47 issues (12 critical, 23 warning, 12 info)
  - Generate fix plan
  - User approval: YES
  - Implement 47 fixes
  - 45 successful, 2 failed (manual review flagged)

Iteration 2:
  - Run all 8 audits
  - Found 2 issues (manual review from iteration 1)
  - Generate fix plan
  - User approval: YES
  - Implement 2 fixes
  - 2 successful

Iteration 3:
  - Run all 8 audits
  - Found 0 issues
  - Clean pass 1/3

Iteration 4:
  - Run all 8 audits
  - Found 0 issues
  - Clean pass 2/3

Iteration 5:
  - Run all 8 audits
  - Found 0 issues
  - Clean pass 3/3

CONVERGED - Production Ready ✓
```

### Example 2: Content Corpus Audit

```bash
# User initiates audit for America 4.0 framework
"Audit America 4.0 framework for consistency"

→ audit-orchestrator loads
→ Detects project type: framework-docs
→ Loads applicable audits: consistency, content, navigation
→ Starts convergence-engine

Iteration 1:
  - consistency-audit: 8 term misuses found
  - content-audit: 3 grammar errors
  - navigation-audit: 1 broken link
  - Total: 12 issues
  - Auto-fix all (user approval: YES)
  - 12 successful

Iteration 2:
  - All audits clean
  - Clean pass 1/3

Iteration 3:
  - All audits clean
  - Clean pass 2/3

Iteration 4:
  - All audits clean
  - Clean pass 3/3

CONVERGED - Production Ready ✓
```

---

## File Structure

### audit-orchestrator/SKILL.md (8KB)

```markdown
---
name: audit-orchestrator
description: >
  Comprehensive audit orchestrator that routes to applicable audit types and
  coordinates convergence workflow for production readiness. Use when: running
  pre-release audits, validating quality, or ensuring production readiness.
---

# Audit Orchestrator

Purpose: Coordinate comprehensive audits and convergence workflow

## When to Load

- "Run convergence audit"
- "Pre-release audit"
- "Production readiness check"
- "Audit everything"
- "Quality validation"

## Detection Logic

[Routing matrix table]

## Available Audits

| Audit | Purpose | Applicable To |
|-------|---------|---------------|
| consistency | Term usage, cross-refs | All projects |
| security | XSS, CSRF, SQL injection | Web apps, APIs |
| quality | Test coverage, linting | All code projects |
| performance | Load time, bundle size | Web apps |
| accessibility | WCAG compliance | Web apps |
| seo | Meta tags, sitemap | Websites |
| content | Grammar, style | All content |
| navigation | Broken links, orphans | All projects |
| dependency | Vulnerabilities | All code projects |

## Workflow

1. Detect project type from corpus-config.json
2. Load applicable audits
3. Route to convergence-engine or single-audit
4. Return results with fix recommendations

See: references/audit-routing.md for detailed routing logic
```

### convergence-engine/SKILL.md (12KB)

```markdown
---
name: convergence-engine
description: >
  Iterative audit workflow that runs audits, identifies issues, plans fixes,
  implements solutions, and repeats until 3 consecutive clean passes. Expensive
  operation for late-stage production readiness. Use when: preparing for release.
---

# Convergence Engine

Purpose: Achieve stable production-ready state through iterative audits

## Algorithm

[Detailed convergence algorithm]

## Safety Mechanisms

- Max iterations: 10 (configurable)
- User approval gates (optional)
- Automatic backups before fixes
- Rollback on fix failure
- Progress logging

## Success Criteria

3 consecutive clean passes = PRODUCTION READY

## Configuration

Via corpus-config.json:
```json
{
  "audit_config": {
    "convergence": {
      "enabled": true,
      "max_iterations": 10,
      "required_clean_passes": 3,
      "approval_required": true
    }
  }
}
```

See: references/convergence-examples.md for usage examples
```

---

## Implementation Priority

### Immediate (Week 1-2)

1. **Create audit-orchestrator skeleton**
   - Basic routing logic
   - Project type detection
   - Audit registry

2. **Implement convergence-engine**
   - Core algorithm
   - Iteration tracking
   - Clean pass detection

3. **Port existing audits**
   - navigation-auditor → navigation-audit
   - consistency-engine → consistency-audit

### Short-term (Week 3-4)

4. **Create missing audits**
   - security-audit (extract from secure-coding-patterns)
   - quality-audit (new)
   - content-audit (new)

5. **Build fix-planner**
   - Plan generation
   - Automatic fix strategies
   - User approval flow

### Medium-term (Week 5-6)

6. **Implement remaining audits**
   - performance-audit
   - accessibility-audit
   - seo-audit
   - dependency-audit

7. **Integration testing**
   - Full convergence workflow
   - Multi-project validation

---

## Success Metrics

- [ ] All 9 audit types implemented
- [ ] Convergence algorithm stable
- [ ] Fix planner >80% auto-fix rate
- [ ] Integration with corpus-config.json
- [ ] All skills <15KB
- [ ] Full test coverage
- [ ] Documentation complete

---

**End of Audit System Design**
**Status:** READY FOR IMPLEMENTATION
**Next Step:** Create audit-orchestrator/SKILL.md
