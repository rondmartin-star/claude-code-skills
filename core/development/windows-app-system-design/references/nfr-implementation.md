# Non-Functional Requirements Implementation

## Authentication Types

### Local Admin Authentication

```python
# app/auth.py - SACRED FILE
def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    hash_obj = hashlib.sha256((salt + password).encode())
    return f"{salt}:{hash_obj.hexdigest()}"

def verify_password(password: str, stored_hash: str) -> bool:
    if ":" not in stored_hash:
        return False
    salt, hash_value = stored_hash.split(":", 1)
    check_hash = hashlib.sha256((salt + password).encode()).hexdigest()
    return secrets.compare_digest(check_hash, hash_value)
```

### Google OAuth

```python
# Settings
GOOGLE_CLIENT_ID: Optional[str] = None
GOOGLE_CLIENT_SECRET: Optional[str] = None
GOOGLE_REDIRECT_URI: str = "http://localhost:8004/auth/google/callback"
ALLOWED_EMAIL_DOMAINS: str = ""  # Comma-separated

# Requires: authlib package
```

## Backup/Restore

### Backup Strategy

```batch
REM scripts/backup.bat
@echo off
setlocal EnableDelayedExpansion
title %APP_NAME% Backup

set "BACKUP_DIR=%APP_DIR%\backups"
set "TIMESTAMP=%date:~-4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%"
set "BACKUP_FILE=%BACKUP_DIR%\%APP_NAME%_%TIMESTAMP%.zip"

REM Create backup directory
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

REM Backup database and config
powershell -Command "Compress-Archive -Path '%APP_DIR%\instance\*.db','%APP_DIR%\.env' -DestinationPath '%BACKUP_FILE%'"

echo Backup created: %BACKUP_FILE%
```

### Restore Points
- Before every update
- On scheduled basis
- On user request

## Business Continuity

### Health Check Endpoint

```python
@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )
```

### Auto-Start Service

```batch
REM scripts/auto-start.bat
REM Add to Windows Task Scheduler for startup
```

## Cybersecurity

### Required Security Measures

| Measure | Implementation |
|---------|----------------|
| Password hashing | SHA-256 with salt (auth.py) |
| Session cookies | httponly=True, samesite="lax" |
| HTTPS in production | Reverse proxy (nginx) |
| Input validation | Pydantic models |
| SQL injection | SQLAlchemy ORM |
| XSS prevention | Jinja2 auto-escaping |
| CSRF protection | SessionMiddleware |

### Encryption at Rest

```python
# scripts/config_crypto.py
# Encrypts sensitive .env values for silent install
```

## Data Import/Export

### Export Patterns

```python
@router.get("/api/export/{entity}")
async def export_data(entity: str, format: str = "csv"):
    # Generate CSV/JSON export
    pass

@router.get("/api/backup/download")
async def download_backup():
    # Download full database backup
    pass
```

### Import Patterns

```python
@router.post("/api/import/{entity}")
async def import_data(entity: str, file: UploadFile):
    # Parse and validate uploaded file
    # Insert records with conflict handling
    pass
```

## API Endpoint Design

### Standard CRUD Pattern

| Method | Path | Purpose | Auth |
|--------|------|---------|------|
| GET | /items | List all | User |
| GET | /items/{id} | Get one | User |
| POST | /items | Create | User |
| PUT | /items/{id} | Update | Owner |
| DELETE | /items/{id} | Delete | Owner |

### Response Shapes

```python
# List with pagination
{
    "items": [...],
    "total": 100,
    "page": 1,
    "per_page": 20,
    "pages": 5
}

# Single item
{
    "id": 1,
    "name": "Example",
    ...
}

# Error
{
    "detail": "Error message",
    "errors": {"field": ["message"]}  # Validation
}
```

### Configuration API (No Hardcoding)

```python
# GET /api/config/{key}
{"key": "statuses", "values": ["Draft", "Active", "Archived"]}

# POST /api/config/{key}
{"values": ["Draft", "Active", "Archived", "Deleted"]}
```

## Theme System

### Three Modes Required
1. Light - Traditional light background
2. Dark - High-contrast dark background
3. System - Follows OS preference

### Implementation

```html
<html data-bs-theme="dark">
<script>
(function() {
    const theme = localStorage.getItem('app-theme') || 'system';
    const effective = theme === 'system'
        ? (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
        : theme;
    document.documentElement.setAttribute('data-bs-theme', effective);
})();
</script>
```

## Application Ontology

### Single Source of Names

```python
# app/ontology.py
"""Define ALL names here. Reference from code. NEVER invent names elsewhere."""

@dataclass(frozen=True)
class UserModel:
    TABLE: str = "users"
    FIELDS: Dict[str, str] = field(default_factory=lambda: {
        "id": "id",
        "email": "email",
        "name": "name",  # NOT "username" or "display_name"
    })

@dataclass(frozen=True)
class Routes:
    Auth: AuthRoutes = field(default_factory=AuthRoutes)
    Users: UserRoutes = field(default_factory=UserRoutes)
```

**Why:** Prevents model-route-template name mismatches.

## Multi-Tenant Design

**Ask early:** "Will there ever be multiple venues/locations/organizations?"

If yes:
- Add venue_id FK to all relevant tables
- Filter all queries by venue_id
- Accept venue_id in API endpoints
- Design UI with entity selector

**For detailed patterns and code examples:**
```
/mnt/skills/user/windows-app-system-design/references/patterns.md
```

## Integration Services

When integrating with external hardware/services:

1. Create dedicated service classes (VMixService, QSysService)
2. Return ConnectionStatus enum and CommandResult dataclass
3. Use factory functions for dependency injection
4. Accept venue_id for multi-venue testing

**For detailed implementation templates:**
```
/mnt/skills/user/windows-app-system-design/references/patterns.md
```
