"""Temporary in-memory user store (replaced by PostgreSQL in Phase 8)."""

from supportgenie.auth.passwords import hash_password, verify_password

# username -> {"password_hash": ..., "role": ...}
# WARNING: in-memory only — all users are lost when the server restarts.
_users = {}


def create_user(username, password, role="user"):
    if username in _users:
        return False
    _users[username] = {
        "password_hash": hash_password(password),
        "role": role,
    }
    return True


def authenticate_user(username, password):
    user = _users.get(username)
    if user is None:
        return None
    if not verify_password(password, user["password_hash"]):
        return None
    return {"username": username, "role": user["role"]}