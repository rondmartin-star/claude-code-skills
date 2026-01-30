# Corpus Convert - Convert Existing Projects to Corpus-Enabled

## Purpose

This skill converts existing projects to be corpus-enabled while preserving their existing structure and files. It analyzes your project, infers artifact types, generates `corpus-config.json`, and registers with CorpusHub.

**Critical:** Original files are NEVER deleted. They are marked as deprecated but preserved for reference and rollback.

**Use this skill when:**
- Converting an existing project with documentation
- Migrating from another documentation system
- Adding CorpusHub to a mature project
- Enabling corpus features for legacy projects

**Don't use this skill for:**
- Brand-new projects (use `corpus-init` instead)
- Projects with no documentation files

---

## Workflow Overview

```
User: "Convert this project to use CorpusHub"
↓
0. DETECT corpus status (check if already corpus-enabled)
   → If already enabled: show status and ask if user wants to reconvert
   → If partially enabled: identify issues and suggest fixes
   → If not enabled: proceed with conversion
1. Detect project location (current directory)
2. Scan for documentation files
3. Analyze directory structure
4. Infer artifact types from paths/names
5. Show detected mapping to user
6. Ask for confirmation or customization
7. Ask for source mode (traditional/corpus/hybrid)
8. Optionally extract framework terms
9. Optionally infer relationships
10. Generate corpus-config.json
11. Register with CorpusHub API
12. Create corpus bits from existing files
13. Mark original files as DEPRECATED (not deleted)
14. Report conversion summary
```

**Total time:** 3-5 minutes (longer for large projects)

---

## Step 0: Detection (Pre-Check)

**ALWAYS run detection before converting** to avoid conflicts with existing corpus infrastructure.

### Detection API Call

```javascript
const projectPath = process.cwd(); // or user-specified path
const response = await fetch(`http://localhost:3000/api/corpora/detect?path=${encodeURIComponent(projectPath)}`);
const status = await response.json();
```

### Detection Results

**Case A: Fully Corpus-Enabled**
```javascript
if (status.isCorpusEnabled) {
  console.log(`⚠️  This project is already corpus-enabled: ${status.config.name}`);
  console.log('\nCurrent Status:');
  console.log(`  • Config: ${status.checks.configValid ? '✓ Valid' : '✗ Invalid'}`);
  console.log(`  • Registered: ${status.checks.isRegistered ? '✓ Yes' : '✗ No'}`);
  console.log(`  • Infrastructure: ${status.checks.infrastructureExists ? '✓ Exists' : '✗ Missing'}`);
  console.log(`  • Database: ${status.checks.databaseExists ? '✓ Exists' : '✗ Missing'}`);

  if (status.infrastructure) {
    console.log(`\n  • Corpus has ${status.infrastructure.bitCount} bits`);
  }

  const choice = await askUser({
    question: 'This project is already corpus-enabled. What would you like to do?',
    options: [
      { label: 'View status details', value: 'status' },
      { label: 'Reconvert (regenerates corpus from source)', value: 'reconvert' },
      { label: 'Repair issues', value: 'repair' },
      { label: 'Cancel', value: 'cancel' }
    ]
  });

  if (choice === 'cancel') {
    console.log('✅ Conversion cancelled. No changes made.');
    return;
  }

  if (choice === 'status') {
    // Show full status report
    console.log(JSON.stringify(status, null, 2));
    return;
  }

  if (choice === 'repair') {
    // Show suggested fixes
    console.log('\nSuggested Fixes:');
    status.suggestions.forEach((s, i) => {
      console.log(`${i + 1}. ${s.action}: ${s.description}`);
    });
    return;
  }

  // choice === 'reconvert': warn and proceed
  console.warn('\n⚠️  WARNING: Reconverting will:');
  console.warn('  • Regenerate corpus-config.json');
  console.warn('  • Rebuild all corpus bits');
  console.warn('  • Preserve existing files (marked deprecated)');
  console.warn('  • NOT delete any data');

  const confirm = await askUser({
    question: 'Are you sure you want to reconvert?',
    options: [
      { label: 'Yes, reconvert', value: 'yes' },
      { label: 'No, cancel', value: 'no' }
    ]
  });

  if (confirm === 'no') {
    console.log('✅ Conversion cancelled. No changes made.');
    return;
  }

  // Proceed with reconversion
  console.log('Starting reconversion...');
}
```

**Case B: Partially Corpus-Enabled (has issues)**
```javascript
if (status.checks.configExists && !status.isCorpusEnabled) {
  console.log('⚠️  Found partial corpus infrastructure with issues:');

  // Show detected issues
  console.log('\nIssues:');
  status.issues.forEach(issue => {
    const icon = issue.severity === 'error' ? '✗' : '⚠️';
    console.log(`  ${icon} [${issue.severity}] ${issue.message}`);
    if (issue.details) {
      console.log(`      ${issue.details}`);
    }
  });

  // Show suggestions
  console.log('\nSuggestions:');
  status.suggestions.forEach((s, i) => {
    console.log(`  ${i + 1}. ${s.description}`);
  });

  const choice = await askUser({
    question: 'Would you like to fix issues or start fresh?',
    options: [
      { label: 'Fix existing infrastructure', value: 'fix' },
      { label: 'Start fresh (regenerate)', value: 'fresh' },
      { label: 'Cancel', value: 'cancel' }
    ]
  });

  if (choice === 'cancel') return;

  if (choice === 'fix') {
    // Attempt automated fixes based on suggestions
    console.log('Attempting to fix issues...');
    // Implementation would apply suggested fixes
    return;
  }

  // choice === 'fresh': proceed with conversion
  console.log('Proceeding with fresh conversion...');
}
```

**Case C: Not Corpus-Enabled (Clean Conversion)**
```javascript
if (!status.checks.configExists) {
  // Proceed with standard conversion workflow
  console.log('✅ No existing corpus infrastructure detected. Starting conversion...');
}
```

---

## Key Principle: Preserve Originals

**CRITICAL: Original files are NEVER deleted during conversion.**

Instead, they are:
1. Marked with clear deprecation notices at the top
2. Referenced by `.DEPRECATED` marker files in their directories
3. Kept for reference and rollback purposes
4. Disabled from file watchers (no auto-sync)

After conversion, the **corpus becomes the source of truth**. Users should edit via CorpusHub interface, not the original files.

---

## Project Analysis Phase

### Step 1: Directory Scanning

Scan for documentation files using common patterns:

```javascript
const scanPatterns = [
  "docs/**/*.md",
  "documentation/**/*.md",
  "specs/**/*.md",
  "spec/**/*.md",
  "requirements/**/*.md",
  "design/**/*.md",
  "architecture/**/*.md",
  "api/**/*.{md,yaml,json,openapi}",
  "adr/**/*.md",              // Architecture Decision Records
  "rfc/**/*.md",              // Request for Comments
  "decisions/**/*.md",
  "guides/**/*.md",
  "*.md"                      // Root-level READMEs
];

