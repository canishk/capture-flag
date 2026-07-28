from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.trophies.application.trophy_service import TrophyService
from app.modules.trophies.domain.exceptions import DuplicateTrophyCodeError, TrophyNotFoundError
from app.modules.trophies.schemas.requests import CreateTrophyRequest
from app.modules.trophies.schemas.responses import TrophyAwardResponse, TrophyDefinitionResponse
from app.shared.database.dependencies import DbSession
from app.shared.exceptions.base import ConflictError, NotFoundError
from app.shared.schemas.response import PaginatedResponse, PaginationMeta, SuccessResponse
from app.shared.security.dependencies import (
    CurrentUserContext,
    get_current_user,
    require_admin,
)

router = APIRouter(prefix="/trophies", tags=["Trophies"])


@router.get("", response_model=PaginatedResponse[TrophyDefinitionResponse], summary="List trophies")
async def list_trophies(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(DbSession),
) -> PaginatedResponse[TrophyDefinitionResponse]:
    service = TrophyService(session)
    trophies, total = await service.list_definitions(page=page, page_size=page_size, active_only=True)
    total_pages = (total + page_size - 1) // page_size if total else 0
    return PaginatedResponse(
        data=[TrophyDefinitionResponse.from_entity(t) for t in trophies],
        meta=PaginationMeta(page=page, page_size=page_size, total_items=total, total_pages=total_pages),
    )


@router.get("/me", response_model=PaginatedResponse[TrophyAwardResponse], summary="List my trophies")
async def list_my_trophies(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: CurrentUserContext = Depends(get_current_user),
    session: AsyncSession = Depends(DbSession),
) -> PaginatedResponse[TrophyAwardResponse]:
    service = TrophyService(session)
    awards, total = await service.list_my_awards(
        current_user.user_id, page=page, page_size=page_size
    )
    total_pages = (total + page_size - 1) // page_size if total else 0
    return PaginatedResponse(
        data=[TrophyAwardResponse.from_entities(a, t) for a, t in awards],
        meta=PaginationMeta(page=page, page_size=page_size, total_items=total, total_pages=total_pages),
    )


@router.get("/{trophy_id}", response_model=SuccessResponse[TrophyDefinitionResponse], summary="Get trophy")
async def get_trophy(
    trophy_id: UUID,
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[TrophyDefinitionResponse]:
    service = TrophyService(session)
    try:
        trophy = await service.get_definition(trophy_id)
    except TrophyNotFoundError as exc:
        raise NotFoundError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(data=TrophyDefinitionResponse.from_entity(trophy))


@router.post(
    "",
    response_model=SuccessResponse[TrophyDefinitionResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create trophy definition",
)
async def create_trophy(
    body: CreateTrophyRequest,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[TrophyDefinitionResponse]:
    service = TrophyService(session)
    try:
        trophy = await service.create_definition(
            actor_id=admin.user_id,
            code=body.code,
            name=body.name,
            description=body.description,
            icon=body.icon,
            trigger_type=body.trigger_type,
            criteria=body.criteria,
            is_repeatable=body.is_repeatable,
        )
    except DuplicateTrophyCodeError as exc:
        raise ConflictError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(data=TrophyDefinitionResponse.from_entity(trophy))
