---
name: consistency
description: >
  Validate framework terminology consistency across artifacts. Scans for term usage,
  detects variants/mismatches, checks definitions against canonical source. Use when:
  validating framework alignment, pre-release checks, or part of technical methodology.
---

# Consistency Audit

**Purpose:** Validate framework terminology consistency
**Size:** ~14 KB
**Type:** Audit Type (Part of Technical Methodology)

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Audit consistency"
- "Check framework terms"
- "Validate terminology"
- "Find inconsistencies"

**Context Indicators:**
- Part of convergence (technical methodology)
- Framework term alignment needed
- Pre-release validation
- Cross-document consistency check

---

## Audit Checks

### 1. Framework Term Usage

**Check:** All framework terms used correctly and consistently

**Method:**
1. Load framework categories from corpus-config.json
2. Scan artifacts for term usage
3. Detect variants and misspellings
4. Validate against canonical definitions

**Example Issue:**
```json
{
  "severity": "warning",
  "category": "term_variant",
  "location": "docs/guide.md:42",
  "canonical_term": "OAuth 2.0 with cookie separation",
  "found_term": "OAuth 2",
  "message": "Non-canonical term variant used"
}
```

### 2. Definition Conflicts

**Check:** Term definitions match canonical source

**Method:**
1. Identify term definitions in content
2. Compare with canonical source artifact
3. Flag conflicts

**Example Issue:**
```json
{
  "severity": "critical",
  "category": "definition_conflict",
  "location": "docs/security.md:15",
  "term": "CSRF token validation",
  "canonical_source": "requirements/security.md",
  "message": "Definition differs from canonical source",
  "expected": "CSRF token validation ensures...",
  "actual": "CSRF protection means..."
}
```

### 3. Unknown Terms

**Check:** Terms referenced but not in framework

**Method:**
1. Extract potential framework references
2. Check against framework.categories
3. Flag unknown terms

**Example Issue:**
```json
{
  "severity": "info",
  "category": "unknown_term",
  "location": "docs/api.md:28",
  "found_term": "JWT authentication",
  "message": "Term not in framework configuration",
  "suggestion": "Add to framework.categories if this is a framework term"
}
```

### 4. Cross-Document Consistency

**Check:** Same terms used consistently across documents

**Method:**
1. Build term usage index across all artifacts
2. Detect inconsistent usage patterns
3. Flag documents with variant usage

**Example Issue:**
```json
{
  "severity": "warning",
  "category": "inconsistent_usage",
  "term": "Parameterized queries",
  "usage_patterns": {
    "src/api/users.js": "parameterized queries",
    "docs/security.md": "prepared statements",
    "docs/api.md": "Parameterized queries"
  },
  "message": "Term used inconsistently across documents"
}
```

---

## Configuration

### corpus-config.json

```json
{
  "framework": {
    "categories": [
      {
        "id": "security-concepts",
        "label": "Security Concepts",
        "terms": [
          "OAuth 2.0 with cookie separation",
          "Parameterized queries",
          "CSRF token validation"
        ],
        "canonicalSource": "requirements",
        "matchMode": "word-boundary"
      }
    ]
  },
  "consistency": {
    "enabled": true,
    "scanDirectories": ["src/", "docs/"],
    "severity_threshold": "warning",
    "check_framework_terms": true
  },
  "audit": {
    "convergence": {
      "methodologies": [
        {
          "name": "technical",
          "audits": [
            {
              "id": "consistency",
              "config": {
                "canonical_source": "corpus-config.json",
                "scan_directories": ["src/", "docs/"],
                "severity_threshold": "warning"
              }
            }
          ]
        }
      ]
    }
  }
}
```

### Match Modes

**word-boundary:** Match whole words only
```
✓ "OAuth 2.0" matches "Using OAuth 2.0 for auth"
✗ "OAuth 2.0" doesn't match "MyOAuth2App"
```

**case-insensitive:** Ignore case
```
✓ "oauth 2.0" matches "OAuth 2.0"
✓ "OAuth 2.0" matches "OAUTH 2.0"
```

**exact:** Exact string match
```
✓ "OAuth 2.0" matches "OAuth 2.0"
✗ "OAuth 2.0" doesn't match "oauth 2.0"
```

---

## Detection Algorithm

### Step 1: Load Framework Configuration

```javascript
async function loadFrameworkTerms(projectPath) {
  const config = await loadCorpusConfig(projectPath);

  if (!config.framework?.categories) {
    return {
      categories: [],
      termsIndex: new Map()
    };
  }

  // Build term index
  const termsIndex = new Map();

  config.framework.categories.forEach(category => {
    category.terms.forEach(term => {
      termsIndex.set(term.toLowerCase(), {
        canonical: term,
        category: category.id,
        canonicalSource: category.canonicalSource,
        matchMode: category.matchMode || 'word-boundary'
      });
    });
  });

  return {
    categories: config.framework.categories,
    termsIndex
  };
}
```

### Step 2: Scan Artifacts

```javascript
async function scanArtifacts(projectPath, scanDirs) {
  const termUsage = new Map(); // term → [{file, line, context}]

  for (const dir of scanDirs) {
    const files = await findFiles(path.join(projectPath, dir));

    for (const file of files) {
      const content = await fs.readFile(file, 'utf8');
      const usages = extractTermUsage(content, file);

      usages.forEach(usage => {
        if (!termUsage.has(usage.term)) {
          termUsage.set(usage.term, []);
        }
        termUsage.get(usage.term).push(usage);
      });
    }
  }

  return termUsage;
}
```

### Step 3: Extract Term Usage

