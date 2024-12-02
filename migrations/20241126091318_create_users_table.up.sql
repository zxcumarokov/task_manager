-- 000003_create_users_table.up.sq
CREATE TABLE users (
    username VARCHAR(255) PRIMARY KEY,
    encrypted_password TEXT NOT NULL,
    encrypted_refresh_token TEXT,
    encrypted_access_token TEXT
);

