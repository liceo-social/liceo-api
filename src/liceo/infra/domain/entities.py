from dataclasses import dataclass
from typing import Generic, TypeVar, Callable, Any
from datetime import datetime
from .vo import AuditInfo
from abc import abstractmethod
from liceo.infra.domain import error
from liceo.labs.sherlock.core import Aggregate, AggregateRoot

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


class AuditableAggregateRoot(AggregateRoot, Generic[T]):
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


@dataclass
class PermissionAwareCommand(Generic[T]):
    check_user_permissions: Callable[[list[str], T], Any]

    def check_user_permission(self, permission: str, user_id: T):
        return self.check_user_permissions([permission], user_id)
