---
name: windows-app-ui-design
description: >
  Design user interfaces through role-based workflow guides and interaction
  documentation. Produces page inventories, template hierarchies, form designs,
  and navigation flows. Use when: "design the UI", "create page layouts",
  "plan the user interface", "document user workflows", "design screens".
---

# Windows Application UI Design Skill

**Purpose:** Document user interaction patterns and design interface flows  
**Output:** Page inventories, template hierarchies, workflow guides, form specs  
**Size:** ~10 KB  
**Related Skills:** windows-app-requirements (input), windows-app-system-design

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Design the UI for..."
- "What pages do I need?"
- "Plan the user interface"
- "Document user workflows"
- "Design the screens"
- "How will users interact with..."
- "Create page layouts"
- "Plan the navigation"
- "Here's our logo"
- "Create a brand language"
- "Define the color scheme"
- "What should the app look like?"

**Context Indicators:**
- Requirements are already defined
- Data model may or may not exist yet
- Discussion is about user experience
- Need to document how users accomplish tasks
- User provides organization logo

## ❌ DO NOT LOAD WHEN

- Requirements not yet defined (use requirements skill first)
- User is asking about database schema (use system-design skill)
- User wants to implement code (use build skill)
- User wants to fix a bug (use build skill)

---

## When to Use This Skill

| User Says... | Action |
|--------------|--------|
| "Design the UI for..." | Start UI design process |
| "What pages do I need?" | Create page inventory |
| "Plan the user interface" | Full UI design workflow |
| "Document user workflows" | Role-based workflow guides |
| "Design the screens" | Page layouts and templates |

---

## UI Design Process Overview

```
Requirements → Brand Language → Page Inventory → Template Hierarchy → Workflow Guides → Form Specs
     ↓              ↓                ↓                   ↓                  ↓              ↓
 User Stories  Logo analysis   List all pages    Define templates   Document paths   Form fields
```

---

## Step 0: Establish Brand Language

**Before designing any UI elements, request the organization's logo to establish visual consistency.**

### Request the Logo

Ask the user:
> "Please upload your organization's logo. I'll use it to create a consistent brand language including color palette, typography, and component styling. If you don't have a logo yet, I can proceed with a neutral palette."

### Quick Process

1. **Extract colors** from logo (primary, secondary, accent)
2. **Derive palette** (light/dark variants, neutrals, semantic colors)
3. **Select typography** based on logo style
4. **Define component styling** (buttons, cards, forms)
5. **Create CSS variables** for consistent application

**For detailed templates and CSS examples:**
```
/mnt/skills/user/windows-app-ui-design/references/brand-language.md
```

### If No Logo Provided

Use neutral Bootstrap palette and document for later customization:
```css
--brand-primary: #0d6efd;
--brand-primary-light: #3d8bfd;
--brand-primary-dark: #0a58ca;
```

---

## Step 1: Create Page Inventory

Map user stories to pages:

**Page Inventory Template:**

```markdown
## Page Inventory

### Public Pages (No Auth Required)

| Page | URL | Template | Purpose | Stories |
|------|-----|----------|---------|---------|
| Login | /login | auth/login.html | User authentication | US-001 |
| Register | /register | auth/register.html | New user signup | US-002 |

### User Pages (Auth Required)

| Page | URL | Template | Purpose | Stories |
|------|-----|----------|---------|---------|
| Dashboard | / | dashboard.html | Overview, stats | US-010 |
| Item List | /items | items/list.html | Browse items | US-020 |
| Item Detail | /items/{id} | items/detail.html | View one item | US-021 |
| Item Create | /items/new | items/form.html | Create item | US-022 |
| Item Edit | /items/{id}/edit | items/form.html | Edit item | US-023 |

### Admin Pages (Admin Role Required)

| Page | URL | Template | Purpose | Stories |
|------|-----|----------|---------|---------|
| User List | /admin/users | admin/users.html | Manage users | US-050 |
| Settings | /admin/settings | admin/settings.html | App config | US-051 |
```

---

## Step 2: Design Template Hierarchy

**Standard Template Structure:**

```
templates/
├── base.html                 # Master layout (nav, footer, scripts)
├── dashboard.html            # Extends base
├── auth/
│   ├── login.html           # Extends base
│   └── register.html        # Extends base
├── items/
│   ├── list.html            # Extends base
│   ├── detail.html          # Extends base
│   └── form.html            # Extends base (used for create/edit)
├── admin/
│   ├── users.html           # Extends base
│   └── settings.html        # Extends base
├── partials/
│   ├── _flash.html          # Flash messages (include)
│   ├── _pagination.html     # Pagination controls
│   ├── _item_card.html      # Reusable item display
│   └── _confirm_modal.html  # Delete confirmation
├── help/
│   ├── index.html           # Help center home
│   ├── topic.html           # Individual topic
│   └── shortcuts.html       # Keyboard shortcuts
└── errors/
    ├── 404.html             # Not found
    └── 500.html             # Server error
```

**Base Template Structure:**

