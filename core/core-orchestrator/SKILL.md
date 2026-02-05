---
name: core-orchestrator
description: >
  Main orchestrator for v4.0 Universal Skills Ecosystem. Routes users to appropriate
  skills based on intent: corpus management, auditing, content work, or utilities.
  Integrates battle-plan learning workflow for medium/complex tasks.
  Use when: starting new tasks, unclear which skill to use, or navigating ecosystem.
---

# Core Orchestrator

**Purpose:** Universal ecosystem navigation and routing with learning-first architecture
**Type:** Orchestrator Skill (Entry Point)
**Learning Integration:** Routes complex tasks through battle-plan variants

---

## ⚡ ALWAYS LOAD THIS SKILL

This is the main entry point for the v4.0 Universal Skills Ecosystem. Load when:
- User starts a new task
- Intent is unclear
- Multiple skills might apply
- User asks "what can you do?"

---

## Learning-First Architecture

**Philosophy:** Medium/complex tasks flow through battle-plan learning workflow

**Routing Flow:**
```
User Request
    ↓
Assess Complexity (trivial/simple/medium/complex)
    ↓
├─ Trivial → Direct execution (skip battle-plan)
├─ Simple → Pattern-check only → Direct execution
└─ Medium/Complex → Battle-Plan Variant → Execution
    ├─ Corpus operations → corpus-battle-plan
    ├─ Audit operations → audit-battle-plan
    └─ Content operations → content-battle-plan
```

**Complexity Assessment Criteria:**
```javascript
function assessComplexity(userRequest, context = {}) {
  const indicators = {
    trivial: [
      /^(list|show|display|get|what is)\b/i,  // Read-only queries
      /^help\b/i,                              // Help requests
      context.wordCount < 5                    // Very short requests
    ],
    simple: [
      /^(check|verify|validate)\b.*single/i,   // Single-item checks
      /^(read|view)\b/i,                       // Read operations
      context.estimatedFiles === 1             // Single file operation
    ],
    medium: [
      /\b(initialize|configure|create|setup)\b/i,  // Setup operations
      /\b(fix|update|modify)\b.*multiple/i,        // Multi-item changes
      /\b(review|edit)\b.*document/i,              // Document work
      context.estimatedFiles > 1 && context.estimatedFiles < 5
    ],
    complex: [
      /\b(migrate|convert|refactor)\b/i,           // Structural changes
      /\b(implement|build|develop)\b/i,            // New features
      /\b(convergence|3-3-1)\b/i,                  // Multi-audit convergence
      /\b(architectural|design)\b/i,               // Architectural decisions
      context.estimatedFiles >= 5,                 // Many files affected
      context.multipleAudits === true,             // Multiple audit types
      context.hasRisks === true                    // User-facing or risky changes
    ]
  };

  // Check indicators in order (complex → trivial)
  for (const complexity of ['complex', 'medium', 'simple', 'trivial']) {
    const matches = indicators[complexity].filter(indicator => {
      if (typeof indicator === 'boolean') return indicator;
      if (indicator instanceof RegExp) return indicator.test(userRequest);
      return false;
    });

    if (matches.length > 0) {
      return {
        level: complexity,
        confidence: matches.length / indicators[complexity].length,
        indicators: matches.map(m => m.toString())
      };
    }
  }

  // Default to medium if unclear
  return { level: 'medium', confidence: 0.5, indicators: ['default'] };
}
```

**Battle-Plan Variant Selection:**
```javascript
function selectBattlePlanVariant(category, userRequest) {
  // Map categories to battle-plan variants
  const variantMap = {
    corpus: 'corpus-battle-plan',
    audit: 'audit-battle-plan',
    content: 'content-battle-plan',
    utility: null  // Utilities skip battle-plan (usually simple operations)
  };

  const variant = variantMap[category];

  if (!variant) {
    // No specific variant - use master battle-plan
    return 'battle-plan';
  }

  return variant;
}
```

