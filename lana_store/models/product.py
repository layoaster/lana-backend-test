"""
Definition of Product for in-memory storage.
"""

from typing import Literal

from typing_extensions import TypedDict


ProductCodes = Literal["PEN", "TSHIRT", "MUG"]


class Product(TypedDict):
    """
    Product data dict.
    """

    #: Product's name.
    name: str
    #: Produce price in money-as-integer format.
    price: int
