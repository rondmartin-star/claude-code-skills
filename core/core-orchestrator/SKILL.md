---
name: core-orchestrator
description: >
  Main orchestrator for v4.0 Universal Skills Ecosystem. Routes users to appropriate
  skills based on intent: corpus management, auditing, content work, or utilities.
  Use when: starting new tasks, unclear which skill to use, or navigating ecosystem.
---

# Core Orchestrator

**Purpose:** Universal ecosystem navigation and routing
**Type:** Orchestrator Skill (Entry Point)

---

## ⚡ ALWAYS LOAD THIS SKILL

This is the main entry point for the v4.0 Universal Skills Ecosystem. Load when:
- User starts a new task
- Intent is unclear
- Multiple skills might apply
- User asks "what can you do?"

---

## Intent Detection & Routing

### 1. Corpus Management

**Triggers:**
- "Initialize corpus"
- "Configure corpus"
- "Set up project"
- "Convert to corpus"
- "Manage source modes"

**Route to:**
```javascript
const corpusIntents = {
  initialize: 'corpus-init',
  configure: 'corpus-config',
  convert: 'corpus-convert',
  detect: 'corpus-detect',
  sourceMode: 'source-mode-manager',
  orchestrate: 'corpus-orchestrator'
};

function routeCorpusIntent(userMessage) {
  if (/\b(initialize|init|set up|create)\b.*\bcorpus\b/i.test(userMessage)) {
    return 'corpus-init';
  }
  if (/\b(configure|config|settings)\b.*\bcorpus\b/i.test(userMessage)) {
    return 'corpus-config';
  }
  if (/\b(convert|migrate)\b.*\bcorpus\b/i.test(userMessage)) {
    return 'corpus-convert';
  }
  if (/\b(detect|check|verify)\b.*\bcorpus\b/i.test(userMessage)) {
    return 'corpus-detect';
  }
  if (/\b(source mode|editing|sync)\b/i.test(userMessage)) {
    return 'source-mode-manager';
  }

  // Default to orchestrator for general corpus tasks
  return 'corpus-orchestrator';
}
```

### 2. Audit & Quality

**Triggers:**
- "Audit [quality/security/performance/etc]"
- "Check for issues"
- "Run convergence"
- "Validate [aspect]"

**Route to:**
```javascript
const auditIntents = {
  // Technical methodology
  quality: 'audits/quality',
  security: 'audits/security',
  performance: 'audits/performance',
  dependency: 'audits/dependency',

  // User methodology
  content: 'audits/content',
  accessibility: 'audits/accessibility',
  seo: 'audits/seo',

  // Corpus-specific
  consistency: 'audits/consistency',
  navigation: 'audits/navigation',

  // Orchestration
  convergence: 'convergence-engine',
  planning: 'fix-planner',
  orchestrate: 'audit-orchestrator'
};

function routeAuditIntent(userMessage) {
  // Specific audit types
  if (/\b(quality|code quality|complexity|duplication)\b/i.test(userMessage)) {
    return 'audits/quality';
  }
  if (/\b(security|vulnerability|sql injection|xss)\b/i.test(userMessage)) {
    return 'audits/security';
  }
  if (/\b(performance|slow|optimize|n\+1)\b/i.test(userMessage)) {
    return 'audits/performance';
  }
  if (/\b(dependency|dependencies|outdated|vulnerabilities)\b/i.test(userMessage)) {
    return 'audits/dependency';
  }
  if (/\b(content|grammar|spelling|readability)\b/i.test(userMessage)) {
    return 'audits/content';
  }
  if (/\b(accessibility|wcag|a11y|screen reader)\b/i.test(userMessage)) {
    return 'audits/accessibility';
  }
  if (/\b(seo|search|meta tags|sitemap)\b/i.test(userMessage)) {
    return 'audits/seo';
  }
  if (/\b(consistency|terms|framework)\b/i.test(userMessage)) {
    return 'audits/consistency';
  }
  if (/\b(navigation|links|broken)\b/i.test(userMessage)) {
    return 'audits/navigation';
  }

  // Convergence and planning
  if (/\b(convergence|3-3-1|methodologies)\b/i.test(userMessage)) {
    return 'convergence-engine';
  }
  if (/\b(fix|plan|prioritize|issues)\b/i.test(userMessage)) {
    return 'fix-planner';
  }

  // Default to audit orchestrator
  return 'audit-orchestrator';
}
```

### 3. Content Management

**Triggers:**
- "Review [content]"
- "Edit [document]"
- "Create new [content]"
- "Author [document]"

**Route to:**
```javascript
function routeContentIntent(userMessage) {
  const hasRole = /\b(review|reviewer|edit|editor|author|create)\b/i.exec(userMessage);

  if (!hasRole) {
    return 'review-edit-author';  // Default content skill
  }

  const role = hasRole[1].toLowerCase();

  if (/review/.test(role)) {
    return 'review-edit-author';  // Reviewer mode
  }
  if (/edit/.test(role)) {
    return 'review-edit-author';  // Editor mode
  }
  if (/author|create/.test(role)) {
    return 'review-edit-author';  // Author mode
  }

  return 'review-edit-author';
}
```

### 4. Utilities

**Triggers:**
- "Backup"
- "Restore"
- "Export"
- "Validate"

