# Role-Based Workflow Guide Templates

## Workflow Guide Template

Use this template when documenting workflows for each user role:

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

## Example Role Workflow

### Venue Coordinator Workflow Guide

**Overview:**
Venue Coordinators manage venue availability and approve booking requests
for their assigned venues.

**Primary Tasks:**

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

**Navigation Path:**
```
Dashboard → Pending Requests (2) → Request Detail → Approve/Deny
Dashboard → My Venues → Venue → Block Dates → Calendar
```

**Keyboard Shortcuts:**
| Shortcut | Action |
|----------|--------|
| F1 | Help for current page |
| A | Approve request (on detail page) |
| D | Deny request (on detail page) |
| Ctrl+B | Block dates (on venue page) |

## Form Specification Template

Use this template when documenting form designs:

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

## Navigation Structure Templates

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

## Help System Design

### F1 Context Help

Every page must have a help topic:

| Page Type | Help Topic ID | Content |
|-----------|---------------|---------|
| Dashboard | dashboard | Overview of available actions |
| List | {module} | How to filter, search, navigate |
| Form (Create) | {module}_new | Field explanations, validation |
| Form (Edit) | {module}_edit | What can be changed |
| Detail | {module}_detail | Available actions from here |

### Field Help

Forms with complex fields include help icons:

```html
<label for="field" class="form-label" data-help-field="field_name">
    Field Label <span class="text-danger">*</span>
</label>
```
