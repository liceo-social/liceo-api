UPDATE liceo_users SET 
    password = :password
WHERE id=:id
RETURNING id;