# Entity Design Templates and Patterns

## Entity Specification Template

Use this template when documenting each entity:

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

## Standard Attribute Patterns

Every entity should consider these standard patterns:

```python
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

## Type Guidelines

| Data | Type | Notes |
|------|------|-------|
| Short text | String(100-200) | Set max length |
| Long text | Text | No limit |
| Yes/No | Boolean | Always default |
| Date only | Date | No time |
| Date+time | DateTime | Consider timezone |
| Money | Numeric(10,2) | Never Float |
| Choices | String + API | No hardcoding |

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

## Relationship Patterns

| Pattern | Example | Implementation |
|---------|---------|----------------|
| One-to-Many | User has many Tasks | FK on Task |
| Many-to-Many | Task has many Tags | Association table |
| One-to-One | User has one Profile | FK with unique |
| Self-Referential | Category has parent | FK to same table |

## Deletion Behavior

| Behavior | When to Use | Example |
|----------|-------------|---------|
| CASCADE | Child meaningless without parent | Task → Comments |
| SET NULL | Child can exist alone | Project → Tasks |
| RESTRICT | Prevent if children exist | Category with Tasks |

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

## Attribute Naming Conventions

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

## Critical: Model-Route-Form Alignment

**Column names in models MUST match parameter names in routes and form fields.**

```python
# models.py          routes/services.py       templates/form.html
time = Column(...)   time: str = Form(...)    name="time"
# All three MUST match exactly
```

Use the Ontology to document and enforce naming consistency.

## Critical: Seed Data Validation

Every column used in seed data MUST exist in the model:

```python
# ✗ ERROR: is_default not in model
venue = Venue(name="Main", is_default=True)

# ✓ FIRST add column to model, THEN use in seed data
```
