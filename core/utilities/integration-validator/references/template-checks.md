# Template Inheritance Validation Reference

Detailed procedures for validating Jinja2 template block inheritance.

---

## Template Hierarchy

### UCC-PMS Template Structure

```
templates/
├── base.html                    # Root template (public pages)
│   ├── content                  # Main content area
│   ├── extra_js                 # Additional JavaScript
│   ├── extra_css                # Additional CSS
│   └── chart_js                 # Chart.js include
│
├── admin/
│   └── base.html                # Admin layout (extends base.html)
│       ├── admin_content        # Admin page content
│       ├── page_title           # Page heading text
│       ├── page_actions         # Header action buttons
│       ├── breadcrumb           # Navigation breadcrumb
│       ├── extra_js             # Page-specific JavaScript
│       └── extra_css            # Page-specific CSS
│
├── public/                      # Public pages (extend base.html)
│   └── *.html                   # Use: content, extra_js
│
└── admin/
    ├── requests/*.html          # Use: admin_content, page_title
    ├── assets/*.html            # Use: admin_content, page_title
    ├── venues/*.html            # Use: admin_content, page_title
    └── reports/*.html           # Use: admin_content, extra_js
```

---

## Block Validation Commands

### Find all block definitions

```bash
# All block definitions (including endblock)
grep -rn "{% block" app/templates/ --include="*.html"

# Just opening blocks (without endblock)
grep -rn "{% block" app/templates/ --include="*.html" | grep -v endblock

# Blocks in admin templates only
grep -rn "{% block" app/templates/admin/ --include="*.html" | grep -v endblock
```

### Detect wrong block names

```bash
# Admin templates using 'content' instead of 'admin_content'
grep -rn "{% block content %}" app/templates/admin/ --include="*.html"
# Should return ZERO results

# Admin templates using 'scripts' instead of 'extra_js'
grep -rn "{% block scripts %}" app/templates/admin/ --include="*.html"
# Should return ZERO results

# Templates with {{ super() }} - verify parent has block
grep -rn "{{ super() }}" app/templates/ --include="*.html"
```

### Validate block closure

```bash
# Find unclosed blocks (basic check)
for f in $(find app/templates -name "*.html"); do
    opens=$(grep -c "{% block" "$f" || echo 0)
    closes=$(grep -c "{% endblock" "$f" || echo 0)
    if [ "$opens" != "$closes" ]; then
        echo "MISMATCH: $f (opens=$opens, closes=$closes)"
    fi
done
```

---

## Common Mistakes

### Mistake 1: Wrong block name in admin template

**Wrong:**
```html
{% extends "admin/base.html" %}
{% block content %}  <!-- WRONG! -->
<div>Page content</div>
{% endblock %}
```

**Correct:**
```html
{% extends "admin/base.html" %}
{% block admin_content %}  <!-- CORRECT -->
<div>Page content</div>
{% endblock %}
```

**Symptom:** Sidebar missing, page content replaces entire admin layout

### Mistake 2: Wrong JavaScript block name

**Wrong:**
```html
{% block scripts %}
<script src="custom.js"></script>
{% endblock %}
```

**Correct:**
```html
{% block extra_js %}
<script src="custom.js"></script>
{% endblock %}
```

**Symptom:** Custom JavaScript doesn't load

### Mistake 3: Missing {{ super() }}

**Wrong:**
```html
{% block extra_js %}
<script src="custom.js"></script>
{% endblock %}
```
This replaces ALL parent JavaScript.

**Correct (if parent scripts needed):**
```html
{% block extra_js %}
{{ super() }}
<script src="custom.js"></script>
{% endblock %}
```

### Mistake 4: Block name typo

**Wrong:**
```html
{% block admn_content %}  <!-- Typo! -->
```

**Symptom:** Content doesn't appear (empty block with typo is created)

---

## Block Reference by Template

### base.html (root)

```html
<!DOCTYPE html>
<html>
<head>
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% block content %}{% endblock %}

    <!-- Scripts -->
    {% block chart_js %}
    <script src="chart.js"></script>
    {% endblock %}
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### admin/base.html

```html
{% extends "base.html" %}

{% block content %}
<div class="admin-layout">
    <nav class="sidebar"><!-- sidebar --></nav>
    <main>
        <h1>{% block page_title %}{% endblock %}</h1>
        <div>{% block page_actions %}{% endblock %}</div>
        {% block breadcrumb %}{% endblock %}
        {% block admin_content %}{% endblock %}
    </main>
</div>
{% endblock %}
```

---

## Validation Script

Save as `scripts/validate_templates.py`:

```python
"""
Template Block Validator

Checks that templates use correct block names for their parent.
"""

import re
from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent.parent / "app" / "templates"

# Expected blocks by template type
ADMIN_BLOCKS = {"admin_content", "page_title", "page_actions", "breadcrumb", "extra_js", "extra_css"}
PUBLIC_BLOCKS = {"content", "extra_js", "extra_css"}

# Blocks that should NOT appear in admin templates
WRONG_ADMIN_BLOCKS = {"content", "scripts"}

def validate_templates():
    issues = []

    for template in TEMPLATES_DIR.rglob("*.html"):
        content = template.read_text(encoding="utf-8")
        rel_path = template.relative_to(TEMPLATES_DIR)

        # Find all block definitions
        blocks = re.findall(r'{%\s*block\s+(\w+)', content)

        # Check admin templates
        if str(rel_path).startswith("admin") and "base.html" not in str(rel_path):
            for block in blocks:
                if block in WRONG_ADMIN_BLOCKS:
                    issues.append(f"{rel_path}: Uses '{block}' instead of admin block")

    return issues

if __name__ == "__main__":
    issues = validate_templates()
    if issues:
        print("TEMPLATE ISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("All templates valid!")
```

---

## Debugging Template Issues

### Check which template is rendering

Add to route temporarily:
```python
print(f"Rendering: admin/reports/requests.html")
return templates.TemplateResponse("admin/reports/requests.html", context)
```

### Check block inheritance chain

Add to template temporarily:
```html
<!-- DEBUG: This is admin/reports/requests.html -->
{% block admin_content %}
<!-- DEBUG: admin_content block start -->
...
<!-- DEBUG: admin_content block end -->
{% endblock %}
```

### Verify template extends correct parent

```bash
# Find extends statements
grep -rn "{% extends" app/templates/admin/reports/ --include="*.html"

# Should show: {% extends "admin/base.html" %}
```

---

*End of Template Checks Reference*
