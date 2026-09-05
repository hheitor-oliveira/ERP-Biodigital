from decimal import Decimal
from os import getenv
from uuid import uuid4

import pytest
from sqlalchemy import delete
from sqlalchemy.exc import DataError, IntegrityError, StatementError
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

from domain.enums.status import StatusEnum
from models.base import Base
from models.inventory_models.category_model import CategoryModel
from models.inventory_models.product_model import ProductModel
from models.inventory_models.stock_model import StockModel


pytestmark = [pytest.mark.integration, pytest.mark.postgres]


@pytest.fixture()
def postgres_session():
    database_url = getenv("DATABASE_URL")
    if not database_url or not database_url.startswith(
        ("postgresql://", "postgresql+psycopg://")
    ):
        pytest.skip("DATABASE_URL PostgreSQL não configurada")

    engine = create_engine(database_url)
    Base.metadata.create_all(bind=engine, tables=[CategoryModel.__table__, ProductModel.__table__])
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
    session = SessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.execute(
            delete(ProductModel).where(ProductModel.product_name.like("T041-%"))
        )
        session.execute(
            delete(CategoryModel).where(CategoryModel.category_name.like("T041-%"))
        )
        session.commit()
        session.close()
        engine.dispose()


def unique_name(prefix: str) -> str:
    return f"T041-{prefix}-{uuid4().hex[:8]}".upper()


def create_category(session: Session) -> CategoryModel:
    category = CategoryModel(
        category_name=unique_name("CATEGORY"),
        category_status=StatusEnum.ACTIVE,
    )
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


def create_product(
    session: Session,
    category_id: int,
    *,
    name: str | None = None,
    available_quantity: int | None = 0,
    product_status: StatusEnum | str | None = StatusEnum.ACTIVE,
    include_quantity: bool = True,
    include_status: bool = True,
) -> ProductModel:
    product_data: dict[str, object] = {
        "category_id": category_id,
        "product_name": name or unique_name("PRODUCT"),
        "cost_price": Decimal("10.00"),
        "sale_value": Decimal("15.00"),
    }
    if include_quantity:
        product_data["available_quantity"] = available_quantity
    if include_status:
        product_data["product_status"] = product_status

    product = ProductModel(**product_data)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


def test_foreign_key_rejects_unknown_category_and_rolls_back(postgres_session: Session):
    product = ProductModel(
        category_id=999_999_999,
        product_name=unique_name("ORPHAN"),
        cost_price=Decimal("10.00"),
        sale_value=Decimal("15.00"),
    )
    postgres_session.add(product)

    with pytest.raises(IntegrityError):
        postgres_session.commit()

    postgres_session.rollback()
    assert postgres_session.query(ProductModel).filter_by(
        product_name=product.product_name
    ).one_or_none() is None


def test_unique_constraint_rejects_duplicate_canonical_name(postgres_session: Session):
    category = create_category(postgres_session)
    canonical_name = unique_name("DUPLICATE")
    create_product(postgres_session, category.category_id, name=canonical_name)
    duplicate = ProductModel(
        category_id=category.category_id,
        product_name=canonical_name,
        cost_price=Decimal("20.00"),
        sale_value=Decimal("25.00"),
    )
    postgres_session.add(duplicate)

    with pytest.raises(IntegrityError):
        postgres_session.commit()

    postgres_session.rollback()
    assert postgres_session.query(ProductModel).filter_by(
        product_name=canonical_name
    ).count() == 1


def test_numeric_precision_preserves_scale_and_rejects_overflow(
    postgres_session: Session,
):
    category = create_category(postgres_session)
    valid_product = ProductModel(
        category_id=category.category_id,
        product_name=unique_name("PRECISION"),
        cost_price=Decimal("99999999.99"),
        sale_value=Decimal("0.01"),
    )
    postgres_session.add(valid_product)
    postgres_session.commit()
    postgres_session.refresh(valid_product)

    assert valid_product.cost_price == Decimal("99999999.99")
    assert valid_product.sale_value == Decimal("0.01")

    overflow = ProductModel(
        category_id=category.category_id,
        product_name=unique_name("OVERFLOW"),
        cost_price=Decimal("100000000.00"),
        sale_value=Decimal("15.00"),
    )
    postgres_session.add(overflow)

    with pytest.raises((DataError, StatementError)):
        postgres_session.commit()

    postgres_session.rollback()
    assert postgres_session.get(ProductModel, valid_product.product_id) is not None


