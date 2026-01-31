---
name: dependency
description: >
  Dependency audit checking outdated packages, security vulnerabilities, license
  compliance, and dependency conflicts. Validates dependency health. Use when:
  security review, dependency updates, or part of technical methodology audits.
---

# Dependency Audit

**Purpose:** Dependency health and security validation
**Type:** Audit Type (Part of Technical Methodology)

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Audit dependencies"
- "Check for vulnerabilities"
- "Update dependencies"
- "Check licenses"

**Context Indicators:**
- Security review required
- Part of convergence (technical methodology)
- Dependency updates needed
- License compliance check

---

## Dependency Checks

### 1. Outdated Dependencies

**Check for updates:**
```javascript
async function checkOutdated(packageManager = 'npm') {
  const issues = [];

  const { stdout } = await exec(`${packageManager} outdated --json`);
  const outdated = JSON.parse(stdout);

  for (const [pkg, info] of Object.entries(outdated)) {
    const current = info.current;
    const latest = info.latest;
    const wanted = info.wanted;

    const severity = getSeverity(current, latest);

    issues.push({
      type: 'outdated_dependency',
      package: pkg,
      current,
      wanted,
      latest,
      severity,
      suggestion: `Update to ${latest}`
    });
  }

  return issues;
}

function getSeverity(current, latest) {
  const currentMajor = parseInt(current.split('.')[0]);
  const latestMajor = parseInt(latest.split('.')[0]);

  if (latestMajor > currentMajor + 1) return 'high';
  if (latestMajor > currentMajor) return 'medium';
  return 'low';
}
```

### 2. Security Vulnerabilities

**npm/yarn audit:**
```javascript
async function checkVulnerabilities(packageManager = 'npm') {
  const issues = [];

  const { stdout } = await exec(`${packageManager} audit --json`);
  const audit = JSON.parse(stdout);

  // npm audit format
  if (audit.vulnerabilities) {
    for (const [pkg, vuln] of Object.entries(audit.vulnerabilities)) {
      issues.push({
        type: 'security_vulnerability',
        package: pkg,
        severity: vuln.severity,
        via: vuln.via,
        range: vuln.range,
        fixAvailable: vuln.fixAvailable,
        suggestion: vuln.fixAvailable
          ? 'Run npm audit fix'
          : 'Update dependencies manually'
      });
    }
  }

  return issues;
}
```

**CVE Database Check:**
```javascript
async function checkCVE(dependencies) {
  const issues = [];

  for (const [pkg, version] of Object.entries(dependencies)) {
    const cves = await queryCVEDatabase(pkg, version);

    cves.forEach(cve => {
      issues.push({
        type: 'cve_found',
        package: pkg,
        version,
        cve: cve.id,
        severity: cve.severity,
        description: cve.description,
        suggestion: `Update to ${cve.fixedVersion || 'latest'}`
      });
    });
  }

  return issues;
}
```

### 3. License Compliance

**Check licenses:**
```javascript
async function checkLicenses(packageManager = 'npm') {
  const issues = [];

  // Get all dependencies with licenses
  const { stdout } = await exec('npm list --json --depth=0');
  const tree = JSON.parse(stdout);

  const allowedLicenses = [
    'MIT', 'ISC', 'Apache-2.0', 'BSD-2-Clause',
    'BSD-3-Clause', 'CC0-1.0', 'Unlicense'
  ];

  const deniedLicenses = [
    'GPL-3.0', 'AGPL-3.0', 'LGPL-3.0'
  ];

  const checkDep = (dep, name) => {
    const license = dep.license || 'UNKNOWN';

    if (license === 'UNKNOWN') {
      issues.push({
        type: 'unknown_license',
        package: name,
        severity: 'medium',
        suggestion: 'Verify license manually'
      });
    } else if (deniedLicenses.includes(license)) {
      issues.push({
        type: 'incompatible_license',
        package: name,
        license,
        severity: 'critical',
        suggestion: 'Remove or replace package'
      });
    } else if (!allowedLicenses.includes(license)) {
      issues.push({
        type: 'unverified_license',
        package: name,
        license,
        severity: 'low',
        suggestion: 'Review license compatibility'
      });
    }
  };

  Object.entries(tree.dependencies || {}).forEach(([name, dep]) => {
    checkDep(dep, name);
  });

  return issues;
}
```

