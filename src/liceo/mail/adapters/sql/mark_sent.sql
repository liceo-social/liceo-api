UPDATE liceo_outbound_emails SET
    status= :status,
    sent_at = :sent_at
WHERE id = :id;