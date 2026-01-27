#!/usr/bin/env python3
"""
Bundle and export content in various formats.

Usage:
    python bundle_content.py <path> --format <format> [options]

Formats:
    - zip: Create ZIP archive of all files
    - static: Generate self-contained HTML
    - text: Export as plain text
    - markdown: Export as Markdown
    - json: Export structured data
    - substack: Clean HTML for Substack paste
    - bibtex: Export references as BibTeX (journal articles)
    - deploy: Prepare for web deployment

Options:
    --output <path>    Output file/directory
    --sitemap          Generate sitemap.xml (websites)
    --minify           Minify HTML/CSS/JS

Example:
    python bundle_content.py website/ --format zip
    python bundle_content.py article.html --format markdown
    python bundle_content.py newsletter.html --format substack
"""

import argparse
import json
import re
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from html import unescape
from typing import Optional


class ContentBundler:
    """Bundle and export content in various formats."""
    
    def __init__(self, source_path: Path):
        self.source_path = source_path
        self.is_directory = source_path.is_dir()
    
    def bundle(self, format: str, output_path: Optional[Path] = None, **options) -> Path:
        """Bundle content in specified format."""
        bundlers = {
            'zip': self._bundle_zip,
            'static': self._bundle_static,
            'text': self._bundle_text,
            'markdown': self._bundle_markdown,
            'json': self._bundle_json,
            'substack': self._bundle_substack,
            'bibtex': self._bundle_bibtex,
            'deploy': self._bundle_deploy,
        }
        
        bundler = bundlers.get(format)
        if not bundler:
            raise ValueError(f"Unknown format: {format}")
        
        return bundler(output_path, **options)
    
    def _bundle_zip(self, output_path: Optional[Path], **options) -> Path:
        """Create ZIP archive."""
        if output_path is None:
            output_path = self.source_path.with_suffix('.zip')
        
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            if self.is_directory:
                for file in self.source_path.rglob('*'):
                    if file.is_file():
                        arcname = file.relative_to(self.source_path)
                        zf.write(file, arcname)
            else:
                zf.write(self.source_path, self.source_path.name)
        
        print(f"✓ Created ZIP: {output_path}")
        return output_path
    
    def _bundle_static(self, output_path: Optional[Path], **options) -> Path:
        """Create self-contained HTML with inlined CSS/JS."""
        if self.is_directory:
            raise ValueError("Static bundle only works with single HTML files")
        
        if output_path is None:
            output_path = self.source_path.with_stem(self.source_path.stem + '_static')
        
        content = self.source_path.read_text(encoding='utf-8')
        
        # Inline external CSS
        css_pattern = r'<link[^>]*href=["\']([^"\']+\.css)["\'][^>]*>'
        for match in re.finditer(css_pattern, content):
            css_path = self.source_path.parent / match.group(1)
            if css_path.exists():
                css_content = css_path.read_text(encoding='utf-8')
                style_tag = f'<style>{css_content}</style>'
                content = content.replace(match.group(0), style_tag)
        
        # Inline external JS
        js_pattern = r'<script[^>]*src=["\']([^"\']+\.js)["\'][^>]*></script>'
        for match in re.finditer(js_pattern, content):
            js_path = self.source_path.parent / match.group(1)
            if js_path.exists():
                js_content = js_path.read_text(encoding='utf-8')
                script_tag = f'<script>{js_content}</script>'
                content = content.replace(match.group(0), script_tag)
        
        output_path.write_text(content, encoding='utf-8')
        print(f"✓ Created static HTML: {output_path}")
        return output_path
    
    def _bundle_text(self, output_path: Optional[Path], **options) -> Path:
        """Export as plain text."""
        if output_path is None:
            output_path = self.source_path.with_suffix('.txt')
        
        if self.is_directory:
            texts = []
            for html_file in sorted(self.source_path.rglob('*.html')):
                content = html_file.read_text(encoding='utf-8')
                text = self._html_to_text(content)
                texts.append(f"=== {html_file.name} ===\n\n{text}")
            output_path.write_text('\n\n'.join(texts), encoding='utf-8')
        else:
            content = self.source_path.read_text(encoding='utf-8')
            text = self._html_to_text(content)
            output_path.write_text(text, encoding='utf-8')
        
        print(f"✓ Created text: {output_path}")
        return output_path
    
    def _html_to_text(self, html: str) -> str:
        """Convert HTML to plain text."""
        # Remove script and style
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<div[^>]*class="controls"[^>]*>.*?</div>', '', text, flags=re.DOTALL | re.IGNORECASE)
        
        # Convert headings
        for i in range(1, 7):
            text = re.sub(f'<h{i}[^>]*>([^<]*)</h{i}>', lambda m: '\n' + '#' * i + ' ' + m.group(1) + '\n', text, flags=re.IGNORECASE)
        
        # Convert paragraphs
        text = re.sub(r'<p[^>]*>', '\n', text, flags=re.IGNORECASE)
        text = re.sub(r'</p>', '\n', text, flags=re.IGNORECASE)
        
        # Convert lists
        text = re.sub(r'<li[^>]*>', '\n• ', text, flags=re.IGNORECASE)
        text = re.sub(r'</li>', '', text, flags=re.IGNORECASE)
        
        # Convert breaks
        text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
        text = re.sub(r'<hr\s*/?>', '\n---\n', text, flags=re.IGNORECASE)
        
        # Remove all other tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Clean up whitespace
        text = unescape(text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = text.strip()
        
        return text
    
    def _bundle_markdown(self, output_path: Optional[Path], **options) -> Path:
        """Export as Markdown."""
        if output_path is None:
            output_path = self.source_path.with_suffix('.md')
        
        if self.is_directory:
            raise ValueError("Markdown export only works with single HTML files")
        
        content = self.source_path.read_text(encoding='utf-8')
        md = self._html_to_markdown(content)
        output_path.write_text(md, encoding='utf-8')
        
        print(f"✓ Created Markdown: {output_path}")
        return output_path
    
    def _html_to_markdown(self, html: str) -> str:
        """Convert HTML to Markdown."""
        # Remove script, style, controls
        md = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        md = re.sub(r'<style[^>]*>.*?</style>', '', md, flags=re.DOTALL | re.IGNORECASE)
        md = re.sub(r'<div[^>]*class="controls"[^>]*>.*?</div>', '', md, flags=re.DOTALL | re.IGNORECASE)
        
        # Convert headings
        for i in range(1, 7):
            md = re.sub(f'<h{i}[^>]*>([^<]*)</h{i}>', lambda m: '\n' + '#' * i + ' ' + m.group(1) + '\n', md, flags=re.IGNORECASE)
        
        # Convert formatting
        md = re.sub(r'<strong[^>]*>([^<]*)</strong>', r'**\1**', md, flags=re.IGNORECASE)
        md = re.sub(r'<b[^>]*>([^<]*)</b>', r'**\1**', md, flags=re.IGNORECASE)
        md = re.sub(r'<em[^>]*>([^<]*)</em>', r'*\1*', md, flags=re.IGNORECASE)
        md = re.sub(r'<i[^>]*>([^<]*)</i>', r'*\1*', md, flags=re.IGNORECASE)
        
        # Convert links
        md = re.sub(r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>([^<]*)</a>', r'[\2](\1)', md, flags=re.IGNORECASE)
        
        # Convert images
        md = re.sub(r'<img[^>]*src=["\']([^"\']+)["\'][^>]*alt=["\']([^"\']*)["\'][^>]*/?>', r'![\2](\1)', md, flags=re.IGNORECASE)
        md = re.sub(r'<img[^>]*alt=["\']([^"\']*)["\'][^>]*src=["\']([^"\']+)["\'][^>]*/?>', r'![\1](\2)', md, flags=re.IGNORECASE)
        
        # Convert paragraphs
        md = re.sub(r'<p[^>]*>', '\n', md, flags=re.IGNORECASE)
        md = re.sub(r'</p>', '\n', md, flags=re.IGNORECASE)
        
        # Convert lists
        md = re.sub(r'<ul[^>]*>', '', md, flags=re.IGNORECASE)
        md = re.sub(r'</ul>', '', md, flags=re.IGNORECASE)
        md = re.sub(r'<ol[^>]*>', '', md, flags=re.IGNORECASE)
        md = re.sub(r'</ol>', '', md, flags=re.IGNORECASE)
        md = re.sub(r'<li[^>]*>', '\n- ', md, flags=re.IGNORECASE)
        md = re.sub(r'</li>', '', md, flags=re.IGNORECASE)
        
        # Convert blockquotes
        md = re.sub(r'<blockquote[^>]*>', '\n> ', md, flags=re.IGNORECASE)
        md = re.sub(r'</blockquote>', '\n', md, flags=re.IGNORECASE)
        
        # Convert code
        md = re.sub(r'<code[^>]*>([^<]*)</code>', r'`\1`', md, flags=re.IGNORECASE)
        md = re.sub(r'<pre[^>]*>([^<]*)</pre>', r'\n```\n\1\n```\n', md, flags=re.IGNORECASE)
        
        # Convert breaks
        md = re.sub(r'<br\s*/?>', '\n', md, flags=re.IGNORECASE)
        md = re.sub(r'<hr\s*/?>', '\n---\n', md, flags=re.IGNORECASE)
        
        # Remove remaining tags
        md = re.sub(r'<[^>]+>', '', md)
        
        # Clean up
        md = unescape(md)
        md = re.sub(r'\n{3,}', '\n\n', md)
        md = md.strip()
        
        return md
    
    def _bundle_json(self, output_path: Optional[Path], **options) -> Path:
        """Export as structured JSON."""
        if output_path is None:
            output_path = self.source_path.with_suffix('.json')
        
        if self.is_directory:
            # Export metadata and file list
            metadata_file = self.source_path / 'metadata.json'
            if metadata_file.exists():
                data = json.loads(metadata_file.read_text())
            else:
                data = {"name": self.source_path.name}
            
            data['files'] = [str(f.relative_to(self.source_path)) 
                           for f in self.source_path.rglob('*.html')]
        else:
            content = self.source_path.read_text(encoding='utf-8')
            data = {
                "file": self.source_path.name,
                "title": self._extract_title(content),
                "text": self._html_to_text(content),
                "word_count": len(self._html_to_text(content).split())
            }
        
        output_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
        print(f"✓ Created JSON: {output_path}")
        return output_path
    
    def _extract_title(self, html: str) -> str:
        """Extract title from HTML."""
        title_match = re.search(r'<title>([^<]*)</title>', html, re.IGNORECASE)
        if title_match:
            return unescape(title_match.group(1).strip())
        
        h1_match = re.search(r'<h1[^>]*>([^<]*)</h1>', html, re.IGNORECASE)
        if h1_match:
            return unescape(h1_match.group(1).strip())
        
        return "Untitled"
    
    def _bundle_substack(self, output_path: Optional[Path], **options) -> Path:
        """Clean HTML for Substack paste."""
        if output_path is None:
            output_path = self.source_path.with_stem(self.source_path.stem + '_substack')
        
        if self.is_directory:
            raise ValueError("Substack export only works with single HTML files")
        
        content = self.source_path.read_text(encoding='utf-8')
        
        # Extract article content
        article_match = re.search(r'<article[^>]*>(.*?)</article>', content, re.DOTALL | re.IGNORECASE)
        if article_match:
            content = article_match.group(1)
        else:
            main_match = re.search(r'<main[^>]*>(.*?)</main>', content, re.DOTALL | re.IGNORECASE)
            if main_match:
                content = main_match.group(1)
        
        # Remove controls
        content = re.sub(r'<div[^>]*class="controls"[^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove data attributes
        content = re.sub(r'\s*data-[a-z-]+="[^"]*"', '', content)
        
        # Remove class attributes that Substack won't use
        content = re.sub(r'\s*class="[^"]*"', '', content)
        
        # Remove id attributes
        content = re.sub(r'\s*id="[^"]*"', '', content)
        
        # Clean up whitespace
        content = re.sub(r'\s+>', '>', content)
        content = re.sub(r'>\s+<', '>\n<', content)
        
        output_path.write_text(content.strip(), encoding='utf-8')
        print(f"✓ Created Substack HTML: {output_path}")
        return output_path
    
    def _bundle_bibtex(self, output_path: Optional[Path], **options) -> Path:
        """Export references as BibTeX."""
        if output_path is None:
            output_path = self.source_path.with_suffix('.bib')
        
        # Look for references.json
        if self.is_directory:
            refs_file = self.source_path / 'data' / 'references.json'
        else:
            refs_file = self.source_path.parent / 'data' / 'references.json'
        
        if not refs_file.exists():
            print(f"Warning: No references.json found at {refs_file}")
            return output_path
        
        refs = json.loads(refs_file.read_text())
        
        bibtex_entries = []
        for ref in refs:
            entry = self._ref_to_bibtex(ref)
            if entry:
                bibtex_entries.append(entry)
        
        output_path.write_text('\n\n'.join(bibtex_entries), encoding='utf-8')
        print(f"✓ Created BibTeX: {output_path}")
        return output_path
    
    def _ref_to_bibtex(self, ref: dict) -> str:
        """Convert reference to BibTeX format."""
        ref_type = ref.get('type', 'article')
        ref_id = ref.get('id', 'unknown')
        
        fields = []
        
        # Authors
        authors = ref.get('authors', [])
        if authors:
            author_str = ' and '.join([
                f"{a.get('family', '')}, {a.get('given', '')}"
                for a in authors
            ])
            fields.append(f'  author = {{{author_str}}}')
        
        # Title
        if 'title' in ref:
            fields.append(f"  title = {{{ref['title']}}}")
        
        # Journal/Book
        if 'journal' in ref:
            fields.append(f"  journal = {{{ref['journal']}}}")
        if 'booktitle' in ref:
            fields.append(f"  booktitle = {{{ref['booktitle']}}}")
        
        # Year
        if 'year' in ref:
            fields.append(f"  year = {{{ref['year']}}}")
        
        # Volume, Issue, Pages
        if 'volume' in ref:
            fields.append(f"  volume = {{{ref['volume']}}}")
        if 'issue' in ref:
            fields.append(f"  number = {{{ref['issue']}}}")
        if 'pages' in ref:
            fields.append(f"  pages = {{{ref['pages']}}}")
        
        # DOI
        if 'doi' in ref:
            fields.append(f"  doi = {{{ref['doi']}}}")
        
        return f"@{ref_type}{{{ref_id},\n" + ',\n'.join(fields) + "\n}"
    
    def _bundle_deploy(self, output_path: Optional[Path], **options) -> Path:
        """Prepare for web deployment."""
        if not self.is_directory:
            raise ValueError("Deploy bundle only works with directories")
        
        if output_path is None:
            output_path = self.source_path.parent / f"{self.source_path.name}_deploy"
        
        # Copy all files
        if output_path.exists():
            shutil.rmtree(output_path)
        shutil.copytree(self.source_path, output_path)
        
        # Remove development files
        for pattern in ['*.pyc', '__pycache__', '.git', '.DS_Store', 'metadata.json']:
            for f in output_path.rglob(pattern):
                if f.is_file():
                    f.unlink()
                elif f.is_dir():
                    shutil.rmtree(f)
        
        # Generate sitemap if requested
        if options.get('sitemap'):
            self._generate_sitemap(output_path)
        
        print(f"✓ Created deploy bundle: {output_path}")
        return output_path
    
    def _generate_sitemap(self, root: Path):
        """Generate sitemap.xml."""
        html_files = list(root.rglob('*.html'))
        
        urls = []
        for f in html_files:
            rel_path = f.relative_to(root)
            urls.append(f'  <url><loc>/{rel_path}</loc></url>')
        
        sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>'''
        
        (root / 'sitemap.xml').write_text(sitemap, encoding='utf-8')
        print(f"  Generated sitemap.xml")


def main():
    parser = argparse.ArgumentParser(description="Bundle content in various formats")
    parser.add_argument("path", help="File or directory to bundle")
    parser.add_argument("--format", "-f", required=True,
                       choices=['zip', 'static', 'text', 'markdown', 'json', 'substack', 'bibtex', 'deploy'],
                       help="Output format")
    parser.add_argument("--output", "-o", help="Output path")
    parser.add_argument("--sitemap", action="store_true", help="Generate sitemap (deploy)")
    parser.add_argument("--minify", action="store_true", help="Minify output")
    
    args = parser.parse_args()
    
    source = Path(args.path)
    if not source.exists():
        print(f"Error: Path not found: {source}")
        return 1
    
    output = Path(args.output) if args.output else None
    
    bundler = ContentBundler(source)
    bundler.bundle(args.format, output, sitemap=args.sitemap, minify=args.minify)
    
    return 0


if __name__ == "__main__":
    exit(main())
