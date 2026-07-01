-- =====================================================
-- Knowledge Base Database Schema
-- PostgreSQL
-- =====================================================

-- ==========================================
-- Documents
-- ==========================================
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,

    title VARCHAR(255) NOT NULL,
    file_name VARCHAR(255) NOT NULL,

    document_type VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,

    owner VARCHAR(150) NOT NULL,

    version VARCHAR(20) NOT NULL DEFAULT '1.0',

    status VARCHAR(30) NOT NULL
        CHECK (status IN ('Draft', 'Pending', 'Approved', 'Rejected', 'Archived')),

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- Document Chunks
-- ==========================================
CREATE TABLE document_chunks (

    id SERIAL PRIMARY KEY,

    document_id INTEGER NOT NULL,

    chunk_number INTEGER NOT NULL,

    chunk_text TEXT NOT NULL,

    embedding_id VARCHAR(255),

    page_number INTEGER NOT NULL,

    CONSTRAINT fk_document_chunk
        FOREIGN KEY (document_id)
        REFERENCES documents(id)
        ON DELETE CASCADE,

    CONSTRAINT unique_chunk
        UNIQUE(document_id, chunk_number)
);

-- ==========================================
-- Document Versions
-- ==========================================
CREATE TABLE document_versions (

    id SERIAL PRIMARY KEY,

    document_id INTEGER NOT NULL,

    version VARCHAR(20) NOT NULL,

    uploaded_by INTEGER NOT NULL,

    approved_by INTEGER,

    approval_date TIMESTAMP,

    CONSTRAINT fk_document_version
        FOREIGN KEY (document_id)
        REFERENCES documents(id)
        ON DELETE CASCADE
);

-- ==========================================
-- Document Permissions
-- ==========================================
CREATE TABLE document_permissions (

    id SERIAL PRIMARY KEY,

    role VARCHAR(50) NOT NULL,

    department VARCHAR(100) NOT NULL,

    access_level VARCHAR(20) NOT NULL
        CHECK (access_level IN ('Read', 'Write', 'Admin')),

    CONSTRAINT unique_permission
        UNIQUE(role, department)
);

-- =====================================================
-- Indexes
-- =====================================================

CREATE INDEX idx_documents_title
ON documents(title);

CREATE INDEX idx_documents_department
ON documents(department);

CREATE INDEX idx_documents_owner
ON documents(owner);

CREATE INDEX idx_documents_status
ON documents(status);

CREATE INDEX idx_chunks_document
ON document_chunks(document_id);

CREATE INDEX idx_chunks_embedding
ON document_chunks(embedding_id);

CREATE INDEX idx_versions_document
ON document_versions(document_id);

CREATE INDEX idx_permissions_role
ON document_permissions(role);

CREATE INDEX idx_permissions_department
ON document_permissions(department);