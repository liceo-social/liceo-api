SELECT 
    id,
    recipient,
    subject,
    body,
    status,
    next_attempt,
    created_at,
FROM liceo_outbound_emails
WHERE status = 'PENDING'
AND next_attempt_at <= NOW()
FOR UPDATE SKIP LOCKED
LIMIT 50;
