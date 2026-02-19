SELECT p.*
FROM liceo_permissions p
JOIN liceo_roles_permissions lrp
ON lrp.permission_id = p.id
WHERE lrp.role_id = :role_id
ORDER BY p.name;