```html
<!DOCTYPE html>
<html lang="en" data-bs-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ app_name }}{% endblock %}</title>
    
    <!-- Theme initialization BEFORE CSS -->
    <script>[theme initialization]</script>
    
    <!-- Styles -->
    <link href="bootstrap.css" rel="stylesheet">
    <link href="/static/css/app.css" rel="stylesheet">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        [navigation structure]
    </nav>
    
    <!-- Flash Messages -->
    {% include "partials/_flash.html" %}
    
    <!-- Main Content -->
    <main class="container">
        {% block content %}{% endblock %}
    </main>
    
    <!-- Footer -->
    <footer>
        {{ app_name }} v{{ app_version }}
    </footer>
    
    <!-- Scripts -->
    <script src="bootstrap.js"></script>
    <script src="/static/js/app.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

---

## Step 3: Document Role-Based Workflows

For each user role, document their primary workflows:

**Workflow Guide Template:**

```markdown
## [Role Name] Workflow Guide

### Overview
[Brief description of what this role does in the system]

### Primary Tasks

#### 1. [Task Name]
**Goal:** [What the user wants to accomplish]
**Starting Point:** [Where they begin]
**Steps:**
1. Navigate to [location]
2. Click [button/link]
3. Fill in [form fields]
4. Submit with [button]
**Success Indicator:** [What they see when done]
**Related Pages:** [List of pages involved]

#### 2. [Task Name]
[Repeat pattern]

### Navigation Path
```
Dashboard → [Module] List → [Action] → Confirmation
```

### Common Scenarios
- **Scenario A:** [Description and path]
- **Scenario B:** [Description and path]

### Keyboard Shortcuts
| Shortcut | Action |
|----------|--------|
| F1 | Context help |
| Ctrl+S | Save form |
| Ctrl+N | New item |
```

**Example Role Workflow:**

```markdown
## Venue Coordinator Workflow Guide

### Overview
Venue Coordinators manage venue availability and approve booking requests
for their assigned venues.

### Primary Tasks

#### 1. Review Pending Requests
**Goal:** See all pending booking requests for my venues
**Starting Point:** Dashboard
**Steps:**
1. Look at "Pending Requests" card on dashboard
2. Click request to view details
3. Review date, time, and purpose
4. Click "Approve" or "Deny"
5. Add notes if denying
**Success Indicator:** Request moves to Approved/Denied list
**Related Pages:** Dashboard, Request Detail, My Venues

#### 2. Block Dates
**Goal:** Mark venue as unavailable for specific dates
**Starting Point:** Dashboard or Venue List
**Steps:**
1. Navigate to My Venues
2. Click venue name
3. Click "Block Dates" button
4. Select date range
5. Enter reason (optional)
6. Click "Save"
**Success Indicator:** Calendar shows blocked dates
**Related Pages:** Venue List, Venue Detail, Calendar

### Navigation Path
```
Dashboard → Pending Requests (2) → Request Detail → Approve/Deny
Dashboard → My Venues → Venue → Block Dates → Calendar
```

### Keyboard Shortcuts
| Shortcut | Action |
|----------|--------|
| F1 | Help for current page |
| A | Approve request (on detail page) |
| D | Deny request (on detail page) |
| Ctrl+B | Block dates (on venue page) |
```

---

## Step 4: Design Form Specifications

**Form Specification Template:**

```markdown
## Form: [Form Name]

**URL:** [/path/to/form]
**Purpose:** [What this form does]
**Access:** [Who can access]

### Fields

| Field | Type | Required | Validation | Default | Notes |
|-------|------|----------|------------|---------|-------|
| name | text | Yes | 1-100 chars | - | Displayed in lists |
| category | select | Yes | From API | First option | Dynamic options |
| description | textarea | No | Max 1000 | - | Markdown supported |
| due_date | date | No | Future only | Today | Date picker |
| priority | select | Yes | Fixed list | Medium | Low/Medium/High |
| is_active | checkbox | No | - | true | Toggle switch |

### Form Behavior

**On Load:**
- Populate dropdowns from /api/config/{key}
- Pre-fill with existing data (edit mode)
- Set focus to first field

**On Submit:**
- Validate all required fields
- Show inline errors
- Disable submit button during save
- Redirect to detail page on success
- Show error message on failure

### Layout

```
┌─────────────────────────────────────┐
│ [Form Title]                        │
├─────────────────────────────────────┤
│ Name:        [________________]     │
│ Category:    [▼ Select... ____]     │
│ Description: [________________]     │
│              [________________]     │
│ Due Date:    [📅 ___________]      │
│ Priority:    ○ Low ● Medium ○ High │
│ Active:      [✓]                   │
├─────────────────────────────────────┤
│        [Cancel]  [Save]             │
└─────────────────────────────────────┘
```
```

---

## Step 5: Navigation Structure

**Navigation Design Template:**

```markdown
## Navigation Structure

### Main Navigation (All Users)

```
┌─────────────────────────────────────────────────┐
│ [Logo] App Name    [Dashboard] [Items] [Reports]│
│                                    [User ▼] [🌙]│
└─────────────────────────────────────────────────┘
```

### Sidebar Navigation (If Used)

