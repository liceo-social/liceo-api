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
        '{}'::text[] as permissions
    FROM liceo_roles lr 
) as x
LIMIT :max
OFFSET :offset