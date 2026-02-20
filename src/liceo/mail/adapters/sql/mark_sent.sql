UPDATE liceo_mails SET
    status= :status,
    sent_at = :sent_at
WHERE id = :id;