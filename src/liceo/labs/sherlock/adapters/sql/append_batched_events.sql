INSERT INTO liceo_events 
(
    id, 
    aggregate_id, 
    aggregate_type, 
    version, 
    event_type, 
    created_at, 
    data
) 
VALUES
(
    :id,
    :aggregate_id,
    :aggregate_type,
    :version,
    :event_type,
    :created_at,
    :data
)
ON CONFLICT (aggregate_id, aggregate_type, version) DO NOTHING;