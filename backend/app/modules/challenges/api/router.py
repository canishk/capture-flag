from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.challenges.application.challenge_service import ChallengeService
from app.modules.challenges.domain.exceptions import (
    ChallengeNotFoundError,
    DuplicateChallengeTitleError,
    InvalidChallengeConfigurationError,
    InvalidChallengeStatusTransitionError,
)
from app.modules.challenges.schemas.requests import (
    CreateChallengeRequest,
    ReorderChallengeRequest,
    UpdateChallengeRequest,
)
from app.modules.challenges.schemas.responses import ChallengeResponse
from app.shared.database.dependencies import DbSession
from app.shared.exceptions.base import ConflictError, NotFoundError, ValidationAppError
from app.shared.schemas.response import PaginatedResponse, PaginationMeta, SuccessResponse
from app.shared.security.dependencies import CurrentUserContext, get_optional_current_user, require_admin

router = APIRouter(prefix="/challenges", tags=["Challenges"])


def _is_admin(user: CurrentUserContext | None) -> bool:
    return user is not None and user.is_admin


@router.get("", response_model=PaginatedResponse[ChallengeResponse], summary="List challenges")
async def list_challenges(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category_id: UUID | None = Query(None),
    level_id: UUID | None = Query(None),
    search: str | None = Query(None),
    current_user: CurrentUserContext | None = Depends(get_optional_current_user),
    session: AsyncSession = Depends(DbSession),
) -> PaginatedResponse[ChallengeResponse]:
    service = ChallengeService(session)
    challenges, total = await service.list_challenges(
        page=page,
        page_size=page_size,
        include_non_published=_is_admin(current_user),
        category_id=category_id,
        level_id=level_id,
        search=search,
    )
    total_pages = (total + page_size - 1) // page_size if total else 0
    return PaginatedResponse(
        data=[ChallengeResponse.from_entity(c, include_sensitive=_is_admin(current_user)) for c in challenges],
        meta=PaginationMeta(
            page=page,
            page_size=page_size,
            total_items=total,
            total_pages=total_pages,
        ),
    )


@router.get("/{challenge_id}", response_model=SuccessResponse[ChallengeResponse], summary="Get challenge")
async def get_challenge(
    challenge_id: UUID,
    current_user: CurrentUserContext | None = Depends(get_optional_current_user),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[ChallengeResponse]:
    service = ChallengeService(session)
    try:
        challenge = await service.get_challenge(
            challenge_id, include_non_published=_is_admin(current_user)
        )
    except ChallengeNotFoundError as exc:
        raise NotFoundError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(
        data=ChallengeResponse.from_entity(challenge, include_sensitive=True)
    )


@router.post(
    "",
    response_model=SuccessResponse[ChallengeResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create challenge",
)
async def create_challenge(
    body: CreateChallengeRequest,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[ChallengeResponse]:
    service = ChallengeService(session)
    try:
        challenge = await service.create_challenge(
            actor_id=admin.user_id,
            category_id=body.category_id,
            level_id=body.level_id,
            title=body.title,
            summary=body.summary,
            description=body.description,
            objectives=body.objectives,
            challenge_type=body.challenge_type,
            difficulty=body.difficulty,
            estimated_duration_minutes=body.estimated_duration_minutes,
            base_score=body.base_score,
            evaluation_strategy=body.evaluation_strategy,
            scoring_config=body.scoring_config,
            unlock_config=body.unlock_config,
            is_required=body.is_required,
            display_order=body.display_order,
        )
    except DuplicateChallengeTitleError as exc:
        raise ConflictError(code=exc.code, message=exc.message) from exc
    except InvalidChallengeConfigurationError as exc:
        raise ValidationAppError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(
        data=ChallengeResponse.from_entity(challenge, include_sensitive=True)
    )


@router.patch(
    "/{challenge_id}",
    response_model=SuccessResponse[ChallengeResponse],
    summary="Update challenge",
)
async def update_challenge(
    challenge_id: UUID,
    body: UpdateChallengeRequest,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[ChallengeResponse]:
    service = ChallengeService(session)
    try:
        challenge = await service.update_challenge(
            actor_id=admin.user_id,
            challenge_id=challenge_id,
            title=body.title,
            summary=body.summary,
            description=body.description,
            objectives=body.objectives,
            challenge_type=body.challenge_type,
            difficulty=body.difficulty,
            estimated_duration_minutes=body.estimated_duration_minutes,
            base_score=body.base_score,
            evaluation_strategy=body.evaluation_strategy,
            scoring_config=body.scoring_config,
            unlock_config=body.unlock_config,
            is_required=body.is_required,
        )
    except ChallengeNotFoundError as exc:
        raise NotFoundError(code=exc.code, message=exc.message) from exc
    except DuplicateChallengeTitleError as exc:
        raise ConflictError(code=exc.code, message=exc.message) from exc
    except InvalidChallengeConfigurationError as exc:
        raise ValidationAppError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(
        data=ChallengeResponse.from_entity(challenge, include_sensitive=True)
    )


@router.delete(
    "/{challenge_id}",
    response_model=SuccessResponse[ChallengeResponse],
    summary="Hide challenge",
)
async def hide_challenge(
    challenge_id: UUID,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[ChallengeResponse]:
    service = ChallengeService(session)
    try:
        challenge = await service.hide_challenge(actor_id=admin.user_id, challenge_id=challenge_id)
    except ChallengeNotFoundError as exc:
        raise NotFoundError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(
        data=ChallengeResponse.from_entity(challenge, include_sensitive=True)
    )


@router.post(
    "/{challenge_id}/publish",
    response_model=SuccessResponse[ChallengeResponse],
    summary="Publish challenge",
)
async def publish_challenge(
    challenge_id: UUID,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[ChallengeResponse]:
    service = ChallengeService(session)
    try:
        challenge = await service.publish_challenge(
            actor_id=admin.user_id, challenge_id=challenge_id
        )
    except ChallengeNotFoundError as exc:
        raise NotFoundError(code=exc.code, message=exc.message) from exc
    except InvalidChallengeStatusTransitionError as exc:
        raise ValidationAppError(code=exc.code, message=exc.message) from exc
    except InvalidChallengeConfigurationError as exc:
        raise ValidationAppError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(
        data=ChallengeResponse.from_entity(challenge, include_sensitive=True)
    )


@router.post(
    "/{challenge_id}/archive",
    response_model=SuccessResponse[ChallengeResponse],
    summary="Archive challenge",
)
async def archive_challenge(
    challenge_id: UUID,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[ChallengeResponse]:
    service = ChallengeService(session)
    try:
        challenge = await service.archive_challenge(
            actor_id=admin.user_id, challenge_id=challenge_id
        )
    except ChallengeNotFoundError as exc:
        raise NotFoundError(code=exc.code, message=exc.message) from exc
    except InvalidChallengeStatusTransitionError as exc:
        raise ValidationAppError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(
        data=ChallengeResponse.from_entity(challenge, include_sensitive=True)
    )


@router.patch(
    "/{challenge_id}/order",
    response_model=SuccessResponse[ChallengeResponse],
    summary="Reorder challenge",
)
async def reorder_challenge(
    challenge_id: UUID,
    body: ReorderChallengeRequest,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[ChallengeResponse]:
    service = ChallengeService(session)
    try:
        challenge = await service.reorder_challenge(
            actor_id=admin.user_id,
            challenge_id=challenge_id,
            display_order=body.display_order,
        )
    except ChallengeNotFoundError as exc:
        raise NotFoundError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(
        data=ChallengeResponse.from_entity(challenge, include_sensitive=True)
    )
