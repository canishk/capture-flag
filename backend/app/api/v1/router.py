from fastapi import APIRouter

from app.api.health.router import router as health_router
from app.modules.authentication.api.router import router as auth_router
from app.modules.users.api.router import router as users_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(users_router)
