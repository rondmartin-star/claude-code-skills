---
name: publishing-orchestrator
description: >
  Coordinate content creation across platforms with learning-first architecture. Routes to
  content-creation-ecosystem based on content type. Uses content-battle-plan for medium/complex
  operations. Manages HTML-first workflow with multi-format export. Load when: creating content
  for Bluesky, Substack, websites, blogs, or academic publishing.
---

# Publishing Orchestrator

**Purpose:** Route content creation with battle-plan integration
**Size:** ~9KB
**Action:** Detect content type → Assess complexity → Route with or without battle-plan
**Learning Integration:** Uses content-battle-plan for medium/complex content operations

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "write a post" (Bluesky, social media)
- "create an article" (Substack, newsletter)
- "build a website"
- "blog post"
- "journal article"
- "reference material"
- "create content"
- "publish to"

**Content Platform Keywords:**
- Bluesky, Twitter/X, LinkedIn, social media
- Substack, newsletter, email campaign
- Website, landing page, web pages
- Blog, Medium, article
- Journal, academic, peer-reviewed, citation
- Reference docs, documentation, guide

## ❌ DO NOT LOAD WHEN

- Reading existing content
- Discussing content strategy (not creating)
- Content unrelated to publishing platforms
- Internal documentation (use windows-app skills)

---

## Complexity Assessment for Content Operations

**Before routing, assess complexity to determine if battle-plan workflow is needed:**

```javascript
function assessContentComplexity(contentType, context) {
  const complexityIndicators = {
    trivial: [
      context.informationOnly === true,  // Just asking what platforms we support
      context.noCreation === true         // No actual content creation
    ],
    simple: [
      contentType === 'social-media' && context.threadLength === 1,
      context.wordCount < 300,
      context.templateBased === true
    ],
    medium: [
      contentType === 'newsletter' || contentType === 'blog',
      contentType === 'social-media' && context.threadLength > 1,
      context.wordCount >= 300 && context.wordCount < 2000,
      context.multiFormat === true  // Needs HTML + PDF + DOCX
    ],
    complex: [
      contentType === 'website' && context.pageCount > 1,
      contentType === 'journal',
      context.wordCount >= 2000,
      context.citations === true,
      context.requiresSEO === true,
      context.multiPage === true
    ]
  };

  // Check from complex → trivial
  for (const level of ['complex', 'medium', 'simple', 'trivial']) {
    const matches = complexityIndicators[level].filter(indicator => indicator === true);
    if (matches.length > 0) {
      return {
        level,
        useBattlePlan: (level === 'medium' || level === 'complex'),
        confidence: matches.length / complexityIndicators[level].length
      };
    }
  }

  // Default to medium
  return { level: 'medium', useBattlePlan: true, confidence: 0.5 };
}
```

**Complexity Examples:**

| Content Type | Complexity | Use Battle-Plan? | Reason |
|--------------|------------|------------------|--------|
| Single Bluesky post | Simple | No | Short, single post |
| Bluesky thread (10 posts) | Medium | Yes | Multi-step planning |
| Newsletter article | Medium | Yes | Long-form, structure |
| Blog post with SEO | Medium | Yes | SEO validation, quality |
| Multi-page website | Complex | Yes | Navigation, consistency |
| Journal article | Complex | Yes | Citations, peer review quality |

**Battle-Plan Integration:**
```javascript
async function routeContentWithComplexity(contentType, context) {
  const complexity = assessContentComplexity(contentType, context);

  if (!complexity.useBattlePlan) {
    // Trivial or simple - execute directly
    console.log(`${complexity.level} content - executing directly`);
    return {
      skill: 'content-creation-ecosystem',
      contentType,
      battlePlan: null
    };
  }

  // Medium or complex - use content-battle-plan
  console.log(`${complexity.level} content - using content-battle-plan`);
  return {
    skill: 'content-creation-ecosystem',
    contentType,
    battlePlan: 'content-battle-plan',
    complexity: complexity.level
  };
}
```

---

## Routing Logic

### Decision Matrix (Enhanced with Complexity Assessment)

| User Says | Content Type | Load | Reference File |
|-----------|--------------|------|----------------|
| "Write a Bluesky post about X" | Social media | content-creation-ecosystem | social-media.md |
| "Create Substack article on Y" | Newsletter | content-creation-ecosystem | newsletter.md |
| "Build a landing page" | Website | content-creation-ecosystem | website.md |
| "Write blog post about Z" | Blog | content-creation-ecosystem | blog.md |
| "Create reference docs" | Reference | content-creation-ecosystem | reference-material.md |
| "Write journal article" | Academic | content-creation-ecosystem | journal-article.md |

### Skill Loading Path

