# Security Checklists Reference

Load this file when running security audits, code reviews, or pre-commit checks.

---

## Pre-Commit Security Checklist

Run these checks before every commit to catch security issues early.

### Authentication & Session Management

```bash
# Check for hardcoded secrets
grep -rn "password\s*=\s*['\"][^'\"]\+" app/ --include="*.py"
grep -rn "api_key\s*=\s*['\"][^'\"]\+" app/ --include="*.py"
grep -rn "secret\s*=\s*['\"][^'\"]\+" app/ --include="*.py"

# Check for hardcoded cookie names
grep -rn '"session_token"' app/ --include="*.py" | grep -v "settings\."

# Verify session middleware configuration
grep -rn "SessionMiddleware" app/ --include="*.py"
# Expected: ONE instance in main.py with secret_key and session_cookie parameters

# Check for secure cookie flags
grep -rn "secure=True" app/ --include="*.py"
# Should be present when BASE_URL starts with https://

# Check for httponly cookie flags
grep -rn "httponly=True" app/ --include="*.py"
# Should be present on all session cookies
```

**Pass criteria:**
- [ ] No hardcoded secrets found
- [ ] No hardcoded cookie names (use settings.SESSION_COOKIE_NAME)
- [ ] SessionMiddleware configured with secret_key
- [ ] secure=True when using HTTPS
- [ ] httponly=True on session cookies

### Input Validation

```bash
# Check for raw SQL queries (SQL injection risk)
grep -rn "execute\s*(" app/ --include="*.py" | grep -v "session.execute"

# Check for string formatting in queries
grep -rn "f['\"].*SELECT" app/ --include="*.py"
grep -rn "%s.*SELECT" app/ --include="*.py"

# Check for file path operations without validation
grep -rn "open(" app/ --include="*.py"
# Verify each instance validates/sanitizes the path

# Check for eval/exec usage (code injection risk)
grep -rn "eval\s*(" app/ --include="*.py"
grep -rn "exec\s*(" app/ --include="*.py"
```

**Pass criteria:**
- [ ] No raw SQL string concatenation
- [ ] All database queries use parameterized statements
- [ ] File paths validated before use
- [ ] No eval() or exec() usage

### XSS Protection

```bash
# Check for unescaped output in templates
grep -rn "| safe" templates/ --include="*.html"
grep -rn "{% autoescape off %}" templates/ --include="*.html"

# Check for innerHTML usage
grep -rn "innerHTML" static/ --include="*.js"

# Verify Content-Security-Policy headers
grep -rn "Content-Security-Policy" app/ --include="*.py"
```

**Pass criteria:**
- [ ] All `| safe` filters justified and documented
- [ ] No autoescape disabled unless absolutely necessary
- [ ] No innerHTML usage (use textContent/createElement)
- [ ] CSP headers configured

### CSRF Protection

```bash
# Check all POST routes have CSRF protection
grep -rn "@router.post" app/routes/ --include="*.py" -A 5 | grep -i "csrf"

# Verify forms include CSRF tokens
grep -rn "<form" templates/ --include="*.html" -A 5 | grep -v "csrf_token"
# Flag any forms without csrf_token input
```

**Pass criteria:**
- [ ] All POST/PUT/DELETE routes verify CSRF token
- [ ] All forms include CSRF token field
- [ ] CSRF tokens generated per session

### File Upload Security

```bash
# Check for file upload handlers
grep -rn "UploadFile" app/ --include="*.py"
grep -rn "\.save\s*(" app/ --include="*.py"

# Verify file extension validation
grep -rn "ALLOWED_EXTENSIONS" app/ --include="*.py"

# Check for MIME type validation
grep -rn "content_type" app/ --include="*.py"

# Verify UUID/random filenames used
grep -rn "uuid.uuid4" app/ --include="*.py"
```

**Pass criteria:**
- [ ] File extensions validated against whitelist
- [ ] MIME types validated (not just extension)
- [ ] Files saved with UUID filenames (not user-provided names)
- [ ] Upload size limits enforced

### Authorization & Access Control

