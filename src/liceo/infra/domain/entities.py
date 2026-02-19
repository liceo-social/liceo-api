from dataclasses import dataclass
from typing import Generic, TypeVar, Callable, Any
from datetime import datetime
from .vo import AuditInfo
from liceo.labs.sherlock.domain.entities import Aggregate, AggregateRoot, AggregateId

T = TypeVar("T", bound=AggregateId)
U = TypeVar("U", bound=AggregateId)


class AuditableAggregate(Aggregate[T], Generic[T, U],):
    audit: AuditInfo[U]

    def set_created(self, by: U, when: datetime):
        self.audit = AuditInfo(by)
        self.audit.created_at = when

    def mark_created_by(self, by: U):
        self.audit = AuditInfo(by)
        self.audit.created_at = datetime.now()

    def set_updated(self, by: U, when: datetime):
        self.audit.last_updated_by = by
        self.audit.last_updated_at = when

    def mark_updated_by(self, by: U):
        self.audit.last_updated_by = by
        self.audit.last_updated_at = datetime.now()

    def mark_deleted_by(self, by: U):
        self.audit.deleted_by = by
        self.audit.deleted_at = datetime.now()

    @property
    def created_by(self):
        return self.audit.created_by

    @property
    def created_at(self):
        return self.audit.created_at

    @property
    def last_updated_by(self):
        return self.audit.last_updated_by

    @property
    def last_updated_at(self):
        return self.audit.last_updated_at

    @property
    def deleted_by(self):
        return self.audit.deleted_by

    @property
    def deleted_at(self):
        return self.audit.deleted_at


class AuditableAggregateRoot(AggregateRoot, Generic[T]):
    audit: AuditInfo[T]

    def mark_created_by(self, by: T):
        self.audit = AuditInfo(by)
        self.audit.created_at = datetime.now()

    def mark_updated_by(self, by: T):
        self.audit.last_updated_by = by
        self.audit.last_updated_at = datetime.now()

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
    def last_updated_by(self):
        return self.audit.last_updated_by

    @property
    def last_updated_at(self):
        return self.audit.last_updated_at

    @property
    def deleted_by(self):
        return self.audit.deleted_by

    @property
    def deleted_at(self):
        return self.audit.deleted_at


U = TypeVar("U")


@dataclass
class PermissionAwareCommand(Generic[U]):
    check_permissions: Callable[[list[str], U], Any]

    def check_permission(self, permission: str, user_id: U):
        return self.check_permissions([permission], user_id)


@dataclass
class VersionAwareCommand:
    expected_version: int