**Route to:**
```javascript
const utilityIntents = {
  backup: 'utilities/backup-restore',
  restore: 'utilities/backup-restore',
  export: 'utilities/corpus-export'
};

function routeUtilityIntent(userMessage) {
  if (/\b(backup|create backup)\b/i.test(userMessage)) {
    return 'utilities/backup-restore';
  }
  if (/\b(restore|rollback|recovery)\b/i.test(userMessage)) {
    return 'utilities/backup-restore';
  }
  if (/\b(export|generate|pdf|docx|documentation)\b/i.test(userMessage)) {
    return 'utilities/corpus-export';
  }

  return null;  // No utility match
}
```

---

## Main Routing Logic

**Priority order:**
1. Explicit skill name mentioned
2. Utility operations (backup, export)
3. Audit operations
4. Corpus management
5. Content management

```javascript
async function routeToSkill(userMessage, context = {}) {
  const message = userMessage.toLowerCase();

  // 1. Check for explicit skill name
  const explicitSkill = checkExplicitSkillName(message);
  if (explicitSkill) {
    return { skill: explicitSkill, confidence: 'high' };
  }

  // 2. Check utilities (high priority, specific actions)
  const utilitySkill = routeUtilityIntent(message);
  if (utilitySkill) {
    return { skill: utilitySkill, confidence: 'high' };
  }

  // 3. Check audit operations
  if (/\b(audit|check|validate|scan|analyze)\b/i.test(message)) {
    const auditSkill = routeAuditIntent(message);
    return { skill: auditSkill, confidence: 'high' };
  }

  // 4. Check corpus management
  if (/\bcorpus\b/i.test(message)) {
    const corpusSkill = routeCorpusIntent(message);
    return { skill: corpusSkill, confidence: 'medium' };
  }

  // 5. Check content management
  if (/\b(review|edit|author|content|document)\b/i.test(message)) {
    const contentSkill = routeContentIntent(message);
    return { skill: contentSkill, confidence: 'medium' };
  }

  // 6. No clear match - ask for clarification
  return {
    skill: null,
    confidence: 'low',
    suggestions: getSuggestedSkills(message, context)
  };
}
```

---

## User Guidance

### Welcome Message

When user asks "what can you do?" or similar:

```markdown
# v4.0 Universal Skills Ecosystem

I can help with:

## 🗂 Corpus Management
- Initialize new corpus: "Initialize this as a corpus"
- Configure project: "Configure corpus settings"
- Detect status: "Check if this is corpus-enabled"
- Manage editing modes: "Set up bidirectional sync"

## 🔍 Quality & Auditing
**Technical (How it's built):**
- Code quality: "Audit code quality"
- Security: "Check for vulnerabilities"
- Performance: "Find slow queries"
- Dependencies: "Check outdated packages"

**User (How it's experienced):**
- Content: "Check grammar and readability"
- Accessibility: "Validate WCAG compliance"
- SEO: "Check meta tags"

**Corpus:**
- Consistency: "Check framework terms"
- Navigation: "Find broken links"

**Orchestration:**
- Convergence: "Run 3-3-1 convergence"
- Planning: "Prioritize fixes"

## ✏ Content Management
- Review: "Review this document"
- Edit: "Edit with AI assistance"
- Author: "Create new content"

## 🛠 Utilities
- Backup: "Create backup"
- Restore: "Restore from backup"
- Export: "Export to PDF"

**What would you like to do?**
```

### Disambiguation

When multiple skills match:

```javascript
function disambiguate(matches, userMessage) {
  return `
I found multiple skills that might help:

${matches.map((m, i) => `${i + 1}. **${m.name}** - ${m.description}`).join('\n')}

Which one would you like to use? Or provide more details about what you'd like to do.
  `.trim();
}
```

---

## Skill Categories Reference

### Corpus Management (6 skills)
- corpus-init
- corpus-config
- corpus-convert
- corpus-detect
- source-mode-manager
- corpus-orchestrator

### Audit System (12 skills)
**Technical:** quality, security, performance, dependency
**User:** content, accessibility, seo
**Corpus:** consistency, navigation
**Holistic:** convergence-engine, fix-planner, audit-orchestrator

### Content (1 skill)
- review-edit-author

### Utilities (2 skills)
- backup-restore
- corpus-export

**Total: 21 skills**

---

## Quick Decision Tree

```
User Request
    │
    ├─ Mentions specific skill name? → Load that skill
    │
    ├─ Backup/Export/Restore? → Utilities
    │
    ├─ Audit/Check/Validate?
    │   ├─ Quality/Security/Performance/Dependency? → Technical audits
    │   ├─ Content/A11y/SEO? → User audits
    │   ├─ Consistency/Navigation? → Corpus audits
    │   └─ Convergence/Fix? → Holistic orchestration
    │
    ├─ Corpus/Initialize/Configure? → Corpus management
    │
    ├─ Review/Edit/Author? → Content management
    │
    └─ Unclear → Show welcome message & get clarification
```

---

## Configuration

No configuration needed - this skill routes based on user intent.

---

## Quick Reference

**Route a request:**
```javascript
const result = await routeToSkill(userMessage, context);

if (result.skill) {
  console.log(`Loading skill: ${result.skill}`);
  await loadSkill(result.skill);
} else {
  console.log('Suggestions:', result.suggestions);
}
```

**Get all skills:**
```javascript
const skills = getAllSkills();
console.log(`${skills.length} skills available`);
```

---

*End of Core Orchestrator*
*Part of v4.0.0 Universal Skills Ecosystem*
*Main entry point and navigation hub*
