UPDATE liceo_users SET
    version = :version
WHERE id = :user_id
RETURNING id