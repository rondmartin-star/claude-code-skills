---
name: content-creation-ecosystem
description: >
  Unified content creation and management ecosystem for professional publishing
  across platforms. Creates HTML-first content with optional export to DOCX, PPTX,
  or PDF. Supports: Bluesky posts, Substack articles, blog posts, websites,
  reference materials, and peer-reviewed journal articles. Use when creating
  content for social media, newsletters, websites, blogs, or academic publishing.
  Triggers on: "write a post", "create an article", "build a website", "blog post",
  "journal article", "reference material", "Bluesky", "Substack".
metadata:
  version: "1.0"
  created: "January 2026"
  total_size: "~85KB (orchestrator + 6 specialized skills + scripts)"
---

# Content Creation & Management Ecosystem

A coordinated system for creating professional content across platforms through structured workflows and HTML-first design with multi-format export.

---

## ⚠️ CRITICAL ARCHITECTURE PRINCIPLES ⚠️

### HTML-First Design

All content types are created as HTML first, then optionally converted:

| Output Format | Primary Use | Conversion Path |
|---------------|-------------|-----------------|
| **HTML** | Default, editing, preview | Native |
| **PDF** | Print, distribution | HTML → PDF via script |
| **DOCX** | Collaborative editing | HTML → DOCX via script |
| **PPTX** | Presentations | Delegates to html-presentations |

### Many Small Files Architecture

For efficient revisioning, content is structured as linked small files:

```
project/
├── index.html          # Navigation/entry point
├── sections/
│   ├── introduction.html
│   ├── methodology.html
│   ├── results.html
│   └── conclusion.html
├── assets/
│   ├── figures/
│   └── styles/
└── metadata.json
```

**Benefits:** Change one section without regenerating everything. Git-friendly. Modular reuse.

### Delegation Pattern

This ecosystem delegates rendering to existing skills where appropriate:

| Content Type | Delegated To | Notes |
|--------------|--------------|-------|
| Presentations | `/mnt/skills/user/html-presentations/SKILL.md` | Full keynote/document support |
| Complex charts | Frontend-design skill | Interactive visualizations |
| Brand identity | Marketing-collateral skill | Consistent branding |

---

## When to Load This Skill

**Trigger Phrases:**
- "Write a Bluesky post about..."
- "Create a Substack article on..."
- "Build a website for..."
- "Write a blog post about..."
- "Create reference material for..."
- "Write a journal article on..."
- "I need content for..."
- "Publish this to..."

**Content Type Keywords:**
- Social media: Bluesky, Twitter/X, LinkedIn
- Newsletters: Substack, newsletter, email
- Web: website, landing page, web page
- Blog: blog post, medium, article
- Academic: journal, peer-reviewed, citation, bibliography

---

## Content Type Decision Matrix

| Question | Social Post | Newsletter | Website | Blog | Reference | Journal |
|----------|-------------|------------|---------|------|-----------|---------|
| Length? | <300 chars | 500-3000 words | Varies | 500-2500 words | Varies | 3000-10000 words |
| Audience? | Public/followers | Subscribers | Visitors | Readers | Internal/Reference | Academic peers |
| Tone? | Casual/punchy | Conversational | Professional | Engaging | Formal/technical | Formal/scholarly |
| Citations? | No | Optional | Optional | Optional | Required | Required/formal |
| Review process? | None | Self | Self/team | Self/team | Team | Peer review |

---

## Ecosystem Architecture

```
content-creation/
├── SKILL.md (this file - ~12KB)
│   Entry point, routing, coordination
├── references/
│   ├── social-media.md (~8KB)
│   │   Bluesky, Twitter/X patterns
│   ├── newsletter.md (~10KB)
│   │   Substack, email newsletter patterns
│   ├── website.md (~12KB)
│   │   Multi-page websites, navigation
│   ├── blog.md (~8KB)
│   │   Blog post patterns, SEO
│   ├── reference-material.md (~10KB)
│   │   Resource libraries, documentation
│   ├── journal-article.md (~15KB)
│   │   Academic writing, citations
│   ├── components.md (~20KB)
│   │   Shared HTML components
│   └── validation.md (~8KB)
│       Quality checklists
├── scripts/
│   ├── init_content.py
│   ├── validate_content.py
│   ├── convert_to_docx.py
│   ├── convert_to_pdf.py
│   └── bundle_content.py
└── assets/
    └── templates/
        └── [content type templates]
```

