"""
The API views for the `Cart` resource on the version `v1`.
"""
from typing import Any

from fastapi import APIRouter, HTTPException, Response, status

from lana_store import schemas
from lana_store.core.config import settings
from lana_store.crud.cart import (
    create_new_cart,
    get_cart_by_id,
    remove_cart,
    update_cart_with_product,
)


router = APIRouter()


@router.post("/", response_model=schemas.CartCreateOutput, status_code=201)
async def create_cart() -> Any:
    """
    Creates a cart.
    \f

    :return: New cart.
    """
    return create_new_cart()


@router.get(
    "/{cart_id}",
    response_model=schemas.CartOutput,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Cart not found"}},
)
async def get_cart(cart_id: str) -> Any:
    """
    Retrieves a cart.
    \f

    :param cart_id: Cart Id to lookup.
    :raises HTTPException: Cart not found.
    :return: Correspondent cart.
    """
    cart = get_cart_by_id(cart_id)
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")

    # Adds decimals to format money output
    total_price = str(cart.total / (10 ** settings.MONEY_DECIMALS))

    return schemas.CartOutput(**cart.dict(), total=total_price)


@router.patch(
    "/{cart_id}",
    response_model=schemas.CartUpdateOutput,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Cart not found"}},
)
async def partial_update_cart(cart_id: str, cart_in: schemas.CartUpdateInput) -> Any:
    """
    Updates a cart by adding a product.
    \f

    :param cart_id: Cart Id.
    :param cart_in: Payload of the request.
    :raises HTTPException: Cart not found.
    :return: Updated cart.
    """
    cart = update_cart_with_product(cart_id, cart_in.product)

    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")

    return cart


@router.delete(
    "/{cart_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Cart not found"}},
)
async def delete_cart(cart_id: str) -> Any:
    """
    Removes a cart.
    \f

    :param cart_id: Cart Id.
    :raises HTTPException: Cart not found.
    :return: Empty payload.
    """
    cart = remove_cart(cart_id)

    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
