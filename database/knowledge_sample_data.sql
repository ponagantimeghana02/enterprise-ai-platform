-- Knowledge Base Sample Data
-- Sample data for testing and development

-- Insert sample documents
INSERT INTO documents (title, file_name, document_type, department, owner, version, status) VALUES
    ('Company Security Policy', 'security_policy_v1.pdf', 'policy', 'security', 'alice.johnson', 1, 'approved'),
    ('Employee Handbook 2024', 'employee_handbook_2024.docx', 'handbook', 'hr', 'bob.smith', 2, 'approved'),
    ('Q3 Financial Report', 'q3_financial_report.xlsx', 'report', 'finance', 'charlie.brown', 1, 'pending_review'),
    ('API Integration Guide', 'api_integration_guide.md', 'guide', 'engineering', 'diana.ross', 1, 'draft'),
    ('Marketing Strategy 2024', 'marketing_strategy_2024.pptx', 'strategy', 'marketing', 'edward.wilson', 1, 'approved'),
    ('Data Privacy Compliance', 'data_privacy_compliance.pdf', 'compliance', 'legal', 'fiona.green', 1, 'archived'),
    ('Product Roadmap Q4', 'product_roadmap_q4.pdf', 'roadmap', 'product', 'george.miller', 1, 'approved'),
    ('IT Infrastructure Guide', 'it_infrastructure_guide.docx', 'guide', 'it', 'hannah.davis', 1, 'draft');

-- Insert sample document chunks (for document_id 1 - Company Security Policy)
INSERT INTO document_chunks (document_id, chunk_number, chunk_text, page_number) VALUES
    (1, 1, 'Company Security Policy - Version 1.0', 1),
    (1, 2, 'All employees must follow security protocols when accessing company systems.', 1),
    (1, 3, 'Passwords must be changed every 90 days and should contain at least 12 characters.', 2),
    (1, 4, 'Multi-factor authentication is required for all remote access to company resources.', 2),
    (1, 5, 'Sensitive data must be encrypted both at rest and in transit.', 3);

-- Insert sample document chunks (for document_id 2 - Employee Handbook)
INSERT INTO document_chunks (document_id, chunk_number, chunk_text, page_number) VALUES
    (2, 1, 'Employee Handbook 2024 - Welcome to Our Company', 1),
    (2, 2, 'Our mission is to deliver exceptional value to our customers through innovation.', 1),
    (2, 3, 'Work hours are flexible from 8 AM to 6 PM, with core hours from 10 AM to 4 PM.', 2),
    (2, 4, 'All employees receive 20 days of paid time off per calendar year.', 3),
    (2, 5, 'Health insurance benefits are available to all full-time employees.', 4);

-- Insert sample document versions
INSERT INTO document_versions (document_id, version, uploaded_by, approved_by, approval_date) VALUES
    (1, 1, 'alice.johnson', 'security.admin', '2024-01-15 10:30:00'),
    (2, 1, 'bob.smith', 'hr.director', '2024-01-10 14:20:00'),
    (2, 2, 'bob.smith', 'hr.director', '2024-03-20 11:15:00'),
    (3, 1, 'charlie.brown', NULL, NULL),
    (5, 1, 'edward.wilson', 'marketing.head', '2024-02-28 16:45:00'),
    (7, 1, 'george.miller', 'product.director', '2024-03-10 09:30:00');

-- Insert additional document permissions (beyond defaults)
INSERT INTO document_permissions (role, department, access_level) VALUES
    ('security_analyst', 'security', 'write'),
    ('hr_specialist', 'hr', 'write'),
    ('finance_analyst', 'finance', 'write'),
    ('engineer', 'engineering', 'write'),
    ('marketing_specialist', 'marketing', 'write'),
    ('legal_counsel', 'legal', 'admin'),
    ('product_manager', 'product', 'write'),
    ('it_specialist', 'it', 'write'),
    ('contractor', 'all', 'read'),
    ('intern', 'all', 'read');

-- Update some document chunks with embedding IDs (simulating vector embeddings)
UPDATE document_chunks 
SET embedding_id = 'emb_' || id::text || '_' || document_id::text 
WHERE id <= 10;

-- Verify data insertion
SELECT 'Documents inserted: ' || COUNT(*)::text FROM documents;
SELECT 'Document chunks inserted: ' || COUNT(*)::text FROM document_chunks;
SELECT 'Document versions inserted: ' || COUNT(*)::text FROM document_versions;
SELECT 'Document permissions inserted: ' || COUNT(*)::text FROM document_permissions;