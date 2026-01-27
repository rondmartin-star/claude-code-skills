# Reference Material Content Reference

**Output Types:** Resource libraries, documentation hubs, curated link collections  
**Load when:** User mentions reference material, resource page, library, documentation, or curated links

---

## Reference Material Architecture

### Purpose

Reference materials provide organized, searchable collections of resources for websites, intranets, or knowledge bases. They prioritize findability, categorization, and context.

### Multi-File Structure

```
reference-library/
├── index.html              # Main entry/search
├── categories/
│   ├── category-1.html
│   ├── category-2.html
│   └── category-3.html
├── resources/
│   ├── resource-001.html   # Individual resource pages (optional)
│   ├── resource-002.html
│   └── ...
├── assets/
│   ├── css/
│   └── icons/
├── data/
│   └── resources.json      # Resource database
└── metadata.json
```

### Benefits of This Architecture

| Feature | Benefit |
|---------|---------|
| JSON data source | Easy to update without editing HTML |
| Category pages | Browsable organization |
| Individual resource pages | Deep linking, detailed annotations |
| Search integration | Quick access to specific resources |

---

## Resource Data Schema

`data/resources.json`:
```json
[
  {
    "id": "resource-001",
    "title": "Resource Title",
    "description": "Brief description of what this resource offers.",
    "url": "https://example.com/resource",
    "type": "article",
    "category": "Category Name",
    "tags": ["tag1", "tag2"],
    "source": "Publisher/Author",
    "date": "2026-01-15",
    "readTime": 10,
    "featured": true,
    "annotation": "Curator notes explaining value",
    "line": 50
  }
]
```

### Resource Types

| Type | Use For | Icon Color |
|------|---------|------------|
| `article` | Blog posts, news, written content | Blue |
| `tool` | Software, apps, utilities | Green |
| `video` | YouTube, courses, tutorials | Yellow |
| `book` | Books, ebooks, long-form | Pink |
| `course` | Structured learning paths | Purple |
| `podcast` | Audio content | Orange |
| `template` | Downloadable templates | Gray |

---

## Main Index Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{library_title}} | Resource Library</title>
  <style>
    :root {
      --primary-color: #2563eb;
      --text-color: #1f2937;
      --text-light: #6b7280;
      --bg-color: #ffffff;
      --bg-light: #f9fafb;
      --border-color: #e5e7eb;
    }
    
    body {
      font-family: -apple-system, BlinkMacSystemFont, sans-serif;
      line-height: 1.6;
      color: var(--text-color);
      background: var(--bg-light);
      margin: 0;
    }
    
    .controls {
      background: white;
      padding: 0.75rem 1rem;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      gap: 0.5rem;
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
    }
    
    .library-header {
      background: white;
      padding: 3rem 2rem;
      text-align: center;
      border-bottom: 1px solid var(--border-color);
    }
    
    .search-container {
      max-width: 600px;
      margin: 2rem auto;
      padding: 0 1rem;
    }
    .search-box {
      display: flex;
      background: white;
      border: 2px solid var(--border-color);
      border-radius: 8px;
    }
    .search-box input {
      flex: 1;
      padding: 1rem;
      border: none;
      outline: none;
    }
    
    .main-content {
      max-width: 1200px;
      margin: 0 auto;
      padding: 2rem;
      display: grid;
      grid-template-columns: 250px 1fr;
      gap: 2rem;
    }
    
    .resource-card {
      background: white;
      border-radius: 8px;
      padding: 1.5rem;
      margin-bottom: 1rem;
      border: 1px solid var(--border-color);
    }
    
    .resource-type {
      display: inline-block;
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      font-size: 0.75rem;
      font-weight: 600;
    }
    .resource-type.article { background: #dbeafe; color: #1d4ed8; }
    .resource-type.tool { background: #dcfce7; color: #16a34a; }
    .resource-type.video { background: #fef3c7; color: #d97706; }
    .resource-type.book { background: #fce7f3; color: #db2777; }
    
    @media print {
      .controls, .search-container { display: none; }
    }
  </style>
</head>
<body>
  <div class="controls">
    <button onclick="window.print()">Print</button>
    <button onclick="exportJSON()">Export JSON</button>
    <button onclick="toggleSource()">View Source</button>
  </div>

  <header class="library-header">
    <h1>{{library_title}}</h1>
    <p>{{library_description}}</p>
  </header>

  <div class="search-container">
    <div class="search-box">
      <input type="text" id="search" placeholder="Search resources...">
    </div>
  </div>

  <main class="main-content">
    <aside class="sidebar" id="categories">
      <!-- Categories generated from data -->
    </aside>
    <div id="resources-grid">
      <!-- Resources generated from data -->
    </div>
  </main>

  <script>
    const resources = []; // Loaded from JSON
    
    function renderResources(items) {
      const grid = document.getElementById('resources-grid');
      grid.innerHTML = items.map(r => `
        <div class="resource-card">
          <span class="resource-type ${r.type}">${r.type}</span>
          <h3><a href="${r.url}">${r.title}</a></h3>
          <p>${r.description}</p>
        </div>
      `).join('');
    }
  </script>
</body>
</html>
```

---

## Annotation Guidelines

### What to Include

| Element | Purpose | Example |
|---------|---------|---------|
| **Summary** | Quick overview | "Comprehensive guide to..." |
| **Best for** | Target audience | "Beginners to X" |
| **Key insight** | Main takeaway | "The core framework is..." |
| **Prerequisites** | Required knowledge | "Assumes familiarity with..." |
| **Time investment** | Reading/watching time | "~15 min read" |
| **Quality signal** | Why this source | "Cited by X, peer-reviewed" |

---

## Building the Library

### Step 1: Gather Resources

```bash
python scripts/init_content.py reference-library my-library
```

### Step 2: Categorize

Organize resources into logical categories:
- By topic (e.g., "Design", "Development")
- By skill level (e.g., "Beginner", "Advanced")
- By format (e.g., "Articles", "Videos")

### Step 3: Annotate

Add value through curation:
- Write descriptions explaining *why* this resource matters
- Add tags for discoverability
- Note prerequisites or related resources

---

## Export Options

| Format | Command | Use Case |
|--------|---------|----------|
| Static HTML | `--format static` | Offline use |
| OPML | `--format opml` | RSS readers |
| CSV | `--format csv` | Spreadsheet editing |
| Markdown | `--format markdown` | Documentation sites |

---

## Validation Checklist

### Data Quality

- [ ] All resources have title and description
- [ ] URLs are valid and accessible
- [ ] Categories are consistent
- [ ] Tags are normalized

### Structure

- [ ] Index page renders correctly
- [ ] Search works
- [ ] Category filters work
- [ ] Resource links work

---

*End of Reference Material Content Reference*
