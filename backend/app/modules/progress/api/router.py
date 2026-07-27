from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.progress.application.progress_service import ProgressProjectionService
from app.modules.progress.schemas.responses import LearnerProgressResponse, ProgressSummaryResponse
from app.shared.database.dependencies import DbSession
from app.shared.schemas.response import SuccessResponse
from app.shared.security.dependencies import CurrentUserContext, get_current_user

router = APIRouter(prefix="/progress", tags=["Progress"])


@router.get("/me", response_model=SuccessResponse[LearnerProgressResponse], summary="Get my progress")
async def get_my_progress(
    current_user: CurrentUserContext = Depends(get_current_user),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[LearnerProgressResponse]:
    service = ProgressProjectionService(session)
    progress = await service.get_my_progress(current_user.user_id)
    return SuccessResponse(data=LearnerProgressResponse.from_entity(progress))


@router.get("/summary", response_model=SuccessResponse[ProgressSummaryResponse], summary="Get progress summary")
async def get_progress_summary(
    current_user: CurrentUserContext = Depends(get_current_user),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[ProgressSummaryResponse]:
    service = ProgressProjectionService(session)
    summary = await service.get_summary(current_user.user_id)
    return SuccessResponse(data=ProgressSummaryResponse.from_entity(summary))
