UPDATE liceo_mails SET
    status= :status,
    latest_error = :latest_error,
    next_attempt = :next_attempt
WHERE id = :id;