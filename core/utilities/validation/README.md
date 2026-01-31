# Validation Utility

**Purpose:** Corpus and skill ecosystem validation

**Size:** 12.0 KB

---

## Quick Start

```javascript
// Validate corpus config
const result = await validateCorpusConfig('./corpus-config.json');

// Validate single skill
const skillResult = await validateSkill('./core/corpus/corpus-init');

// Validate entire ecosystem
const ecosystem = await validateEcosystem('./core');
console.log(`${ecosystem.valid}/${ecosystem.totalSkills} valid`);
```

## What It Validates

- **Corpus Config:** Schema, artifact paths, version format
- **Skills:** Frontmatter, size limits, structure
- **References:** Internal links, skill references
- **Ecosystem:** All skills integrity
- **CorpusHub:** API connectivity, registration

## Validation Rules

- SKILL.md must have YAML frontmatter
- Size limit: 15KB per SKILL.md
- Name must be kebab-case
- Description required (no angle brackets)
- All artifact paths must exist

## Output Formats

- CLI summary with colors
- JSON for automation

---

**Part of:** v4.0.0 Universal Skills  
**Category:** Utilities  
**Use for:** QA, CI/CD, pre-deployment
