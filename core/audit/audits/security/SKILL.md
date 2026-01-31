---
name: security
description: >
  Comprehensive security audit checking for vulnerabilities: XSS, SQL injection, CSRF,
  insecure authentication, secrets exposure, and more. Use when: pre-release security
  validation, part of technical methodology, or security-focused review.
---

# Security Audit

**Purpose:** Comprehensive security vulnerability detection
**Size:** ~14 KB
**Type:** Audit Type (Part of Technical Methodology)

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Security audit"
- "Check for vulnerabilities"
- "Scan for security issues"
- "Validate security patterns"

**Context Indicators:**
- Pre-release security review
- Part of convergence (technical methodology)
- Security-focused code review
- Compliance validation

---

## Security Checks

### 1. SQL Injection

**Pattern:** Unparameterized SQL queries

**Vulnerable:**
```javascript
// ✗ Direct string concatenation
db.query(`SELECT * FROM users WHERE id = ${userId}`);

// ✗ Template literals with variables
db.query(`SELECT * FROM users WHERE email = '${email}'`);
```

**Secure:**
```javascript
// ✓ Parameterized queries
db.query('SELECT * FROM users WHERE id = ?', [userId]);

// ✓ Named parameters
db.query('SELECT * FROM users WHERE email = :email', { email });
```

