import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.base import Base
from main import create_app
from tests.factories import sqlalchemy_factories
from tests.factories.user import UserFactory


@pytest.fixture(autouse=True)
def db_session():
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return SessionLocal()


@pytest.fixture(autouse=True)
def set_session_in_factories(db_session: Session):
    for factory in sqlalchemy_factories:
        factory._meta.sqlalchemy_session_factory = lambda: db_session


@pytest.fixture()
def app(db_session: Session):
    app = create_app()
    app.dependency_overrides[get_db] = lambda: db_session
    return app


@pytest.fixture()
def client(app: FastAPI):
    return TestClient(app)


@pytest.fixture
def authenticate_as_user(app: FastAPI):
    user = UserFactory()
    app.dependency_overrides[get_current_user] = lambda: user
    return user


@pytest.fixture
def authenticate_as_admin(app: FastAPI):
    user = UserFactory(role="admin")
    app.dependency_overrides[get_current_user] = lambda: user
    return user