```python
# Always load main ecosystem skill
"~/.claude/skills/publishing/content-creation-ecosystem/SKILL.md"  # ~13.8KB

# Ecosystem internally loads specific reference based on content type:
"~/.claude/skills/publishing/content-creation-ecosystem/references/social-media.md"       # ~7KB
"~/.claude/skills/publishing/content-creation-ecosystem/references/newsletter.md"         # ~11KB
"~/.claude/skills/publishing/content-creation-ecosystem/references/website.md"            # ~15KB
"~/.claude/skills/publishing/content-creation-ecosystem/references/blog.md"               # ~14KB
"~/.claude/skills/publishing/content-creation-ecosystem/references/reference-material.md" # ~8KB
"~/.claude/skills/publishing/content-creation-ecosystem/references/journal-article.md"    # ~17KB
```

---

## Content Type Detection

### Phase 1: Explicit Indicators

Check user prompt for platform/format:

| Keyword | Content Type | Reference |
|---------|--------------|-----------|
| "Bluesky", "Twitter", "X", "LinkedIn" | Social media | social-media.md |
| "Substack", "newsletter", "email" | Newsletter | newsletter.md |
| "website", "landing page", "site" | Website | website.md |
| "blog", "Medium", "post" | Blog | blog.md |
| "reference", "documentation", "guide" | Reference material | reference-material.md |
| "journal", "academic", "peer-reviewed", "citation" | Journal article | journal-article.md |

### Phase 2: Contextual Clues

| Clue | Likely Type |
|------|-------------|
| Character count mentioned (<300) | Social media |
| "subscribers" mentioned | Newsletter |
| "multiple pages" mentioned | Website |
| "SEO" mentioned | Blog |
| "citations" or "bibliography" mentioned | Journal article |
| "publish to specific URL" | Website or blog |

### Phase 3: Discovery Interview

If ambiguous, ask:
> "What type of content are you creating?
> 1. Social media post (Bluesky, Twitter, LinkedIn)
> 2. Newsletter/email (Substack)
> 3. Website (multiple pages)
> 4. Blog post/article
> 5. Reference material/documentation
> 6. Academic/journal article"

---

## Content Creation Examples

### Example 1: Newsletter (Medium - Battle-Plan)

```
User: "Create a newsletter about OAuth learning skills for technical audience"

Content Type Detection:
  - Platform: newsletter (Substack)
  - Keywords: "newsletter"
  - Detected: Newsletter

Complexity Assessment:
  - Content type: newsletter
  - Estimated length: ~800 words (medium)
  - Audience: technical
  - Level: MEDIUM (structured content, audience-specific)
  - Use battle-plan: YES

Routing:
  → content-battle-plan → content-creation-ecosystem → newsletter.md

═══ CONTENT BATTLE-PLAN ═══
Complexity: medium
Target: newsletter

PHASE 1: CLARIFICATION
  Q: Target audience? → Technical
  Q: Length target? → Medium (500-1000 words)
  Q: Primary goal? → Educate
  ✓ Scope clarified

PHASE 2: KNOWLEDGE CHECK (Pattern Library)
  ✓ Found: newsletter-structure-technical (12 uses, 91% engagement)
  ✓ Found: code-snippet-formatting (best practices)
  ⚠️ Antipattern: missing-call-to-action (reduces engagement 40%)
  Recommendation: Use technical newsletter pattern, include CTA

PHASE 3: PRE-MORTEM (Content-Specific Risks)
  Risk #1: Broken links (likelihood: 3, impact: 3)
    Prevention: Validate all links before publishing
  Risk #2: Code examples don't work (likelihood: 3, impact: 4)
    Prevention: Test all code snippets
  Recommendation: GO WITH CAUTION

PHASE 5: EXECUTION
  Applying pattern: newsletter-structure-technical

  Creating content structure:
    ✓ Compelling subject line
    ✓ Opening hook (problem statement)
    ✓ Main content (3 sections)
    ✓ Code examples with syntax highlighting
    ✓ Call-to-action
    ✓ Unsubscribe link

  [VERIFY-EVIDENCE checkpoints:]
    ✓ Subject line: "Your AI has infinite knowledge and zero habits"
    ✓ All links validated (3 external, 2 internal - all 200 OK)
    ✓ Code examples tested (3 snippets - all runnable)
    ✓ Images optimized (2 diagrams, 45KB total)
    ✓ Call-to-action present
    ✓ Preview text set

PHASE 7: DECLARE COMPLETE
  Requirements Met:
    - Core: 6/6 (100%) ✓
    - Subject, content, examples, CTA, links, unsubscribe
  Status: ✓ SHIPPABLE

PHASE 8: PATTERN UPDATE
  Updated pattern: newsletter-structure-technical
    Applications: 13 (was 12)
    Avg engagement: 92% (was 91%)

  New pattern captured:
    - oauth-learning-explanation (novel way to explain concept)
```