**Enhanced Routing with Battle-Plan:**
```javascript
async function routeWithBattlePlan(userRequest, context = {}) {
  // Step 1: Assess complexity
  const complexity = assessComplexity(userRequest, context);
  console.log(`Task complexity: ${complexity.level} (${Math.round(complexity.confidence * 100)}% confidence)`);

  // Step 2: Determine category
  const category = detectCategory(userRequest);  // corpus, audit, content, utility

  // Step 3: Get target skill
  const targetSkill = await routeToSkill(userRequest, context);

  // Step 4: Apply battle-plan routing based on complexity
  if (complexity.level === 'trivial') {
    // Trivial: Skip battle-plan entirely
    console.log('Trivial task - executing directly');
    return { skill: targetSkill.skill, battlePlan: null };
  }

  if (complexity.level === 'simple') {
    // Simple: Pattern-check only (no full battle-plan)
    console.log('Simple task - checking patterns only');
    const patterns = await patternLibrary.findRelevant({
      description: userRequest,
      category: category
    });

    if (patterns.length > 0) {
      console.log(`Found ${patterns.length} relevant patterns`);
    }

    return { skill: targetSkill.skill, battlePlan: null, patterns };
  }

  // Medium or Complex: Full battle-plan workflow
  console.log(`${complexity.level} task - using battle-plan workflow`);
  const battlePlanVariant = selectBattlePlanVariant(category, userRequest);

  return {
    skill: targetSkill.skill,
    battlePlan: battlePlanVariant,
    complexity: complexity.level,
    workflow: 'full'
  };
}
```

**Battle-Plan Execution:**
```javascript
async function executeWithBattlePlan(routing) {
  if (!routing.battlePlan) {
    // No battle-plan - execute directly
    return await loadSkill(routing.skill);
  }

  // Load battle-plan variant
  console.log(`\n═══ BATTLE-PLAN WORKFLOW ═══`);
  console.log(`Variant: ${routing.battlePlan}`);
  console.log(`Target skill: ${routing.skill}`);
  console.log(`Complexity: ${routing.complexity}\n`);

  const battlePlan = await loadSkill(routing.battlePlan);

  // Battle-plan will sequence through 8 phases and eventually execute target skill
  const result = await battlePlan.execute({
    targetSkill: routing.skill,
    userRequest: routing.userRequest,
    complexity: routing.complexity
  });

  return result;
}
```

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

**Enhanced routing with battle-plan integration:**

**Priority order:**
1. Explicit skill name mentioned
2. Utility operations (backup, export)
3. Audit operations
4. Corpus management
5. Content management

**Then apply complexity-based battle-plan routing**

