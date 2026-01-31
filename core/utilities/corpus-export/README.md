# Corpus Export

**Purpose:** Multi-format corpus export utility

**Size:** 10.9 KB

---

## Quick Start

```javascript
// Export to PDF
await exportToPDF(artifactPath, 'output.pdf');

// Export to DOCX
await exportToDOCX(artifactPath, 'output.docx');

// Export entire corpus to JSON
await exportToJSON(corpusPath, 'corpus.json');

// Generate documentation package
await exportDocumentationPackage(corpusPath, './output');
```

## Supported Formats

- **PDF** - Styled documents with TOC
- **DOCX** - Editable Word documents
- **HTML** - Self-contained static pages
- **Markdown** - Plain text format
- **JSON** - Structured data export

## Export Presets

- **Documentation Package:** PDF + HTML + Markdown
- **Client Deliverable:** PDF + DOCX (branded)

## Features

- Combine multiple artifacts
- Custom styling/templates
- Inline assets (CSS, images)
- Table of contents generation
- Cover pages

---

**Part of:** v4.0.0 Universal Skills  
**Category:** Utilities  
**Integration:** CorpusHub API, Pandoc, Puppeteer
