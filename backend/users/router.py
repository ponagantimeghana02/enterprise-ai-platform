from typing import List, Optional
import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from backend.database.db import get_db, User, Role, Permission
from backend.authentication.auth import get_current_user, hash_password

router = APIRouter(tags=["Admin Dashboard"])

# Pydantic Schemas
class PermissionSchema(BaseModel):
    id: int
    permission_name: str
    module: str

    class Config:
        from_attributes = True

class RoleSchema(BaseModel):
    id: int
    name: str
    permissions: List[PermissionSchema] = []

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role_id: int
    role_name: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role_id: int

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role_id: Optional[int] = None

# Role Validation Dependency
def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role.name != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Admin role required."
        )
    return current_user

# --- Roles and Permissions Endpoints ---

@router.get("/roles", response_model=List[RoleSchema], dependencies=[Depends(require_admin)])
def get_roles(db: Session = Depends(get_db)):
    return db.query(Role).all()

@router.get("/permissions", response_model=List[PermissionSchema], dependencies=[Depends(require_admin)])
def get_permissions(db: Session = Depends(get_db)):
    return db.query(Permission).all()

# --- Users CRUD Endpoints ---

@router.get("/users", response_model=List[UserResponse], dependencies=[Depends(require_admin)])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    # Map users to output format containing role_name
    result = []
    for user in users:
        result.append(UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            role_id=user.role_id,
            role_name=user.role.name,
            created_at=user.created_at
        ))
    return result

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    print(db)
    # Check if email is already taken
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )
    
    # Check if role exists
    role = db.query(Role).filter(Role.id == user_in.role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role does not exist."
        )
        
    # Create new user
    new_user = User(
        name=user_in.name,
        email=user_in.email,
        password_hash=hash_password(user_in.password),
        role_id=user_in.role_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return UserResponse(
        id=new_user.id,
        name=new_user.name,
        email=new_user.email,
        role_id=new_user.role_id,
        role_name=role.name,
        created_at=new_user.created_at
    )

@router.put("/users/{id}", response_model=UserResponse, dependencies=[Depends(require_admin)])
def update_user(id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
    # Find user
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
        
    # Update fields if provided
    if user_in.name is not None:
        user.name = user_in.name
    if user_in.email is not None:
        # Check if email is taken by another user
        existing = db.query(User).filter(User.email == user_in.email, User.id != id).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use."
            )
        user.email = user_in.email
    if user_in.password is not None:
        user.password_hash = hash_password(user_in.password)
    if user_in.role_id is not None:
        role = db.query(Role).filter(Role.id == user_in.role_id).first()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role does not exist."
            )
        user.role_id = user_in.role_id
        
    db.commit()
    db.refresh(user)
    
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        role_id=user.role_id,
        role_name=user.role.name,
        created_at=user.created_at
    )

@router.delete("/users/{id}", status_code=status.HTTP_200_OK, dependencies=[Depends(require_admin)])
def delete_user(id: int, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    # Find user
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
        
    # Prevent deleting self
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own admin account."
        )
        
    # Delete user
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully."}
