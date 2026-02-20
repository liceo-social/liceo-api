INSERT INTO liceo_people_contacts
(
    id,
    type,
    value,
    person_id,
    is_emergency,
    created_at,
    created_by
)
VALUES
(
    :id,
    :type,
    :value,
    :person_id,
    :is_emergency,
    :created_at,
    :created_by
) RETURNING id;