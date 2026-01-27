# Navigation Patterns Reference

Complete patterns for implementing and testing navigation in Windows applications.

---

## Navigation Registry Format

### CLAUDE.md Navigation Section

```markdown
## Navigation

### Primary Navigation

**Location:** Base template sidebar

**Routes:**
- Home: `/` → Dashboard overview
- Properties: `/properties` → Properties list with search
  - Add Property: `/properties/new` → Property form
  - View Property: `/properties/{id}` → Property details
  - Edit Property: `/properties/{id}/edit` → Property form (populated)
- Bookings: `/bookings` → Bookings calendar view
  - New Booking: `/bookings/new` → Booking form
  - View Booking: `/bookings/{id}` → Booking details
  - Edit Booking: `/bookings/{id}/edit` → Booking form (populated)
- Guests: `/guests` → Guests list with search
  - Add Guest: `/guests/new` → Guest form
  - View Guest: `/guests/{id}` → Guest details + booking history
- Reports: `/reports` → Reports dashboard
  - Revenue Report: `/reports/revenue` → Revenue analytics
  - Occupancy Report: `/reports/occupancy` → Occupancy trends
- Settings: `/settings` → Settings page
  - Profile: `/settings/profile` → User profile
  - Security: `/settings/security` → Change password
- Logout: `/logout` → Clear session and return to login

### Navigation Entry Points

**Public Access (No Login Required):**
- Login: `/login` → Google OAuth login page

**User Access (All Authenticated Users):**
- All primary navigation routes

**Admin Access (Admin Role Only):**
- Admin Dashboard: `/admin` → Admin control panel
- User Management: `/admin/users` → Manage user roles

### Navigation Testing Checklist

- [ ] All primary nav links appear in sidebar
- [ ] All links lead to correct pages
- [ ] Active route highlighted in navigation
- [ ] Unauthorized routes redirect to home
- [ ] Logout clears session
```

---

## Multi-Level Navigation Patterns

### Pattern 1: Sidebar → Tabs → Cards

**Use Case:** Complex page with multiple sections

**Example:** Property Detail Page

```html
<!-- Sidebar: Main navigation -->
<nav class="sidebar">
  <a href="/" class="nav-item">Dashboard</a>
  <a href="/properties" class="nav-item active">Properties</a>
  <a href="/bookings" class="nav-item">Bookings</a>
</nav>

<!-- Tabs: Section navigation within page -->
<div class="tabs">
  <a href="/properties/{{ property.id }}" class="tab active">Details</a>
  <a href="/properties/{{ property.id }}/bookings" class="tab">Bookings</a>
  <a href="/properties/{{ property.id }}/photos" class="tab">Photos</a>
  <a href="/properties/{{ property.id }}/settings" class="tab">Settings</a>
</div>

<!-- Cards: Action navigation within section -->
<div class="actions">
  <a href="/properties/{{ property.id }}/edit" class="card">
    <h3>Edit Property</h3>
    <p>Update property details</p>
  </a>
  <a href="/bookings/new?property={{ property.id }}" class="card">
    <h3>Create Booking</h3>
    <p>Reserve this property</p>
  </a>
  <a href="/properties/{{ property.id }}/delete" class="card card-danger">
    <h3>Delete Property</h3>
    <p>Permanently remove</p>
  </a>
</div>
```

### Pattern 2: Hierarchical Navigation

**Use Case:** Deep navigation structure

**Example:** Admin → Users → Edit User → Permissions

```python
# Define navigation hierarchy in config
NAVIGATION_HIERARCHY = {
    "admin": {
        "label": "Admin",
        "path": "/admin",
        "children": {
            "users": {
                "label": "Users",
                "path": "/admin/users",
                "children": {
                    "edit": {
                        "label": "Edit User",
                        "path": "/admin/users/{id}/edit",
                        "children": {
                            "permissions": {
                                "label": "Permissions",
                                "path": "/admin/users/{id}/permissions"
                            }
                        }
                    }
                }
            }
        }
    }
}
```

---

## Breadcrumb Patterns

### Implementation: Breadcrumb Component

```html
<!-- templates/components/breadcrumbs.html -->
<nav class="breadcrumbs" aria-label="Breadcrumb">
  <ol>
    {% for crumb in breadcrumbs %}
      <li>
        {% if not loop.last %}
          <a href="{{ crumb.url }}">{{ crumb.label }}</a>
          <span class="separator">/</span>
        {% else %}
          <span class="current">{{ crumb.label }}</span>
        {% endif %}
      </li>
    {% endfor %}
  </ol>
</nav>
```

### Breadcrumb Generation

