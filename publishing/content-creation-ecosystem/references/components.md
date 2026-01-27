# Shared Components Reference

**Purpose:** Reusable HTML components across all content types  
**Load when:** Building any content that needs standard UI elements

---

## Interactive Controls Component

Required on ALL content types:

```html
<div class="controls" id="content-controls">
  <button onclick="toggleView()">View</button>
  <button onclick="window.print()">Print</button>
  <button onclick="generatePDF()">PDF</button>
  <button onclick="openEditor()">Edit</button>
  <span class="word-count" id="word-count">0 words</span>
</div>

<style>
  .controls {
    background: #f5f5f5;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 100;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
  }
  .controls button {
    padding: 0.4rem 0.8rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    background: white;
    cursor: pointer;
    font-size: 0.85rem;
    transition: background 0.15s;
  }
  .controls button:hover {
    background: #e5e5e5;
  }
  .controls .word-count {
    margin-left: auto;
    color: #666;
    font-size: 0.85rem;
  }
  @media print {
    .controls { display: none; }
  }
</style>

<script>
  // Word count
  function updateWordCount() {
    const content = document.querySelector('[data-content-type]');
    if (!content) return;
    const text = content.textContent || '';
    const words = text.trim().split(/\s+/).filter(w => w.length > 0).length;
    const el = document.getElementById('word-count');
    if (el) el.textContent = `${words} words`;
  }

  // View toggle (rendered ↔ source)
  function toggleView() {
    const content = document.querySelector('[data-content-type]');
    if (!content) return;
    
    if (content.dataset.viewMode === 'source') {
      content.innerHTML = content.dataset.rendered;
      content.dataset.viewMode = 'rendered';
    } else {
      content.dataset.rendered = content.innerHTML;
      content.innerHTML = '<pre style="white-space:pre-wrap;font-family:monospace;font-size:12px">' + 
        content.innerHTML.replace(/</g, '&lt;').replace(/>/g, '&gt;') + '</pre>';
      content.dataset.viewMode = 'source';
    }
  }

  // PDF generation via print
  function generatePDF() {
    const controls = document.getElementById('content-controls');
    if (controls) controls.style.display = 'none';
    window.print();
    if (controls) controls.style.display = 'flex';
  }

  // Editor integration with cursor position
  let lastEditLine = 1;
  
  document.addEventListener('click', (e) => {
    const el = e.target.closest('[data-line]');
    if (el) {
      lastEditLine = parseInt(el.dataset.line) || 1;
    }
  });

  function openEditor() {
    const file = window.location.pathname;
    // VS Code URL scheme
    window.location.href = `vscode://file${file}:${lastEditLine}`;
  }

  // Initialize
  document.addEventListener('DOMContentLoaded', updateWordCount);
</script>
```

---

## Typography Components

### Heading Hierarchy

```html
<style>
  h1 { font-size: 2.5rem; line-height: 1.15; margin-bottom: 1rem; }
  h2 { font-size: 1.75rem; line-height: 1.2; margin-top: 2.5rem; margin-bottom: 1rem; }
  h3 { font-size: 1.35rem; line-height: 1.25; margin-top: 2rem; margin-bottom: 0.75rem; }
  h4 { font-size: 1.1rem; line-height: 1.3; margin-top: 1.5rem; margin-bottom: 0.5rem; }
</style>
```

### Lead Paragraph

```html
<p class="lead" data-line="{{line}}">{{intro_text}}</p>

<style>
  .lead {
    font-size: 1.25rem;
    color: #555;
    line-height: 1.6;
    margin-bottom: 2rem;
  }
</style>
```

### Pullquote

```html
<div class="pullquote" data-line="{{line}}">
  "{{quote_text}}"
</div>

<style>
  .pullquote {
    font-size: 1.5rem;
    font-style: italic;
    text-align: center;
    padding: 2rem;
    margin: 2rem 0;
    border-top: 1px solid #ddd;
    border-bottom: 1px solid #ddd;
    color: #333;
  }
