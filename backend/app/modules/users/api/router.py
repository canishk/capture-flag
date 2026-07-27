from uuid import UUID

from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.application.user_service import UserService
from app.modules.users.domain.enums import UserRole, UserStatus
from app.modules.users.domain.exceptions import UserNotFoundError
from app.modules.users.schemas.requests import AdminUpdateUserRequest, UpdateProfileRequest
from app.modules.users.schemas.responses import PublicUserResponse, UserResponse
from app.shared.database.dependencies import DbSession
from app.shared.exceptions.base import NotFoundError, ValidationAppError
from app.shared.schemas.response import PaginatedResponse, PaginationMeta, SuccessResponse
from app.shared.security.dependencies import CurrentUserContext, get_current_user, require_admin
from app.shared.storage.local import LocalStorageService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=SuccessResponse[UserResponse], summary="Get current user profile")
async def get_me(
    current_user: CurrentUserContext = Depends(get_current_user),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[UserResponse]:
    user = await UserService(session).get_profile(current_user.user_id)
    return SuccessResponse(data=UserResponse.from_entity(user))


@router.patch("/me", response_model=SuccessResponse[UserResponse], summary="Update current user profile")
async def update_me(
    body: UpdateProfileRequest,
    current_user: CurrentUserContext = Depends(get_current_user),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[UserResponse]:
    user = await UserService(session).update_profile(
        current_user.user_id,
        display_name=body.display_name,
        preferences=body.preferences,
    )
    return SuccessResponse(data=UserResponse.from_entity(user))


@router.post("/me/avatar", response_model=SuccessResponse[UserResponse], summary="Upload avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: CurrentUserContext = Depends(get_current_user),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[UserResponse]:
    if file.content_type is None:
        raise ValidationAppError(
            message="Invalid avatar file type",
            details={"avatar": ["Content type is required"]},
        )
    content = await file.read()
    storage = LocalStorageService()
    user_service = UserService(session)
    existing = await user_service.get_profile(current_user.user_id)
    storage.delete_avatar(existing.avatar_url)
    avatar_url = storage.save_avatar(
        user_id=current_user.user_id,
        filename=file.filename or "avatar",
        content=content,
        content_type=file.content_type,
    )
    user = await user_service.set_avatar(current_user.user_id, avatar_url)
    return SuccessResponse(data=UserResponse.from_entity(user))


@router.delete("/me/avatar", response_model=SuccessResponse[UserResponse], summary="Delete avatar")
async def delete_avatar(
    current_user: CurrentUserContext = Depends(get_current_user),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[UserResponse]:
    user_service = UserService(session)
    existing = await user_service.get_profile(current_user.user_id)
    LocalStorageService().delete_avatar(existing.avatar_url)
    user = await user_service.clear_avatar(current_user.user_id)
    return SuccessResponse(data=UserResponse.from_entity(user))


@router.get("", response_model=PaginatedResponse[UserResponse], summary="List users (admin)")
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    _admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> PaginatedResponse[UserResponse]:
    users, total = await UserService(session).list_users(
        page=page,
        page_size=page_size,
        search=search,
    )
    total_pages = (total + page_size - 1) // page_size if total else 0
    return PaginatedResponse(
        data=[UserResponse.from_entity(user) for user in users],
        meta=PaginationMeta(
            page=page,
            page_size=page_size,
            total_items=total,
            total_pages=total_pages,
        ),
    )


@router.get("/{user_id}", response_model=SuccessResponse[PublicUserResponse], summary="Get public profile")
async def get_user(
    user_id: UUID,
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[PublicUserResponse]:
    try:
        user = await UserService(session).get_profile(user_id)
    except UserNotFoundError as exc:
        raise NotFoundError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(data=PublicUserResponse.from_entity(user))


@router.patch("/{user_id}", response_model=SuccessResponse[UserResponse], summary="Admin update user")
async def admin_update_user(
    user_id: UUID,
    body: AdminUpdateUserRequest,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[UserResponse]:
    role = UserRole(body.role) if body.role else None
    status_value = UserStatus(body.status) if body.status else None
    user = await UserService(session).update_user_admin(
        actor_id=admin.user_id,
        user_id=user_id,
        role=role,
        status=status_value,
    )
    return SuccessResponse(data=UserResponse.from_entity(user))


@router.post("/{user_id}/disable", response_model=SuccessResponse[UserResponse], summary="Disable user")
async def disable_user(
    user_id: UUID,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[UserResponse]:
    user = await UserService(session).update_user_admin(
        actor_id=admin.user_id,
        user_id=user_id,
        status=UserStatus.DISABLED,
    )
    return SuccessResponse(data=UserResponse.from_entity(user))


@router.post("/{user_id}/enable", response_model=SuccessResponse[UserResponse], summary="Enable user")
async def enable_user(
    user_id: UUID,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[UserResponse]:
    user = await UserService(session).update_user_admin(
        actor_id=admin.user_id,
        user_id=user_id,
        status=UserStatus.ACTIVE,
    )
    return SuccessResponse(data=UserResponse.from_entity(user))
