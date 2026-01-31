---
name: navigation
description: >
  Validate navigation structure and links. Checks for broken internal/external links,
  orphaned pages, circular loops, and navigation consistency. Use when: validating
  site structure, pre-release checks, or as part of holistic methodology audits.
---

# Navigation Audit

**Purpose:** Comprehensive navigation and link validation
**Size:** ~10 KB
**Type:** Audit Type (Part of Holistic Methodology)

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Audit navigation"
- "Check for broken links"
- "Validate site structure"
- "Find orphaned pages"
- "Check navigation paths"

**Context Indicators:**
- Part of convergence audit (holistic methodology)
- Pre-release navigation check
- Site restructuring validation
- Documentation completeness check

---

## Audit Checks

### 1. Broken Internal Links

**Check:** Links to pages within the project
**Method:** Resolve relative/absolute paths and verify files exist

**Common Issues:**
```
- Link to moved/renamed file
- Typo in path
- Case sensitivity mismatch
- Missing file extension
```

**Example Issues:**
```json
{
  "severity": "critical",
  "category": "broken_link",
  "location": "docs/api.md:42",
  "link": "/docs/auth.md",
  "status": "404",
  "message": "Link points to non-existent file"
}
```

### 2. Broken External Links

**Check:** Links to external websites
**Method:** HTTP HEAD request to verify URL is accessible

**Common Issues:**
```
- URL changed/moved
- Site down temporarily
- Invalid URL format
- HTTPS required but HTTP used
```

**Example Issues:**
```json
{
  "severity": "warning",
  "category": "broken_external_link",
  "location": "docs/resources.md:15",
  "link": "https://example.com/old-page",
  "status": "404",
  "message": "External link returns 404"
}
```

### 3. Orphaned Pages

**Check:** Pages not reachable from navigation
**Method:** Graph traversal from entry points

**Common Issues:**
```
- Page created but not linked
- Link removed but page remains
- Documentation section incomplete
- Outdated content not removed
```

**Example Issues:**
```json
{
  "severity": "warning",
  "category": "orphaned_page",
  "location": "docs/old-feature.md",
  "message": "Page exists but is unreachable from navigation",
  "reachable_from": []
}
```

### 4. Circular Navigation Loops

**Check:** Navigation paths that loop back
**Method:** Cycle detection in navigation graph

**Common Issues:**
```
- Breadcrumb loops
- Sidebar navigation circular refs
- Previous/next page loops
```

**Example Issues:**
```json
{
  "severity": "info",
  "category": "circular_loop",
  "path": ["index.md", "about.md", "team.md", "index.md"],
  "message": "Circular navigation detected",
  "loop_length": 3
}
```

### 5. Inconsistent Navigation Structure

**Check:** Navigation elements differ across pages
**Method:** Compare navigation structures

**Common Issues:**
```
- Menu items in different order
- Some pages missing menu items
- Inconsistent breadcrumbs
- Different sidebar structure
```

**Example Issues:**
```json
{
  "severity": "info",
  "category": "inconsistent_structure",
  "pages": ["docs/api.md", "docs/guides.md"],
  "message": "Navigation menu structure differs across pages"
}
```

### 6. Missing Breadcrumbs

**Check:** Pages without breadcrumb navigation
**Method:** Check for breadcrumb elements

**Example Issues:**
```json
{
  "severity": "info",
  "category": "missing_breadcrumb",
  "location": "docs/advanced/performance.md",
  "message": "Page missing breadcrumb navigation"
}
```

---

## Auto-Fix Capabilities

### ✓ Fully Automatic

**Broken Internal Links:**
```
Issue: /docs/auth.md → /docs/authentication.md
Fix: Update link to correct path
Strategy: Search for similar filenames, suggest correction
```

**Case Sensitivity:**
```
Issue: /Docs/API.md (should be /docs/api.md)
Fix: Correct case to match actual file
Strategy: Case-insensitive search, match actual filename
```

### ⚠ User Approval Required

**Broken External Links:**
```
Issue: https://example.com/old-page (404)
Fix Suggestion: Remove link or update to new URL
Strategy: Check if site has redirect, suggest alternative
```

**Orphaned Pages:**
```
Issue: docs/old-feature.md unreachable
Fix Options:
  1. Add link from appropriate parent page
  2. Delete if truly outdated
  3. Add to sitemap/index
Strategy: Analyze page content, suggest best parent
```

### ✗ Manual Only

**Circular Loops:**
```
Issue: Navigation loop detected
Fix: Requires design decision about navigation structure
Strategy: Report loop, let user decide how to break it
```

---

## Configuration

### corpus-config.json

```json
{
  "audit": {
    "navigation": {
      "enabled": true,
      "check_internal_links": true,
      "check_external_links": true,
      "check_orphaned_pages": true,
      "check_circular_loops": true,
      "check_breadcrumbs": false,

      "entry_points": [
        "README.md",
        "docs/index.md",
        "index.html"
      ],

      "ignore_patterns": [
        "node_modules/**",
        ".git/**",
        "dist/**"
      ],

      "external_link_timeout_ms": 5000,
      "external_link_follow_redirects": true,

      "severity_levels": {
        "broken_internal_link": "critical",
        "broken_external_link": "warning",
        "orphaned_page": "warning",
        "circular_loop": "info"
      }
    }
  }
}
```

---

## Usage Examples

### Example 1: Basic Navigation Audit

```javascript
const issues = await runNavigationAudit(projectPath);

console.log(`Found ${issues.length} navigation issues`);

issues.forEach(issue => {
  console.log(`[${issue.severity}] ${issue.location}`);
  console.log(`  ${issue.message}`);
});
```

