# America 4.0 Reference Hub UI Components

## Design System

### Colors (CSS Variables)

```css
:root {
  /* Primary */
  --civic-blue: #0A3161;        /* Headers, primary actions */
  --historical-gold: #BE9958;   /* America 4.0 branding, highlights */

  /* Semantic */
  --community-orange: #E45B2D;  /* Comments, alerts */
  --renewal-green: #2E7D4C;     /* Success, resolved */
  --alert-red: #CF3F4C;         /* Errors, critical */
  --balance-yellow: #FFC857;    /* Warnings */

  /* Neutrals */
  --white: #FFFFFF;
  --off-white: #F8F7F4;
  --light-gray: #E8E6E1;
  --medium-gray: #9B9890;
  --dark-gray: #2D2D2D;
}
```

### Typography

```css
--font-primary: 'Open Sans', sans-serif;    /* UI, body */
--font-secondary: 'Merriweather', serif;    /* Headings, emphasis */
```

---

## Component Library

### Role Selector

```html
<div class="role-selector">
  <button class="role-btn" data-role="viewer">View</button>
  <button class="role-btn active" data-role="reviewer">Review</button>
  <button class="role-btn" data-role="editor">Edit</button>
  <button class="role-btn" data-role="author">Author</button>
</div>
```

**States:**
- `.role-btn` - Default state
- `.role-btn.active` - Currently selected role
- `.role-btn:hover` - Hover state

---

### Review Toolbar

```html
<div class="review-toolbar" id="reviewToolbar">
  <span class="review-toolbar-label">Review Mode:</span>
  <button class="btn btn-secondary" onclick="toggleCommentPanel()">
    Comments <span class="comment-count-badge">5</span>
  </button>
  <button class="btn btn-primary" onclick="generatePlan()">
    Generate Change Plan
  </button>
</div>
```

**Visibility:** Only shown when `currentRole === 'reviewer'`

---

### Comment Panel

```html
<div class="comment-panel" id="commentPanel">
  <div class="comment-panel-header">
    <span class="comment-panel-title">Comments</span>
    <button class="comment-close-btn">&times;</button>
  </div>
  <div class="comment-list" id="commentList">
    <!-- Comment items rendered here -->
  </div>
</div>
```

**States:**
- Default: `transform: translateX(100%)` (hidden)
- `.comment-panel.open`: `transform: translateX(0)` (visible)

---

### Comment Item

```html
<div class="comment-item" data-comment-id="123">
  <div class="comment-header">
    <span class="comment-user">User Name</span>
    <span class="comment-time">2h ago</span>
  </div>
  <div class="comment-selection">"selected text..."</div>
  <div class="comment-text">Comment content here</div>
  <div class="comment-actions">
    <button class="btn btn-secondary">Resolve</button>
  </div>
</div>
```

**States:**
- `.comment-item` - Open comment (orange left border)
- `.comment-item.resolved` - Resolved (green left border, opacity: 0.7)

---

### Add Comment Popup

```html
<div class="add-comment-popup" id="addCommentPopup">
  <div class="comment-selection" id="selectedTextPreview"></div>
  <select class="comment-type-select" id="commentType">
    <option value="general">General Comment</option>
    <option value="clarification">Needs Clarification</option>
    <option value="correction">Correction Needed</option>
    <option value="suggestion">Suggestion</option>
  </select>
  <textarea id="commentText" placeholder="Enter your comment..."></textarea>
  <div class="add-comment-popup-actions">
    <button class="btn btn-secondary">Cancel</button>
    <button class="btn btn-primary">Add Comment</button>
  </div>
</div>
```

**Position:** Absolute, positioned near text selection

---

### Comment Highlight

```html
<mark class="comment-highlight" data-comment-id="123">
  highlighted text
</mark>
```

**Behavior:** Clicking scrolls to and highlights corresponding comment in panel.

---

### Consistency Panel

```html
<div class="consistency-panel" id="consistencyPanel">
  <div class="consistency-header">
    <span class="consistency-title">Consistency Analysis</span>
    <span class="consistency-badge medium">Medium Risk</span>
  </div>
  <div id="consistencyContent">
    <div class="consistency-item warning">
      <strong>principle:</strong> Human Dignity (added 2 references)
    </div>
  </div>
</div>
```

**Badges:**
- `.consistency-badge.low` - Green
- `.consistency-badge.medium` - Yellow
- `.consistency-badge.high` - Red

**Items:**
- `.consistency-item.critical` - Red left border
- `.consistency-item.warning` - Yellow left border
- `.consistency-item.info` - Blue left border

---

### Buttons

```html
<button class="btn btn-primary">Primary Action</button>
<button class="btn btn-secondary">Secondary Action</button>
<button class="btn btn-success">Success Action</button>
```

**Sizes:** Standard 8px 16px padding

---

### Toast Notifications

```html
<div class="toast" id="toast">Message here</div>
```

**States:**
- `.toast` - Hidden
- `.toast.show` - Visible (bottom-right)
- `.toast.success` - Green background
- `.toast.error` - Red background

---

### Editor Panel

```html
<div class="editor-panel" id="editorPanel">
  <div class="editor-header">
    <h3>Edit Content</h3>
    <div>
      <button class="btn btn-secondary">Cancel</button>
      <button class="btn btn-secondary">Check Consistency</button>
      <button class="btn btn-success">Save Changes</button>
    </div>
  </div>

  <div class="consistency-panel"></div>

  <div class="claude-input">
    <input type="text" class="claude-prompt" placeholder="Ask Claude...">
    <button class="btn btn-primary">Ask Claude</button>
  </div>

  <div class="claude-response">
    <div class="claude-response-header">Claude's Suggestion:</div>
    <div id="claudeResponseText"></div>
    <button class="btn btn-secondary">Apply Suggestion</button>
  </div>

  <textarea class="editor-textarea"></textarea>
</div>
```

---

### Artifact Viewer

```html
<div class="artifact-viewer">
  <div class="viewer-toolbar">
    <span class="viewer-title">Artifact Name</span>
    <div class="viewer-actions">
      <button class="btn btn-secondary">Print</button>
      <button class="btn btn-secondary">Download PDF</button>
      <button class="btn btn-secondary">Open in Tab</button>
      <button class="btn btn-primary" id="editBtn">Edit</button>
    </div>
  </div>
  <div id="artifactContent">
    <!-- Content rendered here -->
  </div>
</div>
```

---

### Sidebar Artifact List

```html
<li class="artifact-item" data-path="type/name.html">
  <span class="artifact-icon">📄</span>
  <span class="artifact-name">Document Name</span>
  <span class="artifact-ext">.html</span>
</li>
```

**States:**
- `.artifact-item` - Default
- `.artifact-item.active` - Selected (blue background)
- `.artifact-item:hover` - Hover (light background)

---

## Responsive Behavior

### Breakpoint: 900px

```css
@media (max-width: 900px) {
  .sidebar {
    width: 100%;
    position: static;
  }
  .main-content {
    margin-left: 0;
  }
  .layout {
    flex-direction: column;
  }
}
```

---

## Animations

### Spin (Loading)
```css
@keyframes spin {
  to { transform: rotate(360deg); }
}
```

### Pulse (Highlight)
```css
@keyframes pulse {
  0%, 100% { background-color: var(--off-white); }
  50% { background-color: rgba(228, 91, 45, 0.2); }
}
```
