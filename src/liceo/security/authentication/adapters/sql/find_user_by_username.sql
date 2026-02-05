SELECT
    lu.id,
    lu.username,
    lu.password,
    array_agg(lr.name ORDER BY lr.name) AS roles
FROM liceo_users lu
WHERE lu.username = :username
JOIN liceo_roles_users lru ON lru.user_id = lu.id
JOIN liceo_roles lr ON lru.role_id = lr.id
GROUP BY lu.id, lu.username, lu.password;
