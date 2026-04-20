SELECT
    lu.id,
    MAX(lu.version) as version,
    lu.name,
    lu.surname,
    lu.password,
    lui.storage_id AS photo,
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
    lu.created_by
FROM liceo_users lu
LEFT JOIN liceo_roles_users lru
    ON lru.user_id = lu.id
LEFT JOIN liceo_roles lr
    ON lr.id = lru.role_id
LEFT JOIN liceo_users_images lui
    ON lui.user_id = lu.id
WHERE lu.username = :username
GROUP BY
    lu.id,
    lu.name,
    lu.surname,
    lu.password,
    lu.username,
    lu.password_expired,
    lu.account_active,
    lu.created_at,
    lu.created_by,
    lui.storage_id