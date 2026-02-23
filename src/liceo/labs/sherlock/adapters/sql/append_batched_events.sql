INSERT INTO liceo_events 
(
    id, 
    aggregate_id, 
    aggregate_type, 
    version, 
    event_type, 
    event_at,
    event_by,
    data
) 
VALUES
(
    :id,
    :aggregate_id,
    :aggregate_type,
    :version,
    :event_type,
    :event_at,
    :event_by,
    :data
)
ON CONFLICT (aggregate_id, aggregate_type, version) DO NOTHING;