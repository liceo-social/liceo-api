SELECT
    id,
    filename,
    type,
    path,
    created_at,
    created_by
FROM liceo_storage 
WHERE id = :id;