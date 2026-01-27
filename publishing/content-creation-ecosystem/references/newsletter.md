# Newsletter Content Reference

**Platforms:** Substack, email newsletters, RSS  
**Load when:** User mentions Substack, newsletter, email content, or subscriber communication

---

## Substack Specifications

### Editor Compatibility

Substack accepts HTML but renders through their editor. Ensure compatibility:

| Supported | Not Supported |
|-----------|---------------|
| `<h1>` - `<h6>` headings | Custom CSS classes |
| `<p>` paragraphs | Inline styles (limited) |
| `<strong>`, `<em>` | Custom fonts |
| `<a>` links | JavaScript |
| `<ul>`, `<ol>` lists | Complex tables |
| `<blockquote>` | Iframes (except embeds) |
| `<img>` images | SVG (use PNG/JPG) |
| `<hr>` dividers | Custom colors |

### Content Structure

```
Newsletter Structure:
├── Subject line (hook)
├── Preview text (50-100 chars)
├── Greeting (optional)
├── Hook paragraph
├── Main content (2-5 sections)
├── Call-to-action
└── Sign-off + footer
```

---

## Newsletter Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{subject_line}}</title>
  <style>
    :root {
      --text-color: #1a1a1a;
      --accent-color: #ff6719;
      --bg-color: #ffffff;
      --light-gray: #f7f7f7;
      --border-color: #e5e5e5;
    }
    body {
      font-family: Georgia, 'Times New Roman', serif;
      line-height: 1.7;
      color: var(--text-color);
      max-width: 680px;
      margin: 0 auto;
      padding: 2rem 1rem;
      background: var(--bg-color);
    }
    .controls {
      background: var(--light-gray);
      padding: 1rem;
      border-radius: 8px;
      margin-bottom: 2rem;
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
      align-items: center;
    }
    .controls button {
      padding: 0.5rem 1rem;
      border: 1px solid var(--border-color);
      border-radius: 6px;
      background: white;
      cursor: pointer;
    }
    .controls button:hover {
      background: #f0f0f0;
    }
    .word-count {
      margin-left: auto;
      color: #666;
      font-size: 0.9rem;
    }
    h1 {
      font-size: 2rem;
      line-height: 1.2;
      margin-bottom: 0.5rem;
    }
    h2 {
      font-size: 1.5rem;
      margin-top: 2rem;
      border-bottom: 1px solid var(--border-color);
      padding-bottom: 0.5rem;
    }
    h3 {
      font-size: 1.25rem;
      margin-top: 1.5rem;
    }
    p {
      margin: 1.25rem 0;
    }
    blockquote {
      border-left: 3px solid var(--accent-color);
      margin: 1.5rem 0;
      padding-left: 1.5rem;
      font-style: italic;
      color: #555;
    }
    .pullquote {
      font-size: 1.4rem;
      font-style: italic;
      text-align: center;
      padding: 1.5rem;
      border-top: 1px solid var(--border-color);
      border-bottom: 1px solid var(--border-color);
      margin: 2rem 0;
    }
    a {
      color: var(--accent-color);
      text-decoration: underline;
    }
    img {
      max-width: 100%;
      height: auto;
      margin: 1.5rem 0;
    }
    .caption {
      font-size: 0.9rem;
      color: #666;
      text-align: center;
      margin-top: -1rem;
    }
    .cta-box {
      background: var(--light-gray);
      padding: 1.5rem;
      border-radius: 8px;
      margin: 2rem 0;
      text-align: center;
    }
    .cta-button {
      display: inline-block;
      background: var(--accent-color);
      color: white !important;
      padding: 0.75rem 1.5rem;
      border-radius: 6px;
      text-decoration: none;
      font-weight: bold;
    }
    .divider {
      text-align: center;
      margin: 2rem 0;
      color: #ccc;
    }
    .footnote {
      font-size: 0.9rem;
      color: #666;
      border-top: 1px solid var(--border-color);
      padding-top: 1rem;
      margin-top: 2rem;
    }
    .metadata {
      color: #666;
      font-size: 0.9rem;
      margin-bottom: 2rem;
    }
  </style>
