# Corpus Convert

Convert existing projects to be corpus-enabled while preserving existing structure and files.

## Purpose

Analyzes your project, infers artifact types, generates `corpus-config.json`, and registers with CorpusHub. **Original files are preserved but marked as deprecated.**

## When to Use

- Converting existing project with documentation
- Migrating from another documentation system
- Adding CorpusHub to a mature project
- Enabling corpus features for legacy code

## Critical: Files Never Deleted

Original files are:
- Marked with deprecation notices
- Preserved for reference
- Available for rollback
- Disabled from auto-sync

After conversion, **corpus becomes the source of truth**.

## Files

- **SKILL.md** (~14KB) - Main conversion workflow
- **references/source-modes.md** - Traditional vs Corpus vs Hybrid
- **references/inference-rules.md** - Artifact type detection
- **references/migration-patterns.md** - Common conversion patterns

## Quick Start

1. Navigate to existing project
2. Say: "Convert this project to use CorpusHub"
3. Review detected artifact mapping
4. Confirm or customize
5. Done! Browse to http://localhost:3000

## Source Modes

- **Traditional** - Edit in IDE, corpus for review
- **Corpus** - Edit in browser (recommended for conversion)
- **Hybrid** - Mix of both

## Related Skills

- **corpus-init** - Initialize new projects
- **reviewer** - Review and comment
- **editor** - Edit corpus content
- **admin** - System management
