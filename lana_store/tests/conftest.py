import uuid
from typing import Dict, Generator

import pytest
import requests
from faker import Faker
from fastapi.testclient import TestClient

import lana_store
from lana_store.main import app
from lana_store.models.cart import Cart


@pytest.fixture(scope="module")
def client() -> Generator[requests.Session, None, None]:
    """
    Fast API testing client.
    """
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
def reset_carts_db() -> None:
    """
    Resets the database to isolate tests.
    """
    lana_store.carts_db = dict()


@pytest.fixture(scope="session")
def carts_db() -> Dict[str, Cart]:
    """
    Provides access to the global in-memory carts database object.
    """
    return lana_store.carts_db


@pytest.fixture
def cart_with_pen() -> Cart:
    """
    Sample cart with one `PEN` only and UUID `cc733c92-6853-45f6-8e49-bec741188ebb`.
    """
    faker = Faker()
    Faker.seed(4321)

    cart = Cart(id=uuid.UUID(faker.uuid4()), products=["PEN"])
    lana_store.carts_db[str(cart.id)] = cart

    return cart
