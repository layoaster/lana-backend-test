"""
CRUD operations on the Cart.
"""
from typing import Optional

import lana_store
from lana_store.models.cart import Cart


def create_new_cart() -> Cart:
    """
    Creates a new (empty) cart.

    :return: The new cart object.
    """
    new_cart = Cart()
    lana_store.carts_db[str(new_cart.id)] = new_cart

    return new_cart


def get_cart_by_id(id: str) -> Optional[Cart]:
    """
    Fetches a cart by its Id.

    :param id: Cart Id to search for.
    :return: The correspondent cart object (if any).
    """
    try:
        return lana_store.carts_db[id]
    except KeyError:
        return None
