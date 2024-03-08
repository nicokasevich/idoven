from app.endpoints.auth import router as auth_router
from app.endpoints.ecg import router as ecg_router

__all__ = ["auth_router", "ecg_router"]
