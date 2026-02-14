# Migration Guide: v3.0 → v4.0

**Version:** v4.0.0
**Date:** 2026-02-14
**Audience:** Users migrating from v3.0 to v4.0
**Estimated Time:** 2-4 hours per project

---

## Overview

This guide walks you through migrating from the v3.0 multi-ecosystem architecture to the v4.0 universal architecture.

### What's Changed

**v3.0 (Multi-Ecosystem):**
- Project-specific skills in separate directories
- Hardcoded behavior per project type
- Limited cross-project reuse
- 36+ skills across 5 categories

**v4.0 (Universal Architecture):**
- 61 universal skills available to all projects
- Configuration-driven behavior
- Two-tier architecture (core + config)
- Corpus-first approach as default

---

## Breaking Changes

### Directory Structure

**Old (v3.0):**
```
skills/
├── meta/
├── windows-app/
├── publishing/
├── america40/
└── corpus-hub/
```

**New (v4.0):**
```
skills/
├── core/
│   ├── corpus/
│   ├── audit/
│   ├── content/
│   ├── development/
│   ├── publishing/
│   ├── utilities/
│   └── learning/
└── config/
    ├── templates/
    └── examples/
```

### Skill Loading

**Old:**
```
"Load america40/review-mode"
"Load corpus-hub/editor-mode"
```

**New:**
```
"Review this document" → loads review-edit-author (universal)
```

### Configuration

**Old:** Hardcoded project-specific logic in skills

**New:** Configuration-driven via `corpus-config.json`

---

## Migration Steps

### Step 1: Backup Current Setup

```bash
# Backup your current skills directory
cd ~/.claude
cp -r skills skills.v3.backup

# Backup any project-specific configurations
find . -name "*.json" -path "*/skills/*" -exec cp --parents {} skills.v3.backup/ \;
```

### Step 2: Update Skills Repository

```bash
# Pull latest v4.0 skills
cd ~/.claude/skills
git checkout main
git pull origin main

# Verify v4.0 structure
ls -la core/
ls -la config/
```

### Step 3: Identify Project Type

Determine which v4.0 configuration template matches your project:

| v3.0 Project | v4.0 Template |
|--------------|---------------|
| america40 | `framework-docs.json` |
| corpus-hub | `web-app.json` |
| windows-app | `windows-app.json` |
| generic | `default.json` |

### Step 4: Initialize as Corpus (New Projects)

```bash
# In your project directory
cd /path/to/your/project

# Initialize with appropriate template
claude "Initialize this as a corpus using the [template-name] template"
```

This creates `corpus-config.json` at your project root.

### Step 5: Convert Existing Project

For projects with existing content:

```bash
# In your project directory
claude "Convert this to corpus preserving existing structure"

# This will:
# - Detect existing files and structure
# - Create corpus-config.json
# - Register with CorpusHub (if running)
# - Preserve all existing content
```

### Step 6: Customize Configuration

Edit `corpus-config.json` to match your project's needs:

```json
{
  "corpus": {
    "name": "Your Project",
    "description": "Project description",
    "version": "1.0.0",
    "baseDir": "/absolute/path/to/project"
  },
  "artifacts": {
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
        "id": "terminology",
        "label": "Key Terms",
        "terms": ["Term1", "Term2"],
        "canonicalSource": "documentation"
      }
    ]
  }
}
```

### Step 7: Migrate Custom Skills (If Any)

If you created custom skills in v3.0:

1. **Identify universal equivalents** - Most custom skills now have universal versions
2. **Extract configuration** - Move hardcoded logic to corpus-config.json
3. **Port remaining logic** - Create new universal skill if truly unique

### Step 8: Update Workflows

**Old workflow (v3.0):**
```
1. "Load america40/review-mode"
2. "Review this document"
3. "Add comment about..."
```

**New workflow (v4.0):**
```
1. "Review this document" (automatically loads review-edit-author)
2. "Add comment about..."
```

Skills auto-load based on intent detection.

### Step 9: Test Migration

```bash
# Test corpus detection
claude "Check corpus status"

# Test content operations
claude "Review docs/README.md"

# Test audit operations
claude "Run consistency audit"

# Test convergence (if applicable)
claude "Start convergence audit"
```

### Step 10: Remove v3.0 Backup (Optional)

Once verified:

```bash
# After confirming everything works
rm -rf ~/.claude/skills.v3.backup
```

---

## Feature Mapping

### Content Management

| v3.0 Skill | v4.0 Skill | Notes |
|------------|------------|-------|
| america40/review-mode | review-edit-author | Universal, role-based |
| corpus-hub/editor-mode | review-edit-author | Same skill, editor role |
| corpus-hub/author-mode | review-edit-author | Same skill, author role |
| corpus-hub/document-crud | document-management | Universal CRUD ops |

### Audit & Quality

| v3.0 Skill | v4.0 Skill | Notes |
|------------|------------|-------|
| america40/consistency-audit | audits/consistency | Now universal |
| corpus-hub/navigation-audit | audits/navigation | Now universal |
| (new) | audits/security | New in v4.0 |
| (new) | audits/quality | New in v4.0 |
| (new) | audits/performance | New in v4.0 |

### Development

