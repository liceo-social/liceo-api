CREATE TABLE IF NOT EXISTS liceo_users (
    id TEXT PRIMARY KEY,
    name TEXT,
    username TEXT,
    password TEXT,
    roles TEXT []
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
