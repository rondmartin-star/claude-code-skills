# CorpusHub Reviewer Skill

## Purpose

The Reviewer skill enables browsing artifacts, adding structured comments, and generating change plans from review feedback.

## API Base

`http://localhost:3000`

---

## Browse Artifacts

### List all artifacts
```bash
curl http://localhost:3000/api/artifacts
```
Returns an array of artifacts with `type`, `name`, `title`, and metadata.

### View a specific artifact
```bash
curl http://localhost:3000/api/artifacts/{type}/{name}
```
Returns the artifact's full content, metadata, and version info.

**Parameters:**
- `type` -- artifact type (e.g., `chapter`, `appendix`, `glossary`)
- `name` -- artifact name/slug (e.g., `introduction`, `chapter-1`)

---

## Comments

### Add a comment
```bash
curl -X POST http://localhost:3000/api/comments \
  -H "Content-Type: application/json" \
  -d '{
    "artifact_type": "chapter",
    "artifact_name": "introduction",
    "comment_text": "This section needs a stronger opening thesis.",
    "comment_type": "suggestion",
    "priority": "high"
  }'
```

**Fields:**
| Field | Type | Required | Values |
|-------|------|----------|--------|
| `artifact_type` | string | yes | The artifact's type |
| `artifact_name` | string | yes | The artifact's name |
| `comment_text` | string | yes | The comment body |
| `comment_type` | string | yes | `suggestion`, `issue`, `question`, `praise` |
| `priority` | string | no | `low`, `medium`, `high`, `critical` |

### View comments for an artifact
```bash
curl http://localhost:3000/api/comments/{type}/{name}
```

### View all review comments
```bash
curl http://localhost:3000/api/review/comments
```
Returns all comments across all artifacts, optionally filtered by query params.

### Update comment status
```bash
curl -X PUT http://localhost:3000/api/comments/{id}/status \
  -H "Content-Type: application/json" \
  -d '{"status": "resolved"}'
```

**Status values:** `open`, `in_progress`, `resolved`, `dismissed`

### Reply to a comment
```bash
curl -X POST http://localhost:3000/api/comments/{id}/replies \
  -H "Content-Type: application/json" \
  -d '{"reply_text": "Agreed, I will draft a new opening."}'
```

---

## Change Plans

Change plans group related comments into actionable edit proposals.

### Generate a change plan
```bash
curl -X POST http://localhost:3000/api/plans/generate \
  -H "Content-Type: application/json" \
  -d '{
    "comment_ids": [1, 3, 7],
    "scope": "narrow"
  }'
```

**Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `comment_ids` | array | yes | IDs of comments to include |
| `scope` | string | no | `narrow` (targeted), `broad` (wider implications) |

The response includes a generated plan with proposed changes, affected artifacts, and estimated effort.

### List all plans
```bash
curl http://localhost:3000/api/plans
```

### View a specific plan
```bash
curl http://localhost:3000/api/plans/{id}
```

### Approve or reject a plan
```bash
curl -X PUT http://localhost:3000/api/plans/{id}/status \
  -H "Content-Type: application/json" \
  -d '{"status": "approved"}'
```

**Status values:** `draft`, `approved`, `rejected`, `in_progress`, `completed`

---

## Typical Reviewer Workflow

1. **Browse**: `GET /api/artifacts` to see what's available
2. **Read**: `GET /api/artifacts/{type}/{name}` to review content
3. **Comment**: `POST /api/comments` to leave feedback
4. **Group**: Collect comment IDs for related issues
5. **Plan**: `POST /api/plans/generate` to create a change plan
6. **Approve**: `PUT /api/plans/{id}/status` to approve the plan for editors

---

## Application Project Artifact Reviews

These workflows are designed for reviewing software project artifacts (requirements, system design, API specs, etc.) managed as a CorpusHub corpus.

### Requirements Review

Use this workflow when reviewing requirements documents in an application project corpus.

**Steps:**

1. **Completeness Check** -- Verify all requirements have:
   - Clear acceptance criteria
   - Priority assigned (must-have, should-have, nice-to-have)
   - Stakeholder attribution
   - No ambiguous language ("should," "might," "could" without qualification)

2. **Consistency Check** -- Scan for contradictions across requirements:
   ```bash
   # List all requirements artifacts
   curl http://localhost:3000/api/artifacts?type=requirements
   ```
   - Flag conflicting statements between different requirement documents
   - Check for duplicate requirements with different IDs
   - Verify terminology matches the framework terms defined in the corpus config

3. **Traceability to Design Docs** -- Ensure every requirement maps to at least one design artifact:
   - Cross-reference requirement IDs against system design and architecture docs
   - Flag orphan requirements (no design coverage)
   - Flag gold-plated design elements (design without a backing requirement)

4. **AI Gap Analysis** -- Identify gaps that manual review may miss:
   - Missing non-functional requirements (performance, security, scalability)
   - Edge cases not covered by acceptance criteria
   - Integration points between components that lack explicit requirements
   - Comment findings using `comment_type: "issue"` with appropriate priority

**Comment template for requirements issues:**
```bash
curl -X POST http://localhost:3000/api/comments \
  -H "Content-Type: application/json" \
  -d '{
    "artifact_type": "requirements",
    "artifact_name": "<artifact-name>",
    "comment_text": "[REQ-REVIEW] <finding>",
    "comment_type": "issue",
    "priority": "high"
  }'
```

### System Design Review

Use this workflow when reviewing system design, architecture, and API specification artifacts.

**Steps:**

1. **Architecture Alignment with Requirements** -- Verify the design addresses all requirements:
   - Each must-have requirement should have a clear architectural component
   - Quality attributes (scalability, reliability, etc.) should be reflected in architectural decisions
   - Check that ADRs (Architecture Decision Records) reference the requirements they satisfy

2. **Pattern Consistency** -- Ensure design patterns are applied consistently:
   - Same problems should use the same patterns across the system
   - Check framework terms for approved patterns (e.g., CQRS, event-driven, saga)
   - Flag deviations from stated architectural principles
   - Verify error handling and resilience patterns are uniform

3. **API Surface Review** -- Validate API specifications:
   ```bash
   # List API spec artifacts
   curl http://localhost:3000/api/artifacts?type=api-specs
   ```
   - Consistent naming conventions (URL paths, request/response fields)
   - Proper HTTP method usage (GET for reads, POST for creates, etc.)
   - Error response format consistency
   - Authentication/authorization requirements documented
   - Versioning strategy applied uniformly

4. **Cross-Reference: Data Models and API Specs** -- Check alignment between data layer and API layer:
   - Every API resource should map to a defined data model
   - Field names and types should be consistent between data models and API schemas
   - Relationships in data models should be navigable through API endpoints
   - Flag data model fields exposed in APIs that lack validation rules

**Comment template for design issues:**
```bash
curl -X POST http://localhost:3000/api/comments \
  -H "Content-Type: application/json" \
  -d '{
    "artifact_type": "system-design",
    "artifact_name": "<artifact-name>",
    "comment_text": "[DESIGN-REVIEW] <finding>",
    "comment_type": "issue",
    "priority": "medium"
  }'
```

---

## Tips

- Use `comment_type: "issue"` for problems that must be fixed, `"suggestion"` for optional improvements
- Set `priority: "critical"` sparingly -- only for factual errors or blocking issues
- When generating plans, use `scope: "broad"` if changes may ripple across multiple artifacts
- Check existing comments before adding duplicates: `GET /api/comments/{type}/{name}`
