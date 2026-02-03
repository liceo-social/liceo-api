import logging

from fastapi import Request
from fastapi.responses import JSONResponse, Response

from liceo.infra.domain.error import I18Error


def liceo_handler(request: Request, exc: I18Error) -> Response:
    """
    handles all LiceoError instances
    """
    logging.getLogger("exceptions").error(exc, exc_info=exc)
    return JSONResponse(
        status_code=400,
        content={"code": exc.code, "message": exc.message},
    )
