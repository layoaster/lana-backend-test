"""
CRUD operations on the Cart.
"""
from typing import Optional

import lana_store
from lana_store.models.cart import Cart
from lana_store.models.product import ProductCodes


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


def update_cart_with_product(id: str, product: ProductCodes) -> Optional[Cart]:
    """
    Adds a product to a cart.

    :param id: Id of the cart to update.
    :param product: Product code to be added.
    :type product: str
    :return: The updated cart object (if any).
    """
    try:
        cart = lana_store.carts_db[id]
    except KeyError:
        return None

    cart.products.append(product)

    return cart


def remove_cart(id: str) -> Optional[Cart]:
    """
    Deletes a cart.

    :param id: Id of the cart to be deleted.
    :return: The deleted cart (if any).
    """
    try:
        cart = lana_store.carts_db[id]
    except KeyError:
        return None

    del lana_store.carts_db[id]

    return cart
