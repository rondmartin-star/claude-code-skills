---
name: publishing-orchestrator
description: >
  Coordinate content creation across platforms. Routes to content-creation-ecosystem
  based on content type. Manages HTML-first workflow with multi-format export.
  Load when: creating content for Bluesky, Substack, websites, blogs, or academic
  publishing.
---

# Publishing Orchestrator

**Purpose:** Route content creation requests to appropriate specialized skill
**Size:** ~7KB (intentionally minimal)
**Action:** Detect content type → Load content-creation-ecosystem → Route to reference

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

## Routing Logic

### Decision Matrix

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

## Integration with content-creation-ecosystem

### HTML-First Design

This orchestrator is a thin router. The heavy lifting happens in content-creation-ecosystem:
- **HTML-first:** All content created as HTML first
- **Multi-format export:** HTML → PDF, DOCX, PPTX via scripts
- **Interactive controls:** View/Print/PDF/Edit buttons in HTML
- **Validation:** Platform-specific checks

### Workflow

```
User Request
     │
     ▼
Publishing Orchestrator (detects content type)
     │
     ▼
content-creation-ecosystem/SKILL.md (loads)
     │
     ├─→ routes to social-media.md (for Bluesky posts)
     ├─→ routes to newsletter.md (for Substack articles)
     ├─→ routes to website.md (for multi-page sites)
     ├─→ routes to blog.md (for blog posts)
     ├─→ routes to reference-material.md (for documentation)
     └─→ routes to journal-article.md (for academic papers)
     │
     ▼
Create HTML content
     │
     ├─→ Optional: Export to PDF (via convert_to_pdf.py)
     ├─→ Optional: Export to DOCX (via convert_to_docx.py)
     └─→ Optional: Bundle multi-file (via bundle_content.py)
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

*End of Publishing Orchestrator*