```
┌──────────────────┐
│ 📊 Dashboard     │
├──────────────────┤
│ 📦 Items         │
│   ├─ All Items   │
│   ├─ By Category │
│   └─ Archive     │
├──────────────────┤
│ 📈 Reports       │
├──────────────────┤
│ ⚙️ Settings      │ (Admin only)
│ 👥 Users         │ (Admin only)
└──────────────────┘
```

### Breadcrumb Pattern

```
Dashboard > Items > Electronics > Laptop XYZ
```

### Mobile Navigation

```
┌─────────────────────────────────────────────────┐
│ [≡]  App Name                           [User] │
└─────────────────────────────────────────────────┘

[≡] opens slide-out menu with full navigation
```
```

---

## Step 6: Component Library

**Standard UI Components:**

### Cards

```html
<div class="card">
    <div class="card-header">
        <h5 class="mb-0">[Title]</h5>
    </div>
    <div class="card-body">
        [Content]
    </div>
    <div class="card-footer">
        [Actions]
    </div>
</div>
```

### Data Tables

```html
<table class="table table-striped">
    <thead>
        <tr>
            <th>Column 1</th>
            <th>Column 2</th>
            <th class="text-end">Actions</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>[Data]</td>
            <td>[Data]</td>
            <td class="text-end">
                <a href="..." class="btn btn-sm btn-outline-primary">Edit</a>
                <button class="btn btn-sm btn-outline-danger">Delete</button>
            </td>
        </tr>
    </tbody>
</table>
```

### Action Buttons

| Context | Primary | Secondary | Danger |
|---------|---------|-----------|--------|
| Forms | Save | Cancel | - |
| Lists | New | - | Delete |
| Detail | Edit | Back | Delete |
| Confirmation | Confirm | Cancel | - |

### Status Badges

```html
<span class="badge bg-success">Active</span>
<span class="badge bg-warning text-dark">Pending</span>
<span class="badge bg-danger">Inactive</span>
<span class="badge bg-secondary">Archived</span>
```

---

## Step 7: Help System Design

**F1 Context Help:**

Every page must have a help topic:

| Page Type | Help Topic ID | Content |
|-----------|---------------|---------|
| Dashboard | dashboard | Overview of available actions |
| List | {module} | How to filter, search, navigate |
| Form (Create) | {module}_new | Field explanations, validation |
| Form (Edit) | {module}_edit | What can be changed |
| Detail | {module}_detail | Available actions from here |

**Field Help:**

Forms with complex fields include help icons:

```html
<label for="field" class="form-label" data-help-field="field_name">
    Field Label <span class="text-danger">*</span>
</label>
```

---

## UI Design Checklist

Before proceeding to Build phase:

- [ ] Brand language established (or neutral palette documented)
- [ ] Color palette defined with CSS variables
- [ ] Typography selected
- [ ] Page inventory complete (all pages listed)
- [ ] Template hierarchy defined
- [ ] Role-based workflow guides written
- [ ] Form specifications documented
- [ ] Navigation structure designed
- [ ] Standard components identified
- [ ] Help system topics listed
- [ ] User approved UI design

### Cross-Skill Validation

Before transitioning to **windows-app-build**:
- [ ] Every P0 user story has at least one page
- [ ] Every user role has a documented workflow
- [ ] Form fields align with system-design entity attributes
- [ ] Navigation provides access to all required features

**Validation with requirements skill:**
- [ ] Page inventory covers all user stories
- [ ] Workflows match acceptance criteria paths

**Validation with system-design skill:**
- [ ] Forms match entity field names exactly
- [ ] Dropdowns reference configuration options from data model

**If any item fails:** Resolve before loading build skill.

---

## Exit Gate Questions

Ask the user:

1. "Does this page inventory cover all the features?"
2. "Are the workflows intuitive for each role?"
3. "Is the navigation structure clear?"
4. "Are the form layouts appropriate?"

**When user confirms → Proceed to windows-app-build skill**

---

## UI Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Hardcoded dropdowns | Can't customize | Load from API |
| Too many clicks | Frustration | Flatten navigation |
| No breadcrumbs | Users get lost | Add breadcrumb trail |
| No action feedback | Uncertainty | Flash messages |
| Modal overload | Disruptive | Use inline editing |
| Tiny touch targets | Mobile unusable | Min 44x44px |
| Missing loading states | Appears broken | Spinners/skeletons |
| "Coming Soon" placeholders | Incomplete product | Remove or implement |
| Incomplete CRUD | Non-functional UI | Full create/read/update/delete |
| Non-functional reorder | Broken drag-drop | SortableJS + auto-save |
| Single-entity UI | Breaks with multiples | Show selector if >1 |
| JS sets placeholder not value | Empty form fields | Set `.value` property |

### Critical Rules

1. **No "Coming Soon"** - Never ship placeholder features. Remove from nav or implement.

2. **Complete CRUD** - Every entity needs: Create (form+validation), Read (list+detail), Update (edit form), Delete (confirmation), Reorder (drag-drop with auto-save).

3. **Multi-Entity UI** - If multiple venues/orgs possible, always show selector and pass entity ID to API calls.

---

*End of Windows Application UI Design Skill*
