---
name: review-edit-author
description: >
  Universal content management with three roles: Reviewer (browse, comment, plan),
  Editor (modify with AI), Author (create drafts). Role-driven workflow based on
  corpus-config.json permissions. Use when: working with corpus content in any role.
---

# Review, Edit & Author

**Purpose:** Universal content management for corpus artifacts
**Size:** ~14 KB
**Type:** Core Pattern (Universal)

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Review this content"
- "Edit this artifact"
- "Create new draft"
- "Add comments to document"
- "Modify content with AI"

**Context Indicators:**
- Working with corpus artifacts
- Role-based content operations
- Reviewing or editing documents
- Creating new content

## ❌ DO NOT LOAD WHEN

- Just browsing corpus status (use corpus-detect)
- Managing configuration (use corpus-config)
- Administrative tasks (separate admin skill)

---

## Three Roles

### Role: Reviewer

**Capabilities:**
- Browse artifacts (read-only)
- Add structured comments
- Generate change plans
- Track review progress

**Cannot:**
- Modify content
- Create new artifacts
- Delete content

**Use When:**
- Reviewing content for approval
- Providing feedback
- Planning changes before implementation

### Role: Editor

**Capabilities:**
- All Reviewer capabilities, plus:
- Modify artifact content
- AI-assisted editing
- Version history management
- Implement change plans

**Cannot:**
- Delete artifacts (requires admin)

**Use When:**
- Implementing approved changes
- Refining existing content
- AI-assisted content improvement

### Role: Author

**Capabilities:**
- All Editor capabilities, plus:
- Create new drafts
- AI-assisted content generation
- Analyze framework implications
- Experimental writing

**Use When:**
- Creating new content from scratch
- Drafting new sections
- AI-generated content creation

---

## Role Determination

**From corpus-config.json:**
```json
{
  "roles": {
    "available": ["admin", "editor", "author", "reviewer", "viewer", "pending"],
    "defaultRole": "pending",
    "aiAccess": ["admin", "editor", "author"],
    "editAccess": ["admin", "editor", "author"]
  }
}
```

**Check user's role:**
```javascript
async function getUserRole(userId) {
  const response = await fetch(
    `http://localhost:3000/api/users/${userId}/role`
  );
  const data = await response.json();
  return data.role; // Returns: 'reviewer', 'editor', 'author', etc.
}

function canEdit(role, config) {
  return config.roles.editAccess.includes(role);
}

function canUseAI(role, config) {
  return config.roles.aiAccess.includes(role);
}
```

---

## Reviewer Workflow

### Browse Artifacts

**List all artifacts:**
```javascript
const response = await fetch('http://localhost:3000/api/artifacts');
const artifacts = await response.json();

console.log('Artifacts:');
artifacts.forEach(artifact => {
  console.log(`  - ${artifact.type}: ${artifact.title}`);
});
```

**View specific artifact:**
```javascript
const response = await fetch(
  `http://localhost:3000/api/artifacts/${type}/${name}`
);
const artifact = await response.json();

console.log(`Title: ${artifact.title}`);
console.log(`Type: ${artifact.type}`);
console.log(`Modified: ${artifact.updated_at}`);
console.log(`Content: ${artifact.content_html}`);
```

### Add Comments

**Comment types:**
- `suggestion` - Proposed improvement
- `issue` - Problem to fix
- `question` - Clarification needed
- `praise` - Positive feedback

**Add comment:**
```javascript
const response = await fetch('http://localhost:3000/api/comments', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    artifact_type: 'documentation',
    artifact_name: 'api-guide',
    comment_text: 'Consider adding code example here',
    comment_type: 'suggestion',
    priority: 'medium'
  })
});

const comment = await response.json();
console.log(`Comment added: ${comment.id}`);
```

**View comments:**
```javascript
const response = await fetch(
  `http://localhost:3000/api/comments/${type}/${name}`
);
const comments = await response.json();

comments.forEach(comment => {
  console.log(`[${comment.priority}] ${comment.comment_type}`);
  console.log(`  ${comment.comment_text}`);
  console.log(`  Status: ${comment.status}`);
});
```

### Generate Change Plans

**Create plan from comments:**
```javascript
const response = await fetch('http://localhost:3000/api/plans/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    comment_ids: [1, 3, 7, 12],
    scope: 'moderate'
  })
});

const plan = await response.json();

console.log(`Plan: ${plan.title}`);
console.log(`Impact: ${plan.estimated_impact}`);
console.log(`Changes: ${plan.changes.length} proposed`);
```

**Plan scopes:**
- `narrow` - Address specific comments only
- `moderate` - Include related improvements
- `broad` - Comprehensive revision

---

## Editor Workflow

### Modify Content

**Update artifact:**
```javascript
const response = await fetch(
  `http://localhost:3000/api/artifacts/${type}/${name}`,
  {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      content_html: updatedHTML,
      change_summary: 'Implemented feedback from review #47'
    })
  }
);

const result = await response.json();
console.log(`Updated: ${result.artifact.title}`);
console.log(`Version: ${result.version}`);
```

### AI-Assisted Editing

**Check AI access:**
```javascript
if (!canUseAI(userRole, corpusConfig)) {
  console.error('AI access requires editor, author, or admin role');
  return;
}
```

**AI improvement request:**
```javascript
const response = await fetch('http://localhost:3000/api/ai/improve', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    artifact_type: 'documentation',
    artifact_name: 'api-guide',
    improvement_type: 'clarity',
    context: 'Technical audience, focus on code examples'
  })
});

