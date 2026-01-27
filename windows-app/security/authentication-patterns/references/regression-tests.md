# Authentication Regression Tests

Test patterns to prevent re-occurrence of previously fixed authentication bugs.

---

## Cookie Separation Tests

### Test 1: OAuth State Cookie ≠ Session Cookie

**Bug History:** OAuth state cookie and session cookie had same name, causing login loops.

**Test:**
```python
# tests/test_auth_regressions.py
def test_oauth_state_and_session_cookies_different(settings):
    """Regression: OAuth state cookie must have different name from session cookie.

    Fixed in build 26015-1430
    Root cause: Both cookies named "session", causing collision
    """
    assert settings.OAUTH_STATE_COOKIE_NAME != settings.SESSION_COOKIE_NAME

    # Verify default values are different
    assert "oauth" in settings.OAUTH_STATE_COOKIE_NAME.lower()
    assert settings.SESSION_COOKIE_NAME != "oauth_state"
```

### Test 2: State Cookie Deleted After Login

**Bug History:** OAuth state cookie persisted after successful login.

**Test:**
```python
def test_state_cookie_deleted_after_callback(client, monkeypatch):
    """Regression: OAuth state cookie should be deleted after successful callback.

    Fixed in build 26016-0945
    Root cause: Forgot to call response.delete_cookie()
    """
    # Mock OAuth userinfo response
    async def mock_userinfo(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self):
                return {
                    "email": "test@example.com",
                    "name": "Test User",
                    "picture": "https://example.com/photo.jpg"
                }
        return MockResponse()

    # Initiate OAuth flow to get state cookie
    login_response = client.get("/login", follow_redirects=False)
    state = login_response.cookies.get("oauth_state")

    # Mock OAuth callback
    monkeypatch.setattr("httpx.AsyncClient.post", mock_oauth_token)
    monkeypatch.setattr("httpx.AsyncClient.get", mock_userinfo)

    callback_response = client.get(
        f"/auth/callback?code=test&state={state}",
        cookies={"oauth_state": state},
        follow_redirects=False
    )

    # Verify state cookie deleted
    assert "oauth_state" not in callback_response.cookies
    # Session cookie should be set
    assert "session" in callback_response.cookies
```

---

## First-User Admin Tests

### Test 1: First User Gets ADMIN Role

**Bug History:** First user wasn't automatically assigned ADMIN role.

**Test:**
```python
def test_first_user_becomes_admin(db_session, client, monkeypatch):
    """Regression: First user to register must become ADMIN.

    Fixed in build 26014-1615
    Root cause: Role assignment logic missing
    """
    # Ensure database is empty
    from app.models import User
    assert db_session.query(User).count() == 0

    # Mock OAuth userinfo
    async def mock_userinfo(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self):
                return {
                    "email": "first@example.com",
                    "name": "First User"
                }
        return MockResponse()

    monkeypatch.setattr("httpx.AsyncClient.get", mock_userinfo)

    # Complete OAuth flow
    # ... (login and callback steps)

    # Verify first user is ADMIN
    user = db_session.query(User).filter(User.email == "first@example.com").first()
    assert user is not None
    assert user.role == UserRole.ADMIN
```

### Test 2: Second User Gets USER Role

**Bug History:** All users were being assigned ADMIN role.

**Test:**
```python
def test_second_user_is_not_admin(db_session, client, monkeypatch):
    """Regression: Only first user should be ADMIN, subsequent users are USER.

    Fixed in build 26014-1620
    Root cause: Missing check for existing users
    """
    from app.models import User, UserRole

    # Create first user manually
    first_user = User(
        email="admin@example.com",
        name="Admin User",
        role=UserRole.ADMIN
    )
    db_session.add(first_user)
    db_session.commit()

    # Mock OAuth for second user
    async def mock_userinfo(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self):
                return {
                    "email": "second@example.com",
                    "name": "Second User"
                }
        return MockResponse()

    monkeypatch.setattr("httpx.AsyncClient.get", mock_userinfo)

    # Complete OAuth flow for second user
    # ...

    # Verify second user is USER, not ADMIN
    second_user = db_session.query(User).filter(User.email == "second@example.com").first()
    assert second_user is not None
    assert second_user.role == UserRole.USER
    assert second_user.role != UserRole.ADMIN
```

---

## Domain Restriction Tests

### Test 1: Allowed Domain Accepts Users

**Bug History:** Domain restriction rejected all users (including allowed domain).

