from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.hints.application.hint_service import HintService
from app.modules.hints.domain.exceptions import (
    DuplicateHintOrderError,
    HintNotFoundError,
    InvalidHintConfigurationError,
)
from app.modules.hints.schemas.requests import (
    CreateHintRequest,
    ReorderHintRequest,
    UpdateHintRequest,
)
from app.modules.hints.schemas.responses import HintResponse
from app.shared.database.dependencies import DbSession
from app.shared.exceptions.base import ConflictError, NotFoundError, ValidationAppError
from app.shared.schemas.response import PaginatedResponse, PaginationMeta, SuccessResponse
from app.shared.security.dependencies import (
    CurrentUserContext,
    get_optional_current_user,
    require_admin,
)

router = APIRouter(prefix="/hints", tags=["Hints"])


def _is_admin(user: CurrentUserContext | None) -> bool:
    return user is not None and user.is_admin


@router.get(
    "/challenge/{challenge_id}",
    response_model=PaginatedResponse[HintResponse],
    summary="List hints for challenge",
)
async def list_hints_for_challenge(
    challenge_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: CurrentUserContext | None = Depends(get_optional_current_user),
    session: AsyncSession = Depends(DbSession),
) -> PaginatedResponse[HintResponse]:
    service = HintService(session)
    try:
        hints, total = await service.list_hints_for_challenge(
            challenge_id,
            page=page,
            page_size=page_size,
            include_non_published=_is_admin(current_user),
        )
    except InvalidHintConfigurationError as exc:
        raise NotFoundError(code="CHALLENGE_NOT_FOUND", message=exc.message) from exc
    total_pages = (total + page_size - 1) // page_size if total else 0
    return PaginatedResponse(
        data=[HintResponse.from_entity(h) for h in hints],
        meta=PaginationMeta(
            page=page,
            page_size=page_size,
            total_items=total,
            total_pages=total_pages,
        ),
    )


@router.get("/{hint_id}", response_model=SuccessResponse[HintResponse], summary="Get hint")
async def get_hint(
    hint_id: UUID,
    current_user: CurrentUserContext | None = Depends(get_optional_current_user),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[HintResponse]:
    service = HintService(session)
    try:
        hint = await service.get_hint(hint_id, include_non_published=_is_admin(current_user))
    except HintNotFoundError as exc:
        raise NotFoundError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(data=HintResponse.from_entity(hint))


@router.post(
    "",
    response_model=SuccessResponse[HintResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create hint",
)
async def create_hint(
    body: CreateHintRequest,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[HintResponse]:
    service = HintService(session)
    try:
        hint = await service.create_hint(
            actor_id=admin.user_id,
            challenge_id=body.challenge_id,
            title=body.title,
            content=body.content,
            display_order=body.display_order,
            penalty_config=body.penalty_config,
            unlock_config=body.unlock_config,
        )
    except DuplicateHintOrderError as exc:
        raise ConflictError(code=exc.code, message=exc.message) from exc
    except InvalidHintConfigurationError as exc:
        raise ValidationAppError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(data=HintResponse.from_entity(hint))


@router.patch("/{hint_id}", response_model=SuccessResponse[HintResponse], summary="Update hint")
async def update_hint(
    hint_id: UUID,
    body: UpdateHintRequest,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[HintResponse]:
    service = HintService(session)
    try:
        hint = await service.update_hint(
            actor_id=admin.user_id,
            hint_id=hint_id,
            title=body.title,
            content=body.content,
            penalty_config=body.penalty_config,
            unlock_config=body.unlock_config,
        )
    except HintNotFoundError as exc:
        raise NotFoundError(code=exc.code, message=exc.message) from exc
    except InvalidHintConfigurationError as exc:
        raise ValidationAppError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(data=HintResponse.from_entity(hint))


@router.delete("/{hint_id}", response_model=SuccessResponse[HintResponse], summary="Hide hint")
async def hide_hint(
    hint_id: UUID,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[HintResponse]:
    service = HintService(session)
    try:
        hint = await service.hide_hint(actor_id=admin.user_id, hint_id=hint_id)
    except HintNotFoundError as exc:
        raise NotFoundError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(data=HintResponse.from_entity(hint))


@router.post(
    "/{hint_id}/publish",
    response_model=SuccessResponse[HintResponse],
    summary="Publish hint",
)
async def publish_hint(
    hint_id: UUID,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[HintResponse]:
    service = HintService(session)
    try:
        hint = await service.publish_hint(actor_id=admin.user_id, hint_id=hint_id)
    except HintNotFoundError as exc:
        raise NotFoundError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(data=HintResponse.from_entity(hint))


@router.patch(
    "/challenge/{challenge_id}/order",
    response_model=SuccessResponse[HintResponse],
    summary="Reorder hint within challenge",
)
async def reorder_hint(
    challenge_id: UUID,
    body: ReorderHintRequest,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[HintResponse]:
    service = HintService(session)
    try:
        hint = await service.reorder_hint(
            actor_id=admin.user_id,
            challenge_id=challenge_id,
            hint_id=body.hint_id,
            display_order=body.display_order,
        )
    except HintNotFoundError as exc:
        raise NotFoundError(code=exc.code, message=exc.message) from exc
    except DuplicateHintOrderError as exc:
        raise ConflictError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(data=HintResponse.from_entity(hint))
