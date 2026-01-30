# Setup - Corpus Enablement Tools

Interactive tools for initializing and converting projects to be corpus-enabled.

## Overview

The setup category provides two specialized skills for corpus-enablement:

| Skill | Purpose | Use When |
|-------|---------|----------|
| **corpus-init** | Initialize new projects | Starting from scratch, greenfield projects |
| **corpus-convert** | Convert existing projects | Adding CorpusHub to mature projects with existing docs |

## corpus-init

Initialize brand-new projects as corpus-enabled.

**Features:**
- Interactive prompts with smart defaults
- 4 project types (Software, Documentation, Research, Requirements)
- Automatic directory creation
- Opt-out question (corpus by default)
- Zero manual configuration

**Quick Start:**
```
"Initialize corpus for my project"
```

**Output:**
- `corpus-config.json`
- Directory structure
- Registered with CorpusHub
- Ready to use

**Files:**
- `corpus-init/SKILL.md` (~12KB)
- `corpus-init/references/project-types.md`
- `corpus-init/references/templates.md`

---

## corpus-convert

Convert existing projects while preserving structure.

**Features:**
- Automatic project analysis
- Artifact type inference
- Framework term extraction
- Relationship detection
- **Files never deleted** (marked deprecated)

**Quick Start:**
```
"Convert this project to use CorpusHub"
```

**Output:**
- `corpus-config.json` matching existing structure
- Corpus bits from existing files
- Original files marked deprecated
- Registered with CorpusHub

**Files:**
- `corpus-convert/SKILL.md` (~14KB)
- `corpus-convert/references/source-modes.md`
- `corpus-convert/references/inference-rules.md`
- `corpus-convert/references/migration-patterns.md`

---

## Which Should I Use?

### Use **corpus-init** if:
- Starting a new project
- No existing documentation
- Want standard directory structure
- Prefer guided setup

### Use **corpus-convert** if:
- Existing project with docs
- Want to preserve existing structure
- Migrating from another system
- Have specific directory layout

---

## Common Workflows

### Workflow 1: New Software Project
```
User: "Initialize corpus for my app"
→ corpus-init
→ Asks project type: Software Application
→ Creates docs/ directories
→ Generates corpus-config.json
→ Registers with CorpusHub
→ Done!
```

### Workflow 2: Existing Project Conversion
```
User: "Convert this project to use CorpusHub"
→ corpus-convert
→ Scans for documentation
→ Shows detected artifact mapping
→ User confirms
→ Converts files, marks originals deprecated
→ Registers with CorpusHub
→ Done!
```

---

## Key Principles

### For corpus-init:
- **Opt-out by default** - First question enables/disables corpus
- **Smart defaults** - Project type determines structure
- **Zero editing** - No manual JSON required

### For corpus-convert:
- **Preserve originals** - Files never deleted
- **Clear deprecation** - Notices in original files
- **Corpus as truth** - After conversion, edit via CorpusHub
- **Rollback available** - Original files preserved

---

## Prerequisites

Both skills require:
- CorpusHub server running at http://localhost:3000
- Write permissions in project directory
- Node.js (for CorpusHub)

Start server:
```bash
cd "G:\My Drive\Projects\CorpusHub"
npm start
```

---

## Related Skills

- **corpus-hub-orchestrator** - Routes to appropriate setup skill
- **reviewer** - Review and comment on artifacts
- **editor** - Edit corpus content
- **author** - Create new drafts
- **admin** - System administration

---

## Tips

1. **New projects:** Use corpus-init, accept defaults
2. **Existing projects:** Use corpus-convert, review mapping
3. **Backup first:** Commit to git before converting
4. **Test workflow:** Make test edit after setup
5. **Consistency checking:** Enable for better terminology
6. **Framework terms:** Auto-extract when converting
7. **Rollback safe:** Original files always preserved

---

## Documentation

- Full templates: `corpus-init/references/templates.md`
- Project types: `corpus-init/references/project-types.md`
- Source modes: `corpus-convert/references/source-modes.md`
- Migration patterns: `corpus-convert/references/migration-patterns.md`

---

## Support

For issues or questions:
1. Check skill README files
2. Review reference documentation
3. Consult CorpusHub documentation
4. Check server logs for errors
