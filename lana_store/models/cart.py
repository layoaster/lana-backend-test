"""
Definition of Cart for in-memory storage.
"""
import uuid
from collections import Counter
from typing import List

from pydantic import BaseModel, UUID4

from lana_store.core.config import settings
from lana_store.models.product import ProductCodes


class Cart(BaseModel):
    """
    Representation of a shopping cart for the database.
    """

    #: UUIDv4 that uniquely identifies the Cart.
    id: UUID4 = uuid.uuid4()
    #: List of checked-out products.
    products: List[ProductCodes] = []

    @property
    def total(self) -> int:
        """
        Calculates the cart's `total` amount of money. Applies the correspondent
        promotional discounts over Pens and T-Shirts (if any).

        :return: Total value of products in the cart after discounts with the
            money-as-integer format.
        """
        p_counter = Counter(self.products)

        total = 0
        for product, count in p_counter.items():
            if product == "PEN":
                total += (count // 2) * settings.PRODUCT_TABLE[product]["price"]
                total += settings.PRODUCT_TABLE[product]["price"] if count % 2 != 0 else 0

            elif product == "TSHIRT":
                if count < 3:
                    total += settings.PRODUCT_TABLE[product]["price"] * count
                else:
                    total += int((settings.PRODUCT_TABLE[product]["price"] * count) * (1 - 0.25))

            else:
                total += settings.PRODUCT_TABLE[product]["price"] * count

        return total
