# Edit Orchestrator

## Purpose

Coordinates the Editor role workflow: making direct changes to artifacts with real-time consistency monitoring and version control.

## Workflow

```
1. User selects artifact to edit
2. Editor panel opens with current content
3. User makes changes (with optional Claude assistance)
4. User clicks "Check Consistency" to preview implications
5. Claude analyzes changes against framework terms
6. Implied updates shown to user
7. User saves changes (version created automatically)
8. Changes viewable on refresh
```

## Sub-Skills

### direct-edit
- Load artifact content into editor
- Handle Claude-assisted editing requests
- Save with version creation

### consistency-monitor
- Detect changes to framework terms
- Identify affected documents
- Generate implied update recommendations

## Framework Terms Monitored

### Principles (7)
- Human Dignity and Inclusion
- Social and Ecological Interconnection
- Economic Justice and Opportunity
- Democratic Governance and Rule of Law
- Global Citizenship and Leadership
- Creative and Cultural Flourishing
- Evidence-Based Decision Making

### Roles (14)
Citizen, Representative, Expert, Educator, Facilitator, Democracy Auditor,
Communicator, Contributor, Community Builder, Bridge Builder,
Cultural Creator, Protector, Systems Designer, Implementer

### Key Terms
Variable Geometry, Curated Failure, Attractor Theory, Democracy Auditor,
America 1.0/2.0/3.0/4.0

## API Integration

```javascript
// Preview consistency implications
POST /api/artifacts/:type/:name/preview-changes
{ newContent: "edited content" }

// Save with versioning
PUT /api/artifacts/:type/:name
{ content: "new content", change_summary: "description" }

// View version history
GET /api/artifacts/:type/:name/history

// Revert to version
POST /api/artifacts/:type/:name/revert/:version
```

## Consistency Analysis Output

```json
{
  "changes": [
    {
      "type": "principle|role|key_term",
      "term": "affected term",
      "change": "added|removed|modified",
      "count_change": 2
    }
  ],
  "implications": [
    {
      "document_pattern": "affected document path",
      "reason": "why update needed",
      "severity": "critical|warning|info"
    }
  ],
  "consistency_risk": "high|medium|low"
}
```

## Version Control

- Every save creates a new version
- Content hash ensures integrity
- Change source tracked (direct_edit, revert, plan)
- Full rollback capability
