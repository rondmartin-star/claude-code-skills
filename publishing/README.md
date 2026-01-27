# Publishing Skills - Multi-Platform Content Creation

HTML-first content creation with export to DOCX, PPTX, and PDF across multiple platforms.

**Category:** Publishing
**Skills:** 2 (1 orchestrator + 1 ecosystem)
**Total Size:** ~21KB SKILL.md + references

---

## Overview

Publishing skills coordinate content creation across platforms using an HTML-first workflow with multi-format export capabilities.

```
publishing-orchestrator
└─→ content-creation-ecosystem
    ├─→ social-media.md (Bluesky, Twitter)
    ├─→ newsletter.md (Substack, email)
    ├─→ website.md (Static sites, blogs)
    ├─→ blog.md (Personal/professional blogs)
    ├─→ reference.md (Technical documentation)
    └─→ journal.md (Academic publishing)
```

---

## Skills in This Category

### publishing-orchestrator (~7KB)
**Purpose:** Route to content-creation-ecosystem based on content type

**When to load:**
- "Write a post..."
- "Create an article..."
- "Build a website..."
- "Blog post about..."
- "Write a journal article..."

**Content type detection:**

**Phase 1: Keywords**
- "Bluesky", "Twitter", "post" → social-media
- "Substack", "newsletter" → newsletter
- "website", "static site" → website
- "blog post", "blog" → blog
- "reference material", "documentation" → reference
- "journal article", "academic" → journal

**Phase 2: Interview (if ambiguous)**
Ask user to clarify:
- Platform/audience?
- Length?
- Format requirements?

**Phase 3: Route**
Load content-creation-ecosystem with appropriate reference file

---

### content-creation-ecosystem (~14KB + refs)
**Purpose:** Create HTML-first content with optional export to DOCX, PPTX, PDF

**When to load:**
- Any content creation request
- Always loaded by publishing-orchestrator

**Workflow:**
1. **Create HTML** - Core content format
2. **Style with CSS** - Platform-specific styling
3. **Export** - Convert to target format
   - Bluesky: Plain text (character limit)
   - Substack: HTML (embedded)
   - DOCX: python-docx conversion
   - PPTX: python-pptx conversion
   - PDF: WeasyPrint conversion

**Supported platforms:**
- Social media (Bluesky, Twitter)
- Newsletter (Substack)
- Website (static HTML)
- Blog (WordPress, Ghost, static)
- Reference material (technical docs)
- Journal (peer-reviewed articles)

**Key features:**
- HTML-first approach
- Reusable CSS components
- Multi-format export
- Platform-specific optimizations
- Asset management (images, fonts)

**Reference files:**
- social-media.md (~7KB) - Bluesky/Twitter patterns
- newsletter.md (~11KB) - Substack formatting
- website.md - Static site generation
- blog.md - Blog post templates
- reference.md - Technical documentation
- journal.md - Academic paper formatting

---

## Content Type Comparison

| Type | Length | Format | Primary Platform | Export |
|------|--------|--------|-----------------|--------|
| **Social Media** | 50-500 chars | Plain text | Bluesky, Twitter | Text only |
| **Newsletter** | 500-3000 words | HTML | Substack | HTML, PDF |
| **Website** | Variable | HTML/CSS | Static hosting | HTML |
| **Blog Post** | 1000-3000 words | HTML/Markdown | WordPress, Ghost | HTML, PDF |
| **Reference** | Variable | HTML | Documentation site | HTML, PDF |
| **Journal** | 3000-8000 words | LaTeX/HTML | Academic journals | PDF, DOCX |

---

## Common Workflows

### Workflow 1: Bluesky Post

```
User: "Write a Bluesky post about my new feature"
→ publishing-orchestrator
→ Detects: "Bluesky" + "post"
→ content-creation-ecosystem (social-media.md)
→ Create HTML draft
→ Export to plain text
→ Verify character count (300 limit)
→ Provide post text
```

### Workflow 2: Substack Newsletter

```
User: "Create a newsletter article about property management trends"
→ publishing-orchestrator
→ Detects: "newsletter"
→ content-creation-ecosystem (newsletter.md)
→ Create HTML article
→ Add inline CSS styling
→ Format for Substack
→ Export HTML + PDF
→ Provide both versions
```

### Workflow 3: Technical Documentation

```
User: "Create reference documentation for our API"
→ publishing-orchestrator
→ Detects: "reference documentation"
→ content-creation-ecosystem (reference.md)
→ Create structured HTML
→ Add code syntax highlighting
→ Generate table of contents
→ Export HTML + PDF
→ Provide both versions
```

### Workflow 4: Academic Paper

```
User: "Write a journal article about our research findings"
→ publishing-orchestrator
→ Detects: "journal article"
→ content-creation-ecosystem (journal.md)
→ Follow academic structure (Abstract, Intro, Methods, Results, Discussion)
→ Format citations
→ Generate bibliography
→ Export PDF + DOCX
→ Provide both versions
```

---

## HTML-First Philosophy

### Why HTML First?

