from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.achievements.application.achievement_service import AchievementService
from app.modules.achievements.domain.exceptions import (
    AchievementNotFoundError,
    DuplicateAchievementCodeError,
)
from app.modules.achievements.schemas.requests import CreateAchievementRequest
from app.modules.achievements.schemas.responses import (
    AchievementDefinitionResponse,
    UserAchievementResponse,
)
from app.shared.database.dependencies import DbSession
from app.shared.exceptions.base import ConflictError, NotFoundError
from app.shared.schemas.response import PaginatedResponse, PaginationMeta, SuccessResponse
from app.shared.security.dependencies import (
    CurrentUserContext,
    get_current_user,
    get_optional_current_user,
    require_admin,
)

router = APIRouter(prefix="/achievements", tags=["Achievements"])


@router.get("", response_model=PaginatedResponse[AchievementDefinitionResponse], summary="List achievements")
async def list_achievements(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: CurrentUserContext | None = Depends(get_optional_current_user),
    session: AsyncSession = Depends(DbSession),
) -> PaginatedResponse[AchievementDefinitionResponse]:
    service = AchievementService(session)
    include_hidden = current_user is not None and current_user.is_admin
    achievements, total = await service.list_definitions(
        page=page, page_size=page_size, include_hidden=include_hidden
    )
    total_pages = (total + page_size - 1) // page_size if total else 0
    return PaginatedResponse(
        data=[AchievementDefinitionResponse.from_entity(a) for a in achievements],
        meta=PaginationMeta(page=page, page_size=page_size, total_items=total, total_pages=total_pages),
    )


@router.get("/me", response_model=PaginatedResponse[UserAchievementResponse], summary="List my achievements")
async def list_my_achievements(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: CurrentUserContext = Depends(get_current_user),
    session: AsyncSession = Depends(DbSession),
) -> PaginatedResponse[UserAchievementResponse]:
    service = AchievementService(session)
    rows, total = await service.list_my_achievements(
        current_user.user_id, page=page, page_size=page_size
    )
    total_pages = (total + page_size - 1) // page_size if total else 0
    return PaginatedResponse(
        data=[UserAchievementResponse.from_entities(p, a) for p, a in rows],
        meta=PaginationMeta(page=page, page_size=page_size, total_items=total, total_pages=total_pages),
    )


@router.post(
    "",
    response_model=SuccessResponse[AchievementDefinitionResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create achievement",
)
async def create_achievement(
    body: CreateAchievementRequest,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[AchievementDefinitionResponse]:
    service = AchievementService(session)
    try:
        achievement = await service.create_definition(
            actor_id=admin.user_id,
            code=body.code,
            name=body.name,
            description=body.description,
            icon=body.icon,
            criteria_type=body.criteria_type,
            target_count=body.target_count,
            is_hidden=body.is_hidden,
        )
    except DuplicateAchievementCodeError as exc:
        raise ConflictError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(data=AchievementDefinitionResponse.from_entity(achievement))


@router.get(
    "/{achievement_id}",
    response_model=SuccessResponse[AchievementDefinitionResponse],
    summary="Get achievement",
)
async def get_achievement(
    achievement_id: UUID,
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[AchievementDefinitionResponse]:
    service = AchievementService(session)
    try:
        achievement = await service.get_definition(achievement_id)
    except AchievementNotFoundError as exc:
        raise NotFoundError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(data=AchievementDefinitionResponse.from_entity(achievement))