**Test:**
```python
def test_allowed_domain_user_can_login(db_session, client, settings, monkeypatch):
    """Regression: Users from allowed domain should be accepted.

    Fixed in build 26015-1045
    Root cause: Domain check logic inverted
    """
    settings.GOOGLE_ALLOWED_DOMAIN = "example.com"

    # Mock OAuth userinfo with allowed domain
    async def mock_userinfo(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self):
                return {
                    "email": "user@example.com",  # Matches allowed domain
                    "name": "Allowed User"
                }
        return MockResponse()

    monkeypatch.setattr("httpx.AsyncClient.get", mock_userinfo)

    # Complete OAuth flow
    # ... (should succeed)

    # Verify user created
    from app.models import User
    user = db_session.query(User).filter(User.email == "user@example.com").first()
    assert user is not None
```

### Test 2: Non-Allowed Domain Rejected

**Bug History:** Domain restriction wasn't enforced.

**Test:**
```python
def test_non_allowed_domain_rejected(db_session, client, settings, monkeypatch):
    """Regression: Users from non-allowed domains should be rejected.

    Fixed in build 26015-1050
    Root cause: Domain check missing
    """
    settings.GOOGLE_ALLOWED_DOMAIN = "example.com"

    # Mock OAuth userinfo with different domain
    async def mock_userinfo(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self):
                return {
                    "email": "user@attacker.com",  # Different domain
                    "name": "Attacker"
                }
        return MockResponse()

    monkeypatch.setattr("httpx.AsyncClient.get", mock_userinfo)

    # Complete OAuth flow
    response = # ... (callback request)

    # Verify rejection
    assert response.status_code == 403
    assert "Only example.com accounts are allowed" in response.text

    # Verify user NOT created
    from app.models import User
    user = db_session.query(User).filter(User.email == "user@attacker.com").first()
    assert user is None
```

---

## State Validation Tests

### Test 1: Missing State Rejected

**Bug History:** Callback accepted requests without state parameter.

**Test:**
```python
def test_callback_rejects_missing_state(client):
    """Regression: Callback must reject requests without state parameter.

    Fixed in build 26016-1120
    Root cause: State validation skipped
    """
    response = client.get("/auth/callback?code=test_code")

    assert response.status_code == 400
    assert "Missing code or state" in response.text
```

### Test 2: Mismatched State Rejected

**Bug History:** State token validation wasn't comparing correctly.

**Test:**
```python
def test_callback_rejects_mismatched_state(client):
    """Regression: Callback must reject mismatched state tokens (CSRF protection).

    Fixed in build 26016-1125
    Root cause: State comparison used == instead of secrets.compare_digest
    """
    # Get valid state from login
    login_response = client.get("/login", follow_redirects=False)
    state_cookie = login_response.cookies.get("oauth_state")

    # Send callback with different state
    response = client.get(
        "/auth/callback?code=test&state=wrong_state",
        cookies={"oauth_state": state_cookie}
    )

    assert response.status_code == 400
    assert "Invalid state" in response.text
```

---

## Session Management Tests

### Test 1: Logout Clears Session

**Bug History:** Logout endpoint didn't delete session cookie.

**Test:**
```python
def test_logout_clears_session_cookie(client):
    """Regression: Logout must delete session cookie.

    Fixed in build 26017-0930
    Root cause: response.delete_cookie() not called
    """
    # Create session
    response = client.get(
        "/",
        cookies={"session": "test_session_token"}
    )

    # Logout
    logout_response = client.get("/logout", follow_redirects=False)

    # Verify session cookie deleted
    # (FastAPI sets max_age=0 to delete)
    session_cookie = logout_response.cookies.get("session")
    assert session_cookie == "" or "max-age=0" in str(logout_response.headers.get("set-cookie", ""))
```

### Test 2: Session Expires After Timeout

**Bug History:** Sessions never expired.

**Test:**
```python
import time

def test_session_expires_after_timeout(db_session, client):
    """Regression: Sessions should expire after configured timeout.

    Fixed in build 26017-1445
    Root cause: Session expiration not implemented
    """
    from app.models import Session
    from datetime import datetime, timedelta

    # Create session with old timestamp
    old_session = Session(
        token="old_token",
        user_id=1,
        created_at=datetime.utcnow() - timedelta(days=8)  # 8 days old
    )
    db_session.add(old_session)
    db_session.commit()

    # Try to use old session
    response = client.get("/profile", cookies={"session": "old_token"})

    # Should be redirected to login (session expired)
    assert response.status_code == 302
    assert "/login" in response.headers["location"]
```

