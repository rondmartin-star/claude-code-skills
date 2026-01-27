# OAuth Implementation Examples

Complete OAuth implementation patterns for Google and Microsoft identity providers.

---

## Google OAuth 2.0 Implementation

### Configuration (settings.py)

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # OAuth Configuration
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_ALLOWED_DOMAIN: str = ""  # e.g., "example.com" for domain restriction

    # Session Configuration
    SECRET_KEY: str
    SESSION_COOKIE_NAME: str = "session"
    OAUTH_STATE_COOKIE_NAME: str = "oauth_state"  # CRITICAL: Different from session cookie

    # Base URL (for redirect_uri)
    BASE_URL: str  # e.g., "https://app.example.com" or "http://localhost:8008"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
```

### OAuth Routes (app/routes/auth.py)

```python
from fastapi import APIRouter, Request, HTTPException, Response
from fastapi.responses import RedirectResponse
import httpx
import secrets
from urllib.parse import urlencode

from app.config import settings
from app.database import get_db
from app.models import User, UserRole

router = APIRouter(tags=["auth"])

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

@router.get("/login")
def login(request: Request):
    """Initiate OAuth flow - redirect to Google."""
    # Generate random state token for CSRF protection
    state = secrets.token_urlsafe(32)

    # Build redirect_uri
    redirect_uri = f"{settings.BASE_URL}/auth/callback"

    # Google OAuth parameters
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "access_type": "offline",
        "prompt": "select_account"
    }

    # Build authorization URL
    auth_url = f"{GOOGLE_AUTH_URL}?{urlencode(params)}"

    # Store state in cookie (for validation in callback)
    response = RedirectResponse(auth_url)
    response.set_cookie(
        key=settings.OAUTH_STATE_COOKIE_NAME,  # Different from session cookie!
        value=state,
        max_age=600,  # 10 minutes
        httponly=True,
        secure=settings.BASE_URL.startswith("https://"),
        samesite="lax"
    )

    return response


