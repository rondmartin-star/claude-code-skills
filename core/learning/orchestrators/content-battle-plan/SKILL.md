---
name: content-battle-plan
description: >
  Battle-plan variant for content creation (newsletters, blogs, documentation, social).
  Specializes master battle-plan with content structure patterns, style antipatterns,
  and quality validation. Use when: creating newsletters, blog posts, documentation.
---

# Content Battle-Plan

**Purpose:** Learning-first workflow for content creation
**Type:** Battle-Plan Variant (Specialized for Content)
**Base:** Extends master battle-plan

---

## Specializations

### 1. Pattern Library Focus

**Category:** content-operations

**Patterns Directory:**
```
.corpus/learning/patterns/content-operations/
├── newsletter-patterns.json
├── blog-patterns.json
├── documentation-patterns.json
└── social-media-patterns.json
```

**Common Content Patterns:**
- newsletter-structure (proven layouts)
- blog-seo-optimization (title, meta, headings)
- documentation-clarity (structure, examples, diagrams)
- social-thread-format (engaging thread structure)

**Common Antipatterns:**
- missing-call-to-action (no clear next step)
- wall-of-text (no paragraph breaks)
- broken-links (dead links in content)
- inconsistent-voice (tone shifts mid-content)

### 2. Pre-Mortem Risk Database

**Risk Database:** `.corpus/learning/risks/content-risks.json`

**Content-Specific Risks:**
```json
{
  "newsletter": [
    {
      "risk": "Broken links in newsletter",
      "likelihood": 3,
      "impact": 3,
      "prevention": "Validate all links before publishing"
    },
    {
      "risk": "Formatting breaks in email clients",
      "likelihood": 4,
      "impact": 3,
      "prevention": "Test in multiple email clients"
    }
  ],
  "blog": [
    {
      "risk": "Poor SEO (title, meta, headings)",
      "likelihood": 3,
      "impact": 4,
      "prevention": "Apply blog-seo-optimization pattern"
    },
    {
      "risk": "No clear call-to-action",
      "likelihood": 4,
      "impact": 3,
      "prevention": "Check for CTA before publishing"
    }
  ],
  "documentation": [
    {
      "risk": "Missing code examples",
      "likelihood": 3,
      "impact": 4,
      "prevention": "Include runnable examples for each concept"
    },
    {
      "risk": "Outdated screenshots/examples",
      "likelihood": 4,
      "impact": 3,
      "prevention": "Verify examples work before publishing"
    }
  ]
}
```

### 3. Verify-Evidence Checks

**Content-specific evidence requirements:**

**For newsletters:**
```javascript
{
  requiredEvidence: [
    "Subject line exists and compelling",
    "All links validated (no 404s)",
    "Images load correctly",
    "Call-to-action present",
    "Unsubscribe link included",
    "Preview text set"
  ]
}
```

**For blog posts:**
```javascript
{
  requiredEvidence: [
    "SEO title set (50-60 chars)",
    "Meta description set (150-160 chars)",
    "H1 heading exists and matches title",
    "Images have alt text",
    "Internal links included",
    "Call-to-action present"
  ]
}
```

### 4. Example Flow: Create Newsletter

```
User: "Create newsletter about OAuth learning skills"

═══ PHASE 1: CLARIFICATION ═══
CLARIFY-REQUIREMENTS:
  Q: Target audience? (Technical/Non-technical)
  Q: Length target? (Short/Medium/Long)
  Q: Primary goal? (Educate/Promote/Engage)
  [User answers: Technical, Medium, Educate]
  ✓ Scope clarified

═══ PHASE 2: KNOWLEDGE CHECK ═══
PATTERN-LIBRARY (content-operations/newsletter):
  ✓ Found: newsletter-structure-technical (12 uses, 91% engagement)
  ✓ Found: code-snippet-formatting (best practices)
  ⚠️ Antipattern: missing-call-to-action (reduces engagement 40%)
  Recommendation: Use technical newsletter pattern, include CTA

═══ PHASE 3: RISK ASSESSMENT ═══
PRE-MORTEM (content-specific):
  Risk #1: Broken links (likelihood: 3, impact: 3)
    Prevention: Validate all links before sending
  Risk #2: Code examples don't work (likelihood: 3, impact: 4)
    Prevention: Test all code snippets
  Recommendation: GO WITH CAUTION
  Conditions: Validate links, test code examples

═══ PHASE 5: EXECUTION ═══
Applying pattern: newsletter-structure-technical

Creating content structure:
  ✓ Compelling subject line
  ✓ Opening hook (problem statement)
  ✓ Main content (3 sections):
    - Section 1: The Problem (knowing that vs knowing how)
    - Section 2: The Solution (learning skills)
    - Section 3: How to Apply (battle-plan pattern)
  ✓ Code examples with syntax highlighting
  ✓ Call-to-action (try battle-plan on next task)
  ✓ Unsubscribe link

[VERIFY-EVIDENCE checkpoints:]
  ✓ Subject line: "Your AI has infinite knowledge and zero habits"
  ✓ All links validated (3 external, 2 internal - all 200 OK)
  ✓ Code examples tested (3 snippets - all runnable)
  ✓ Images optimized (2 diagrams, 45KB total)
  ✓ Call-to-action present
  ✓ Preview text set

═══ PHASE 7: DECLARE COMPLETE ═══
Requirements Met:
  - Core: 6/6 (100%) ✓
  - Subject, content, examples, CTA, links, unsubscribe

Status: ✓ SHIPPABLE

Deferred (nice-to-haves):
  - A/B test subject lines
  - Add video walkthrough
  - Create PDF version

═══ PHASE 8: PATTERN UPDATE ═══
Updated pattern: newsletter-structure-technical
  Applications: 13 (was 12)
  Avg engagement: 92% (was 91%)

New pattern captured:
  - oauth-learning-explanation (novel way to explain concept)
```

---

## Configuration

```json
{
  "contentBattlePlan": {
    "extends": "battle-plan",
    "patternLibrary": {
      "category": "content-operations",
      "subcategories": ["newsletter", "blog", "documentation", "social-media"]
    },
    "preMortem": {
      "riskDatabase": ".corpus/learning/risks/content-risks.json",
      "alwaysCheckLinks": true,
      "alwaysCheckCallToAction": true
    },
    "verifyEvidence": {
      "validateLinks": true,
      "checkImages": true,
      "verifySEO": true,
      "testCodeExamples": true
    },
    "quality": {
      "readabilityCheck": true,
      "grammarCheck": false,
      "plagiarismCheck": false
    }
  }
}
```

---

*End of Content Battle-Plan*
*Specialized variant for content creation*
*Extends master battle-plan with content patterns and quality validation*
