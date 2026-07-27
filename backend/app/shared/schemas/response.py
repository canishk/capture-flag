from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

T = TypeVar("T")


class ApiModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class ErrorBody(ApiModel):
    code: str
    message: str
    details: dict[str, Any] = Field(default_factory=dict)


class ErrorResponse(ApiModel):
    success: bool = False
    error: ErrorBody


class SuccessResponse(ApiModel, Generic[T]):
    success: bool = True
    data: T
    meta: dict[str, Any] | None = None


class PaginationMeta(ApiModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int


class PaginatedResponse(ApiModel, Generic[T]):
    success: bool = True
    data: list[T]
    meta: PaginationMeta
