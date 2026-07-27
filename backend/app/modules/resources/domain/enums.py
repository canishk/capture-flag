from enum import StrEnum


class ResourceType(StrEnum):
    ARTICLE = "article"
    DOCUMENTATION = "documentation"
    VIDEO = "video"
    PDF = "pdf"
    DOWNLOAD = "download"
    EXTERNAL_TOOL = "external_tool"


class ResourceStatus(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    HIDDEN = "hidden"
    ARCHIVED = "archived"
