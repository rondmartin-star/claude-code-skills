# Accessibility Audit

**Purpose:** WCAG 2.1 AA accessibility compliance validation

**Size:** 14.6 KB

---

## Quick Start

```javascript
// Run accessibility audit
const issues = await runAudit('accessibility', projectConfig);

// Check specific areas
const semanticIssues = checkSemanticHTML(ast);
const contrastIssues = await checkColorContrast(styles);
const ariaIssues = checkARIA(ast);
```

## What It Does

- Validates semantic HTML
- Checks ARIA attributes
- Analyzes color contrast ratios
- Verifies keyboard navigation
- Validates images and media
- Checks form accessibility
- Monitors focus management

## When to Use

✅ WCAG compliance required
✅ Accessibility review
✅ Part of user methodology

❌ Performance issues (use performance audit)
❌ Content quality (use content audit)

## WCAG Levels

- AA: 4.5:1 contrast (normal text)
- AA: 3:1 contrast (large text)  
- AAA: 7:1 contrast (normal text)

---

**Part of:** v4.0.0 Universal Skills  
**Category:** User Methodology  
**Auto-fix:** Alt attributes, ARIA attributes
