"""
Lana Store client.
"""

from typing import List, Optional

from rich.console import Console
from rich.pretty import Pretty
from rich.prompt import IntPrompt
from rich.text import Text
from rich.theme import Theme

from lana_client import gui
from lana_client.api import LanaStoreApi
from lana_client.config import settings


# Created carts
cart_ids: List[str] = []
# Cart currently selected.
selected_cart: Optional[int] = None

# Rich themes
# fmt: off
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "khaki1",
    "danger": "bold red"
})
# fmt: on

api_client = LanaStoreApi()

console = Console(theme=custom_theme)
layout = gui.make_layout()
layout["header"].update(gui.Header())
layout["carts"].update(gui.CartList(cart_ids))
layout["content"].update(gui.CartDetail([]))
layout["footer"].update(gui.Status())


def create_cart() -> None:
    """
    GUI helper to create a new cart.
    """
    global selected_cart

    resp = api_client.create_cart()
    if resp.status_code != 201:
        # Error processing the request.
        layout["content"].update(Pretty(resp.json()))
        layout["footer"].update(gui.Status(Text("[ERROR] Cannot create cart", style="danger")))
        return None

    cart_data = resp.json()

    cart_ids.append(cart_data["id"])
    selected_cart = len(cart_ids) - 1

    # Update GUI panels
    layout["carts"].update(gui.CartList(cart_ids, selected_cart))
    layout["content"].update(gui.CartDetail(cart_data["products"]))
    layout["footer"].update(gui.Status(Text("New cart created!", style="info")))


def refresh_cart() -> bool:
    """
    GUI helper to display carts content.

    *Note:* Before calling this method make sure that `selected_cart != None`.

    :return: `True` if cart data could be fetched, `False` otherwise.
    """
    resp = api_client.get_cart(cart_ids[selected_cart])  # type: ignore
    if resp.status_code != 200:
        # Error processing the request.
        layout["content"].update(Pretty(resp.json()))
        layout["footer"].update(gui.Status(Text("[ERROR] Cannot get cart content", style="danger")))
        return False

    cart_data = resp.json()

    # Update GUI panels
    layout["content"].update(gui.CartDetail(cart_data["products"], cart_data["total"]))

    return True


def select_cart(cart_index: int) -> None:
    """
    GUI helper to select a new cart.

    :param cart_index: Cart index.
    """
    global selected_cart

    if selected_cart is None:
        layout["footer"].update(gui.Status(Text("Must create a cart first! ", style="warning")))
        return None

    selected_cart = cart_index - 1

    if refresh_cart():
        # Update GUI panels
        layout["carts"].update(gui.CartList(cart_ids, selected_cart))
        layout["footer"].update(gui.Status(Text("Cart selected! :smiley:")))


def add_product(product_index: int) -> None:
    """
    GUI helper to add a product to a cart.

    :param product_index: Product index.
    """
    if selected_cart is None:
        layout["footer"].update(gui.Status(Text("Must create a cart first! ", style="warning")))
        return None

    product = settings.CLIENT_PRODUCT_CODES[product_index - 1]

    resp = api_client.add_product(cart_ids[selected_cart], product)
    if resp.status_code != 200:
        # Error processing the request.
        layout["content"].update(Pretty(resp.json()))
        layout["footer"].update(gui.Status(Text("[ERROR] Cannot add product", style="error")))
        return None

    if refresh_cart():
        # Update GUI panels
        layout["footer"].update(gui.Status(Text("Product added!", style="info")))


def delete_cart() -> None:
    """
    GUI helper to delete a cart.
    """
    global selected_cart

    if selected_cart is None:
        layout["footer"].update(gui.Status(Text("Must create a cart first! ", style="warning")))
        return None

    resp = api_client.remove_cart(cart_ids[selected_cart])
    if resp.status_code != 204:
        # Error processing the request.
        layout["content"].update(Pretty(resp.json()))
        layout["footer"].update(gui.Status(Text("[ERROR] Cannot delete the cart", style="error")))
        return None

    cart_ids.pop(selected_cart)

    if len(cart_ids):
        selected_cart = 0
    else:
        selected_cart = None

    refresh_cart()
    # Update GUI panels
    layout["footer"].update(gui.Status(Text("Cart deleted!", style="info")))


def display_products() -> None:
    """
    GUI helper to display the variety of products that are available in the
    footer layout.
    """
    product_range: str = ""
    for count, product in enumerate(settings.CLIENT_PRODUCT_CODES):
        product_range = "".join((product_range, f"{count + 1}-{product}   "))

    layout["footer"].update(
        gui.Status(Text("".join(("Available Products: ", product_range)), style="warning"))
    )


if __name__ == "__main__":
    with console.screen() as screen:
        while True:
            screen.update(layout)
            option = IntPrompt.ask("Select an option: ", choices=[f"{i + 1}" for i in range(5)])

            if option == 1:
                create_cart()

            elif option == 2:
                screen.update(layout)
                cart_selection = IntPrompt.ask(
                    "Select a cart: ", choices=[f"{i + 1}" for i in range(len(cart_ids))]
                )
                select_cart(cart_selection)

            elif option == 3:
                display_products()
                screen.update(layout)
                product_selection = IntPrompt.ask(
                    "Select a product: ",
                    choices=[f"{i + 1}" for i in range(len(settings.CLIENT_PRODUCT_CODES))],
                )
                add_product(product_selection)

            elif option == 4:
                delete_cart()

            else:
                break
