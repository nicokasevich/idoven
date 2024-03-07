from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import database
from app.endpoints import auth_router


def create_app() -> FastAPI:
    database.Base.metadata.create_all(bind=database.engine)

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router)

    return app
