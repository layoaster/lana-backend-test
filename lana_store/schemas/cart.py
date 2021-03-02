"""
API (de)serialization schemes for the `Cart` resource.
"""
from typing import List

from pydantic import BaseModel, Field, UUID4

from lana_store.models.product import ProductCodes


class CartBase(BaseModel):
    """
    Properties common to other schemes.
    """

    id: UUID4 = Field(example="e44fd23b-f8a5-4285-8b04-e0334315f26e")
    products: List[ProductCodes] = Field(example=["PEN", "MUG"])


class CartOutput(CartBase):
    """
    Response scheme of the cart fetching endpoint.
    """

    total: str = Field(example="22.05")


class CartCreateOutput(CartBase):
    """
    Response scheme of the cart creation endpoint.
    """

    pass
