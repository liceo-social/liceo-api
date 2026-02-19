UPDATE liceo_roles SET 
    version = :version,
    last_updated_by = :last_updated_by,
    last_updated_at = :last_updated_at
WHERE id = :id;