### Example 2: Single Bluesky Post (Simple - No Battle-Plan)

```
User: "Write a short post about Claude Code for Bluesky"

Content Type Detection:
  - Platform: social media (Bluesky)
  - Keywords: "Bluesky", "post"
  - Detected: Social media

Complexity Assessment:
  - Content type: social-media
  - Length: single post (<300 chars)
  - Level: SIMPLE (short, single post)
  - Use battle-plan: NO

Routing:
  → content-creation-ecosystem → social-media.md (direct)

Execution:
  - Load content-creation-ecosystem
  - Load social-media.md reference
  - Create short post
  - Validate character limit
  - Done

[No battle-plan overhead - fast execution for simple content]
```

---

## Integration with content-creation-ecosystem

### HTML-First Design

This orchestrator is a thin router. The heavy lifting happens in content-creation-ecosystem:
- **HTML-first:** All content created as HTML first
- **Multi-format export:** HTML → PDF, DOCX, PPTX via scripts
- **Interactive controls:** View/Print/PDF/Edit buttons in HTML
- **Validation:** Platform-specific checks

### Workflow (Enhanced with Battle-Plan)

```
User Request
     │
     ▼
Publishing Orchestrator
     ├─ Detects content type
     └─ Assesses complexity
          │
          ├─ Trivial/Simple → Direct execution
          │     │
          │     ▼
          │  content-creation-ecosystem/SKILL.md (loads)
          │     │
          │     ▼
          │  Create content (fast path)
          │
          └─ Medium/Complex → Battle-Plan workflow
                │
                ▼
             content-battle-plan
                │
                ├─ PHASE 1: Clarification (target audience, length, goal)
                ├─ PHASE 2: Pattern check (newsletter-structure, blog-seo)
                ├─ PHASE 3: Pre-mortem (broken links, no CTA, SEO issues)
                ├─ PHASE 4: Confirmation (get user approval)
                ├─ PHASE 5: Execute
                │     │
                │     ▼
                │  content-creation-ecosystem/SKILL.md
                │     │
                │     ├─→ routes to social-media.md
                │     ├─→ routes to newsletter.md
                │     ├─→ routes to website.md
                │     ├─→ routes to blog.md
                │     ├─→ routes to reference-material.md
                │     └─→ routes to journal-article.md
                │     │
                │     ▼
                │  Create HTML content
                │     │
                │     ├─ [VERIFY-EVIDENCE: Links valid ✓]
                │     ├─ [VERIFY-EVIDENCE: Images have alt text ✓]
                │     ├─ [VERIFY-EVIDENCE: SEO metadata present ✓]
                │     │
                │     ├─→ Optional: Export to PDF
                │     ├─→ Optional: Export to DOCX
                │     └─→ Optional: Bundle multi-file
                │
                ├─ PHASE 7: Declare complete (block perfectionism)
                └─ PHASE 8: Pattern update (save learnings)
```

---

## Delegation to Other Skills

### When content-creation-ecosystem delegates

The content-creation-ecosystem skill may delegate to:
- **html-presentations:** For keynote/presentation content
- **marketing-collateral:** For brand-consistent materials

**Note:** Publishing orchestrator does NOT directly invoke these. The content-creation-ecosystem handles delegation internally.

### External dependencies

If user mentions:
- "Create a presentation" → Suggest html-presentations skill
- "Create marketing materials" → Suggest marketing-collateral skill
- "Design a logo" → Suggest marketing-collateral skill

---

## Content Type Quick Reference

| Type | Length | Audience | Tone | Citations | Review |
|------|--------|----------|------|-----------|--------|
| **Social** | <300 chars | Public | Casual/punchy | No | None |
| **Newsletter** | 500-3000 words | Subscribers | Conversational | Optional | Self |
| **Website** | Varies | Visitors | Professional | Optional | Team |
| **Blog** | 500-2500 words | Readers | Engaging | Optional | Self |
| **Reference** | Varies | Internal/users | Formal/technical | Required | Team |
| **Journal** | 3000-10000 words | Academics | Formal/scholarly | Required | Peer review |

---

## Exit Gates

### After Content Creation

Before delivery:
- [ ] No placeholder text remaining
- [ ] All links resolve correctly
- [ ] Images have alt text
- [ ] Title and metadata complete
- [ ] Interactive controls functional (View/Print/PDF/Edit)
- [ ] Platform-specific requirements met

### Platform-Specific Requirements

**Bluesky/Social:**
- [ ] Under 300 characters per post
- [ ] Hashtags appropriate
- [ ] Thread structure clear (if multi-post)

**Substack/Newsletter:**
- [ ] Compatible with Substack editor
- [ ] Subscriber focus clear
- [ ] Call-to-action present

