from fastapi import status
from fastapi.testclient import TestClient

from lana_store.api.v1.api import api_router
from lana_store.core.config import settings
from lana_store.models.cart import Cart


def test_create_cart(client: TestClient) -> None:
    """
    Test view that create new carts :func:`lana_store.api.v1.endpoints.create_cart`.
    """
    resp = client.post(f"{settings.API_V1_STR}{api_router.url_path_for('create_cart')}")

    assert resp.status_code == status.HTTP_201_CREATED
    content = resp.json()
    assert content["id"]
    assert content["products"] == []


class TestGetCart:
    """
    Set of tests for the view that retrieves carts
    :func:`lana_store.api.v1.endpoints.get_cart`.
    """

    def test_with_valid_cart(self, client: TestClient, cart_with_pen: Cart) -> None:
        """
        Test when the cart exists. It also tests money formatting.
        """
        resp = client.get(
            f"{settings.API_V1_STR}"
            f"{api_router.url_path_for('get_cart', cart_id=str(cart_with_pen.id))}"
        )

        assert resp.status_code == status.HTTP_200_OK
        content = resp.json()
        assert content["id"] == str(cart_with_pen.id)
        assert content["products"] == ["PEN"]
        assert content["total"] == "5.00"

    def test_with_invalid_cart(self, client: TestClient, cart_with_pen: Cart) -> None:
        """
        Test when the cart does not exists.
        """
        resp = client.get(
            f"{settings.API_V1_STR}" f"{api_router.url_path_for('get_cart', cart_id='invalid-id')}"
        )

        assert resp.status_code == status.HTTP_404_NOT_FOUND
        content = resp.json()
        assert "detail" in content


class TestPartialUpdateCart:
    """
    Set of tests for the view that add products to carts
    :func:`lana_store.api.v1.endpoints.partial_update_cart`.
    """

    def test_with_valid_product(self, client: TestClient, cart_with_pen: Cart) -> None:
        """
        Test with a valid product code.
        """
        payload = {"product": "MUG"}
        resp = client.patch(
            f"{settings.API_V1_STR}"
            f"{api_router.url_path_for('partial_update_cart', cart_id=str(cart_with_pen.id))}",
            json=payload,
        )

        assert resp.status_code == status.HTTP_200_OK
        content = resp.json()
        assert content["products"] == ["PEN", "MUG"]

    def test_with_invalid_product(self, client: TestClient, cart_with_pen: Cart) -> None:
        """
        Test with an invalid product code.
        """
        payload = {"product": "INVALID"}
        resp = client.patch(
            f"{settings.API_V1_STR}"
            f"{api_router.url_path_for('partial_update_cart', cart_id=str(cart_with_pen.id))}",
            json=payload,
        )

        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        content = resp.json()
        assert "detail" in content
        assert "unexpected value", content["detail"]["msg"]

    def test_with_invalid_cart(self, client: TestClient, cart_with_pen: Cart) -> None:
        """
        Test when the cart does not exists.
        """
        payload = {"product": "MUG"}
        resp = client.patch(
            f"{settings.API_V1_STR}"
            f"{api_router.url_path_for('partial_update_cart', cart_id='invalid-id')}",
            json=payload,
        )

        assert resp.status_code == status.HTTP_404_NOT_FOUND
        content = resp.json()
        assert "detail" in content


class TestDeleteCart:
    """
    Set of tests for the view that removes carts
    :func:`lana_store.api.v1.endpoints.delete_cart`.
    """

    def test_with_valid_cart(self, client: TestClient, cart_with_pen: Cart) -> None:
        """
        Test when the cart exists.
        """
        resp = client.delete(
            f"{settings.API_V1_STR}"
            f"{api_router.url_path_for('delete_cart', cart_id=str(cart_with_pen.id))}"
        )

        assert resp.status_code == status.HTTP_204_NO_CONTENT

    def test_with_invalid_cart(self, client: TestClient, cart_with_pen: Cart) -> None:
        """
        Test when the cart does not exists.
        """
        resp = client.delete(
            f"{settings.API_V1_STR}"
            f"{api_router.url_path_for('delete_cart', cart_id='invalid-id')}"
        )

        assert resp.status_code == status.HTTP_404_NOT_FOUND
        content = resp.json()
        assert "detail" in content
