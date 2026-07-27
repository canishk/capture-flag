from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.levels.application.level_service import LevelService
from app.modules.levels.domain.exceptions import LevelNotFoundError
from app.modules.levels.schemas.requests import (
    CreateLevelRequest,
    ReorderLevelRequest,
    UpdateLevelRequest,
)
from app.modules.levels.schemas.responses import LevelResponse
from app.shared.database.dependencies import DbSession
from app.shared.exceptions.base import NotFoundError
from app.shared.schemas.response import PaginatedResponse, PaginationMeta, SuccessResponse
from app.shared.security.dependencies import CurrentUserContext, get_optional_current_user, require_admin

router = APIRouter(prefix="/levels", tags=["Levels"])


def _is_admin(user: CurrentUserContext | None) -> bool:
    return user is not None and user.is_admin


@router.get("", response_model=PaginatedResponse[LevelResponse], summary="List levels")
async def list_levels(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category_id: UUID | None = Query(None),
    current_user: CurrentUserContext | None = Depends(get_optional_current_user),
    session: AsyncSession = Depends(DbSession),
) -> PaginatedResponse[LevelResponse]:
    service = LevelService(session)
    levels, total = await service.list_levels(
        page=page,
        page_size=page_size,
        include_hidden=_is_admin(current_user),
        category_id=category_id,
    )
    total_pages = (total + page_size - 1) // page_size if total else 0
    return PaginatedResponse(
        data=[LevelResponse.from_entity(level) for level in levels],
        meta=PaginationMeta(
            page=page,
            page_size=page_size,
            total_items=total,
            total_pages=total_pages,
        ),
    )


@router.get("/{level_id}", response_model=SuccessResponse[LevelResponse], summary="Get level")
async def get_level(
    level_id: UUID,
    current_user: CurrentUserContext | None = Depends(get_optional_current_user),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[LevelResponse]:
    service = LevelService(session)
    try:
        level = await service.get_level(level_id, include_hidden=_is_admin(current_user))
    except LevelNotFoundError as exc:
        raise NotFoundError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(data=LevelResponse.from_entity(level))


@router.post(
    "",
    response_model=SuccessResponse[LevelResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create level",
)
async def create_level(
    body: CreateLevelRequest,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[LevelResponse]:
    service = LevelService(session)
    level = await service.create_level(
        actor_id=admin.user_id,
        category_id=body.category_id,
        name=body.name,
        description=body.description,
        display_order=body.display_order,
        unlock_config=body.unlock_config,
    )
    return SuccessResponse(data=LevelResponse.from_entity(level))


@router.patch("/{level_id}", response_model=SuccessResponse[LevelResponse], summary="Update level")
async def update_level(
    level_id: UUID,
    body: UpdateLevelRequest,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[LevelResponse]:
    service = LevelService(session)
    level = await service.update_level(
        actor_id=admin.user_id,
        level_id=level_id,
        name=body.name,
        description=body.description,
        unlock_config=body.unlock_config,
    )
    return SuccessResponse(data=LevelResponse.from_entity(level))


@router.delete("/{level_id}", response_model=SuccessResponse[LevelResponse], summary="Hide level")
async def hide_level(
    level_id: UUID,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[LevelResponse]:
    service = LevelService(session)
    level = await service.hide_level(actor_id=admin.user_id, level_id=level_id)
    return SuccessResponse(data=LevelResponse.from_entity(level))


@router.post(
    "/{level_id}/restore",
    response_model=SuccessResponse[LevelResponse],
    summary="Restore hidden level",
)
async def restore_level(
    level_id: UUID,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[LevelResponse]:
    service = LevelService(session)
    level = await service.restore_level(actor_id=admin.user_id, level_id=level_id)
    return SuccessResponse(data=LevelResponse.from_entity(level))


@router.patch(
    "/{level_id}/order",
    response_model=SuccessResponse[LevelResponse],
    summary="Reorder level",
)
async def reorder_level(
    level_id: UUID,
    body: ReorderLevelRequest,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[LevelResponse]:
    service = LevelService(session)
    level = await service.reorder_level(
        actor_id=admin.user_id,
        level_id=level_id,
        display_order=body.display_order,
    )
    return SuccessResponse(data=LevelResponse.from_entity(level))
