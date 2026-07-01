-- PostgreSQL Database Design for FastAPI Backend

-- Drop existing tables (in reverse dependency order)
DROP TABLE IF EXISTS audit_logs;
DROP TABLE IF EXISTS refresh_tokens;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS role_permissions;
DROP TABLE IF EXISTS permissions;
DROP TABLE IF EXISTS roles;

-- 1. Roles Table
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Seed Roles
INSERT INTO roles (id, name) VALUES
(1, 'Admin'),
(2, 'HR'),
(3, 'Manager'),
(4, 'Employee'),
(5, 'Support')
ON CONFLICT (id) DO NOTHING;

-- 2. Permissions Table
CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    permission_name VARCHAR(100) UNIQUE NOT NULL,
    module VARCHAR(50) NOT NULL
);

-- Seed Permissions
INSERT INTO permissions (id, permission_name, module) VALUES
(1, 'Leave Policies', 'hr'),
(2, 'Onboarding', 'hr'),
(3, 'HR Documents', 'hr'),
(4, 'Payroll', 'finance'),
(5, 'Finance', 'finance'),
(6, 'Chat', 'assistant'),
(7, 'RAG', 'assistant'),
(8, 'Agents', 'assistant'),
(9, 'Users Dashboard', 'admin'),
(10, 'Audit Logs', 'admin'),
(11, 'Settings', 'admin')
ON CONFLICT (id) DO NOTHING;

-- 3. Role Permissions Mapping Table (RBAC Join Table)
CREATE TABLE role_permissions (
    role_id INT REFERENCES roles(id) ON DELETE CASCADE,
    permission_id INT REFERENCES permissions(id) ON DELETE CASCADE,
    PRIMARY KEY (role_id, permission_id)
);

-- Seed Role Permissions mapping
-- Admin gets all permissions (1 to 11)
INSERT INTO role_permissions (role_id, permission_id) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11);

-- HR gets Leave Policies, Onboarding, HR Documents, Chat, RAG, Agents
INSERT INTO role_permissions (role_id, permission_id) VALUES
(2, 1), (2, 2), (2, 3), (2, 6), (2, 7), (2, 8);

-- Manager gets Payroll, Finance, Chat, RAG, Agents, Leave Policies, Onboarding
INSERT INTO role_permissions (role_id, permission_id) VALUES
(3, 1), (3, 2), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8);

-- Employee gets Chat, RAG, Agents
INSERT INTO role_permissions (role_id, permission_id) VALUES
(4, 6), (4, 7), (4, 8);

-- Support gets Chat, RAG, Agents
INSERT INTO role_permissions (role_id, permission_id) VALUES
(5, 6), (5, 7), (5, 8);

-- 4. Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_id INT REFERENCES roles(id) ON DELETE RESTRICT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed an Admin User
-- Email: admin@example.com
-- Password: adminpassword (hashed using bcrypt)
INSERT INTO users (id, name, email, password_hash, role_id) VALUES
(1, 'System Admin', 'admin@example.com', '$2b$12$7wA8q95D/d6V5vX0w9Tye.mG3X5iB/yX2rW4q2r9D5P8h7M1i1vSq', 1)
ON CONFLICT (id) DO NOTHING;

-- 5. Refresh Tokens Table (session tracking & expiry)
CREATE TABLE refresh_tokens (
    id SERIAL PRIMARY KEY,
    token VARCHAR(512) UNIQUE NOT NULL,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Audit Logs Table (API access log)
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT REFERENCES users(id) ON DELETE SET NULL,
    user_email VARCHAR(100),
    ip VARCHAR(45) NOT NULL,
    endpoint VARCHAR(255) NOT NULL,
    action VARCHAR(50) NOT NULL, -- GET, POST, PUT, DELETE, etc.
    status INT NOT NULL          -- Response status code
);
