from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.categories.application.category_service import CategoryService
from app.modules.categories.domain.exceptions import CategoryNotFoundError
from app.modules.categories.schemas.requests import (
    CreateCategoryRequest,
    ReorderCategoryRequest,
    UpdateCategoryRequest,
)
from app.modules.categories.schemas.responses import CategoryResponse
from app.shared.database.dependencies import DbSession
from app.shared.exceptions.base import NotFoundError
from app.shared.schemas.response import PaginatedResponse, PaginationMeta, SuccessResponse
from app.shared.security.dependencies import (
    CurrentUserContext,
    get_optional_current_user,
    require_admin,
)

router = APIRouter(prefix="/categories", tags=["Categories"])


def _is_admin(user: CurrentUserContext | None) -> bool:
    return user is not None and user.is_admin


@router.get("", response_model=PaginatedResponse[CategoryResponse], summary="List categories")
async def list_categories(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    current_user: CurrentUserContext | None = Depends(get_optional_current_user),
    session: AsyncSession = Depends(DbSession),
) -> PaginatedResponse[CategoryResponse]:
    service = CategoryService(session)
    categories, total = await service.list_categories(
        page=page,
        page_size=page_size,
        include_hidden=_is_admin(current_user),
        search=search,
    )
    total_pages = (total + page_size - 1) // page_size if total else 0
    return PaginatedResponse(
        data=[CategoryResponse.from_entity(c) for c in categories],
        meta=PaginationMeta(
            page=page,
            page_size=page_size,
            total_items=total,
            total_pages=total_pages,
        ),
    )


@router.get("/{category_id}", response_model=SuccessResponse[CategoryResponse], summary="Get category")
async def get_category(
    category_id: UUID,
    current_user: CurrentUserContext | None = Depends(get_optional_current_user),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[CategoryResponse]:
    service = CategoryService(session)
    try:
        category = await service.get_category(category_id, include_hidden=_is_admin(current_user))
    except CategoryNotFoundError as exc:
        raise NotFoundError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(data=CategoryResponse.from_entity(category))


@router.post(
    "",
    response_model=SuccessResponse[CategoryResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create category",
)
async def create_category(
    body: CreateCategoryRequest,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[CategoryResponse]:
    service = CategoryService(session)
    category = await service.create_category(
        actor_id=admin.user_id,
        name=body.name,
        description=body.description,
        icon=body.icon,
        display_order=body.display_order,
    )
    return SuccessResponse(data=CategoryResponse.from_entity(category))


@router.patch("/{category_id}", response_model=SuccessResponse[CategoryResponse], summary="Update category")
async def update_category(
    category_id: UUID,
    body: UpdateCategoryRequest,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[CategoryResponse]:
    service = CategoryService(session)
    category = await service.update_category(
        actor_id=admin.user_id,
        category_id=category_id,
        name=body.name,
        description=body.description,
        icon=body.icon,
    )
    return SuccessResponse(data=CategoryResponse.from_entity(category))


@router.delete("/{category_id}", response_model=SuccessResponse[CategoryResponse], summary="Hide category")
async def hide_category(
    category_id: UUID,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[CategoryResponse]:
    service = CategoryService(session)
    category = await service.hide_category(actor_id=admin.user_id, category_id=category_id)
    return SuccessResponse(data=CategoryResponse.from_entity(category))


@router.post(
    "/{category_id}/restore",
    response_model=SuccessResponse[CategoryResponse],
    summary="Restore hidden category",
)
async def restore_category(
    category_id: UUID,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[CategoryResponse]:
    service = CategoryService(session)
    category = await service.restore_category(actor_id=admin.user_id, category_id=category_id)
    return SuccessResponse(data=CategoryResponse.from_entity(category))


@router.patch(
    "/{category_id}/order",
    response_model=SuccessResponse[CategoryResponse],
    summary="Reorder category",
)
async def reorder_category(
    category_id: UUID,
    body: ReorderCategoryRequest,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[CategoryResponse]:
    service = CategoryService(session)
    category = await service.reorder_category(
        actor_id=admin.user_id,
        category_id=category_id,
        display_order=body.display_order,
    )
    return SuccessResponse(data=CategoryResponse.from_entity(category))
