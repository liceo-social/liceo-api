-- ########################
-- ###        ADMIN     ###
-- ########################

CREATE TABLE IF NOT EXISTS liceo_users (
    id TEXT PRIMARY KEY,
    version INTEGER NOT NULL,
    name TEXT,
    surname TEXT,
    username TEXT,
    password TEXT,
    password_expired BOOLEAN DEFAULT FALSE,
    account_active BOOLEAN DEFAULT FALSE,
    account_blocked BOOLEAN DEFAULT FALSE,
    account_expired BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL,
    created_by TEXT NOT NULL,
    last_updated_at TIMESTAMP,
    last_updated_by TEXT,
    UNIQUE("username")
);

CREATE TABLE IF NOT EXISTS liceo_permissions (
    id TEXT PRIMARY KEY,
    name TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS liceo_roles (
    id TEXT PRIMARY KEY,
    version INTEGER NOT NULL,
    name TEXT,
    description TEXT,
    created_at TIMESTAMP NOT NULL,
    created_by TEXT NOT NULL,
    last_updated_at TIMESTAMP,
    last_updated_by TEXT,
    CONSTRAINT fk_roles_created_by FOREIGN KEY (created_by) REFERENCES liceo_users(id),
    CONSTRAINT fk_roles_last_updated_by FOREIGN KEY (last_updated_by) REFERENCES liceo_users(id)
);

CREATE TABLE IF NOT EXISTS liceo_roles_permissions (
    role_id TEXT,
    permission_id TEXT,
    UNIQUE("role_id", "permission_id"),
    CONSTRAINT fk_roles_permissions_roles FOREIGN KEY (role_id) REFERENCES liceo_roles(id),
    CONSTRAINT fk_roles_permissions_permissions FOREIGN KEY (permission_id) REFERENCES liceo_permissions(id)
);

CREATE TABLE IF NOT EXISTS liceo_roles_users (
    role_id TEXT,
    user_id TEXT,
    UNIQUE("role_id", "user_id"),
    CONSTRAINT fk_roles_users_roles FOREIGN KEY (role_id) REFERENCES liceo_roles(id),
    CONSTRAINT fk_roles_users_users FOREIGN KEY (user_id) REFERENCES liceo_users(id)
);


-- ########################
-- ###      FILES       ###
-- ########################

CREATE TABLE IF NOT EXISTS liceo_storage (
    id TEXT PRIMARY KEY,
    version INTEGER NOT NULL,
    filename TEXT,
    type TEXT,
    path TEXT,
    created_at TIMESTAMP NOT NULL,
    created_by TEXT NOT NULL,
    CONSTRAINT fk_storage_created_by FOREIGN KEY (created_by) REFERENCES liceo_users(id)
);

CREATE TABLE IF NOT EXISTS liceo_users_images (
    user_id TEXT,
    storage_id TEXT,
    dimension TEXT DEFAULT 'original', -- small, medium, large, original
    created_at TIMESTAMP NOT NULL,
    created_by TEXT NOT NULL,
    CONSTRAINT fk_users_images_created_by FOREIGN KEY (created_by) REFERENCES liceo_users(id),
    CONSTRAINT fk_users_images_users FOREIGN KEY (user_id) REFERENCES liceo_users(id),
    CONSTRAINT fk_users_images_storage FOREIGN KEY (storage_id) REFERENCES liceo_storage(id)
);

-- ########################
-- ###      MAILS       ###
-- ########################

CREATE TABLE liceo_mails (
    id TEXT PRIMARY KEY,
    version INTEGER NOT NULL,
    recipient TEXT NOT NULL,
    subject TEXT NOT NULL,
    body TEXT NOT NULL,
    status TEXT NOT NULL, -- PENDING, SENT, FAILED
    retry_count INT NOT NULL DEFAULT 0,
    max_retries INT NOT NULL DEFAULT 5,
    next_attempt_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    last_error TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by TEXT,
    sent_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_outbound_emails_created_by FOREIGN KEY (created_by) REFERENCES liceo_users(id)
);

CREATE INDEX idx_liceo_mails_status_next_attempt
ON liceo_mails (status, next_attempt_at);

-- ########################
-- ###     EVENTS       ###
-- ########################

CREATE TABLE IF NOT EXISTS liceo_events (
    id TEXT PRIMARY KEY,
    version INTEGER NOT NULL,
    aggregate_id TEXT,
    aggregate_type TEXT,
    event_type TEXT,
    created_at TIMESTAMP,
    data JSONB,
    UNIQUE("aggregate_id", "aggregate_type", "version")
);

-- ########################
-- ###     PEOPLE       ###
-- ########################

CREATE TABLE IF NOT EXISTS liceo_people (
    id TEXT PRIMARY KEY,
    version INTEGER NOT NULL,
    name TEXT,
    surname TEXT,
    photo TEXT,
    alias TEXT,
    birthdate TIMESTAMP,
    sex TEXT,
    genre TEXT,
    responsible_id TEXT,
    created_at TIMESTAMP NOT NULL,
    created_by TEXT NOT NULL,
    last_updated_at TIMESTAMP,
    last_updated_by TEXT,
    CONSTRAINT fk_people_responsible FOREIGN KEY (responsible_id) REFERENCES liceo_users(id),
    CONSTRAINT fk_people_created_by FOREIGN KEY (created_by) REFERENCES liceo_users(id),
    CONSTRAINT fk_people_last_updated_by FOREIGN KEY (last_updated_by) REFERENCES liceo_users(id)
);

CREATE TABLE IF NOT EXISTS liceo_people_contacts (
    id TEXT PRIMARY KEY,
    version INTEGER NOT NULL,
    type TEXT NOT NULL,
    value TEXT NOT NULL,
    relationship TEXT NOT NULL,
    person_id TEXT,
    is_emergency BOOLEAN,
    created_at TIMESTAMP NOT NULL,
    created_by TEXT NOT NULL,
    last_updated_at TIMESTAMP,
    last_updated_by TEXT,
    CONSTRAINT fk_contacts_person FOREIGN KEY (person_id) REFERENCES liceo_people(id),
    CONSTRAINT fk_contacts_created_by FOREIGN KEY (created_by) REFERENCES liceo_users(id),
    CONSTRAINT fk_contacts_last_updated_by FOREIGN KEY (last_updated_by) REFERENCES liceo_users(id)
);

CREATE TABLE IF NOT EXISTS liceo_people_identifications (
    id TEXT PRIMARY KEY,
    version INTEGER NOT NULL,
    type TEXT,
    value TEXT,
    expiration_date TIMESTAMP,
    person_id TEXT,
    created_at TIMESTAMP NOT NULL,
    created_by TEXT NOT NULL,
    last_updated_at TIMESTAMP,
    last_updated_by TEXT,
    CONSTRAINT fk_identifications_person FOREIGN KEY (person_id) REFERENCES liceo_people(id),
    CONSTRAINT fk_identifications_created_by FOREIGN KEY (created_by) REFERENCES liceo_users(id),
    CONSTRAINT fk_identifications_last_updated_by FOREIGN KEY (last_updated_by) REFERENCES liceo_users(id)
);