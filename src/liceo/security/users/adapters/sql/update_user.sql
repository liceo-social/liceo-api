UPDATE liceo_users SET 
    name = :name,
    surname = :surname,
    username = :username    
WHERE id = :id
RETURNING id;