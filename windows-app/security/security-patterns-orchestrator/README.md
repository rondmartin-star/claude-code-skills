# security-patterns-orchestrator

Coordinate security skill loading based on implementation context. Routes between authentication-patterns and secure-coding-patterns to ensure comprehensive security implementation.

---

## Size

- **SKILL.md:** ~7KB
- **References:** None (routes to other skills' references)
- **Total:** ~7KB

---

## When to Load

### Trigger Phrases

- "Add OAuth login"
- "Implement authentication"
- "Add Google/Microsoft login"
- "Secure this form"
- "Add file upload"
- "Handle user input"
- "Security audit"
- "Run security checklist"
- "Prevent XSS/CSRF"

### Context Indicators

- User mentions authentication
- Form creation with user input
- File upload implementation
- Security concerns
- Pre-deployment validation

---

## Purpose

This orchestrator determines which security skill(s) to load based on the implementation context:

- **Authentication-only tasks** → Load authentication-patterns
- **Input validation tasks** → Load secure-coding-patterns
- **Combined tasks** → Load both skills
- **Security audits** → Load both skills

---

## Routing Logic

### Decision Matrix

| User Says | Context | Load | Rationale |
|-----------|---------|------|-----------|
| "Add Google OAuth" | OAuth setup | authentication-patterns ONLY | OAuth configuration, no input handling yet |
| "Create login form" | Login implementation | authentication + secure-coding | Auth setup + form security together |
| "Add user registration" | Registration form | secure-coding-patterns ONLY | Input validation, no OAuth setup needed |
| "Secure file upload" | File handling | secure-coding-patterns ONLY | Input validation and security patterns |
| "Add admin login" | Admin auth | authentication + secure-coding | Both OAuth and role-based access control |
| "Security audit" | Pre-deployment | BOTH | Comprehensive security validation |

### Three Routing Modes

**Mode 1: Authentication-Only**
- OAuth flow implementation
- Session management
- First-user admin pattern
- Domain restriction
- Cookie configuration

**Mode 2: Secure-Coding-Only**
- Input validation
- CSRF protection
- XSS prevention
- SQL injection prevention
- File upload security

**Mode 3: Both Skills**
- Login forms (auth + validation)
- Registration forms (creation + security)
- Admin panels (auth + access control)
- Comprehensive audits

---

## Integration with windows-app-build

The orchestrator is typically loaded alongside windows-app-build:

```
User: "Add Google OAuth login"
→ windows-app-build loads (primary, handles routes)
→ security-patterns-orchestrator loads (coordinator)
→ authentication-patterns loads (specialist)

Three skills active:
- Build: Creates routes and templates
- Security Orch: Coordinates security validation
- Auth: Validates OAuth patterns
```

---

## Exit Gates

The orchestrator defines when security implementation is complete:

### After OAuth Implementation

- [ ] OAuth routes created (`/login`, `/auth/callback`)
- [ ] State and session cookies separated (different names)
- [ ] First-user admin logic implemented
- [ ] Domain restriction configured (if needed)
- [ ] Regression tests added

**Exit:** Mark authentication complete, unload authentication-patterns

### After Form Security

- [ ] CSRF tokens in all POST forms
- [ ] Input validation (server-side with Pydantic)
- [ ] XSS prevention (auto-escaping verified)
- [ ] File uploads secured (if applicable)
- [ ] Security checklist passed

**Exit:** Mark input validation complete, unload secure-coding-patterns

### Before SHIP Mode

- [ ] Pre-commit security checklist run
- [ ] All regression tests pass
- [ ] No hardcoded secrets
- [ ] Security patterns validated

**Exit:** All security skills can unload, ready for deployment

---

## Reference Files

This orchestrator doesn't have its own references - it routes to:

**authentication-patterns/references/**
- oauth-examples.md (15KB) - Google/Microsoft OAuth implementations
- regression-tests.md (15KB) - Cookie, admin, domain tests

**secure-coding-patterns/references/**
- security-checklists.md (12KB) - Pre-commit, code review, pentesting
- vulnerability-examples.md (16KB) - XSS, CSRF, SQL injection examples

---

## Related Skills

### Coordinates

- **authentication-patterns** - OAuth implementation specialist
- **secure-coding-patterns** - Input validation specialist

### Works With

- **windows-app-build** - Primary implementation skill
- **windows-app-orchestrator** - Phase coordinator (loads this skill when needed)

### Loads From

- **windows-app-build** - When auth/security tasks detected
- **windows-app-orchestrator** - During build phase with security requirements

---

## Common Workflows

### Workflow 1: OAuth Implementation

```
User: "Add Google OAuth login"
→ windows-app-build
→ security-patterns-orchestrator
→ authentication-patterns

Process:
1. Create OAuth routes
2. Separate state and session cookies
3. Implement first-user admin
4. Add regression tests
5. Validate patterns
6. Exit: OAuth complete
```

### Workflow 2: Secure Form

```
User: "Create booking form with validation"
→ windows-app-build
→ security-patterns-orchestrator
→ secure-coding-patterns

Process:
1. Create form route and template
2. Add CSRF token
3. Implement Pydantic validation
4. Ensure auto-escaping
5. Run security checklist
6. Exit: Form secure
```

### Workflow 3: Combined (Login Form)

```
User: "Create login page with OAuth"
→ windows-app-build
→ security-patterns-orchestrator
→ authentication-patterns + secure-coding-patterns

Process:
1. Create login route
2. Implement OAuth flow (auth skill)
3. Validate form security (secure skill)
4. Test cookie separation
5. Run all security checks
6. Exit: Login complete and secure
```

### Workflow 4: Security Audit

```
User: "Run security audit before deployment"
→ windows-app-build (SHIP mode)
→ security-patterns-orchestrator
→ authentication-patterns + secure-coding-patterns

Process:
1. Check OAuth implementation (auth)
2. Run pre-commit checklist (secure)
3. Validate all patterns
4. Run all regression tests
5. Generate audit report
6. Exit: Ready for deployment
```

---

## Best Practices

### 1. Load Early

Don't wait for security bugs - load during initial implementation:

```
User: "Create user management"
→ IMMEDIATELY load security-patterns-orchestrator
→ Implement security patterns from start
→ Avoid rework later
```

### 2. Use Both Skills When Appropriate

Don't assume one is enough:

```
OAuth + Form = authentication-patterns + secure-coding-patterns
Not just one or the other
```

### 3. Run Comprehensive Audits

Before SHIP mode, always load both skills for full validation:

```
Pre-deployment = Load both skills, run all checklists
```

### 4. Document Exit Criteria

Clearly define when each skill can be unloaded:

```
Auth complete: OAuth working, tests passing
Secure complete: Checklists passed, no vulnerabilities
```

---

## Version

- **Version:** 1.0
- **Created:** 2026-01-27
- **Last Updated:** 2026-01-27
- **Status:** Production

---

*Security Patterns Orchestrator - Coordinated Security Implementation*
