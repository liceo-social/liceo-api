INSERT INTO liceo_users (
    id,
    name,
    surname,
    username,    
    created_at,
    created_by
)
VALUES
(
    :id,
    :name,
    :surname,
    :username,
    :created_at,
    :created_by
) RETURNING id;