# SEO Audit

**Purpose:** Search engine optimization validation

**Size:** 15.1 KB

---

## Quick Start

```javascript
// Run SEO audit
const issues = await runAudit('seo', projectConfig);

// Check specific areas
const metaIssues = checkMetaTags(html);
const structuredData = checkStructuredData(html);
const sitemapIssues = await checkSitemap(sitemapUrl);
```

## What It Does

- Validates meta tags (title, description)
- Checks Open Graph and Twitter cards
- Validates structured data (JSON-LD)
- Analyzes sitemaps and robots.txt
- Reviews heading structure (H1 uniqueness)
- Checks internal linking
- Validates image alt text and filenames
- Verifies mobile-friendliness

## When to Use

✅ Pre-launch SEO review
✅ Search ranking concerns
✅ Part of user methodology (discoverability)

❌ Accessibility (use accessibility audit)
❌ Performance (use performance audit)

## Key Checks

- Title: 50-60 characters
- Description: 150-160 characters
- One H1 per page
- Structured data present
- Sitemap and robots.txt exist

---

**Part of:** v4.0.0 Universal Skills  
**Category:** User Methodology (Discoverability)  
**Auto-fix:** Viewport, canonical tags
