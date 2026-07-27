from fastapi import APIRouter

from app.shared.database.session import check_database_connection
from app.shared.schemas.response import ApiModel, SuccessResponse

router = APIRouter(tags=["Health"])


class HealthStatus(ApiModel):
    status: str
    database: str


class ReadyStatus(ApiModel):
    ready: bool
    database: bool


@router.get("/health", response_model=SuccessResponse[HealthStatus], summary="Health check")
async def health() -> SuccessResponse[HealthStatus]:
    db_ok = await check_database_connection()
    return SuccessResponse(
        data=HealthStatus(
            status="healthy" if db_ok else "degraded",
            database="up" if db_ok else "down",
        )
    )


@router.get("/live", summary="Liveness probe")
async def live() -> dict[str, str]:
    return {"status": "alive"}


@router.get("/ready", response_model=SuccessResponse[ReadyStatus], summary="Readiness probe")
async def ready() -> SuccessResponse[ReadyStatus]:
    db_ok = await check_database_connection()
    return SuccessResponse(
        data=ReadyStatus(
            ready=db_ok,
            database=db_ok,
        )
    )
