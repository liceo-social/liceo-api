INSERT INTO liceo_people
(
    id,
    name,
    surname,
    photo,
    alias,
    birthdate,
    sex,
    genre,
    responsible_id,
    created_at,
    created_by
)
VALUES
(
    :id,
    :name,
    :surname,
    :photo,
    :alias,
    :birthdate,
    :sex,
    :genre,
    :responsible_id,
    :created_at,
    :created_by
) RETURNING id;