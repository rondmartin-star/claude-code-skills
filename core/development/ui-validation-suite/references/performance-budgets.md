# Performance Budgets & Core Web Vitals

**Version:** 1.0.0
**Last Updated:** 2026-02-14

---

## Overview

Performance budgets enforce size limits and speed targets to ensure fast, responsive user experiences. Core Web Vitals measure real-world user experience metrics.

---

## Performance Budgets

### Bundle Size Budgets

| Resource | Budget | Rationale |
|----------|--------|-----------|
| **Total Bundle** | 500 KB | Load in <3s on 3G (1.6 Mbps) |
| **JavaScript** | 300 KB | Parse/execute time < 1s |
| **CSS** | 50 KB | Render-blocking critical path |
| **Images** | 200 KB | Initial viewport images |
| **Fonts** | 100 KB | Essential fonts only |

**Formula:**
```
Load Time (s) = Bundle Size (KB) / Network Speed (KBps)
3G speed: ~170 KBps
500 KB / 170 KBps ≈ 2.9s
```

---

### Per-Route Budgets

```json
{
  "routes": {
    "/": {
      "js": "250 KB",
      "css": "30 KB",
      "total": "400 KB"
    },
    "/dashboard": {
      "js": "350 KB",
      "css": "40 KB",
      "total": "500 KB"
    },
    "/settings": {
      "js": "200 KB",
      "css": "25 KB",
      "total": "300 KB"
    }
  }
}
```

---

## Bundle Size Analysis

### Rollup/Vite Plugin

```typescript
import { defineConfig } from 'vite';
import { analyzer } from 'rollup-plugin-analyzer';

export default defineConfig({
  build: {
    rollupOptions: {
      plugins: [
        analyzer({
          summaryOnly: true,
          limit: 10
        })
      ]
    }
  }
});
```

### Webpack Bundle Analyzer

```typescript
import { BundleAnalyzerPlugin } from 'webpack-bundle-analyzer';

module.exports = {
  plugins: [
    new BundleAnalyzerPlugin({
      analyzerMode: 'static',
      reportFilename: 'bundle-report.html',
      openAnalyzer: false,
      generateStatsFile: true
    })
  ]
};
```

---

### Bundle Analysis Script

```typescript
import fs from 'fs';
import path from 'path';

interface BundleStats {
  file: string;
  size: number;
  gzipSize: number;
  percentage: number;
}

async function analyzeBundleSize(distDir: string): Promise<BundleStats[]> {
  const files = fs.readdirSync(distDir);
  const stats: BundleStats[] = [];

  let totalSize = 0;

  for (const file of files) {
    const filePath = path.join(distDir, file);
    const stat = fs.statSync(filePath);

    if (stat.isFile() && /\.(js|css)$/.test(file)) {
      const size = stat.size;
      const gzipSize = await getGzipSize(filePath);

      totalSize += size;

      stats.push({
        file,
        size,
        gzipSize,
        percentage: 0 // Calculate after totalSize known
      });
    }
  }

  // Calculate percentages
  stats.forEach(s => {
    s.percentage = (s.size / totalSize) * 100;
  });

  return stats.sort((a, b) => b.size - a.size);
}
```

---

### Budget Validation

```typescript
interface BudgetConfig {
  total: number;
  js: number;
  css: number;
}

const DEFAULT_BUDGET: BudgetConfig = {
  total: 500 * 1024, // 500 KB
  js: 300 * 1024,    // 300 KB
  css: 50 * 1024     // 50 KB
};

async function validateBudget(
  distDir: string,
  budget: BudgetConfig = DEFAULT_BUDGET
): Promise<BudgetValidation> {
  const stats = await analyzeBundleSize(distDir);

  const jsSize = stats
    .filter(s => s.file.endsWith('.js'))
    .reduce((sum, s) => sum + s.size, 0);

  const cssSize = stats
    .filter(s => s.file.endsWith('.css'))
    .reduce((sum, s) => sum + s.size, 0);

  const totalSize = jsSize + cssSize;

  return {
    totalSize,
    jsSize,
    cssSize,
    totalExceeded: totalSize > budget.total,
    jsExceeded: jsSize > budget.js,
    cssExceeded: cssSize > budget.css,
    recommendations: generateBudgetRecommendations(totalSize, jsSize, cssSize, budget)
  };
}
```

---

## Core Web Vitals

### Three Key Metrics

| Metric | Good | Needs Improvement | Poor | Weight |
|--------|------|-------------------|------|--------|
| **LCP** | ≤2.5s | 2.5-4.0s | >4.0s | 40% |
| **FID** | ≤100ms | 100-300ms | >300ms | 30% |
| **CLS** | ≤0.1 | 0.1-0.25 | >0.25 | 30% |

---

### 1. Largest Contentful Paint (LCP)

**Definition:** Time until largest content element is rendered

