# Validation Reference

**Purpose:** Quality assurance checklists for all content types  
**Load when:** Preparing content for delivery or troubleshooting issues

---

## Universal Validation Checklist

Apply to ALL content types before delivery:

### Structure

- [ ] Title present and descriptive
- [ ] All sections complete (no placeholders)
- [ ] Logical flow from start to finish
- [ ] Appropriate length for content type

### Technical

- [ ] Valid HTML5 (no unclosed tags)
- [ ] No literal escape sequences (`\n`, `\t`, `\r`)
- [ ] All images have `alt` attributes
- [ ] All links functional
- [ ] Controls (View/Print/PDF/Edit) working

### Content Quality

- [ ] No spelling errors
- [ ] No grammar errors
- [ ] Consistent tone throughout
- [ ] Clear and concise language
- [ ] No placeholder text remaining

### Accessibility

- [ ] Heading hierarchy logical (h1 → h2 → h3)
- [ ] Color contrast meets WCAG AA (4.5:1)
- [ ] Images have descriptive alt text
- [ ] Links have meaningful text (not "click here")

---

## Content-Type Specific Checklists

### Bluesky Post

- [ ] Each post ≤ 300 characters
- [ ] Thread numbering correct (1/N, 2/N...)
- [ ] Hook post captures attention
- [ ] CTA in final post
- [ ] Hashtags relevant (2-3 max)
- [ ] Images have alt text

### Substack Newsletter

- [ ] Subject line compelling (under 60 chars)
- [ ] Preview text complements subject
- [ ] Opening hook in first paragraph
- [ ] Clear value proposition
- [ ] CTA present and specific
- [ ] HTML compatible with Substack editor
- [ ] Mobile display verified

### Website

- [ ] All pages have unique titles
- [ ] Navigation consistent across pages
- [ ] Links between pages work
- [ ] Meta descriptions set
- [ ] Open Graph tags present
- [ ] Mobile responsive
- [ ] 404 page exists
- [ ] sitemap.xml generated

### Blog Post

- [ ] Title optimized for SEO (under 60 chars)
- [ ] Meta description set (150-160 chars)
- [ ] Primary keyword in title and H1
- [ ] Internal links present
- [ ] External links to authority sources
- [ ] Images optimized (< 200KB)
- [ ] Reading time calculated
- [ ] Author attribution present

### Reference Library

- [ ] All resources have title and description
- [ ] URLs verified and accessible
- [ ] Categories consistent
- [ ] Tags normalized
- [ ] Search functionality works
- [ ] Filtering works
- [ ] Annotations add value

### Journal Article

- [ ] Follows target journal format (IMRaD etc.)
- [ ] Abstract includes all required elements
- [ ] Word count within limits
- [ ] Citation style consistent
- [ ] All citations have matching references
- [ ] All references cited in text
- [ ] Figures/tables properly labeled
- [ ] DOIs included where available
- [ ] DOCX export clean

---

## Validation Script Usage

### Run Full Validation

```bash
python scripts/validate_content.py path/to/content.html
```

### Check Specific Issues

```bash
# Check links only
python scripts/validate_content.py content.html --check-links

# Check accessibility
python scripts/validate_content.py content.html --check-a11y

# Check HTML validity
python scripts/validate_content.py content.html --check-html

# Check word count
python scripts/validate_content.py content.html --word-count
```

### Validate Entire Project

```bash
python scripts/validate_content.py project-folder/ --all
```

---

## Common Issues and Fixes

### HTML Issues

| Issue | Detection | Fix |
|-------|-----------|-----|
| Unclosed tag | `grep -n '<[^/]*[^>]$'` | Close the tag |
| Literal `\n` | `grep -n '\\n'` | Use `<br>` or `<p>` |
| Missing alt | `grep -n '<img[^>]*[^alt]>'` | Add `alt=""` |
| Empty href | `grep -n 'href=""'` | Add valid URL |

### Content Issues

| Issue | Detection | Fix |
|-------|-----------|-----|
| Placeholder text | Search "TODO", "FIXME", "{{" | Replace with content |
| Duplicate heading | Check H1 count | Ensure single H1 |
| Long paragraphs | > 200 words | Break into smaller paragraphs |
| Missing CTA | Check end of content | Add call-to-action |

### Accessibility Issues

| Issue | Detection | Fix |
|-------|-----------|-----|
| Low contrast | Contrast checker | Increase color difference |
| Skip heading level | H1 → H3 | Use H2 between |
| Meaningless link | "Click here" | Use descriptive text |
| Missing lang | `<html>` tag | Add `lang="en"` |

---

## Pre-Export Checklist

Before generating final output:

### For PDF Export

- [ ] Print preview checked
- [ ] Page breaks appropriate
- [ ] Colors display in print
- [ ] No content cut off
- [ ] Headers/footers correct

### For DOCX Export

- [ ] Styles map correctly
- [ ] Images embedded
- [ ] Tables render properly
- [ ] Links preserved
- [ ] Track changes clean

### For Web Deployment

- [ ] All assets in correct locations
- [ ] Relative paths used
- [ ] No hardcoded localhost URLs
- [ ] Meta tags complete
- [ ] Favicon present

---

## Quality Metrics

### Word Count Targets

| Content Type | Target | Max |
|--------------|--------|-----|
| Bluesky post | 150-250 chars | 300 chars |
| Newsletter | 500-2000 words | 3000 words |
| Blog post | 1000-1500 words | 3000 words |
| Journal article | 3000-6000 words | 10000 words |

### Readability Targets

| Audience | Grade Level | Flesch Score |
|----------|-------------|--------------|
| General public | 8th grade | 60-70 |
| Professional | 10-12th grade | 50-60 |
| Academic | Graduate | 30-50 |

### Performance Targets

| Metric | Target |
|--------|--------|
| Page load time | < 3 seconds |
| Image size | < 200KB each |
| Total page size | < 1MB |
| First contentful paint | < 1.5 seconds |

---

## Validation Report Template

```markdown
# Content Validation Report

**File:** {{filename}}
**Type:** {{content_type}}
**Date:** {{date}}

## Summary

| Category | Status | Issues |
|----------|--------|--------|
| Structure | ✓/✗ | {{count}} |
| Technical | ✓/✗ | {{count}} |
| Content | ✓/✗ | {{count}} |
| Accessibility | ✓/✗ | {{count}} |

## Details

### Issues Found

1. **{{issue_title}}**
   - Location: Line {{line}}
   - Severity: {{severity}}
   - Fix: {{fix_description}}

### Passed Checks

- {{passed_check_1}}
- {{passed_check_2}}

## Recommendations

{{recommendations}}

---

**Overall Status:** {{PASS/FAIL}}
```

---

## Automated Checks

The validation script performs these automated checks:

```
Structure Checks:
├── Title present
├── Required sections exist
├── Heading hierarchy valid
└── No empty sections

Technical Checks:
├── HTML validity
├── No escape sequences
├── Images have alt text
├── Links are valid
└── Controls present

Content Checks:
├── Word count in range
├── No placeholder text
├── Metadata complete
└── Citations formatted (academic)

Accessibility Checks:
├── Color contrast
├── Heading levels
├── Link text quality
└── ARIA labels where needed
```

---

*End of Validation Reference*
