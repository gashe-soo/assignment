from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status

from app.company.exceptions import NotFoundCompanyException
from app.tag.exceptions import NotFoundTagException


def not_found_tag_handler(
    request: Request, exc: NotFoundTagException
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": exc.message}
    )


def not_found_company_handler(
    request: Request, exc: NotFoundCompanyException
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": exc.message}
    )


exception_handlers = [
    (NotFoundTagException, not_found_tag_handler),
    (NotFoundCompanyException, not_found_company_handler),
]
