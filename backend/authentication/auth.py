import datetime
import bcrypt
import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from backend.database.db import get_db
from backend.database.models import User
from backend.settings.config import settings

security = HTTPBearer()

ALGORITHM = "HS256"


# ============================================================
# Password Hashing
# ============================================================

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(
        password.encode("utf-8"),
        salt
    ).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except Exception:
        return False


# ============================================================
# Access Token
# ============================================================

def create_access_token(
    data: dict,
    expires_delta: datetime.timedelta = None
):

    payload = data.copy()

    expire = (
        datetime.datetime.utcnow()
        + (
            expires_delta
            if expires_delta
            else datetime.timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        )
    )

    payload.update({"exp": expire})

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=ALGORITHM
    )


# ============================================================
# Refresh Token
# ============================================================

def create_refresh_token(
    data: dict,
    expires_delta: datetime.timedelta = None
):

    payload = data.copy()

    expire = (
        datetime.datetime.utcnow()
        + (
            expires_delta
            if expires_delta
            else datetime.timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS
            )
        )
    )

    payload.update({"exp": expire})

    return jwt.encode(
        payload,
        settings.JWT_REFRESH_SECRET_KEY,
        algorithm=ALGORITHM
    )


# ============================================================
# Decode Tokens
# ============================================================

def decode_access_token(token: str):

    try:

        return jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[ALGORITHM]
        )

    except jwt.ExpiredSignatureError:

        raise HTTPException(
            status_code=401,
            detail="Access token expired"
        )

    except jwt.InvalidTokenError:

        raise HTTPException(
            status_code=401,
            detail="Invalid access token"
        )


def decode_refresh_token(token: str):

    try:

        return jwt.decode(
            token,
            settings.JWT_REFRESH_SECRET_KEY,
            algorithms=[ALGORITHM]
        )

    except jwt.ExpiredSignatureError:

        raise HTTPException(
            status_code=401,
            detail="Refresh token expired"
        )

    except jwt.InvalidTokenError:

        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )


# ============================================================
# Current User
# ============================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    payload = decode_access_token(token)

    email = payload.get("sub")

    if email is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    if not user.is_active:

        raise HTTPException(
            status_code=403,
            detail="Inactive user"
        )

    return user


# ============================================================
# Role Checking
# ============================================================

def require_role(role_name: str):

    def checker(
        current_user: User = Depends(get_current_user)
    ):

        roles = [
            role.name
            for role in current_user.roles
        ]

        if role_name not in roles:

            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        return current_user

    return checker


# ============================================================
# Permission Checking
# ============================================================

def require_permission(permission_name: str):

    def checker(
        current_user: User = Depends(get_current_user)
    ):

        permissions = []

        for role in current_user.roles:

            for permission in role.permissions:

                permissions.append(permission.name)

        if permission_name not in permissions:

            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )

        return current_user

    return checker