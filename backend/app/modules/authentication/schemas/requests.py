from pydantic import EmailStr, Field

from app.shared.schemas.response import ApiModel


class RegisterRequest(ApiModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    display_name: str = Field(min_length=2, max_length=100)


class LoginRequest(ApiModel):
    email: EmailStr
    password: str


class RefreshRequest(ApiModel):
    refresh_token: str


class ForgotPasswordRequest(ApiModel):
    email: EmailStr


class ResetPasswordRequest(ApiModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


class ChangePasswordRequest(ApiModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=128)


class VerifyEmailRequest(ApiModel):
    token: str


class LogoutRequest(ApiModel):
    refresh_token: str | None = None
