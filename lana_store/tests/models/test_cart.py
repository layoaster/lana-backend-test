from lana_store.models.cart import Cart


class TestCartTotal:
    """
    Set of tests for the cart's `total` property
    :func:`lana_store.models.cart.Cart.total` (discounts bussiness logic).
    """

    def test_with_no_discounts(self) -> None:
        """
        Test when no discounts are to be applied.
        """
        cart_sample = Cart(products=["PEN", "MUG", "TSHIRT"])

        assert cart_sample.total == 3250

    def test_with_pen_discount_and_even_number(self) -> None:
        """
        Test when PEN discounts are applicable over an even number of pens.
        """
        cart_sample = Cart(products=["PEN", "PEN", "MUG", "TSHIRT"])

        assert cart_sample.total == 3250

    def test_with_pen_discount_and_odd_number(self) -> None:
        """
        Test when PEN discounts are applicable over an odd number of pens.
        """
        cart_sample = Cart(products=["PEN", "PEN", "PEN", "PEN", "PEN"])

        assert cart_sample.total == 1500

    def test_with_tshirt_discount(self) -> None:
        """
        Test when a TSHIRT discount is applicable.
        """
        cart_sample = Cart(products=["TSHIRT", "TSHIRT", "TSHIRT", "PEN", "TSHIRT"])

        assert cart_sample.total == 6500
