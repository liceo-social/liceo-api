INSERT INTO events (id, aggregate_id, version, event_type, "when", data)
SELECT
    :id,
    :aggregate_id,
    :version,
    :event_type,
    :when,
    :data
WHERE (
    SELECT COALESCE(MAX(version), 0)
    FROM events
    WHERE aggregate_id = :aggregate_id
) = :version;
