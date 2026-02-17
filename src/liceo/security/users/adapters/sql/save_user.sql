INSERT INTO liceo_users (
    id,
    version,
    name,
    surname,
    username,    
    created_at,
    created_by
)
VALUES
(
    :id,
    :version,
    :name,
    :surname,
    :username,
    :created_at,
    :created_by
) RETURNING id;