</style>
```

### Blockquote

```html
<blockquote data-line="{{line}}">
  <p>{{quote_text}}</p>
  <cite>— {{attribution}}</cite>
</blockquote>

<style>
  blockquote {
    border-left: 4px solid var(--accent-color, #2563eb);
    margin: 2rem 0;
    padding: 0.5rem 0 0.5rem 1.5rem;
    font-style: italic;
    color: #555;
  }
  blockquote cite {
    display: block;
    margin-top: 0.5rem;
    font-size: 0.9rem;
    font-style: normal;
    color: #777;
  }
</style>
```

---

## Card Components

### Basic Card

```html
<div class="card" data-line="{{line}}">
  <h3 class="card-title">{{title}}</h3>
  <p class="card-description">{{description}}</p>
</div>

<style>
  .card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: box-shadow 0.2s;
  }
  .card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  }
  .card-title {
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
  }
  .card-description {
    color: #6b7280;
    font-size: 0.95rem;
  }
</style>
```

### Feature Card

```html
<div class="feature-card" data-line="{{line}}">
  <div class="feature-icon">{{icon}}</div>
  <h3>{{title}}</h3>
  <p>{{description}}</p>
</div>

<style>
  .feature-card {
    text-align: center;
    padding: 2rem 1.5rem;
    background: #f9fafb;
    border-radius: 12px;
  }
  .feature-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
  }
  .feature-card h3 {
    margin-bottom: 0.75rem;
  }
</style>
```

### Link Card (for resource libraries)

```html
<a href="{{url}}" class="link-card" data-line="{{line}}">
  <span class="link-card-type">{{type}}</span>
  <h3>{{title}}</h3>
  <p>{{description}}</p>
  <span class="link-card-meta">{{source}} · {{date}}</span>
</a>

