import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from backend.database.db import get_db, User, RefreshToken
from backend.authentication.auth import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_refresh_token
)

router = APIRouter(tags=["Authentication"])

# Pydantic Request/Response models
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str

class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LogoutRequest(BaseModel):
    refresh_token: str

@router.post("/login", response_model=LoginResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    # Get user role and permission names
    permissions = [p.permission_name for p in user.role.permissions]
    
    # Create tokens
    access_token_data = {
        "sub": user.email,
        "role": user.role.name,
        "permissions": permissions
    }
    refresh_token_data = {
        "sub": user.email
    }
    
    access_token = create_access_token(data=access_token_data)
    refresh_token = create_refresh_token(data=refresh_token_data)
    
    # Save refresh token in database
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(days=7)
    db_refresh_token = RefreshToken(
        token=refresh_token,
        user_id=user.id,
        expires_at=expires_at
    )
    db.add(db_refresh_token)
    db.commit()
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/logout")
def logout(body: LogoutRequest, db: Session = Depends(get_db)):
    # Delete refresh token from DB
    db_token = db.query(RefreshToken).filter(RefreshToken.token == body.refresh_token).first()
    if db_token:
        db.delete(db_token)
        db.commit()
    return {"message": "Successfully logged out"}

@router.post("/refresh-token", response_model=RefreshResponse)
def refresh_token_route(body: RefreshRequest, db: Session = Depends(get_db)):
    # Decode and validate refresh token
    payload = decode_refresh_token(body.refresh_token)
    email: str = payload.get("sub")
    
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token payload"
        )
    
    # Check if token exists in DB
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == body.refresh_token,
        RefreshToken.expires_at > datetime.datetime.utcnow()
    ).first()
    
    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is invalid or expired"
        )
    
    # Fetch user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    # Create new access token
    permissions = [p.permission_name for p in user.role.permissions]
    access_token_data = {
        "sub": user.email,
        "role": user.role.name,
        "permissions": permissions
    }
    new_access_token = create_access_token(data=access_token_data)
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }
