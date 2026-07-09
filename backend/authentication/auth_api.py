from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from backend.database.db import get_db
from backend.database.models import User
from backend.authentication.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    get_current_user
)

router = APIRouter()

# ============================================================
# Request Models
# ============================================================

class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    department: str
    designation: str
    phone: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ============================================================
# Register
# ============================================================

@router.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):

    existing = db.query(User).filter(
        User.email == request.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    username = db.query(User).filter(
        User.username == request.username
    ).first()

    if username:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    user = User(
        first_name=request.first_name,
        last_name=request.last_name,
        username=request.username,
        email=request.email,
        password_hash=hash_password(request.password),
        department=request.department,
        designation=request.designation,
        phone=request.phone,
        is_active=True,
        is_verified=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "User registered successfully",
        "user_id": user.id
    }


# ============================================================
# Login
# ============================================================

@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == request.email
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        request.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {
            "sub": user.email
        }
    )

    refresh_token = create_refresh_token(
        {
            "sub": user.email
        }
    )

    return {

        "access_token": access_token,

        "refresh_token": refresh_token,

        "token_type": "bearer",

        "user": {

            "id": user.id,

            "email": user.email,

            "username": user.username,

            "first_name": user.first_name,

            "last_name": user.last_name,

            "department": user.department

        }

    }


# ============================================================
# Current User
# ============================================================

@router.get("/me")
def me(
    current_user: User = Depends(get_current_user)
):

    return {

        "id": current_user.id,

        "username": current_user.username,

        "email": current_user.email,

        "department": current_user.department,

        "designation": current_user.designation,

        "roles": [
            role.name
            for role in current_user.roles
        ]

    }


# ============================================================
# Refresh Token
# ============================================================

class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/refresh")
def refresh_token(
    request: RefreshRequest
):

    from backend.authentication.auth import (
        decode_refresh_token
    )

    payload = decode_refresh_token(
        request.refresh_token
    )

    access_token = create_access_token(
        {
            "sub": payload["sub"]
        }
    )

    return {

        "access_token": access_token,

        "token_type": "bearer"

    }


# ============================================================
# Logout
# ============================================================

@router.post("/logout")
def logout():

    return {

        "message": "Logout successful"

    }