const improved = await response.json();
console.log('AI Suggestions:');
console.log(improved.suggestions);
```

**Improvement types:**
- `clarity` - Make content clearer
- `conciseness` - Reduce wordiness
- `completeness` - Fill gaps
- `consistency` - Align with framework terms
- `voice` - Match voice attributes

### Implement Change Plans

**Execute plan:**
```javascript
const response = await fetch(`http://localhost:3000/api/plans/${planId}/execute`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    approve_changes: true,
    backup_before: true
  })
});

const result = await response.json();

console.log(`Executed: ${result.changes_applied} changes`);
console.log(`Backup: ${result.backup_path}`);
```

### Version History

**View versions:**
```javascript
const response = await fetch(
  `http://localhost:3000/api/artifacts/${type}/${name}/versions`
);
const versions = await response.json();

versions.forEach(v => {
  console.log(`Version ${v.version}: ${v.created_at}`);
  console.log(`  ${v.change_summary}`);
});
```

**Restore version:**
```javascript
await fetch(
  `http://localhost:3000/api/artifacts/${type}/${name}/restore/${versionId}`,
  { method: 'POST' }
);

console.log('Restored to previous version');
```

---

## Author Workflow

### Create New Drafts

**Create artifact:**
```javascript
const response = await fetch('http://localhost:3000/api/artifacts', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    type: 'documentation',
    name: 'new-feature-guide',
    title: 'New Feature Guide',
    content_html: '<h1>New Feature Guide</h1>...',
    status: 'draft'
  })
});

const artifact = await response.json();
console.log(`Created: ${artifact.id}`);
```

**Draft statuses:**
- `draft` - Work in progress
- `review` - Ready for review
- `approved` - Approved for publication
- `published` - Live content

### AI-Assisted Writing

**Generate content:**
```javascript
const response = await fetch('http://localhost:3000/api/ai/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    prompt: 'Write a guide for API authentication',
    artifact_type: 'documentation',
    framework_context: true,
    voice_attributes: ['professional', 'technical', 'clear'],
    length: 'medium'
  })
});

const generated = await response.json();
console.log('AI Generated Content:');
console.log(generated.content_html);
```

### Analyze Framework Implications

**Check framework alignment:**
```javascript
const response = await fetch('http://localhost:3000/api/artifacts/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    content_html: draftContent,
    check_framework_terms: true,
    check_voice: true
  })
});

const analysis = await response.json();

console.log('Framework Analysis:');
console.log(`  Terms used: ${analysis.framework_terms.length}`);
console.log(`  Voice alignment: ${analysis.voice_score}%`);
console.log(`  Issues: ${analysis.issues.length}`);
```

---

## Configuration-Driven Behavior

### Voice Attributes

**Applied to AI operations:**
```json
{
  "voice": {
    "attributes": ["professional", "technical", "clear"],
    "avoid": ["marketing speak", "jargon"],
    "preferredTerms": {
      "OAuth 2.0 with cookie separation": "OAuth"
    }
  }
}
```

**Usage:**
```javascript
// AI respects voice attributes automatically
const aiResponse = await generateContent({
  voice: corpusConfig.voice
});
```

### Framework Terms

**Auto-suggest during editing:**
```javascript
function suggestFrameworkTerms(content, framework) {
  const suggestions = [];

  framework.categories.forEach(category => {
    category.terms.forEach(term => {
      if (!content.includes(term)) {
        // Check if related terms exist
        const variants = findVariants(content, term);
        if (variants.length > 0) {
          suggestions.push({
            term,
            canonical: term,
            found: variants,
            category: category.label
          });
        }
      }
    });
  });

  return suggestions;
}
```

---

## Permissions & Safety

### Role-Based Access Control

```javascript
async function checkPermission(operation, userRole, config) {
  const permissions = {
    browse: ['admin', 'editor', 'author', 'reviewer', 'viewer'],
    comment: ['admin', 'editor', 'author', 'reviewer'],
    edit: config.roles.editAccess,
    create: config.roles.aiAccess,
    ai: config.roles.aiAccess,
    delete: ['admin']
  };

  if (!permissions[operation].includes(userRole)) {
    throw new Error(`Role '${userRole}' cannot perform '${operation}'`);
  }

  return true;
}
```

### Backup Before Modification

```javascript
async function safeModify(artifactId, newContent) {
  // Always backup before editing
  await fetch(`http://localhost:3000/api/artifacts/${artifactId}/backup`, {
    method: 'POST'
  });

  // Then modify
  await fetch(`http://localhost:3000/api/artifacts/${artifactId}`, {
    method: 'PUT',
    body: JSON.stringify({ content_html: newContent })
  });
}
```

---

## Quick Reference

**Check role:**
```javascript
const role = await getUserRole(userId);
const canEdit = corpusConfig.roles.editAccess.includes(role);
```

**Add comment (reviewer):**
```javascript
await addComment(type, name, 'suggestion', 'Add example here');
```

**Edit content (editor):**
```javascript
await updateArtifact(type, name, newContent, 'Improved clarity');
```

**Create draft (author):**
```javascript
await createArtifact('documentation', 'new-guide', title, content);
```

**AI assist (editor/author):**
```javascript
const improved = await aiImprove(type, name, 'clarity');
```

---

*End of Review, Edit & Author*
*Part of v4.0.0 Universal Skills Ecosystem*
*Consolidates: corpus-hub/reviewer, corpus-hub/editor, corpus-hub/author, america40/review, america40/edit, america40/author*
