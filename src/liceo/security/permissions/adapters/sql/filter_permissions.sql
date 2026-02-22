SELECT
    x.*,
    COUNT(*) OVER () AS total_count
FROM
(
    SELECT lp.*
    FROM liceo_permissions lp
    WHERE lp.name ilike :name
    ORDER BY lp.name ASC
) as x
LIMIT :max
OFFSET :offset;