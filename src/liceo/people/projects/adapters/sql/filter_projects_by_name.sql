SELECT 
    x.*,
    COUNT(*) OVER () AS total_count
FROM
(
    SELECT p.*
    FROM liceo_projects p
    WHERE p.name ilike :name
    ORDER BY p.name
) as x
LIMIT :max
OFFSET :offset