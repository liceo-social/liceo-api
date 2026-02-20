INSERT INTO liceo_people_identifications
(
    id,
    type,
    value,
    person_id,
    created_at,
    created_by
)
VALUESVersio
(
    :id,
    :type,
    :value,
    :person_id,
    :created_at,
    :created_by
) RETURNING id;