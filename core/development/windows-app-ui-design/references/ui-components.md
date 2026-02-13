# UI Components and Templates

## Template Hierarchy

### Standard Template Structure

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

## Base Template Structure

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

## Page Inventory Template

Use this template when documenting all pages:

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

## Component Library

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

### Flash Messages

```html
<!-- partials/_flash.html -->
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    <div class="container mt-3">
      {% for category, message in messages %}
        <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
          {{ message }}
          <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
      {% endfor %}
    </div>
  {% endif %}
{% endwith %}
```

### Pagination

```html
<!-- partials/_pagination.html -->
<nav aria-label="Page navigation">
  <ul class="pagination justify-content-center">
    <li class="page-item {% if not prev_page %}disabled{% endif %}">
      <a class="page-link" href="?page={{ prev_page }}">Previous</a>
    </li>
    {% for p in range(1, pages + 1) %}
      <li class="page-item {% if p == page %}active{% endif %}">
        <a class="page-link" href="?page={{ p }}">{{ p }}</a>
      </li>
    {% endfor %}
    <li class="page-item {% if not next_page %}disabled{% endif %}">
      <a class="page-link" href="?page={{ next_page }}">Next</a>
    </li>
  </ul>
</nav>
```

### Confirmation Modal

```html
<!-- partials/_confirm_modal.html -->
<div class="modal fade" id="confirmModal" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Confirm Action</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">
        Are you sure you want to proceed?
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
        <button type="button" class="btn btn-danger" id="confirmButton">Confirm</button>
      </div>
    </div>
  </div>
</div>
```

### Loading Spinner

```html
<div class="text-center my-5">
  <div class="spinner-border text-primary" role="status">
    <span class="visually-hidden">Loading...</span>
  </div>
</div>
```

### Empty State

```html
<div class="text-center my-5">
  <p class="text-muted">No items found</p>
  <a href="/items/new" class="btn btn-primary">Create First Item</a>
</div>
```

## Form Components

### Text Input

```html
<div class="mb-3">
  <label for="name" class="form-label">Name <span class="text-danger">*</span></label>
  <input type="text" class="form-control" id="name" name="name" required>
  <div class="invalid-feedback">Please provide a name.</div>
</div>
```

### Select Dropdown

```html
<div class="mb-3">
  <label for="category" class="form-label">Category <span class="text-danger">*</span></label>
  <select class="form-select" id="category" name="category" required>
    <option value="">Select...</option>
    <option value="1">Category 1</option>
    <option value="2">Category 2</option>
  </select>
  <div class="invalid-feedback">Please select a category.</div>
</div>
```

### Textarea

```html
<div class="mb-3">
  <label for="description" class="form-label">Description</label>
  <textarea class="form-control" id="description" name="description" rows="3"></textarea>
  <div class="form-text">Optional details about this item.</div>
</div>
```

### Date Picker

```html
<div class="mb-3">
  <label for="due_date" class="form-label">Due Date</label>
  <input type="date" class="form-control" id="due_date" name="due_date">
</div>
```

### Checkbox

```html
<div class="mb-3 form-check">
  <input type="checkbox" class="form-check-input" id="is_active" name="is_active" checked>
  <label class="form-check-label" for="is_active">Active</label>
</div>
```

### Radio Buttons

```html
<div class="mb-3">
  <label class="form-label">Priority</label>
  <div class="form-check">
    <input class="form-check-input" type="radio" name="priority" id="priority_low" value="Low">
    <label class="form-check-label" for="priority_low">Low</label>
  </div>
  <div class="form-check">
    <input class="form-check-input" type="radio" name="priority" id="priority_medium" value="Medium" checked>
    <label class="form-check-label" for="priority_medium">Medium</label>
  </div>
  <div class="form-check">
    <input class="form-check-input" type="radio" name="priority" id="priority_high" value="High">
    <label class="form-check-label" for="priority_high">High</label>
  </div>
</div>
```
