from pydantic import Field

from app.shared.schemas.response import ApiModel


class CreateCategoryRequest(ApiModel):
    name: str = Field(min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=2000)
    icon: str = Field(min_length=1, max_length=120)
    display_order: int | None = Field(default=None, ge=0)


class UpdateCategoryRequest(ApiModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=2000)
    icon: str | None = Field(default=None, min_length=1, max_length=120)


class ReorderCategoryRequest(ApiModel):
    display_order: int = Field(ge=0)
