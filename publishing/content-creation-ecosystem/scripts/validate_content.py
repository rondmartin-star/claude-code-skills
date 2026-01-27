#!/usr/bin/env python3
"""
Validate content files before delivery.

Usage:
    python validate_content.py <path> [options]

Options:
    --check-links    Only check links
    --check-a11y     Only check accessibility
    --check-html     Only check HTML validity
    --word-count     Show word count only
    --all            Validate entire directory
    --verbose        Show detailed output

Example:
    python validate_content.py post.html
    python validate_content.py website/ --all
    python validate_content.py article.html --check-links
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple
from html.parser import HTMLParser
from urllib.parse import urlparse


class ContentValidator:
    """Validates HTML content files."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.errors: List[Tuple[str, str, int]] = []  # (type, message, line)
        self.warnings: List[Tuple[str, str, int]] = []
        self.stats = {
            "word_count": 0,
            "headings": [],
            "links": [],
            "images": []
        }
    
    def validate_file(self, filepath: Path) -> bool:
        """Validate a single HTML file."""
        if not filepath.exists():
            self.errors.append(("file", f"File not found: {filepath}", 0))
            return False
        
        content = filepath.read_text(encoding='utf-8')
        
        # Run all checks
        self._check_html_structure(content)
        self._check_escape_sequences(content)
        self._check_accessibility(content)
        self._check_placeholders(content)
        self._check_controls(content)
        self._calculate_stats(content)
        
        return len(self.errors) == 0
    
    def _check_html_structure(self, content: str) -> None:
        """Check basic HTML structure."""
        # Check for DOCTYPE
        if not content.strip().lower().startswith('<!doctype html>'):
            self.errors.append(("html", "Missing DOCTYPE declaration", 1))
        
        # Check for required elements
        if '<html' not in content.lower():
            self.errors.append(("html", "Missing <html> tag", 0))
        if '<head>' not in content.lower():
            self.errors.append(("html", "Missing <head> section", 0))
        if '<body>' not in content.lower():
            self.errors.append(("html", "Missing <body> section", 0))
        if '<title>' not in content.lower():
            self.errors.append(("html", "Missing <title> tag", 0))
        
        # Check for lang attribute
        if not re.search(r'<html[^>]*lang=', content, re.IGNORECASE):
            self.warnings.append(("a11y", "Missing lang attribute on <html>", 0))
        
        # Check for viewport meta
        if 'viewport' not in content.lower():
            self.warnings.append(("html", "Missing viewport meta tag", 0))
        
        # Check for unclosed tags (basic check)
        open_tags = re.findall(r'<([a-z0-9]+)[^>]*>', content, re.IGNORECASE)
        close_tags = re.findall(r'</([a-z0-9]+)>', content, re.IGNORECASE)
        self_closing = {'br', 'hr', 'img', 'input', 'meta', 'link', 'area', 'base', 'col', 'embed', 'source', 'track', 'wbr'}
        
        open_counts = {}
        for tag in open_tags:
            tag_lower = tag.lower()
            if tag_lower not in self_closing:
                open_counts[tag_lower] = open_counts.get(tag_lower, 0) + 1
        
        for tag in close_tags:
            tag_lower = tag.lower()
            open_counts[tag_lower] = open_counts.get(tag_lower, 0) - 1
        
        for tag, count in open_counts.items():
            if count > 0:
                self.errors.append(("html", f"Unclosed <{tag}> tag(s): {count}", 0))
            elif count < 0:
                self.errors.append(("html", f"Extra closing </{tag}> tag(s): {abs(count)}", 0))
    
    def _check_escape_sequences(self, content: str) -> None:
        """Check for literal escape sequences that should be HTML."""
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            # Check for literal \n (not \\n which is escaped backslash)
            if re.search(r'(?<!\\)\\n', line):
                self.errors.append(("escape", f"Literal \\n found - use <br> or <p>", i))
            
            if re.search(r'(?<!\\)\\t', line):
                self.errors.append(("escape", f"Literal \\t found - use CSS spacing", i))
            
            if re.search(r'(?<!\\)\\r', line):
                self.errors.append(("escape", f"Literal \\r found - remove", i))
    
    def _check_accessibility(self, content: str) -> None:
        """Check accessibility requirements."""
        # Check images for alt text
        img_tags = re.findall(r'<img[^>]*>', content, re.IGNORECASE)
        for img in img_tags:
            if 'alt=' not in img.lower():
                self.errors.append(("a11y", "Image missing alt attribute", 0))
        
        # Check heading hierarchy
        headings = re.findall(r'<h([1-6])[^>]*>', content, re.IGNORECASE)
        heading_levels = [int(h) for h in headings]
        
        if heading_levels:
            # Should start with h1
            if heading_levels[0] != 1:
                self.warnings.append(("a11y", f"First heading is h{heading_levels[0]}, should be h1", 0))
            
            # Check for skipped levels
            for i in range(1, len(heading_levels)):
                if heading_levels[i] > heading_levels[i-1] + 1:
                    self.warnings.append(("a11y", f"Heading level skipped: h{heading_levels[i-1]} to h{heading_levels[i]}", 0))
            
            # Check for multiple h1
            h1_count = heading_levels.count(1)
            if h1_count > 1:
                self.warnings.append(("a11y", f"Multiple h1 tags found: {h1_count}", 0))
            elif h1_count == 0:
                self.errors.append(("a11y", "No h1 tag found", 0))
        
        # Check links
        links = re.findall(r'<a[^>]*>([^<]*)</a>', content, re.IGNORECASE)
        generic_link_texts = ['click here', 'here', 'link', 'read more', 'more']
        for link_text in links:
            if link_text.lower().strip() in generic_link_texts:
                self.warnings.append(("a11y", f"Generic link text: '{link_text}'", 0))
    
    def _check_placeholders(self, content: str) -> None:
        """Check for remaining placeholder text."""
        placeholders = [
            (r'\{\{[^}]+\}\}', "Template placeholder"),
            (r'TODO', "TODO marker"),
            (r'FIXME', "FIXME marker"),
            (r'XXX', "XXX marker"),
            (r'Lorem ipsum', "Lorem ipsum placeholder"),
        ]
        
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            for pattern, desc in placeholders:
                if re.search(pattern, line, re.IGNORECASE):
                    self.errors.append(("placeholder", f"{desc} found", i))
    
    def _check_controls(self, content: str) -> None:
        """Check for interactive controls."""
        if 'data-content-type' in content:
            # This is a content file, should have controls
            has_print = 'print()' in content or 'window.print' in content
            has_view = 'toggleView' in content or 'View' in content
            
            if not has_print:
                self.warnings.append(("controls", "No print functionality detected", 0))
    
    def _calculate_stats(self, content: str) -> None:
        """Calculate content statistics."""
        # Strip HTML tags for word count
        text = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        words = [w for w in text.split() if len(w) > 0]
        self.stats["word_count"] = len(words)
        
        # Extract headings
        self.stats["headings"] = re.findall(r'<h([1-6])[^>]*>([^<]*)</h\1>', content, re.IGNORECASE)
        
        # Extract links
        self.stats["links"] = re.findall(r'href=["\']([^"\']+)["\']', content, re.IGNORECASE)
        
        # Extract images
        self.stats["images"] = re.findall(r'src=["\']([^"\']+)["\']', content, re.IGNORECASE)
    
    def check_links(self, content: str, base_path: Path) -> None:
        """Check if links resolve correctly."""
        links = re.findall(r'href=["\']([^"\']+)["\']', content, re.IGNORECASE)
        
        for link in links:
            if link.startswith('#'):
                # Internal anchor
                anchor_id = link[1:]
                if f'id="{anchor_id}"' not in content and f"id='{anchor_id}'" not in content:
                    self.warnings.append(("link", f"Anchor target not found: {link}", 0))
            elif link.startswith('http://') or link.startswith('https://'):
                # External link - just note it
                if self.verbose:
                    print(f"  External link: {link}")
            elif link.startswith('mailto:') or link.startswith('tel:'):
                # Contact links - OK
                pass
            elif link.startswith('javascript:'):
                self.warnings.append(("link", f"JavaScript link: {link}", 0))
            else:
                # Relative link - check if file exists
                link_path = base_path.parent / link
                if not link_path.exists():
                    self.errors.append(("link", f"Broken link: {link}", 0))
    
    def report(self) -> str:
        """Generate validation report."""
        lines = []
        
        lines.append("=" * 60)
        lines.append("CONTENT VALIDATION REPORT")
        lines.append("=" * 60)
        lines.append("")
        
        # Statistics
        lines.append("Statistics:")
        lines.append(f"  Word count: {self.stats['word_count']}")
        lines.append(f"  Headings: {len(self.stats['headings'])}")
        lines.append(f"  Links: {len(self.stats['links'])}")
        lines.append(f"  Images: {len(self.stats['images'])}")
        lines.append("")
        
        # Errors
        if self.errors:
            lines.append(f"ERRORS ({len(self.errors)}):")
            for err_type, message, line in self.errors:
                line_str = f" (line {line})" if line > 0 else ""
                lines.append(f"  ✗ [{err_type}] {message}{line_str}")
            lines.append("")
        
        # Warnings
        if self.warnings:
            lines.append(f"WARNINGS ({len(self.warnings)}):")
            for warn_type, message, line in self.warnings:
                line_str = f" (line {line})" if line > 0 else ""
                lines.append(f"  ⚠ [{warn_type}] {message}{line_str}")
            lines.append("")
        
        # Summary
        lines.append("-" * 60)
        if self.errors:
            lines.append(f"Status: ✗ FAILED ({len(self.errors)} errors, {len(self.warnings)} warnings)")
        elif self.warnings:
            lines.append(f"Status: ⚠ PASSED WITH WARNINGS ({len(self.warnings)} warnings)")
        else:
            lines.append("Status: ✓ PASSED")
        lines.append("=" * 60)
        
        return "\n".join(lines)


