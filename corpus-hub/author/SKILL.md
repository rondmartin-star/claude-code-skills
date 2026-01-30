# CorpusHub Author Skill

## Purpose

The Author skill enables creating new content drafts with AI assistance, iterating on drafts, and analyzing how new content affects the existing corpus.

## API Base

`http://localhost:3000`

---

## Generate a Draft

### Create a new draft with AI assistance
```bash
curl -X POST http://localhost:3000/api/drafts/generate \
  -H "Content-Type: application/json" \
  -d '{
    "content_type": "chapter",
    "title": "The Role of Infrastructure",
    "prompt": "Write a chapter exploring how modern infrastructure investment drives economic renewal, focusing on energy, transportation, and digital systems.",
    "target_location": "chapters/infrastructure",
    "context_artifacts": [
      {"type": "chapter", "name": "introduction"},
      {"type": "glossary", "name": "framework-terms"}
    ]
  }'
```

**Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `content_type` | string | yes | The artifact type for the new draft (e.g., `chapter`, `appendix`) |
| `title` | string | yes | Working title for the draft |
| `prompt` | string | yes | Detailed instructions for what to write |
| `target_location` | string | no | Where the artifact should live in the corpus structure |
| `context_artifacts` | array | no | Existing artifacts to reference for tone, terms, and continuity |

**Response:** Returns a draft object with `id`, `title`, `content`, `content_type`, `status`, and `created_at`.

The AI generation respects the corpus config's voice guidelines, framework terms, and style rules. Providing `context_artifacts` improves consistency with existing content.

---

## Manage Drafts

### List all drafts
```bash
curl http://localhost:3000/api/drafts
```
Returns all drafts with their status (`draft`, `review`, `approved`, `published`).

### View a specific draft
```bash
curl http://localhost:3000/api/drafts/{id}
```

### Update a draft
```bash
curl -X PUT http://localhost:3000/api/drafts/{id} \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# The Role of Infrastructure\n\nRevised content here...",
    "title": "Infrastructure and Economic Renewal"
  }'
```

**Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `content` | string | no | Updated draft content |
| `title` | string | no | Updated title |

---

## Analyze Implications

### Check how a draft affects the existing corpus
```bash
curl -X POST http://localhost:3000/api/drafts/{id}/analyze-implications
```

Returns an analysis including:
- **Term conflicts**: New terms that clash with existing framework terms
- **Thematic overlaps**: Sections that cover similar ground as existing artifacts
- **Cross-references**: Suggested references to/from existing artifacts
- **Consistency notes**: Potential voice or style deviations
- **Gap coverage**: Which corpus gaps the draft addresses

Use this before finalizing a draft to ensure it integrates well with the existing corpus.

---

## AI Editing Assistance

### Use AI to refine draft content
```bash
curl -X POST http://localhost:3000/api/claude \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Revise this draft section to better align with the assertive, forward-looking voice used in the introduction chapter.",
    "context": "The draft section text..."
  }'
```

This is the same AI endpoint used by editors, but authors typically use it for:
- Refining tone and voice
- Expanding outlines into full prose
- Tightening arguments
- Generating section transitions

---

## Typical Author Workflow

1. **Research**: `GET /api/artifacts` to understand existing corpus structure
2. **Generate**: `POST /api/drafts/generate` with detailed prompt and context
3. **Review draft**: `GET /api/drafts/{id}` to read the generated content
4. **Iterate**: `PUT /api/drafts/{id}` to refine, optionally using `POST /api/claude` for AI help
5. **Analyze**: `POST /api/drafts/{id}/analyze-implications` to check corpus fit
6. **Refine**: Address any implication issues found
7. **Submit**: Move draft to review status for reviewers to evaluate

## Tips

- Always provide `context_artifacts` when generating -- it dramatically improves consistency
- Use the glossary/framework-terms artifact as context to ensure correct terminology
- Run implication analysis early and often, not just at the end
- For long documents, generate section by section and combine
- The `target_location` field helps the system understand where the content fits in the corpus hierarchy
