INSERT INTO liceo_files
(
    id,
    filename,
    path,
    created_at,
    created_by
)
VALUES
(
    :id,
    :filename,
    :path,
    :created_at,
    :created_by
) RETURNING id;