from sqlalchemy.orm import Session

from backend.database.db import SessionLocal
from backend.database.models import (
    User,
    Role,
    Permission
)

from backend.authentication.auth import hash_password


def seed_database():

    db: Session = SessionLocal()

    try:

        # -------------------------
        # Roles
        # -------------------------

        admin_role = db.query(Role).filter(
            Role.name == "Admin"
        ).first()

        if not admin_role:

            admin_role = Role(
                name="Admin",
                description="System Administrator"
            )

            db.add(admin_role)

        user_role = db.query(Role).filter(
            Role.name == "User"
        ).first()

        if not user_role:

            user_role = Role(
                name="User",
                description="Normal User"
            )

            db.add(user_role)

        db.commit()

        # -------------------------
        # Permissions
        # -------------------------

        permissions = [
            "chat",
            "documents",
            "upload",
            "delete_document",
            "approve_document",
            "retrieve",
            "admin",
            "workflow",
            "agents",
            "monitoring"
        ]

        permission_objects = []

        for permission in permissions:

            p = db.query(Permission).filter(
                Permission.name == permission
            ).first()

            if not p:

                p = Permission(
                    name=permission,
                    description=permission
                )

                db.add(p)

            permission_objects.append(p)

        db.commit()

        admin_role.permissions = permission_objects

        db.commit()

        # -------------------------
        # Admin User
        # -------------------------

        admin = db.query(User).filter(
            User.email == "admin@example.com"
        ).first()

        if not admin:

            admin = User(

                first_name="System",

                last_name="Administrator",

                username="admin",

                email="admin@example.com",

                password_hash=hash_password(
                    "admin123"
                ),

                department="Administration",

                designation="Administrator",

                phone="9999999999",

                is_active=True,

                is_verified=True

            )

            admin.roles.append(admin_role)

            db.add(admin)

            db.commit()

            print("Admin user created")

        else:

            print("Admin already exists")

    finally:

        db.close()


if __name__ == "__main__":

    seed_database()