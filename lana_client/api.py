"""
Lana Store API consumer.
"""
from typing import Any, Dict, Optional

import backoff
import requests

from lana_client.config import ProductCodes, settings


class ApiConsumerBase:
    """
    Base class to make specific service API consumers. It makes HTTP requests
    with an exponential backoff retry logic.
    """

    #: Max number of seconds to wait for server to send a response.
    # Avoids blocking indefinitely).
    max_request_timeout = settings.CLIENT_API_CONSUMER_MAX_REQUEST_TIMEOUT

    def __init__(self, json: bool = True):
        """
        Class initialization.
        :param json: `True` to consume JSON APIs, default to `True`.
        :param api_key: Dictionary with the API key and its url parameter,
            defaults to None.
        """
        # Build `Session` object ready to consume APIs.
        self.session = requests.Session()

        self.json = json
        if json:
            self.session.headers["Content-Type"] = "application/json"
            self.session.headers["Accept"] = "application/json"

    @backoff.on_exception(
        backoff.expo,
        (
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
        ),
        max_tries=settings.CLIENT_API_CONSUMER_MAX_TRIES,
    )
    def make_request(
        self,
        verb: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        """
        Makes HTTPs requests falling back to an exponential back-off strategy
        in case of network failures.
        :param verb: The HTTP verb of the request. Valid choices:
            [`GET`,`POST`, `PUT`, `PATCH`, 'DELETE`].
        :param url: The request URL.
        :param params: The URL parameters of the request, defaults to None.
        :param payload: The body of the request, defaults to None.
        :raises ValueError: For invalid HTTP verbs.
        :return: The request response.
        """
        if verb in ("GET", "POST", "PUT", "PATCH", "DELETE"):
            return self.session.request(
                verb,
                url,
                params=params,
                data=payload if not self.json else None,
                json=payload if self.json else None,
                timeout=self.max_request_timeout,
            )
        else:
            raise ValueError(
                f"Invalid HTTP verb '{verb}'. "
                f"Valid options: 'GET', 'POST', 'PUT', 'PATCH' or 'DELETE'"
            )


class LanaStoreApi(ApiConsumerBase):
    """
    Consumer of the Lana Store API.
    """

    #: Carts endpoint's base url.
    CARTS_ENDPOINT = "/".join((settings.CLIENT_STORE_API_BASE_URL, "carts/"))

    def __init__(self) -> None:
        """
        Class initialization.
        """
        super().__init__(json=True)

    def create_cart(self) -> requests.Response:
        """
        Creates a new Cart
        """
        return self.make_request("POST", self.CARTS_ENDPOINT)

    def get_cart(self, cart_id: str) -> requests.Response:
        """
        Fetches a cart.

        :param cart_id: Cart Id.
        :return: HTTP response object.
        """

        return self.make_request("GET", "".join((self.CARTS_ENDPOINT, cart_id)))

    def remove_cart(self, cart_id: str) -> requests.Response:
        """
        Removes a cart.

        :param cart_id: Cart Id.
        :return: HTTP response object.
        """
        return self.make_request("DELETE", "".join((self.CARTS_ENDPOINT, cart_id)))

    def add_product(self, cart_id: str, product: ProductCodes) -> requests.Response:
        """
        Adds a product to a cart.

        :param cart_id: Cart Id.
        :param product: Product (code) to add to the cart.
        :return: HTTP response object.
        """
        return self.make_request(
            "PATCH", "".join((self.CARTS_ENDPOINT, cart_id)), payload={"product": product}
        )
