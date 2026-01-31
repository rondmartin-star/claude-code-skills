# Core Orchestrator

**Purpose:** Main entry point and navigation for v4.0 Universal Skills Ecosystem

**Size:** 9.9 KB

---

## What It Does

Routes users to the right skill based on intent:
- Corpus management (initialize, configure, detect)
- Auditing (quality, security, performance, etc.)
- Content work (review, edit, author)
- Utilities (backup, export)

## Intent Detection

Analyzes user messages for keywords and patterns:
- "Initialize corpus" → corpus-init
- "Audit security" → audits/security
- "Create backup" → utilities/backup-restore
- "Export to PDF" → utilities/corpus-export
- "Review document" → review-edit-author

## Routing Priority

1. Explicit skill name mentioned
2. Utility operations (high priority)
3. Audit operations
4. Corpus management
5. Content management
6. Ask for clarification

## Ecosystem Overview

- **Corpus:** 6 skills
- **Audit:** 12 skills
- **Content:** 1 skill
- **Utilities:** 2 skills
- **Total:** 21 skills

---

**Part of:** v4.0.0 Universal Skills  
**Category:** Orchestrator  
**Always load first** for navigation
