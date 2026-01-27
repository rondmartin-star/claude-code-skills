# Website Content Reference

**Output Types:** Multi-page websites, landing pages, single-page sites  
**Load when:** User mentions website, web pages, landing page, homepage, or site architecture

---

## Website Architecture

### Small Files, Linked Together

For efficient revisioning, websites use linked architecture:

```
website/
├── index.html              # Homepage/entry
├── pages/
│   ├── about.html
│   ├── services.html
│   ├── contact.html
│   └── blog/
│       ├── index.html      # Blog listing
│       ├── post-001.html
│       └── post-002.html
├── components/
│   ├── header.html         # Shared header
│   ├── footer.html         # Shared footer
│   └── nav.html            # Navigation
├── assets/
│   ├── css/
│   │   ├── main.css        # Shared styles
│   │   └── pages/          # Page-specific styles
│   ├── js/
│   │   ├── main.js
│   │   └── components/
│   └── images/
├── metadata.json           # Site configuration
└── sitemap.xml             # For SEO
```

### Benefits of Linked Architecture

| Benefit | How |
|---------|-----|
| Efficient revision | Change one file without regenerating all |
| Git-friendly | Clear change history per file |
| Modular reuse | Components shared across pages |
| Fast loading | Only load what's needed |
| Easy maintenance | Find and fix issues quickly |

---

## Base Page Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{{meta_description}}">
  <meta name="keywords" content="{{keywords}}">
  
  <!-- Open Graph -->
  <meta property="og:title" content="{{title}}">
  <meta property="og:description" content="{{og_description}}">
  <meta property="og:image" content="{{og_image}}">
  <meta property="og:url" content="{{canonical_url}}">
  
  <title>{{page_title}} | {{site_name}}</title>
  
  <link rel="canonical" href="{{canonical_url}}">
  <link rel="stylesheet" href="/assets/css/main.css">
  <link rel="stylesheet" href="/assets/css/pages/{{page_id}}.css">
</head>
<body data-page="{{page_id}}">
  <!-- Development Controls -->
  <div class="dev-controls" id="dev-controls">
    <button onclick="toggleView()">View</button>
    <button onclick="window.print()">Print</button>
    <button onclick="generatePDF()">PDF</button>
    <button onclick="openEditor()">Edit</button>
    <span class="page-info">{{page_id}}</span>
  </div>

  <!-- Include Header -->
  <div data-include="components/header.html"></div>
  
  <main id="main-content" data-line="1">
    {{content}}
  </main>
  
  <!-- Include Footer -->
  <div data-include="components/footer.html"></div>
  
  <script src="/assets/js/main.js"></script>
  <script>
    // Include component loader
    document.querySelectorAll('[data-include]').forEach(async (el) => {
      const path = el.dataset.include;
      const response = await fetch(path);
      const html = await response.text();
      el.innerHTML = html;
    });

    // Dev controls
    function toggleView() {
      const main = document.getElementById('main-content');
      if (main.dataset.viewMode === 'source') {
        main.innerHTML = main.dataset.rendered;
        main.dataset.viewMode = 'rendered';
      } else {
        main.dataset.rendered = main.innerHTML;
        main.innerHTML = '<pre style="white-space: pre-wrap">' + 
          main.innerHTML.replace(/</g, '&lt;') + '</pre>';
        main.dataset.viewMode = 'source';
      }
    }

    function generatePDF() {
      document.getElementById('dev-controls').style.display = 'none';
      window.print();
      document.getElementById('dev-controls').style.display = 'flex';
    }

    function openEditor() {
      const line = window.lastEditLine || 1;
      const file = document.body.dataset.page + '.html';
      // Open in default editor at line (implementation varies)
      window.location.href = `vscode://file/${file}:${line}`;
    }

    // Track cursor position
    document.addEventListener('click', (e) => {
      const el = e.target.closest('[data-line]');
      if (el) window.lastEditLine = el.dataset.line;
    });
  </script>
