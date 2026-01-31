---
name: seo
description: >
  SEO audit checking meta tags, structured data, sitemaps, heading structure, and
  discoverability. Validates search engine optimization. Use when: SEO review,
  pre-launch validation, or part of user methodology audits.
---

# SEO Audit

**Purpose:** Search engine optimization validation
**Type:** Audit Type (Part of User Methodology)

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Audit SEO"
- "Check meta tags"
- "Validate structured data"
- "Review search optimization"

**Context Indicators:**
- Pre-launch SEO review
- Part of convergence (user methodology)
- Search ranking concerns
- Discoverability optimization

---

## SEO Checks

### 1. Meta Tags

**Required Tags:**
- `<title>` (50-60 chars)
- `<meta name="description">` (150-160 chars)
- `<meta name="viewport">`
- `<link rel="canonical">`

**Detection:**
```javascript
function checkMetaTags(html) {
  const issues = [];
  const $ = cheerio.load(html);

  // Title tag
  const title = $('title').text();
  if (!title) {
    issues.push({
      type: 'missing_title',
      severity: 'critical',
      suggestion: 'Add <title> tag'
    });
  } else if (title.length < 30 || title.length > 60) {
    issues.push({
      type: 'title_length',
      length: title.length,
      optimal: '50-60 characters',
      severity: 'medium',
      suggestion: 'Adjust title length for optimal display'
    });
  }

  // Meta description
  const description = $('meta[name="description"]').attr('content');
  if (!description) {
    issues.push({
      type: 'missing_description',
      severity: 'critical',
      suggestion: 'Add meta description'
    });
  } else if (description.length < 120 || description.length > 160) {
    issues.push({
      type: 'description_length',
      length: description.length,
      optimal: '150-160 characters',
      severity: 'medium'
    });
  }

  // Viewport
  if (!$('meta[name="viewport"]').length) {
    issues.push({
      type: 'missing_viewport',
      severity: 'high',
      suggestion: 'Add viewport meta tag for mobile'
    });
  }

  // Canonical URL
  if (!$('link[rel="canonical"]').length) {
    issues.push({
      type: 'missing_canonical',
      severity: 'medium',
      suggestion: 'Add canonical URL to prevent duplicate content'
    });
  }

  return issues;
}
```

### 2. Open Graph & Social

**Facebook/LinkedIn (Open Graph):**
```javascript
function checkOpenGraph(html) {
  const issues = [];
  const $ = cheerio.load(html);

  const requiredOG = [
    'og:title',
    'og:description',
    'og:image',
    'og:url',
    'og:type'
  ];

  requiredOG.forEach(property => {
    if (!$(`meta[property="${property}"]`).length) {
      issues.push({
        type: 'missing_og_tag',
        property,
        severity: 'medium',
        suggestion: `Add ${property} meta tag`
      });
    }
  });

  // Image dimensions
  const ogImage = $('meta[property="og:image"]').attr('content');
  if (ogImage && !$('meta[property="og:image:width"]').length) {
    issues.push({
      type: 'missing_og_image_dimensions',
      severity: 'low',
      suggestion: 'Add og:image:width and og:image:height'
    });
  }

  return issues;
}
```

**Twitter Cards:**
```javascript
function checkTwitterCards(html) {
  const issues = [];
  const $ = cheerio.load(html);

  const requiredTwitter = [
    'twitter:card',
    'twitter:title',
    'twitter:description',
    'twitter:image'
  ];

  requiredTwitter.forEach(name => {
    if (!$(`meta[name="${name}"]`).length) {
      issues.push({
        type: 'missing_twitter_tag',
        name,
        severity: 'low',
        suggestion: `Add ${name} meta tag`
      });
    }
  });

  return issues;
}
```

### 3. Structured Data (JSON-LD)

**Schema.org Validation:**
```javascript
function checkStructuredData(html) {
  const issues = [];
  const $ = cheerio.load(html);

  const jsonLdScripts = $('script[type="application/ld+json"]');

  if (jsonLdScripts.length === 0) {
    issues.push({
      type: 'missing_structured_data',
      severity: 'medium',
      suggestion: 'Add JSON-LD structured data'
    });
    return issues;
  }

  jsonLdScripts.each((i, script) => {
    try {
      const data = JSON.parse($(script).html());

      // Validate required fields
      if (!data['@context']) {
        issues.push({
          type: 'missing_context',
          severity: 'high',
          suggestion: 'Add @context to structured data'
        });
      }

      if (!data['@type']) {
        issues.push({
          type: 'missing_type',
          severity: 'high',
          suggestion: 'Add @type to structured data'
        });
      }

      // Validate by type
      if (data['@type'] === 'Article') {
        validateArticle(data, issues);
      } else if (data['@type'] === 'Product') {
        validateProduct(data, issues);
      }

    } catch (e) {
      issues.push({
        type: 'invalid_json_ld',
        error: e.message,
        severity: 'critical'
      });
    }
  });

  return issues;
}

function validateArticle(data, issues) {
  const required = ['headline', 'author', 'datePublished', 'image'];

  required.forEach(field => {
    if (!data[field]) {
      issues.push({
        type: 'missing_article_field',
        field,
        severity: 'medium',
        suggestion: `Add ${field} to Article schema`
      });
    }
  });
}
```

