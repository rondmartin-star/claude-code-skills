#!/usr/bin/env python3
"""
Convert HTML content to PDF format.

Usage:
    python convert_to_pdf.py <input.html> [--output <output.pdf>]

Requirements:
    pip install weasyprint

Example:
    python convert_to_pdf.py article.html
    python convert_to_pdf.py article.html --output submission.pdf
"""

import argparse
import sys
from pathlib import Path

try:
    from weasyprint import HTML
    HAS_DEPENDENCIES = True
except ImportError:
    HAS_DEPENDENCIES = False


class HTMLToPdfConverter:
    """Convert HTML content to PDF format using browser-based rendering."""

    def __init__(self, base_url: str = None):
        self.base_url = base_url

    def convert(self, html_path: Path, output_path: Path):
        """Convert HTML file to PDF."""
        html_doc = HTML(filename=str(html_path), base_url=self.base_url or str(html_path.parent))
        html_doc.write_pdf(str(output_path))

    def convert_string(self, html_content: str, output_path: Path):
        """Convert HTML string to PDF."""
        html_doc = HTML(string=html_content, base_url=self.base_url)
        html_doc.write_pdf(str(output_path))


def main():
    parser = argparse.ArgumentParser(
        description='Convert HTML content to PDF format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python convert_to_pdf.py article.html
    python convert_to_pdf.py article.html --output submission.pdf
        """
    )
    parser.add_argument('input', type=Path, help='Input HTML file')
    parser.add_argument('--output', '-o', type=Path, help='Output PDF file (default: input with .pdf extension)')

    args = parser.parse_args()

    if not HAS_DEPENDENCIES:
        print("Error: Required dependencies not installed.")
        print("Install with: pip install weasyprint")
        sys.exit(1)

    input_path = args.input.resolve()
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    output_path = args.output or input_path.with_suffix('.pdf')
    output_path = output_path.resolve()

    converter = HTMLToPdfConverter()
    try:
        converter.convert(input_path, output_path)
        print(f"PDF created: {output_path}")
    except Exception as e:
        print(f"Error converting to PDF: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
