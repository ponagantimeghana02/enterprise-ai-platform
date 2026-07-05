from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func

from sqlalchemy.orm import relationship

from backend.database.db import Base


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


class DocumentPermission(Base):

    __tablename__ = "document_permissions"

    id = Column(Integer, primary_key=True)

    role = Column(String(100), nullable=False)

    department = Column(String(100), nullable=False)

    access_level = Column(String(50), nullable=False)