from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.leaderboards.application.leaderboard_service import LeaderboardService
from app.modules.leaderboards.domain.enums import LeaderboardPeriod
from app.modules.leaderboards.schemas.responses import LeaderboardEntryResponse
from app.shared.database.dependencies import DbSession
from app.shared.schemas.response import PaginatedResponse, PaginationMeta, SuccessResponse
from app.shared.security.dependencies import CurrentUserContext, get_current_user

router = APIRouter(prefix="/leaderboards", tags=["Leaderboards"])


@router.get("", response_model=PaginatedResponse[LeaderboardEntryResponse], summary="Get leaderboard")
async def get_leaderboard(
    period: LeaderboardPeriod = Query(LeaderboardPeriod.ALL_TIME),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(DbSession),
) -> PaginatedResponse[LeaderboardEntryResponse]:
    service = LeaderboardService(session)
    entries, total = await service.get_rankings(period, page=page, page_size=page_size)
    total_pages = (total + page_size - 1) // page_size if total else 0
    return PaginatedResponse(
        data=[LeaderboardEntryResponse.from_entity(e) for e in entries],
        meta=PaginationMeta(page=page, page_size=page_size, total_items=total, total_pages=total_pages),
    )


@router.get("/me", response_model=SuccessResponse[LeaderboardEntryResponse | None], summary="Get my rank")
async def get_my_rank(
    period: LeaderboardPeriod = Query(LeaderboardPeriod.ALL_TIME),
    current_user: CurrentUserContext = Depends(get_current_user),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[LeaderboardEntryResponse | None]:
    service = LeaderboardService(session)
    entry = await service.get_my_ranking(current_user.user_id, period)
    data = LeaderboardEntryResponse.from_entity(entry) if entry else None
    return SuccessResponse(data=data)