---

## Quick Start by Content Type

### Bluesky Post
```
Load: references/social-media.md
Constraints: 300 characters, thread support, hashtags
Output: Plain text or HTML preview
```

### Substack Article
```
Load: references/newsletter.md
Structure: Hook → Value → CTA
Output: HTML with Substack-compatible formatting
```

### Website
```
Load: references/website.md
Structure: Multi-file linked architecture
Output: HTML files + assets folder
```

### Blog Post
```
Load: references/blog.md
Structure: Title → Hook → Body → CTA
Output: Single HTML or markdown
```

### Reference Material
```
Load: references/reference-material.md
Structure: Topic → Categories → Links → Annotations
Output: HTML resource library
```

### Journal Article
```
Load: references/journal-article.md
Structure: IMRaD or discipline-specific
Output: HTML + export to DOCX for submission
```

---

## Interactive Controls (All Content Types)

Every HTML output includes interactive controls:

```
┌────────────────────────────────────────────────────────────────┐
│ [View] [Print] [PDF] [Edit in HTML Editor] │ Word Count: XXXX │
└────────────────────────────────────────────────────────────────┘
```

### Control Functions

| Button | Function |
|--------|----------|
| **View** | Toggle between rendered and source view |
| **Print** | Open print dialog (Ctrl/Cmd+P) |
| **PDF** | Generate PDF via browser print-to-PDF |
| **Edit** | Open in external HTML editor at cursor position |

### Cursor Position Tracking

The Edit button opens the HTML file in an editor at the position corresponding to the last cursor position in the rendered content:

1. Content elements have `data-line` attributes
2. Click/selection tracked via JavaScript
3. Editor opened with `+line:column` argument

---

## HTML Template Structure

### Base Template (All Content Types)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{title}}</title>
  <style>
    :root {
      --primary-color: #2563eb;
      --text-color: #1f2937;
      --bg-color: #ffffff;
      --accent-color: #3b82f6;
    }
    /* Content-type specific styles */
  </style>
</head>
<body>
  <div class="controls" id="content-controls">
    <!-- Interactive controls injected here -->
  </div>
  <main class="content" data-content-type="{{type}}">
    <!-- Content here -->
  </main>
  <script>
    // Control panel and cursor tracking
  </script>
