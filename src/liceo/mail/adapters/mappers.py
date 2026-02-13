from ..domain import entities, vo


def sql_row_to_mail(rows: list[dict]) -> list[entities.Mail]:
    mail_list = []
    for row in rows:
        mail = entities.Mail(id=vo.MailId(row["id"]))
        mail.recipient = row["recipient"]
        mail.subject = row["subject"]
        mail.body = row["body"]
        mail.status = row["status"]
        mail.retry_count = row["retry_count"]
        mail.max_retries = row["max_retries"]
        mail.next_attempt_at = row["next_attempt_at"]
        mail.last_error = row["last_error"]
        mail.created_at = row["created_at"]
        mail.sent_at = row["sent_at"]
        mail_list.append(mail)
    return mail_list
