INSERT INTO liceo_storage
(
    id,
    filename,
    type,
    path,
    created_at,
    created_by
)
VALUES
(
    :id,
    :filename,
    :type,
    :path,
    :created_at,
    :created_by
) RETURNING id;