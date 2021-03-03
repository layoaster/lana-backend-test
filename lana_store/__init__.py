"""
Define the carts database as an in-memory object globally accessible.
"""
from typing import Dict

from lana_store.models.cart import Cart

carts_db: Dict[str, Cart] = dict()
