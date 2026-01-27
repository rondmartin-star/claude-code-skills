# Journal Article Content Reference

**Output Types:** Peer-reviewed journal articles, academic papers, formal research  
**Load when:** User mentions journal article, peer-reviewed, academic paper, research publication, or formal citation requirements

---

## Academic Article Structure

### IMRaD Format (Standard)

Most scientific journals use Introduction, Methods, Results, and Discussion:

```
Article Structure:
├── Title
├── Abstract (150-300 words)
├── Keywords (5-8)
├── Introduction
│   └── Literature review → Research gap → Objectives
├── Methods
│   └── Design → Participants → Procedures → Analysis
├── Results
│   └── Findings organized by research questions
├── Discussion
│   └── Interpretation → Implications → Limitations → Future
├── Conclusion
├── References
└── Appendices (optional)
```

### Humanities/Social Sciences Format

```
Article Structure:
├── Title
├── Abstract
├── Introduction
├── Literature Review (separate section)
├── Theoretical Framework
├── Methodology
├── Analysis/Findings
├── Discussion
├── Conclusion
├── References
└── Appendices
```

---

## HTML Template for Journal Articles

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{article_title}}</title>
  
  <!-- Academic metadata -->
  <meta name="citation_title" content="{{article_title}}">
  <meta name="citation_author" content="{{author_1}}">
  <meta name="citation_author" content="{{author_2}}">
  <meta name="citation_publication_date" content="{{year}}/{{month}}/{{day}}">
  <meta name="citation_journal_title" content="{{journal_name}}">
  <meta name="citation_volume" content="{{volume}}">
  <meta name="citation_issue" content="{{issue}}">
  <meta name="citation_firstpage" content="{{first_page}}">
  <meta name="citation_lastpage" content="{{last_page}}">
  <meta name="citation_doi" content="{{doi}}">
  
  <style>
    :root {
      --text-color: #1a1a1a;
      --text-light: #555;
      --accent-color: #2563eb;
      --bg-color: #ffffff;
      --border-color: #ddd;
    }
    
    @page {
      size: letter;
      margin: 1in;
    }
    
    body {
      font-family: 'Times New Roman', Times, serif;
      font-size: 12pt;
      line-height: 2;
      color: var(--text-color);
      max-width: 8.5in;
      margin: 0 auto;
      padding: 1in;
      background: var(--bg-color);
    }
    
    .controls {
      font-family: -apple-system, BlinkMacSystemFont, sans-serif;
      background: #f5f5f5;
      padding: 0.75rem 1rem;
      border-radius: 8px;
      margin-bottom: 2rem;
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
      align-items: center;
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
    .controls select {
      padding: 0.4rem;
      border: 1px solid var(--border-color);
      border-radius: 4px;
    }
    .controls .word-count {
      margin-left: auto;
      color: var(--text-light);
      font-size: 0.85rem;
    }
    
    .article-header {
      text-align: center;
      margin-bottom: 2rem;
    }
    
    h1.article-title {
      font-size: 16pt;
      font-weight: bold;
      margin-bottom: 1rem;
      line-height: 1.3;
    }
    
    .authors {
      font-size: 12pt;
      margin-bottom: 0.5rem;
    }
    .author-name {
      font-weight: normal;
    }
    .author-affiliation {
      font-size: 10pt;
      color: var(--text-light);
    }
    
    .correspondence {
      font-size: 10pt;
      color: var(--text-light);
      margin-top: 1rem;
    }
    
    .abstract {
      margin: 2rem 0;
      padding: 1rem;
      background: #f9f9f9;
      border-left: 3px solid var(--accent-color);
    }
    .abstract h2 {
      font-size: 12pt;
      font-weight: bold;
      margin-bottom: 0.5rem;
    }
    .abstract p {
      margin: 0;
      text-align: justify;
    }
    
    .keywords {
      font-size: 11pt;
      margin-top: 1rem;
    }
    .keywords strong {
      font-weight: bold;
    }
    
    h2 {
      font-size: 14pt;
      font-weight: bold;
      margin-top: 2rem;
      margin-bottom: 1rem;
      text-transform: uppercase;
    }
    
    h3 {
      font-size: 12pt;
      font-weight: bold;
      font-style: italic;
      margin-top: 1.5rem;
      margin-bottom: 0.5rem;
    }
    
    h4 {
      font-size: 12pt;
      font-style: italic;
      margin-top: 1rem;
      margin-bottom: 0.5rem;
    }
    
    p {
      text-align: justify;
      text-indent: 0.5in;
      margin: 0 0 1rem 0;
    }
    
    p.no-indent {
      text-indent: 0;
    }
    
    .citation {
      color: var(--accent-color);
      cursor: pointer;
    }
    .citation:hover {
      text-decoration: underline;
    }
    
    blockquote {
      margin: 1rem 0 1rem 0.5in;
      padding-left: 0.5in;
      font-size: 11pt;
      line-height: 1.8;
    }
    
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 1rem 0;
      font-size: 11pt;
    }
    
    table caption {
      font-weight: bold;
      text-align: left;
      margin-bottom: 0.5rem;
    }
    
    th, td {
      padding: 0.5rem;
      text-align: left;
      border-bottom: 1px solid var(--border-color);
    }
    
    th {
      border-top: 2px solid var(--text-color);
      border-bottom: 1px solid var(--text-color);
      font-weight: bold;
    }
    
    tbody tr:last-child td {
      border-bottom: 2px solid var(--text-color);
    }
    
    .table-note {
      font-size: 10pt;
      color: var(--text-light);
      margin-top: 0.5rem;
    }
    
    figure {
      margin: 1.5rem 0;
      text-align: center;
    }
    
    figure img {
      max-width: 100%;
    }
    
    figcaption {
      font-size: 11pt;
      text-align: left;
      margin-top: 0.5rem;
    }
    figcaption strong {
      font-weight: bold;
    }
    
    .references {
      margin-top: 2rem;
    }
    
    .references h2 {
      margin-bottom: 1rem;
    }
    
    .reference-list {
      font-size: 11pt;
      line-height: 1.6;
    }
    
    .reference-item {
      margin-bottom: 1rem;
      padding-left: 0.5in;
      text-indent: -0.5in;
    }
    
    .appendix {
      margin-top: 2rem;
      page-break-before: always;
    }
    
    @media print {
      .controls { display: none; }
      body { padding: 0; max-width: none; }
      .abstract { break-inside: avoid; }
      table { break-inside: avoid; }
      figure { break-inside: avoid; }
    }
  </style>