---

## OAuth Provider Error Handling Tests

### Test 1: OAuth Error Parameter Handled

**Bug History:** OAuth errors from provider caused 500 errors.

**Test:**
```python
def test_callback_handles_oauth_error_parameter(client):
    """Regression: Callback must handle error parameter from OAuth provider.

    Fixed in build 26018-1015
    Root cause: error parameter not checked
    """
    response = client.get(
        "/auth/callback?error=access_denied&error_description=User+cancelled"
    )

    # Should return 400, not 500
    assert response.status_code == 400
    assert "access_denied" in response.text or "User cancelled" in response.text
```

### Test 2: Token Exchange Failure Handled

**Bug History:** Failed token exchange caused unhandled exceptions.

**Test:**
```python
def test_callback_handles_token_exchange_failure(client, monkeypatch):
    """Regression: Callback must handle failed token exchange gracefully.

    Fixed in build 26018-1030
    Root cause: No error handling for token endpoint failures
    """
    # Mock token endpoint failure
    async def mock_token_failure(*args, **kwargs):
        class MockResponse:
            status_code = 400
            text = "invalid_grant"
        return MockResponse()

    monkeypatch.setattr("httpx.AsyncClient.post", mock_token_failure)

    # Get valid state
    login_response = client.get("/login", follow_redirects=False)
    state = login_response.cookies.get("oauth_state")

    # Try callback
    response = client.get(
        f"/auth/callback?code=invalid_code&state={state}",
        cookies={"oauth_state": state}
    )

    # Should return 500 with clear message, not crash
    assert response.status_code == 500
    assert "Failed to obtain access token" in response.text
```

---

## HTTPS Cookie Security Tests

### Test 1: Secure Flag Set for HTTPS

**Bug History:** Cookies didn't have secure flag when using HTTPS.

**Test:**
```python
def test_cookies_have_secure_flag_for_https(settings, client, monkeypatch):
    """Regression: Cookies must have secure=True when BASE_URL is HTTPS.

    Fixed in build 26019-0845
    Root cause: secure flag hardcoded to False
    """
    settings.BASE_URL = "https://app.example.com"

    # Login and check cookie
    login_response = client.get("/login", follow_redirects=False)

    set_cookie_header = login_response.headers.get("set-cookie", "")
    assert "Secure" in set_cookie_header or "secure" in set_cookie_header
```

### Test 2: Secure Flag Not Set for HTTP

**Bug History:** Cookies had secure flag for HTTP, breaking local development.

**Test:**
```python
def test_cookies_no_secure_flag_for_http(settings, client):
    """Regression: Cookies should NOT have secure flag for HTTP (local dev).

    Fixed in build 26019-0850
    Root cause: secure flag always True
    """
    settings.BASE_URL = "http://localhost:8008"

    # Login and check cookie
    login_response = client.get("/login", follow_redirects=False)

    set_cookie_header = login_response.headers.get("set-cookie", "")
    # Secure flag should NOT be present
    assert "Secure" not in set_cookie_header
```

---

## Test Fixtures

### OAuth Mock Fixtures

```python
# tests/conftest.py
import pytest
from unittest.mock import AsyncMock

@pytest.fixture
def mock_google_oauth(monkeypatch):
    """Mock Google OAuth endpoints for testing."""

    async def mock_token_exchange(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self):
                return {"access_token": "mock_access_token"}
        return MockResponse()

    async def mock_userinfo(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self):
                return {
                    "email": "test@example.com",
                    "name": "Test User",
                    "picture": "https://example.com/photo.jpg"
                }
        return MockResponse()

    monkeypatch.setattr("httpx.AsyncClient.post", mock_token_exchange)
    monkeypatch.setattr("httpx.AsyncClient.get", mock_userinfo)

    return {"email": "test@example.com", "name": "Test User"}


@pytest.fixture
def authenticated_client(client, db_session):
    """Create client with valid session cookie."""
    from app.models import User, UserRole
    import secrets

    # Create user
    user = User(
        email="test@example.com",
        name="Test User",
        role=UserRole.USER
    )
    db_session.add(user)
    db_session.commit()

    # Create session
    session_token = secrets.token_urlsafe(32)

    # Return client with session cookie
    client.cookies.set("session", session_token)
    return client
```

---

*End of Authentication Regression Tests*
