"""
app/api/v1/router.py
─────────────────────
Central v1 router — aggregates all endpoint routers.

Adding a new feature = import its router here and call include_router().
No changes needed anywhere else.
"""

from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.patients import router as patients_router
from app.api.v1.endpoints.reports import router as reports_router
from app.api.v1.endpoints.chat import router as chat_router

# All routes under /api/v1/
api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(patients_router)
api_router.include_router(reports_router)
api_router.include_router(chat_router)