</head>
<body>
  <div class="controls" id="controls">
    <button onclick="window.print()">Print</button>
    <button onclick="generatePDF()">PDF</button>
    <button onclick="exportDOCX()">Export DOCX</button>
    <button onclick="toggleSource()">View Source</button>
    <select id="citation-style" onchange="reformatCitations()">
      <option value="apa7">APA 7th</option>
      <option value="mla9">MLA 9th</option>
      <option value="chicago">Chicago</option>
      <option value="harvard">Harvard</option>
      <option value="ieee">IEEE</option>
      <option value="vancouver">Vancouver</option>
    </select>
    <span class="word-count" id="word-count">0 words</span>
  </div>

  <article class="journal-article" data-content-type="journal-article">
    <header class="article-header">
      <h1 class="article-title" data-line="1">{{title}}</h1>
      
      <div class="authors">
        <span class="author-name">{{author_1_name}}<sup>1</sup></span>,
        <span class="author-name">{{author_2_name}}<sup>2</sup></span>
      </div>
      
      <div class="affiliations">
        <p class="author-affiliation"><sup>1</sup>{{affiliation_1}}</p>
        <p class="author-affiliation"><sup>2</sup>{{affiliation_2}}</p>
      </div>
      
      <p class="correspondence">
        Corresponding author: {{corresponding_email}}
      </p>
    </header>

    <section class="abstract" data-line="15">
      <h2>Abstract</h2>
      <p>{{abstract_text}}</p>
      <p class="keywords"><strong>Keywords:</strong> {{keywords}}</p>
    </section>

    <main id="article-body">
      <section data-line="25">
        <h2>Introduction</h2>
        <!-- Introduction content -->
      </section>

      <section data-line="50">
        <h2>Methods</h2>
        <!-- Methods content -->
      </section>

      <section data-line="100">
        <h2>Results</h2>
        <!-- Results content -->
      </section>

      <section data-line="150">
        <h2>Discussion</h2>
        <!-- Discussion content -->
      </section>

      <section data-line="200">
        <h2>Conclusion</h2>
        <!-- Conclusion content -->
      </section>
    </main>

    <section class="references" data-line="220">
      <h2>References</h2>
      <div class="reference-list" id="reference-list">
        <!-- References formatted by selected style -->
      </div>
    </section>
  </article>

  <script>
    // Word count
    function updateWordCount() {
      const body = document.getElementById('article-body').textContent;
      const words = body.trim().split(/\s+/).length;
      document.getElementById('word-count').textContent = `${words} words`;
    }
    updateWordCount();

    // Citation formatting
    const references = [
      // Reference data stored here
    ];

    function reformatCitations() {
      const style = document.getElementById('citation-style').value;
      // Reformat references based on selected style
      console.log('Reformatting to:', style);
    }

    // Export functions
    function generatePDF() {
      document.getElementById('controls').style.display = 'none';
      window.print();
      document.getElementById('controls').style.display = 'flex';
    }

    function exportDOCX() {
      alert('DOCX export initiated. Use scripts/convert_to_docx.py');
    }

    function toggleSource() {
      const article = document.querySelector('.journal-article');
      if (article.dataset.mode === 'source') {
        location.reload();
      } else {
        article.dataset.mode = 'source';
        article.innerHTML = '<pre style="white-space:pre-wrap;font-family:monospace">' + 
          article.innerHTML.replace(/</g,'&lt;') + '</pre>';
      }
    }

    // Track cursor for editor integration
    let lastLine = 1;
    document.addEventListener('click', (e) => {
      const el = e.target.closest('[data-line]');
      if (el) lastLine = parseInt(el.dataset.line);
    });
  </script>
