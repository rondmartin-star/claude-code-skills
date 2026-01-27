#!/usr/bin/env python3
"""
Initialize a new content project.

Usage:
    python init_content.py <content_type> <project_name> [--output-dir <path>]

Content Types:
    - bluesky: Bluesky thread template
    - newsletter: Substack/email newsletter
    - website: Multi-page website structure
    - blog: Single blog post
    - reference: Resource library
    - journal: Academic journal article

Example:
    python init_content.py newsletter my-newsletter
    python init_content.py website company-site --output-dir ./projects
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path


def create_directory(path: Path) -> None:
    """Create directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)


def write_file(path: Path, content: str) -> None:
    """Write content to file."""
    path.write_text(content, encoding='utf-8')


def get_metadata(project_name: str, content_type: str) -> dict:
    """Generate metadata for the project."""
    return {
        "name": project_name,
        "type": content_type,
        "created": datetime.now().isoformat(),
        "version": "1.0.0",
        "author": "",
        "description": ""
    }


def init_bluesky(project_dir: Path, project_name: str) -> None:
    """Initialize Bluesky thread project."""
    create_directory(project_dir)
    
    thread_html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bluesky Thread Preview</title>
  <style>
    :root { --bluesky-blue: #0085ff; --border: #e0e0e0; }
    body { font-family: -apple-system, sans-serif; max-width: 600px; margin: 2rem auto; padding: 1rem; background: #f7f9fa; }
    .controls { background: white; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; }
    .controls button { padding: 0.5rem 1rem; margin-right: 0.5rem; border: 1px solid var(--border); border-radius: 6px; background: white; cursor: pointer; }
    .thread-post { background: white; border: 1px solid var(--border); border-radius: 12px; padding: 1rem; margin-bottom: 0.5rem; }
    .post-content { white-space: pre-wrap; }
    .char-count { text-align: right; font-size: 0.8rem; color: #666; }
    .char-count.over { color: #dc2626; font-weight: bold; }
  </style>
</head>
<body>
  <div class="controls">
    <button onclick="window.print()">Print</button>
    <button onclick="copyThread()">Copy All</button>
  </div>
  <div class="thread" data-content-type="bluesky">
    <div class="thread-post" data-line="1">
      <div class="post-content">Your hook post goes here. Make it attention-grabbing! 1/3</div>
      <div class="char-count">73/300</div>
    </div>
    <div class="thread-post" data-line="5">
      <div class="post-content">Your main point goes here. Add value for your readers. 2/3</div>
      <div class="char-count">62/300</div>
    </div>
    <div class="thread-post" data-line="9">
      <div class="post-content">Your call-to-action goes here. What should readers do next? 3/3</div>
      <div class="char-count">68/300</div>
    </div>
  </div>
  <script>
    function copyThread() {
      const posts = document.querySelectorAll('.post-content');
      let text = Array.from(posts).map(p => p.textContent.trim()).join('\\n\\n---\\n\\n');
      navigator.clipboard.writeText(text);
      alert('Thread copied!');
    }
  </script>
</body>
</html>'''
    write_file(project_dir / "thread.html", thread_html)
    write_file(project_dir / "metadata.json", json.dumps(get_metadata(project_name, "bluesky"), indent=2))
    print(f"✓ Created Bluesky thread project: {project_dir}")


def init_newsletter(project_dir: Path, project_name: str) -> None:
    """Initialize newsletter project."""
    create_directory(project_dir)
    
    newsletter_html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Newsletter Title</title>
  <style>
    body { font-family: Georgia, serif; line-height: 1.7; max-width: 680px; margin: 0 auto; padding: 2rem; }
    .controls { background: #f5f5f5; padding: 1rem; border-radius: 8px; margin-bottom: 2rem; display: flex; gap: 0.5rem; }
    .controls button { padding: 0.5rem 1rem; border: 1px solid #ddd; border-radius: 4px; background: white; cursor: pointer; }
    h1 { font-size: 2rem; line-height: 1.2; }
    h2 { font-size: 1.5rem; margin-top: 2rem; }
    .metadata { color: #666; font-size: 0.9rem; margin-bottom: 2rem; }
    .cta-box { background: #f9f9f9; padding: 1.5rem; border-radius: 8px; text-align: center; margin: 2rem 0; }
    @media print { .controls { display: none; } }
  </style>
</head>
<body>
  <div class="controls">
    <button onclick="window.print()">Print</button>
    <button onclick="copyHTML()">Copy HTML</button>
  </div>
  <article data-content-type="newsletter">
    <header>
      <h1 data-line="1">Newsletter Title Here</h1>
      <div class="metadata">By Author · Date · X min read</div>
    </header>
    <main id="content">
      <p data-line="5">Your opening hook goes here.</p>
      <h2 data-line="10">Section One</h2>
      <p data-line="12">Main content paragraph.</p>
      <div class="cta-box" data-line="30">
        <p><strong>Enjoyed this?</strong></p>
        <p>Subscribe for more content like this.</p>
      </div>
    </main>
  </article>
  <script>
    function copyHTML() {
      navigator.clipboard.writeText(document.querySelector('article').innerHTML);
      alert('HTML copied!');
    }
  </script>
</body>
</html>'''
    write_file(project_dir / "newsletter.html", newsletter_html)
    write_file(project_dir / "metadata.json", json.dumps(get_metadata(project_name, "newsletter"), indent=2))
    print(f"✓ Created newsletter project: {project_dir}")


def init_website(project_dir: Path, project_name: str) -> None:
    """Initialize multi-page website project."""
    create_directory(project_dir)
    create_directory(project_dir / "pages")
    create_directory(project_dir / "assets" / "css")
    create_directory(project_dir / "assets" / "js")
    create_directory(project_dir / "assets" / "images")
    
    index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Home | Site Name</title>
  <link rel="stylesheet" href="assets/css/main.css">
</head>
<body data-page="home">
  <div class="controls">
    <button onclick="window.print()">Print</button>
    <button onclick="toggleView()">View Source</button>
  </div>
  <header class="site-header">
    <nav><a href="/">Home</a> <a href="/pages/about.html">About</a></nav>
  </header>
  <main data-content-type="website" data-line="1">
    <section class="hero">
      <h1>Welcome to Your Site</h1>
      <p>Your tagline here.</p>
    </section>
  </main>
  <footer class="site-footer"><p>&copy; 2026 Site Name</p></footer>
  <script src="assets/js/main.js"></script>
</body>
</html>'''
    write_file(project_dir / "index.html", index_html)
    
    main_css = ''':root { --primary: #2563eb; --text: #1f2937; --border: #e5e7eb; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, sans-serif; line-height: 1.6; color: var(--text); }
.controls { background: #f5f5f5; padding: 0.75rem; display: flex; gap: 0.5rem; }
.controls button { padding: 0.4rem 0.8rem; border: 1px solid var(--border); border-radius: 4px; background: white; cursor: pointer; }
.site-header { padding: 1rem 2rem; border-bottom: 1px solid var(--border); }
.site-header nav { display: flex; gap: 1.5rem; }
.site-header a { color: var(--text); text-decoration: none; }
.hero { padding: 4rem 2rem; text-align: center; }
.hero h1 { font-size: 2.5rem; margin-bottom: 1rem; }
.site-footer { padding: 2rem; text-align: center; border-top: 1px solid var(--border); }
@media print { .controls { display: none; } }'''
    write_file(project_dir / "assets" / "css" / "main.css", main_css)
    
    main_js = '''function toggleView() {
  const main = document.querySelector('main');
  if (main.dataset.mode === 'source') { location.reload(); }
  else { main.dataset.mode = 'source'; main.innerHTML = '<pre>' + main.innerHTML.replace(/</g, '&lt;') + '</pre>'; }
}'''
    write_file(project_dir / "assets" / "js" / "main.js", main_js)
    
    metadata = get_metadata(project_name, "website")
    metadata["pages"] = [{"id": "home", "path": "/index.html", "title": "Home"}]
    write_file(project_dir / "metadata.json", json.dumps(metadata, indent=2))
    print(f"✓ Created website project: {project_dir}")


def init_blog(project_dir: Path, project_name: str) -> None:
    """Initialize blog post project."""
    create_directory(project_dir)
    
    blog_html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Meta description here">
  <title>Blog Post Title</title>
  <style>
    body { font-family: Georgia, serif; line-height: 1.8; max-width: 720px; margin: 0 auto; padding: 2rem; }
    .controls { background: #f5f5f5; padding: 0.75rem; border-radius: 8px; margin-bottom: 2rem; display: flex; gap: 0.5rem; }
    .controls button { padding: 0.4rem 0.8rem; border: 1px solid #ddd; border-radius: 4px; background: white; cursor: pointer; }
    h1 { font-size: 2.5rem; line-height: 1.15; margin-bottom: 0.5rem; }
    h2 { font-size: 1.75rem; margin-top: 2.5rem; }
    .meta { color: #666; font-size: 0.9rem; margin-bottom: 2rem; }
    .lead { font-size: 1.25rem; color: #555; font-style: italic; }
    @media print { .controls { display: none; } }
  </style>
</head>
<body>
  <div class="controls">
    <button onclick="window.print()">Print</button>
    <button onclick="generatePDF()">PDF</button>
  </div>
  <article data-content-type="blog-post">
    <header>
      <h1 data-line="1">Your Blog Post Title</h1>
      <div class="meta">By Author · Date · X min read</div>
      <p class="lead" data-line="5">Your compelling lead paragraph.</p>
    </header>
    <main id="content">
      <h2 data-line="10">First Section</h2>
      <p data-line="12">Your content here.</p>
    </main>
  </article>
  <script>
    function generatePDF() {
      document.querySelector('.controls').style.display = 'none';
      window.print();
      document.querySelector('.controls').style.display = 'flex';
    }
  </script>
</body>
</html>'''
    write_file(project_dir / "post.html", blog_html)
    write_file(project_dir / "metadata.json", json.dumps(get_metadata(project_name, "blog"), indent=2))
    print(f"✓ Created blog post project: {project_dir}")


def init_reference(project_dir: Path, project_name: str) -> None:
    """Initialize reference library project."""
    create_directory(project_dir)
    create_directory(project_dir / "data")
    
    resources = [{"id": "resource-001", "title": "Sample Resource", "description": "Description.", "url": "https://example.com", "type": "article", "category": "Getting Started", "tags": ["tag1"]}]
    write_file(project_dir / "data" / "resources.json", json.dumps(resources, indent=2))
    
    index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Resource Library</title>
  <style>
    body { font-family: -apple-system, sans-serif; max-width: 1200px; margin: 0 auto; padding: 2rem; }
    .resource-card { background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 1.5rem; margin-bottom: 1rem; }
    .resource-card h3 a { color: #1f2937; text-decoration: none; }
    .resource-card h3 a:hover { color: #2563eb; }
  </style>
</head>
<body>
  <header><h1>Resource Library</h1></header>
  <main id="resources" data-content-type="reference"></main>
  <script>
    fetch('data/resources.json').then(r => r.json()).then(resources => {
      document.getElementById('resources').innerHTML = resources.map(r => 
        '<div class="resource-card"><h3><a href="' + r.url + '">' + r.title + '</a></h3><p>' + r.description + '</p></div>'
      ).join('');
    });
  </script>
</body>
</html>'''
    write_file(project_dir / "index.html", index_html)
    write_file(project_dir / "metadata.json", json.dumps(get_metadata(project_name, "reference"), indent=2))
    print(f"✓ Created reference library project: {project_dir}")


def init_journal(project_dir: Path, project_name: str) -> None:
    """Initialize journal article project."""
    create_directory(project_dir)
    create_directory(project_dir / "figures")
    create_directory(project_dir / "data")
    
    journal_html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Article Title</title>
  <style>
    body { font-family: 'Times New Roman', serif; font-size: 12pt; line-height: 2; max-width: 8.5in; margin: 0 auto; padding: 1in; }
    .controls { font-family: sans-serif; background: #f5f5f5; padding: 0.75rem; margin-bottom: 2rem; display: flex; gap: 0.5rem; }
    .controls button, .controls select { padding: 0.4rem 0.8rem; border: 1px solid #ddd; border-radius: 4px; background: white; }
    .article-header { text-align: center; margin-bottom: 2rem; }
    h1 { font-size: 16pt; }
    h2 { font-size: 14pt; text-transform: uppercase; margin-top: 2rem; }
    p { text-align: justify; text-indent: 0.5in; }
    .abstract { background: #f9f9f9; padding: 1rem; border-left: 3px solid #2563eb; margin: 2rem 0; }
    .abstract p { text-indent: 0; }
    .reference-item { padding-left: 0.5in; text-indent: -0.5in; margin-bottom: 1rem; }
    @media print { .controls { display: none; } }
  </style>
</head>
<body>
  <div class="controls">
    <button onclick="window.print()">Print</button>
    <button onclick="alert('Use: python scripts/convert_to_docx.py')">Export DOCX</button>
    <select id="citation-style">
      <option value="apa7">APA 7th</option>
      <option value="mla9">MLA 9th</option>
      <option value="chicago">Chicago</option>
    </select>
  </div>
  <article data-content-type="journal-article">
    <header class="article-header">
      <h1 data-line="1">Article Title</h1>
      <p>Author Name<sup>1</sup></p>
      <p><sup>1</sup>Affiliation</p>
    </header>
    <section class="abstract" data-line="10">
      <h2>Abstract</h2>
      <p>Your abstract here (150-300 words).</p>
      <p><strong>Keywords:</strong> keyword1, keyword2</p>
    </section>
    <section data-line="20"><h2>Introduction</h2><p>Introduction content.</p></section>
    <section data-line="40"><h2>Methods</h2><p>Methods content.</p></section>
    <section data-line="60"><h2>Results</h2><p>Results content.</p></section>
    <section data-line="80"><h2>Discussion</h2><p>Discussion content.</p></section>
    <section data-line="100"><h2>Conclusion</h2><p>Conclusion content.</p></section>
    <section class="references" data-line="120">
      <h2>References</h2>
      <div class="reference-item">Author, A. A. (Year). Title. Journal, Volume(Issue), Pages.</div>
    </section>
  </article>
</body>
</html>'''
    write_file(project_dir / "article.html", journal_html)
    
    references = [{"id": "author2020", "type": "article", "authors": [{"family": "Author", "given": "A."}], "title": "Article Title", "journal": "Journal Name", "year": 2020}]
    write_file(project_dir / "data" / "references.json", json.dumps(references, indent=2))
    write_file(project_dir / "metadata.json", json.dumps(get_metadata(project_name, "journal"), indent=2))
    print(f"✓ Created journal article project: {project_dir}")


def main():
    parser = argparse.ArgumentParser(description="Initialize a new content project")
    parser.add_argument("content_type", choices=["bluesky", "newsletter", "website", "blog", "reference", "journal"])
    parser.add_argument("project_name", help="Name of the project")
    parser.add_argument("--output-dir", "-o", default=".", help="Output directory")
    
    args = parser.parse_args()
    project_dir = Path(args.output_dir) / args.project_name
    
    if project_dir.exists():
        print(f"Error: Directory already exists: {project_dir}")
        return 1
    
    initializers = {
        "bluesky": init_bluesky, "newsletter": init_newsletter, "website": init_website,
        "blog": init_blog, "reference": init_reference, "journal": init_journal
    }
    
    initializers[args.content_type](project_dir, args.project_name)
    print(f"\nNext steps:\n  1. cd {project_dir}\n  2. Edit the HTML files\n  3. Run: python validate_content.py .")
    return 0


if __name__ == "__main__":
    exit(main())
