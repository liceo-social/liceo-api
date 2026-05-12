INSERT INTO liceo_users_ott
(
    id,
    user_id,
    token_hash,
    created_at,
    expires_at
)
VALUES
(
    :id,
    :user_id,
    :token_hash,
    :created_at,
    :expires_at
);