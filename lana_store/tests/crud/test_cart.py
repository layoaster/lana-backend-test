from typing import Dict

from lana_store import crud
from lana_store.models.cart import Cart


def test_create_cart() -> None:
    """
    Test of cart creation :func:`lana_store.crud.cart.create_new_cart`.
    """
    cart = crud.create_new_cart()

    assert cart
    assert cart.id
    assert not len(cart.products)


class TestGetCartById:
    """
    Tests cart retrieval by Id :func:`lana_store.crud.cart.get_cart_by_id`.
    """

    def test_when_cart_exists(self, cart_with_pen: Cart) -> None:
        """
        The when fetching an existent cart.
        """
        cart = crud.get_cart_by_id("cc733c92-6853-45f6-8e49-bec741188ebb")

        assert cart
        assert cart.id == cart_with_pen.id
        assert cart.products == ["PEN"]

    def test_when_cart_does_not_exist(self) -> None:
        """
        The when fetching an inexistent cart.
        """
        cart = crud.get_cart_by_id("cc733c92-6853-45f6-8e49-bec741188ebb")

        assert not cart


class TestUpdateCartWithProduct:
    """
    Tests cart update by Id :func:`lana_store.crud.cart.update_cart_with_product`.
    """

    def test_when_cart_exists(self, cart_with_pen: Cart) -> None:
        """
        The when updating an existent cart.
        """
        cart = crud.update_cart_with_product("cc733c92-6853-45f6-8e49-bec741188ebb", "TSHIRT")

        assert cart
        assert cart.products == ["PEN", "TSHIRT"]

    def test_when_cart_does_not_exist(self) -> None:
        """
        The when updating an inexistent cart.
        """
        cart = crud.update_cart_with_product("f728b4fa-4248-5e3a-0a5d-2f346baa9455", "MUG")

        assert not cart


class TestRemoveCart:
    """
    Tests cart removal :func:`lana_store.crud.cart.remove_cart`.
    """

    def test_when_cart_exists(self, carts_db: Dict[str, Cart], cart_with_pen: Cart) -> None:
        """
        The when deleting an existent cart.
        """
        cart = crud.remove_cart("cc733c92-6853-45f6-8e49-bec741188ebb")

        assert cart
        assert cart is cart_with_pen
        assert not len(carts_db)

    def test_when_cart_does_not_exist(self) -> None:
        """
        The when deleting an inexistent cart.
        """
        cart = crud.remove_cart("eb1167b3-67a9-c378-7c65-c1e582e2e662")

        assert not cart
