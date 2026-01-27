# Security Skills - Authentication & Secure Coding

Coordinated security implementation for Windows applications.

**Sub-Category:** windows-app/security
**Skills:** 3 (1 orchestrator + 2 specialized)
**Total Size:** ~29KB SKILL.md + ~58KB references

---

## Overview

Security skills use an orchestrator pattern to route between authentication and secure coding patterns based on implementation context.

```
security-patterns-orchestrator
├─→ authentication-patterns (OAuth, sessions, first-user admin)
└─→ secure-coding-patterns (XSS, CSRF, SQL injection, input validation)
```

---

## Skills in This Sub-Category

### security-patterns-orchestrator (~7KB)
**Purpose:** Route to appropriate security skill based on context

**When to load:**
- "Add OAuth login..."
- "Implement authentication..."
- "Secure this form..."
- "Add file upload..."
- "Run security audit..."

**Routing logic:**

| User Says | Load |
|-----------|------|
| "Add Google OAuth" | authentication-patterns ONLY |
| "Create login form" | authentication-patterns + secure-coding-patterns |
| "Add user registration" | secure-coding-patterns ONLY |
| "Secure file upload" | secure-coding-patterns ONLY |
| "Security audit" | BOTH (comprehensive check) |

**Exit gates:**
- After OAuth implementation → Mark auth complete
- After form security → Mark validation complete
- Before SHIP mode → Run security checklist

---

### authentication-patterns (~10KB + 30KB ref)
**Purpose:** OAuth-first authentication with Google/Microsoft

**When to load:**
- Implementing OAuth 2.0
- Setting up Google login
- Configuring Microsoft Azure AD
- First-user admin pattern needed

**Key patterns:**
1. **OAuth-First:** No password forms, OAuth only
2. **Cookie Separation:** OAuth state ≠ auth session (CRITICAL)
3. **First-User Admin:** First user automatically gets ADMIN role
4. **Domain Restriction:** Optional email domain filtering

**References:**
- oauth-examples.md (15KB)
  - Complete Google OAuth implementation
  - Complete Microsoft OAuth implementation
  - Common pitfalls and solutions
  - Manual testing procedures

- regression-tests.md (15KB)
  - Cookie separation tests
  - First-user admin tests
  - Domain restriction tests
  - State validation tests
  - Session management tests

**Critical errors prevented:**
- E005: Login loop (OAuth cookie = session cookie)
- E006: Google OAuth 400 (private IP in redirect_uri)
- E014: Non-admin first user (role assignment missing)

---

### secure-coding-patterns (~12KB + 28KB ref)
**Purpose:** Prevent XSS, CSRF, SQL injection, and other vulnerabilities

**When to load:**
- Creating forms
- Handling user input
- Implementing file upload
- Preventing XSS/CSRF
- Running security audits

**Key patterns:**
1. **Input Validation:** Pydantic models, server-side validation
2. **CSRF Protection:** Tokens in all POST forms
3. **XSS Prevention:** Auto-escaping, no `| safe` without justification
4. **SQL Injection:** Parameterized queries, SQLAlchemy ORM
5. **File Upload Security:** Extension whitelist, MIME validation, UUID filenames

**References:**
- security-checklists.md (12KB)
  - Pre-commit security checklist
  - Code review security checklist
  - Penetration testing checklist
  - Incident response checklist

- vulnerability-examples.md (16KB)
  - SQL injection (vulnerable → exploit → fix)
  - XSS (reflected and stored)
  - CSRF attacks
  - IDOR (Insecure Direct Object Reference)
  - Path traversal
  - Command injection
  - File upload attacks
  - Broken authentication
  - Missing security headers

**Critical errors prevented:**
- SQL injection via string concatenation
- XSS via `| safe` filter abuse
- CSRF via missing token validation
- IDOR via missing ownership checks
- Path traversal via user-controlled filenames

---

## Integration with windows-app-build

Security skills are often loaded alongside windows-app-build:

### Pattern 1: OAuth Implementation

```
User: "Add Google OAuth login"
→ windows-app-build loads (primary)
→ security-patterns-orchestrator detects "OAuth"
→ authentication-patterns loads (specialized)

Both skills active:
- Build handles route creation
- Auth validates OAuth patterns
- Build runs tests
- Auth confirms no cookie collisions
```

### Pattern 2: Form Creation

```
User: "Create booking form with file upload"
→ windows-app-build loads (primary)
→ security-patterns-orchestrator detects "form" + "upload"
→ secure-coding-patterns loads (specialized)

Both skills active:
- Build creates form route and template
- Security validates CSRF tokens
- Security validates file upload security
- Build runs tests
```

### Pattern 3: Security Audit (Pre-SHIP)

```
User: "Ready to deliver, run security audit"
→ windows-app-build loads (SHIP mode)
→ security-patterns-orchestrator loads (audit)
→ authentication-patterns checks auth patterns
→ secure-coding-patterns runs checklists

All three active:
- Auth validates OAuth implementation
- Secure validates input handling
- Build runs all tests
- All checklists verified
```

