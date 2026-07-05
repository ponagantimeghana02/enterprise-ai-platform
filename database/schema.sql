CREATE TABLE roles(
    id SERIAL PRIMARY KEY,
    role_name VARCHAR(100) UNIQUE
);
CREATE TABLE permissions(
    id SERIAL PRIMARY KEY,
    permission_name VARCHAR(225),
    module_name VARCHAR(225),
);
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200),
    email VARCHAR(255) UNIQUE,
    password_hash TEXT,
    role INTEGER REFERENCES roles(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action TEXT,
    endpoint TEXT,
    ip_address TEXT,
    status VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO roles(role_name)
VALUES
('Admin'),
('HR'),
('Manager'),
('Employee'),
('Support');