```javascript
function extractTermUsage(content, filePath) {
  const usages = [];
  const lines = content.split('\n');

  framework.termsIndex.forEach((termInfo, termLower) => {
    const { canonical, matchMode } = termInfo;

    let pattern;

    switch (matchMode) {
      case 'word-boundary':
        pattern = new RegExp(`\\b${escapeRegex(canonical)}\\b`, 'gi');
        break;
      case 'case-insensitive':
        pattern = new RegExp(escapeRegex(canonical), 'gi');
        break;
      case 'exact':
        pattern = new RegExp(escapeRegex(canonical), 'g');
        break;
    }

    lines.forEach((line, idx) => {
      const matches = line.matchAll(pattern);

      for (const match of matches) {
        usages.push({
          term: canonical,
          found: match[0],
          file: filePath,
          line: idx + 1,
          context: line.trim(),
          isExact: match[0] === canonical
        });
      }
    });
  });

  return usages;
}
```

### Step 4: Detect Issues

```javascript
async function detectConsistencyIssues(termUsage, framework) {
  const issues = [];

  // Check for term variants
  termUsage.forEach((usages, term) => {
    const variants = new Set();

    usages.forEach(usage => {
      if (usage.found !== usage.term) {
        variants.add(usage.found);
      }
    });

    if (variants.size > 0) {
      variants.forEach(variant => {
        const locations = usages
          .filter(u => u.found === variant)
          .map(u => `${u.file}:${u.line}`);

        issues.push({
          severity: 'warning',
          category: 'term_variant',
          term: term,
          variant: variant,
          locations,
          message: `Non-canonical variant "${variant}" used (canonical: "${term}")`
        });
      });
    }
  });

  // Check for unknown terms
  const unknownTerms = await detectUnknownTerms(termUsage, framework);
  issues.push(...unknownTerms);

  // Check for definition conflicts
  const conflicts = await detectDefinitionConflicts(termUsage, framework);
  issues.push(...conflicts);

  return issues;
}
```

### Step 5: Check Canonical Definitions

```javascript
async function detectDefinitionConflicts(termUsage, framework) {
  const issues = [];

  for (const category of framework.categories) {
    if (!category.canonicalSource) continue;

    const canonicalArtifact = await loadCanonicalSource(category.canonicalSource);

    for (const term of category.terms) {
      const canonicalDef = extractDefinition(canonicalArtifact, term);

      if (!canonicalDef) {
        issues.push({
          severity: 'warning',
          category: 'missing_canonical_definition',
          term,
          canonicalSource: category.canonicalSource,
          message: `Term "${term}" not found in canonical source`
        });
        continue;
      }

      // Check other artifacts for conflicting definitions
      const usages = termUsage.get(term) || [];

      for (const usage of usages) {
        const def = extractDefinition(usage.file, term);

        if (def && def !== canonicalDef) {
          issues.push({
            severity: 'critical',
            category: 'definition_conflict',
            location: `${usage.file}:${usage.line}`,
            term,
            canonicalSource: category.canonicalSource,
            expected: canonicalDef,
            actual: def,
            message: `Definition differs from canonical source`
          });
        }
      }
    }
  }

  return issues;
}
```

---

## Auto-Fix Capabilities

### ✓ Fully Automatic

**Term Variants:**
```
Issue: "oauth 2.0" instead of "OAuth 2.0"
Fix: Replace with canonical term
Strategy: Simple string replacement with canonical term
```

### ⚠ User Approval Required

**Definition Conflicts:**
```
Issue: Definition differs from canonical
Fix Options:
  1. Use canonical definition
  2. Update canonical source
  3. Mark as intentional variation
Strategy: Show diff, let user decide
```

### ✗ Manual Only

**Unknown Terms:**
```
Issue: Term not in framework
Fix: Requires deciding if term should be in framework
Strategy: Report, let user add to framework.categories if needed
```

---

## Integration with Technical Methodology

Consistency audit is part of the **technical methodology** in 3-3-1 convergence:

```json
{
  "audit": {
    "convergence": {
      "methodologies": [
        {
          "name": "technical",
          "description": "How it works",
          "audits": [
            "consistency",       // ← This audit
            "security",
            "quality"
          ]
        }
      ]
    }
  }
}
```

**Technical Perspective:**
- Are framework terms used correctly?
- Do definitions match canonical sources?
- Is terminology consistent across codebase?

---

## Output Format

```json
{
  "audit_type": "consistency",
  "timestamp": "2026-01-31T10:00:00Z",
  "project_path": "/path/to/project",
  "summary": {
    "framework_categories": 3,
    "total_terms": 15,
    "artifacts_scanned": 47,
    "term_usages": 234,
    "variants_found": 8,
    "definition_conflicts": 2,
    "unknown_terms": 3
  },
  "issues": [
    {
      "severity": "warning",
      "category": "term_variant",
      "term": "OAuth 2.0 with cookie separation",
      "variant": "OAuth 2",
      "locations": [
        "src/api/auth.js:42",
        "docs/security.md:15"
      ],
      "message": "Non-canonical variant used",
      "auto_fixable": true,
      "suggested_fix": "Replace with 'OAuth 2.0 with cookie separation'"
    }
  ]
}
```

---

## Quick Reference

**Run consistency audit:**
```javascript
const issues = await runAudit('consistency', projectConfig);
```

**Check specific term:**
```javascript
const usages = await findTermUsages(projectPath, 'OAuth 2.0');
```

**Validate framework:**
```javascript
const validation = await validateFramework(projectPath);
console.log(`Terms: ${validation.termCount}`);
console.log(`Issues: ${validation.issueCount}`);
```

---

*End of Consistency Audit*
*Part of v4.0.0 Universal Skills Ecosystem*
*Methodology: Technical (How it works)*