---

## Security Workflow

### Phase 1: Design (Before Implementation)

**Questions to answer:**
- What authentication method? (OAuth vs password)
- Which OAuth provider? (Google, Microsoft, both)
- Domain restriction needed?
- What user roles? (Admin, Staff, User)

**Output:**
- Authentication strategy documented
- OAuth provider configured
- Redirect URIs registered

### Phase 2: Implementation

**Tasks:**
1. Implement OAuth routes (`/login`, `/auth/callback`)
2. Separate OAuth state and session cookies
3. Configure first-user admin logic
4. Add CSRF tokens to all forms
5. Implement input validation
6. Secure file uploads (if applicable)

**Validation:**
- Regression tests pass
- Security checklist complete
- No hardcoded secrets

### Phase 3: Testing

**Tests:**
- OAuth flow (login, callback, logout)
- Cookie separation (state ≠ session)
- First user becomes admin
- Domain restriction (if configured)
- CSRF protection (reject missing tokens)
- Input validation (reject malicious input)
- File upload security (reject dangerous files)

### Phase 4: Audit (Pre-Deployment)

**Checklists:**
- [ ] Pre-commit security checklist (from secure-coding-patterns)
- [ ] Code review security checklist
- [ ] Penetration testing (manual)
- [ ] All regression tests pass

---

## Common Security Issues

### Issue 1: Cookie Name Collision

**Symptom:** Login redirects back to login page immediately

**Root Cause:** OAuth state cookie has same name as session cookie

**Fix:**
```python
# WRONG
OAUTH_STATE_COOKIE = "session"  # Collides!
SESSION_COOKIE = "session"

# RIGHT
OAUTH_STATE_COOKIE_NAME = "oauth_state"
SESSION_COOKIE_NAME = "session"
```

**Reference:** authentication-patterns/references/regression-tests.md

---

### Issue 2: Private IP in redirect_uri

**Symptom:** Google OAuth returns 400 "redirect_uri_mismatch"

**Root Cause:** Using `192.168.x.x` in BASE_URL

**Fix:**
```python
# WRONG
BASE_URL = "http://192.168.0.100:8008"

# RIGHT (development)
BASE_URL = "http://localhost:8008"

# RIGHT (production)
BASE_URL = "https://app.example.com"
```

**Reference:** authentication-patterns/references/oauth-examples.md#common-pitfalls

---

### Issue 3: XSS via | safe

**Symptom:** Malicious JavaScript executes on page

**Root Cause:** Using `| safe` filter without sanitizing input

**Fix:**
```html
<!-- WRONG -->
<div>{{ user_input | safe }}</div>

<!-- RIGHT: Auto-escape (default) -->
<div>{{ user_input }}</div>

<!-- RIGHT: Sanitize first if HTML needed -->
<div>{{ sanitized_html | safe }}</div>
```

**Reference:** secure-coding-patterns/references/vulnerability-examples.md#xss

---

## Security Testing Matrix

| Test Type | Skill | Reference |
|-----------|-------|-----------|
| OAuth flow | authentication-patterns | regression-tests.md |
| Cookie separation | authentication-patterns | regression-tests.md |
| First-user admin | authentication-patterns | regression-tests.md |
| CSRF protection | secure-coding-patterns | vulnerability-examples.md |
| XSS prevention | secure-coding-patterns | vulnerability-examples.md |
| SQL injection | secure-coding-patterns | vulnerability-examples.md |
| File upload | secure-coding-patterns | vulnerability-examples.md |
| Pre-commit checks | secure-coding-patterns | security-checklists.md |

---

## Best Practices

### 1. Load Security Early

Don't wait until bugs appear - load security skills during initial implementation:

```
User: "Create login page"
→ IMMEDIATELY load security-patterns-orchestrator
→ Implement correctly from start
→ Avoid rework later
```

### 2. Use Regression Tests

Every security fix should have a regression test:

```python
def test_regression_cookie_separation():
    """Regression: OAuth state cookie must differ from session cookie.

    Fixed in build 26015-1430
    Root cause: Both named "session"
    """
    assert settings.OAUTH_STATE_COOKIE_NAME != settings.SESSION_COOKIE_NAME
```

### 3. Run Checklists Before SHIP

**Pre-delivery security audit:**
- [ ] Run pre-commit checklist (grep commands)
- [ ] Manual penetration testing
- [ ] All regression tests pass
- [ ] No secrets in code

### 4. Document Vulnerabilities

Log all security issues in ERROR-AND-FIXES-LOG.md:

```markdown
### Error 23: XSS via | safe Filter
**Error**: Malicious script executed on profile page
**Root Cause**: User bio displayed with `| safe` without sanitization
**Fix**: Removed `| safe`, use auto-escaping
**Prevention**: Never use `| safe` on user input
```

---

## Related Skills

- **windows-app-build** - Primary implementation skill
- **windows-app-orchestrator** - Phase coordinator
- **navigation-auditor** - Verify auth routes accessible

---

*Security Sub-Category - OAuth-First Authentication & Secure Coding*
