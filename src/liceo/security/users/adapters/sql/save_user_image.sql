INSERT INTO liceo_users_images
(
    user_id,
    storage_id,
    dimension,
    created_at,
    created_by
)
VALUES
(
    :user_id,
    :storage_id,
    :dimension,
    :created_at,
    :created_by
)
ON CONFLICT (user_id, dimension)
DO UPDATE SET
    storage_id=:storage_id,
    dimension=:dimension,
    last_updated_at=:last_updated_at,
    last_updated_by=:last_updated_by;