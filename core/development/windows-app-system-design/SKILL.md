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
**Size:** ~10 KB
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

Quick reference:

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

**For detailed entity specification template and standard attribute patterns:**
```
references/entity-templates.md
```

Quick checklist per entity:
- [ ] Primary key (id)
- [ ] Timestamps (created_at, updated_at)
- [ ] Ownership (created_by_id, owned_by_id)
- [ ] Soft delete (is_deleted, deleted_at) if needed
- [ ] Status field (is_active) if needed
- [ ] Relationships with cardinality
- [ ] Deletion behaviors decided

### Step 4: Naming Conventions

**Critical: Model-Route-Form Alignment**

Column names in models MUST match parameter names in routes and form fields.

```python
# models.py          routes/services.py       templates/form.html
time = Column(...)   time: str = Form(...)    name="time"
# All three MUST match exactly
```

**Avoid verbose prefixes:**
- liturgical_season → season
- sermon_preacher → preacher (unless multiple preacher types)
- sequence_order → sort_order

**Document naming decisions in ontology.py or design doc.**

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

## Non-Functional Requirements

**For detailed NFR implementation code and patterns:**
```
references/nfr-implementation.md
```

### Authentication Types Quick Reference

**Local Admin:**
- SHA-256 with salt (auth.py SACRED FILE)
- Password hashing and verification functions

**Google OAuth:**
- Settings: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
- Requires: authlib package

### Backup/Restore

**Strategy:**
- Backup script: scripts/backup.bat
- Includes database + .env files
- Restore points: before updates, scheduled, on request

### Business Continuity

**Required:**
- Health check endpoint (/health)
- Auto-start service (Task Scheduler)
- Database connection monitoring

### Cybersecurity

**Minimum Security Measures:**
- Password hashing (SHA-256 + salt)
- Session cookies (httponly=True, samesite="lax")
- Input validation (Pydantic)
- SQL injection prevention (ORM)
- XSS prevention (Jinja2 auto-escaping)
- CSRF protection (SessionMiddleware)

### Data Import/Export

**Patterns:**
- Export: GET /api/export/{entity} (CSV/JSON)
- Import: POST /api/import/{entity} (file upload)
- Backup download: GET /api/backup/download

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

### Configuration API (No Hardcoding)

All dropdown options and configurable values from API:

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

**Implementation:** See references/nfr-implementation.md for code

---

## Application Ontology

**Single Source of Names:**

```python
# app/ontology.py
"""Define ALL names here. Reference from code. NEVER invent names elsewhere."""
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
- [ ] Naming conventions documented
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

**For detailed pattern implementations:**
```
references/entity-templates.md
references/patterns.md
```

Quick reference:
- User/Auth Pattern
- Lookup Table (No Hardcoding)
- Audit Trail
- Hierarchical (Self-Reference)
- Multi-Tenant Design
- Integration Services

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

## Critical Reminders

1. **Seed Data Validation:** Every column used in seed data MUST exist in the model first
2. **Multi-Tenant Design:** Ask early: "Will there ever be multiple venues/locations/organizations?"
3. **Consistent Naming:** Establish and document naming patterns early
4. **No Hardcoding:** All dropdown options and config values from API/database

---

## Reference Files

**Detailed templates and examples:**
- `references/entity-templates.md` - Entity specs, attributes, patterns
- `references/nfr-implementation.md` - Auth, backup, security, API code
- `references/patterns.md` - Multi-tenant, integration services

---

*End of Windows Application System Design Skill*
