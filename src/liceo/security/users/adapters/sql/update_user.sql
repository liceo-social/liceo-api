UPDATE liceo_users SET 
    version = :version,
    name=:name,
    surname=:surname,
    username=:username,
    last_updated_at=:last_updated_at,
    last_updated_by=:last_updated_by
WHERE id=:id
RETURNING id, version;