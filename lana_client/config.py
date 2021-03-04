from typing import List, Literal

from pydantic import BaseSettings

ProductCodes = Literal["PEN", "TSHIRT", "MUG"]


class ClientSettings(BaseSettings):
    """
    Provides support for configuration with env-vars.
    """

    #: Products data.
    CLIENT_PRODUCT_CODES: List[ProductCodes] = ["PEN", "TSHIRT", "MUG"]

    #: Lana Store API base path.
    CLIENT_STORE_API_BASE_URL: str = "http://127.0.0.1:8000/api/v1"

    #: Max retry attempts for failed HTTP requests
    CLIENT_API_CONSUMER_MAX_TRIES: int = 3

    #: HTTP read request max timeout (seconds).
    CLIENT_API_CONSUMER_MAX_REQUEST_TIMEOUT: int = 5

    class Config:
        case_sensitive = True


settings = ClientSettings()
