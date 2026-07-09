

CREATE INDEX IF NOT EXISTS idx_users_email
ON users(email);

CREATE INDEX IF NOT EXISTS idx_users_role
ON users(role);



CREATE INDEX IF NOT EXISTS idx_chat_user
ON chat_history(user_id);

CREATE INDEX IF NOT EXISTS idx_chat_created
ON chat_history(created_at DESC);



CREATE INDEX IF NOT EXISTS idx_documents_category
ON documents(category);

CREATE INDEX IF NOT EXISTS idx_documents_created
ON documents(created_at DESC);



CREATE INDEX IF NOT EXISTS idx_embeddings_doc
ON embeddings(document_id);


-- Audit Logs

CREATE INDEX IF NOT EXISTS idx_audit_user
ON audit_logs(user_id);

CREATE INDEX IF NOT EXISTS idx_audit_time
ON audit_logs(created_at DESC);



CREATE INDEX IF NOT EXISTS idx_chat_user_time
ON chat_history(user_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_doc_category_status
ON documents(category,status);


SELECT *
FROM chat_history
WHERE user_id=15;

-- AFTER

SELECT
id,
question,
answer,
created_at
FROM chat_history
WHERE user_id=15
ORDER BY created_at DESC
LIMIT 20;



SELECT *
FROM documents
WHERE category='AI';

-- AFTER

SELECT
id,
title,
category
FROM documents
WHERE category='AI';



EXPLAIN ANALYZE

SELECT
id,
question,
answer
FROM chat_history
WHERE user_id=15;



CREATE TABLE IF NOT EXISTS audit_logs_partitioned(

id SERIAL,

user_id INTEGER,

action TEXT,

created_at TIMESTAMP

)
PARTITION BY RANGE(created_at);


CREATE TABLE audit_logs_2025

PARTITION OF audit_logs_partitioned

FOR VALUES FROM ('2025-01-01')

TO ('2026-01-01');


CREATE TABLE audit_logs_2026

PARTITION OF audit_logs_partitioned

FOR VALUES FROM ('2026-01-01')

TO ('2027-01-01');

