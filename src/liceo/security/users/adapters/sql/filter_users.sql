SELECT 
    x.*,
   COUNT(*) OVER () AS total_count
FROM
(
SELECT
    lu.id,
    lu.name,
    max(lu.version) as version,
    lu.name || ' ' || lu.surname AS full_name,
    lu.surname,
    lu.username,
    COALESCE(
        array_agg(lr.name) FILTER (WHERE lr.name IS NOT NULL),
        '{}'::text[]
    ) AS roles,
    lu.password_expired,
    lu.account_active,
    lu.account_blocked,
    lu.account_expired,    
    lu.created_at,
    lui.storage_id AS photo
FROM liceo_users lu
LEFT JOIN liceo_roles_users lru
    ON lru.user_id = lu.id
LEFT JOIN liceo_roles lr
    ON lr.id = lru.role_id
LEFT JOIN liceo_users_images lui
    ON lui.user_id = lu.id
WHERE lu.name ilike :name
AND lu.surname = :surname
GROUP BY
    lu.id,
    lu.name,
    lu.surname,
    lu.username,
    lu.password_expired,
    lu.account_active,
    lu.created_at,
    lui.storage_id
) AS x 
ORDER BY x.created_at DESC
LIMIT :max
OFFSET :offset;