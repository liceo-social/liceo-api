SELECT
    lu.id,
    lu.username,
    CONCAT(lu.name, ' ', lu.surname) as full_name,
    COUNT(*) OVER () AS total_count
FROM liceo_users lu
WHERE lu.name ilike :name
AND lu.surname = :surname
ORDER BY created_at DESC
LIMIT :max OFFSET :offset;
