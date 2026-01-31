---
name: corpus-export
description: >
  Export utility for corpus data to multiple formats (PDF, DOCX, HTML, Markdown, JSON).
  Supports single artifacts, collections, or entire corpus. Use when: generating
  documentation, creating deliverables, or sharing corpus content.
---

# Corpus Export

**Purpose:** Multi-format corpus export utility
**Type:** Utility Skill (Universal)

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Export to PDF"
- "Generate documentation"
- "Export corpus"
- "Create deliverables"

**Context Indicators:**
- Documentation generation needed
- Client deliverables
- Publishing content
- Archival purposes

---

## Export Formats

### 1. PDF Export

**Single Artifact:**
```javascript
async function exportToPDF(artifactPath, outputPath, options = {}) {
  const {
    includeTableOfContents = true,
    includeCoverPage = true,
    pageSize = 'A4',
    margins = { top: '1in', bottom: '1in', left: '1in', right: '1in' }
  } = options;

  // Read HTML content
  const html = fs.readFileSync(artifactPath, 'utf8');

  // Add styling for PDF
  const styledHTML = `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <style>
        body { font-family: 'Arial', sans-serif; line-height: 1.6; }
        h1 { page-break-before: always; color: #333; }
        h1:first-of-type { page-break-before: avoid; }
        code { background: #f4f4f4; padding: 2px 5px; }
        pre { background: #f4f4f4; padding: 10px; overflow-x: auto; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
      </style>
    </head>
    <body>${html}</body>
    </html>
  `;

  // Use Puppeteer for PDF generation
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setContent(styledHTML);

  await page.pdf({
    path: outputPath,
    format: pageSize,
    margin: margins,
    printBackground: true
  });

  await browser.close();

  return { outputPath, size: fs.statSync(outputPath).size };
}
```

**Multiple Artifacts (Combined):**
```javascript
async function exportMultipleToPDF(artifacts, outputPath, options = {}) {
  const combinedHTML = [];

  // Add cover page
  if (options.includeCoverPage) {
    combinedHTML.push(generateCoverPage(options.title || 'Corpus Export'));
  }

  // Add table of contents
  if (options.includeTableOfContents) {
    combinedHTML.push(generateTableOfContents(artifacts));
  }

  // Add each artifact
  for (const artifact of artifacts) {
    const html = fs.readFileSync(artifact.path, 'utf8');
    combinedHTML.push(`
      <div class="artifact" data-name="${artifact.name}">
        <h1>${artifact.title || artifact.name}</h1>
        ${html}
      </div>
    `);
  }

  return await exportToPDF(
    { content: combinedHTML.join('\n\n') },
    outputPath,
    options
  );
}
```

### 2. DOCX Export

**Using Pandoc:**
```javascript
async function exportToDOCX(artifactPath, outputPath, options = {}) {
  const {
    referenceDoc = null,  // Custom template
    includeMetadata = true
  } = options;

  // Convert HTML to Markdown first (Pandoc handles MD better)
  const html = fs.readFileSync(artifactPath, 'utf8');
  const markdown = htmlToMarkdown(html);

  // Write temporary markdown file
  const tempMD = `/tmp/export-${Date.now()}.md`;
  fs.writeFileSync(tempMD, markdown);

  // Build Pandoc command
  let cmd = `pandoc "${tempMD}" -o "${outputPath}"`;

  if (referenceDoc) {
    cmd += ` --reference-doc="${referenceDoc}"`;
  }

  if (includeMetadata) {
    cmd += ' --standalone';
  }

  await exec(cmd);

  // Cleanup
  fs.unlinkSync(tempMD);

  return { outputPath, size: fs.statSync(outputPath).size };
}
```

### 3. Markdown Export

**Convert from HTML:**
```javascript
function htmlToMarkdown(html) {
  const turndown = new TurndownService({
    headingStyle: 'atx',
    codeBlockStyle: 'fenced'
  });

  // Custom rules for better conversion
  turndown.addRule('tables', {
    filter: 'table',
    replacement: (content, node) => {
      // Convert HTML tables to Markdown tables
      return convertTableToMarkdown(node);
    }
  });

  return turndown.turndown(html);
}

async function exportToMarkdown(artifactPath, outputPath) {
  const html = fs.readFileSync(artifactPath, 'utf8');
  const markdown = htmlToMarkdown(html);

  fs.writeFileSync(outputPath, markdown);

  return { outputPath, size: fs.statSync(outputPath).size };
}
```

### 4. Static HTML Export

**Self-contained HTML:**
```javascript
async function exportToHTML(artifactPath, outputPath, options = {}) {
  const {
    inlineCSS = true,
    inlineImages = true,
    includeNavigation = true
  } = options;

  const html = fs.readFileSync(artifactPath, 'utf8');
  const $ = cheerio.load(html);

  // Inline CSS
  if (inlineCSS) {
    $('link[rel="stylesheet"]').each((i, link) => {
      const href = $(link).attr('href');
      const css = fs.readFileSync(path.resolve(path.dirname(artifactPath), href), 'utf8');
      $(link).replaceWith(`<style>${css}</style>`);
    });
  }

  // Inline images (base64)
  if (inlineImages) {
    $('img').each((i, img) => {
      const src = $(img).attr('src');
      if (!src.startsWith('data:') && !src.startsWith('http')) {
        const imagePath = path.resolve(path.dirname(artifactPath), src);
        if (fs.existsSync(imagePath)) {
          const imageData = fs.readFileSync(imagePath);
          const ext = path.extname(imagePath).slice(1);
          const base64 = imageData.toString('base64');
          $(img).attr('src', `data:image/${ext};base64,${base64}`);
        }
      }
    });
  }

  fs.writeFileSync(outputPath, $.html());

  return { outputPath, size: fs.statSync(outputPath).size };
}
```

### 5. JSON Export

**Structured Data:**
```javascript
async function exportToJSON(corpusPath, outputPath, options = {}) {
  const {
    includeContent = true,
    includeMetadata = true,
    includeTerms = true
  } = options;

  const config = JSON.parse(
    fs.readFileSync(path.join(corpusPath, 'corpus-config.json'), 'utf8')
  );

  const export_data = {
    name: config.name,
    version: config.version,
    exportDate: new Date().toISOString()
  };

  if (includeMetadata) {
    export_data.metadata = {
      voice: config.voice,
      roles: config.roles,
      framework: config.framework
    };
  }

  if (includeTerms) {
    export_data.terms = config.terms;
  }

  if (includeContent) {
    export_data.artifacts = {};

    for (const [name, artifact] of Object.entries(config.artifacts || {})) {
      const artifactPath = path.join(corpusPath, artifact.path);

      if (fs.statSync(artifactPath).isDirectory()) {
        // Directory of files
        const files = await glob(`${artifactPath}/**/*.{html,md}`);
        export_data.artifacts[name] = {};

        for (const file of files) {
          const relativePath = path.relative(artifactPath, file);
          export_data.artifacts[name][relativePath] = fs.readFileSync(file, 'utf8');
        }
      } else {
        // Single file
        export_data.artifacts[name] = fs.readFileSync(artifactPath, 'utf8');
      }
    }
  }

  fs.writeFileSync(outputPath, JSON.stringify(export_data, null, 2));

  return { outputPath, size: fs.statSync(outputPath).size };
}
```

---

## Export Presets

### Documentation Package

**Generate full documentation:**
```javascript
async function exportDocumentationPackage(corpusPath, outputDir) {
  const config = JSON.parse(
    fs.readFileSync(path.join(corpusPath, 'corpus-config.json'), 'utf8')
  );

  await fs.mkdir(outputDir, { recursive: true });

  const results = {
    pdf: null,
    html: null,
    markdown: null
  };

  // Combined PDF
  const artifacts = Object.entries(config.artifacts || {})
    .map(([name, artifact]) => ({
      name,
      path: path.join(corpusPath, artifact.path),
      title: artifact.title || name
    }));

  results.pdf = await exportMultipleToPDF(
    artifacts,
    path.join(outputDir, `${config.name}-documentation.pdf`),
    {
      title: `${config.name} Documentation`,
      includeCoverPage: true,
      includeTableOfContents: true
    }
  );

  // Static HTML site
  results.html = await exportToHTMLSite(
    corpusPath,
    path.join(outputDir, 'html')
  );

  // Markdown files
  results.markdown = await exportAllToMarkdown(
    corpusPath,
    path.join(outputDir, 'markdown')
  );

  return results;
}
```

### Client Deliverable

**Professional package:**
```javascript
async function exportClientDeliverable(corpusPath, outputDir, clientName) {
  const timestamp = new Date().toISOString().split('T')[0];
  const deliverableDir = path.join(outputDir, `${clientName}-${timestamp}`);

  await fs.mkdir(deliverableDir, { recursive: true });

  // PDF with custom branding
  await exportMultipleToPDF(
    getClientArtifacts(corpusPath),
    path.join(deliverableDir, 'Documentation.pdf'),
    {
      includeCoverPage: true,
      coverTemplate: 'templates/client-cover.html',
      watermark: clientName
    }
  );

  // DOCX for editing
  await exportToDOCX(
    path.join(corpusPath, 'requirements'),
    path.join(deliverableDir, 'Requirements.docx'),
    {
      referenceDoc: 'templates/corporate-template.docx'
    }
  );

  // ZIP the deliverable
  await zipDirectory(deliverableDir, `${deliverableDir}.zip`);

  return {
    path: `${deliverableDir}.zip`,
    contents: await fs.readdir(deliverableDir)
  };
}
```

---

## CorpusHub Integration

### API Endpoints

**Export Artifact:**
```
POST /api/artifacts/:id/export
Body: { format: "pdf", options: {} }
Response: { downloadUrl, expiresAt }
```

**Export Corpus:**
```
POST /api/corpora/:slug/export
Body: { format: "json", includeContent: true }
Response: { downloadUrl, size, expiresAt }
```

**Export Preset:**
```
POST /api/corpora/:slug/export/preset/:presetName
Response: { downloadUrl, files: [], expiresAt }
```

---

## Configuration

```json
{
  "export": {
    "formats": {
      "pdf": {
        "pageSize": "A4",
        "margins": "1in",
        "includeTOC": true
      },
      "docx": {
        "template": "templates/default.docx"
      },
      "html": {
        "inlineAssets": true,
        "includeNavigation": true
      }
    },
    "presets": {
      "documentation": ["pdf", "html", "markdown"],
      "deliverable": ["pdf", "docx"]
    }
  }
}
```

---

## Quick Reference

**Export single artifact:**
```javascript
await exportToPDF('/path/to/artifact.html', '/path/to/output.pdf');
```

**Export entire corpus:**
```javascript
await exportToJSON('/path/to/corpus', '/path/to/corpus-export.json');
```

**Generate documentation package:**
```javascript
await exportDocumentationPackage('/path/to/corpus', '/path/to/output');
```

---

*End of Corpus Export*
*Part of v4.0.0 Universal Skills Ecosystem*
*Category: Utilities*
*Multi-format export and documentation generation*