</body>
</html>
```

---

## Export Workflow

### HTML → PDF

```bash
python scripts/convert_to_pdf.py input.html --output output.pdf
```

Uses browser-based rendering for accurate CSS support.

### HTML → DOCX

```bash
python scripts/convert_to_docx.py input.html --output output.docx
```

Preserves structure, headings, lists, tables. Images embedded.

### Multi-File Bundle

```bash
python scripts/bundle_content.py project/ --format zip
```

Creates distributable package with all linked files.

---

## Validation Checklist

Before delivery, verify:

### All Content Types
- [ ] No placeholder text remaining
- [ ] All links resolve correctly
- [ ] Images have alt text
- [ ] Title and metadata complete
- [ ] Controls function correctly

### Platform-Specific
- [ ] **Bluesky:** Under 300 characters per post
- [ ] **Substack:** Compatible with Substack editor
- [ ] **Website:** All pages linked, navigation works
- [ ] **Blog:** SEO metadata present
- [ ] **Reference:** All sources cited
- [ ] **Journal:** Citation format correct (APA/MLA/Chicago/etc.)

---

## Error Prevention

| Common Error | Prevention |
|--------------|------------|
| Broken links in multi-file | Run `validate_content.py` before delivery |
| Missing images | Use relative paths, verify existence |
| Character limit exceeded | Show real-time count for social media |
| Citation format errors | Use reference manager integration |
| Export formatting loss | Test export early in workflow |

---

## Content Type Quick Reference

| Type | Load Reference | Key Constraint | Typical Output |
|------|----------------|----------------|----------------|
| Bluesky | social-media.md | 300 chars | Text/thread |
| Substack | newsletter.md | Subscriber focus | HTML article |
| Website | website.md | Multi-page | HTML + assets |
| Blog | blog.md | SEO optimized | HTML/markdown |
| Reference | reference-material.md | Organized links | HTML library |
| Journal | journal-article.md | Formal citations | HTML → DOCX |

---

## Resources

**Reference Files:**
- `references/social-media.md` - Bluesky, Twitter/X patterns
- `references/newsletter.md` - Substack, email templates
- `references/website.md` - Multi-page site architecture
- `references/blog.md` - Blog post patterns
- `references/reference-material.md` - Resource library design
- `references/journal-article.md` - Academic writing
- `references/components.md` - Shared HTML components
- `references/validation.md` - Quality checklists

**Scripts:**
- `scripts/init_content.py` - Initialize new content project
- `scripts/validate_content.py` - Pre-delivery validation
- `scripts/convert_to_docx.py` - HTML to DOCX conversion
- `scripts/convert_to_pdf.py` - HTML to PDF conversion
- `scripts/bundle_content.py` - Package for distribution

**Delegated Skills:**
- `/mnt/skills/user/html-presentations/SKILL.md` - Presentations
- `/mnt/skills/user/marketing-collateral/SKILL.md` - Brand identity

---

## Integration with Marketing Collateral Ecosystem

This ecosystem integrates with the Marketing Collateral skill for brand-consistent content:

### Delegation Pattern

| When Creating | Delegate To | For |
|---------------|-------------|-----|
| Brand identity | `/mnt/skills/user/marketing-collateral/SKILL.md` | Logo, colors, typography |
| Presentations | `/mnt/skills/user/html-presentations/SKILL.md` | Keynote/document presentations |
| Marketing copy | Marketing Collateral's content-strategy.md | Messaging frameworks |

### Brand Specification Integration

When user has existing brand spec from marketing-collateral:

```
1. Load brand spec from prior session
2. Apply brand colors to CSS :root variables
3. Use brand typography
4. Maintain voice/tone consistency
5. Include brand assets (logo, etc.)
```

### Content-to-Marketing Pipeline

```
Content Creation → Marketing Collateral → Distribution
     ↓                    ↓                    ↓
  Blog post         Brand-consistent      Multi-channel
  Newsletter        presentation          deployment
  Article           print collateral      
```

---

## Discovery Interview Process

When content requirements are unclear, conduct discovery:

### Phase 1: Content Basics (3-5 questions)

**Q1: Content Type**
```
What type of content do you need?
- Social media post (Bluesky, Twitter, LinkedIn)
- Newsletter/email (Substack)
- Website pages
- Blog post/article
- Reference library
- Academic/journal article
```

**Q2: Audience**
```
Who is this for?
- General public
- Specific professional audience
- Academic peers
- Internal team
- Existing subscribers/followers
```

**Q3: Purpose**
```
What should this content achieve?
- Inform/educate
- Persuade/convince
- Entertain
- Document/reference
- Drive action (CTA)
```

### Phase 2: Content Details (2-4 questions)

**Q4: Existing Materials**
```
Do you have any existing content to work from?
- Outline or notes
- Previous version to update
- Research/sources
- Brand guidelines
```

**Q5: Format Requirements**
```
Any specific format requirements?
- Length constraints
- Citation style (academic)
- Visual elements needed
- Output format (HTML, PDF, DOCX)
```

### Phase 3: Brand Context (if applicable)

**Q6: Brand Identity**
```
Do you have existing brand materials?
- Logo (upload if available)
- Color palette
- Typography preferences
- Brand voice guidelines
```

---

## Error Prevention

| Common Error | Prevention | Fix |
|--------------|------------|-----|
| Wrong content type | Ask clarifying questions | Re-select appropriate reference |
| Missing brand consistency | Load brand spec first | Apply CSS variables |
| Broken links in multi-file | Validate before delivery | Run validate_content.py |
| Character limits exceeded | Show real-time counts | Trim content |
| Export formatting issues | Test export early | Adjust source HTML |
| Missing interactive controls | Use component template | Add controls div |

---

## Success Metrics

Content ecosystem succeeds when:

- [ ] **Speed:** First draft in 15-45 minutes (varies by type)
- [ ] **Quality:** Passes validation with 0 errors
- [ ] **Consistency:** Brand elements applied correctly
- [ ] **Usability:** Controls (View/Print/PDF/Edit) functional
- [ ] **Portability:** Exports work in target platforms
- [ ] **Maintainability:** Multi-file structure enables efficient revision

---

*End of Content Creation & Management Ecosystem Orchestrator - v1.0*
