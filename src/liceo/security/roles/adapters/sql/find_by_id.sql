SELECT 
    lr.id,
    lr.name,
    lr.description,
    MAX(lr.version) as version,
    COALESCE(
        array_agg(lp.name) FILTER (WHERE lp.name IS NOT NULL),
        '{}'::text[]
    ) AS permissions
FROM liceo_roles lr 
LEFT JOIN liceo_roles_permissions lrp ON lr.id = lrp.role_id
LEFT JOIN liceo_permissions lp ON lp.id = lrp.permission_id
WHERE lr.id = :id
GROUP BY
    lr.id,
    lr.name,
    lr.description
