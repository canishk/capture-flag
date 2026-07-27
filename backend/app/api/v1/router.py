from fastapi import APIRouter

from app.api.health.router import router as health_router
from app.modules.authentication.api.router import router as auth_router
from app.modules.categories.api.router import router as categories_router
from app.modules.challenges.api.router import router as challenges_router
from app.modules.evaluations.api.router import router as evaluations_router
from app.modules.hints.api.router import router as hints_router
from app.modules.levels.api.router import router as levels_router
from app.modules.progress.api.router import router as progress_router
from app.modules.resources.api.router import router as resources_router
from app.modules.submissions.api.router import router as submissions_router
from app.modules.users.api.router import router as users_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(categories_router)
api_router.include_router(levels_router)
api_router.include_router(challenges_router)
api_router.include_router(submissions_router)
api_router.include_router(evaluations_router)
api_router.include_router(progress_router)
api_router.include_router(hints_router)
api_router.include_router(resources_router)
api_router.include_router(users_router)
