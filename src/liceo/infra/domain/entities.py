from typing import Generic, TypeVar
from datetime import datetime
from .vo import AuditInfo
from liceo.labs.sherlock.core import Aggregate

T = TypeVar("T")


class AuditableAggregate(Aggregate, Generic[T]):
    audit: AuditInfo[T]

    def mark_created_by(self, by: T):
        self.audit = AuditInfo(by)
        self.audit.created_at = datetime.now()

    def mark_modified_by(self, by: T):
        self.audit.last_modified_by = by
        self.audit.last_modified_at = datetime.now()

    def mark_deleted_by(self, by: T):
        self.audit.deleted_by = by
        self.audit.deleted_at = datetime.now()

    @property
    def created_by(self):
        return self.audit.created_by

    @property
    def created_at(self):
        return self.audit.created_at

    @property
    def last_modified_by(self):
        return self.audit.last_modified_by

    @property
    def last_modified_at(self):
        return self.audit.last_modified_at

    @property
    def deleted_by(self):
        return self.audit.deleted_by

    @property
    def deleted_at(self):
        return self.audit.deleted_at