```javascript
async function routeToSkill(userMessage, context = {}) {
  const message = userMessage.toLowerCase();

  // 1. Check for explicit skill name
  const explicitSkill = checkExplicitSkillName(message);
  if (explicitSkill) {
    return { skill: explicitSkill, confidence: 'high', category: detectCategoryFromSkill(explicitSkill) };
  }

  // 2. Check utilities (high priority, specific actions)
  const utilitySkill = routeUtilityIntent(message);
  if (utilitySkill) {
    return { skill: utilitySkill, confidence: 'high', category: 'utility' };
  }

  // 3. Check audit operations
  if (/\b(audit|check|validate|scan|analyze)\b/i.test(message)) {
    const auditSkill = routeAuditIntent(message);
    return { skill: auditSkill, confidence: 'high', category: 'audit' };
  }

  // 4. Check corpus management
  if (/\bcorpus\b/i.test(message)) {
    const corpusSkill = routeCorpusIntent(message);
    return { skill: corpusSkill, confidence: 'medium', category: 'corpus' };
  }

  // 5. Check content management
  if (/\b(review|edit|author|content|document)\b/i.test(message)) {
    const contentSkill = routeContentIntent(message);
    return { skill: contentSkill, confidence: 'medium', category: 'content' };
  }

  // 6. No clear match - ask for clarification
  return {
    skill: null,
    confidence: 'low',
    category: null,
    suggestions: getSuggestedSkills(message, context)
  };
}

function detectCategoryFromSkill(skillName) {
  if (/corpus/.test(skillName)) return 'corpus';
  if (/audit|convergence|fix/.test(skillName)) return 'audit';
  if (/review|edit|author|content/.test(skillName)) return 'content';
  if (/backup|export|restore/.test(skillName)) return 'utility';
  return 'other';
}

/**
 * MAIN ENTRY POINT: Enhanced routing with battle-plan integration
 */
async function route(userRequest, context = {}) {
  // Step 1: Detect target skill and category
  const routing = await routeToSkill(userRequest, context);

  if (!routing.skill) {
    // No skill matched - show suggestions
    return {
      action: 'clarify',
      suggestions: routing.suggestions
    };
  }

  // Step 2: Assess complexity
  const complexity = assessComplexity(userRequest, {
    ...context,
    category: routing.category,
    targetSkill: routing.skill
  });

  // Step 3: Determine if battle-plan is needed
  const needsBattlePlan = complexity.level === 'medium' || complexity.level === 'complex';

  if (!needsBattlePlan) {
    // Trivial or simple - execute directly (optionally with pattern-check)
    console.log(`${complexity.level} task - executing directly`);

    if (complexity.level === 'simple') {
      // Quick pattern check
      const patterns = await patternLibrary.findRelevant({
        description: userRequest,
        category: routing.category
      });

      if (patterns.length > 0) {
        console.log(`Found ${patterns.length} relevant patterns - applying automatically`);
      }
    }

    return {
      action: 'execute',
      skill: routing.skill,
      complexity: complexity.level,
      battlePlan: null
    };
  }

  // Step 4: Select battle-plan variant
  const battlePlanVariant = selectBattlePlanVariant(routing.category, userRequest);

  console.log(`\n═══ BATTLE-PLAN ROUTING ═══`);
  console.log(`Complexity: ${complexity.level}`);
  console.log(`Category: ${routing.category}`);
  console.log(`Battle-plan variant: ${battlePlanVariant}`);
  console.log(`Target skill: ${routing.skill}`);
  console.log(`═══════════════════════════\n`);

  return {
    action: 'battle-plan',
    skill: routing.skill,
    battlePlan: battlePlanVariant,
    complexity: complexity.level,
    category: routing.category,
    userRequest: userRequest
  };
}
```

---

## Battle-Plan Integration Examples

### Example 1: Trivial Task (No Battle-Plan)

```
User: "List all corpus configurations"

Assessment:
  - Complexity: TRIVIAL (read-only query)
  - Category: corpus
  - Target skill: corpus-config

Routing:
  - Battle-plan: NO (trivial task)
  - Action: Execute directly

Result: Load corpus-config skill and list configurations
```

### Example 2: Simple Task (Pattern-Check Only)

```
User: "Check if this file has accessibility issues"

Assessment:
  - Complexity: SIMPLE (single-file check)
  - Category: audit
  - Target skill: audits/accessibility

Routing:
  - Battle-plan: NO (simple task)
  - Pattern-check: YES
  - Action: Quick pattern lookup → Execute directly

Result:
  - Found pattern: "wcag-validation-common-issues" (8 applications, 94% success)
  - Apply pattern automatically
  - Execute accessibility audit with known patterns
```

### Example 3: Medium Task (Full Battle-Plan)