**Detection:**
```javascript
const sqlInjectionPatterns = [
  /db\.query\s*\(`[^`]*\$\{/g,  // Template literals with ${var}
  /db\.query\s*\(".*"\s*\+/g,    // String concatenation
  /\.execute\s*\(`SELECT.*\$\{/g // Execute with template literals
];
```

### 2. Cross-Site Scripting (XSS)

**Pattern:** Unescaped output to HTML

**Vulnerable:**
```javascript
// ✗ Direct insertion
element.innerHTML = userInput;

// ✗ Unescaped template output
res.send(`<h1>${userInput}</h1>`);
```

**Secure:**
```javascript
// ✓ Escaped output
element.textContent = userInput;

// ✓ Using escape function
res.send(`<h1>${escapeHtml(userInput)}</h1>`);
```

**Detection:**
```javascript
const xssPatterns = [
  /\.innerHTML\s*=\s*[^escapeHtml]/g,
  /res\.send\(`.*\$\{(?!escapeHtml)/g,
  /document\.write\(/g
];
```

### 3. CSRF Protection

**Pattern:** State-changing operations without CSRF tokens

**Vulnerable:**
```javascript
// ✗ No CSRF check on POST
app.post('/api/delete', (req, res) => {
  deleteUser(req.body.userId);
});
```

**Secure:**
```javascript
// ✓ CSRF token validation
app.post('/api/delete', csrfProtection, (req, res) => {
  deleteUser(req.body.userId);
});

// ✓ Manual validation
app.post('/api/delete', (req, res) => {
  if (!validateCSRFToken(req.body.csrf_token)) {
    return res.status(403).send('Invalid CSRF token');
  }
  deleteUser(req.body.userId);
});
```

**Detection:**
```javascript
const csrfIssues = [];

// Check POST/PUT/DELETE routes
routes.filter(r => ['POST', 'PUT', 'DELETE'].includes(r.method))
  .forEach(route => {
    if (!route.middleware.includes('csrfProtection') &&
        !route.code.includes('validateCSRF')) {
      csrfIssues.push({
        route: route.path,
        method: route.method,
        severity: 'critical'
      });
    }
  });
```

### 4. Authentication Issues

**Pattern:** Insecure authentication implementation

**Common Issues:**
- Plaintext passwords
- Weak session management
- Missing rate limiting
- No account lockout

**Vulnerable:**
```javascript
// ✗ Plaintext password comparison
if (user.password === inputPassword) {
  login(user);
}

// ✗ Predictable session IDs
const sessionId = Date.now().toString();
```

**Secure:**
```javascript
// ✓ Hashed password comparison
if (await bcrypt.compare(inputPassword, user.passwordHash)) {
  login(user);
}

// ✓ Cryptographically secure session IDs
const sessionId = crypto.randomBytes(32).toString('hex');
```

**Detection:**
```javascript
const authIssues = [
  // Plain password comparisons
  /\.password\s*===\s*/g,
  // Date.now() for IDs
  /Date\.now\(\)\.toString\(\)/g,
  // Missing bcrypt
  /password.*===.*input/gi
];
```

### 5. Secrets Exposure

**Pattern:** Hardcoded secrets or secrets in logs

**Vulnerable:**
```javascript
// ✗ Hardcoded API key
const API_KEY = 'sk_live_abc123...';

// ✗ Logging sensitive data
console.log('User password:', password);

// ✗ Secrets in error messages
res.status(500).send(`DB connection failed: ${dbPassword}`);
```

**Secure:**
```javascript
// ✓ Environment variables
const API_KEY = process.env.API_KEY;

// ✓ Redacted logging
console.log('User authenticated:', userId);

// ✓ Generic error messages
res.status(500).send('Database connection error');
```

**Detection:**
```javascript
const secretPatterns = [
  /['"]sk_live_[a-zA-Z0-9]{20,}['"]/g,  // API keys
  /['"]ghp_[a-zA-Z0-9]{36}['"]/g,       // GitHub tokens
  /password\s*=\s*['"][^'"]+['"]/gi,    // Hardcoded passwords
  /console\.log.*password/gi             // Password logging
];
```

### 6. Insecure HTTP

**Pattern:** Using HTTP instead of HTTPS

**Vulnerable:**
```javascript
// ✗ HTTP only
app.listen(3000);

// ✗ No HTTPS redirect
app.get('/', (req, res) => {
  res.send('Hello');
});
```

**Secure:**
```javascript
// ✓ HTTPS enforcement
app.use((req, res, next) => {
  if (!req.secure && req.get('x-forwarded-proto') !== 'https') {
    return res.redirect('https://' + req.get('host') + req.url);
  }
  next();
});

// ✓ HSTS header
app.use(helmet.hsts({
  maxAge: 31536000,
  includeSubDomains: true
}));
```

### 7. Rate Limiting

**Pattern:** Missing rate limiting on sensitive endpoints

**Vulnerable:**
```javascript
// ✗ No rate limit on login
app.post('/api/login', async (req, res) => {
  const user = await authenticate(req.body);
  res.json({ token: user.token });
});
```

**Secure:**
```javascript
// ✓ Rate limiting
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5 // 5 attempts
});

app.post('/api/login', loginLimiter, async (req, res) => {
  const user = await authenticate(req.body);
  res.json({ token: user.token });
});
```

### 8. File Upload Validation

**Pattern:** Unrestricted file uploads

**Vulnerable:**
```javascript
// ✗ No validation
app.post('/upload', upload.single('file'), (req, res) => {
  saveFile(req.file);
});
```

**Secure:**
```javascript
// ✓ File type validation
const fileFilter = (req, file, cb) => {
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
  if (!allowedTypes.includes(file.mimetype)) {
    return cb(new Error('Invalid file type'));
  }
  cb(null, true);
};

app.post('/upload', upload.single('file', { fileFilter }), (req, res) => {
  saveFile(req.file);
});
```

---

## Configuration

### corpus-config.json

```json
{
  "audit": {
    "convergence": {
      "methodologies": [
        {
          "name": "technical",
          "audits": [
            {
              "id": "security",
              "config": {
                "checks": [
                  "xss",
                  "csrf",
                  "sql_injection",
                  "authentication",
                  "secrets_exposure",
                  "https_enforcement",
                  "rate_limiting",
                  "file_uploads"
                ],
                "exclude_patterns": ["test/**", "*.test.js"],
                "severity_levels": {
                  "sql_injection": "critical",
                  "xss": "critical",
                  "csrf": "high",
                  "secrets_exposure": "critical",
                  "rate_limiting": "medium"
                }
              }
            }
          ]
        }
      ]
    }
  }
}
```

---

## Auto-Fix Capabilities

### ✓ Fully Automatic

**SQL Injection:**
```
Issue: db.query(`SELECT * FROM users WHERE id = ${userId}`)
Fix: db.query('SELECT * FROM users WHERE id = ?', [userId])
Strategy: Convert template literals to parameterized queries
```

**XSS:**
```
Issue: element.innerHTML = userInput
Fix: element.textContent = userInput
Strategy: Replace innerHTML with textContent
```

### ⚠ User Approval Required

**CSRF Protection:**
```
Issue: POST route without CSRF protection
Fix: Add csrfProtection middleware
Strategy: Insert middleware, may require setup
```

**Rate Limiting:**
```
Issue: Login endpoint without rate limiting
Fix: Add rate limiting middleware
Strategy: Configure limits, requires decision on thresholds
```

### ✗ Manual Only

**Authentication Issues:**
```
Issue: Weak authentication implementation
Fix: Requires architectural changes
Strategy: Report issue, provide guidance
```

---

## Output Format

```json
{
  "audit_type": "security",
  "timestamp": "2026-01-31T10:00:00Z",
  "project_path": "/path/to/project",
  "summary": {
    "files_scanned": 147,
    "vulnerabilities_found": 23,
    "critical": 5,
    "high": 8,
    "medium": 7,
    "low": 3
  },
  "vulnerabilities": [
    {
      "severity": "critical",
      "category": "sql_injection",
      "location": "src/api/users.js:42",
      "code_snippet": "db.query(`SELECT * FROM users WHERE id = ${userId}`)",
      "message": "SQL injection vulnerability - use parameterized queries",
      "auto_fixable": true,
      "suggested_fix": "db.query('SELECT * FROM users WHERE id = ?', [userId])",
      "cwe": "CWE-89",
      "owasp": "A03:2021 – Injection"
    }
  ]
}
```

---

## Integration with Technical Methodology

Security audit is part of the **technical methodology** in 3-3-1 convergence:

```json
{
  "methodologies": [
    {
      "name": "technical",
      "description": "How it works",
      "audits": [
        "security",      // ← This audit
        "quality",
        "performance",
        "consistency"
      ]
    }
  ]
}
```

**Technical Perspective:**
- Are there exploitable vulnerabilities?
- Is authentication secure?
- Are secrets properly protected?
- Is HTTPS enforced?

---

## Quick Reference

**Run security audit:**
```javascript
const issues = await runAudit('security', projectConfig);
```

**Check specific vulnerability:**
```javascript
const sqlIssues = await checkSQLInjection(projectPath);
```

**Generate security report:**
```javascript
const report = await generateSecurityReport(projectPath);
console.log(`Vulnerabilities: ${report.summary.vulnerabilities_found}`);
console.log(`Critical: ${report.summary.critical}`);
```

---

*End of Security Audit*
*Part of v4.0.0 Universal Skills Ecosystem*
*Methodology: Technical (How it works)*
*OWASP Top 10 & CWE Coverage*