const excludePatterns = [
  "node_modules/**",
  ".git/**",
  "dist/**",
  "build/**",
  "*.min.js"
];
```

### Step 2: Artifact Type Inference

Infer artifact types from file paths:

| File Pattern | Inferred Type | Label |
|-------------|---------------|-------|
| `**/requirements/**/*.md` | `requirements` | "Requirements" |
| `**/design/**/*.md` | `design` | "Design Documents" |
| `**/architecture/**/*.md` | `architecture` | "Architecture" |
| `**/api/**/*` | `api-specs` | "API Specifications" |
| `**/adr/**/*.md` or `**/decisions/**/*.md` | `decisions` | "Architecture Decisions" |
| `**/specs/**/*.md` or `**/spec/**/*.md` | `specifications` | "Specifications" |
| `**/guides/**/*.md` | `guides` | "Guides" |
| `README.md`, `CONTRIBUTING.md` | `project-docs` | "Project Documentation" |

### Step 3: Extension Detection

Group files by artifact type and detect all extensions used:

```javascript
// Example result:
{
  "requirements": [".md", ".html"],
  "api-specs": [".md", ".yaml", ".json", ".openapi"],
  "design": [".md", ".html"]
}
```

### Step 4: Show Analysis to User

```
📊 Project Analysis Complete

Found 47 documentation files across 5 artifact types:

  📁 requirements/         12 files  (.md)
  📁 design/               8 files   (.md)
  📁 api/                  15 files  (.md, .yaml)
  📁 architecture/         6 files   (.md)
  📁 decisions/            6 files   (.md)

Suggested mapping:
  requirements/     → Requirements
  design/           → Design Documents
  api/              → API Specifications
  architecture/     → Architecture
  decisions/        → Architecture Decisions

