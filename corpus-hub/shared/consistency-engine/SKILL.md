# CorpusHub Consistency Engine (Shared Skill)

## Purpose

The Consistency Engine ensures coherence across the corpus by scanning for term misuse, broken references, style deviations, and structural issues. It is driven by the corpus-config.json framework terms and voice definitions.

## API Base

`http://localhost:3000`

---

## Full Consistency Scan

### Run a scan across all artifacts
```bash
curl -X POST http://localhost:3000/api/consistency/scan
```

**Response structure:**
```json
{
  "scan_id": "scan-2025-01-15-001",
  "timestamp": "2025-01-15T10:30:00Z",
  "summary": {
    "total_issues": 12,
    "critical": 1,
    "warning": 7,
    "info": 4
  },
  "issues": [
    {
      "id": "issue-001",
      "severity": "critical",
      "category": "term_misuse",
      "artifact_type": "chapter",
      "artifact_name": "economic-policy",
      "location": "paragraph 3",
      "description": "Term 'industrial policy' used instead of framework term 'strategic industrial investment'",
      "suggestion": "Replace with the defined framework term"
    }
  ]
}
```

### Issue Categories

| Category | Description | Severity Range |
|----------|-------------|----------------|
| `term_misuse` | Using non-standard terms when a framework term exists | warning - critical |
| `broken_reference` | Cross-reference to a non-existent artifact | critical |
| `style_deviation` | Content that doesn't match the corpus voice guidelines | info - warning |
| `orphaned_artifact` | Artifact not referenced by any other artifact | info |
| `duplicate_content` | Substantially similar content in multiple artifacts | warning |
| `missing_definition` | Term used without definition in glossary | warning |

---

## Preview Changes

### Check consistency impact before committing an edit
```bash
curl -X POST http://localhost:3000/api/artifacts/{type}/{name}/preview-changes \
  -H "Content-Type: application/json" \
  -d '{
    "newContent": "The proposed new content..."
  }'
```

Returns:
- Diff between current and proposed content
- New consistency issues introduced by the change
- Existing consistency issues resolved by the change
- Affected cross-references

This is the same endpoint used by the Editor skill but is documented here for its consistency-checking role.

---

## View Issues

### Get all open consistency issues
```bash
curl http://localhost:3000/api/consistency/issues
```

Optional query parameters:
- `severity` -- filter by severity (`critical`, `warning`, `info`)
- `category` -- filter by category (e.g., `term_misuse`)
- `artifact_type` -- filter by artifact type
- `artifact_name` -- filter by specific artifact

```bash
# Get only critical term misuse issues
curl "http://localhost:3000/api/consistency/issues?severity=critical&category=term_misuse"
```

---

## View References

### Check cross-references for a specific entity
```bash
curl "http://localhost:3000/api/consistency/references?reference_type=term&reference_id=strategic-industrial-investment"
```

**Parameters:**
| Param | Description |
|-------|-------------|
| `reference_type` | Type of reference: `term`, `artifact`, `section` |
| `reference_id` | The identifier of the referenced entity |

Returns all artifacts that reference the specified entity, along with the context of each reference.

---

## Framework Terms System

The consistency engine is driven by framework terms defined in `corpus-config.json`. Each term has:

- **term**: The canonical term text
- **definition**: What it means in this corpus
- **aliases**: Acceptable alternative forms
- **avoid**: Terms that should NOT be used (replaced by this term)

Example from config:
```json
{
  "term": "strategic industrial investment",
  "definition": "Government-directed capital allocation toward domestic manufacturing and technology sectors",
  "aliases": ["strategic investment", "SII"],
  "avoid": ["industrial policy", "government spending", "subsidies"]
}
```

The scanner flags any use of "avoid" terms and suggests the canonical framework term.

---

## Interpreting Scan Results

### Severity Levels

- **Critical**: Must be fixed. Broken references, incorrect term usage that changes meaning.
- **Warning**: Should be fixed. Style drift, non-preferred terminology, minor inconsistencies.
- **Info**: Optional. Suggestions for improvement, orphaned artifacts, structural notes.

### Recommended Actions

1. **Critical issues**: Fix immediately via the Editor skill
2. **Warning issues**: Create comments via the Reviewer skill, then generate a change plan
3. **Info issues**: Track for future cleanup; no immediate action needed

### Post-Scan Workflow

1. Run scan: `POST /api/consistency/scan`
2. Review critical issues first
3. For each critical issue, either edit directly or create a review comment
4. Group related warnings into change plans
5. Re-scan after fixes to verify resolution
