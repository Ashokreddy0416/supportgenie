"""Signup and login API endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from fastapi import Depends
from sqlalchemy.orm import Session

from supportgenie.db.database import get_session
from supportgenie.db.users_repo import create_user, authenticate_user
from supportgenie.auth.tokens import create_token

router = APIRouter(prefix="/auth", tags=["auth"])


class SignupRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=100)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/signup")
def signup(request: SignupRequest, session: Session = Depends(get_session)):
    created = create_user(session, request.username, request.password)
    if not created:
        raise HTTPException(status_code=409, detail="Username already exists.")
    return {"message": "Account created successfully."}


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, session: Session = Depends(get_session)):
    user = authenticate_user(session, request.username, request.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    token = create_token(user["username"], user["role"])
    return TokenResponse(access_token=token)