Use this mapping? [Yes / No - I'll customize]
```

---

## Interactive Prompts

### Prompt 1: Confirm Detected Mapping

```
❓ Use detected artifact mapping?

The following artifact types were detected:
  • requirements/ → Requirements (.md)
  • design/ → Design Documents (.md)
  • api/ → API Specifications (.md, .yaml)
  • architecture/ → Architecture (.md)
  • decisions/ → Architecture Decisions (.md)

Options:
  ✅ Yes - looks good (Recommended)
  ❌ No - I'll customize paths and types

Default: Yes
```

If "No", allow user to:
- Add/remove artifact types
- Change paths
- Change labels
- Modify extensions

### Prompt 2: Source Mode

```
❓ What source mode should we use?

Source mode determines how edits are handled:

  1. Traditional (edit in IDE, corpus for review)
     • Source files are authoritative
     • Corpus HTML generated for review/comments
     • File watchers sync changes to corpus
     • Best for: Software projects

  2. Corpus (edit in browser, sync to files)
     • Corpus is authoritative
     • Original files marked as deprecated
     • All edits via CorpusHub interface
     • Best for: Documentation projects

  3. Hybrid (mix of both)
     • Some artifacts traditional, some corpus
     • Advanced per-artifact configuration
     • Best for: Complex projects

Default: Corpus (for conversion)

❓ Which mode? [1-3]
```

### Prompt 3: File Watchers (if Traditional/Hybrid)

```
❓ Enable file watchers for bidirectional sync?

File watchers monitor source files and auto-update corpus HTML when changes are detected.

Options:
  • Yes - enable watchers (Recommended for traditional mode)
  • No - manual sync only

Default: Yes

⚠️  Note: In corpus mode, watchers are disabled for deprecated files.
```

### Prompt 4: Framework Term Extraction

```
❓ Extract framework terms from existing docs?

Framework terms help maintain terminology consistency across your corpus.

Options:
  • Yes - auto-detect terms (Recommended)
  • No - I'll add manually later

Default: Yes

If enabled, the top 20 most frequent capitalized terms will be suggested.
```

### Prompt 5: Relationship Inference

```
❓ Infer relationships between documents?

Relationships connect related artifacts (e.g., code implementing requirements).

Options:
  1. Yes - link analysis (fast)
     → Parses markdown links: [text](path/file.md)
     → Creates REFERENCES edges

  2. Yes - AI-assisted (slower, more accurate)
     → Uses Claude API to detect semantic relationships
     → Requires API key

  3. No - skip relationship inference

Default: Yes - link analysis

❓ Which option? [1-3]
```

---

## File Deprecation Process

**Critical:** Original files are preserved but marked as deprecated.

### Deprecation Steps

For each converted file:

1. **Read original content**
2. **Convert to HTML** (if needed)
3. **Save to corpus directory**
4. **Add deprecation notice** to original file (prepend)
5. **Create .DEPRECATED marker** in directory
6. **Create bit record** with `sourceOfTruth: 'corpus'`
7. **Disable file watcher** for this file

### Deprecation Notice Format

#### For Markdown Files (`.md`)

```markdown
> **⚠️ DEPRECATED**: This file has been migrated to CorpusHub.
> Please edit via CorpusHub interface at http://localhost:3000
> This file is kept for reference only and will NOT be automatically updated.

[Original content follows...]
```

#### For HTML Files (`.html`)

```html
<!-- ⚠️ DEPRECATED: This file has been migrated to CorpusHub. -->
<!-- Please edit via CorpusHub interface at http://localhost:3000 -->
<!-- This file is kept for reference only and will NOT be automatically updated. -->

[Original content follows...]
```

#### For YAML Files (`.yaml`, `.yml`)

```yaml
# ⚠️ DEPRECATED: This file has been migrated to CorpusHub.
# Please edit via CorpusHub interface at http://localhost:3000
# This file is kept for reference only and will NOT be automatically updated.

[Original content follows...]
```

### .DEPRECATED Marker File

Created once per directory with migrated files:

```
This directory contains deprecated files migrated to CorpusHub.

Edit these documents via CorpusHub interface at:
  http://localhost:3000

Original files are preserved for reference only.
They will NOT be automatically updated.

Conversion date: 2026-01-30T18:45:00Z
Corpus slug: my-existing-project

To rollback: Delete corpus-config.json and remove deprecation notices
```

---

## Conversion Summary Report

After successful conversion:

```
✅ Corpus conversion complete!

Corpus: "My Existing Project"
Slug: "my-existing-project"
Database: data/corpora/my-existing-project.db

Summary:
  📁 Artifact types: 5 (requirements, design, api-specs, architecture, decisions)
  📄 Files discovered: 47
  🔗 Bits created: 47
  🔀 Relationships inferred: 23
  🏷️  Framework terms: 15 (3 categories)
  ⚠️  Original files: MARKED AS DEPRECATED (not deleted)

Artifacts by type:
  • requirements:    12 files
  • design:          8 files
  • api-specs:       15 files
  • architecture:    6 files
  • decisions:       6 files

Source mode: corpus (corpus is now source of truth)
File watchers: disabled for deprecated files

⚠️ IMPORTANT: Original Files Preserved
  • Original files have deprecation notices at the top
  • .DEPRECATED marker files created in migrated directories
  • DO NOT EDIT original files - changes will not sync
  • All edits should be made via CorpusHub at http://localhost:3000
  • Original files kept for reference and rollback if needed

Relationships detected:
  • REFERENCES: 18 (from markdown links)
  • IMPLEMENTS: 3 (code → requirements)
  • SUPPORTS: 2 (guides → specs)

Framework terms extracted:
  • quality-attributes: scalability, reliability, security (7 terms)
  • design-patterns: microservices, event-driven, CQRS (5 terms)
  • stakeholders: product-owner, tech-lead, architect (3 terms)

Next steps:
  1. Review generated corpus-config.json
  2. Browse to http://localhost:3000
  3. Verify all artifacts are visible
  4. Make test edit to confirm corpus workflow
  5. Run consistency scan to find issues
  6. Optional: Archive deprecated files once confident in migration

Configuration saved to: ./corpus-config.json

Rollback instructions:
  1. Delete corpus-config.json
  2. Remove deprecation notices from files
  3. Delete .DEPRECATED marker files
  4. Delete corpus/ directory
```

---

## Implementation Steps

### 1. Check Prerequisites

```bash
# Verify CorpusHub server is running
curl http://localhost:3000/api/health

# If not:
echo "Start CorpusHub: cd \"G:\\My Drive\\Projects\\CorpusHub\" && npm start"
```

### 2. Scan Project Directory

```bash
PROJECT_DIR=$(pwd)
echo "Scanning: $PROJECT_DIR"

# Use glob patterns to find documentation
find docs/ -name "*.md" 2>/dev/null || true
find specs/ -name "*.md" 2>/dev/null || true
# ... etc
```

### 3. Analyze File Structure

Group files by inferred artifact type, count files, detect extensions.

### 4. Generate corpus-config.json

Based on detected structure:

```javascript
const config = {
  corpus: {
    name: path.basename(PROJECT_DIR),
    description: `Artifact corpus for ${path.basename(PROJECT_DIR)}`,
    version: "1.0.0",
    baseDir: "."
  },
  artifacts: inferredArtifacts,
  framework: extractedTerms ? { categories: extractedTerms } : null,
  voice: null,
  roles: {
    available: ["admin", "editor", "viewer", "pending"],
    defaultRole: "pending",
    aiAccess: ["admin", "editor"],
    editAccess: ["admin", "editor"]
  },
  consistency: { enabled: !!extractedTerms }
};

fs.writeFileSync('corpus-config.json', JSON.stringify(config, null, 2));
```

### 5. Register with CorpusHub

```bash
curl -X POST http://localhost:3000/api/corpora/register \
  -H "Content-Type: application/json" \
  -d "{
    \"path\": \"$PROJECT_DIR\",
    \"name\": \"My Existing Project\",
    \"sourceMode\": \"corpus\",
    \"corpusDir\": \"corpus\",
    \"scanPatterns\": [\"docs/**/*.md\", \"specs/**/*.md\"],
    \"excludePatterns\": [\"node_modules/**\", \".git/**\"]
  }"
