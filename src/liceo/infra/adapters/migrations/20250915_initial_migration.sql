-- ########################
-- ###        ADMIN     ###
-- ########################

CREATE TABLE IF NOT EXISTS liceo_users (
    id TEXT PRIMARY KEY,
    name TEXT,
    surname TEXT,
    username TEXT,
    password TEXT,
    password_expired BOOLEAN DEFAULT FALSE,
    account_active BOOLEAN DEFAULT FALSE,
    account_blocked BOOLEAN DEFAULT FALSE,
    account_expired BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP,
    created_by TEXT
);

CREATE TABLE IF NOT EXISTS liceo_permissions (
    id TEXT PRIMARY KEY,
    name TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS liceo_roles (
    id TEXT PRIMARY KEY,
    name TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS liceo_roles_permissions (
    role_id TEXT,
    permission_id TEXT,
    UNIQUE("role_id", "permission_id")
);

CREATE TABLE IF NOT EXISTS liceo_roles_users (
    role_id TEXT,
    user_id TEXT,
    UNIQUE("role_id", "user_id")
);

CREATE TABLE IF NOT EXISTS liceo_events (
    id TEXT PRIMARY KEY,
    aggregate_id TEXT,
    version INTEGER,
    event_type TEXT,
    "when" TIMESTAMP,
    data JSONB
    -- UNIQUE("aggregate_id", "version")
);


-- ########################
-- ###      FILES       ###
-- ########################

CREATE TABLE IF NOT EXISTS liceo_files (
    id TEXT PRIMARY KEY,
    filename TEXT,
    path TEXT,
    created_at TIMESTAMP,
    created_by TEXT
);