<style>
  .link-card {
    display: block;
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 1.5rem;
    text-decoration: none;
    color: inherit;
    transition: all 0.2s;
  }
  .link-card:hover {
    border-color: var(--accent-color, #2563eb);
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  }
  .link-card-type {
    display: inline-block;
    padding: 0.2rem 0.5rem;
    background: #dbeafe;
    color: #1d4ed8;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
  }
  .link-card h3 {
    margin-bottom: 0.5rem;
  }
  .link-card p {
    color: #6b7280;
    font-size: 0.9rem;
    margin-bottom: 0.75rem;
  }
  .link-card-meta {
    font-size: 0.8rem;
    color: #9ca3af;
  }
</style>
```

---

## CTA Components

### CTA Box

```html
<div class="cta-box" data-line="{{line}}">
  <h3>{{headline}}</h3>
  <p>{{description}}</p>
  <a href="{{url}}" class="cta-button">{{button_text}}</a>
</div>

<style>
  .cta-box {
    background: #f9fafb;
    padding: 2rem;
    border-radius: 12px;
    text-align: center;
    margin: 2rem 0;
  }
  .cta-box h3 {
    margin-bottom: 0.5rem;
  }
  .cta-box p {
    color: #6b7280;
    margin-bottom: 1.5rem;
  }
  .cta-button {
    display: inline-block;
    background: var(--accent-color, #2563eb);
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: 6px;
    text-decoration: none;
    font-weight: 600;
    transition: background 0.2s;
  }
  .cta-button:hover {
    background: #1d4ed8;
  }
</style>
```

### Inline CTA

```html
<p class="inline-cta" data-line="{{line}}">
  {{text}} <a href="{{url}}">{{link_text}} →</a>
</p>

<style>
  .inline-cta {
    padding: 1rem 1.5rem;
    background: #fffbeb;
    border-left: 4px solid #f59e0b;
    border-radius: 0 8px 8px 0;
  }
  .inline-cta a {
    font-weight: 600;
    color: #d97706;
  }
</style>
```

---

## Navigation Components

### Breadcrumb

```html
<nav class="breadcrumb" aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/blog/">Blog</a></li>
    <li aria-current="page">{{current_page}}</li>
  </ol>
</nav>

<style>
  .breadcrumb ol {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    list-style: none;
    padding: 0;
    font-size: 0.9rem;
  }
  .breadcrumb li:not(:last-child)::after {
    content: '/';
    margin-left: 0.5rem;
    color: #9ca3af;
  }
  .breadcrumb a {
    color: #6b7280;
    text-decoration: none;
  }
  .breadcrumb a:hover {
    color: var(--accent-color, #2563eb);
  }
  .breadcrumb [aria-current] {
    color: #1f2937;
    font-weight: 500;
  }
</style>
```

### Pagination

```html
<nav class="pagination" aria-label="Pagination">
  <a href="?page={{prev}}" class="pagination-prev">← Previous</a>
  <span class="pagination-info">Page {{current}} of {{total}}</span>
  <a href="?page={{next}}" class="pagination-next">Next →</a>
</nav>

<style>
  .pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    margin: 2rem 0;
  }
  .pagination a {
    padding: 0.5rem 1rem;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    text-decoration: none;
    color: #374151;
  }
  .pagination a:hover {
    background: #f3f4f6;
  }
  .pagination-info {
    color: #6b7280;
  }
</style>
```

---

## Form Components

### Input Field

```html
<div class="form-group">
  <label for="{{id}}">{{label}}</label>
  <input type="{{type}}" id="{{id}}" name="{{name}}" 
         placeholder="{{placeholder}}" {{required}}>
</div>

<style>
  .form-group {
    margin-bottom: 1rem;
  }
  .form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
  }
  .form-group input,
  .form-group textarea,
  .form-group select {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 1rem;
  }
  .form-group input:focus,
  .form-group textarea:focus {
    outline: none;
    border-color: var(--accent-color, #2563eb);
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
  }
</style>
```

---

## Table Components

### Basic Table

```html
<table class="data-table" data-line="{{line}}">
  <caption>{{caption}}</caption>
  <thead>
    <tr>
      <th>{{col1}}</th>
      <th>{{col2}}</th>
      <th>{{col3}}</th>
    </tr>
  </thead>
  <tbody>
    <!-- Data rows -->
  </tbody>
</table>

<style>
  .data-table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.5rem 0;
  }
  .data-table caption {
    text-align: left;
    font-weight: 600;
    margin-bottom: 0.5rem;
  }
  .data-table th,
  .data-table td {
    padding: 0.75rem 1rem;
    text-align: left;
    border-bottom: 1px solid #e5e7eb;
  }
  .data-table th {
    background: #f9fafb;
    font-weight: 600;
  }
  .data-table tbody tr:hover {
    background: #f9fafb;
  }
</style>
```

---

## Image Components

### Figure with Caption

```html
<figure data-line="{{line}}">
  <img src="{{src}}" alt="{{alt}}" loading="lazy">
  <figcaption>{{caption}}</figcaption>
</figure>

<style>
  figure {
    margin: 2rem 0;
  }
  figure img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
  }
  figcaption {
    margin-top: 0.75rem;
    font-size: 0.9rem;
    color: #6b7280;
    text-align: center;
    font-style: italic;
  }
</style>
```

---

## Utility Classes

```css
/* Spacing */
.mt-0 { margin-top: 0; }
.mt-1 { margin-top: 0.5rem; }
.mt-2 { margin-top: 1rem; }
.mt-4 { margin-top: 2rem; }
.mb-0 { margin-bottom: 0; }
.mb-1 { margin-bottom: 0.5rem; }
.mb-2 { margin-bottom: 1rem; }
.mb-4 { margin-bottom: 2rem; }

/* Text alignment */
.text-left { text-align: left; }
.text-center { text-align: center; }
.text-right { text-align: right; }

/* Display */
.hidden { display: none; }
.flex { display: flex; }
.grid { display: grid; }

/* Text styles */
.text-sm { font-size: 0.875rem; }
.text-lg { font-size: 1.125rem; }
.text-muted { color: #6b7280; }
.font-bold { font-weight: 700; }

/* Print utilities */
@media print {
  .no-print { display: none; }
  .print-only { display: block; }
}
```

---

*End of Shared Components Reference*
