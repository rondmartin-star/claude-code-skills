---
name: integration-validator
description: >
  Validate integration points between components: database schema vs models,
  template inheritance, frontend dependencies. Use when: pre-deployment,
  after schema changes, debugging 500 errors, or before packaging.
---

# Integration Validator

**Purpose:** Detect integration errors that static analysis misses
**Size:** ~8.5 KB (references: ~33 KB)
**Philosophy:** Catch runtime-only errors before deployment

---

## LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Validate schema matches models"
- "Check template inheritance"
- "Debug 500 error"
- "Pre-deployment validation"
- "Integration check"
- "Why is sidebar missing"
- "Charts not rendering"
- "no such column error"

**Context Indicators:**
- After model changes (new columns, relationships)
- After template changes (new pages, extending base)
- Before packaging/deployment
- 500 errors on pages that should work
- UI elements missing unexpectedly

## DO NOT LOAD WHEN

- Writing new code (use windows-app-build)
- Running unit tests (use test framework)
- General development without integration issues

---

## Parallel Execution (v4.1)

**NEW:** Run all 4 checks concurrently for 4x speedup.

**Performance:**
- Sequential: 12m 10s (run checks one by one)
- Parallel: 3m 20s (run all 4 simultaneously)
- Speedup: 3.65x faster

**How to Use:**
In a single message, ask to "run all integration checks in parallel" or "validate integration points concurrently". This launches 4 independent Tasks that execute simultaneously:

1. Database schema check (Task 1)
2. Model attribute check (Task 2)
3. Template block check (Task 3)
4. Frontend dependency check (Task 4)

Results aggregate automatically when all complete.

**When to Use:**
- ✅ Pre-deployment validation (need all results fast)
- ✅ CI/CD pipelines (optimize build time)
- ✅ Weekly full audits
- ⚠️ Debugging specific issue (use sequential, single check)

**Details:** See `references/parallel-validation.md` for complete pattern, examples, and configuration.

---

## Quick Validation Commands

Run these checks to detect integration issues:

### 1. Database Schema Validation

Compare model definitions to actual database columns:

```bash
# Python script - run from app directory
python -c "
from app.models import *
from app.database import engine
from sqlalchemy import inspect

inspector = inspect(engine)
models = [Asset, AssetMaintenance, Request, Venue, Booking, User, Vendor]

print('=== DATABASE SCHEMA CHECK ===')
issues = []
for model in models:
    try:
        table = model.__tablename__
        db_cols = {c['name'] for c in inspector.get_columns(table)}
        model_cols = {c.name for c in model.__table__.columns}
        missing_in_db = model_cols - db_cols
        extra_in_db = db_cols - model_cols
        if missing_in_db:
            issues.append(f'MISSING in {table}: {missing_in_db}')
            print(f'[X] {table}: MISSING columns {missing_in_db}')
        elif extra_in_db:
            print(f'[~] {table}: Extra DB columns {extra_in_db}')
        else:
            print(f'[OK] {table}')
    except Exception as e:
        print(f'[?] {model.__name__}: {e}')

if issues:
    print(f'\n{len(issues)} issue(s) found - run migrations')
else:
    print('\nAll models match database schema')
"
```

### 2. Model Attribute Validation

Find code accessing model fields and verify names:

```bash
# Common problematic field patterns
grep -rn "\.next_maintenance_date" app/ --include="*.py"   # Wrong: should be next_maintenance
grep -rn "\.warranty_expiration" app/ --include="*.py"      # Wrong: should be warranty_expiry
grep -rn "\.model_number" app/ --include="*.py"             # Wrong: should be model
grep -rn "\.assigned_to_id" app/ --include="*.py"           # Wrong: should be assigned_to
grep -rn "\.actual_cost" app/ --include="*.py"              # Wrong: field may not exist

# Correct field patterns (should find matches)
grep -rn "\.next_maintenance[^_]" app/ --include="*.py"
grep -rn "\.warranty_expiry" app/ --include="*.py"
```

### 3. Template Block Validation

Check child templates use correct block names:

```bash
# Find all block definitions in child templates
grep -rn "{% block" app/templates/admin/ --include="*.html" | grep -v endblock

# Expected blocks for admin templates (from admin/base.html):
# - admin_content (NOT content)
# - page_title
# - page_actions
# - breadcrumb
# - extra_js (NOT scripts)
# - extra_css

# Find wrong block usage
grep -rn "{% block content %}" app/templates/admin/ --include="*.html"
grep -rn "{% block scripts %}" app/templates/admin/ --include="*.html"
# These should return ZERO results for admin templates
```

