# Author Orchestrator

## Purpose

Coordinates the Author role workflow: requesting Claude to draft new content, editing drafts, and analyzing framework implications before committing.

## Workflow

```
1. User requests new content (post, article, spec section)
2. Claude generates draft aligned with framework
3. User reviews and edits draft
4. User requests implication analysis
5. Claude identifies affected documents and consistency needs
6. User reviews implications (accept/modify/abandon)
7. Draft committed with accepted implications applied
```

## Sub-Skills

### draft-generation
- Generate content from user prompt
- Align with 7 principles
- Use established voice and terminology

### implication-analysis
- Analyze draft for new definitions
- Detect modified concept interpretations
- Identify documents needing cross-references

## Content Types

- **post**: Bluesky/social media post (300-500 words)
- **article**: SubStack article (800-1200 words)
- **specification_section**: Framework specification section
- **onboarding**: Coalition onboarding material

## API Integration

```javascript
// Generate draft
POST /api/drafts/generate
{
  content_type: "post|article|specification_section",
  title: "Draft Title",
  prompt: "What to write about",
  target_location: "optional path",
  context_artifacts: ["optional", "references"]
}

// Update draft
PUT /api/drafts/:id
{ content: "edited content", title: "updated title" }

// Analyze implications
POST /api/drafts/:id/analyze-implications

// Get drafts
GET /api/drafts
```

## Draft Generation Prompt

System context for draft generation:
```
You are drafting content for the America 4.0 democratic renewal framework.
Framework principles: [list]
Voice: Bridge-building, measured patriotism, practical idealism, future-focused.

Generate well-structured content that aligns with framework principles.
Include JSON alignment block at end:
{
  "principles_referenced": [],
  "roles_referenced": [],
  "terms_used": []
}
```

## Implication Analysis Output

```json
{
  "new_definitions": [
    {
      "term": "new term introduced",
      "definition": "how it's defined",
      "recommendation": "add_to_glossary|define_inline|no_action"
    }
  ],
  "modified_concepts": [
    {
      "concept": "existing concept",
      "assessment": "consistent|extension|conflict"
    }
  ],
  "affected_documents": [
    {
      "document": "path to doc",
      "reason": "why it should reference this",
      "priority": "required|recommended|optional"
    }
  ],
  "consistency_score": "high|medium|low"
}
```

## Voice Guidelines

All drafts must:
- Use "democratic renewal" not "saving democracy"
- Use "evidence-based governance" not "expert rule"
- Avoid partisan framing
- Balance aspiration with practicality
- Reference founding documents where appropriate
