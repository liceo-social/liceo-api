UPDATE liceo_users SET
    version = :version,
    password_expired = :password_expired,
    account_active = :account_active,
    account_blocked = :account_blocked,
    account_expired = :account_expired,
    last_updated_at = :last_updated_at,
    last_updated_by = :last_updated_by
WHERE id=:id
RETURNING id;