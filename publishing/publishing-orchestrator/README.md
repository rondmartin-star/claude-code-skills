# publishing-orchestrator

Coordinate content creation across platforms by routing to content-creation-ecosystem based on content type. Manages HTML-first workflow with multi-format export.

---

## Size

- **SKILL.md:** ~7KB
- **References:** None (routes to content-creation-ecosystem references)
- **Total:** ~7KB

---

## When to Load

### Trigger Phrases

- "Write a post"
- "Create an article"
- "Build a website"
- "Blog post about"
- "Write for Bluesky"
- "Create newsletter"
- "Journal article"
- "Reference material"
- "Technical documentation"

### Context Indicators

- User mentions content creation
- Platform name mentioned (Bluesky, Substack, etc.)
- Content type mentioned (post, article, blog, etc.)
- Publishing/writing request

---

## Purpose

This orchestrator determines which reference file in content-creation-ecosystem to load based on content type:

- **Social media** → social-media.md (Bluesky, Twitter)
- **Newsletter** → newsletter.md (Substack, email)
- **Website** → website.md (Static sites)
- **Blog** → blog.md (WordPress, Ghost)
- **Reference** → reference.md (Technical docs)
- **Journal** → journal.md (Academic papers)

---

## Content Type Detection

### Phase 1: Keyword Matching

| Keywords | Content Type | Reference File |
|----------|--------------|----------------|
| "Bluesky", "Twitter", "post" | Social Media | social-media.md |
| "Substack", "newsletter", "email" | Newsletter | newsletter.md |
| "website", "static site", "landing page" | Website | website.md |
| "blog post", "blog", "WordPress" | Blog | blog.md |
| "reference", "documentation", "API docs" | Reference | reference.md |
| "journal", "academic", "paper", "research" | Journal | journal.md |

### Phase 2: Discovery Interview (if ambiguous)

When keywords don't clearly indicate type, ask:

**Question 1: Platform/Audience**
- "Where will this be published?"
- Options: Social media, Newsletter platform, Website, Blog, Documentation site, Academic journal

**Question 2: Length**
- "How long should this be?"
- Options: Short (50-500 words), Medium (500-3000), Long (3000+)

**Question 3: Format Requirements**
- "What format do you need?"
- Options: Plain text, HTML, Markdown, PDF, DOCX

### Phase 3: Route to Ecosystem

Once content type determined, load content-creation-ecosystem with appropriate reference:

```
publishing-orchestrator
└─→ content-creation-ecosystem
    └─→ [content-type].md reference
```

---

## Routing Logic

### Decision Matrix

| User Request | Detection | Route To |
|--------------|-----------|----------|
| "Write a Bluesky post" | Platform: Bluesky | social-media.md |
| "Create article about..." | Ambiguous length | Ask: Platform? → Route based on answer |
| "Newsletter for Substack" | Platform: Substack | newsletter.md |
| "Build landing page" | Type: Website | website.md |
| "Blog post about feature" | Type: Blog | blog.md |
| "API documentation" | Type: Reference | reference.md |
| "Research paper" | Type: Journal | journal.md |

### Content Type Characteristics

**Social Media:**
- Length: 50-500 characters
- Format: Plain text
- Features: Character limits, hashtags, links
- Export: Text only

**Newsletter:**
- Length: 500-3000 words
- Format: HTML
- Features: Inline styling, images, CTA
- Export: HTML, PDF

**Website:**
- Length: Variable
- Format: HTML/CSS
- Features: Multi-page, navigation, responsive
- Export: HTML files

**Blog:**
- Length: 1000-3000 words
- Format: HTML/Markdown
- Features: Featured images, categories, tags
- Export: HTML, PDF

**Reference:**
- Length: Variable
- Format: HTML
- Features: Table of contents, code blocks, syntax highlighting
- Export: HTML, PDF

**Journal:**
- Length: 3000-8000 words
- Format: LaTeX/HTML
- Features: Abstract, citations, figures, tables
- Export: PDF, DOCX

---

## Integration with content-creation-ecosystem

The orchestrator always loads content-creation-ecosystem, which then loads the appropriate reference file:

```
User: "Write a Bluesky post about my new feature"
→ publishing-orchestrator detects: "Bluesky" + "post"
→ Loads content-creation-ecosystem
→ Ecosystem loads social-media.md reference
→ Create HTML draft
→ Export to plain text (300 char limit)
→ Provide post text
```

---

## HTML-First Workflow

All content types follow the HTML-first pattern:

1. **Create HTML** - Core content in semantic HTML
2. **Style with CSS** - Platform-specific styling
3. **Export to target** - Convert to final format

```html
<!-- HTML source (universal) -->
<article>
  <h1>Title</h1>
  <p>Content here...</p>
</article>

<!-- Exports to: -->
- Plain text (social media)
- Styled HTML (newsletter, website, blog)
- PDF (reference, journal)
- DOCX (journal editing)
```