</head>
<body>
  <div class="controls" id="content-controls">
    <button onclick="window.print()">Print</button>
    <button onclick="generatePDF()">PDF</button>
    <button onclick="copyHTML()">Copy HTML</button>
    <button onclick="toggleSource()">View Source</button>
    <span class="word-count" id="word-count">0 words</span>
  </div>

  <article class="newsletter" data-content-type="newsletter">
    <header>
      <h1 data-line="1">{{title}}</h1>
      <div class="metadata">
        <span>{{author}}</span> · <span>{{date}}</span> · <span>{{read_time}} min read</span>
      </div>
    </header>
    
    <main id="content">
      <!-- Newsletter content here -->
    </main>
    
    <footer class="footnote">
      <p>Thanks for reading! If you found this valuable, consider sharing with someone who'd appreciate it.</p>
    </footer>
  </article>

  <script>
    // Word count
    function updateWordCount() {
      const content = document.getElementById('content').textContent;
      const words = content.trim().split(/\s+/).length;
      document.getElementById('word-count').textContent = words + ' words';
    }
    updateWordCount();

    // Copy HTML
    function copyHTML() {
      const article = document.querySelector('.newsletter').innerHTML;
      navigator.clipboard.writeText(article);
      alert('HTML copied to clipboard!');
    }

    // Generate PDF via print
    function generatePDF() {
      document.querySelector('.controls').style.display = 'none';
      window.print();
      document.querySelector('.controls').style.display = 'flex';
    }

    // Toggle source view
    function toggleSource() {
      const article = document.querySelector('.newsletter');
      if (article.dataset.sourceMode === 'true') {
        article.innerHTML = article.dataset.rendered;
        article.dataset.sourceMode = 'false';
      } else {
        article.dataset.rendered = article.innerHTML;
        article.dataset.sourceMode = 'true';
        article.innerHTML = '<pre>' + article.innerHTML.replace(/</g, '&lt;').replace(/>/g, '&gt;') + '</pre>';
      }
    }

    // Cursor position tracking for edit button
    document.addEventListener('click', (e) => {
      const element = e.target.closest('[data-line]');
      if (element) {
        window.lastEditLine = element.dataset.line;
      }
    });
  </script>
</body>
</html>
```

---

## Content Section Templates

### Hook Paragraph

Opens with immediate value. Patterns:

| Type | Pattern | Example |
|------|---------|---------|
| Story | Personal anecdote | "Last week, I made a mistake that cost..." |
| Insight | Surprising observation | "The most productive people don't optimize time..." |
| Question | Curiosity gap | "What if everything you knew about X was wrong?" |
| Stat | Data-driven | "Only 3% of people actually do X..." |
| Prediction | Forward-looking | "In 5 years, Y will be completely different..." |

### Section Structure

```html
<h2 data-line="{{line}}">{{section_title}}</h2>
<p data-line="{{line}}">{{opening_context}}</p>
<p data-line="{{line}}">{{main_point}}</p>
<p data-line="{{line}}">{{supporting_detail}}</p>
```

### Pullquote

```html
<div class="pullquote" data-line="{{line}}">
  "{{memorable_quote}}"
</div>
```

### CTA Box

```html
<div class="cta-box" data-line="{{line}}">
  <p><strong>{{cta_headline}}</strong></p>
  <p>{{cta_description}}</p>
  <a href="{{cta_link}}" class="cta-button">{{cta_text}}</a>
