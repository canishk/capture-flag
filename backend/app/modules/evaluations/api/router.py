from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.evaluations.application.evaluation_service import EvaluationService
from app.modules.evaluations.domain.exceptions import (
    EvaluationConfigurationError,
    EvaluationNotFoundError,
    UnsupportedEvaluationStrategyError,
)
from app.modules.evaluations.schemas.requests import PreviewEvaluationRequest
from app.modules.evaluations.schemas.responses import EvaluationResponse, PreviewEvaluationResponse
from app.shared.database.dependencies import DbSession
from app.shared.exceptions.base import NotFoundError, ValidationAppError
from app.shared.schemas.response import SuccessResponse
from app.shared.security.dependencies import CurrentUserContext, require_admin

router = APIRouter(prefix="/evaluations", tags=["Evaluations"])


@router.get("/strategies", response_model=SuccessResponse[list[str]], summary="List evaluation strategies")
async def list_strategies(
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[list[str]]:
    service = EvaluationService(session)
    return SuccessResponse(data=service.list_strategies())


@router.post("/preview", response_model=SuccessResponse[PreviewEvaluationResponse], summary="Preview evaluation")
async def preview_evaluation(
    body: PreviewEvaluationRequest,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[PreviewEvaluationResponse]:
    service = EvaluationService(session)
    try:
        result = await service.preview_evaluation(
            body.answer, body.evaluation_strategy, body.base_score
        )
    except (UnsupportedEvaluationStrategyError, EvaluationConfigurationError) as exc:
        raise ValidationAppError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(data=PreviewEvaluationResponse.from_result(result))


@router.get(
    "/submission/{submission_id}",
    response_model=SuccessResponse[EvaluationResponse],
    summary="Get evaluation for submission",
)
async def get_evaluation_for_submission(
    submission_id: UUID,
    admin: CurrentUserContext = Depends(require_admin),
    session: AsyncSession = Depends(DbSession),
) -> SuccessResponse[EvaluationResponse]:
    service = EvaluationService(session)
    try:
        evaluation = await service.get_evaluation_by_submission(submission_id)
    except EvaluationNotFoundError as exc:
        raise NotFoundError(code=exc.code, message=exc.message) from exc
    return SuccessResponse(data=EvaluationResponse.from_entity(evaluation))
