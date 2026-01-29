# Review Orchestrator

## Purpose

Coordinates the Reviewer role workflow: navigating artifacts, adding comments/annotations, and generating change plans from accumulated feedback.

## Workflow

```
1. User browses artifacts in Reference Hub
2. User selects text and adds comment
3. Comments accumulate with type (general/clarification/correction/suggestion)
4. User requests "Generate Change Plan"
5. Claude analyzes comments and proposes structured changes
6. User reviews, accepts/modifies/rejects plan
7. Approved plan is implemented
```

## Sub-Skills

### comment-management
- Add comments with text selection context
- Categorize by type and priority
- Track resolution status

### plan-generation
- Analyze open comments for artifact
- Generate structured change plan
- Identify cross-document implications

## Comment Types

- **general**: General feedback or observation
- **clarification**: Something needs clarifying
- **correction**: Error that needs fixing
- **suggestion**: Improvement idea

## API Integration

```javascript
// Add comment
POST /api/comments
{
  artifact_type, artifact_name,
  selection_text, selection_start, selection_end,
  comment_text, comment_type, priority
}

// Generate plan from comments
POST /api/plans/generate
{
  artifact_type, artifact_name,
  scope: 'artifact' | 'all_open'
}

// Approve/reject plan
PUT /api/plans/:id/status
{ status: 'approved' | 'rejected' }
```

## Plan Generation Prompt

When generating a change plan, analyze comments and output:
```json
{
  "summary": "Brief overview of changes",
  "changes": [
    {
      "comment_id": 1,
      "change_type": "edit|add|remove|restructure",
      "location": "section or line reference",
      "proposed_text": "new content",
      "rationale": "why this change"
    }
  ],
  "consistency_implications": [
    {
      "document": "path to affected doc",
      "reason": "why update needed",
      "priority": "required|recommended"
    }
  ]
}
```

## Voice Requirements

When generating plans:
- Use bridge-building language (avoid partisan framing)
- Maintain practical idealism
- Reference specific principles/roles where applicable
- Preserve document structure and formatting