### 4. Dependency Conflicts

**Version conflicts:**
```javascript
async function checkConflicts() {
  const issues = [];

  const { stdout } = await exec('npm list --json');
  const tree = JSON.parse(stdout);

  // Find duplicate packages with different versions
  const versions = new Map();

  const traverse = (deps, path = []) => {
    for (const [name, dep] of Object.entries(deps || {})) {
      const version = dep.version;

      if (!versions.has(name)) {
        versions.set(name, new Set());
      }
      versions.get(name).add(version);

      if (dep.dependencies) {
        traverse(dep.dependencies, [...path, name]);
      }
    }
  };

  traverse(tree.dependencies);

  // Report conflicts
  for (const [pkg, versionSet] of versions) {
    if (versionSet.size > 1) {
      issues.push({
        type: 'version_conflict',
        package: pkg,
        versions: Array.from(versionSet),
        severity: 'medium',
        suggestion: 'Resolve version conflicts with npm dedupe'
      });
    }
  }

  return issues;
}
```

### 5. Unused Dependencies

**Find unused:**
```javascript
async function checkUnused(projectPath) {
  const issues = [];

  const packageJson = JSON.parse(
    fs.readFileSync(path.join(projectPath, 'package.json'), 'utf8')
  );

  const declared = {
    ...packageJson.dependencies,
    ...packageJson.devDependencies
  };

  // Scan code for imports
  const files = await glob(`${projectPath}/src/**/*.{js,ts,jsx,tsx}`);
  const imported = new Set();

  for (const file of files) {
    const content = fs.readFileSync(file, 'utf8');
    const ast = parse(content);

    traverse(ast, {
      ImportDeclaration: (path) => {
        const source = path.node.source.value;

        // Extract package name
        const pkg = source.startsWith('@')
          ? source.split('/').slice(0, 2).join('/')
          : source.split('/')[0];

        imported.add(pkg);
      },
      CallExpression: (path) => {
        // Check for require()
        if (path.node.callee.name === 'require') {
          const arg = path.node.arguments[0];
          if (arg?.type === 'StringLiteral') {
            const pkg = arg.value.split('/')[0];
            imported.add(pkg);
          }
        }
      }
    });
  }

  // Find unused
  for (const pkg of Object.keys(declared)) {
    if (!imported.has(pkg)) {
      issues.push({
        type: 'unused_dependency',
        package: pkg,
        severity: 'low',
        suggestion: 'Remove from package.json'
      });
    }
  }

  return issues;
}
```

### 6. Circular Dependencies

**Detect circles:**
```javascript
function checkCircular(projectPath) {
  const issues = [];
  const graph = new Map();

  // Build dependency graph
  const files = glob.sync(`${projectPath}/src/**/*.{js,ts,jsx,tsx}`);

  files.forEach(file => {
    const imports = getImports(file);
    graph.set(file, imports);
  });

  // DFS to find cycles
  const visited = new Set();
  const recursionStack = new Set();

  const hasCycle = (node, path = []) => {
    visited.add(node);
    recursionStack.add(node);

    const neighbors = graph.get(node) || [];

    for (const neighbor of neighbors) {
      if (!visited.has(neighbor)) {
        if (hasCycle(neighbor, [...path, node])) {
          return true;
        }
      } else if (recursionStack.has(neighbor)) {
        // Found cycle
        issues.push({
          type: 'circular_dependency',
          cycle: [...path, node, neighbor],
          severity: 'high',
          suggestion: 'Refactor to break circular dependency'
        });
        return true;
      }
    }

    recursionStack.delete(node);
    return false;
  };

  for (const node of graph.keys()) {
    if (!visited.has(node)) {
      hasCycle(node);
    }
  }

  return issues;
}
```

### 7. Dependency Size

