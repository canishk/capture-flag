from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.shared.exceptions.base import AppError
from app.shared.logging.setup import get_logger
from app.shared.schemas.response import ErrorBody, ErrorResponse

logger = get_logger(__name__)


async def app_error_handler(_request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            success=False,
            error=ErrorBody(code=exc.code, message=exc.message, details=exc.details),
        ).model_dump(by_alias=True),
    )


async def validation_error_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    details: dict[str, Any] = {}
    for error in exc.errors():
        loc = error.get("loc", ())
        field = ".".join(str(part) for part in loc if part != "body")
        details[field or "body"] = [error.get("msg", "Invalid value")]
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            success=False,
            error=ErrorBody(
                code="VALIDATION_ERROR",
                message="Validation failed",
                details=details,
            ),
        ).model_dump(by_alias=True),
    )


async def http_exception_handler(
    _request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            success=False,
            error=ErrorBody(
                code="HTTP_ERROR",
                message=str(exc.detail),
                details={},
            ),
        ).model_dump(by_alias=True),
    )


async def unhandled_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    logger.exception("unhandled exception", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            success=False,
            error=ErrorBody(
                code="INTERNAL_ERROR",
                message="An unexpected error occurred",
                details={},
            ),
        ).model_dump(by_alias=True),
    )
