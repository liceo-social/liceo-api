SELECT
    lu.id,
    lu.name || ' ' || lu.surname AS full_name,
    lu.username,
    COALESCE(
        array_agg(lr.name) FILTER (WHERE lr.name IS NOT NULL),
        '{}'::text[]
    ) AS roles,
    lu.password_expired,
    lu.account_active,
    lu.account_blocked,
    lu.account_expired,
    COUNT(*) OVER () AS total_count
FROM liceo_users lu
LEFT JOIN liceo_roles_users lru
    ON lru.user_id = lu.id
LEFT JOIN liceo_roles lr
    ON lr.id = lru.role_id
WHERE lu.name ilike :name
AND lu.surname = :surname
GROUP BY
    lu.id,
    lu.username,
    lu.password_expired,
    lu.account_active
LIMIT :max
OFFSET :offset;