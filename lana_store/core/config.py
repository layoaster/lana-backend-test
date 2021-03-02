"""
Application settings.
"""
from typing import Dict, List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator

from lana_store.models.product import Product, ProductCodes


class Settings(BaseSettings):
    """
    Provides support for configuration with env-vars.
    """

    #: Project's name.
    PROJECT_NAME: str = "Lana Store"
    #: Subpath of the API version 1.
    API_V1_STR: str = "/api/v1"

    #: BACKEND_CORS_ORIGINS is a JSON-formatted list of origins.
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000"]'
    CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, value: Union[str, List[str]]) -> Union[List[str], str]:
        """
        Parse and deserialize the env-var data.

        :param value: Raw env-var value.
        :raises ValueError: When env-var contains wrong data type and/or format.
        :return: List of CORS origins or a single origin string
        """
        if isinstance(value, str) and not value.startswith("["):
            return [i.strip() for i in value.split(",")]
        elif isinstance(value, (list, str)):
            return value
        raise ValueError(value)

    #: Money decimal precision.
    MONEY_DECIMALS: int = 2

    #: Products data.
    PRODUCT_TABLE: Dict[ProductCodes, Product] = {
        "PEN": {"name": "Lana Pen", "price": 500},
        "TSHIRT": {"name": "Lana T-Shirt", "price": 2000},
        "MUG": {"name": "Lana Coffee Mug", "price": 750},
    }

    class Config:
        case_sensitive = True


settings = Settings()
