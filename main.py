from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.endpoints import auth_router, ecg_router


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router)
    app.include_router(ecg_router)

    return app