</body>
</html>
```

---

## Citation Formats

### APA 7th Edition

**Journal Article:**
```
Author, A. A., & Author, B. B. (Year). Title of article. Title of Periodical, 
    volume(issue), page–page. https://doi.org/xxxxx
```

**Book:**
```
Author, A. A. (Year). Title of work: Capital letter also for subtitle. Publisher.
```

**In-text:**
- (Author, Year)
- Author (Year)
- (Author, Year, p. X)

### MLA 9th Edition

**Journal Article:**
```
Author Last, First. "Title of Article." Title of Journal, vol. #, no. #, Year, 
    pp. #-#.
```

**In-text:**
- (Author Page)
- Author (Page)

### Chicago (Author-Date)

**Journal Article:**
```
Author Last, First. Year. "Article Title." Journal Title volume (issue): pages. 
    https://doi.org/xxxxx.
```

### IEEE

**Journal Article:**
```
[#] A. Author and B. Author, "Title of article," Abbrev. Title of Journal, 
    vol. #, no. #, pp. ###–###, Month Year.
```

### Vancouver

**Journal Article:**
```
Author AA, Author BB. Title of article. Abbreviated Journal Title. Year;Volume
    (Issue):Pages.
```

---

## Section Templates

### Introduction

```html
<section data-line="{{line}}">
  <h2>Introduction</h2>
  
  <!-- Opening: Establish topic importance -->
  <p data-line="{{line}}">
    {{opening_context}}
  </p>
  
  <!-- Literature review: What's known -->
  <p data-line="{{line}}">
    {{literature_summary}}
    <span class="citation" data-ref="author2020">(Author, 2020)</span>
  </p>
  
  <!-- Gap: What's missing -->
  <p data-line="{{line}}">
    {{research_gap}}
  </p>
  
  <!-- Purpose: What this study does -->
  <p data-line="{{line}}">
    {{study_purpose}}
  </p>
  
  <!-- Preview: How article is organized (optional) -->
  <p data-line="{{line}}">
    {{article_overview}}
  </p>
</section>
```

### Methods

```html
<section data-line="{{line}}">
  <h2>Methods</h2>
  
  <h3>Participants</h3>
  <p data-line="{{line}}">
    {{participant_description}}
  </p>
  
  <h3>Materials</h3>
  <p data-line="{{line}}">
    {{materials_description}}
  </p>
  
  <h3>Procedure</h3>
  <p data-line="{{line}}">
    {{procedure_description}}
  </p>
  
  <h3>Data Analysis</h3>
  <p data-line="{{line}}">
    {{analysis_description}}
  </p>
</section>
```

### Results

```html
<section data-line="{{line}}">
  <h2>Results</h2>
  
  <!-- Descriptive statistics -->
  <p class="no-indent" data-line="{{line}}">
    {{descriptive_overview}}
  </p>
  
  <!-- Table -->
  <table>
    <caption>Table 1. {{table_title}}</caption>
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
  <p class="table-note">Note. {{table_notes}}</p>
  
  <!-- Main findings -->
  <h3>{{finding_1_heading}}</h3>
  <p data-line="{{line}}">
    {{finding_1_description}}
  </p>
  
  <!-- Figure -->
  <figure>
    <img src="{{figure_path}}" alt="{{figure_alt}}">
    <figcaption><strong>Figure 1.</strong> {{figure_caption}}</figcaption>
  </figure>
</section>
```

### Discussion

```html
<section data-line="{{line}}">
  <h2>Discussion</h2>
  
  <!-- Summary of findings -->
  <p data-line="{{line}}">
    {{findings_summary}}
  </p>
  
  <!-- Interpretation -->
  <p data-line="{{line}}">
    {{interpretation}}
  </p>
  
  <!-- Relation to literature -->
  <p data-line="{{line}}">
    {{literature_connection}}
  </p>
  
  <!-- Implications -->
  <h3>Implications</h3>
  <p data-line="{{line}}">
    {{theoretical_implications}}
  </p>
  <p data-line="{{line}}">
    {{practical_implications}}
  </p>
  
  <!-- Limitations -->
  <h3>Limitations</h3>
  <p data-line="{{line}}">
    {{limitations}}
  </p>
  
  <!-- Future research -->
  <h3>Future Directions</h3>
  <p data-line="{{line}}">
    {{future_research}}
  </p>
</section>
```

---

## Multi-File Structure for Complex Articles

```
journal-article/
├── index.html              # Full article
├── sections/
│   ├── abstract.html
│   ├── introduction.html
│   ├── methods.html
│   ├── results.html
│   ├── discussion.html
│   └── references.html
├── figures/
│   ├── figure-1.png
│   └── figure-2.png
├── tables/
│   ├── table-1.html
│   └── table-2.html
├── supplementary/
│   ├── appendix-a.html
│   └── data.csv
├── data/
│   └── references.json
└── metadata.json
```

---

## Export to DOCX

Journal submissions typically require Word format:

```bash
python scripts/convert_to_docx.py article.html \
  --template journal-template.docx \
  --output submission.docx
```

### DOCX Template Features

- Double-spaced text
- 1-inch margins
- Times New Roman 12pt
- Page numbers
- Running head
- Line numbers (optional)

---

## Common Journal Requirements

| Element | Typical Requirement |
|---------|---------------------|
| Word count | 3,000-10,000 (varies by journal) |
| Abstract | 150-300 words |
| Keywords | 5-8 |
| References | Varies (20-60 typical) |
| Figures/Tables | Often max 6-8 combined |
| Margins | 1 inch all sides |
| Font | Times New Roman 12pt |
| Spacing | Double |
| File format | .docx (usually) |

---

## Validation Checklist

### Structure

- [ ] Title is clear and specific
- [ ] Abstract includes purpose, methods, results, conclusions
- [ ] Keywords are appropriate for indexing
- [ ] All sections present and properly ordered
- [ ] Headings follow hierarchy

### Content

- [ ] Literature review is current and relevant
- [ ] Methods described in sufficient detail for replication
- [ ] Results organized logically
- [ ] Discussion interprets findings (not repeats them)
- [ ] Limitations acknowledged
- [ ] Conclusion doesn't overstate findings

### Citations

- [ ] All claims supported by citations
- [ ] Citation style consistent throughout
- [ ] All cited works appear in references
- [ ] All references are cited in text
- [ ] DOIs included where available

### Technical

- [ ] Word count within limits
- [ ] Figures/tables labeled correctly
- [ ] Tables formatted properly
- [ ] Images high resolution (300+ DPI)
- [ ] No placeholder text remaining

### Formatting

- [ ] Double-spaced
- [ ] Proper margins
- [ ] Page numbers
- [ ] Running head (if required)
- [ ] Clean export to DOCX

---

## Export Options

```bash
# HTML to DOCX for submission
python scripts/convert_to_docx.py article.html --output submission.docx

# Generate PDF for sharing
python scripts/convert_to_pdf.py article.html --output article.pdf

# Extract references as BibTeX
python scripts/bundle_content.py article.html --format bibtex
```

---

*End of Journal Article Content Reference*
