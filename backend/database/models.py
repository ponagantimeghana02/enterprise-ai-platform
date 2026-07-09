from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    Table,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.database.db import Base

# =====================================================
# Many-to-Many Association Tables
# =====================================================

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE")),
)

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE")),
    Column("permission_id", Integer, ForeignKey("permissions.id", ondelete="CASCADE")),
)

# =====================================================
# Permission
# =====================================================

class Permission(Base):

    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), unique=True, nullable=False)

    description = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    roles = relationship(
        "Role",
        secondary=role_permissions,
        back_populates="permissions"
    )

# =====================================================
# Role
# =====================================================

class Role(Base):

    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), unique=True, nullable=False)

    description = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    users = relationship(
        "User",
        secondary=user_roles,
        back_populates="roles"
    )

    permissions = relationship(
        "Permission",
        secondary=role_permissions,
        back_populates="roles"
    )

# =====================================================
# User
# =====================================================

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    first_name = Column(String(100))

    last_name = Column(String(100))

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    username = Column(
        String(100),
        unique=True,
        nullable=False
    )

    password_hash = Column(Text, nullable=False)

    department = Column(String(100))

    designation = Column(String(100))

    phone = Column(String(20))

    is_active = Column(Boolean, default=True)

    is_verified = Column(Boolean, default=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    roles = relationship(
        "Role",
        secondary=user_roles,
        back_populates="users"
    )

    refresh_tokens = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete"
    )

# =====================================================
# Refresh Token
# =====================================================

class RefreshToken(Base):

    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE")
    )

    token = Column(Text)

    expires_at = Column(DateTime)

    revoked = Column(Boolean, default=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user = relationship(
        "User",
        back_populates="refresh_tokens"
    )

# =====================================================
# Existing Document Models
# =====================================================

class Document(Base):

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)

    file_name = Column(String(255), unique=True, nullable=False)

    document_type = Column(String(50), nullable=False)

    department = Column(String(100), nullable=False)

    owner = Column(String(100), nullable=False)

    version = Column(Integer, default=1)

    status = Column(String(30), default="Pending")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    chunks = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete"
    )

    versions = relationship(
        "DocumentVersion",
        back_populates="document",
        cascade="all, delete"
    )
# =====================================================
# Document Chunks
# =====================================================

class DocumentChunk(Base):

    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True)

    document_id = Column(
        Integer,
        ForeignKey("documents.id", ondelete="CASCADE")
    )

    chunk_number = Column(Integer)

    chunk_text = Column(Text)

    embedding_id = Column(String(255))

    page_number = Column(Integer)

    document = relationship(
        "Document",
        back_populates="chunks"
    )


# =====================================================
# Document Versions
# =====================================================

class DocumentVersion(Base):

    __tablename__ = "document_versions"

    id = Column(Integer, primary_key=True)

    document_id = Column(
        Integer,
        ForeignKey("documents.id", ondelete="CASCADE")
    )

    version = Column(Integer)

    uploaded_by = Column(String(100))

    approved_by = Column(String(100))

    approval_date = Column(DateTime)

    document = relationship(
        "Document",
        back_populates="versions"
    )


# =====================================================
# Document Permissions
# =====================================================

class DocumentPermission(Base):

    __tablename__ = "document_permissions"

    id = Column(Integer, primary_key=True)

    role = Column(String(100), nullable=False)

    department = Column(String(100), nullable=False)

    access_level = Column(String(50), nullable=False)