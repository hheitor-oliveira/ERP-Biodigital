from __future__ import annotations

from pathlib import Path
import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from api.app import app as fastapi_app
from api.dependencies import (
    get_authenticated_user,
    get_session,
    verify_access_token,
)
from domain.enums.status import StatusEnum
from domain.inventory.category import Category
from models.base import Base
from models.inventory_models.category_model import CategoryModel  # noqa: F401
from models.inventory_models.product_model import ProductModel  # noqa: F401
from models.user_model.user_model import UserModel


@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    yield engine
    engine.dispose()


@pytest.fixture()
def db_session(test_engine):
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    SessionLocal = sessionmaker(bind=test_engine, expire_on_commit=False)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def app(db_session):
    def override_get_session():
        yield db_session

    fastapi_app.dependency_overrides[get_session] = override_get_session
    try:
        yield fastapi_app
    finally:
        fastapi_app.dependency_overrides.clear()


@pytest.fixture()
def client(app):
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def authenticated_client(client, app):
    authenticated_user = UserModel(
        user_id=1,
        user_name="Integration User",
        user_email="integration@example.com",
        user_password="hashed-password",
        admin=False,
    )
    app.dependency_overrides[get_authenticated_user] = (
        lambda: authenticated_user
    )
    app.dependency_overrides[verify_access_token] = lambda: authenticated_user
    yield client
    app.dependency_overrides.pop(get_authenticated_user, None)
    app.dependency_overrides.pop(verify_access_token, None)


@pytest.fixture()
def category_name() -> str:
    return "Categoria Válida"


@pytest.fixture()
def category_payload(category_name: str) -> dict[str, str]:
    return {"name": category_name}


@pytest.fixture()
def normalized_category_name() -> str:
    return "  Categoria Válida  "


@pytest.fixture()
def category_factory(db_session):
    def factory(
        name: str = "Categoria Válida",
        status: StatusEnum = StatusEnum.ACTIVE,
    ) -> CategoryModel:
        category_model = CategoryModel(
            category_name=name,
            category_status=status,
        )
        db_session.add(category_model)
        db_session.commit()
        db_session.refresh(category_model)
        return category_model

    return factory


@pytest.fixture()
def category_domain_factory() -> Category:
    return Category(name="Categoria Válida")