```
User: "Initialize this as a corpus with code quality audits"

Assessment:
  - Complexity: MEDIUM (initialization, multiple files)
  - Category: corpus
  - Target skill: corpus-init

Routing:
  - Battle-plan: YES
  - Variant: corpus-battle-plan
  - Action: Full battle-plan workflow

Result:
═══ BATTLE-PLAN WORKFLOW ═══
Variant: corpus-battle-plan
Target skill: corpus-init
Complexity: medium

PHASE 1: CLARIFICATION
  Q: Which audits? → Code quality
  Q: Initialize where? → /users/project (confirmed)
  ✓ Scope clarified

PHASE 2: KNOWLEDGE CHECK
  ✓ Found pattern: corpus-init-directory-structure (15 uses, 93% success)
  ⚠️ Antipattern: wrong-directory-init (3 occurrences)

PHASE 3: PRE-MORTEM
  Risk #1: Wrong directory (likelihood: 3, impact: 4)
    Prevention: Confirm directory with user
  Risk #2: Overwrite existing (likelihood: 2, impact: 5)
    Prevention: Check for existing .corpus/
  Recommendation: GO (with confirmations)

PHASE 4: CONFIRMATION
  About to initialize corpus in: /users/project
  Proceed? [Y/n] → YES

PHASE 5: EXECUTION
  [corpus-init executes with monitoring]

PHASE 7: DECLARE COMPLETE
  ✓ SHIPPABLE (all requirements met)

PHASE 8: PATTERN UPDATE
  Updated pattern: corpus-init-directory-structure (16 applications, 93.75% success)
```

### Example 4: Complex Task (Full Battle-Plan)

```
User: "Run convergence to fix all code quality and security issues"

Assessment:
  - Complexity: COMPLEX (multiple audits, many fixes, GATE convergence)
  - Category: audit
  - Target skill: convergence-engine

Routing:
  - Battle-plan: YES
  - Variant: audit-battle-plan
  - Action: Full battle-plan workflow

Result:
═══ BATTLE-PLAN WORKFLOW ═══
Variant: audit-battle-plan
Target skill: convergence-engine
Complexity: complex

PHASE 2: KNOWLEDGE CHECK
  ✓ Found 45 fix patterns in library
  ⚠️ Antipattern: fix-symptom-not-cause (8 occurrences)

PHASE 3: PRE-MORTEM
  Risk #1: Fixes break functionality (likelihood: 4, impact: 5)
    Prevention: Run tests after each fix
  Risk #2: GATE doesn't converge (likelihood: 3, impact: 4)
    Prevention: detect-infinite-loop, fix root causes
  Recommendation: GO WITH CAUTION

PHASE 5: EXECUTION
  [convergence-engine runs with full monitoring]
  - verify-evidence checkpoints
  - detect-infinite-loop protection
  - manage-context for long sessions

PHASE 7: DECLARE COMPLETE
  ✓ SHIPPABLE (3 clean GATE passes)

PHASE 8: PATTERN UPDATE
  - 3 new fix patterns saved
  - 2 antipatterns updated
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

## Quick Decision Tree (Enhanced with Battle-Plan)

```
User Request
    │
    ├─ Mentions specific skill name? → Detect category → Assess complexity
    │
    ├─ Backup/Export/Restore? → Utilities → Assess complexity
    │
    ├─ Audit/Check/Validate? → Detect audit type → Assess complexity
    │   ├─ Quality/Security/Performance/Dependency? → Technical audits
    │   ├─ Content/A11y/SEO? → User audits
    │   ├─ Consistency/Navigation? → Corpus audits
    │   └─ Convergence/Fix? → Holistic orchestration
    │
    ├─ Corpus/Initialize/Configure? → Corpus management → Assess complexity
    │
    ├─ Review/Edit/Author? → Content management → Assess complexity
    │
    └─ Unclear → Show welcome message & get clarification

        ↓ (After skill detection)

    COMPLEXITY ASSESSMENT
        │
        ├─ TRIVIAL (read-only, help)
        │   → Execute directly (no battle-plan)
        │
        ├─ SIMPLE (single-item checks)
        │   → Pattern-check → Execute directly
        │
        ├─ MEDIUM (setup, multi-item, documents)
        │   → Battle-Plan Variant → 8-Phase Workflow → Execute
        │       ├─ Corpus category → corpus-battle-plan
        │       ├─ Audit category → audit-battle-plan
        │       └─ Content category → content-battle-plan
        │
        └─ COMPLEX (migrations, convergence, architecture)
            → Battle-Plan Variant → 8-Phase Workflow → Execute
                ├─ Corpus category → corpus-battle-plan
                ├─ Audit category → audit-battle-plan
                └─ Content category → content-battle-plan
