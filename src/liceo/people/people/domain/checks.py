from . import vo, errors


def check_basic_details(details: vo.BasicDetails):
    if not (details.name and details.name.strip()):
        raise errors.BasicDetailsError("name")

    if not (details.surname and details.surname.strip()):
        raise errors.BasicDetailsError("surname")

    if details.alias is not None and not details.alias.strip():
        raise errors.BasicDetailsError("alias")

    if details.photo is not None and not details.photo.strip():
        raise errors.BasicDetailsError("photo")

    if not details.birthdate:
        raise errors.BasicDetailsError("birthdate")

    if not details.sex:
        raise errors.BasicDetailsError("sex")

    if not details.genre:
        raise errors.BasicDetailsError("genre")
