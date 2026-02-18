UPDATE liceo_roles SET
    version = :version,
    name = :name,
    description = :description
WHERE id = :id;