```

The registration service will:
- Create corpus/ directory
- Scan files
- Convert to HTML
- Create bits
- Infer relationships
- Start file watchers (if traditional)

### 6. Mark Original Files as Deprecated

For each converted file:

```bash
# Add deprecation notice
DEPRECATION="<deprecation notice for file type>"
ORIGINAL_CONTENT=$(cat "$file")
echo "$DEPRECATION" > "$file"
echo "$ORIGINAL_CONTENT" >> "$file"

# Create .DEPRECATED marker in directory
echo "Deprecated files - edit via CorpusHub" > "$(dirname $file)/.DEPRECATED"
```

### 7. Switch to New Corpus

```bash
curl -X POST http://localhost:3000/api/corpora/switch \
  -H "Content-Type: application/json" \
  -d "{\"slug\": \"my-existing-project\"}"
```

### 8. Verify

```bash
curl http://localhost:3000/api/corpora/active
curl http://localhost:3000/api/artifacts
```

---

## Error Handling

### Error: No Documentation Found

```
❌ No documentation files found

Searched for:
  • docs/**/*.md
  • specs/**/*.md
  • requirements/**/*.md
  • (and 10 more patterns)

This project may not have documentation, or it's in a non-standard location.

Options:
  1. Specify custom search patterns
  2. Use corpus-init to set up new structure
  3. Cancel conversion