### 4. Frontend Dependency Check

Verify JavaScript libraries are loaded:

```bash
# Find Chart.js usage
grep -rn "new Chart" app/static/js/ --include="*.js"
grep -rn "Chart\." app/static/js/ --include="*.js"

# Verify Chart.js is loaded in base template
grep -n "chart.js" app/templates/base.html

# Find other common library usages
grep -rn "moment(" app/static/js/ --include="*.js"      # Requires moment.js
grep -rn "flatpickr" app/static/js/ --include="*.js"    # Requires flatpickr
grep -rn "Sortable" app/static/js/ --include="*.js"     # Requires SortableJS
```

---

## Error Detection Table

| Symptom | Quick Check | Root Cause | Fix |
|---------|-------------|------------|-----|
| `no such column: X` | Schema validation script | Model has column, DB doesn't | `ALTER TABLE ADD COLUMN X` |
| `has no attribute 'X'` | Grep for `.X` in code | Code uses wrong field name | Fix field name to match model |
| Missing sidebar | Grep for `{% block content %}` | Wrong block name | Change to `{% block admin_content %}` |
| Charts don't render | Check for Chart.js CDN | Library not loaded | Add `<script src="chart.js">` to base |
| `'None' has no attribute` | Check template guards | Null value accessed | Add `{% if x %}` guards |
| 500 on page load | Check server logs | Usually attribute/column error | Follow error message |
| JavaScript errors | Browser console | Missing dependency | Add CDN or local script |
| Form not submitting | Check block names | Wrong block prevents CSRF | Fix template inheritance |

---

## Prevention Patterns

| Pattern | Prevents | When to Apply |
|---------|----------|---------------|
| Run schema validation after model changes | Column mismatch | After editing models.py |
| Grep for field names before using | Typos in field access | When writing queries |
| Document parent template blocks | Block name errors | In CLAUDE.md |
| CDN inventory in project docs | Missing libraries | When adding JS features |
| Integration tests with real DB | Runtime-only errors | CI/CD pipeline |
| Template rendering tests | Block inheritance issues | Test suite |

---

## Common Field Name Gotchas

| Wrong | Correct | Model |
|-------|---------|-------|
| `next_maintenance_date` | `next_maintenance` | Asset |
| `warranty_expiration` | `warranty_expiry` | Asset |
| `model_number` | `model` | Asset |
| `assigned_to_id` | `assigned_to` | Request |
| `actual_cost` | `estimated_cost` | Request |
| `maintenance_type_enum` | `maintenance_type` | AssetMaintenance |

---

## Template Block Reference

### admin/base.html blocks:
| Block Name | Purpose | Content Type |
|------------|---------|--------------|
| `admin_content` | Main page content | HTML |
| `page_title` | H1 title text | Text only |
| `page_actions` | Header buttons | Buttons/links |
| `breadcrumb` | Breadcrumb nav | nav element |
| `extra_js` | Page-specific JS | script tags |
| `extra_css` | Page-specific CSS | style/link tags |

### base.html blocks:
| Block Name | Purpose |
|------------|---------|
| `content` | Full page content (public pages) |
| `extra_js` | Additional JavaScript |
| `extra_css` | Additional CSS |
| `chart_js` | Chart.js include |

---

## SQLite Migration Patterns

When schema validation finds missing columns:

```sql
-- Add missing column
ALTER TABLE table_name ADD COLUMN column_name TYPE DEFAULT value;

-- Examples:
ALTER TABLE asset_maintenance ADD COLUMN maintenance_type_enum VARCHAR(50);
ALTER TABLE asset_maintenance ADD COLUMN duration_hours FLOAT;
ALTER TABLE asset_maintenance ADD COLUMN request_id INTEGER REFERENCES requests(id);

-- Note: SQLite doesn't support DROP COLUMN or column type changes
-- For those, must recreate table
```

---

## References

For detailed procedures:

- Database schema validation: `references/database-checks.md`
- Template inheritance patterns: `references/template-checks.md`
- Frontend dependency tracking: `references/frontend-checks.md`
- **Parallel execution (NEW):** `references/parallel-validation.md` - 4x faster validation

---

*End of Integration Validator*
