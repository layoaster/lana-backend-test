"""
Layout elements and other GUI related components.
"""
from collections import Counter
from datetime import datetime
from typing import List, Optional

from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


def make_layout() -> Layout:
    """
    Setup the GUI layout.

    :return The GUI layout.
    """
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=4),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=4),
    )
    layout["main"].split(
        Layout(name="carts", ratio=1),
        Layout(name="content", ratio=2, minimum_size=60),
        direction="horizontal",
    )
    return layout


class Header:
    """
    Display header with clock.
    """

    def __rich__(self) -> Panel:
        """
        Setup of rich renderables.

        :return: Panel with the proper content to draw.
        """
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "[b]Cart Manager[/b]",
            datetime.now().ctime().replace(":", "[blink]:[/]"),
        )
        grid.add_row(
            "[b]1:[/b] Create cart  "
            "[b]2:[/b] Select cart  "
            "[b]3:[/b] Add product  "
            "[b]4:[/b] Delete cart  "
            "[b]5:[/b] Exit"
        )
        return Panel(grid, title="Status", style="white on blue")


class Status:
    """
    Display status messages in footer.
    """

    def __init__(self, text: Text = Text("")):
        """
        Class initializer.

        :param text: Text to display.
        """
        self.text = text

    def __rich__(self) -> Panel:
        """
        Setup of rich renderables.

        :return: Panel with the proper content to draw.
        """
        grid = Table.grid(expand=True)
        grid.add_column(justify="left")
        grid.add_row(self.text)
        return Panel(grid, style="white on black")


class CartList:
    """
    Display the list of carts.
    """

    def __init__(self, carts: Optional[List[str]] = None, select: int = 0):
        """
        Class initializer.

        :param carts: List of carts.
        :param select: Cart to be selected.
        """
        self.select = select

        if carts:
            self.carts = carts
        else:
            self.carts = []

    def __rich__(self) -> Panel:
        """
        Setup of rich renderables.

        :return: Panel with the proper content to draw.
        """
        grid = Table.grid(expand=True)
        grid.add_column(justify="left")
        grid.add_column(justify="left", max_width=36)
        grid.add_row()

        if not self.carts:
            grid.add_row("", "[grey69]-- empty --[/grey69]")

        for index, cart_id in enumerate(self.carts):
            if index == self.select:
                # Highlights the selected cart
                text_cart_id = f"[white on grey69]{cart_id}[/white on grey69]"
            else:
                text_cart_id = f"{cart_id}"

            grid.add_row(f"{index + 1}", text_cart_id)

        return Panel(grid, title="Carts List", style="white on black")


class CartDetail:
    """
    Displays the products of a cart.
    """

    def __init__(self, products: List[str], total: str = "0.00"):
        """
        Class initializer.

        :param products: List of products.
        :param total: Total value of the cart.
        """
        self.products = products
        self.total = total

    def __rich__(self) -> Panel:
        """
        Setup of rich renderables.

        :return: Panel with the proper content to draw..
        """
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", max_width=8)
        grid.add_column(justify="left")
        grid.add_row("Quantity", "Product", style="grey69")
        grid.add_row("--------", "-----------")

        for product, count in Counter(self.products).items():
            grid.add_row(f"{count:>8}", f"{product}")

        grid.add_row("", "")
        grid.add_row("--------", "-----------")
        grid.add_row("Total", f"{self.total}")

        return Panel(grid, title="Products in Cart", style="white on black")
