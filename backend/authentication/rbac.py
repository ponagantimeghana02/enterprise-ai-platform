from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.db import get_db
from backend.database.models import User
from backend.authentication.auth import get_current_user


# ==========================================================
# Role Verification
# ==========================================================

def require_role(role_name: str):

    def checker(
        current_user: User = Depends(get_current_user)
    ):

        roles = [role.name for role in current_user.roles]

        if role_name not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"'{role_name}' role required."
            )

        return current_user

    return checker


# ==========================================================
# Permission Verification
# ==========================================================

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
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"'{permission_name}' permission required."
            )

        return current_user

    return checker


# ==========================================================
# Admin Only
# ==========================================================

def admin_only(
    current_user: User = Depends(get_current_user)
):

    roles = [role.name for role in current_user.roles]

    if "Admin" not in roles:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required."
        )

    return current_user


# ==========================================================
# HR Only
# ==========================================================

def hr_only(
    current_user: User = Depends(get_current_user)
):

    if current_user.department != "HR":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="HR department access required."
        )

    return current_user


# ==========================================================
# IT Only
# ==========================================================

def it_only(
    current_user: User = Depends(get_current_user)
):

    if current_user.department != "IT":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="IT department access required."
        )

    return current_user


# ==========================================================
# Finance Only
# ==========================================================

def finance_only(
    current_user: User = Depends(get_current_user)
):

    if current_user.department != "Finance":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Finance department access required."
        )

    return current_user


# ==========================================================
# Active User Only
# ==========================================================

def active_user(
    current_user: User = Depends(get_current_user)
):

    if not current_user.is_active:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive account."
        )

    return current_user
# ==========================================================
# RBAC Checker Class
# ==========================================================

class RBACChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user=Depends(get_current_user)):
        user_roles = [role.name for role in current_user.roles]

        if not any(role in user_roles for role in self.allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )

        return current_user