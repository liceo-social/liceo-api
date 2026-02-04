SELECT
    lu.*,
    COUNT(*) OVER () AS total_count
FROM liceo_users lu
WHERE lu.name ilike :name
AND lu.surname = :surname
ORDER BY created_at DESC
LIMIT :max OFFSET :offset;
