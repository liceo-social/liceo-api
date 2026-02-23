INSERT INTO liceo_storage
(
    id,
    version,
    filename,
    type,
    path,
    created_at,
    created_by
)
VALUES
(
    :id,
    :version,
    :filename,
    :type,
    :path,
    :created_at,
    :created_by
) RETURNING id;