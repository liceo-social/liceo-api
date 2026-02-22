from datetime import datetime
from pydantic import BaseModel, Field
from liceo.security.common.adapters.requests import UserContextModel
from ..application import dtos
from ..domain import vo


class EmergencyContactRequest(BaseModel):
    type: vo.ContactType
    value: str = Field(le=20)
    relationship: vo.ContactRelationship
    notes: str | None = Field(le=200)


class OfficialIdentificationRequest(BaseModel):
    type: vo.IdentificationType
    value: str = Field(le=50)
    expiration_date: datetime | None


class CreatePersonDetails(BaseModel):
    name: str = Field(le=100)
    surname: str = Field(le=200)
    photo: str | None
    alias: str = Field(le=100)
    birthdate: datetime
    sex: vo.Sex
    genre: vo.Genre
    official_id: OfficialIdentificationRequest
    emergency_contact: EmergencyContactRequest
    projects: list[str]
    responsible: str
    created_by: str


class CreatePersonRequest(BaseModel):
    user: UserContextModel
    details: CreatePersonDetails

    def to_dto(self) -> dtos.CreatePersonDTO:
        return dtos.CreatePersonDTO(
            name=self.details.name,
            surname=self.details.surname,
            photo=self.details.photo,
            alias=self.details.alias,
            birthdate=self.details.birthdate,
            sex=self.details.sex.value,
            genre=self.details.genre.value,
            official_id_type=self.details.official_id.type.value,
            official_id_value=self.details.official_id.value,
            official_id_expiration_date=self.details.official_id.expiration_date,
            emergency_contact_type=self.details.emergency_contact.type.value,
            emergency_contact_value=self.details.emergency_contact.value,
            emergency_contact_relationship=self.details.emergency_contact.relationship.value,
            emergency_contact_notes=self.details.emergency_contact.notes,
            projects=self.details.projects,
            responsible=self.details.responsible,
            created_by=self.user.id
        )
