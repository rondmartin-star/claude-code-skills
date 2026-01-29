# Consistency Engine Skill

## Purpose

Core logic for detecting framework consistency issues, tracking cross-references, and ensuring all documents maintain alignment with canonical definitions.

## What It Tracks

### 1. Seven Principles
Definitions and applications across all documents.

**Canonical Source:** `03-specifications/v1.0/america40.comprehensive-framework-synthesis-streamlined.md`

### 2. Fourteen Stakeholder Roles
Definitions, functions, and relationships.

**Canonical Source:** `03-specifications/v1.0/america40.stakeholder-roles.md`

### 3. Key Terms
- Variable Geometry
- Curated Failure
- Attractor Theory
- Democracy Auditor
- America 1.0/2.0/3.0/4.0

### 4. Cross-References
Document dependencies and citation networks.

## Detection Algorithm

```javascript
async function detectConsistencyIssues(artifactType, artifactName, content) {
  const issues = [];

  // 1. Parse content for framework references
  const references = extractReferences(content);

  // 2. Validate against canonical definitions
  for (const ref of references) {
    const canonical = await getCanonicalDefinition(ref.type, ref.id);

    if (!canonical) {
      issues.push({
        type: 'unknown_reference',
        severity: 'warning',
        location: ref.location,
        description: `Unknown ${ref.type}: "${ref.id}"`
      });
      continue;
    }

    // Check for definition conflicts
    if (ref.isDefinition && ref.text !== canonical.text) {
      issues.push({
        type: 'definition_conflict',
        severity: 'critical',
        location: ref.location,
        description: `Definition differs from canonical source`,
        expected: canonical.text,
        actual: ref.text
      });
    }
  }

  // 3. Check for orphaned references
  const orphans = await findOrphanedReferences(artifactType, artifactName);
  issues.push(...orphans);

  // 4. Validate cross-document consistency
  const crossDoc = await validateCrossDocumentConsistency(references);
  issues.push(...crossDoc);

  return issues;
}
```

## Reference Extraction

```javascript
function extractReferences(content) {
  const references = [];

  // Extract principle references
  const principlePatterns = [
    /Human Dignity and Inclusion/gi,
    /Social and Ecological Interconnection/gi,
    /Economic Justice and Opportunity/gi,
    /Democratic Governance and Rule of Law/gi,
    /Global Citizenship and Leadership/gi,
    /Creative and Cultural Flourishing/gi,
    /Evidence-Based Decision Making/gi
  ];

  for (const pattern of principlePatterns) {
    const matches = content.matchAll(pattern);
    for (const match of matches) {
      references.push({
        type: 'principle',
        id: match[0],
        location: match.index,
        context: extractContext(content, match.index)
      });
    }
  }

  // Extract role references
  const roles = [
    'Citizen', 'Representative', 'Expert', 'Educator', 'Facilitator',
    'Democracy Auditor', 'Communicator', 'Contributor', 'Community Builder',
    'Bridge Builder', 'Cultural Creator', 'Protector', 'Systems Designer', 'Implementer'
  ];

  for (const role of roles) {
    const pattern = new RegExp(`\\b${role}\\b`, 'gi');
    const matches = content.matchAll(pattern);
    for (const match of matches) {
      references.push({
        type: 'role',
        id: role,
        location: match.index,
        context: extractContext(content, match.index)
      });
    }
  }

  // Extract key term references
  const keyTerms = [
    'Variable Geometry', 'Curated Failure', 'Attractor Theory',
    'America 1.0', 'America 2.0', 'America 3.0', 'America 4.0'
  ];

  for (const term of keyTerms) {
    const pattern = new RegExp(term, 'gi');
    const matches = content.matchAll(pattern);
    for (const match of matches) {
      references.push({
        type: 'key_term',
        id: term,
        location: match.index,
        context: extractContext(content, match.index)
      });
    }
  }

  return references;
}
```

## Implied Changes Detection

When content is modified, detect what other documents need updates:

