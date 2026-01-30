# Inference Rules - Artifact Types, Terms, and Relationships

Automated detection algorithms used during project conversion.

---

## Artifact Type Inference

### Path-Based Detection

| Pattern | Type | Label | Confidence |
|---------|------|-------|-----------|
| `**/requirements/**` | requirements | Requirements | High |
| `**/req/**` | requirements | Requirements | Medium |
| `**/design/**` | design | Design Documents | High |
| `**/architecture/**` | architecture | Architecture | High |
| `**/arch/**` | architecture | Architecture | Medium |
| `**/api/**` | api-specs | API Specifications | High |
| `**/adr/**` | decisions | Architecture Decisions | High |
| `**/decisions/**` | decisions | Architecture Decisions | High |
| `**/specs/**` or `**/spec/**` | specifications | Specifications | High |
| `**/guides/**` or `**/guide/**` | guides | Guides | High |
| `**/docs/**` | documentation | Documentation | Low |
| `README.md` (root) | project-docs | Project Documentation | High |

### Content-Based Detection

If path-based fails, analyze file content:

```javascript
function inferFromContent(content) {
  if (content.includes('# User Story') || content.includes('As a')) {
    return 'stories';
  }
  if (content.includes('## API Endpoint') || content.includes('openapi:')) {
    return 'api-specs';
  }
  if (content.includes('# ADR') || content.includes('Architecture Decision')) {
    return 'decisions';
  }
  if (content.includes('## Requirements')) {
    return 'requirements';
  }
  return 'documentation';  // Default
}
```

---

## Framework Term Extraction

### Algorithm

1. **Tokenize** all documentation files
2. **Extract** capitalized phrases (2-5 words)
3. **Filter** common phrases:
   - "The Project"
   - "This Document"
   - "Table Of Contents"
4. **Count** frequency across corpus
5. **Rank** by occurrence
6. **Suggest** top 20-30 terms

### Example

```javascript
{
  "Microservices Architecture": 23,  // High frequency
  "API Gateway Pattern": 18,
  "Event-Driven Design": 15,
  "Circuit Breaker": 12,
  "Service Mesh": 11,
  "The Project": 45  // Filtered out (noise)
}
```

### Categorization Heuristics

```javascript
function categorizeTerms(terms) {
  const categories = {
    patterns: [],
    technologies: [],
    stakeholders: [],
    quality: []
  };

  for (const term of terms) {
    if (term.includes('Pattern') || term.includes('Architecture')) {
      categories.patterns.push(term);
    } else if (term.includes('scalability') || term.includes('reliability')) {
      categories.quality.push(term);
    } else if (term.includes('Team') || term.includes('Owner')) {
      categories.stakeholders.push(term);
    }
  }

  return categories;
}
```

---

## Relationship Inference

### Link Analysis (Fast)

Parse markdown links:

```markdown
See [Authentication API](../api/auth.md) for details.
```

Creates:
```javascript
{
  source: "current-file",
  target: "api/auth",
  relationship: "REFERENCES"
}
```

### Cross-Reference Detection

```markdown
Implements requirement REQ-001
```

Creates:
```javascript
{
  source: "current-file",
  target: "requirements/req-001",
  relationship: "IMPLEMENTS"
}
```

### Directory Structure Inference

```
guides/
  getting-started.md  → SUPPORTS → specs/overview.md
architecture/
  overview.md → SUPPORTS → design/*.md
```

### AI-Assisted (Optional)

Use Claude API for semantic analysis:

```javascript
async function detectRelationship(docA, docB) {
  const prompt = `
Analyze these two documents:

Document A: ${docA.title}
Content: ${docA.excerpt}

Document B: ${docB.title}
Content: ${docB.excerpt}

Relationship? (IMPLEMENTS, REFERENCES, SUPPORTS, NONE)
  `;

  const response = await claude.complete(prompt);
  return parseRelationship(response);
}
```

---

## Bit Type Inference

48 bit types available. Common ones:

| Content Indicators | Bit Type |
|-------------------|----------|
| "# User Story", "As a" | user-story |
| "## Acceptance Criteria" | acceptance-criteria |
| "# ADR", "Decision:" | architecture-decision |
| "openapi:", "swagger:" | api-specification |
| "# Test Case", "Given/When/Then" | test-case |
| Class definition in code | code-class |
| Function with docstring | code-function |
| README in root | readme |

### Default Fallback

If no match: `documentation` (generic type)

---

## Tips

1. **Path-based is fastest** - Use consistent directory structure
2. **Content analysis is backup** - For non-standard layouts
3. **Manual override available** - User can correct inferences
4. **Framework terms help** - Enable consistency checking
5. **Link analysis sufficient** - AI-assisted optional