| v3.0 Skill | v4.0 Skill | Notes |
|------------|------------|-------|
| windows-app/* | development/windows-app-* | Restructured, enhanced |
| (new) | development/ui-generation-* | New in v4.0/v4.1 |

### Publishing

| v3.0 Skill | v4.0 Skill | Notes |
|------------|------------|-------|
| publishing/blog-post | publishing/content-creation | Universal content creation |
| publishing/multi-platform | publishing/content-creation | Same skill, multi-platform mode |

---

## Configuration Examples

### Migrating America 4.0 Framework

**Old (v3.0):** Skills in `america40/` directory

**New (v4.0):** Use `framework-docs.json` template

```json
{
  "corpus": {
    "name": "America 4.0 Framework",
    "description": "America 4.0 Civic Innovation Framework",
    "version": "4.0.0"
  },
  "artifacts": {
    "framework-docs": {
      "path": "framework",
      "label": "Framework Documentation",
      "extensions": [".md"],
      "sourceMode": "corpus"
    },
    "api-docs": {
      "path": "api",
      "label": "API Documentation",
      "extensions": [".md"],
      "sourceMode": "bidirectional"
    }
  },
  "framework": {
    "categories": [
      {
        "id": "principles",
        "label": "Core Principles",
        "terms": ["Open Government", "Civic Innovation", "Digital Democracy"],
        "canonicalSource": "framework-docs"
      }
    ]
  }
}
```

### Migrating CorpusHub Platform

**Old (v3.0):** Skills in `corpus-hub/` directory

**New (v4.0):** Use `web-app.json` template

```json
{
  "corpus": {
    "name": "CorpusHub Platform",
    "description": "CorpusHub knowledge management platform",
    "version": "2.0.0"
  },
  "artifacts": {
    "source-code": {
      "path": "src",
      "extensions": [".js", ".jsx", ".ts", ".tsx"],
      "sourceMode": "source"
    },
    "documentation": {
      "path": "docs",
      "extensions": [".md"],
      "sourceMode": "bidirectional"
    }
  },
  "audit": {
    "methodology": "multi-methodology-3-3-1",
    "applicable_audits": ["security", "quality", "performance", "consistency"]
  }
}
```

### Migrating Windows Desktop App

**Old (v3.0):** Skills in `windows-app/` directory

**New (v4.0):** Use `windows-app.json` template

```json
{
  "corpus": {
    "name": "Operations Hub",
    "description": "Windows desktop operations management",
    "version": "1.0.0"
  },
  "artifacts": {
    "source-code": {
      "path": "app",
      "extensions": [".cs", ".xaml"],
      "sourceMode": "source"
    },
    "installers": {
      "path": "installers",
      "extensions": [".wxs", ".wxi"],
      "sourceMode": "source"
    }
  },
  "development": {
    "platform": "windows",
    "framework": "wpf",
    "packaging": "msi"
  }
}
```

---

## Troubleshooting

### Issue: "Skill not found"

**Problem:** Old v3.0 skill names no longer work

**Solution:** Use intent-based loading instead
```bash
# Old: "Load america40/review-mode"
# New: "Review this document"
```

### Issue: "Configuration not found"

**Problem:** Project not corpus-enabled

**Solution:** Initialize or convert project
```bash
claude "Initialize this as a corpus"
# or
claude "Convert this to corpus"
```

### Issue: "CorpusHub not running"

**Problem:** Skills can't connect to CorpusHub

**Solution:** Start CorpusHub or use offline mode
```bash
# Start CorpusHub
"C:\Program Files\CorpusHub\CorpusHub.exe"

# Or continue without CorpusHub (some features limited)
```

### Issue: "Custom skill no longer works"

**Problem:** Custom v3.0 skill not compatible

**Solution:** Check if universal equivalent exists, or port to v4.0
```bash
# Find equivalent skill
claude "What skills handle [your use case]?"
```

---

## Performance Improvements

**v4.0 offers significant performance gains:**

- **Faster skill loading:** Intent-based detection (no manual loading)
- **Parallelization:** v4.1 adds 40-50% speed improvement
- **Reduced complexity:** Single universal skill vs multiple project-specific versions
- **Better caching:** Shared skills across all projects

---

## Getting Help

**Questions during migration:**
1. Check this guide first
2. Review `CLAUDE.md` for current architecture
3. Check `ARCHITECTURE-v4.md` for design details
4. Open issue at: https://github.com/pterodactyl-holdings/claude-skills/issues

**Migration support:**
- America 4.0 projects: See `config/examples/america40-config.json`
- CorpusHub projects: See `config/examples/corpushub-config.json`
- Windows apps: See `config/templates/windows-app.json`

---

## Post-Migration Checklist

- [ ] Backup v3.0 setup completed
- [ ] v4.0 skills pulled from git
- [ ] Project initialized/converted to corpus
- [ ] `corpus-config.json` created and customized
- [ ] Tested basic operations (review, audit, etc.)
- [ ] Verified CorpusHub integration (if applicable)
- [ ] Updated team documentation
- [ ] Removed v3.0 backup (after verification)

---

## Next Steps

**After successful migration:**

1. **Explore v4.1 features** - See `PARALLELIZATION-GUIDE.md`
2. **Optimize configuration** - Review `CONFIG-REFERENCE.md`
3. **Set up convergence** - If applicable, configure multi-methodology audit
4. **Train team** - Share this guide with team members

---

**Migration Complete!** 🎉

Your project is now on v4.0 universal architecture with access to all 61 skills.

---

**Last Updated:** 2026-02-14
**Version:** v4.0.0
**Status:** Complete migration guide
