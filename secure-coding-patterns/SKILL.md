---
name: secure-coding-patterns
description: >
  Proactive security guidance during implementation. Covers authentication,
  template security, form patterns, database queries, file handling, and
  configuration. Load alongside windows-app-build for secure development.
---

# Secure Coding Patterns

**Purpose:** Prevent security issues during implementation (not just detect after)
**Size:** ~8 KB
**Philosophy:** Security by design, not security by audit

---

## LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "add authentication"
- "create a form"
- "file upload"
- "user input"
- "database query"
- "add a route"
- "handle user data"

**Context Indicators:**
- Implementing features that handle user input
- Creating forms or API endpoints
- Working with file uploads
- Adding authentication/authorization
- Writing database queries

## DO NOT LOAD WHEN

- Pure UI/styling work
- Documentation only
- Configuration without secrets
- Read-only operations on static data

---

## Security-First Mindset

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   EVERY USER INPUT IS POTENTIALLY MALICIOUS                 │
│   EVERY ROUTE NEEDS EXPLICIT AUTH CONSIDERATION             │
│   EVERY TEMPLATE VARIABLE NEEDS ESCAPING REVIEW             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Reference: Before You Write...

### Before Writing ANY Route

```
[ ] Does it need authentication?
    → Add auth check as FIRST line
[ ] Does it accept user input?
    → Plan validation before processing
[ ] Does it render user content?
    → NEVER use |safe on user data
[ ] Does it modify data?
    → Require CSRF token
```

### Before Writing ANY Form

```
[ ] Add CSRF token input IMMEDIATELY
    <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
[ ] If file upload: add enctype AND accept
    enctype="multipart/form-data"
    accept=".jpg,.png,.pdf"
[ ] Plan server-side validation
    → Client validation is UX, not security
[ ] NEVER nest forms
    → Use JavaScript fetch() for sub-operations
```

### Before Writing ANY Query

```
[ ] Use ORM methods ONLY
    db.query(User).filter(User.id == user_id)  ✓
    db.execute(f"SELECT * WHERE id = {user_id}")  ✗
[ ] If dynamic columns needed: whitelist them
    allowed = {"name", "email", "created_at"}
    if sort_by not in allowed: raise ValueError
```

### Before Adding ANY Configuration

```
[ ] Add to config.py with Pydantic validation
[ ] Add to .env.example with placeholder
[ ] Import from config module, never os.environ
[ ] If sensitive: add to SENSITIVE_SETTINGS list
```

---

## Authentication Patterns

### Route Protection (FastAPI)

```python
# CORRECT - Auth check first
@router.post("/admin/settings")
async def update_settings(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user(request, db)
    if not current_user:
        return RedirectResponse("/login", status_code=303)
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(403, "Admin required")

    # Now safe to proceed...
```

### Role Hierarchy

```python
# Define clear hierarchy
ROLE_LEVELS = {
    UserRole.VIEWER: 1,
    UserRole.USER: 2,
    UserRole.MANAGER: 3,
    UserRole.ADMIN: 4,
}

def require_role(user, minimum_role):
    if ROLE_LEVELS.get(user.role, 0) < ROLE_LEVELS[minimum_role]:
        raise HTTPException(403, f"Requires {minimum_role.value} role")
```

---

## Template Security

### The |safe Filter Rule

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   NEVER use |safe on user-generated content                 │
│                                                             │
│   User content includes:                                    │
│   - Form submissions                                        │
│   - Comments, reviews, descriptions                         │
│   - Profile fields (bio, about)                             │
│   - Any field users can edit                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**When |safe IS acceptable:**
- Server-generated HTML (icons, formatted dates)
- Admin-only content that only admins can edit
- Static configuration values
- Sanitized HTML (after bleach.clean())

```html
<!-- DANGEROUS - User can inject scripts -->
{{ user.bio|safe }}
{{ comment.content|safe }}

<!-- SAFE - Server-generated -->
{{ pagination_html|safe }}
{{ icon_svg|safe }}

<!-- SAFE - Sanitized first -->
{{ article.content|sanitize_html|safe }}
```

### Input Display

```html
<!-- Auto-escaped (default, safe) -->
{{ user.name }}
{{ request.description }}

<!-- If you MUST allow some HTML, sanitize first -->
{% set clean_content = content|sanitize_html %}
{{ clean_content|safe }}
```

---

## Form Security

### Complete Secure Form Pattern

```html
<form method="post"
      action="{{ url_for('module.action') }}"
      {% if has_file_input %}enctype="multipart/form-data"{% endif %}>

    <!-- CSRF token - ALWAYS FIRST -->
    <input type="hidden" name="csrf_token" value="{{ csrf_token }}">

    <!-- Form fields with validation attributes -->
    <input type="email"
           name="email"
           required
           pattern="[^@]+@[^@]+\.[^@]+"
           maxlength="255">

    <!-- File input with restrictions -->
    <input type="file"
           name="document"
           accept=".pdf,.doc,.docx,.jpg,.png"
           {% if required %}required{% endif %}>

    <button type="submit">Submit</button>
</form>
```

### Multi-Operation Pages (No Nested Forms)