</body>
</html>
```

---

## Shared Components

### Header Component

`components/header.html`:
```html
<header class="site-header">
  <div class="header-container">
    <a href="/" class="logo">
      <img src="/assets/images/logo.svg" alt="{{site_name}}">
    </a>
    
    <nav class="main-nav" aria-label="Main navigation">
      <ul>
        <li><a href="/" {{#if home}}class="active"{{/if}}>Home</a></li>
        <li><a href="/pages/about.html" {{#if about}}class="active"{{/if}}>About</a></li>
        <li><a href="/pages/services.html" {{#if services}}class="active"{{/if}}>Services</a></li>
        <li><a href="/pages/blog/" {{#if blog}}class="active"{{/if}}>Blog</a></li>
        <li><a href="/pages/contact.html" {{#if contact}}class="active"{{/if}}>Contact</a></li>
      </ul>
    </nav>
    
    <button class="mobile-menu-toggle" aria-label="Toggle menu">
      <span></span>
      <span></span>
      <span></span>
    </button>
  </div>
</header>
```

### Footer Component

`components/footer.html`:
```html
<footer class="site-footer">
  <div class="footer-container">
    <div class="footer-brand">
      <img src="/assets/images/logo.svg" alt="{{site_name}}">
      <p>{{tagline}}</p>
    </div>
    
    <nav class="footer-nav">
      <h3>Quick Links</h3>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/pages/about.html">About</a></li>
        <li><a href="/pages/services.html">Services</a></li>
        <li><a href="/pages/contact.html">Contact</a></li>
      </ul>
    </nav>
    
    <div class="footer-contact">
      <h3>Contact</h3>
      <p>{{email}}</p>
      <p>{{phone}}</p>
      <p>{{address}}</p>
    </div>
    
    <div class="footer-social">
      <h3>Follow Us</h3>
      <a href="{{twitter_url}}" aria-label="Twitter">Twitter</a>
      <a href="{{linkedin_url}}" aria-label="LinkedIn">LinkedIn</a>
    </div>
  </div>
  
  <div class="footer-bottom">
    <p>&copy; {{year}} {{site_name}}. All rights reserved.</p>
    <nav>
      <a href="/pages/privacy.html">Privacy</a>
      <a href="/pages/terms.html">Terms</a>
    </nav>
  </div>
</footer>
```

---

## Page Type Templates

### Homepage

```html
<main id="main-content">
  <!-- Hero Section -->
  <section class="hero" data-line="1">
    <div class="hero-content">
      <h1>{{headline}}</h1>
      <p class="hero-subtitle">{{subheadline}}</p>
      <div class="hero-cta">
        <a href="{{primary_cta_url}}" class="btn btn-primary">{{primary_cta}}</a>
        <a href="{{secondary_cta_url}}" class="btn btn-secondary">{{secondary_cta}}</a>
      </div>
    </div>
    <div class="hero-media">
      <img src="{{hero_image}}" alt="{{hero_alt}}">
    </div>
  </section>

  <!-- Features Section -->
  <section class="features" data-line="20">
    <h2>{{features_headline}}</h2>
    <div class="features-grid">
      <!-- Feature cards -->
    </div>
  </section>

  <!-- Social Proof Section -->
  <section class="social-proof" data-line="40">
    <h2>Trusted By</h2>
    <div class="logo-strip">
      <!-- Partner/client logos -->
    </div>
  </section>

  <!-- CTA Section -->
  <section class="cta-section" data-line="60">
    <h2>{{cta_headline}}</h2>
    <p>{{cta_description}}</p>
    <a href="{{cta_url}}" class="btn btn-primary">{{cta_text}}</a>
  </section>
</main>
```

### About Page

```html
<main id="main-content">
  <section class="page-hero" data-line="1">
    <h1>About Us</h1>
    <p class="lead">{{about_tagline}}</p>
  </section>

  <section class="about-story" data-line="10">
    <h2>Our Story</h2>
    <div class="story-content">
      {{story_content}}
    </div>
  </section>

  <section class="about-mission" data-line="30">
    <h2>Our Mission</h2>
    <p>{{mission_statement}}</p>
  </section>

  <section class="about-team" data-line="40">
    <h2>Our Team</h2>
    <div class="team-grid">
      <!-- Team member cards -->
    </div>
  </section>

  <section class="about-values" data-line="60">
    <h2>Our Values</h2>
    <div class="values-list">
      <!-- Value items -->
    </div>
  </section>
</main>
```

### Services Page

```html
<main id="main-content">
  <section class="page-hero" data-line="1">
    <h1>Our Services</h1>
    <p class="lead">{{services_tagline}}</p>
  </section>

  <section class="services-overview" data-line="10">
    <div class="services-grid">
      <!-- Service cards with links to detail pages -->
    </div>
  </section>

  <section class="services-process" data-line="40">
    <h2>How We Work</h2>
    <div class="process-steps">
      <!-- Process step items -->
    </div>
  </section>

  <section class="services-cta" data-line="60">
    <h2>Ready to Get Started?</h2>
    <a href="/pages/contact.html" class="btn btn-primary">Contact Us</a>
  </section>
</main>
```

### Contact Page

```html
<main id="main-content">
  <section class="page-hero" data-line="1">
    <h1>Contact Us</h1>
    <p class="lead">{{contact_tagline}}</p>
  </section>

  <section class="contact-content" data-line="10">
    <div class="contact-info">
      <h2>Get in Touch</h2>
      <p><strong>Email:</strong> {{email}}</p>
      <p><strong>Phone:</strong> {{phone}}</p>
      <p><strong>Address:</strong> {{address}}</p>
    </div>
    
    <form class="contact-form" action="{{form_action}}" method="POST">
      <div class="form-group">
        <label for="name">Name</label>
        <input type="text" id="name" name="name" required>
      </div>
      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" name="email" required>
      </div>
      <div class="form-group">
        <label for="message">Message</label>
        <textarea id="message" name="message" rows="5" required></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Send Message</button>
    </form>
  </section>
</main>
```

---

## Blog Structure

### Blog Index

`pages/blog/index.html`:
```html
<main id="main-content">
  <section class="blog-header" data-line="1">
    <h1>Blog</h1>
    <p>Insights, updates, and ideas</p>
  </section>

  <section class="blog-posts" data-line="10">
    <!-- Post cards generated from posts -->
    <article class="post-card">
      <a href="post-001.html">
        <img src="{{post_image}}" alt="">
        <div class="post-card-content">
          <time>{{date}}</time>
          <h2>{{title}}</h2>
          <p>{{excerpt}}</p>
        </div>
      </a>
    </article>
  </section>

  <nav class="blog-pagination" data-line="50">
    <a href="?page=1" class="active">1</a>
    <a href="?page=2">2</a>
    <a href="?page=3">3</a>
  </nav>
</main>
```

### Blog Post

```html
<article class="blog-post" data-line="1">
  <header class="post-header">
    <time datetime="{{iso_date}}">{{formatted_date}}</time>
    <h1>{{title}}</h1>
    <p class="post-meta">By {{author}} · {{read_time}} min read</p>
  </header>

  <div class="post-content" data-line="10">
    {{content}}
  </div>

  <footer class="post-footer" data-line="100">
    <div class="post-tags">
      {{#each tags}}
      <a href="/pages/blog/?tag={{this}}">{{this}}</a>
      {{/each}}
    </div>
    
    <div class="post-share">
      <span>Share:</span>
      <a href="{{twitter_share}}">Twitter</a>
      <a href="{{linkedin_share}}">LinkedIn</a>
    </div>
  </footer>
</article>

<nav class="post-navigation">
  {{#if prev_post}}
  <a href="{{prev_post.url}}" class="prev">
    <span>Previous</span>
    <span>{{prev_post.title}}</span>
  </a>
  {{/if}}
  {{#if next_post}}
  <a href="{{next_post.url}}" class="next">
    <span>Next</span>
    <span>{{next_post.title}}</span>
  </a>
  {{/if}}
</nav>
```

---

## Metadata Configuration

`metadata.json`:
```json
{
  "site": {
    "name": "Site Name",
    "tagline": "Site tagline",
    "url": "https://example.com",
    "language": "en"
  },
  "contact": {
    "email": "hello@example.com",
    "phone": "+1 (555) 123-4567",
    "address": "123 Main St, City, State 12345"
  },
  "social": {
    "twitter": "https://twitter.com/handle",
    "linkedin": "https://linkedin.com/company/name",
    "github": "https://github.com/org"
  },
  "pages": [
    {"id": "home", "path": "/", "title": "Home"},
    {"id": "about", "path": "/pages/about.html", "title": "About"},
    {"id": "services", "path": "/pages/services.html", "title": "Services"},
    {"id": "blog", "path": "/pages/blog/", "title": "Blog"},
    {"id": "contact", "path": "/pages/contact.html", "title": "Contact"}
  ],
  "build": {
    "lastUpdated": "2026-01-24",
    "version": "1.0.0"
  }
}
```

---

## CSS Structure

### Main Stylesheet

`assets/css/main.css`:
```css
:root {
  --primary-color: #2563eb;
  --secondary-color: #1e40af;
  --accent-color: #3b82f6;
  --text-color: #1f2937;
  --text-light: #6b7280;
  --bg-color: #ffffff;
  --bg-light: #f9fafb;
  --border-color: #e5e7eb;
  --success: #10b981;
  --error: #ef4444;
  
  --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-serif: Georgia, 'Times New Roman', serif;
  --font-mono: 'SF Mono', Monaco, Consolas, monospace;
  
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 2rem;
  --spacing-xl: 4rem;
  
  --max-width: 1200px;
  --content-width: 800px;
}

/* Reset and base styles */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: var(--font-sans);
  line-height: 1.6;
  color: var(--text-color);
  background: var(--bg-color);
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
  line-height: 1.2;
  font-weight: 700;
}

/* Layout */
.container {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 var(--spacing-md);
}

/* Components imported from separate files */
@import 'components/header.css';
@import 'components/footer.css';
@import 'components/buttons.css';
@import 'components/forms.css';
@import 'components/cards.css';
```

---

## Validation Checklist

### Site-Wide

- [ ] All pages have valid HTML5
- [ ] All pages have meta descriptions
- [ ] All pages have Open Graph tags
- [ ] Navigation works on all pages
- [ ] Footer links correct
- [ ] Mobile responsive on all pages
- [ ] 404 page exists

### Page-Specific

- [ ] Title unique and descriptive
- [ ] H1 present and unique per page
- [ ] Images have alt text
- [ ] Links are not broken
- [ ] Forms submit correctly
- [ ] Page loads under 3 seconds

### SEO

- [ ] sitemap.xml generated
- [ ] robots.txt present
- [ ] Canonical URLs set
- [ ] Structured data (JSON-LD) where appropriate

---

## Build Commands

```bash
# Initialize new website
python scripts/init_content.py website my-website

# Validate all pages
python scripts/validate_content.py website/ --all

# Bundle for deployment
python scripts/bundle_content.py website/ --format deploy

# Generate sitemap
python scripts/bundle_content.py website/ --sitemap
```

---

*End of Website Content Reference*
