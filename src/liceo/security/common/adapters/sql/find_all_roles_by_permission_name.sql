SELECT 
lr.name as role_name
FROM liceo_permissions lp
JOIN liceo_roles_permissions lrp
ON lp.id = lrp.permission_id
JOIN liceo_roles lr 
ON lr.id = lrp.role_id
WHERE lp.name = :name;