from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.authentication.application.auth_service import AuthService
from app.modules.authentication.schemas.requests import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    LoginRequest,
    LogoutRequest,
    RefreshRequest,
    RegisterRequest,
    ResetPasswordRequest,
    VerifyEmailRequest,
)
from app.modules.authentication.schemas.responses import (
    MessageResponse,
    RegisterResponse,
    SessionUserResponse,
    TokenResponse,
)
from app.modules.users.application.user_service import UserService
from app.shared.database.dependencies import DbSession
from app.shared.schemas.response import SuccessResponse
from app.shared.security.dependencies import CurrentUserContext, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


def _token_response(token_pair) -> TokenResponse:
    return TokenResponse(
        access_token=token_pair.access_token,
        refresh_token=token_pair.refresh_token,
        token_type=token_pair.token_type,
        expires_in=token_pair.expires_in,
    )


@router.post(
    "/register",
    response_model=SuccessResponse[RegisterResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Register a new account",
)
async def register(
    body: RegisterRequest,
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[RegisterResponse]:
    service = AuthService(session)
    user_id, tokens, verification_token = await service.register(
        email=body.email,
        password=body.password,
        display_name=body.display_name,
    )
    return SuccessResponse(
        data=RegisterResponse(
            user_id=user_id,
            verification_required=verification_token is not None,
            tokens=_token_response(tokens) if tokens else None,
            verification_token=verification_token,
        )
    )


@router.post("/login", response_model=SuccessResponse[TokenResponse], summary="Login")
async def login(
    body: LoginRequest,
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[TokenResponse]:
    service = AuthService(session)
    tokens = await service.login(email=body.email, password=body.password)
    return SuccessResponse(data=_token_response(tokens))


@router.post("/logout", response_model=SuccessResponse[MessageResponse], summary="Logout")
async def logout(
    body: LogoutRequest,
    current_user: CurrentUserContext = Depends(get_current_user),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[MessageResponse]:
    service = AuthService(session)
    await service.logout(user_id=current_user.user_id, refresh_token=body.refresh_token)
    return SuccessResponse(data=MessageResponse(message="Logged out successfully"))


@router.post("/refresh", response_model=SuccessResponse[TokenResponse], summary="Refresh tokens")
async def refresh(
    body: RefreshRequest,
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[TokenResponse]:
    service = AuthService(session)
    tokens = await service.refresh(refresh_token=body.refresh_token)
    return SuccessResponse(data=_token_response(tokens))


@router.post(
    "/forgot-password",
    response_model=SuccessResponse[MessageResponse],
    summary="Request password reset",
)
async def forgot_password(
    body: ForgotPasswordRequest,
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[MessageResponse]:
    service = AuthService(session)
    await service.request_password_reset(email=body.email)
    return SuccessResponse(
        data=MessageResponse(
            message="If the email exists, a password reset link has been sent"
        )
    )


@router.post(
    "/reset-password",
    response_model=SuccessResponse[MessageResponse],
    summary="Reset password",
)
async def reset_password(
    body: ResetPasswordRequest,
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[MessageResponse]:
    service = AuthService(session)
    await service.reset_password(token=body.token, new_password=body.new_password)
    return SuccessResponse(data=MessageResponse(message="Password reset successfully"))


@router.post(
    "/change-password",
    response_model=SuccessResponse[MessageResponse],
    summary="Change password",
)
async def change_password(
    body: ChangePasswordRequest,
    current_user: CurrentUserContext = Depends(get_current_user),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[MessageResponse]:
    service = AuthService(session)
    await service.change_password(
        user_id=current_user.user_id,
        current_password=body.current_password,
        new_password=body.new_password,
    )
    return SuccessResponse(data=MessageResponse(message="Password changed successfully"))


@router.post(
    "/verify-email",
    response_model=SuccessResponse[MessageResponse],
    summary="Verify email address",
)
async def verify_email(
    body: VerifyEmailRequest,
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[MessageResponse]:
    service = AuthService(session)
    await service.verify_email(token=body.token)
    return SuccessResponse(data=MessageResponse(message="Email verified successfully"))


@router.get("/me", response_model=SuccessResponse[SessionUserResponse], summary="Current session")
async def me(
    current_user: CurrentUserContext = Depends(get_current_user),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[SessionUserResponse]:
    user = await UserService(session).get_profile(current_user.user_id)
    return SuccessResponse(
        data=SessionUserResponse(
            user_id=user.id,
            email=user.email,
            display_name=user.display_name,
            role=user.role.value,
            status=user.status.value,
        )
    )
