import pytest

from domain.enums.status import StatusEnum


@pytest.mark.integration
def test_list_categories_endpoint_returns_active_and_inactive_categories(
    authenticated_client,
    category_factory,
):
    category_factory(name="Categoria Ativa", status=StatusEnum.ACTIVE)
    category_factory(name="Categoria Inativa", status=StatusEnum.INACTIVE)

    response = authenticated_client.get("/category/list")

    assert response.status_code == 200

    payload = response.json()
    assert len(payload) == 2
    assert payload == [
        {
            "id": payload[0]["id"],
            "name": "CATEGORIA ATIVA",
            "status": "ACTIVE",
        },
        {
            "id": payload[1]["id"],
            "name": "CATEGORIA INATIVA",
            "status": "INACTIVE",
        },
    ]


@pytest.mark.integration
def test_list_categories_endpoint_returns_empty_list_when_no_categories_exist(
    authenticated_client,
):
    response = authenticated_client.get("/category/list")

    assert response.status_code == 200
    assert response.json() == []