### 4. Sitemaps & Robots

**Sitemap Validation:**
```javascript
async function checkSitemap(sitemapUrl) {
  const issues = [];

  try {
    const response = await fetch(sitemapUrl);

    if (response.status !== 200) {
      issues.push({
        type: 'sitemap_not_found',
        url: sitemapUrl,
        status: response.status,
        severity: 'high',
        suggestion: 'Create sitemap.xml'
      });
      return issues;
    }

    const xml = await response.text();
    const $ = cheerio.load(xml, { xmlMode: true });

    const urls = $('url');

    if (urls.length === 0) {
      issues.push({
        type: 'empty_sitemap',
        severity: 'high',
        suggestion: 'Add URLs to sitemap'
      });
    }

    // Check for required fields
    urls.each((i, url) => {
      const loc = $(url).find('loc').text();
      const lastmod = $(url).find('lastmod').text();

      if (!loc) {
        issues.push({
          type: 'sitemap_missing_loc',
          severity: 'high'
        });
      }

      if (!lastmod) {
        issues.push({
          type: 'sitemap_missing_lastmod',
          url: loc,
          severity: 'low',
          suggestion: 'Add <lastmod> to sitemap entries'
        });
      }
    });

  } catch (e) {
    issues.push({
      type: 'sitemap_error',
      error: e.message,
      severity: 'high'
    });
  }

  return issues;
}
```

**Robots.txt:**
```javascript
async function checkRobots(robotsUrl) {
  const issues = [];

  try {
    const response = await fetch(robotsUrl);

    if (response.status !== 200) {
      issues.push({
        type: 'robots_not_found',
        severity: 'medium',
        suggestion: 'Create robots.txt'
      });
      return issues;
    }

    const content = await response.text();

    // Check for sitemap reference
    if (!content.includes('Sitemap:')) {
      issues.push({
        type: 'robots_missing_sitemap',
        severity: 'low',
        suggestion: 'Add Sitemap reference to robots.txt'
      });
    }

    // Check for user-agent
    if (!content.includes('User-agent:')) {
      issues.push({
        type: 'robots_missing_user_agent',
        severity: 'medium',
        suggestion: 'Add User-agent directive'
      });
    }

  } catch (e) {
    issues.push({
      type: 'robots_error',
      error: e.message,
      severity: 'medium'
    });
  }

  return issues;
}
```

### 5. Heading Structure

**SEO Perspective:**
```javascript
function checkHeadingsSEO(html) {
  const issues = [];
  const $ = cheerio.load(html);

  // Only one H1
  const h1Count = $('h1').length;

  if (h1Count === 0) {
    issues.push({
      type: 'missing_h1',
      severity: 'critical',
      suggestion: 'Add exactly one H1 per page'
    });
  } else if (h1Count > 1) {
    issues.push({
      type: 'multiple_h1',
      count: h1Count,
      severity: 'high',
      suggestion: 'Use only one H1 per page'
    });
  }

  // H1 content
  const h1Text = $('h1').first().text().trim();
  if (h1Text.length < 20 || h1Text.length > 70) {
    issues.push({
      type: 'h1_length',
      length: h1Text.length,
      optimal: '20-70 characters',
      severity: 'low'
    });
  }

  return issues;
}
```

### 6. Internal Linking

**Link Analysis:**
```javascript
function checkInternalLinks(html, baseUrl) {
  const issues = [];
  const $ = cheerio.load(html);

  const links = $('a[href]');
  const internalLinks = [];

  links.each((i, link) => {
    const href = $(link).attr('href');

    if (isInternalLink(href, baseUrl)) {
      internalLinks.push(href);

      // Check for descriptive text
      const text = $(link).text().trim();

      if (!text || text.toLowerCase() === 'click here' || text.toLowerCase() === 'read more') {
        issues.push({
          type: 'non_descriptive_link',
          text,
          href,
          severity: 'low',
          suggestion: 'Use descriptive link text'
        });
      }

      // Check for nofollow on internal
      if ($(link).attr('rel')?.includes('nofollow')) {
        issues.push({
          type: 'nofollow_internal',
          href,
          severity: 'medium',
          suggestion: 'Remove nofollow from internal links'
        });
      }
    }
  });

  // Check for orphan pages
  if (internalLinks.length < 3) {
    issues.push({
      type: 'low_internal_links',
      count: internalLinks.length,
      severity: 'medium',
      suggestion: 'Add more internal links (3+ recommended)'
    });
  }

  return issues;
}
```

### 7. Image Optimization (SEO)