```javascript
async function detectImpliedChanges(oldContent, newContent, artifactType, artifactName) {
  const implied = [];

  // 1. Find changes in framework terms
  const oldRefs = extractReferences(oldContent);
  const newRefs = extractReferences(newContent);

  // 2. Detect added/removed/modified references
  const added = newRefs.filter(n => !oldRefs.some(o => o.id === n.id && o.type === n.type));
  const removed = oldRefs.filter(o => !newRefs.some(n => n.id === o.id && n.type === o.type));

  // 3. Find documents that reference the same concepts
  for (const ref of [...added, ...removed]) {
    const relatedDocs = await findDocumentsReferencing(ref.type, ref.id);

    for (const doc of relatedDocs) {
      if (doc.artifact_type === artifactType && doc.artifact_name === artifactName) continue;

      implied.push({
        document: `${doc.artifact_type}/${doc.artifact_name}`,
        reference: ref,
        reason: ref in added
          ? `New reference to "${ref.id}" may need cross-referencing`
          : `Removed reference to "${ref.id}" may need updating`,
        severity: 'warning',
        priority: doc.is_definition ? 'required' : 'recommended'
      });
    }
  }

  return implied;
}
```

## Cross-Document Validation

```javascript
async function validateCrossDocumentConsistency(references) {
  const issues = [];

  // Build reference graph
  const graph = await buildReferenceGraph();

  // Check for circular definitions
  const cycles = detectCycles(graph);
  for (const cycle of cycles) {
    issues.push({
      type: 'circular_reference',
      severity: 'warning',
      description: `Circular reference detected: ${cycle.join(' → ')}`
    });
  }

  // Check for broken references
  for (const ref of references) {
    if (ref.type === 'document_ref') {
      const exists = await documentExists(ref.target);
      if (!exists) {
        issues.push({
          type: 'broken_reference',
          severity: 'error',
          description: `Referenced document does not exist: ${ref.target}`
        });
      }
    }
  }

  return issues;
}
```

## Database Schema

```sql
-- Framework references for tracking
CREATE TABLE framework_references (
  id INTEGER PRIMARY KEY,
  artifact_type TEXT NOT NULL,
  artifact_name TEXT NOT NULL,
  reference_type TEXT NOT NULL,      -- principle/role/term/document
  reference_id TEXT NOT NULL,
  section_id TEXT,
  line_number INTEGER,
  context_text TEXT,
  is_definition INTEGER DEFAULT 0,   -- True if this is THE definition
  is_modified INTEGER DEFAULT 0,     -- True if diverges from canonical
  last_verified DATETIME
);

-- Consistency issues detected
CREATE TABLE consistency_issues (
  id INTEGER PRIMARY KEY,
  issue_type TEXT NOT NULL,
  severity TEXT DEFAULT 'warning',   -- critical/error/warning/info
  artifact_type TEXT NOT NULL,
  artifact_name TEXT NOT NULL,
  section_id TEXT,
  line_number INTEGER,
  description TEXT NOT NULL,
  expected_value TEXT,
  actual_value TEXT,
  status TEXT DEFAULT 'detected',    -- detected/reviewed/resolved/ignored
  resolution_note TEXT,
  detected_at DATETIME
);
```

## API Endpoints

```javascript
// Full framework consistency scan
POST /api/consistency/scan
Response: { scanned: true, issues_found: 12 }

// Get current issues
GET /api/consistency/issues?severity=critical
Response: [{ id, type, severity, description, ... }]

// Preview changes before saving
POST /api/artifacts/:type/:name/preview-changes
{ newContent: "..." }
Response: { changes: [...], analysis: {...}, implied: [...] }

// Get framework reference map
GET /api/consistency/references?reference_type=principle
Response: [{ artifact, reference_type, reference_id, context }]
```

## Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| critical | Definition conflicts with canonical | Block until resolved |
| error | Broken references or missing requirements | Should resolve before save |
| warning | Potential inconsistencies | Review recommended |
| info | Suggestions for improvement | Optional consideration |
