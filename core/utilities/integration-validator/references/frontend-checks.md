# Frontend Dependency Validation Reference

Detailed procedures for validating JavaScript library dependencies.

---

## CDN Inventory

Track all CDN libraries used in the application:

### UCC-PMS CDN Libraries

| Library | Version | CDN URL | Used In |
|---------|---------|---------|---------|
| Bootstrap CSS | 5.3.2 | cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css | base.html |
| Bootstrap JS | 5.3.2 | cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js | base.html |
| Bootstrap Icons | 1.11.1 | cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css | base.html |
| Chart.js | 4.4.0 | cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js | base.html (chart_js block) |

### Adding New Libraries

When adding a new library:

1. Add CDN to appropriate template (usually base.html)
2. Document in this inventory
3. Document in project CLAUDE.md
4. Add dependency check to validation

---

## Dependency Validation Commands

### Find library usage in JavaScript

```bash
# Chart.js
grep -rn "new Chart" app/static/js/ --include="*.js"
grep -rn "Chart\." app/static/js/ --include="*.js"

# Moment.js
grep -rn "moment(" app/static/js/ --include="*.js"

# jQuery (if used)
grep -rn "\$(" app/static/js/ --include="*.js"
grep -rn "jQuery" app/static/js/ --include="*.js"

# Flatpickr
grep -rn "flatpickr" app/static/js/ --include="*.js"

# SortableJS
grep -rn "Sortable\." app/static/js/ --include="*.js"
grep -rn "new Sortable" app/static/js/ --include="*.js"
```

### Verify library is loaded

```bash
# Check base template for CDN includes
grep -n "chart.js" app/templates/base.html
grep -n "moment" app/templates/base.html
grep -n "flatpickr" app/templates/base.html

# Check all templates for script includes
grep -rn "<script src=" app/templates/ --include="*.html"
```

---

## Common Issues

### Issue 1: Library used but not loaded

**Symptom:** Console error: `Chart is not defined` or `ReferenceError`

**Detection:**
```bash
# Find Chart.js usage
grep -rn "new Chart" app/static/js/

# Verify Chart.js loaded
grep -rn "chart.js" app/templates/
```

**Fix:** Add CDN to base.html or appropriate template

### Issue 2: Library loaded too late

**Symptom:** Script runs before library loads

**Detection:** Check script order in rendered HTML

**Fix:** Ensure library CDN appears BEFORE custom scripts

### Issue 3: Version mismatch

**Symptom:** Deprecated API warnings, unexpected behavior

**Detection:** Check CDN URL version vs documentation

**Fix:** Update CDN URL to compatible version

### Issue 4: Duplicate library loads

**Symptom:** Conflicts, doubled event handlers

**Detection:**
```bash
grep -c "chart.js" app/templates/*.html
# Should be 1 (in base.html only)
```

**Fix:** Load library only once in base template

---

## Library Load Order

Correct order in templates:

```html
<!-- 1. CSS first -->
<link href="bootstrap.css" rel="stylesheet">
<link href="custom.css" rel="stylesheet">

<!-- 2. Content -->
<body>...</body>

<!-- 3. Core libraries -->
<script src="bootstrap.bundle.min.js"></script>

<!-- 4. Additional libraries -->
<script src="chart.js"></script>
<script src="moment.js"></script>

<!-- 5. Application scripts -->
<script src="app.js"></script>

<!-- 6. Page-specific scripts (in extra_js block) -->
{% block extra_js %}{% endblock %}
```

---

## Browser Console Debugging

### Check if library is loaded

```javascript
// In browser console
typeof Chart !== 'undefined'  // Should be true
typeof moment !== 'undefined' // Should be true
typeof $ !== 'undefined'      // jQuery check
```

### Find load errors

1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for red error messages
4. Go to Network tab
5. Look for failed (red) script loads

### Common console errors

| Error | Meaning | Fix |
|-------|---------|-----|
| `X is not defined` | Library not loaded | Add CDN |
| `X is not a function` | Wrong version or not loaded | Check version |
| `Failed to load resource` | CDN URL wrong or blocked | Fix URL or use local copy |
| `SyntaxError` | Malformed JavaScript | Check script file |

---

## Validation Script

Save as `scripts/validate_frontend.py`:

```python
"""
Frontend Dependency Validator

Checks that JavaScript libraries used in code are loaded in templates.
"""

import re
from pathlib import Path

APP_DIR = Path(__file__).parent.parent / "app"

# Library patterns and their expected CDN markers
LIBRARIES = {
    "Chart.js": {
        "usage_pattern": r"new Chart\(|Chart\.",
        "cdn_marker": "chart.js",
        "search_path": APP_DIR / "static" / "js"
    },
    "Moment.js": {
        "usage_pattern": r"moment\(|moment\.",
        "cdn_marker": "moment",
        "search_path": APP_DIR / "static" / "js"
    },
    "Flatpickr": {
        "usage_pattern": r"flatpickr\(|flatpickr\.",
        "cdn_marker": "flatpickr",
        "search_path": APP_DIR / "static" / "js"
    }
}

def check_library(name, config):
    issues = []
    usage_found = False
    cdn_found = False

    # Check for usage in JS files
    for js_file in config["search_path"].rglob("*.js"):
        content = js_file.read_text(encoding="utf-8", errors="ignore")
        if re.search(config["usage_pattern"], content):
            usage_found = True
            break

    # Check for CDN in templates
    templates_dir = APP_DIR / "templates"
    for template in templates_dir.rglob("*.html"):
        content = template.read_text(encoding="utf-8", errors="ignore")
        if config["cdn_marker"] in content.lower():
            cdn_found = True
            break

    if usage_found and not cdn_found:
        issues.append(f"{name}: Used in JS but CDN not found in templates")

    return issues

def validate():
    all_issues = []
    for name, config in LIBRARIES.items():
        issues = check_library(name, config)
        all_issues.extend(issues)

    if all_issues:
        print("FRONTEND DEPENDENCY ISSUES:")
        for issue in all_issues:
            print(f"  - {issue}")
        return False
    else:
        print("All frontend dependencies valid!")
        return True

if __name__ == "__main__":
    validate()
```

---

## Adding New Library Checklist

When adding a new JavaScript library:

- [ ] Add CDN to base.html or appropriate template
- [ ] Use specific version (not "latest")
- [ ] Add to CDN Inventory table above
- [ ] Document in CLAUDE.md
- [ ] Add usage pattern to validation script
- [ ] Test in browser DevTools
- [ ] Verify no duplicate loads

---

*End of Frontend Checks Reference*
