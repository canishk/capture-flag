from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.submissions.application.submission_service import SubmissionService
from app.modules.submissions.domain.enums import SubmissionStatus
from app.modules.submissions.domain.exceptions import (
    InvalidSubmissionError,
    SubmissionAccessDeniedError,
    SubmissionNotFoundError,
)
from app.modules.submissions.schemas.requests import CreateSubmissionRequest
from app.modules.submissions.schemas.responses import SubmissionResponse
from app.shared.database.dependencies import DbSession
from app.shared.exceptions.base import ForbiddenError, NotFoundError, ValidationAppError
from app.shared.schemas.response import PaginatedResponse, PaginationMeta, SuccessResponse
from app.shared.security.dependencies import (
    CurrentUserContext,
    get_current_user,
    require_admin,
)

router = APIRouter(prefix="/submissions", tags=["Submissions"])


@router.post(
    "",
    response_model=SuccessResponse[SubmissionResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create submission",
)
async def create_submission(
    body: CreateSubmissionRequest,
    current_user: CurrentUserContext = Depends(get_current_user),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[SubmissionResponse]:
    service = SubmissionService(session)
    try:
        submission = await service.create_submission(
            user_id=current_user.user_id,
            challenge_id=body.challenge_id,
            answer=body.answer,
        )
    except InvalidSubmissionError as exc:
        raise ValidationAppError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(data=SubmissionResponse.from_entity(submission))


@router.get("/me", response_model=PaginatedResponse[SubmissionResponse], summary="List my submissions")
async def list_my_submissions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    challenge_id: UUID | None = Query(None),
    current_user: CurrentUserContext = Depends(get_current_user),
    session: AsyncSession = Depends(DbSession),
) -> PaginatedResponse[SubmissionResponse]:
    service = SubmissionService(session)
    submissions, total = await service.list_my_submissions(
        current_user.user_id,
        page=page,
        page_size=page_size,
        challenge_id=challenge_id,
    )
    total_pages = (total + page_size - 1) // page_size if total else 0
    return PaginatedResponse(
        data=[SubmissionResponse.from_entity(s) for s in submissions],
        meta=PaginationMeta(
            page=page,
            page_size=page_size,
            total_items=total,
            total_pages=total_pages,
        ),
    )


@router.get(
    "/challenge/{challenge_id}",
    response_model=PaginatedResponse[SubmissionResponse],
    summary="List my submissions for challenge",
)
async def list_challenge_submissions(
    challenge_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: CurrentUserContext = Depends(get_current_user),
    session: AsyncSession = Depends(DbSession),
) -> PaginatedResponse[SubmissionResponse]:
    service = SubmissionService(session)
    submissions, total = await service.list_my_submissions(
        current_user.user_id,
        page=page,
        page_size=page_size,
        challenge_id=challenge_id,
    )
    total_pages = (total + page_size - 1) // page_size if total else 0
    return PaginatedResponse(
        data=[SubmissionResponse.from_entity(s) for s in submissions],
        meta=PaginationMeta(
            page=page,
            page_size=page_size,
            total_items=total,
            total_pages=total_pages,
        ),
    )


@router.get("/{submission_id}", response_model=SuccessResponse[SubmissionResponse], summary="Get submission")
async def get_submission(
    submission_id: UUID,
    current_user: CurrentUserContext = Depends(get_current_user),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[SubmissionResponse]:
    service = SubmissionService(session)
    try:
        submission = await service.get_submission(
            submission_id,
            requester_id=current_user.user_id,
            is_admin=current_user.is_admin,
        )
    except SubmissionNotFoundError as exc:
        raise NotFoundError(code=exc.code, message=exc.message) from exc
    except SubmissionAccessDeniedError as exc:
        raise ForbiddenError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(data=SubmissionResponse.from_entity(submission))


@router.get("", response_model=PaginatedResponse[SubmissionResponse], summary="List submissions (admin)")
async def list_submissions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user_id: UUID | None = Query(None),
    challenge_id: UUID | None = Query(None),
    submission_status: SubmissionStatus | None = Query(None, alias="status"),
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> PaginatedResponse[SubmissionResponse]:
    service = SubmissionService(session)
    submissions, total = await service.list_submissions(
        page=page,
        page_size=page_size,
        user_id=user_id,
        challenge_id=challenge_id,
        status=submission_status,
    )
    total_pages = (total + page_size - 1) // page_size if total else 0
    return PaginatedResponse(
        data=[SubmissionResponse.from_entity(s) for s in submissions],
        meta=PaginationMeta(
            page=page,
            page_size=page_size,
            total_items=total,
            total_pages=total_pages,
        ),
    )
