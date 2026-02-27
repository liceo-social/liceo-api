INSERT INTO liceo_projects_coordinators
(
    id,
    version,
    project_id,
    user_id,
    is_owner,
    created_by,
    created_at
)
VALUES
(
    :id,
    :version,
    :project_id,
    :user_id,
    :is_owner,
    :created_by,
    :created_at
) RETURNING id;