**Target:** ≤ 2.5 seconds

#### Measure LCP

```typescript
import lighthouse from 'lighthouse';

async function measureLCP(url: string): Promise<number> {
  const result = await lighthouse(url, {
    onlyCategories: ['performance']
  });

  return result.lhr.audits['largest-contentful-paint'].numericValue;
}
```

#### Improve LCP

1. **Optimize server response time (TTFB)**
   ```nginx
   # Enable HTTP/2
   listen 443 ssl http2;

   # Enable compression
   gzip on;
   gzip_types text/plain text/css application/json application/javascript;
   ```

2. **Preload critical resources**
   ```svelte
   <svelte:head>
     <link rel="preload" href="/fonts/Inter.woff2" as="font" type="font/woff2" crossorigin />
     <link rel="preload" href="/critical.css" as="style" />
   </svelte:head>
   ```

3. **Optimize images**
   ```svelte
   <!-- Use modern formats -->
   <picture>
     <source srcset="hero.avif" type="image/avif" />
     <source srcset="hero.webp" type="image/webp" />
     <img src="hero.jpg" alt="Hero image" loading="eager" />
   </picture>

   <!-- Size attributes prevent layout shift -->
   <img src="image.jpg" width="800" height="600" alt="..." />
   ```

---

### 2. First Input Delay (FID)

**Definition:** Time from first user interaction to browser response

**Target:** ≤ 100 milliseconds

#### Measure FID

```typescript
async function measureFID(url: string): Promise<number> {
  const result = await lighthouse(url, {
    onlyCategories: ['performance']
  });

  return result.lhr.audits['max-potential-fid'].numericValue;
}
```

#### Improve FID

1. **Code splitting**
   ```typescript
   // SvelteKit automatic code splitting
   const Dashboard = () => import('./Dashboard.svelte');

   // Vite manual chunks
   export default defineConfig({
     build: {
       rollupOptions: {
         output: {
           manualChunks: {
             vendor: ['svelte', 'svelte/store'],
             utils: ['./src/lib/utils']
           }
         }
       }
     }
   });
   ```

2. **Defer non-critical JavaScript**
   ```svelte
   <svelte:head>
     <script src="/critical.js"></script>
     <script src="/analytics.js" defer></script>
     <script src="/chat-widget.js" async></script>
   </svelte:head>
   ```

3. **Reduce main thread work**
   ```typescript
   // ❌ Bad: Blocks main thread
   function processLargeArray(data) {
     return data.map(item => expensiveOperation(item));
   }

   // ✅ Good: Use Web Worker
   const worker = new Worker('/worker.js');
   worker.postMessage(data);
   worker.onmessage = (e) => {
     const results = e.data;
   };
   ```

---

### 3. Cumulative Layout Shift (CLS)

**Definition:** Sum of all unexpected layout shifts

**Target:** ≤ 0.1

#### Measure CLS

```typescript
async function measureCLS(url: string): Promise<number> {
  const result = await lighthouse(url, {
    onlyCategories: ['performance']
  });

  return result.lhr.audits['cumulative-layout-shift'].numericValue;
}
```

#### Improve CLS

1. **Set image dimensions**
   ```svelte
   <!-- ❌ Bad: No dimensions -->
   <img src="image.jpg" alt="..." />

   <!-- ✅ Good: Explicit dimensions -->
   <img src="image.jpg" width="800" height="600" alt="..." />

   <!-- ✅ Good: Aspect ratio in CSS -->
   <img src="image.jpg" alt="..." style="aspect-ratio: 16/9" />
   ```

2. **Reserve space for dynamic content**
   ```svelte
   <script>
     let ads = [];
     onMount(async () => {
       ads = await fetchAds();
     });
   </script>

   <!-- ✅ Reserve 300px height for ad -->
   <div class="ad-container" style="min-height: 300px;">
     {#if ads.length > 0}
       <Ad data={ads[0]} />
     {:else}
       <div class="skeleton" style="height: 300px;"></div>
     {/if}
   </div>
   ```

3. **Avoid inserting content above existing content**
   ```svelte
   <!-- ❌ Bad: Pushes content down -->
   <script>
     let banner = null;
     onMount(async () => {
       banner = await fetchBanner(); // Causes layout shift
     });
   </script>

   {#if banner}
     <Banner data={banner} />
   {/if}
   <main>Content</main>

   <!-- ✅ Good: Fixed position or bottom insertion -->
   <main>Content</main>
   {#if banner}
     <Banner data={banner} style="position: fixed; top: 0;" />
   {/if}
   ```

4. **Use font-display: swap**
   ```css
   @font-face {
     font-family: 'Inter';
     src: url('/fonts/Inter.woff2') format('woff2');
     font-display: swap; /* Prevent invisible text */
   }
   ```

---

## Real User Monitoring (RUM)

