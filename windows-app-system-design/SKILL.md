---
name: windows-app-system-design
description: >
  Design system architecture with MVC separation, data models, and non-functional
  requirements. Covers authentication strategies, backup/restore, cybersecurity,
  data import/export, and technology selection. Use when: "design the data model",
  "plan the architecture", "choose technologies", "define the database schema".
---

# Windows Application System Design Skill

**Purpose:** Design data structures, architecture, and infrastructure patterns  
**Output:** Data models, API specs, technology decisions, NFR implementations  
**Size:** ~12 KB  
**Related Skills:** windows-app-requirements (input), windows-app-build (output)

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Design the data model"
- "Plan the architecture"
- "What entities do I need?"
- "Define the database schema"
- "Choose technologies"
- "How should I structure..."
- "Design the API"
- "Plan authentication"

**Context Indicators:**
- Requirements are already defined
- Discussion is about data structures
- Discussion is about system architecture
- Need to decide on technology stack
- Planning authentication/security approach

## ❌ DO NOT LOAD WHEN

- Requirements not yet defined (use requirements skill first)
- User is asking about UI/pages (use ui-design skill)
- User wants to implement code (use build skill)
- User wants to fix a bug (use build skill)
- User has existing package to modify (use build skill)

---

## When to Use This Skill

| User Says... | Action |
|--------------|--------|
| "Design the data model" | Entity/relationship design |
| "Plan the architecture" | Full system design |
| "Choose technologies" | Technology stack selection |
| "Define database schema" | Data model phase |
| "How should I structure..." | Architecture guidance |

---

## Standard Architecture

**Every application follows MVC with strict separation:**

```
┌─────────────────────────────────────────────────────────────┐
│  PRESENTATION LAYER (View)                                  │
│  - Jinja2 templates (templates/)                            │
│  - Static files (static/css, static/js, static/images)     │
│  - Display only - NO business logic                         │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  CONTROLLER LAYER (Routes)                                  │
│  - FastAPI routes (routes/*.py)                             │
│  - Request handling, input validation                       │
│  - Delegates to services - stays THIN                       │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  SERVICE LAYER (Business Logic)                             │
│  - Service classes (services/*.py)                          │
│  - Business rules, workflows, calculations                  │
│  - HTTP-independent - no Request objects                    │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  DATA LAYER (Model)                                         │
│  - SQLAlchemy models (models.py)                            │
│  - Database operations                                      │
│  - Pure data structure - NO business logic                  │
└─────────────────────────────────────────────────────────────┘
```

**Separation Rules:**

| Layer | Does | Does NOT |
|-------|------|----------|
| Model | Define data structure, relationships | Contain business logic |
| View | Display data, format for presentation | Query database, calculate |
| Controller | Route requests, call services | Contain business logic |
| Service | Business logic, validation | Handle HTTP, render templates |

---

## Data Model Design

### Step 1: Extract Entities from Requirements

Read user stories and identify the **nouns**:

From: "Create a **task** with a **category** assigned to a **project**"

Entities found:
- Task ✓
- Category ✓  
- Project ✓
- User ✓ (implied)

### Step 2: Define Relationships

| Pattern | Example | Implementation |
|---------|---------|----------------|
| One-to-Many | User has many Tasks | FK on Task |
| Many-to-Many | Task has many Tags | Association table |
| One-to-One | User has one Profile | FK with unique |
| Self-Referential | Category has parent | FK to same table |

**Deletion Behavior:**

| Behavior | When to Use | Example |
|----------|-------------|---------|
| CASCADE | Child meaningless without parent | Task → Comments |
| SET NULL | Child can exist alone | Project → Tasks |
| RESTRICT | Prevent if children exist | Category with Tasks |

### Step 3: Entity Specification

```markdown
## Entity: [Name]

**Description:** [What this represents]
**From Stories:** US-XXX, US-YYY

### Attributes

| Attribute | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| id | Integer | Yes | auto | Primary key |
| name | String(100) | Yes | - | Unique per scope |
| status | String(20) | Yes | "Active" | From config |
| created_at | DateTime | Yes | now() | Auto-set |
| updated_at | DateTime | Yes | now() | Auto-update |

### Relationships

| Related | Type | FK Location | On Delete |
|---------|------|-------------|-----------|
| User | M:1 | self.user_id | SET NULL |
| Tag | M:M | entity_tags | CASCADE |

### Indexes
- name (for search)
- status, created_at (for filtering)
```

