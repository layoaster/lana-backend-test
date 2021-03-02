"""
The API views for the `Cart` resource on the version `v1`.
"""
from typing import Any

from fastapi import APIRouter, HTTPException, status

from lana_store import schemas
from lana_store.core.config import settings
from lana_store.crud.cart import create_new_cart, get_cart_by_id


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
    responses={404: {"description": "Cart not found"}},
)
async def get_cart(cart_id: str) -> Any:
    """
    Retrieves a cart.
    \f

    :param cart_id: Cart Id to lookup.
    :return: Correspondent cart.
    """
    cart = get_cart_by_id(cart_id)
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")

    # Adds decimals to format money output
    total_price = str(cart.total * (10 ** settings.MONEY_DECIMALS))

    return schemas.CartOutput(**cart.dict(), total=total_price)