```bash
# Check for missing authorization checks
grep -rn "@router\.(get|post|put|delete)" app/routes/ --include="*.py" -A 2 | grep -v "current_user"
# Flag routes that don't check authentication

# Verify role-based access control
grep -rn "UserRole\." app/ --include="*.py"
grep -rn "require_role" app/ --include="*.py"

# Check for direct object references
grep -rn "\.id\s*==" app/ --include="*.py"
# Verify each instance checks ownership
```

**Pass criteria:**
- [ ] All protected routes check authentication
- [ ] Role-based access implemented consistently
- [ ] Direct object references validated (IDOR prevention)
- [ ] User can only access their own resources

---

## Code Review Security Checklist

Use this checklist when reviewing code for security issues.

### Authentication Flow Review

- [ ] **Password Storage:** Passwords hashed with bcrypt/argon2 (not MD5/SHA1)
- [ ] **Password Validation:** Minimum length enforced (8+ characters)
- [ ] **Login Rate Limiting:** Failed login attempts rate-limited
- [ ] **Session Expiration:** Sessions expire after inactivity
- [ ] **Logout Functionality:** Logout clears session completely
- [ ] **OAuth Flow:** State parameter used and validated
- [ ] **OAuth Cookies:** State cookie ≠ auth cookie (different names)
- [ ] **Redirect Validation:** OAuth redirect_uri validated

### Template Security Review

- [ ] **Auto-Escaping:** Templates use auto-escaping by default
- [ ] **Safe Filter:** All `| safe` usages justified in comments
- [ ] **URL Generation:** URLs built with url_for() or direct paths (not string concat)
- [ ] **User Content:** User-generated content always escaped
- [ ] **JavaScript Embedding:** No user data embedded in <script> tags without escaping
- [ ] **Link Targets:** External links have `rel="noopener noreferrer"`

### API Security Review

- [ ] **Input Validation:** All inputs validated with Pydantic models
- [ ] **Output Encoding:** Responses properly encoded (JSON/XML/etc)
- [ ] **Error Messages:** Errors don't leak sensitive info (stack traces, paths)
- [ ] **Rate Limiting:** API endpoints rate-limited
- [ ] **CORS:** CORS configured restrictively (not `*` in production)
- [ ] **API Keys:** API keys rotatable and stored securely

### Database Security Review

- [ ] **Parameterized Queries:** All queries use SQLAlchemy ORM or parameters
- [ ] **Mass Assignment:** Only allowed fields updatable (no .update(**request.json))
- [ ] **Sensitive Data:** Passwords/secrets never logged
- [ ] **Migration Safety:** Migrations don't drop columns with data
- [ ] **Backup Encryption:** Backups encrypted at rest

### Dependency Security Review

- [ ] **Version Pinning:** requirements.txt has exact versions
- [ ] **Known Vulnerabilities:** Run `pip-audit` to check for CVEs
- [ ] **Minimal Dependencies:** Only necessary packages included
- [ ] **Dependency Sources:** All from PyPI (not git repos)

---

## Penetration Testing Checklist

Manual security testing procedures to run before production deployment.

### Authentication Testing

1. **Password Attacks**
   - [ ] Try weak passwords (should be rejected)
   - [ ] Try common passwords (should be rejected)
   - [ ] Try SQL injection in password field (`' OR '1'='1`)
   - [ ] Verify account lockout after N failed attempts

2. **Session Testing**
   - [ ] Verify session expires after timeout
   - [ ] Try reusing old session token (should fail)
   - [ ] Try accessing protected page without login (should redirect)
   - [ ] Verify logout invalidates session completely

