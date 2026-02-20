import pytest
from datetime import datetime
from liceo.people.people.domain import entities, vo, errors


def create_main_id():
    return vo.Identification(type="national", value="000000000Z")


def create_emergency_contact():
    return vo.EmergencyContact(type="mobile", value={})


def test_create_a_new_person_successfully():
    person = entities.Person.create(entities.Person.CreatePersonCommand(
        id=vo.PersonId("person-id"),
        name="John",
        photo=None,
        surname="Perez Doe",
        alias="reckless",
        birthdate=datetime.fromisocalendar(1980, 1, 1),
        sex=vo.Sex.MALE,
        genre=vo.Genre.HETERO,
        main_id=create_main_id(),
        emergency_contact=create_emergency_contact(),
        responsible=vo.UserId(id="responsible-id"),
        is_responsible_from_projects=True,
        created_by=vo.UserId(id="user-id"),
        projects=[vo.ProjectId(id="project_id")]
    ))

    assert person._version == 1
    assert person.emergency_contact
    assert person.main_id


def test_create_fails_because_missing_projects():
    with pytest.raises(errors.NoProjectsAttached):
        entities.Person.create(entities.Person.CreatePersonCommand(
            id=vo.PersonId("person-id"),
            name="John",
            photo=None,
            surname="Perez Doe",
            alias="reckless",
            birthdate=datetime.fromisocalendar(1980, 1, 1),
            sex=vo.Sex.MALE,
            genre=vo.Genre.HETERO,
            main_id=create_main_id(),
            emergency_contact=create_emergency_contact(),
            responsible=vo.UserId(id="responsible-id"),
            is_responsible_from_projects=True,
            created_by=vo.UserId(id="user-id"),
            projects=[]
        ))


def test_create_fails_because_missing_responsible():
    with pytest.raises(errors.NoResponsible):
        entities.Person.create(entities.Person.CreatePersonCommand(
            id=vo.PersonId("person-id"),
            name="John",
            photo=None,
            surname="Perez Doe",
            alias="reckless",
            birthdate=datetime.fromisocalendar(1980, 1, 1),
            sex=vo.Sex.MALE,
            genre=vo.Genre.HETERO,
            main_id=create_main_id(),
            emergency_contact=create_emergency_contact(),
            responsible=None,
            is_responsible_from_projects=False,
            created_by=vo.UserId(id="user-id"),
            projects=[vo.ProjectId(id="project")]
        ))


def test_create_fails_because_responsible_is_not_from_projects():
    with pytest.raises(errors.ResponsibleNotFromProjects):
        entities.Person.create(entities.Person.CreatePersonCommand(
            id=vo.PersonId("person-id"),
            name="John",
            photo=None,
            surname="Perez Doe",
            alias="reckless",
            birthdate=datetime.fromisocalendar(1980, 1, 1),
            sex=vo.Sex.MALE,
            genre=vo.Genre.HETERO,
            main_id=create_main_id(),
            emergency_contact=create_emergency_contact(),
            responsible=vo.UserId(id="responsible"),
            is_responsible_from_projects=False,
            created_by=vo.UserId(id="user-id"),
            projects=[vo.ProjectId(id="project")]
        ))