---

## Common Workflows

### Workflow 1: Social Media Post

```
User: "Write a Bluesky post about our property management feature"
→ publishing-orchestrator
→ Detects: "Bluesky" keyword
→ content-creation-ecosystem (social-media.md)

Process:
1. Create HTML draft
2. Extract text content
3. Verify character count (≤300)
4. Optimize for engagement
5. Provide plain text
```

### Workflow 2: Newsletter Article

```
User: "Create a Substack newsletter about market trends"
→ publishing-orchestrator
→ Detects: "Substack" keyword
→ content-creation-ecosystem (newsletter.md)

Process:
1. Create HTML article structure
2. Add inline CSS styling
3. Format for Substack
4. Export HTML version
5. Export PDF backup
6. Provide both versions
```

### Workflow 3: Technical Documentation

```
User: "Create API reference documentation"
→ publishing-orchestrator
→ Detects: "API reference" keywords
→ content-creation-ecosystem (reference.md)

Process:
1. Create structured HTML
2. Add code syntax highlighting
3. Generate table of contents
4. Make responsive
5. Export HTML + PDF
6. Provide both versions
```

### Workflow 4: Ambiguous Request

```
User: "Create an article"
→ publishing-orchestrator
→ No clear platform detected
→ Discovery interview

Questions:
1. "Where will this be published?" → User: "My blog"
2. "How long should it be?" → User: "About 2000 words"
3. Route to: blog.md

Process:
1. Create blog post structure
2. Add featured image placeholder
3. Format with blog CSS
4. Export HTML + PDF
5. Provide both versions
```

---

## Exit Criteria

Content creation complete when:

- [ ] Content created in HTML format
- [ ] Platform-specific styling applied
- [ ] Exported to target format(s)
- [ ] Character/word count appropriate
- [ ] Images optimized (if applicable)
- [ ] Links verified
- [ ] Final output provided to user

---

## Reference Files (Via content-creation-ecosystem)

The orchestrator routes to content-creation-ecosystem, which loads:

**Social Media:**
- social-media.md (~7KB) - Bluesky/Twitter patterns, character limits

**Newsletter:**
- newsletter.md (~11KB) - Substack formatting, inline CSS

**Website:**
- website.md - Static site generation, responsive design

**Blog:**
- blog.md - Blog post templates, featured images

**Reference:**
- reference.md - Technical documentation, syntax highlighting

**Journal:**
- journal.md - Academic formatting, citations, IMRaD structure

---

## Related Skills

### Coordinates

- **content-creation-ecosystem** - Main content creation skill

### Works With

- **conversation-snapshot** - Archive content creation sessions
- **skill-ecosystem-manager** - Create new content type skills

### Loaded By

- User directly (trigger phrases)
- windows-app-orchestrator (for documentation generation)

---

## Platform-Specific Notes

### Bluesky / Twitter
- **Limit:** 300 chars (Bluesky), 280 (Twitter)
- **Links:** Count as 23 characters
- **No HTML:** Plain text only
- **Optimization:** Front-load key info

### Substack
- **Format:** Full HTML support
- **Length:** 500-3000 words optimal
- **Images:** Inline with captions
- **CTA:** "Subscribe" button automatic

### WordPress / Ghost
- **Format:** HTML or Markdown
- **Featured image:** Required
- **Categories/Tags:** Organized content
- **SEO:** Meta descriptions important

### Academic Journals
- **Structure:** IMRaD (Intro, Methods, Results, Discussion)
- **Citations:** Numbered references
- **Figures/Tables:** High-resolution, captioned
- **Format:** PDF primary, DOCX for editing

---

## Best Practices

### 1. Clarify Early

If ambiguous, run discovery interview immediately:

```
User: "Write an article"
→ Don't guess - ask about platform and length
→ Route to correct content type
```

### 2. HTML-First Always

Even for plain text output, start with HTML:

```
HTML → Extract text (for social media)
HTML → Style and export (for newsletters)
HTML → PDF conversion (for journals)
```

### 3. Optimize for Platform

Apply platform-specific best practices:

```
Bluesky: Front-load, use hashtags sparingly
Substack: Strong intro, CTA at end
Blog: SEO-friendly headings, meta description
Journal: Follow IMRaD, cite properly
```

### 4. Provide Multiple Formats

When applicable, export to multiple formats:

```
Newsletter: HTML (primary) + PDF (backup)
Reference: HTML (web) + PDF (print)
Journal: PDF (primary) + DOCX (editing)
```

---

## Version

- **Version:** 1.0
- **Created:** 2026-01-27
- **Last Updated:** 2026-01-27
- **Status:** Production

---

*Publishing Orchestrator - HTML-First Multi-Platform Content Creation*
