# Dependency Audit

**Purpose:** Dependency health and security validation

**Size:** 12.4 KB

---

## Quick Start

```javascript
// Run dependency audit
const issues = await runAudit('dependency', projectConfig);

// Check specific areas
const outdated = await checkOutdated('npm');
const vulnerabilities = await checkVulnerabilities('npm');
const licenses = await checkLicenses();
```

## What It Does

- Checks for outdated dependencies
- Scans for security vulnerabilities (CVE)
- Validates license compliance
- Detects version conflicts
- Finds unused dependencies
- Detects circular dependencies
- Analyzes dependency sizes

## When to Use

✅ Security review required
✅ Dependency updates needed
✅ Part of technical methodology

❌ Code quality (use quality audit)
❌ Application security (use security audit)

## Key Checks

- Security: CVE database + npm audit
- Licenses: MIT, ISC, Apache-2.0 allowed
- Size: Max 500KB per dependency
- Conflicts: Multiple versions detected

---

**Part of:** v4.0.0 Universal Skills  
**Category:** Technical Methodology  
**Auto-fix:** npm audit fix, remove unused
