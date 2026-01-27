---
name: security-patterns-orchestrator
description: >
  Coordinate security skill loading based on implementation context. Routes between
  authentication-patterns and secure-coding-patterns. Ensures security validation
  during build phase. Load when: implementing authentication, handling user input,
  or running security audits.
---

# Security Patterns Orchestrator

**Purpose:** Load only the security skills needed for the current context
**Size:** ~7KB (intentionally minimal)
**Action:** Detect security context → Load relevant skill(s) → Validate

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "implement authentication"
- "add login"
- "secure this form"
- "handle user input"
- "file upload"
- "add OAuth"
- "security audit"
- "add Google login"
- "user registration"

**Context Indicators:**
- User mentions security in context of windows-app development
- Build skill detects authentication or form implementation
- SHIP mode requires security validation
- Form handling or file upload features

## ❌ DO NOT LOAD WHEN

- General security discussion (not specific to windows-app)
- Reading security documentation
- Security unrelated to authentication or input handling

---

## Routing Logic

### Decision Matrix

| User Says | Context | Load | Rationale |
|-----------|---------|------|-----------|
| "Add Google OAuth" | OAuth setup | authentication-patterns ONLY | OAuth configuration, no input handling yet |
| "Create login form" | Login implementation | authentication-patterns + secure-coding-patterns | Auth setup + form security together |
| "Add user registration" | Registration form | secure-coding-patterns ONLY | Input validation, no OAuth setup needed |
| "File upload feature" | File handling | secure-coding-patterns ONLY | File security patterns only |
| "Security audit" | Pre-delivery | BOTH (in sequence) | Comprehensive security review |
| "Add forgot password" | Password reset | authentication-patterns + secure-coding-patterns | Auth flow + form handling |

### Skill Loading Paths

```python
# Authentication setup (OAuth, session management)
"~/.claude/skills/windows-app/security/authentication-patterns/SKILL.md"  # ~5.6KB

# Secure implementation (forms, queries, templates)
"~/.claude/skills/windows-app/security/secure-coding-patterns/SKILL.md"  # ~12.5KB
```

**Rules:**
- Load authentication-patterns for OAuth/session setup
- Load secure-coding-patterns for form/input/file handling
- Load BOTH when feature involves authentication AND user input
- Always validate security before SHIP mode

---

## Integration with windows-app-build

### Build Skill Auto-Loads Security Orchestrator When:

**Scenario 1: ADD mode + authentication feature**
- **Detects:** "login", "OAuth", "session", "auth" in feature description
- **Action:** Load security-patterns-orchestrator → routes to authentication-patterns
- **Example:** "Add Google OAuth login" → authentication-patterns

**Scenario 2: ADD mode + user input feature**
- **Detects:** "form", "input", "upload", "query" in feature description
- **Action:** Load security-patterns-orchestrator → routes to secure-coding-patterns
- **Example:** "Add contact form" → secure-coding-patterns

**Scenario 3: SHIP mode (before delivery)**
- **Always run security validation**
- **Action:** Load secure-coding-patterns for checklist validation
- **Check:** All security requirements met

### Validation Points

```
During Development (ADD/FIX):
│
├─ Authentication feature detected
│  └─ Load authentication-patterns
│     ├─ Validate: Cookie separation (auth ≠ state)
│     ├─ Validate: First user gets ADMIN role
│     ├─ Validate: Domain restriction configured
│     └─ Validate: No password form (OAuth-only)
│
├─ Form feature detected
│  └─ Load secure-coding-patterns
│     ├─ Validate: CSRF token in all POST forms
│     ├─ Validate: Server-side validation
│     ├─ Validate: No |safe on user content
│     └─ Validate: No nested forms
│
└─ File upload detected
   └─ Load secure-coding-patterns
      ├─ Validate: Extension whitelist defined
      ├─ Validate: MIME type validation
      ├─ Validate: Size limits enforced
      └─ Validate: Safe filename generation (UUID)

Before Delivery (SHIP):
│
└─ Run complete security checklist
   ├─ Authentication & Authorization
   ├─ Input Handling
   ├─ Output Rendering
   ├─ Database Queries
   └─ Configuration Security
```

