"""Repository for user data access (database-backed)."""

from sqlalchemy.orm import Session

from supportgenie.db.models import User
from supportgenie.auth.passwords import hash_password, verify_password


def create_user(session: Session, username, password, role="user"):
    existing = session.query(User).filter(User.username == username).first()
    if existing is not None:
        return False

    user = User(
        username=username,
        password_hash=hash_password(password),
        role=role,
    )
    session.add(user)
    session.commit()
    return True


def authenticate_user(session: Session, username, password):
    user = session.query(User).filter(User.username == username).first()
    if user is None:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return {"username": user.username, "role": user.role}