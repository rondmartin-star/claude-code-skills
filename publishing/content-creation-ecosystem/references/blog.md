# Blog Post Content Reference

**Output Types:** Individual blog posts, article series  
**Load when:** User mentions blog post, article, Medium, or content marketing piece

---

## Blog Post Structure

### Standard Article Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{{meta_description}}">
  <meta name="author" content="{{author}}">
  <meta name="keywords" content="{{keywords}}">
  
  <!-- Open Graph -->
  <meta property="og:type" content="article">
  <meta property="og:title" content="{{title}}">
  <meta property="og:description" content="{{og_description}}">
  <meta property="og:image" content="{{og_image}}">
  <meta property="article:published_time" content="{{iso_date}}">
  <meta property="article:author" content="{{author}}">
  <meta property="article:tag" content="{{tags}}">
  
  <title>{{title}}</title>
  
  <style>
    :root {
      --text-color: #1f2937;
      --text-light: #6b7280;
      --accent-color: #2563eb;
      --bg-color: #ffffff;
      --bg-light: #f9fafb;
      --border-color: #e5e7eb;
    }
    
    body {
      font-family: Georgia, 'Times New Roman', serif;
      line-height: 1.8;
      color: var(--text-color);
      max-width: 720px;
      margin: 0 auto;
      padding: 2rem 1.5rem;
      background: var(--bg-color);
    }
    
    .controls {
      background: var(--bg-light);
      padding: 0.75rem 1rem;
      border-radius: 8px;
      margin-bottom: 2rem;
      display: flex;
      gap: 0.5rem;
      align-items: center;
      flex-wrap: wrap;
      position: sticky;
      top: 0;
      z-index: 100;
    }
    .controls button {
      padding: 0.4rem 0.8rem;
      border: 1px solid var(--border-color);
      border-radius: 4px;
      background: white;
      cursor: pointer;
      font-size: 0.85rem;
    }
    .controls button:hover { background: #f0f0f0; }
    .controls .word-count {
      margin-left: auto;
      color: var(--text-light);
      font-size: 0.85rem;
    }
    
    article { position: relative; }
    
    h1 {
      font-size: 2.5rem;
      line-height: 1.15;
      margin-bottom: 0.5rem;
      font-weight: 700;
    }
    
    .meta {
      color: var(--text-light);
      font-family: -apple-system, BlinkMacSystemFont, sans-serif;
      font-size: 0.9rem;
      margin-bottom: 2rem;
      display: flex;
      gap: 1rem;
      flex-wrap: wrap;
    }
    
    .lead {
      font-size: 1.25rem;
      color: var(--text-light);
      margin-bottom: 2rem;
      font-style: italic;
    }
    
    h2 {
      font-size: 1.75rem;
      margin-top: 2.5rem;
      margin-bottom: 1rem;
    }
    
    h3 {
      font-size: 1.35rem;
      margin-top: 2rem;
      margin-bottom: 0.75rem;
    }
    
    p { margin: 1.25rem 0; }
    
    a {
      color: var(--accent-color);
      text-decoration: underline;
    }
    
    blockquote {
      border-left: 4px solid var(--accent-color);
      margin: 2rem 0;
      padding: 0.5rem 0 0.5rem 1.5rem;
      font-style: italic;
      color: var(--text-light);
    }
    
    .pullquote {
      font-size: 1.5rem;
      text-align: center;
      padding: 2rem;
      margin: 2rem -1rem;
      background: var(--bg-light);
      border-radius: 8px;
      font-style: italic;
    }
    
    img {
      max-width: 100%;
      height: auto;
      margin: 2rem 0;
      border-radius: 8px;
    }
    
    .caption {
      text-align: center;
      font-size: 0.9rem;
      color: var(--text-light);
      margin-top: -1.5rem;
      margin-bottom: 2rem;
      font-style: italic;
    }
    
    ul, ol {
      margin: 1.25rem 0;
      padding-left: 1.5rem;
    }
    
    li { margin: 0.5rem 0; }
    
    code {
      font-family: 'SF Mono', Monaco, monospace;
      background: var(--bg-light);
      padding: 0.2rem 0.4rem;
      border-radius: 4px;
      font-size: 0.9em;
    }
    
    pre {
      background: #1f2937;
      color: #f9fafb;
      padding: 1.5rem;
      border-radius: 8px;
      overflow-x: auto;
      margin: 2rem 0;
    }
    pre code {
      background: none;
      padding: 0;
    }
    
    .tags {
      margin-top: 3rem;
      padding-top: 1.5rem;
      border-top: 1px solid var(--border-color);
    }
    .tags a {
      display: inline-block;
      background: var(--bg-light);
      padding: 0.25rem 0.75rem;
      border-radius: 100px;
      font-size: 0.85rem;
      margin-right: 0.5rem;
      text-decoration: none;
      color: var(--text-light);
    }
    
    .author-box {
      margin-top: 3rem;
      padding: 1.5rem;
      background: var(--bg-light);
      border-radius: 8px;
      display: flex;
      gap: 1rem;
      align-items: flex-start;
    }
    .author-avatar {
      width: 64px;
      height: 64px;
      border-radius: 50%;
      background: var(--accent-color);
    }
    .author-bio { flex: 1; }
    .author-name { font-weight: 700; margin-bottom: 0.25rem; }
    .author-desc { font-size: 0.9rem; color: var(--text-light); }
    
    .cta-box {
      margin: 3rem 0;
      padding: 2rem;
      background: var(--bg-light);
      border-radius: 8px;
      text-align: center;
    }
    .cta-button {
      display: inline-block;
      background: var(--accent-color);
      color: white !important;
      padding: 0.75rem 1.5rem;
      border-radius: 6px;
      text-decoration: none;
      font-weight: 600;
      font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    @media print {
      .controls { display: none; }
      body { max-width: none; padding: 0; }
    }
  </style>
</head>
<body>
  <div class="controls" id="controls">
    <button onclick="toggleView()">View</button>
    <button onclick="window.print()">Print</button>
    <button onclick="generatePDF()">PDF</button>
    <button onclick="openEditor()">Edit</button>
    <span class="word-count" id="word-count">0 words · 0 min read</span>
  </div>

  <article data-content-type="blog-post">
    <header>
      <h1 data-line="1">{{title}}</h1>
      <div class="meta">
        <span>By {{author}}</span>
        <time datetime="{{iso_date}}">{{formatted_date}}</time>
        <span>{{read_time}} min read</span>
      </div>
      <p class="lead" data-line="5">{{lead}}</p>
    </header>

    <div class="content" id="content" data-line="10">
      <!-- Content sections here -->
    </div>

    <footer>
      <div class="tags">
        <!-- Tags here -->
      </div>
      
      <div class="author-box">
        <div class="author-avatar"></div>
        <div class="author-bio">
          <div class="author-name">{{author}}</div>
          <div class="author-desc">{{author_bio}}</div>
        </div>
      </div>
    </footer>
  </article>

  <script>
    // Word count and read time
    function updateStats() {
      const content = document.getElementById('content').textContent;
      const words = content.trim().split(/\s+/).length;
      const readTime = Math.ceil(words / 200);
      document.getElementById('word-count').textContent = 
        `${words} words · ${readTime} min read`;
    }
    updateStats();

    // View toggle
    function toggleView() {
      const content = document.getElementById('content');
      if (content.dataset.mode === 'source') {
        content.innerHTML = content.dataset.html;
        content.dataset.mode = 'rendered';
      } else {
        content.dataset.html = content.innerHTML;
        content.innerHTML = '<pre style="white-space:pre-wrap">' + 
          content.innerHTML.replace(/</g,'&lt;') + '</pre>';
        content.dataset.mode = 'source';
      }
    }

    // PDF generation
    function generatePDF() {
      document.getElementById('controls').style.display = 'none';
      window.print();
      document.getElementById('controls').style.display = 'flex';
    }

    // Editor integration
    let lastLine = 1;
    document.addEventListener('click', (e) => {
      const el = e.target.closest('[data-line]');
      if (el) lastLine = parseInt(el.dataset.line);
    });
    
    function openEditor() {
      // Adjust based on available editor
      const file = window.location.pathname;
      window.location.href = `vscode://file${file}:${lastLine}`;
    }
  </script>
</body>
</html>
```

---

## Content Patterns

### Opening Patterns

| Type | Structure | Best For |
|------|-----------|----------|
| **Story Hook** | Anecdote → Lesson → Promise | Personal/experiential content |
| **Problem-Agitate-Solve** | Problem → Consequences → Your solution | How-to/educational |
| **Contrarian** | Common belief → Why it's wrong → Better way | Thought leadership |
| **Data Lead** | Surprising stat → Context → Implications | Research-based |
| **Question** | Provocative question → Why it matters → Preview | Curiosity-driven |

### Story Hook Example

```html
<p data-line="10">
  Last Tuesday, I deleted 3,000 lines of code I'd spent two weeks writing.
</p>
<p data-line="12">
  It felt terrible. And it was exactly the right thing to do.
</p>
<p data-line="14">
  Here's what I learned about knowing when to cut your losses—and why 
  the sunk cost fallacy is your worst enemy in creative work.
</p>
```

### Problem-Agitate-Solve Example

```html
<p data-line="10">
  Most productivity advice doesn't work. You've tried the systems, 
  bought the apps, and read the books. Yet you still end each day 
  feeling like you didn't accomplish what matters.
</p>
<p data-line="14">
  The problem isn't your willpower or your tools. It's that 
  traditional productivity advice was designed for factories, 
  not knowledge work.
</p>
<p data-line="18">
  In this post, I'll share the framework that helped me double my 
  meaningful output while working fewer hours.
</p>
```

---

## Section Templates

### Regular Section

```html
<h2 data-line="{{line}}">{{section_title}}</h2>
<p data-line="{{line}}">{{opening}}</p>
<p data-line="{{line}}">{{main_point}}</p>
<p data-line="{{line}}">{{supporting_detail}}</p>
```

### Section with Example

```html
<h2 data-line="{{line}}">{{section_title}}</h2>
<p data-line="{{line}}">{{context}}</p>

<h3 data-line="{{line}}">Example: {{example_title}}</h3>
<p data-line="{{line}}">{{example_narrative}}</p>

<p data-line="{{line}}">{{takeaway}}</p>
```

### Section with List

```html
<h2 data-line="{{line}}">{{section_title}}</h2>
<p data-line="{{line}}">{{intro}}</p>

<ol data-line="{{line}}">
  <li><strong>{{item_1_title}}:</strong> {{item_1_desc}}</li>
  <li><strong>{{item_2_title}}:</strong> {{item_2_desc}}</li>
  <li><strong>{{item_3_title}}:</strong> {{item_3_desc}}</li>
</ol>

<p data-line="{{line}}">{{synthesis}}</p>
```

### Pullquote

```html
<div class="pullquote" data-line="{{line}}">
  "{{memorable_quote}}"
</div>
```

---

## SEO Best Practices

### Title Optimization

| Element | Guideline |
|---------|-----------|
| Length | 50-60 characters |
| Keyword | Include primary keyword |
| Power words | Use emotional triggers |
| Format | Consider number or "How to" |

### Meta Description

```html
<meta name="description" content="{{meta_description}}">
<!-- 150-160 characters, include keyword, compelling call to action -->
```

### Heading Hierarchy

```
H1: Article title (once, at top)
  H2: Major sections (3-6 per article)
    H3: Subsections (as needed)
      H4: Rarely needed
```

### Internal/External Links

| Type | Guideline |
|------|-----------|
| Internal links | 2-5 per 1000 words |
| External links | 1-3 authoritative sources |
| Anchor text | Descriptive, not "click here" |

---

## Blog Post Lengths

| Type | Word Count | Use Case |
|------|------------|----------|
| Quick tip | 300-500 | Single focused insight |
| Standard | 1000-1500 | Most topics |
| In-depth | 2000-3000 | Comprehensive guides |
| Ultimate guide | 3000+ | Pillar content |

### Reading Time Formula

```
Read time = Word count / 200 words per minute
```

---

## Multi-Part Series

For longer content, split into linked articles:

```
series/
├── index.html           # Series overview
├── part-1-intro.html
├── part-2-deep-dive.html
├── part-3-application.html
└── metadata.json
```

### Series Navigation Component

```html
<nav class="series-nav">
  <h4>This Post is Part of a Series</h4>
  <ol>
    <li><a href="part-1.html">Part 1: Introduction</a></li>
    <li class="current">Part 2: Deep Dive (You are here)</li>
    <li><a href="part-3.html">Part 3: Application</a></li>
  </ol>
</nav>
```

---

## CTA Patterns

### Mid-Article CTA

```html
<div class="cta-box" data-line="{{line}}">
  <p><strong>Want more insights like this?</strong></p>
  <p>{{cta_description}}</p>
  <a href="{{cta_url}}" class="cta-button">{{cta_text}}</a>
</div>
```

### End-of-Article CTA Types

| Goal | CTA Example |
|------|-------------|
| Newsletter | "Get weekly insights delivered" |
| Comment | "What's your experience with X?" |
| Share | "Know someone who'd find this useful?" |
| Related | "Continue reading: [Related Article]" |
| Product | "See how [Product] can help" |

---

## Export Options

### Markdown

```bash
python scripts/bundle_content.py post.html --format markdown
```

For platforms that prefer Markdown (Dev.to, Medium import, etc.).

### RSS Feed Item

```bash
python scripts/bundle_content.py post.html --format rss
```

Generates `<item>` element for RSS feed.

### JSON (API)

```bash
python scripts/bundle_content.py post.html --format json
```

Structured data for headless CMS or API consumption.

---

## Validation Checklist

### Content

- [ ] Title is compelling and under 60 chars
- [ ] Opening hook captures attention
- [ ] Each section has clear purpose
- [ ] Transitions between sections smooth
- [ ] Conclusion provides value/CTA
- [ ] No placeholder text remaining

### SEO

- [ ] Meta description set (150-160 chars)
- [ ] Primary keyword in title and H1
- [ ] Alt text on all images
- [ ] Internal links present
- [ ] External links to authoritative sources

### Technical

- [ ] HTML validates
- [ ] Images optimized (<200KB)
- [ ] Links all work
- [ ] Mobile display correct
- [ ] Read time calculated

---

*End of Blog Post Content Reference*