---

## Exit Gates

### After Authentication Implementation

Before proceeding:
- [ ] OAuth state cookie ≠ auth session cookie (separate cookie names)
- [ ] First user automatically receives ADMIN role
- [ ] Domain restriction configured (if applicable)
- [ ] Login page has NO password form (OAuth-only)
- [ ] Session expiry configured
- [ ] Logout clears all auth cookies

### After Form Implementation

Before proceeding:
- [ ] CSRF token present in all POST forms
- [ ] Server-side validation implemented (never trust client)
- [ ] No |safe filter on user-provided content
- [ ] No nested forms (use JavaScript for sub-operations)
- [ ] Form errors display safely (no raw error messages)
- [ ] Input sanitization in place

### After File Upload Implementation

Before proceeding:
- [ ] Extension whitelist defined (e.g., .jpg, .png, .pdf)
- [ ] MIME type validation (not just extension check)
- [ ] File size limits enforced
- [ ] Safe filename generation (UUID, no user input)
- [ ] Files stored outside webroot
- [ ] Virus scanning enabled (if available)

### Before SHIP Mode

Before delivery:
- [ ] All authentication exit gates passed
- [ ] All form exit gates passed
- [ ] All file upload exit gates passed (if applicable)
- [ ] No hardcoded secrets in code
- [ ] All routes have appropriate auth checks
- [ ] Security audit clean (no warnings)

---

## Common Security Patterns

### When to Load Both Skills

Load authentication-patterns + secure-coding-patterns together when:
1. **Login form creation:** OAuth setup + form security
2. **Registration with profile:** Auth setup + input validation
3. **Password reset flow:** Auth management + form handling
4. **Admin user creation:** Auth roles + input validation

### Load Order

```
1. Load authentication-patterns FIRST (OAuth/session setup)
2. Then load secure-coding-patterns (form/input security)
3. Validate authentication setup
4. Then validate form security
```

### Context Budget

| Scenario | Skills Loaded | Total Size |
|----------|---------------|------------|
| OAuth only | orchestrator + auth | ~13KB |
| Forms only | orchestrator + secure-coding | ~20KB |
| Auth + Forms | orchestrator + both | ~25KB |
| Security audit | orchestrator + both | ~25KB |

---

## Error Recovery

If wrong security skill loaded:
1. **Note what was needed vs. what was loaded**
2. **Load correct skill explicitly**
3. **Update routing logic if pattern was missed**

Example:
```
User: "Add file upload"
Loaded: authentication-patterns (wrong)
Should have: secure-coding-patterns
Fix: Load secure-coding-patterns now
Update: Add "file upload" to secure-coding triggers
```

---

## Cross-Skill Coordination

### With windows-app-build

- **Automatic loading:** Build skill automatically loads this orchestrator when security keywords detected
- **Manual loading:** User can explicitly request "security review" or "audit security"
- **SHIP mode:** Always runs security validation

### With Other Skills

- **windows-app-orchestrator:** May route to this orchestrator based on context
- **conversation-snapshot:** Security decisions documented in snapshot
- **skill-ecosystem-manager:** Security patterns fed back for skill improvement

---

## Quick Reference

### Skill Selection Flowchart

```
Is this about authentication/OAuth?
│
├─ YES → authentication-patterns
│   │
│   └─ Does it also involve forms?
│       │
│       ├─ YES → Load secure-coding-patterns too
│       └─ NO → Just authentication-patterns
│
└─ NO → Is it about user input/forms/files?
    │
    ├─ YES → secure-coding-patterns
    └─ NO → Neither skill needed
```

---

*End of Security Patterns Orchestrator*