3. **OAuth Testing**
   - [ ] Try CSRF attack on OAuth flow (manipulate state parameter)
   - [ ] Try replay attack (reuse authorization code)
   - [ ] Verify redirect_uri validation (can't redirect to attacker site)

### Injection Testing

1. **SQL Injection**
   - [ ] Try `' OR '1'='1` in all input fields
   - [ ] Try `'; DROP TABLE users; --` in text inputs
   - [ ] Try UNION-based injection: `' UNION SELECT * FROM users --`
   - [ ] Verify error messages don't expose database structure

2. **XSS Testing**
   - [ ] Try `<script>alert('XSS')</script>` in all inputs
   - [ ] Try event handlers: `<img src=x onerror=alert('XSS')>`
   - [ ] Try in URL parameters: `?name=<script>alert('XSS')</script>`
   - [ ] Verify output is escaped in all contexts

3. **Command Injection**
   - [ ] Try `; ls -la` in file upload filenames
   - [ ] Try `| whoami` in any shell-executed fields
   - [ ] Verify no user input passed to os.system() or subprocess.shell=True

### Access Control Testing

1. **Horizontal Privilege Escalation**
   - [ ] Try accessing another user's resources (change ID in URL)
   - [ ] Try accessing another org's data (if multi-tenant)
   - [ ] Verify all queries filter by current user/org

2. **Vertical Privilege Escalation**
   - [ ] Try accessing admin pages as regular user
   - [ ] Try admin API endpoints as regular user
   - [ ] Verify role checks on all privileged operations

3. **IDOR Testing**
   - [ ] Change IDs in URLs to access other records
   - [ ] Change IDs in POST bodies
   - [ ] Verify ownership checks before data access

### File Upload Testing

1. **Malicious Files**
   - [ ] Try uploading .php, .exe, .sh files (should be rejected)
   - [ ] Try double extension: `file.jpg.php` (should be rejected)
   - [ ] Try null byte: `file.php%00.jpg` (should be rejected)
   - [ ] Try ZIP bomb (huge decompressed size)

2. **Path Traversal**
   - [ ] Try filename: `../../etc/passwd` (should be sanitized)
   - [ ] Try filename with backslashes: `..\..\..\windows\system32`
   - [ ] Verify files saved with UUID names, not user-provided

### Network Security Testing

1. **HTTPS Testing**
   - [ ] Verify HTTP redirects to HTTPS
   - [ ] Verify HTTPS uses TLS 1.2+ (not SSLv3, TLS 1.0)
   - [ ] Verify strong cipher suites (no RC4, DES)
   - [ ] Check certificate validity and chain

2. **Header Testing**
   - [ ] Verify `Strict-Transport-Security` header present
   - [ ] Verify `X-Content-Type-Options: nosniff` present
   - [ ] Verify `X-Frame-Options: DENY` or `SAMEORIGIN`
   - [ ] Verify `Content-Security-Policy` configured

3. **Cookie Testing**
   - [ ] Verify cookies have `Secure` flag (HTTPS only)
   - [ ] Verify cookies have `HttpOnly` flag (no JavaScript access)
   - [ ] Verify cookies have `SameSite` flag (CSRF protection)

---

## Automated Security Tools

### Static Analysis

```bash
# Bandit - Python security linter
pip install bandit
bandit -r app/ -f html -o security-report.html

# Expected: No HIGH severity issues
# Review MEDIUM issues case-by-case
```

### Dependency Scanning

```bash
# pip-audit - Check for known vulnerabilities
pip install pip-audit
pip-audit --desc

# Expected: 0 vulnerabilities
# Update vulnerable packages immediately
```

### Secret Scanning

```bash
# git-secrets - Prevent committing secrets
git secrets --scan

# truffleHog - Find secrets in git history
pip install truffleHog
truffleHog --regex --entropy=True .
```

---

## Incident Response Checklist

If a security issue is discovered in production:

### Immediate Actions (Within 1 Hour)

- [ ] **Assess Severity:** Critical/High/Medium/Low
- [ ] **Contain Breach:** Block attacker IPs, disable affected features
- [ ] **Preserve Evidence:** Copy logs, database snapshots
- [ ] **Notify Team:** Alert all developers and stakeholders

### Investigation (Within 24 Hours)

- [ ] **Identify Attack Vector:** How was the vulnerability exploited?
- [ ] **Assess Impact:** What data was accessed/modified/deleted?
- [ ] **Check for Persistence:** Backdoors, additional vulnerabilities?
- [ ] **Review Logs:** Full timeline of attacker actions

### Remediation (Within 48 Hours)

- [ ] **Patch Vulnerability:** Fix the root cause
- [ ] **Deploy Fix:** Roll out patched version
- [ ] **Reset Credentials:** Rotate all affected secrets/keys
- [ ] **Verify Fix:** Re-test to confirm vulnerability closed

### Post-Incident (Within 1 Week)

- [ ] **User Notification:** Inform affected users (if data breach)
- [ ] **Root Cause Analysis:** Document why it happened
- [ ] **Prevention Measures:** Update checklists, add tests
- [ ] **Security Training:** Team review of lessons learned

---

*End of Security Checklists Reference*