### web-vitals Library

```typescript
import { getCLS, getFID, getLCP } from 'web-vitals';

function sendToAnalytics(metric) {
  const body = JSON.stringify(metric);
  const url = '/analytics';

  // Use `navigator.sendBeacon()` if available, falling back to `fetch()`
  if (navigator.sendBeacon) {
    navigator.sendBeacon(url, body);
  } else {
    fetch(url, { body, method: 'POST', keepalive: true });
  }
}

getCLS(sendToAnalytics);
getFID(sendToAnalytics);
getLCP(sendToAnalytics);
```

---

## Lighthouse CI Integration

### GitHub Actions

```yaml
name: Lighthouse CI

on: [push, pull_request]

jobs:
  lhci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm run build
      - name: Run Lighthouse CI
        run: |
          npm install -g @lhci/cli
          lhci autorun
        env:
          LHCI_GITHUB_APP_TOKEN: ${{ secrets.LHCI_GITHUB_APP_TOKEN }}
```

### lighthouserc.js

```javascript
module.exports = {
  ci: {
    collect: {
      startServerCommand: 'npm run preview',
      url: ['http://localhost:4173/'],
      numberOfRuns: 3
    },
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'categories:accessibility': ['error', { minScore: 0.9 }],
        'first-contentful-paint': ['error', { maxNumericValue: 2000 }],
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
        'total-blocking-time': ['error', { maxNumericValue: 300 }]
      }
    },
    upload: {
      target: 'temporary-public-storage'
    }
  }
};
```

---

## Optimization Strategies

### 1. Code Splitting

```typescript
// Route-based splitting (SvelteKit automatic)
const routes = {
  '/': () => import('./routes/index.svelte'),
  '/about': () => import('./routes/about.svelte'),
  '/contact': () => import('./routes/contact.svelte')
};

// Component-based splitting
<script>
  import { onMount } from 'svelte';

  let HeavyComponent;

  onMount(async () => {
    HeavyComponent = (await import('./HeavyComponent.svelte')).default;
  });
</script>

{#if HeavyComponent}
  <svelte:component this={HeavyComponent} />
{/if}
```

---

### 2. Tree Shaking

```typescript
// ❌ Bad: Imports entire library
import _ from 'lodash';
const result = _.chunk(array, 2);

// ✅ Good: Import only what you need
import chunk from 'lodash/chunk';
const result = chunk(array, 2);

// ✅ Better: Use native methods
const result = array.reduce((acc, _, i) =>
  i % 2 ? acc : [...acc, array.slice(i, i + 2)],
  []
);
```

---

### 3. Lazy Loading

```svelte
<!-- Images -->
<img src="image.jpg" loading="lazy" alt="..." />

<!-- Components -->
<script>
  import { onMount, onDestroy } from 'svelte';

  let observer;
  let component;
  let isVisible = false;

  onMount(() => {
    observer = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting) {
        isVisible = true;
        import('./HeavyComponent.svelte').then(m => component = m.default);
        observer.disconnect();
      }
    });
    observer.observe(element);
  });

  onDestroy(() => observer?.disconnect());
</script>

<div bind:this={element}>
  {#if isVisible && component}
    <svelte:component this={component} />
  {/if}
</div>
```

---

### 4. Compression

```nginx
# Enable Gzip
gzip on;
gzip_comp_level 6;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

# Enable Brotli (better than Gzip)
brotli on;
brotli_comp_level 6;
brotli_types text/plain text/css application/json application/javascript text/xml application/xml;
```

---

## Performance Budget Report

```typescript
interface PerformanceReport {
  timestamp: string;
  bundle: {
    total: number;
    js: number;
    css: number;
    exceedsBudget: boolean;
  };
  coreWebVitals: {
    lcp: number;
    fid: number;
    cls: number;
    score: number;
  };
  lighthouse: {
    performance: number;
    accessibility: number;
    bestPractices: number;
    seo: number;
  };
  recommendations: string[];
}

async function generatePerformanceReport(url: string): Promise<PerformanceReport> {
  const [bundleStats, coreWebVitals, lighthouseResult] = await Promise.all([
    analyzeBundleSize('./dist'),
    measureCoreWebVitals(url),
    lighthouse(url)
  ]);

  return {
    timestamp: new Date().toISOString(),
    bundle: bundleStats,
    coreWebVitals,
    lighthouse: {
      performance: lighthouseResult.lhr.categories.performance.score * 100,
      accessibility: lighthouseResult.lhr.categories.accessibility.score * 100,
      bestPractices: lighthouseResult.lhr.categories['best-practices'].score * 100,
      seo: lighthouseResult.lhr.categories.seo.score * 100
    },
    recommendations: generateRecommendations(bundleStats, coreWebVitals, lighthouseResult)
  };
}
```

---

*End of Performance Budgets Reference*
