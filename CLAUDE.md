# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Claude Code Skills Ecosystem

**Project:** Claude Code Skills Library
**Type:** Meta-Project (Skill Management System)
**Version:** 3.0.0
**Owner:** Pterodactyl Holdings, LLC
**Status:** Production

---

## Repository Overview

This repository contains a comprehensive ecosystem of Claude Code skills organized into five major categories:

1. **meta/** - Ecosystem management and skill development tools
2. **windows-app/** - Full Windows application development lifecycle
3. **publishing/** - Multi-platform content creation
4. **america40/** - America 4.0 framework review and update system
5. **corpus-hub/** - Corpus management platform with plugin architecture

Each category contains orchestrator skills that route to specialized sub-skills based on context.

---

## Architecture

### Core Patterns

**Hierarchical Orchestrators**: Top-level orchestrators analyze intent and route to specialized skills
- Orchestrators are lightweight (<10KB) and focus on routing logic
- Specialized skills contain domain expertise and detailed guidance
- Skills load reference files on-demand to stay under size limits

**Size Optimization**:
- SKILL.md target: <15KB (essential guidance only)
- Detailed examples and templates in `references/` subdirectories
- Load reference files only when needed for specific tasks

**Fool-Proof Design**:
- Sensible defaults that work out-of-the-box
- Auto-detect and auto-configure where possible
- Clear error messages with actionable guidance
- Designed for users with varying technical backgrounds

**Golden Rule - Never Rebuild**:
- Always iterate on existing baselines
- Preserve working state
- Track changes in CHANGELOG.md files
- Make minimal, targeted changes only

**Error-Driven Improvement**:
- Log errors in ERROR-AND-FIXES-LOG.md
- Create regression tests for fixed issues
- Update skills based on real-world problems
- Continuous refinement based on actual usage

---

## Directory Structure

```
skills/
├── CLAUDE.md                       # This file
├── README.md                       # Ecosystem overview
├── tools/                          # Validation and packaging utilities
│   ├── quick_validate.py           # SKILL.md frontmatter validation
│   └── package_skill.py            # Package skills for distribution
│
├── meta/                           # Ecosystem management (4 skills)
│   ├── skill-ecosystem-manager/    # Create and maintain skills
│   ├── conversation-snapshot/      # Portable context preservation
│   ├── navigation-auditor/         # Verify navigation paths
│   └── plugin-ecosystem/           # External plugin integrations
│
├── windows-app/                    # Windows development (8 skills)
│   ├── windows-app-orchestrator/   # Phase coordinator
│   ├── windows-app-requirements/   # User stories & acceptance criteria
│   ├── windows-app-system-design/  # Data models & API design
│   ├── windows-app-ui-design/      # Page inventory & navigation
│   ├── windows-app-build/          # Implementation & testing
│   ├── windows-app-supervision/    # NSSM service & MSI packaging
│   └── security/                   # Security sub-category (3 skills)
│       ├── security-patterns-orchestrator/
│       ├── authentication-patterns/  # OAuth-first authentication
│       └── secure-coding-patterns/   # XSS, CSRF, SQL injection prevention
│
├── publishing/                     # Content creation (2 skills)
│   ├── publishing-orchestrator/
│   └── content-creation-ecosystem/ # HTML-first with DOCX/PDF export
│
├── america40/                      # America 4.0 framework (7+ skills)
│   ├── america40-orchestrator/     # Role-based routing
│   ├── review/                     # Reviewer role
│   ├── edit/                       # Editor role
│   ├── author/                     # Author role
│   ├── shared/                     # Shared utilities
│   │   ├── backup-archive/
│   │   ├── consistency-engine/
│   │   ├── framework-context/
│   │   └── implementation-executor/
│   └── webapp-extensions/          # Reference Hub webapp specs
│
└── corpus-hub/                     # Corpus management (10+ skills)
    ├── corpus-hub-orchestrator/    # Intent detection & routing
    ├── setup/                      # Initialization & conversion
    │   ├── corpus-init/            # New project setup
    │   └── corpus-convert/         # Convert existing projects
    ├── reviewer/                   # Browse, comment, plan changes
    ├── editor/                     # Modify artifacts with AI
    ├── author/                     # Create new drafts
    ├── admin/                      # User mgmt, backups, health
    ├── management/
    │   └── corpus-status/          # Status tracking
    └── shared/                     # Shared utilities
        ├── consistency-engine/
        ├── corpus-config/
        ├── project-templates/
        └── backup-archive/
```

---

## Common Development Tasks

### Validating Skills

Validate SKILL.md frontmatter and structure:

```bash
# Validate a single skill
python tools/quick_validate.py path/to/skill-directory

# Example
python tools/quick_validate.py meta/skill-ecosystem-manager
```

**Validation checks**:
- YAML frontmatter exists and is valid
- Required fields: `name`, `description`
- Name follows kebab-case convention
- Description doesn't contain angle brackets
- No unexpected frontmatter properties

### Packaging Skills

Package a skill for distribution:

```bash
# Package to current directory
python tools/package_skill.py path/to/skill-directory

# Package to specific output directory
python tools/package_skill.py path/to/skill-directory ./dist

# Example
python tools/package_skill.py meta/conversation-snapshot ./dist
```

Creates a `.skill` file (zip format) containing the entire skill directory.

### Checking Skill Sizes

Monitor SKILL.md file sizes to ensure compliance with <15KB target:

```bash
# Check size of a specific SKILL.md
wc -c windows-app/windows-app-build/SKILL.md

# Find all SKILL.md files over 15KB
find . -name "SKILL.md" -exec wc -c {} \; | awk '$1 > 15360 {print}'
```

### Finding Skills

Locate all SKILL.md files:

```bash
find . -name "SKILL.md"
```

Find skills by pattern:

```bash
# Find all orchestrators
find . -name "*orchestrator*" -type d

# Find all shared utilities
find . -path "*/shared/*" -name "SKILL.md"
```

---

## Skill Loading and Navigation

### Entry Points by Category

**Meta Skills** (Ecosystem Management):
- "Create a new skill" → skill-ecosystem-manager
- "Save this conversation" → conversation-snapshot
- "Audit navigation" → navigation-auditor
- "Manage plugins" → plugin-ecosystem

**Windows Development**:
- "Build a Windows app" → windows-app-orchestrator
- "Start coding" → windows-app-build
- "Add OAuth login" → security-patterns-orchestrator → authentication-patterns
- "Security audit" → security-patterns-orchestrator → secure-coding-patterns
- "Deploy to production" → windows-app-supervision

**Content Creation**:
- "Write a blog post" → publishing-orchestrator → content-creation-ecosystem
- "Create newsletter" → publishing-orchestrator → content-creation-ecosystem

**America 4.0 Framework**:
- "Review framework docs" → america40-orchestrator → review-orchestrator
- "Edit specifications" → america40-orchestrator → edit-orchestrator
- "Draft new content" → america40-orchestrator → author-orchestrator

**CorpusHub Platform**:
- "Initialize corpus" → corpus-hub-orchestrator → corpus-init
- "Convert project to corpus" → corpus-hub-orchestrator → corpus-convert
- "Review artifacts" → corpus-hub-orchestrator → reviewer
- "Edit documents" → corpus-hub-orchestrator → editor
- "Create new content" → corpus-hub-orchestrator → author
- "Manage corpus" → corpus-hub-orchestrator → admin

### Orchestrator Routing Logic

**windows-app-orchestrator**: Routes by development phase
```
Requirements → windows-app-requirements
Design (data) → windows-app-system-design
Design (UI) → windows-app-ui-design
Implementation → windows-app-build
  ├─ Auth/Security → security-patterns-orchestrator
  │   ├─ OAuth/Sessions → authentication-patterns
  │   └─ Input Validation → secure-coding-patterns
Deployment → windows-app-supervision
```

**security-patterns-orchestrator**: Routes by security context
```
Authentication → authentication-patterns
Secure Coding → secure-coding-patterns
```

**publishing-orchestrator**: Routes by content type
```
Social Media → content-creation-ecosystem (social-media.md)
Newsletter → content-creation-ecosystem (newsletter.md)
Blog/Website → content-creation-ecosystem (website.md)
Journal → content-creation-ecosystem (journal.md)
```

**america40-orchestrator**: Routes by user role
```
Reviewer → review-orchestrator
Editor → edit-orchestrator
Author → author-orchestrator
Consistency → shared/consistency-engine
```

**corpus-hub-orchestrator**: Routes by intent and role
```
Setup (new) → setup/corpus-init
Setup (existing) → setup/corpus-convert
Review → reviewer
Edit → editor
Create → author
Admin → admin
Status → management/corpus-status
```

---

## Key Architectural Concepts

### SKILL.md Structure

Every skill follows this pattern:

```yaml
---
name: skill-name-in-kebab-case
description: >
  Brief description of what this skill does.
  Use when: [specific trigger conditions]
---

# Skill Name

[Essential guidance and instructions]

## When to Load This Skill

[Clear trigger phrases and context indicators]

## Core Guidance

[Key patterns, checklists, decision trees]

## Reference Files

[Links to detailed examples in references/ subdirectory]
```

### Reference Files

To keep SKILL.md files small, detailed content lives in `references/`:

```
skill-name/
├── SKILL.md                    # Core guidance (<15KB)
├── README.md                   # Quick reference
├── references/                 # Detailed documentation
│   ├── examples.md             # Code examples
│   ├── patterns.md             # Implementation patterns
│   ├── templates.md            # Boilerplate code
│   └── checklists.md           # Validation procedures
├── CHANGELOG.md                # Version history
└── ERROR-AND-FIXES-LOG.md      # Known issues and fixes
```

### Shared Utilities Pattern

Multiple ecosystems include `shared/` directories with common utilities:

**consistency-engine**: Cross-artifact consistency scanning
- Used by: america40, corpus-hub
- Scans for term mismatches, broken references, style violations

**backup-archive**: Backup creation and restoration
- Used by: america40, corpus-hub
- Creates timestamped backups, manages retention

**framework-context**: Load canonical framework definitions
- Used by: america40
- Ensures alignment with 7 principles and 14 roles

**corpus-config**: Manage corpus configuration files
- Used by: corpus-hub
- Defines artifacts, terms, voice, roles

---

## Ecosystem-Specific Guidance

### CorpusHub Platform

**Project Location**: `G:\My Drive\Projects\CorpusHub`

**Architecture**:
- Backend: Express.js with SQLite
- Frontend: Vanilla JavaScript
- API Base URL: `http://localhost:3000`
- Plugin System: Each corpus has `corpus-config.json` under `plugins/<name>/`

**Multi-Corpus Support**:
- Multiple corpora via hot-swap
- Per-corpus databases in `data/corpora/<slug>.db`
- Check active corpus before operations: `GET /api/corpora/active`

**Key API Endpoints**:
```bash
# Health check
GET /api/health

# Corpus management
GET /api/corpora              # List all corpora
GET /api/corpora/active       # Get active corpus
POST /api/corpora/register    # Register new corpus (admin)
POST /api/corpora/switch      # Switch active corpus
DELETE /api/corpora/:slug     # Unregister corpus (admin)

# Artifacts
GET /api/artifacts            # List all artifacts
GET /api/artifacts/:id        # Get artifact details
PUT /api/artifacts/:id        # Update artifact

# Admin
GET /api/admin/stats          # System statistics
```

**Project-Root Convention**:
- Projects discovered by `corpus-config.json` at root
- Template at `plugins/templates/application-project/corpus-config.json`

### America 4.0 Framework

**Framework Context**: Always load canonical sources for consistency
- Principles: `03-specifications/v1.0/america40.comprehensive-framework-synthesis-streamlined.md`
- Roles: `03-specifications/v1.0/america40.stakeholder-roles.md`
- Style: `04-marketing/messaging/america40-style-guide.md`

**Roles and Capabilities**:
- **Reviewer**: Navigate artifacts, add comments/annotations, generate change plans
- **Editor**: Make direct changes, preview consistency implications, track version history
- **Author**: Draft new content with framework alignment and AI assistance

**Reference Hub Webapp**: Located in `07-webapp/`
- Provides web interface for framework documents
- See `webapp-extensions/` for API specs, database schema, UI components

### Windows Application Development

**Development Phases**:
1. **Requirements** (windows-app-requirements): User stories, acceptance criteria
2. **System Design** (windows-app-system-design): Data models, API endpoints, architecture
3. **UI Design** (windows-app-ui-design): Page inventory, navigation flows, forms
4. **Build** (windows-app-build): Implementation, testing, validation
5. **Deployment** (windows-app-supervision): NSSM service, health checks, MSI packaging

**Security Integration**:
- OAuth-first authentication pattern (authentication-patterns)
- Cookie separation for security tokens
- First-user becomes admin automatically
- Input validation and CSRF protection (secure-coding-patterns)
- Security checklists run during build phase

**Reference Files**: windows-app-build has extensive references (124KB total):
- `deployment-patterns.md`
- `installer-patterns.md`
- `error-catalog.md`
- `plugin-integration.md`
- `security-patterns.md`

### Content Creation

**HTML-First Workflow**:
1. Create content in semantic HTML
2. Export to platform-specific formats:
   - DOCX (via Pandoc)
   - PDF (via headless Chrome)
   - PPTX (via Python script)
   - Plain text (for social media)

**Platform Support**:
- Social Media: Bluesky, Twitter (character limits, threading)
- Newsletter: Substack (HTML email formatting)
- Website: Static sites (Jekyll, Hugo)
- Journal: Academic publishing (citations, references)

**Scripts**: Located in `publishing/content-creation-ecosystem/scripts/`
- `init_content.py` - Initialize new content project
- `validate_content.py` - Validate HTML structure
- `convert_to_docx.py` - Export to Word
- `convert_to_pdf.py` - Export to PDF
- `bundle_content.py` - Package for distribution

---

## Testing and Validation

### Pre-Commit Checks

Before committing changes to skills:

1. **Frontmatter Validation**: Run `python tools/quick_validate.py` on modified skills
2. **Size Check**: Verify SKILL.md files stay under 15KB target (or document exception)
3. **Cross-References**: Ensure all reference file links resolve correctly
4. **Documentation**: Update README.md if skill behavior changed

### Integration Testing

Test multi-skill workflows:

1. **Orchestrator Routing**: Verify orchestrators route to correct sub-skills
2. **Cross-Skill Coordination**: Test hand-offs between related skills
3. **Reference Loading**: Ensure reference files load when needed
4. **Error Handling**: Verify error messages are actionable

### Navigation Auditing

Use navigation-auditor skill to verify:
- All documented navigation paths work
- No orphaned skills (unreachable)
- No circular dependencies
- All orchestrators have valid routes

---

## File Naming Conventions

**Skills**: `skill-name-in-kebab-case/`
- Examples: `skill-ecosystem-manager/`, `windows-app-build/`, `corpus-init/`

**Orchestrators**: `category-orchestrator/`
- Examples: `windows-app-orchestrator/`, `security-patterns-orchestrator/`

**Reference Files**: `descriptive-name.md`
- Examples: `deployment-patterns.md`, `social-media.md`, `api-specifications.md`

**Logs**: `ERROR-AND-FIXES-LOG.md`, `CHANGELOG.md`

**Metadata**: `SKILL.md`, `README.md`, `CLAUDE.md`

---

## Known Issues and Exceptions

### Size Exceptions

**windows-app-build**: 17KB (13% over target)
- **Justification**: Core implementation skill with complex decision trees
- **Mitigation**: Extracted 124KB to reference files (deployment, installer, error catalog)

**content-creation-ecosystem**: 14KB (within buffer)
- **Justification**: Multi-platform content creation with format-specific guidance
- **Mitigation**: Platform details in reference files

### Git Status Anomalies

The repository shows unusual untracked files with encoding issues:
```
?? "windows-app/windows-app-build/references´Ç³ && cp C´Ǧ..."
```

These appear to be shell command artifacts and should be cleaned:
```bash
git clean -fd
```

---

## Version History

### v3.0.0 (2026-01-31) - Multi-Ecosystem Expansion

**Added**:
- America 4.0 Review & Update System (7+ skills)
- CorpusHub Platform (10+ skills)
- corpus-hub-v2 (in development)

**Updated**:
- CLAUDE.md to reflect current architecture
- Documentation to cover all five ecosystems

**Total Skills**: 36+ across 5 major categories

### v2.0.0 (2026-01-27) - Comprehensive Restructure

**Changes**:
- Flat → 3-tier directory structure
- Created security-patterns-orchestrator, publishing-orchestrator
- Condensed windows-app-build from 40KB to 17KB
- Added 20 README files, 10 reference files (153KB)

**Total Skills**: 15 (meta, windows-app, publishing)

### v1.0.0 (2026-01-20) - Initial Version

- 13 skills in flat structure
- Basic documentation
- windows-app-build 40KB (oversized)

---

## Contributing

### Creating New Skills

1. Use `skill-ecosystem-manager` skill to design new skills
2. Follow size guidelines (<15KB SKILL.md)
3. Extract verbose content to `references/` subdirectory
4. Create `README.md` with quick reference
5. Update category `README.md`
6. Run `python tools/quick_validate.py` before committing

### Improving Existing Skills

1. Log issue in skill's `ERROR-AND-FIXES-LOG.md`
2. Create regression test for the error
3. Update SKILL.md or reference files
4. Increment version in `CHANGELOG.md`
5. Validate with quick_validate.py

### Refactoring Skills

**When to refactor**:
- Skill significantly exceeds 15KB
- Multiple skills have overlapping functionality
- New patterns emerge from error logs
- User feedback indicates confusion

**Process**:
1. Use conversation-snapshot to preserve context
2. Analyze current skill structure
3. Plan refactoring (extract vs consolidate)
4. Implement changes incrementally
5. Validate continuously
6. Update all cross-references
7. Document in CHANGELOG.md

---

## License

Proprietary - Pterodactyl Holdings, LLC

---

*Last Updated: 2026-01-31*
*Version: 3.0.0*
*Total Skills: 36+ across 5 major ecosystems*
