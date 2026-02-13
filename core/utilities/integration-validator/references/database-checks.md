# Database Schema Validation Reference

Detailed procedures for validating database schema matches model definitions.

---

## Full Schema Validation Script

Save as `scripts/validate_schema.py`:

```python
"""
Database Schema Validator

Compares SQLAlchemy model definitions to actual database schema.
Run after any model changes to detect drift.

Usage:
    python scripts/validate_schema.py
"""

import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import inspect, text
from app.database import engine
from app.models import (
    User, Request, Asset, AssetMaintenance, Venue, Booking,
    Vendor, VendorContact, HelpContent, AuditLog,
    RequestAsset, RequestVenue, ProposalAttachment,
    AssetAttributeDefinition, AssetAttributeValue
)

def get_model_columns(model):
    """Extract column names and types from model."""
    return {
        col.name: {
            'type': str(col.type),
            'nullable': col.nullable,
            'primary_key': col.primary_key,
            'foreign_key': bool(col.foreign_keys)
        }
        for col in model.__table__.columns
    }

def get_db_columns(inspector, table_name):
    """Extract column info from database."""
    try:
        columns = inspector.get_columns(table_name)
        return {
            col['name']: {
                'type': str(col['type']),
                'nullable': col.get('nullable', True),
                'primary_key': col.get('primary_key', False)
            }
            for col in columns
        }
    except Exception:
        return None

def validate_schema():
    """Compare all models to database."""
    inspector = inspect(engine)

    models = [
        User, Request, Asset, AssetMaintenance, Venue, Booking,
        Vendor, VendorContact, HelpContent, AuditLog,
        RequestAsset, RequestVenue, ProposalAttachment,
        AssetAttributeDefinition, AssetAttributeValue
    ]

    issues = []

    print("=" * 60)
    print("DATABASE SCHEMA VALIDATION")
    print("=" * 60)

    for model in models:
        table = model.__tablename__
        model_cols = get_model_columns(model)
        db_cols = get_db_columns(inspector, table)

        if db_cols is None:
            print(f"\n[MISSING TABLE] {table}")
            issues.append(f"Table {table} does not exist")
            continue

        model_names = set(model_cols.keys())
        db_names = set(db_cols.keys())

        missing_in_db = model_names - db_names
        extra_in_db = db_names - model_names

        if missing_in_db or extra_in_db:
            print(f"\n[MISMATCH] {table}")
            if missing_in_db:
                print(f"  Missing in DB: {missing_in_db}")
                for col in missing_in_db:
                    col_info = model_cols[col]
                    issues.append(f"ALTER TABLE {table} ADD COLUMN {col} {col_info['type']};")
            if extra_in_db:
                print(f"  Extra in DB: {extra_in_db}")
        else:
            print(f"[OK] {table}")

    print("\n" + "=" * 60)
    if issues:
        print(f"FOUND {len(issues)} ISSUE(S)")
        print("\nSuggested migrations:")
        for issue in issues:
            if issue.startswith("ALTER"):
                print(f"  {issue}")
    else:
        print("ALL MODELS MATCH DATABASE")
    print("=" * 60)

    return len(issues) == 0

if __name__ == "__main__":
    success = validate_schema()
    sys.exit(0 if success else 1)
```

---

## Migration Script Template

When validation fails, use this template:

```python
"""
Migration: Add missing columns to {table}
Date: YYYY-MM-DD
Issue: Schema drift detected by validation

Run with: python scripts/migrate_{table}.py
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "instance" / "ucc_pms.db"

MIGRATIONS = [
    # Format: (column_name, sql_type, default_value_or_None)
    ("new_column", "VARCHAR(100)", None),
    ("another_column", "INTEGER", "0"),
]

def run_migration():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for col_name, col_type, default in MIGRATIONS:
        try:
            if default is not None:
                sql = f"ALTER TABLE {table} ADD COLUMN {col_name} {col_type} DEFAULT {default}"
            else:
                sql = f"ALTER TABLE {table} ADD COLUMN {col_name} {col_type}"

            cursor.execute(sql)
            print(f"[OK] Added column: {col_name}")
        except sqlite3.OperationalError as e:
            if "duplicate column" in str(e).lower():
                print(f"[SKIP] Column exists: {col_name}")
            else:
                print(f"[ERROR] {col_name}: {e}")

    conn.commit()
    conn.close()
    print("\nMigration complete!")

if __name__ == "__main__":
    run_migration()
```

---

## SQLite Limitations

SQLite has limited ALTER TABLE support:

| Operation | Supported | Workaround |
|-----------|-----------|------------|
| ADD COLUMN | Yes | Direct ALTER |
| DROP COLUMN | SQLite 3.35+ | Recreate table |
| RENAME COLUMN | SQLite 3.25+ | Recreate table |
| Change type | No | Recreate table |
| Add constraint | No | Recreate table |

### Table Recreation Pattern

When ALTER TABLE isn't sufficient:

```sql
-- 1. Create new table with correct schema
CREATE TABLE new_table (
    id INTEGER PRIMARY KEY,
    column1 TEXT,
    column2 INTEGER,
    -- new/modified columns
);

-- 2. Copy data
INSERT INTO new_table (id, column1, column2)
SELECT id, column1, column2 FROM old_table;

-- 3. Drop old table
DROP TABLE old_table;

-- 4. Rename new table
ALTER TABLE new_table RENAME TO old_table;

-- 5. Recreate indexes
CREATE INDEX idx_name ON old_table(column1);
```

---

## Common Schema Issues

### Issue: Column exists in model but not in DB

**Symptom:** `sqlite3.OperationalError: no such column: table.column`

**Detection:**
```python
model_cols - db_cols  # Returns missing columns
```

**Fix:**
```sql
ALTER TABLE table_name ADD COLUMN column_name TYPE;
```

### Issue: Column type mismatch

**Symptom:** Data truncation, unexpected NULL values

**Detection:**
Compare `model_cols[name]['type']` vs `db_cols[name]['type']`

**Fix:** Recreate table (SQLite limitation)

### Issue: Missing foreign key

**Symptom:** Orphaned records, constraint violations

**Detection:**
```python
for col in model.__table__.columns:
    if col.foreign_keys:
        print(f"{col.name} -> {col.foreign_keys}")
```

**Fix:** Add column with REFERENCES clause

---

## Automated Validation

Add to CI/CD pipeline:

```yaml
# .github/workflows/validate.yml
- name: Validate Schema
  run: |
    python scripts/validate_schema.py
    if [ $? -ne 0 ]; then
      echo "Schema drift detected!"
      exit 1
    fi
```

---

*End of Database Checks Reference*
