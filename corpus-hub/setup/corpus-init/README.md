# Corpus Init

Initialize brand-new projects as corpus-enabled with interactive prompts and smart defaults.

## Purpose

Makes corpus-enablement as simple as answering 3-5 questions. Creates directory structure, generates `corpus-config.json`, and registers with CorpusHub—all automatically.

## When to Use

- Starting a new software project
- Creating a documentation repository
- Beginning a research/writing project
- Setting up requirements management system

## Opt-Out by Default

**Important:** The first question asks if you want CorpusHub features. Select "No" to skip corpus setup entirely. You can always enable later with `corpus convert`.

## Files

- **SKILL.md** (~12KB) - Main initialization workflow
- **references/project-types.md** - Detailed type detection and examples
- **references/templates.md** - Full corpus-config.json templates

## Quick Start

1. Navigate to your project directory
2. Say: "Initialize corpus for this project" or "Enable CorpusHub"
3. Answer interactive prompts
4. Done! Browse to http://localhost:3000

## Project Types

1. **Software Application** - Code + documentation
2. **Documentation Only** - Pure documentation
3. **Research/Writing** - Papers, articles, reports
4. **Requirements Management** - User stories, acceptance criteria

## Related Skills

- **corpus-convert** - Convert existing projects
- **reviewer** - Review and comment on artifacts
- **editor** - Edit corpus content
- **admin** - Manage system settings