**Website:**
- [ ] All pages linked
- [ ] Navigation works
- [ ] Responsive design
- [ ] Assets bundled

**Blog:**
- [ ] SEO metadata present
- [ ] Title tag optimized
- [ ] Meta description written
- [ ] Image optimization

**Reference:**
- [ ] All sources cited
- [ ] Internal links verified
- [ ] Code examples tested

**Journal:**
- [ ] Citation format correct (APA/MLA/Chicago)
- [ ] Abstract present
- [ ] Methodology documented
- [ ] References complete

### Before Export

Before exporting to PDF/DOCX:
- [ ] HTML validates
- [ ] CSS renders correctly
- [ ] Images embedded
- [ ] Fonts supported
- [ ] Test export with sample

---

## Validation Workflow

### Automated Validation

```bash
# Run content validation script
python ~/.claude/skills/publishing/content-creation-ecosystem/scripts/validate_content.py input.html

# Checks:
# - No placeholder text
# - All links resolve
# - Images have alt text
# - Character limits (if social media)
# - Citation format (if journal)
```

### Manual Validation

1. **Preview in browser:** Open HTML in Chrome/Firefox
2. **Test controls:** Click View/Print/PDF/Edit buttons
3. **Check links:** Click all hyperlinks
4. **Verify images:** Confirm all images load
5. **Test export:** Generate PDF/DOCX and review

---

## Context Budget

| Scenario | Skills Loaded | Total Size |
|----------|---------------|------------|
| Social media post | orchestrator + ecosystem + social-media.md | ~28KB |
| Newsletter | orchestrator + ecosystem + newsletter.md | ~32KB |
| Website | orchestrator + ecosystem + website.md | ~36KB |
| Blog post | orchestrator + ecosystem + blog.md | ~35KB |
| Reference docs | orchestrator + ecosystem + reference-material.md | ~29KB |
| Journal article | orchestrator + ecosystem + journal-article.md | ~38KB |

**Note:** Only the relevant reference file is loaded, not all 6 references.

---

## Error Recovery

If wrong content type detected:
1. **Clarify with user:** "I detected [X] content type. Is that correct?"
2. **Load correct reference:** Switch to appropriate reference file
3. **Update routing logic:** If pattern was missed, note for improvement

Example:
```
User: "Write an article about React hooks"
Detected: Newsletter (wrong - ambiguous "article")
Should be: Blog post
Fix: Load blog.md reference
Clarify: "Is this a blog post or newsletter article?"
```

---

## Cross-Skill Coordination

### Standalone Content Creation

User explicitly asks for content:
```
User request → Publishing orchestrator → content-creation-ecosystem → deliver
```

### Part of Larger Workflow

Content creation within broader project:
```
marketing-collateral skill creates brand identity
    ↓
Invokes content-creation-ecosystem for branded content
    ↓
Publishing orchestrator may not be in the path
```

### With Other Skills

- **marketing-collateral:** Provides brand spec for consistent styling
- **conversation-snapshot:** Content decisions documented
- **html-presentations:** For presentation-style content

---

## Quick Reference: Content Type Selection

### Flowchart

```
What platform is this for?
│
├─ Social media platform (Bluesky, Twitter, LinkedIn)
│  └─→ social-media.md
│
├─ Email/newsletter platform (Substack)
│  └─→ newsletter.md
│
├─ Website (multiple pages, navigation)
│  └─→ website.md
│
├─ Blog platform (Medium, personal blog)
│  └─→ blog.md
│
├─ Documentation/reference
│  └─→ reference-material.md
│
└─ Academic journal
   └─→ journal-article.md
```

---

## Configuration

**Battle-Plan Integration Settings:**

```json
{
  "publishingOrchestrator": {
    "battlePlan": {
      "enabled": true,
      "variant": "content-battle-plan",
      "complexityThresholds": {
        "social-media": {
          "singlePost": "simple",
          "thread": "medium"
        },
        "newsletter": "medium",
        "blog": "medium",
        "website": "complex",
        "journal": "complex",
        "reference": "medium"
      },
      "autoAssessComplexity": true,
      "alwaysUseForWebsite": true,
      "alwaysUseForJournal": true
    },
    "contentValidation": {
      "validateLinks": true,
      "checkImages": true,
      "verifySEO": true,
      "testCodeExamples": true
    }
  }
}
```

**Override complexity for specific content:**
```javascript
await publishContent('newsletter', {
  forceComplexity: 'simple',  // Skip battle-plan for quick draft
  skipValidation: false
});
```

---

*End of Publishing Orchestrator*
*Learning Integration: Uses content-battle-plan for medium/complex content operations*
*Ensures quality through pattern library and pre-mortem risk assessment*
