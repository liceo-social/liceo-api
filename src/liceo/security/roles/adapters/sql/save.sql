INSERT INTO liceo_roles 
(
    id,
    version,
    name,
    description,
    created_by,
    created_at
)
VALUES
(
    :id,
    :version,
    :name,
    :description,
    :created_by,
    :created_at
) RETURNING id;