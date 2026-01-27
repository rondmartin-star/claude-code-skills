# Claude Code Skills Ecosystem

Comprehensive skill library for Windows application development and content creation.

**Version:** 2.0
**Last Updated:** 2026-01-27
**Total Skills:** 15 (13 original + 2 new orchestrators)

---

## Quick Start

### Loading Skills

Skills are automatically loaded based on trigger phrases:

```bash
# Windows development
"I want to build an app" → windows-app-orchestrator
"Start coding" → windows-app-build
"Add OAuth login" → security-patterns-orchestrator

# Content creation
"Write a Bluesky post" → publishing-orchestrator
"Create an article" → content-creation-ecosystem
```

### Directory Structure

```
skills/
├── meta/                           # Ecosystem management
│   ├── skill-ecosystem-manager/
│   ├── conversation-snapshot/
│   ├── navigation-auditor/
│   └── plugin-ecosystem/
│
├── windows-app/                    # Windows development lifecycle
│   ├── windows-app-orchestrator/   # Phase coordinator
│   ├── windows-app-requirements/   # Requirements gathering
│   ├── windows-app-system-design/  # Data model & API design
│   ├── windows-app-ui-design/      # UI & navigation design
│   ├── windows-app-build/          # Implementation & testing
│   ├── windows-app-supervision/    # Packaging & deployment
│   └── security/                   # Security sub-category
│       ├── security-patterns-orchestrator/
│       ├── authentication-patterns/
│       └── secure-coding-patterns/
│
└── publishing/                     # Content creation
    ├── publishing-orchestrator/
    └── content-creation-ecosystem/
```

---

## Skill Categories

### Meta Skills (Ecosystem Management)

Skills for managing the Claude Code ecosystem itself.

| Skill | Size | Purpose |
|-------|------|---------|
| **skill-ecosystem-manager** | ~8KB | Create and maintain skills, error-driven improvement |
| **conversation-snapshot** | ~6KB | Portable snapshots for continuing work in new contexts |
| **navigation-auditor** | ~7KB | Verify navigation paths and feature reachability |
| **plugin-ecosystem** | ~5KB | Manage external plugin integrations |

### Windows-App Skills (Development Lifecycle)

Complete workflow from requirements to production deployment.

| Skill | Size | Purpose | Phase |
|-------|------|---------|-------|
| **windows-app-orchestrator** | ~12KB + 16KB ref | Phase coordinator, skill routing | All |
| **windows-app-requirements** | ~8KB + 16KB ref | User stories, acceptance criteria | Requirements |
| **windows-app-system-design** | ~10KB | Data models, API endpoints, architecture | Design |
| **windows-app-ui-design** | ~9KB | Page inventory, navigation flows, forms | Design |
| **windows-app-build** | ~17KB + 124KB ref | Implementation, testing, validation | Build |
| **windows-app-supervision** | ~8KB + 33KB ref | NSSM service, health checks, MSI packaging | Deployment |

### Security Skills (Authentication & Secure Coding)

Coordinated security implementation patterns.

| Skill | Size | Purpose |
|-------|------|---------|
| **security-patterns-orchestrator** | ~7KB | Route between authentication and secure-coding skills |
| **authentication-patterns** | ~10KB + 30KB ref | OAuth-first authentication, first-user admin |
| **secure-coding-patterns** | ~12KB + 28KB ref | XSS, CSRF, SQL injection prevention |

### Publishing Skills (Content Creation)

Multi-platform content creation with HTML-first workflow.

| Skill | Size | Purpose |
|-------|------|---------|
| **publishing-orchestrator** | ~7KB | Route by content type (social, newsletter, blog, journal) |
| **content-creation-ecosystem** | ~14KB + refs | HTML-first with DOCX/PPTX/PDF export |

---

## Orchestrator Pattern

Orchestrators coordinate skill loading based on context:

```
windows-app-orchestrator
├─→ requirements (gathering phase)
├─→ system-design (architecture phase)
├─→ ui-design (interface phase)
├─→ build (implementation phase)
│   └─→ security-patterns-orchestrator (if auth/security needed)
│       ├─→ authentication-patterns (OAuth, sessions)
│       └─→ secure-coding-patterns (input validation, CSRF)
└─→ supervision (deployment phase)

publishing-orchestrator
└─→ content-creation-ecosystem
    ├─→ social-media.md (Bluesky, Twitter)
    ├─→ newsletter.md (Substack)
    ├─→ website.md (Static sites)
    └─→ journal.md (Academic publishing)
```

