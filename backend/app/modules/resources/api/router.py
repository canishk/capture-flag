from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.resources.application.resource_service import ResourceService
from app.modules.resources.domain.enums import ResourceType
from app.modules.resources.domain.exceptions import (
    InvalidResourceConfigurationError,
    ResourceNotFoundError,
)
from app.modules.resources.schemas.requests import (
    CreateResourceRequest,
    LinkResourceRequest,
    UpdateResourceRequest,
)
from app.modules.resources.schemas.responses import ResourceResponse
from app.shared.database.dependencies import DbSession
from app.shared.exceptions.base import NotFoundError, ValidationAppError
from app.shared.schemas.response import PaginatedResponse, PaginationMeta, SuccessResponse
from app.shared.security.dependencies import (
    CurrentUserContext,
    get_optional_current_user,
    require_admin,
)

router = APIRouter(prefix="/resources", tags=["Resources"])


def _is_admin(user: CurrentUserContext | None) -> bool:
    return user is not None and user.is_admin


@router.get("", response_model=PaginatedResponse[ResourceResponse], summary="List resources")
async def list_resources(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    resource_type: ResourceType | None = Query(None),
    search: str | None = Query(None),
    tag: str | None = Query(None),
    current_user: CurrentUserContext | None = Depends(get_optional_current_user),
    session: AsyncSession = Depends(DbSession),
) -> PaginatedResponse[ResourceResponse]:
    service = ResourceService(session)
    resources, total = await service.list_resources(
        page=page,
        page_size=page_size,
        include_non_published=_is_admin(current_user),
        resource_type=resource_type,
        search=search,
        tag=tag,
    )
    total_pages = (total + page_size - 1) // page_size if total else 0
    return PaginatedResponse(
        data=[ResourceResponse.from_entity(r) for r in resources],
        meta=PaginationMeta(
            page=page,
            page_size=page_size,
            total_items=total,
            total_pages=total_pages,
        ),
    )


@router.get(
    "/challenge/{challenge_id}",
    response_model=PaginatedResponse[ResourceResponse],
    summary="List resources for challenge",
)
async def list_resources_for_challenge(
    challenge_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: CurrentUserContext | None = Depends(get_optional_current_user),
    session: AsyncSession = Depends(DbSession),
) -> PaginatedResponse[ResourceResponse]:
    service = ResourceService(session)
    try:
        resources, total = await service.list_resources_for_challenge(
            challenge_id,
            page=page,
            page_size=page_size,
            include_non_published=_is_admin(current_user),
        )
    except InvalidResourceConfigurationError as exc:
        raise NotFoundError(code="CHALLENGE_NOT_FOUND", message=exc.message) from exc
    total_pages = (total + page_size - 1) // page_size if total else 0
    return PaginatedResponse(
        data=[ResourceResponse.from_entity(r) for r in resources],
        meta=PaginationMeta(
            page=page,
            page_size=page_size,
            total_items=total,
            total_pages=total_pages,
        ),
    )


@router.get("/{resource_id}", response_model=SuccessResponse[ResourceResponse], summary="Get resource")
async def get_resource(
    resource_id: UUID,
    current_user: CurrentUserContext | None = Depends(get_optional_current_user),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[ResourceResponse]:
    service = ResourceService(session)
    try:
        resource = await service.get_resource(
            resource_id, include_non_published=_is_admin(current_user)
        )
    except ResourceNotFoundError as exc:
        raise NotFoundError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(data=ResourceResponse.from_entity(resource))


@router.post(
    "",
    response_model=SuccessResponse[ResourceResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create resource",
)
async def create_resource(
    body: CreateResourceRequest,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[ResourceResponse]:
    service = ResourceService(session)
    try:
        resource = await service.create_resource(
            actor_id=admin.user_id,
            title=body.title,
            summary=body.summary,
            description=body.description,
            resource_type=body.resource_type,
            url=body.url,
            file_path=body.file_path,
            author=body.author,
            source=body.source,
            tags=body.tags,
        )
    except InvalidResourceConfigurationError as exc:
        raise ValidationAppError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(data=ResourceResponse.from_entity(resource))


@router.patch(
    "/{resource_id}",
    response_model=SuccessResponse[ResourceResponse],
    summary="Update resource",
)
async def update_resource(
    resource_id: UUID,
    body: UpdateResourceRequest,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[ResourceResponse]:
    service = ResourceService(session)
    try:
        resource = await service.update_resource(
            actor_id=admin.user_id,
            resource_id=resource_id,
            title=body.title,
            summary=body.summary,
            description=body.description,
            resource_type=body.resource_type,
            url=body.url,
            file_path=body.file_path,
            author=body.author,
            source=body.source,
            tags=body.tags,
        )
    except ResourceNotFoundError as exc:
        raise NotFoundError(code=exc.code, message=exc.message) from exc
    except InvalidResourceConfigurationError as exc:
        raise ValidationAppError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(data=ResourceResponse.from_entity(resource))


@router.delete(
    "/{resource_id}",
    response_model=SuccessResponse[ResourceResponse],
    summary="Hide resource",
)
async def hide_resource(
    resource_id: UUID,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[ResourceResponse]:
    service = ResourceService(session)
    try:
        resource = await service.hide_resource(actor_id=admin.user_id, resource_id=resource_id)
    except ResourceNotFoundError as exc:
        raise NotFoundError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(data=ResourceResponse.from_entity(resource))


@router.post(
    "/{resource_id}/publish",
    response_model=SuccessResponse[ResourceResponse],
    summary="Publish resource",
)
async def publish_resource(
    resource_id: UUID,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[ResourceResponse]:
    service = ResourceService(session)
    try:
        resource = await service.publish_resource(actor_id=admin.user_id, resource_id=resource_id)
    except ResourceNotFoundError as exc:
        raise NotFoundError(code=exc.code, message=exc.message) from exc
    except InvalidResourceConfigurationError as exc:
        raise ValidationAppError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(data=ResourceResponse.from_entity(resource))


@router.post(
    "/{resource_id}/link",
    response_model=SuccessResponse[dict],
    summary="Link resource to challenge",
)
async def link_resource(
    resource_id: UUID,
    body: LinkResourceRequest,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[dict]:
    service = ResourceService(session)
    try:
        await service.link_to_challenge(
            actor_id=admin.user_id,
            resource_id=resource_id,
            challenge_id=body.challenge_id,
        )
    except ResourceNotFoundError as exc:
        raise NotFoundError(code=exc.code, message=exc.message) from exc
    except InvalidResourceConfigurationError as exc:
        raise ValidationAppError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(data={"linked": True})


@router.post(
    "/{resource_id}/unlink",
    response_model=SuccessResponse[dict],
    summary="Unlink resource from challenge",
)
async def unlink_resource(
    resource_id: UUID,
    body: LinkResourceRequest,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[dict]:
    service = ResourceService(session)
    try:
        await service.unlink_from_challenge(
            actor_id=admin.user_id,
            resource_id=resource_id,
            challenge_id=body.challenge_id,
        )
    except ResourceNotFoundError as exc:
        raise NotFoundError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(data={"linked": False})