### Example 2: Auto-Fix Broken Links

```javascript
const issues = await runNavigationAudit(projectPath);
const fixableIssues = issues.filter(i => i.auto_fixable);

console.log(`Found ${fixableIssues.length} auto-fixable issues`);

const plan = generateFixPlan(fixableIssues);
const results = await implementFixes(plan);

console.log(`Fixed ${results.successful}/${fixableIssues.length} issues`);
```

### Example 3: Generate Sitemap

```javascript
const graph = await buildNavigationGraph(projectPath);

// Find all reachable pages
const reachable = graph.getReachablePages();

// Find orphaned pages
const orphaned = graph.findOrphanedPages();

console.log(`Reachable pages: ${reachable.length}`);
console.log(`Orphaned pages: ${orphaned.length}`);

// Generate sitemap.xml
const sitemap = generateSitemap(reachable);
await writeSitemap(sitemap);
```

---

## Navigation Graph

### Building the Graph

```javascript
const graph = {
  nodes: new Map(),  // page path → node info
  edges: new Map()   // page path → array of linked pages
};

// 1. Scan all pages
for (const page of allPages) {
  graph.nodes.set(page.path, {
    path: page.path,
    title: page.title,
    type: page.type
  });
}

// 2. Extract links from each page
for (const page of allPages) {
  const links = extractLinks(page.content);
  graph.edges.set(page.path, links);
}

// 3. Analyze graph
const reachable = findReachablePages(graph, entryPoints);
const orphaned = findOrphanedPages(graph, reachable);
const loops = findCircularLoops(graph);
```

### Graph Analysis

**Reachability:**
```javascript
function findReachablePages(graph, entryPoints) {
  const reachable = new Set();
  const queue = [...entryPoints];

  while (queue.length > 0) {
    const current = queue.shift();
    if (reachable.has(current)) continue;

    reachable.add(current);

    const links = graph.edges.get(current) || [];
    queue.push(...links);
  }

  return Array.from(reachable);
}
```

**Orphan Detection:**
```javascript
function findOrphanedPages(graph, reachable) {
  const allPages = Array.from(graph.nodes.keys());
  return allPages.filter(page => !reachable.includes(page));
}
```

**Cycle Detection:**
```javascript
function findCircularLoops(graph) {
  const loops = [];
  const visited = new Set();
  const stack = [];

  function dfs(node) {
    if (stack.includes(node)) {
      // Found cycle
      const cycleStart = stack.indexOf(node);
      loops.push(stack.slice(cycleStart));
      return;
    }

    if (visited.has(node)) return;

    visited.add(node);
    stack.push(node);

    const links = graph.edges.get(node) || [];
    links.forEach(link => dfs(link));

    stack.pop();
  }

  graph.nodes.forEach((_, node) => dfs(node));
  return loops;
}
```

---

## Integration with Holistic Methodology

Navigation audit is typically part of the **holistic methodology** in 3-3-1 convergence:

```json
{
  "audit": {
    "convergence": {
      "methodologies": [
        {
          "name": "holistic",
          "description": "How it fits together",
          "audits": [
            "navigation",       // ← This audit
            "consistency",
            "documentation",
            "dependency"
          ]
        }
      ]
    }
  }
}
```

**Holistic Perspective:**
- Are all pages reachable?
- Is navigation structure consistent?
- Do users have clear paths to all content?
- Is documentation complete and linked?

---

## Performance Considerations

**Internal Link Checks:**
- Fast: File system lookups
- O(n) where n = number of links

**External Link Checks:**
- Slow: HTTP requests
- Can timeout or fail
- Use parallel requests with limit
- Cache results for repeated checks

**Optimization:**
```javascript
// Parallel external link checking with concurrency limit
const CONCURRENT_REQUESTS = 10;

async function checkExternalLinks(links) {
  const chunks = chunkArray(links, CONCURRENT_REQUESTS);
  const results = [];

  for (const chunk of chunks) {
    const chunkResults = await Promise.all(
      chunk.map(link => checkLink(link))
    );
    results.push(...chunkResults);
  }

  return results;
}
```

---

## Output Format

```json
{
  "audit_type": "navigation",
  "timestamp": "2026-01-31T10:00:00Z",
  "project_path": "/path/to/project",
  "summary": {
    "total_pages": 47,
    "total_links": 234,
    "internal_links": 198,
    "external_links": 36,
    "broken_internal": 3,
    "broken_external": 2,
    "orphaned_pages": 1,
    "circular_loops": 0
  },
  "issues": [
    {
      "severity": "critical",
      "category": "broken_link",
      "location": "docs/api.md:42",
      "link": "/docs/auth.md",
      "status": "404",
      "message": "Link points to non-existent file",
      "auto_fixable": true,
      "suggested_fix": "Update to /docs/authentication.md"
    }
  ]
}
```

---

## Quick Reference

**Run Navigation Audit:**
```javascript
const issues = await runAudit('navigation', projectConfig);
```

**Check Specific:**
```javascript
// Only check internal links
const issues = await checkInternalLinks(projectPath);

// Only find orphaned pages
const orphaned = await findOrphanedPages(projectPath);

// Only check for circular loops
const loops = await findCircularLoops(projectPath);
```

**Generate Reports:**
```javascript
const report = await generateNavigationReport(projectPath);
console.log(`Total pages: ${report.summary.total_pages}`);
console.log(`Broken links: ${report.summary.broken_internal}`);
console.log(`Orphaned: ${report.summary.orphaned_pages}`);
```

---

*End of Navigation Audit*
*Part of v4.0.0 Universal Skills Ecosystem*
*Methodology: Holistic (How it fits together)*
