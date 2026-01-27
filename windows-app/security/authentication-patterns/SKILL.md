---
name: authentication-patterns
description: >
  OAuth-first authentication patterns for staff applications. Covers Google/Microsoft
  OAuth setup, cookie separation, first-user admin pattern, and domain restriction.
  Use when: implementing login, OAuth, authentication, or user provisioning.
---

# Authentication Patterns

**Purpose:** OAuth-first authentication for staff applications  
**Size:** ~4 KB

---

## ⚡ LOAD THIS SKILL WHEN

- "OAuth", "Google login", "Microsoft login"
- "authentication", "login page", "sign in"
- "user provisioning", "first user"
- "domain restriction", "allowed domain"

---

## OAuth-Only Authentication (Preferred)

Local username/password is **deprecated** for staff applications.

### Benefits

| OAuth | Local Auth |
|-------|------------|
| No password storage | Must secure passwords |
| Enterprise identity | Separate credentials |
| Auto provisioning | Manual user creation |
| Domain restriction | Custom validation |

### When Local Auth is Acceptable

- Development/testing without OAuth configured
- No internet access
- Standalone tools without enterprise integration

Even then, OAuth should be primary; local auth as fallback only.

---

## Implementation Patterns

### Login Page: OAuth Only

```html
<!-- NO password form for OAuth-only apps -->
<div class="login-container">
    <h1>Sign In</h1>
    <a href="{{ url_for('oauth.google_login') }}" class="oauth-btn">
        <img src="/static/img/google-logo.svg" alt="Google">
        Sign in with Google
    </a>
</div>
<!-- NO "or sign in with email" divider -->
```

### First User = Admin

```python
from app.models import User, UserRole

user = User(
    email=email,
    name=name,
    role=UserRole.ADMIN if db.query(User).count() == 0 else UserRole.VIEWER,
    auth_provider="google",
    is_active=True
)
```

### Domain Restriction

```python
GOOGLE_ALLOWED_DOMAIN = os.getenv("GOOGLE_ALLOWED_DOMAIN", "")

if GOOGLE_ALLOWED_DOMAIN:
    email_domain = email.split("@")[1]
    if email_domain != GOOGLE_ALLOWED_DOMAIN:
        raise HTTPException(403, f"Only @{GOOGLE_ALLOWED_DOMAIN} accounts allowed")
```

---

## ⚠️ CRITICAL: Cookie Separation

OAuth state and auth session **MUST** use different cookies.

### Wrong (Causes Login Loops)

```python
# Same cookie for both - BREAKS LOGIN
app.add_middleware(
    SessionMiddleware,
    session_cookie=settings.SESSION_COOKIE_NAME,  # Conflicts!
)
```

### Correct

```python
# Separate cookies
AUTH_SESSION_COOKIE = f"{APP_NAME}_session"      # For auth
OAUTH_STATE_COOKIE = f"{APP_NAME}_oauth_state"   # For OAuth state

app.add_middleware(
    SessionMiddleware,
    session_cookie=OAUTH_STATE_COOKIE,  # OAuth state only
)
```

### Symptom of Cookie Conflict

Login appears successful → immediately redirects back to login page.

---

## Google OAuth Setup

### Environment Variables

```env
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-secret
GOOGLE_ALLOWED_DOMAIN=ucc-austin.org
BASE_URL=https://pms.ucc-austin.org
```

### Redirect URI Configuration

In Google Cloud Console → Credentials → OAuth 2.0 Client:

```
Authorized redirect URIs:
https://pms.ucc-austin.org/oauth/google/callback
http://localhost:8008/oauth/google/callback  (for testing)
```

### Private IP Rejection

Google OAuth **blocks** redirects to private IPs (192.168.x.x, 10.x.x.x).

| Scenario | Solution |
|----------|----------|
| Local dev | Use `localhost` not `192.168.x.x` |
| Production | Use public domain with Caddy |
| Internal access | Add hosts file entry (requires admin) |

**Hosts file modification requires Administrator privileges.** See `windows-app-build` skill for auto-elevation pattern.

---

## Regression Tests

```python
def test_oauth_cookie_separated():
    """OAuth state and auth session must use different cookies."""
    main_py = Path('app/main.py').read_text()
    if 'SessionMiddleware' in main_py:
        assert 'session_cookie=settings.SESSION_COOKIE_NAME' not in main_py, \
            "OAuth state cookie must be separate from auth session cookie"

def test_login_template_oauth_only():
    """Login page should not have password form for OAuth-only apps."""
    login_html = Path('app/templates/public/login.html').read_text()
    if 'google_oauth_enabled' in login_html:
        has_password = 'type="password"' in login_html
        has_divider = 'or sign in with' in login_html.lower()
        if not has_password:
            assert not has_divider, "Remove divider for OAuth-only"

def test_first_user_admin_pattern():
    """First OAuth user should become admin."""
    oauth_routes = Path('app/routes/oauth_routes.py').read_text()
    assert 'count() == 0' in oauth_routes or 'first user' in oauth_routes.lower(), \
        "OAuth should assign ADMIN to first user"
```

---

## Checklist

### OAuth Implementation

- [ ] Login page has OAuth button only (no password form)
- [ ] No "or sign in with" divider for OAuth-only
- [ ] OAuth state cookie differs from auth session cookie
- [ ] First user gets ADMIN role automatically
- [ ] GOOGLE_ALLOWED_DOMAIN is set (not empty)
- [ ] Redirect URI registered in Google Console

### Testing

- [ ] Login → callback → dashboard works
- [ ] Domain restriction rejects other domains
- [ ] First user is admin, second user is viewer
- [ ] Logout clears session properly

---

*End of Authentication Patterns Skill*
