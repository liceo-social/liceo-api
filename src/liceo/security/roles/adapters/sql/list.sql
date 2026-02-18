SELECT
    x.*,
    COUNT(*) OVER () AS total_count
FROM
(
    SELECT 
        lr.id,
        lr.name,
        lr.description
    FROM liceo_roles lr 
) as x
LIMIT :max
OFFSET :offset