def test_non_negative_constraints_reject_prices_and_quantity(
    postgres_session: Session,
):
    category = create_category(postgres_session)
    invalid_values = [
        {"product_name": unique_name("NEGATIVE-COST"), "cost_price": Decimal("-1.00")},
        {"product_name": unique_name("NEGATIVE-SALE"), "sale_value": Decimal("-1.00")},
        {"product_name": unique_name("NEGATIVE-QTY"), "available_quantity": -1},
    ]

    for values in invalid_values:
        product = ProductModel(
            category_id=category.category_id,
            product_name=values["product_name"],
            cost_price=values.get("cost_price", Decimal("10.00")),
            sale_value=values.get("sale_value", Decimal("15.00")),
            available_quantity=values.get("available_quantity", 0),
        )
        postgres_session.add(product)

        with pytest.raises(IntegrityError):
            postgres_session.commit()
        postgres_session.rollback()

    assert postgres_session.query(ProductModel).count() == 0


def test_status_constraint_accepts_only_domain_values(postgres_session: Session):
    category = create_category(postgres_session)
    for status in StatusEnum:
        product = create_product(postgres_session, category.category_id, product_status=status)
        assert product.product_status == status

    invalid_product = ProductModel(
        category_id=category.category_id,
        product_name=unique_name("INVALID-STATUS"),
        cost_price=Decimal("10.00"),
        sale_value=Decimal("15.00"),
        product_status="INVALID",
    )
    postgres_session.add(invalid_product)

    with pytest.raises((DataError, StatementError, IntegrityError)):
        postgres_session.commit()

    postgres_session.rollback()


def test_database_defaults_set_quantity_and_status(postgres_session: Session):
    category = create_category(postgres_session)
    product = ProductModel(
        category_id=category.category_id,
        product_name=unique_name("DEFAULTS"),
        cost_price=Decimal("10.00"),
        sale_value=Decimal("15.00"),
    )
    postgres_session.add(product)
    postgres_session.commit()
    postgres_session.refresh(product)

    assert product.available_quantity == 0
    assert product.product_status == StatusEnum.ACTIVE


def test_duplicate_name_race_allows_only_one_transaction(postgres_session: Session):
    category = create_category(postgres_session)
    engine = postgres_session.get_bind()
    first_session = sessionmaker(bind=engine, expire_on_commit=False)()
    second_session = sessionmaker(bind=engine, expire_on_commit=False)()
    name = unique_name("RACE")

    try:
        create_product(first_session, category.category_id, name=name)
        second_session.add(
            ProductModel(
                category_id=category.category_id,
                product_name=name,
                cost_price=Decimal("10.00"),
                sale_value=Decimal("15.00"),
            )
        )

        with pytest.raises(IntegrityError):
            second_session.commit()
        second_session.rollback()

        assert first_session.query(ProductModel).filter_by(product_name=name).count() == 1
        assert second_session.query(ProductModel).filter_by(product_name=name).count() == 1
    finally:
        first_session.close()
        second_session.close()


def test_failed_update_rolls_back_and_preserves_product(postgres_session: Session):
    category = create_category(postgres_session)
    product = create_product(
        postgres_session,
        category.category_id,
        name=unique_name("PRESERVE"),
        available_quantity=7,
        product_status=StatusEnum.INACTIVE,
    )
    original_id = product.product_id
    original_name = product.product_name
    product.product_name = unique_name("CHANGED")
    product.cost_price = Decimal("-1.00")
    product.available_quantity = -1

    with pytest.raises(IntegrityError):
        postgres_session.commit()

    postgres_session.rollback()
    persisted = postgres_session.get(ProductModel, original_id)
    assert persisted is not None
    assert persisted.product_id == original_id
    assert persisted.product_name == original_name
    assert persisted.cost_price == Decimal("10.00")
    assert persisted.sale_value == Decimal("15.00")
    assert persisted.available_quantity == 7
    assert persisted.product_status == StatusEnum.INACTIVE


def test_product_quantity_is_not_stock_specific_quantity():
    assert "available_quantity" in ProductModel.__table__.columns
    assert "stock_quantity" not in ProductModel.__table__.columns
    assert "stock_quantity" not in StockModel.__table__.columns