**Bundle impact:**
```javascript
async function checkDependencySize(projectPath) {
  const issues = [];

  const packageJson = JSON.parse(
    fs.readFileSync(path.join(projectPath, 'package.json'), 'utf8')
  );

  const deps = packageJson.dependencies || {};

  for (const [pkg, version] of Object.entries(deps)) {
    const size = await getPackageSize(pkg, version);

    if (size > 500 * 1024) {  // 500KB
      issues.push({
        type: 'large_dependency',
        package: pkg,
        size: (size / 1024).toFixed(2) + ' KB',
        severity: size > 1024 * 1024 ? 'high' : 'medium',
        suggestion: 'Consider lighter alternative or code splitting'
      });
    }
  }

  return issues;
}

async function getPackageSize(pkg, version) {
  // Query bundlephobia API
  const response = await fetch(
    `https://bundlephobia.com/api/size?package=${pkg}@${version}`
  );

  const data = await response.json();
  return data.gzip || data.size;
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
          "name": "technical",
          "audits": [
            {
              "id": "dependency",
              "config": {
                "check_outdated": true,
                "check_vulnerabilities": true,
                "check_licenses": true,
                "check_unused": true,
                "check_circular": true,
                "max_dependency_size_kb": 500,
                "allowed_licenses": [
                  "MIT", "ISC", "Apache-2.0",
                  "BSD-2-Clause", "BSD-3-Clause"
                ],
                "denied_licenses": [
                  "GPL-3.0", "AGPL-3.0", "LGPL-3.0"
                ],
                "package_manager": "npm"
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

**npm audit fix:**
```
Issue: Security vulnerability with auto-fix
Fix: Run npm audit fix
Strategy: Automated patch update
```

**Unused dependencies:**
```
Issue: Package never imported
Fix: Remove from package.json
Strategy: Safe removal
```

### ⚠ User Approval Required

**Outdated dependencies:**
```
Issue: Package 2 major versions behind
Fix: Update to latest
Strategy: Test after update, user approves
```

**Version conflicts:**
```
Issue: Same package, multiple versions
Fix: Run npm dedupe
Strategy: User reviews changes
```

### ✗ Manual Only

**License violations:**
```
Issue: GPL-3.0 license incompatible
Fix: Replace with compatible alternative
Strategy: Suggest alternatives, user chooses
```

**Circular dependencies:**
```
Issue: Files import each other
Fix: Refactor architecture
Strategy: Provide refactoring guidance
```

---

## Output Format

```json
{
  "audit_type": "dependency",
  "timestamp": "2026-01-31T10:00:00Z",
  "project_path": "/path/to/project",
  "summary": {
    "total_dependencies": 150,
    "outdated": 25,
    "vulnerabilities": {
      "critical": 1,
      "high": 3,
      "medium": 5,
      "low": 8
    },
    "license_issues": 2,
    "unused": 4,
    "conflicts": 3
  },
  "issues": [
    {
      "severity": "critical",
      "category": "security_vulnerability",
      "package": "lodash",
      "current": "4.17.15",
      "fixAvailable": "4.17.21",
      "cve": "CVE-2020-8203",
      "suggestion": "Run npm audit fix",
      "auto_fixable": true
    },
    {
      "severity": "high",
      "category": "outdated_dependency",
      "package": "react",
      "current": "16.8.0",
      "latest": "18.2.0",
      "suggestion": "Update to 18.2.0",
      "auto_fixable": false
    }
  ]
}
```

---

## Integration with Technical Methodology

Dependency audit is part of the **technical methodology**:

```json
{
  "methodologies": [
    {
      "name": "technical",
      "description": "How it's built",
      "audits": [
        "dependency",        // ← This audit
        "quality",
        "security",
        "performance"
      ]
    }
  ]
}
```

**Technical Perspective:**
- Are dependencies up to date?
- Are there security vulnerabilities?
- Is license compliance maintained?
- Are dependency sizes reasonable?

---

*End of Dependency Audit*
*Part of v4.0.0 Universal Skills Ecosystem*
*Methodology: Technical (How it's built)*
*Dependency health and security validation*
