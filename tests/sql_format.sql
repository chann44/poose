-- 20240101120000_create_users.sql

-- +migrate Up
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL
);

-- +migrate Down
DROP TABLE users;