**Alt Text for SEO:**
```javascript
function checkImagesForSEO(html) {
  const issues = [];
  const $ = cheerio.load(html);

  $('img').each((i, img) => {
    const alt = $(img).attr('alt');
    const src = $(img).attr('src');

    // Missing alt
    if (!alt) {
      issues.push({
        type: 'missing_alt_seo',
        src,
        severity: 'high',
        suggestion: 'Add descriptive alt text for SEO'
      });
    }

    // Alt too short
    if (alt && alt.length < 5) {
      issues.push({
        type: 'alt_too_short',
        alt,
        src,
        severity: 'low',
        suggestion: 'Use more descriptive alt text'
      });
    }

    // Check file names
    if (src && /image\d+\.jpg|img\d+\.png/i.test(src)) {
      issues.push({
        type: 'non_descriptive_filename',
        src,
        severity: 'low',
        suggestion: 'Use descriptive file names'
      });
    }
  });

  return issues;
}
```

### 8. Mobile-Friendliness

**Mobile SEO Factors:**
```javascript
function checkMobileFriendly(html) {
  const issues = [];
  const $ = cheerio.load(html);

  // Viewport
  const viewport = $('meta[name="viewport"]').attr('content');
  if (!viewport || !viewport.includes('width=device-width')) {
    issues.push({
      type: 'not_mobile_friendly',
      severity: 'critical',
      suggestion: 'Add viewport meta tag with width=device-width'
    });
  }

  // Font sizes
  $('*').each((i, el) => {
    const fontSize = $(el).css('font-size');
    if (fontSize && parseInt(fontSize) < 12) {
      issues.push({
        type: 'font_too_small',
        element: el.tagName,
        fontSize,
        severity: 'medium',
        suggestion: 'Use minimum 12px font size'
      });
    }
  });

  // Touch targets
  $('button, a').each((i, el) => {
    const width = $(el).width();
    const height = $(el).height();

    if (width < 44 || height < 44) {
      issues.push({
        type: 'touch_target_too_small',
        element: el.tagName,
        size: `${width}x${height}`,
        severity: 'medium',
        suggestion: 'Use minimum 44x44px touch targets'
      });
    }
  });

  return issues;
}
```

---

## Configuration

### corpus-config.json

```json
{
  "audit": {
    "convergence": {
      "methodologies": [
        {
          "name": "user",
          "audits": [
            {
              "id": "seo",
              "config": {
                "check_meta_tags": true,
                "check_open_graph": true,
                "check_twitter_cards": true,
                "check_structured_data": true,
                "check_sitemap": true,
                "check_robots": true,
                "sitemap_url": "https://example.com/sitemap.xml",
                "robots_url": "https://example.com/robots.txt",
                "base_url": "https://example.com"
              }
            }
          ]
        }
      ]
    }
  }
}
```

---

## Auto-Fix Capabilities

### ✓ Fully Automatic

**Missing viewport:**
```
Issue: No viewport meta tag
Fix: Add <meta name="viewport" content="width=device-width, initial-scale=1">
Strategy: Standard viewport tag
```

**Missing canonical:**
```
Issue: No canonical URL
Fix: Add <link rel="canonical" href="current-url">
Strategy: Use current page URL
```

### ⚠ User Approval Required

**Title/description length:**
```
Issue: Title too long (75 chars)
Fix: Suggest shortened version
Strategy: Preserve meaning, reduce length
```

**Structured data:**
```
Issue: Missing Article schema
Fix: Generate basic JSON-LD structure
Strategy: User fills in specific content
```

### ✗ Manual Only

**Content optimization:**
```
Issue: Low keyword density
Fix: Requires content rewriting
Strategy: Provide SEO recommendations
```

**Link building:**
```
Issue: Low internal links
Fix: Requires editorial decisions
Strategy: Suggest related pages to link
```

---

## Output Format

```json
{
  "audit_type": "seo",
  "timestamp": "2026-01-31T10:00:00Z",
  "project_path": "/path/to/project",
  "summary": {
    "pages_scanned": 25,
    "meta_tag_issues": 8,
    "structured_data_issues": 3,
    "sitemap_issues": 1,
    "heading_issues": 5,
    "link_issues": 12
  },
  "issues": [
    {
      "severity": "critical",
      "category": "missing_title",
      "location": "pages/about.html",
      "suggestion": "Add <title> tag",
      "auto_fixable": true
    },
    {
      "severity": "medium",
      "category": "title_length",
      "location": "pages/products.html",
      "length": 75,
      "optimal": "50-60 characters",
      "auto_fixable": false
    }
  ]
}
```

---

## Integration with User Methodology

SEO audit is part of the **user methodology** (discoverability):

```json
{
  "methodologies": [
    {
      "name": "user",
      "description": "How it's experienced",
      "audits": [
        "seo",               // ← This audit
        "accessibility",
        "content"
      ]
    }
  ]
}
```

**User Perspective (Discoverability):**
- Can users find the content via search?
- Is content properly indexed?
- Are social shares optimized?
- Is mobile experience good for SEO?

---

*End of SEO Audit*
*Part of v4.0.0 Universal Skills Ecosystem*
*Methodology: User (Discoverability)*
*Search engine optimization validation*
