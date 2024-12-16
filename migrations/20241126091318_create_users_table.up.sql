CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    encrypted_password TEXT NOT NULL,
    encrypted_refresh_token TEXT,
    encrypted_access_token TEXT
);