---

## Design Philosophy

### 1. Size Efficiency
- **SKILL.md target:** <15KB (essential guidance)
- **Reference files:** Detailed examples and templates
- **Load on demand:** Only include references when needed

### 2. Specialization
- One skill, one purpose
- Orchestrators coordinate, specialists execute
- Clear entry/exit criteria for each skill

### 3. Fool-Proof
- Users may have no technical background
- Provide sensible defaults
- Auto-detect and auto-configure
- Clear error messages with actionable guidance

### 4. Iteration Over Rebuilding
- **Golden Rule:** Never rebuild from scratch
- Always iterate on baseline
- Preserve working state
- Track changes in CHANGELOG.md

### 5. Error-Driven Improvement
- Log errors in ERROR-AND-FIXES-LOG.md
- Create regression tests
- Update skills based on real issues
- Continuous refinement

---

## Ecosystem Metrics

### Coverage
- **Total Skills:** 15
- **Reference Files:** 17 (241KB total documentation)
- **Categories:** 4 (meta, windows-app, security, publishing)
- **Orchestrators:** 3 (windows-app, security, publishing)

### Size Compliance
- **Skills <15KB:** 13/15 (87%)
- **Skills 15-20KB:** 2/15 (windows-app-build 17KB, content-creation 14KB)
- **Average SKILL.md size:** ~9.5KB
- **Average reference size:** ~14KB

### Documentation
- **Skills with README:** 15/15 (100%)
- **Skills with references:** 10/15 (67%)
- **Categories with README:** 4/4 (100%)

---

## Common Workflows

### Workflow 1: New Windows Application

```
User: "I want to build a property management system"
→ windows-app-orchestrator loads
→ Routes to windows-app-requirements
→ Gather user stories and acceptance criteria
→ Exit to system-design
→ Design data models and API endpoints
→ Exit to ui-design
→ Design pages and navigation
→ Exit to build
→ Implement application
→ Exit to supervision
→ Package and deploy
```

### Workflow 2: Add OAuth to Existing App

```
User: "Add Google OAuth login"
→ windows-app-build loads (implementation)
→ Detects authentication requirement
→ security-patterns-orchestrator loads
→ Routes to authentication-patterns
→ Implement OAuth flow with cookie separation
→ Validate with regression tests
→ Complete
```

### Workflow 3: Security Audit

```
User: "Run security audit on my app"
→ windows-app-build loads
→ security-patterns-orchestrator loads
→ secure-coding-patterns loads
→ Run all security checklists
→ Report vulnerabilities
→ Fix identified issues
→ Re-validate
```

### Workflow 4: Create Content

```
User: "Write a Bluesky post about my new feature"
→ publishing-orchestrator loads
→ Detects content type: social media
→ content-creation-ecosystem loads
→ Uses social-media.md reference
→ Creates HTML-first post
→ Export to plain text for Bluesky
```

---

## Version History

### v2.0 (2026-01-27)
- **Restructure:** Flat → 3-tier directory structure
- **New orchestrators:** security-patterns, publishing
- **Size optimization:** windows-app-build 40KB → 17KB
- **Documentation:** Added 20 README files
- **References:** Added 10 new reference files (153KB)
- **Total refactor:** 39 files created/modified

### v1.0 (2026-01-20)
- Initial flat structure
- 13 skills at root level
- Basic documentation
- windows-app-build 40KB (oversized)

---

## Contributing

### Creating New Skills

1. Use skill-ecosystem-manager
2. Follow size guidelines (<15KB SKILL.md)
3. Create reference files for detailed content
4. Add README.md to skill directory
5. Update category README
6. Test with validation tools

### Improving Existing Skills

1. Log errors in ERROR-AND-FIXES-LOG.md
2. Create regression tests
3. Update SKILL.md or reference files
4. Increment version number
5. Document in CHANGELOG.md

---

## Support

- **Issues:** Log in skill's ERROR-AND-FIXES-LOG.md
- **Questions:** Use conversation-snapshot for context preservation
- **Validation:** Run `tools/quick_validate.py`

---

## License

Proprietary - Pterodactyl Holdings, LLC

---

*Claude Code Skills Ecosystem v2.0 - Production-Grade Windows Development*
