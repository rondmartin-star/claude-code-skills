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
**Related Skills:** windows-app-requirements (input), windows-app-system-design, windows-app-ui-testing (verification)

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

1. Extract colors from logo (primary, secondary, accent)
2. Derive palette (light/dark variants, neutrals, semantic colors)
3. Select typography based on logo style
4. Define component styling (buttons, cards, forms)
5. Create CSS variables for consistent application

**For detailed brand language templates and CSS examples:**
```
references/brand-language.md
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

Map user stories to pages.

**For detailed page inventory template:**
```
references/ui-components.md
```

Quick reference structure:
- **Public Pages** (no auth): Login, Register
- **User Pages** (auth required): Dashboard, List, Detail, Create/Edit
- **Admin Pages** (admin role): User Management, Settings

Columns to document:
- Page name
- URL path
- Template file
- Purpose
- Related user stories

---

## Step 2: Design Template Hierarchy

**Standard Template Structure:**

```
templates/
├── base.html                 # Master layout (nav, footer, scripts)
├── dashboard.html            # Extends base
├── auth/                     # Authentication pages
├── items/                    # Entity-specific pages
├── admin/                    # Admin pages
├── partials/                 # Reusable components
├── help/                     # Help system
└── errors/                   # Error pages
```

**For detailed template structure and base template HTML:**
```
references/ui-components.md
```

**Template Principles:**
- One base.html extends by all pages
- Partials for reusable components (_flash, _pagination, etc.)
- Entity pages grouped by folder
- Help and error pages in dedicated folders

---

## Step 3: Document Role-Based Workflows

For each user role, document their primary workflows.

**For detailed workflow guide template and examples:**
```
references/workflow-templates.md
```

Quick workflow structure:
- **Overview:** What this role does
- **Primary Tasks:** Goal, starting point, steps, success indicator
- **Navigation Path:** Visual flow diagram
- **Common Scenarios:** Real-world examples
- **Keyboard Shortcuts:** Productivity shortcuts

---

## Step 4: Design Form Specifications

**For detailed form specification template:**
```
references/workflow-templates.md
```

Quick form documentation checklist:
- [ ] URL and purpose
- [ ] Field list (name, type, required, validation, default)
- [ ] Form behavior (on load, on submit)
- [ ] Layout diagram
- [ ] Error handling
- [ ] Success/redirect behavior

**Form Field Types:**
- Text, textarea, select, date, checkbox, radio
- All required fields marked with (*)
- Validation rules documented
- Default values specified

---

## Step 5: Navigation Structure

**Navigation Design Quick Reference:**

**Main Navigation:**
- Horizontal top nav with logo, main sections, user menu, theme toggle
- Mobile: Hamburger menu with slide-out

**Sidebar Navigation (optional):**
- Hierarchical menu with sections
- Role-based visibility

**Breadcrumbs:**
- Show current location in hierarchy
- Clickable path back to parent pages

**For detailed navigation templates:**
```
references/workflow-templates.md
```

---

## Step 6: Component Library

**Standard UI Components:**

**For complete component library with HTML examples:**
```
references/ui-components.md
```

Quick reference:
- **Cards:** Header, body, footer structure
- **Tables:** Striped tables with action columns
- **Buttons:** Primary, secondary, danger by context
- **Badges:** Status indicators (success, warning, danger)
- **Forms:** Input, select, textarea, date, checkbox, radio
- **Modals:** Confirmation dialogs
- **Flash messages:** Success/error notifications
- **Pagination:** Page navigation controls

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

Forms with complex fields include help icons (data-help-field attribute).

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

## Implementation Verification with Playwright

**Critical Insight:** UI design → code → Playwright verification

After implementing UI designs in the build phase, use **Playwright** to verify the implementation matches the design specifications.

### Why Playwright for UI Verification

**Problem:** Claude Code is bad at pixel-perfect UI when looking at code alone.

**Solution:** Use Playwright to view the **rendered page** in browser, not just code files.

### Visual Iteration Pattern

```
Design Phase (this skill):
1. Create page mockups and specifications
2. Document exact layouts, colors, spacing
3. Approve design with user

Build Phase (windows-app-build):
4. Implement HTML/CSS/JS
5. Load Playwright MCP: /plugin playwright
6. "Spin out Playwright browser, open localhost"
7. Compare rendered page to design spec
8. Make adjustments based on visual feedback
9. Repeat until pixel-perfect
```

### When to Load Playwright Skill

**After build implements UI, load `windows-app-ui-testing` skill to:**
- Verify implementation matches design spec
- Test responsive layouts (mobile/tablet/desktop)
- Validate interactive behaviors (dropdowns, modals, forms)
- Take screenshots for documentation
- Create visual regression tests

### Example Verification Workflow

```javascript
// After implementing login page from design spec

await page.goto('http://localhost:3000/login')

// Verify layout matches design
await expect(page.locator('.login-form')).toHaveCSS('max-width', '400px')
await expect(page.locator('h1')).toHaveText('Welcome Back')

// Verify colors match brand palette
await expect(page.locator('.btn-primary')).toHaveCSS(
  'background-color',
  'rgb(13, 110, 253)'  // --brand-primary from design
)

// Take screenshot for design approval
await page.screenshot({ path: 'login-implemented.png' })
```

### Handoff to Build Phase

When transitioning to implementation:
1. **windows-app-build** implements the HTML/CSS/JS
2. **windows-app-ui-testing** verifies it matches design
3. Iterate visually using Playwright browser
4. User approves final implementation

**Key Rule:** Never approve UI implementation without viewing in Playwright browser.

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

## Reference Files

**Detailed templates and examples:**
- `references/brand-language.md` - Color palette, typography, CSS variables
- `references/workflow-templates.md` - Workflow guides, form specs, navigation
- `references/ui-components.md` - Template hierarchy, base template, component library

---

*End of Windows Application UI Design Skill*
