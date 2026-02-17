from shortuuid import random
from liceo.mail.domain.entities import Mail
from liceo.labs.db.sql import sql, SQLRepository
from ..application.repository import MailRepository
from .mappers import sql_row_to_mail


class SQLMailRepository(MailRepository, SQLRepository):
    def generate_id(self) -> str:
        return random()

    def save(self, mail: Mail) -> Mail:
        sql = self.resolve_sql(self.save)
        self._get_connection().execute(
            sql,
            params={
                "id": mail.id.id,
                "version": mail._version,
                "recipient": mail.recipient,
                "subject": mail.subject,
                "body": mail.body,
                "status": mail.status,
                "next_attempt_at": mail.next_attempt_at,
                "created_at": mail.created_at,
            }
        )
        return mail

    @sql(sql_row_to_mail)
    def fetch_pending(self) -> list[Mail]:
        return []

    def mark_failed(self, mail: Mail) -> Mail:
        sql = self.resolve_sql(self.mark_failed)
        self._get_connection().execute(
            sql,
            params={
                "id": mail.id,
                "status": mail.status,
                "next_attempt": mail.next_attempt_at,
                "retry_count": mail.retry_count,
                "last_error": mail.last_error,
            }
        )
        return mail

    def mark_sent(self, mail: Mail) -> Mail:
        sql = self.resolve_sql(self.mark_failed)
        self._get_connection().execute(
            sql,
            params={
                "id": mail.id,
                "status": mail.status,
                "sent_at": mail.sent_at
            }
        )
        return mail