```python
# app/utils/breadcrumbs.py
from typing import List, Dict

def generate_breadcrumbs(path: str, params: dict = None) -> List[Dict[str, str]]:
    """
    Generate breadcrumbs from URL path.

    Examples:
    - /properties → [Home, Properties]
    - /properties/123 → [Home, Properties, Maple Street House]
    - /properties/123/edit → [Home, Properties, Maple Street House, Edit]
    """

    breadcrumbs = [{"label": "Home", "url": "/"}]

    # Parse path
    parts = [p for p in path.split("/") if p]

    if not parts:
        return breadcrumbs

    # Build breadcrumbs
    current_path = ""

    for i, part in enumerate(parts):
        current_path += f"/{part}"

        # Check if part is an ID (numeric)
        if part.isdigit():
            # Fetch object label from database
            prev_part = parts[i - 1] if i > 0 else ""
            label = get_object_label(prev_part, part, params)
        else:
            # Use capitalized part name
            label = part.replace("-", " ").title()

        breadcrumbs.append({
            "label": label,
            "url": current_path
        })

    return breadcrumbs


def get_object_label(resource_type: str, object_id: str, params: dict) -> str:
    """Get human-readable label for object ID."""

    if resource_type == "properties":
        from app.models import Property
        property = db.query(Property).filter(Property.id == int(object_id)).first()
        return property.name if property else f"Property {object_id}"

    if resource_type == "bookings":
        from app.models import Booking
        booking = db.query(Booking).filter(Booking.id == int(object_id)).first()
        return f"Booking #{booking.id}" if booking else f"Booking {object_id}"

    # Default: Use ID
    return f"{resource_type.title()} {object_id}"
```

### Usage in Routes

```python
from app.utils.breadcrumbs import generate_breadcrumbs

@router.get("/properties/{property_id}/edit")
def edit_property(property_id: int, request: Request, db: Session = Depends(get_db)):
    property = db.query(Property).filter(Property.id == property_id).first()

    breadcrumbs = generate_breadcrumbs(
        request.url.path,
        params={"property": property}
    )
    # Result: [
    #   {"label": "Home", "url": "/"},
    #   {"label": "Properties", "url": "/properties"},
    #   {"label": "Maple Street House", "url": "/properties/123"},
    #   {"label": "Edit", "url": "/properties/123/edit"}
    # ]

    return templates.TemplateResponse("properties/form.html", {
        "request": request,
        "property": property,
        "breadcrumbs": breadcrumbs
    })
```

---

## Active Route Highlighting

### Pattern 1: CSS Class Based

```html
<!-- Base template: app/templates/base.html -->
<nav class="sidebar">
  <a href="/" class="nav-item {% if request.url.path == '/' %}active{% endif %}">
    Dashboard
  </a>

  <a href="/properties" class="nav-item {% if request.url.path.startswith('/properties') %}active{% endif %}">
    Properties
  </a>

  <a href="/bookings" class="nav-item {% if request.url.path.startswith('/bookings') %}active{% endif %}">
    Bookings
  </a>
</nav>

<style>
.nav-item {
  color: #666;
  text-decoration: none;
  padding: 8px 16px;
  display: block;
}

.nav-item.active {
  color: #0066cc;
  background-color: #e6f2ff;
  border-left: 3px solid #0066cc;
}

.nav-item:hover {
  background-color: #f5f5f5;
}
</style>
```

### Pattern 2: Template Helper

```python
# app/templates_config.py
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

def is_active_route(request_path: str, route_pattern: str) -> bool:
    """Check if current route matches pattern."""
    if route_pattern == "/":
        return request_path == "/"
    return request_path.startswith(route_pattern)

templates.env.globals["is_active_route"] = is_active_route
```

```html
<!-- Usage in template -->
<nav class="sidebar">
  <a href="/" class="nav-item {{ 'active' if is_active_route(request.url.path, '/') else '' }}">
    Dashboard
  </a>

  <a href="/properties" class="nav-item {{ 'active' if is_active_route(request.url.path, '/properties') else '' }}">
    Properties
  </a>
</nav>
```

---

## Context-Aware Navigation

### Pattern: Adaptive Navigation Based on User State

```html
<!-- Base template with conditional navigation -->
<nav class="sidebar">
  <!-- Always visible -->
  <a href="/" class="nav-item">Dashboard</a>

  <!-- Admin only -->
  {% if user and user.role == 'ADMIN' %}
    <a href="/admin" class="nav-item">Admin</a>
    <a href="/admin/users" class="nav-item">Users</a>
  {% endif %}

  <!-- Authenticated users -->
  {% if user %}
    <a href="/profile" class="nav-item">Profile</a>
    <a href="/logout" class="nav-item">Logout</a>
  {% else %}
    <a href="/login" class="nav-item">Login</a>
  {% endif %}
</nav>
```

### Pattern: Contextual Actions