@router.get("/auth/callback")
async def auth_callback(
    request: Request,
    response: Response,
    code: str = None,
    state: str = None,
    error: str = None
):
    """Handle OAuth callback from Google."""

    # Check for OAuth error
    if error:
        raise HTTPException(400, f"OAuth error: {error}")

    if not code or not state:
        raise HTTPException(400, "Missing code or state")

    # Validate state token (CSRF protection)
    stored_state = request.cookies.get(settings.OAUTH_STATE_COOKIE_NAME)
    if not stored_state or stored_state != state:
        raise HTTPException(400, "Invalid state token")

    # Exchange authorization code for access token
    redirect_uri = f"{settings.BASE_URL}/auth/callback"

    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            GOOGLE_TOKEN_URL,
            data={
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri
            }
        )

        if token_response.status_code != 200:
            raise HTTPException(500, "Failed to obtain access token")

        tokens = token_response.json()
        access_token = tokens.get("access_token")

        # Fetch user info
        userinfo_response = await client.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"}
        )

        if userinfo_response.status_code != 200:
            raise HTTPException(500, "Failed to fetch user info")

        userinfo = userinfo_response.json()

    # Extract user details
    email = userinfo.get("email")
    name = userinfo.get("name")
    picture = userinfo.get("picture")

    if not email:
        raise HTTPException(400, "Email not provided by OAuth provider")

    # Domain restriction
    if settings.GOOGLE_ALLOWED_DOMAIN:
        email_domain = email.split("@")[1]
        if email_domain != settings.GOOGLE_ALLOWED_DOMAIN:
            raise HTTPException(
                403,
                f"Only {settings.GOOGLE_ALLOWED_DOMAIN} accounts are allowed"
            )

    # Get or create user
    db = next(get_db())
    user = db.query(User).filter(User.email == email).first()

    if not user:
        # First user becomes ADMIN
        is_first_user = db.query(User).count() == 0
        role = UserRole.ADMIN if is_first_user else UserRole.USER

        user = User(
            email=email,
            name=name,
            picture=picture,
            role=role
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Create session token
    session_token = secrets.token_urlsafe(32)

    # Store session in database or cache
    # (Implementation depends on session storage strategy)

    # Set session cookie (DIFFERENT from OAuth state cookie)
    redirect_response = RedirectResponse("/", status_code=302)
    redirect_response.set_cookie(
        key=settings.SESSION_COOKIE_NAME,  # NOT oauth_state_cookie!
        value=session_token,
        max_age=86400 * 7,  # 7 days
        httponly=True,
        secure=settings.BASE_URL.startswith("https://"),
        samesite="lax"
    )

    # Delete OAuth state cookie (no longer needed)
    redirect_response.delete_cookie(settings.OAUTH_STATE_COOKIE_NAME)

    return redirect_response


@router.get("/logout")
def logout(response: Response):
    """Clear session and redirect to homepage."""
    redirect_response = RedirectResponse("/", status_code=302)

    # Delete session cookie
    redirect_response.delete_cookie(settings.SESSION_COOKIE_NAME)

    return redirect_response
```

---

## Microsoft OAuth (Azure AD) Implementation

### Configuration (settings.py)

```python
class Settings(BaseSettings):
    # Microsoft OAuth Configuration
    MICROSOFT_CLIENT_ID: str
    MICROSOFT_CLIENT_SECRET: str
    MICROSOFT_TENANT_ID: str = "common"  # or specific tenant ID

    # Allowed domain for organizational accounts
    MICROSOFT_ALLOWED_DOMAIN: str = ""

    # Session configuration (same as Google)
    SECRET_KEY: str
    SESSION_COOKIE_NAME: str = "session"
    OAUTH_STATE_COOKIE_NAME: str = "oauth_state"
    BASE_URL: str

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
```

### OAuth Routes (app/routes/auth_microsoft.py)

```python
from fastapi import APIRouter, Request, HTTPException, Response
from fastapi.responses import RedirectResponse
import httpx
import secrets
from urllib.parse import urlencode

from app.config import settings
from app.database import get_db
from app.models import User, UserRole

router = APIRouter(tags=["auth"])

MICROSOFT_AUTH_URL = f"https://login.microsoftonline.com/{settings.MICROSOFT_TENANT_ID}/oauth2/v2.0/authorize"
MICROSOFT_TOKEN_URL = f"https://login.microsoftonline.com/{settings.MICROSOFT_TENANT_ID}/oauth2/v2.0/token"
MICROSOFT_USERINFO_URL = "https://graph.microsoft.com/v1.0/me"

@router.get("/login/microsoft")
def login_microsoft(request: Request):
    """Initiate Microsoft OAuth flow."""
    state = secrets.token_urlsafe(32)
    redirect_uri = f"{settings.BASE_URL}/auth/microsoft/callback"

    params = {
        "client_id": settings.MICROSOFT_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile User.Read",
        "state": state,
        "response_mode": "query"
    }

    auth_url = f"{MICROSOFT_AUTH_URL}?{urlencode(params)}"

    response = RedirectResponse(auth_url)
    response.set_cookie(
        key=settings.OAUTH_STATE_COOKIE_NAME,
        value=state,
        max_age=600,
        httponly=True,
        secure=settings.BASE_URL.startswith("https://"),
        samesite="lax"
    )

    return response


@router.get("/auth/microsoft/callback")
async def microsoft_callback(
    request: Request,
    response: Response,
    code: str = None,
    state: str = None,
    error: str = None,
    error_description: str = None
):
    """Handle Microsoft OAuth callback."""

    if error:
        raise HTTPException(400, f"OAuth error: {error_description or error}")

    if not code or not state:
        raise HTTPException(400, "Missing code or state")

    # Validate state
    stored_state = request.cookies.get(settings.OAUTH_STATE_COOKIE_NAME)
    if not stored_state or stored_state != state:
        raise HTTPException(400, "Invalid state token")

    redirect_uri = f"{settings.BASE_URL}/auth/microsoft/callback"

    async with httpx.AsyncClient() as client:
        # Exchange code for token
        token_response = await client.post(
            MICROSOFT_TOKEN_URL,
            data={
                "client_id": settings.MICROSOFT_CLIENT_ID,
                "client_secret": settings.MICROSOFT_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri
            }
        )

        if token_response.status_code != 200:
            raise HTTPException(500, f"Token exchange failed: {token_response.text}")

        tokens = token_response.json()
        access_token = tokens.get("access_token")

        # Fetch user info from Microsoft Graph
        userinfo_response = await client.get(
            MICROSOFT_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"}
        )

        if userinfo_response.status_code != 200:
            raise HTTPException(500, "Failed to fetch user info")

        userinfo = userinfo_response.json()

    # Extract user details
    email = userinfo.get("mail") or userinfo.get("userPrincipalName")
    name = userinfo.get("displayName")

    if not email:
        raise HTTPException(400, "Email not provided by Microsoft")

    # Domain restriction
    if settings.MICROSOFT_ALLOWED_DOMAIN:
        email_domain = email.split("@")[1]
        if email_domain != settings.MICROSOFT_ALLOWED_DOMAIN:
            raise HTTPException(
                403,
                f"Only {settings.MICROSOFT_ALLOWED_DOMAIN} accounts are allowed"
            )

    # Get or create user (same pattern as Google)
    db = next(get_db())
    user = db.query(User).filter(User.email == email).first()

    if not user:
        is_first_user = db.query(User).count() == 0
        role = UserRole.ADMIN if is_first_user else UserRole.USER

        user = User(
            email=email,
            name=name,
            role=role
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Create session
    session_token = secrets.token_urlsafe(32)

    redirect_response = RedirectResponse("/", status_code=302)
    redirect_response.set_cookie(
        key=settings.SESSION_COOKIE_NAME,
        value=session_token,
        max_age=86400 * 7,
        httponly=True,
        secure=settings.BASE_URL.startswith("https://"),
        samesite="lax"
    )

    redirect_response.delete_cookie(settings.OAUTH_STATE_COOKIE_NAME)

    return redirect_response
```

---

## Common OAuth Pitfalls & Solutions

### Pitfall 1: Cookie Name Collision

**Problem:** Using same cookie name for OAuth state and session.

**Symptom:** Login redirects back to login page immediately.

**Solution:**
```python
# WRONG
OAUTH_STATE_COOKIE = "session"  # Collides!
SESSION_COOKIE = "session"

# RIGHT
OAUTH_STATE_COOKIE_NAME = "oauth_state"  # Different names
SESSION_COOKIE_NAME = "session"
```

### Pitfall 2: Private IP in redirect_uri

**Problem:** Using private IP (192.168.x.x) in OAuth redirect_uri.

**Symptom:** Google OAuth returns 400 error "redirect_uri_mismatch".

**Solution:**
```python
# WRONG
BASE_URL = "http://192.168.0.100:8008"

# RIGHT (for development)
BASE_URL = "http://localhost:8008"

# RIGHT (for production)
BASE_URL = "https://app.example.com"
```

### Pitfall 3: Missing State Validation

**Problem:** Not validating state token in callback.

**Symptom:** Vulnerable to CSRF attacks.

**Solution:**
```python
# WRONG - No validation
@router.get("/auth/callback")
def callback(code: str):
    # Exchange code for token...

# RIGHT - Validate state
@router.get("/auth/callback")
def callback(request: Request, code: str, state: str):
    stored_state = request.cookies.get(OAUTH_STATE_COOKIE_NAME)
    if not stored_state or stored_state != state:
        raise HTTPException(400, "Invalid state")
    # Exchange code for token...
```

### Pitfall 4: Not Deleting State Cookie

**Problem:** OAuth state cookie persists after login.

**Symptom:** Security risk, cookie clutter.

**Solution:**
```python
# After successful login:
redirect_response = RedirectResponse("/")
redirect_response.delete_cookie(OAUTH_STATE_COOKIE_NAME)  # Clean up
return redirect_response
```

---

## Testing OAuth Implementation

### Manual Testing Checklist

- [ ] **Initiate flow:** `/login` redirects to Google/Microsoft
- [ ] **Consent screen:** Shows correct app name and scopes
- [ ] **Successful callback:** User logged in, redirected to homepage
- [ ] **State validation:** Manipulating state parameter fails
- [ ] **Domain restriction:** Non-allowed domain email rejected
- [ ] **First user admin:** First user gets ADMIN role
- [ ] **Subsequent users:** Later users get USER role
- [ ] **Session cookie:** Set with correct flags (httponly, secure for HTTPS)
- [ ] **State cookie:** Deleted after callback
- [ ] **Logout:** Clears session, redirects to homepage

### Automated Testing (pytest)

```python
# tests/test_oauth.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_redirects_to_oauth_provider():
    """Login endpoint should redirect to OAuth provider."""
    response = client.get("/login", follow_redirects=False)

    assert response.status_code == 302
    assert "accounts.google.com" in response.headers["location"]
    assert "oauth_state" in response.cookies


def test_callback_validates_state():
    """Callback should reject mismatched state."""
    # Get state from login
    login_response = client.get("/login", follow_redirects=False)
    state_cookie = login_response.cookies.get("oauth_state")

    # Try callback with different state
    response = client.get(
        f"/auth/callback?code=test_code&state=wrong_state",
        cookies={"oauth_state": state_cookie}
    )

    assert response.status_code == 400
    assert "Invalid state" in response.text


def test_first_user_becomes_admin(db_session):
    """First user to register should get ADMIN role."""
    # Mock OAuth userinfo response
    # ... (requires mocking httpx)

    # Verify user created with ADMIN role
    from app.models import User, UserRole
    user = db_session.query(User).first()
    assert user.role == UserRole.ADMIN
```

---

*End of OAuth Implementation Examples*