### Step 4: Standard Attribute Patterns

```python
# Every entity should consider:

# Identity
id = Column(Integer, primary_key=True, autoincrement=True)

# Timestamps
created_at = Column(DateTime, server_default=func.now())
updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

# Ownership
created_by_id = Column(Integer, ForeignKey('users.id'))
owned_by_id = Column(Integer, ForeignKey('users.id'))

# Soft Delete
is_deleted = Column(Boolean, default=False)
deleted_at = Column(DateTime, nullable=True)

# Status
is_active = Column(Boolean, default=True)
```

**Type Guidelines:**

| Data | Type | Notes |
|------|------|-------|
| Short text | String(100-200) | Set max length |
| Long text | Text | No limit |
| Yes/No | Boolean | Always default |
| Date only | Date | No time |
| Date+time | DateTime | Consider timezone |
| Money | Numeric(10,2) | Never Float |
| Choices | String + API | No hardcoding |

---

## Technology Stack

### Standard Stack (Default)

| Layer | Technology | Why |
|-------|------------|-----|
| Backend | FastAPI | Async, modern, auto-docs |
| ORM | SQLAlchemy 2.0 | Mature, well-supported |
| Database | SQLite | Zero config, portable |
| Templates | Jinja2 | FastAPI native |
| Frontend | Bootstrap 5 + vanilla JS | No build step |
| Auth | Session-based | Simple, stateful |
| Packaging | Batch + venv | Windows native |

### When to Deviate

| Requirement | Consider Instead |
|-------------|------------------|
| 100+ concurrent users | PostgreSQL |
| Complex frontend state | React/Vue |
| Stateless scaling | JWT tokens |
| Team collaboration | Docker |
| Linux deployment | Shell scripts |

---

## Non-Functional Requirements Implementation

### Authentication Types

**Local Admin:**
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

**Google OAuth:**
```python
# Settings
GOOGLE_CLIENT_ID: Optional[str] = None
GOOGLE_CLIENT_SECRET: Optional[str] = None
GOOGLE_REDIRECT_URI: str = "http://localhost:8004/auth/google/callback"
ALLOWED_EMAIL_DOMAINS: str = ""  # Comma-separated

# Requires: authlib package
```

### Backup/Restore

**Backup Strategy:**
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

**Restore Points:**
- Before every update
- On scheduled basis
- On user request

### Business Continuity

**Health Check Endpoint:**
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

**Auto-Start Service:**
```batch
REM scripts/auto-start.bat
REM Add to Windows Task Scheduler for startup
```

### Cybersecurity

**Required Security Measures:**

| Measure | Implementation |
|---------|----------------|
| Password hashing | SHA-256 with salt (auth.py) |
| Session cookies | httponly=True, samesite="lax" |
| HTTPS in production | Reverse proxy (nginx) |
| Input validation | Pydantic models |
| SQL injection | SQLAlchemy ORM |
| XSS prevention | Jinja2 auto-escaping |
| CSRF protection | SessionMiddleware |

**Encryption at Rest:**
```python
# scripts/config_crypto.py
# Encrypts sensitive .env values for silent install
```

### Data Import/Export

**Export Patterns:**
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

**Import Patterns:**
```python
@router.post("/api/import/{entity}")
async def import_data(entity: str, file: UploadFile):
    # Parse and validate uploaded file
    # Insert records with conflict handling
    pass
```

---

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

---

## Theme System

**Three Modes Required:**
1. Light - Traditional light background
2. Dark - High-contrast dark background  
3. System - Follows OS preference

**Implementation:**
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

---

## Application Ontology

**Single Source of Names:**

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

---

## Design Deliverables Checklist

Before proceeding to Build phase:

- [ ] All entities defined with attributes
- [ ] All relationships documented with cardinality
- [ ] Foreign key delete behaviors decided
- [ ] Configuration options identified (no hardcoding)
- [ ] Technology stack selected and justified
- [ ] API endpoints designed
- [ ] Authentication strategy chosen
- [ ] Backup/restore approach defined
- [ ] Security measures identified
- [ ] Import/export requirements documented
- [ ] User approved system design

