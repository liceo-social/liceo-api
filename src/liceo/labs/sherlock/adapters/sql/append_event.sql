INSERT INTO liceo_events (id, aggregate_id, version, event_type, "when", data)
SELECT
    :id,
    :aggregate_id,
    :version,
    :event_type,
    :when,
    :data
WHERE (
    SELECT COALESCE(MAX(version), 0)
    FROM liceo_events
    WHERE aggregate_id = :aggregate_id
) = :version;
