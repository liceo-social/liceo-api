INSERT INTO liceo_projects_people
(
    id,
    version,
    project_id,
    person_id
)
VALUES
(
    :id,
    :version,
    :project_id,
    :person_id
) RETURNING id;