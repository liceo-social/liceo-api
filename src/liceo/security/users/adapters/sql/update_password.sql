UPDATE liceo_users SET 
    password = :password,
    last_updated_at = :last_updated_at,
    last_updated_by = :last_updated_by
WHERE id=:id
RETURNING id;