```

**8-Phase Battle-Plan Workflow:**
```
1. CLARIFY-REQUIREMENTS (force problem articulation)
2. PATTERN-LIBRARY (check known solutions)
3. PRE-MORTEM (anticipate failures)
4. CONFIRM-OPERATION (get user approval)
5. EXECUTE (with monitoring: verify-evidence, detect-infinite-loop, manage-context)
6. ERROR-REFLECTION (if errors occurred)
7. DECLARE-COMPLETE (block perfectionism)
8. PATTERN-UPDATE (save learnings)
```

---

## Configuration

**Battle-Plan Integration Settings:**

```json
{
  "coreOrchestrator": {
    "battlePlan": {
      "enabled": true,
      "complexityThresholds": {
        "trivial": {
          "useBattlePlan": false,
          "usePatternCheck": false
        },
        "simple": {
          "useBattlePlan": false,
          "usePatternCheck": true
        },
        "medium": {
          "useBattlePlan": true,
          "variant": "auto"
        },
        "complex": {
          "useBattlePlan": true,
          "variant": "auto"
        }
      },
      "variantMapping": {
        "corpus": "corpus-battle-plan",
        "audit": "audit-battle-plan",
        "content": "content-battle-plan",
        "utility": null
      },
      "autoDetectComplexity": true,
      "allowUserOverride": true
    }
  }
}
```

---

## Quick Reference

**Enhanced routing with battle-plan:**
```javascript
// Main routing entry point
const routing = await route(userRequest, context);

if (routing.action === 'clarify') {
  // No clear skill match
  console.log('Suggestions:', routing.suggestions);
  return;
}

if (routing.action === 'execute') {
  // Trivial or simple - execute directly
  console.log(`Executing ${routing.skill} (${routing.complexity})`);
  await loadSkill(routing.skill);
  return;
}

if (routing.action === 'battle-plan') {
  // Medium or complex - use battle-plan workflow
  console.log(`Using ${routing.battlePlan} for ${routing.skill}`);
  const battlePlan = await loadSkill(routing.battlePlan);
  const result = await battlePlan.execute({
    targetSkill: routing.skill,
    userRequest: routing.userRequest,
    complexity: routing.complexity
  });
  return result;
}
```

**Assess complexity manually:**
```javascript
const complexity = assessComplexity(userRequest, context);
console.log(`Complexity: ${complexity.level} (${complexity.confidence * 100}% confidence)`);
```

**Select battle-plan variant:**
```javascript
const variant = selectBattlePlanVariant('corpus', userRequest);
console.log(`Battle-plan variant: ${variant}`);  // corpus-battle-plan
```

**Get all skills:**
```javascript
const skills = getAllSkills();
console.log(`${skills.length} skills available`);
```

---

## Integration with Learning Skills

**Pattern Library:**
- Trivial tasks: Skip entirely
- Simple tasks: Quick lookup before execution
- Medium/Complex tasks: Full pattern-library check in Phase 2 of battle-plan

**Pre-Mortem:**
- Only runs for medium/complex tasks (via battle-plan)
- Uses category-specific risk databases

**Monitoring:**
- verify-evidence, detect-infinite-loop, manage-context only active during battle-plan execution
- Trivial/simple tasks execute without monitoring overhead

**Feedback Loop:**
- Pattern library grows with each battle-plan execution
- Antipatterns captured from ERROR-AND-FIXES-LOG.md files
- Compound learning: each task builds on previous learnings

---

*End of Core Orchestrator*
*Part of v4.0.0 Universal Skills Ecosystem*
*Main entry point and navigation hub*
*Enhanced with learning-first architecture via battle-plan integration*