def validate_directory(dir_path: Path, verbose: bool = False) -> bool:
    """Validate all HTML files in a directory."""
    html_files = list(dir_path.rglob("*.html"))
    
    if not html_files:
        print(f"No HTML files found in: {dir_path}")
        return False
    
    all_passed = True
    
    for filepath in html_files:
        print(f"\nValidating: {filepath}")
        validator = ContentValidator(verbose=verbose)
        
        content = filepath.read_text(encoding='utf-8')
        validator.validate_file(filepath)
        validator.check_links(content, filepath)
        
        print(validator.report())
        
        if validator.errors:
            all_passed = False
    
    return all_passed


def main():
    parser = argparse.ArgumentParser(description="Validate content files")
    parser.add_argument("path", help="File or directory to validate")
    parser.add_argument("--check-links", action="store_true", help="Check links only")
    parser.add_argument("--check-a11y", action="store_true", help="Check accessibility only")
    parser.add_argument("--check-html", action="store_true", help="Check HTML only")
    parser.add_argument("--word-count", action="store_true", help="Show word count only")
    parser.add_argument("--all", action="store_true", help="Validate entire directory")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    path = Path(args.path)
    
    if not path.exists():
        print(f"Error: Path not found: {path}")
        return 1
    
    if path.is_dir() or args.all:
        dir_path = path if path.is_dir() else path.parent
        success = validate_directory(dir_path, args.verbose)
    else:
        validator = ContentValidator(verbose=args.verbose)
        content = path.read_text(encoding='utf-8')
        
        if args.word_count:
            validator._calculate_stats(content)
            print(f"Word count: {validator.stats['word_count']}")
            return 0
        
        validator.validate_file(path)
        validator.check_links(content, path)
        print(validator.report())
        success = len(validator.errors) == 0
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