</div>
```

### Divider

```html
<div class="divider">• • •</div>
```

---

## Newsletter Patterns

### Value-First Structure (Teaching)

```
1. Hook (why this matters now)
2. Problem (what's broken)
3. Insight (the key reframe)
4. Framework (actionable steps)
5. Example (proof it works)
6. CTA (what to do next)
```

### Story-Driven Structure

```
1. Scene (set the stage)
2. Conflict (tension point)
3. Turning point (insight moment)
4. Resolution (what changed)
5. Lesson (takeaway)
6. Application (how reader can use this)
```

### Curated Roundup Structure

```
1. Theme introduction
2. Item 1 + commentary
3. Item 2 + commentary
4. Item 3 + commentary
5. Synthesis (what connects them)
6. Your take
```

---

## Formatting Best Practices

### Paragraph Length

| Good | Avoid |
|------|-------|
| 2-4 sentences | Wall of text paragraphs |
| Mix of lengths | All same length |
| One idea per paragraph | Multiple ideas per paragraph |

### Visual Breaks

Every 3-4 paragraphs, include one of:
- Subheading
- Pullquote
- Image
- List
- Divider

### Lists

Use sparingly and purposefully:

```html
<ul>
  <li><strong>Bold lead-in:</strong> Explanation follows</li>
  <li><strong>Another point:</strong> With its explanation</li>
</ul>
```

---

## Subject Line Patterns

| Type | Pattern | Example |
|------|---------|---------|
| How-to | How to [achieve X] | "How to write faster without sacrificing quality" |
| Number | [N] ways to [benefit] | "5 ways to improve your morning routine" |
| Question | Why [surprising thing]? | "Why do smart people make dumb decisions?" |
| Contrast | [Common belief] vs [reality] | "What you think vs what actually works" |
| Curiosity | The [adjective] [topic] | "The counterintuitive truth about productivity" |

### Preview Text

50-100 characters that complement (don't repeat) the subject:

```
Subject: How to write faster
Preview: The surprising technique that changed everything
```

---

## Substack-Specific Features

### Embedded Content

```html
<!-- YouTube embed -->
<p>[Substack will convert YouTube URLs to embeds]</p>

<!-- Tweet embed -->
<p>[Substack will convert Twitter URLs to embeds]</p>
```

### Subscription CTA

```html
<div class="cta-box">
  <p><strong>Enjoying this?</strong></p>
  <p>Subscribe to get essays like this every week.</p>
  <a href="{{subscribe_url}}" class="cta-button">Subscribe</a>
</div>
```

### Paid Content Divider

```html
<hr>
<p><em>This post is for paid subscribers</em></p>
```

---

## Multi-File Newsletter Structure

For longer newsletters or series:

```
newsletter-issue-001/
├── index.html          # Main article
├── sections/
│   ├── intro.html
│   ├── section-1.html
│   ├── section-2.html
│   └── conclusion.html
├── assets/
│   └── images/
└── metadata.json
```

`metadata.json`:
```json
{
  "title": "Newsletter Title",
  "subject": "Email subject line",
  "preview": "Preview text",
  "author": "Author Name",
  "date": "2026-01-24",
  "issue": 1,
  "series": "Series Name"
}
```

---

## Validation Checklist

### Content Quality

- [ ] Hook captures attention in first paragraph
- [ ] Each section has clear purpose
- [ ] Transitions between sections smooth
- [ ] CTA is specific and actionable
- [ ] Length appropriate (typically 500-3000 words)

### Technical

- [ ] All HTML is Substack-compatible
- [ ] Images optimized (<500KB each)
- [ ] Links all functional
- [ ] No broken embeds
- [ ] Preview text set

### Before Sending

- [ ] Subject line tested (multiple options)
- [ ] Preview text complements subject
- [ ] Proofread for typos
- [ ] All placeholders replaced
- [ ] Mobile preview checked

---

## Export for Substack

### Direct HTML Copy

```bash
python scripts/bundle_content.py newsletter.html --format substack
```

Outputs clean HTML compatible with Substack's editor paste function.

### Markdown Alternative

```bash
python scripts/bundle_content.py newsletter.html --format markdown
```

For editors that prefer Markdown input.

---

*End of Newsletter Content Reference*