1. **Universal format** - Works everywhere
2. **Semantic structure** - Meaningful markup
3. **CSS styling** - Flexible presentation
4. **Easy export** - Convert to other formats
5. **Version control** - Git-friendly

### HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Article Title</title>
    <style>
        /* Inline CSS for portability */
        body { font-family: Georgia, serif; max-width: 800px; margin: 0 auto; }
        h1 { color: #2c3e50; }
        p { line-height: 1.6; }
    </style>
</head>
<body>
    <article>
        <header>
            <h1>Article Title</h1>
            <p class="byline">By Author Name • Date</p>
        </header>

        <section>
            <h2>Section Heading</h2>
            <p>Content here...</p>
        </section>
    </article>
</body>
</html>
```

### Export Process

**HTML → Plain Text (Social Media)**
```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_content, 'html.parser')
text = soup.get_text(separator='\n', strip=True)
```

**HTML → PDF**
```python
from weasyprint import HTML

HTML(string=html_content).write_pdf('output.pdf')
```

**HTML → DOCX**
```python
from docx import Document
from bs4 import BeautifulSoup

doc = Document()
soup = BeautifulSoup(html_content, 'html.parser')

for element in soup.find_all(['h1', 'h2', 'p']):
    if element.name == 'h1':
        doc.add_heading(element.text, level=1)
    elif element.name == 'h2':
        doc.add_heading(element.text, level=2)
    elif element.name == 'p':
        doc.add_paragraph(element.text)

doc.save('output.docx')
```

---

## Platform-Specific Considerations

### Bluesky / Twitter
- **Character limit:** 300 (Bluesky), 280 (Twitter)
- **Links:** Count as 23 characters
- **Hashtags:** Optional, use sparingly
- **Formatting:** Plain text only, no markup

### Substack
- **Length:** 500-3000 words typical
- **Formatting:** Full HTML support
- **Images:** Inline with captions
- **Code:** Use `<pre><code>` blocks
- **CTA:** "Subscribe" button automatic

### Static Website
- **Structure:** Semantic HTML5
- **Styling:** External CSS or inline
- **Responsive:** Mobile-first design
- **Assets:** Relative paths for portability

### Academic Journal
- **Format:** PDF primary, DOCX for editing
- **Citations:** Numbered references
- **Figures:** High-resolution images
- **Tables:** Properly formatted with captions
- **Structure:** IMRaD format (Introduction, Methods, Results, Discussion)

---

## Asset Management

### Images

**Organization:**
```
content/
├── article.html
└── assets/
    ├── images/
    │   ├── header.jpg
    │   └── diagram.png
    └── styles/
        └── article.css
```

**HTML references:**
```html
<img src="assets/images/header.jpg" alt="Description" />
```

### Fonts

**Web fonts:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
```

**Local fonts (for PDF):**
```css
@font-face {
    font-family: 'Custom';
    src: url('assets/fonts/custom.woff2') format('woff2');
}
```

---

## Quality Checklist

### Before Publishing

**Content:**
- [ ] Grammar and spelling checked
- [ ] Links verified
- [ ] Images optimized
- [ ] Citations formatted correctly
- [ ] Metadata complete (title, author, date)

**Format:**
- [ ] HTML validates (W3C validator)
- [ ] CSS renders correctly
- [ ] Mobile-responsive
- [ ] Print stylesheet (if PDF)
- [ ] Accessibility (alt text, semantic HTML)

**Export:**
- [ ] PDF renders correctly
- [ ] DOCX formatting preserved
- [ ] Plain text readable
- [ ] File sizes acceptable

---

## Integration with Other Skills

Publishing skills are independent but can integrate:

**With windows-app-build:**
- Generate documentation from code comments
- Create user manuals from UI specifications
- Export API reference from OpenAPI spec

**With conversation-snapshot:**
- Archive content creation sessions
- Preserve drafts across contexts
- Resume editing in new chat

---

## Best Practices

### 1. Start with Structure

Define outline before writing:
```markdown
1. Introduction
   - Hook
   - Context
   - Thesis
2. Body
   - Point 1
   - Point 2
   - Point 3
3. Conclusion
   - Summary
   - Call to action
```

### 2. Use Semantic HTML

```html
<!-- GOOD -->
<article>
  <header><h1>Title</h1></header>
  <section><h2>Heading</h2><p>Content</p></section>
</article>

<!-- BAD -->
<div class="article">
  <div class="title">Title</div>
  <div class="content">Content</div>
</div>
```

### 3. Inline CSS for Portability

External stylesheets break when content is moved. Use inline or `<style>` tag.

### 4. Test All Export Formats

Don't just check HTML - verify PDF, DOCX, and plain text exports look correct.

### 5. Version Control Content

Track content changes with git:
```bash
git add content/article.html
git commit -m "Draft 1: Introduction complete"
```

---

## Related Skills

- **skill-ecosystem-manager** - Create new content type skills
- **conversation-snapshot** - Archive content creation sessions

---

*Publishing Category - HTML-First Multi-Platform Content Creation*