### Cross-Skill Validation

Before transitioning to **windows-app-build**:
- [ ] Every user story's data needs are covered by entities
- [ ] Entity attributes support all form fields in UI design
- [ ] API endpoints support all UI interactions
- [ ] Authentication supports all user roles from requirements

**Validation with requirements skill:**
- [ ] Each P0 user story maps to at least one entity
- [ ] NFRs are addressed by technology choices

**Validation with ui-design skill:**
- [ ] Entity field names match form field names exactly
- [ ] Configuration options support all dropdowns
- [ ] API endpoints exist for all AJAX interactions

**If any item fails:** Resolve before loading build skill.

---

## Exit Gate Questions

Ask the user:

1. "Does this data model capture all the information you need?"
2. "Are the relationships correct?"
3. "What options should be configurable?"
4. "Is the authentication approach appropriate?"
5. "Are there specific security requirements?"

**When user confirms → Proceed to windows-app-build skill**

---

## Common Design Patterns

### User/Auth Pattern
```
User
├── id, email, password_hash
├── name, is_admin, is_active
└── created_at, last_login
```

### Lookup Table (No Hardcoding)
```
SystemSetting
├── id, key (unique), value (JSON)
└── For: dropdown options, app config
```

### Audit Trail
```
AuditLog
├── entity_type, entity_id
├── action, old_values, new_values
└── user_id, timestamp
```

### Hierarchical (Self-Reference)
```
Category
├── id, name, parent_id (FK to self)
└── level (computed)
```

---

## Red Flags to Address

| Red Flag | Risk | Resolution |
|----------|------|------------|
| Entity 30+ attributes | God object | Split into related entities |
| No timestamps | Can't track history | Add created_at, updated_at |
| Hardcoded options | Can't customize | Create lookup table |
| Unclear ownership | Auth holes | Add user_id FKs |
| Float for money | Rounding errors | Use Numeric(10,2) |
| No soft delete | Can't recover | Add is_deleted flag |
| Single-tenant model | Scaling issues | Add venue/org FK from start |
| Column name ≠ form field | Runtime errors | Document naming in ontology |

---

## Critical: Model-Route-Form Alignment

**Column names in models MUST match parameter names in routes and form fields.**

```python
# models.py          routes/services.py       templates/form.html
time = Column(...)   time: str = Form(...)    name="time"
# All three MUST match exactly
```

Use the Ontology to document and enforce naming consistency.

## Critical: Attribute Naming Conventions

**Establish naming conventions during design to prevent implementation errors:**

### Avoid Verbose Prefixes in Column Names

| Verbose (Avoid) | Concise (Prefer) | Why |
|-----------------|------------------|-----|
| liturgical_season | season | Context implicit in model |
| liturgical_color | season_color | Shorter, still clear |
| sermon_preacher | preacher | OR keep if other preachers exist |
| sequence_order | sort_order | Standard convention |

### Document Naming Decisions

Create a field mapping table in design docs:

```markdown
| Concept | Model Field | Form Field | API Field |
|---------|-------------|------------|-----------|
| Liturgical season | season | season | season |
| Season color | season_color | season_color | seasonColor |
| Service time | time | service_time | time |
```

### Pre-Implementation Naming Review

Before transitioning to build phase, verify:
- [ ] No verbose prefixes that could be shortened
- [ ] Consistent naming across related models
- [ ] Field names documented in ontology.py or design doc
- [ ] Form field names match model column names

---

## Critical: Seed Data Validation

Every column used in seed data MUST exist in the model:

```python
# ✗ ERROR: is_default not in model
venue = Venue(name="Main", is_default=True)

# ✓ FIRST add column to model, THEN use in seed data
```

---

## Critical: Multi-Tenant Design

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

---

## Critical: Consistent Naming

Establish naming conventions early. Document the pattern:

```markdown
Pattern: "[Ordinal] [Unit] of [Category]"
Examples: "First Sunday of Advent", "Second Sunday of Lent"
```

---

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

---

*End of Windows Application System Design Skill*
