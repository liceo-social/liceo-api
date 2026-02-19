SELECT
    x.*,
    COUNT(*) OVER () AS total_count
FROM
(
    SELECT 
        lr.id,
        lr.version,
        lr.name,
        lr.description,
        lr.created_at,
        lr.created_by,
        lr.last_updated_at,
        lr.last_updated_by,
        '{}'::text[] as permissions
    FROM liceo_roles lr 
) as x
LIMIT :max
OFFSET :offset