[1-3]?
```

### Error: Ambiguous Artifact Types

```
⚠️  Multiple possible mappings detected

The directory "docs/" contains mixed file types:
  • requirements/
  • design/
  • random-notes/

Cannot determine artifact type for: "random-notes/"

Please specify:
  1. Treat as "documentation" (generic)
  2. Treat as "design"
  3. Skip this directory
  4. Create new artifact type

[1-4]?
```

### Error: Bit ID Conflicts

```
⚠️  Duplicate file names detected

Multiple files named "overview.md":
  • docs/requirements/overview.md
  • docs/design/overview.md

Resolution:
  → requirements-overview
  → design-overview

Proceed with automatic resolution? [Y/n]
```

### Error: Failed to Parse File

```
⚠️  Could not parse file: api/broken.yaml

Error: Invalid YAML syntax at line 23

Options:
  • Skip this file (Recommended)
  • Include as-is (may cause issues)
  • Manual fix required

[1-2]?
```

### Error: Registration Failed

```
❌ Corpus registration failed

API response: "Duplicate corpus slug: my-existing-project"

A corpus with this name already exists.

Options:
  1. Use different project name
  2. Unregister existing corpus first
  3. Switch to existing corpus
  4. Cancel

[1-4]?
```

---

## Framework Term Extraction

### Extraction Algorithm

1. **Scan all documentation files**
2. **Extract capitalized phrases** (2+ words)
3. **Count frequency** across all files
4. **Filter noise** (common words like "The Project")
5. **Rank by frequency**
6. **Suggest top 20** as framework terms
7. **Group by category** (heuristic or manual)

### Example Extraction

```
Framework terms extracted from 47 files:

Top terms by frequency:
  1. "Microservices Architecture" (23 occurrences)
  2. "API Gateway Pattern" (18 occurrences)
  3. "Event-Driven Design" (15 occurrences)
  4. "Circuit Breaker" (12 occurrences)
  5. "Service Mesh" (11 occurrences)
  ...

Suggested categories:
  • architecture-patterns: Microservices, API Gateway, Event-Driven
  • resilience-patterns: Circuit Breaker, Retry Logic, Bulkhead
  • integration-patterns: Service Mesh, Message Queue, REST API

Add these terms to corpus-config.json? [Y/n]
```

---

## Relationship Inference

### Link Analysis (Fast)

Parse markdown files for links:

```markdown
<!-- In requirements/auth.md -->
See [API Specification](../api/auth-api.md) for implementation details.
```

Creates edge:
```javascript
{
  source: "requirements/auth",
  target: "api/auth-api",
  relationship: "REFERENCES"
}
```

### AI-Assisted (Slower, More Accurate)

Use Claude API to analyze document pairs:

```
Prompt: Do these two documents have a semantic relationship?

Document A: requirements/authentication.md
"Users must be able to log in with email and password..."

Document B: api/auth-endpoints.md
"POST /api/auth/login - Authenticates user..."

Response: Yes, Document B implements the requirement in Document A.
Relationship: IMPLEMENTS
```

Creates edge:
```javascript
{
  source: "api/auth-endpoints",
  target: "requirements/authentication",
  relationship: "IMPLEMENTS"
}
```

---

## References

**Detailed information:**
- Source modes: See `references/source-modes.md`
- Inference rules: See `references/inference-rules.md`
- Migration patterns: See `references/migration-patterns.md`

**Related skills:**
- Initialize new projects: `corpus-init`
- Review artifacts: `reviewer`
- Edit artifacts: `editor`

**API Endpoints:**
- Register corpus: `POST /api/corpora/register`
- Switch corpus: `POST /api/corpora/switch`
- Check active: `GET /api/corpora/active`

---

## Tips

1. **Backup first:** Commit changes to git before converting
2. **Test on small project:** Try with a test project first
3. **Review mapping:** Verify artifact type detection before proceeding
4. **Corpus mode recommended:** For conversions, corpus mode is simpler
5. **Framework terms:** Extract terms - helps with consistency
6. **Relationships:** Link analysis is fast and usually sufficient
7. **Rollback available:** Original files are preserved for rollback
8. **Test workflow:** Make a test edit after conversion to verify
9. **Archive later:** Keep deprecated files until confident in migration
10. **Gradual migration:** Can convert one artifact type at a time