```html
<!-- Property detail page with context-aware actions -->
{% if user and user.role == 'ADMIN' %}
  <!-- Admin sees all actions -->
  <div class="actions">
    <a href="/properties/{{ property.id }}/edit" class="button">Edit</a>
    <a href="/properties/{{ property.id }}/delete" class="button button-danger">Delete</a>
    <a href="/bookings/new?property={{ property.id }}" class="button button-primary">Create Booking</a>
  </div>

{% elif user and user.role == 'STAFF' %}
  <!-- Staff sees limited actions -->
  <div class="actions">
    <a href="/bookings/new?property={{ property.id }}" class="button button-primary">Create Booking</a>
  </div>

{% else %}
  <!-- Public sees view only -->
  <div class="actions">
    <a href="/contact?subject=Inquiry about {{ property.name }}" class="button">Contact Us</a>
  </div>
{% endif %}
```

---

## Navigation Testing

### Test 1: All Primary Routes Reachable

```python
# tests/test_navigation.py
import pytest
from fastapi.testclient import TestClient

def test_all_primary_routes_reachable(client: TestClient, authenticated_user):
    """All primary navigation routes should be reachable."""

    primary_routes = [
        "/",
        "/properties",
        "/properties/new",
        "/bookings",
        "/bookings/new",
        "/guests",
        "/reports",
        "/settings"
    ]

    for route in primary_routes:
        response = client.get(route, cookies={"session": authenticated_user.session_token})

        assert response.status_code == 200, f"Route {route} returned {response.status_code}"
```

### Test 2: Navigation Links Present

```python
from bs4 import BeautifulSoup

def test_navigation_links_present(client: TestClient, authenticated_user):
    """Sidebar navigation should contain all expected links."""

    response = client.get("/", cookies={"session": authenticated_user.session_token})
    soup = BeautifulSoup(response.text, 'html.parser')

    sidebar = soup.find('nav', class_='sidebar')
    links = [a.get('href') for a in sidebar.find_all('a')]

    expected_links = ["/", "/properties", "/bookings", "/guests", "/reports", "/settings", "/logout"]

    for expected in expected_links:
        assert expected in links, f"Navigation missing link: {expected}"
```

### Test 3: Active Route Highlighted

```python
def test_active_route_highlighted(client: TestClient, authenticated_user):
    """Current route should have 'active' class."""

    response = client.get("/properties", cookies={"session": authenticated_user.session_token})
    soup = BeautifulSoup(response.text, 'html.parser')

    properties_link = soup.find('a', href='/properties')
    assert 'active' in properties_link.get('class', []), "Active route not highlighted"

    # Non-active routes should NOT have active class
    bookings_link = soup.find('a', href='/bookings')
    assert 'active' not in bookings_link.get('class', []), "Inactive route incorrectly highlighted"
```

### Test 4: Unauthorized Routes Redirect

```python
def test_admin_routes_require_admin_role(client: TestClient, regular_user):
    """Admin routes should redirect non-admin users."""

    admin_routes = [
        "/admin",
        "/admin/users",
        "/admin/users/1/edit"
    ]

    for route in admin_routes:
        response = client.get(route, cookies={"session": regular_user.session_token}, follow_redirects=False)

        assert response.status_code == 302, f"Route {route} should redirect non-admin"
        assert response.headers["location"] == "/" or response.headers["location"] == "/login"
```

### Test 5: Breadcrumbs Generated

```python
def test_breadcrumbs_generated_correctly(client: TestClient, authenticated_user, sample_property):
    """Breadcrumbs should show navigation hierarchy."""

    response = client.get(
        f"/properties/{sample_property.id}/edit",
        cookies={"session": authenticated_user.session_token}
    )
    soup = BeautifulSoup(response.text, 'html.parser')

    breadcrumbs = soup.find('nav', class_='breadcrumbs')
    crumbs = [li.get_text(strip=True) for li in breadcrumbs.find_all('li')]

    expected_crumbs = ["Home", "Properties", sample_property.name, "Edit"]

    for expected in expected_crumbs:
        assert any(expected in crumb for crumb in crumbs), f"Breadcrumb missing: {expected}"
```

---

## Navigation Documentation Template

```markdown
## Navigation

### Overview
Brief description of the navigation structure (sidebar, tabs, breadcrumbs, etc.)

### Primary Navigation

**Location:** {Where navigation appears}

**Routes:**
- {Label}: `{path}` → {Description}
  - {Sub-label}: `{sub-path}` → {Sub-description}

### Entry Points

**Public Access:**
- {List of public routes}

**Authenticated Access:**
- {List of authenticated routes}

**Admin Access:**
- {List of admin-only routes}

### Navigation Patterns

**Active Route:** {How active route is highlighted}
**Breadcrumbs:** {Where breadcrumbs appear}
**Mobile:** {Mobile navigation behavior}

### Testing

- [ ] All primary routes reachable
- [ ] Active route highlighted correctly
- [ ] Unauthorized routes redirect
- [ ] Breadcrumbs generate correctly
- [ ] Mobile navigation works
```

---

*End of Navigation Patterns Reference*