```html
<!-- Main form for primary data -->
<form id="main-form" method="post">
    <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
    <!-- Primary fields -->
    <button type="submit">Save Changes</button>
</form>

<!-- Secondary operations use JavaScript, NOT nested forms -->
<div class="upload-section">
    <input type="file" id="attachment">
    <button type="button" id="upload-btn">Upload</button>
</div>

<script>
document.getElementById('upload-btn').addEventListener('click', async () => {
    const formData = new FormData();
    formData.append('file', document.getElementById('attachment').files[0]);
    formData.append('csrf_token', '{{ csrf_token }}');

    await fetch('{{ url_for("module.upload") }}', {
        method: 'POST',
        body: formData
    });
});
</script>
```

---

## Database Security

### Query Patterns

```python
# CORRECT - ORM with parameterization
user = db.query(User).filter(User.email == email).first()
requests = db.query(Request).filter(
    Request.status.in_([Status.NEW, Status.IN_PROGRESS])
).all()

# CORRECT - Text with parameters
result = db.execute(
    text("SELECT * FROM users WHERE email = :email"),
    {"email": email}
)

# WRONG - String interpolation
db.execute(f"SELECT * FROM users WHERE email = '{email}'")  # SQL INJECTION!
db.execute("SELECT * FROM users WHERE email = '%s'" % email)  # SQL INJECTION!
```

### Dynamic Queries (Whitelist Approach)

```python
# When user controls sort/filter columns
ALLOWED_SORT_COLUMNS = {"name", "created_at", "status", "priority"}
ALLOWED_FILTER_COLUMNS = {"status", "category", "assigned_to"}

def get_filtered_results(db, filters: dict, sort_by: str):
    query = db.query(Request)

    for key, value in filters.items():
        if key not in ALLOWED_FILTER_COLUMNS:
            continue  # Silently ignore invalid filters
        column = getattr(Request, key, None)
        if column:
            query = query.filter(column == value)

    if sort_by in ALLOWED_SORT_COLUMNS:
        query = query.order_by(getattr(Request, sort_by))

    return query.all()
```

---

## File Upload Security

### Complete Validation Chain

```python
from pathlib import Path
import uuid
import magic  # python-magic for MIME detection

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx'}
ALLOWED_MIME_TYPES = {
    'image/jpeg', 'image/png', 'image/gif',
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

async def save_upload(file: UploadFile, entity_type: str, entity_id: int) -> str:
    # 1. Check extension
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"File type {ext} not allowed")

    # 2. Check file size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise ValueError("File too large")

    # 3. Check MIME type (don't trust Content-Type header)
    mime_type = magic.from_buffer(content, mime=True)
    if mime_type not in ALLOWED_MIME_TYPES:
        raise ValueError(f"File type {mime_type} not allowed")

    # 4. Generate safe filename (NEVER use user filename)
    safe_name = f"{uuid.uuid4().hex}{ext}"

    # 5. Store in isolated directory
    upload_dir = Path("instance/uploads") / entity_type / str(entity_id)
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / safe_name
    file_path.write_bytes(content)

    return safe_name
```

---

## Configuration Security

### Settings Pattern

```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Required - no default
    SECRET_KEY: str

    # With validation
    PORT: int = 8008

    # Sensitive - will be encrypted if stored in DB
    SMTP_PASSWORD: str = ""
    GOOGLE_CLIENT_SECRET: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

# Define which settings are sensitive
SENSITIVE_SETTINGS = [
    "smtp.password",
    "google.client_secret",
    "api_keys.*"  # Pattern matching
]
```

### Never Do This

```python
# WRONG - Hardcoded secrets
API_KEY = "sk-abc123..."
PASSWORD = "admin123"

# WRONG - Direct environ access in routes
import os
key = os.environ.get("API_KEY")

# CORRECT - Via config module
from app.config import settings
key = settings.API_KEY
```

---

## Checklist for New Features

```
Authentication & Authorization
[ ] Route has auth check (if needed)
[ ] Role requirements enforced
[ ] User can only access their own data

Input Handling
[ ] All inputs validated server-side
[ ] Appropriate type coercion
[ ] Length limits enforced

Output Rendering
[ ] No |safe on user content
[ ] Proper encoding for context (HTML, JS, URL)

Forms
[ ] CSRF token present
[ ] enctype for file uploads
[ ] No nested forms

Database
[ ] ORM or parameterized queries only
[ ] No string interpolation in SQL

File Uploads
[ ] Extension whitelist
[ ] MIME type validation
[ ] Size limits
[ ] Safe filename generation

Configuration
[ ] Secrets in .env, not code
[ ] Documented in .env.example
[ ] Imported from config module
```

---

## Common Vulnerabilities Quick Reference

| Vulnerability | Prevention |
|--------------|------------|
| XSS | Never `\|safe` on user content |
| SQL Injection | ORM only, parameterized queries |
| CSRF | Token in all POST forms |
| Path Traversal | UUID filenames, no user paths |
| Auth Bypass | Check auth first in every route |
| Secrets Leak | .env not in repo, config module |
| Nested Forms | JavaScript for sub-operations |
