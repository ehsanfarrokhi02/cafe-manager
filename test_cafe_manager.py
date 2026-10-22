
import unittest
from unittest.mock import patch, call
import cafe_manager


class TestCafeManager(unittest.TestCase):

    def test_menu_prices(self):
        self.assertEqual(cafe_manager.menu["Espresso"], 260000)
        self.assertEqual(cafe_manager.menu["Americano"], 270000)
        self.assertEqual(cafe_manager.menu["Cappucino"], 300000)
        self.assertEqual(cafe_manager.menu["Latte"], 300000)
        self.assertEqual(cafe_manager.menu["Cheescacke"], 380000)


class TestShowMenu(unittest.TestCase):

    def test_show_menu(self):
        with patch("builtins.print") as mock_print:
            cafe_manager.show_menu()

        expected_calls = [
            call("Espresso", ":", 260000),
            call("Americano", ":", 270000),
            call("Cappucino", ":", 300000),
            call("Latte", ":", 300000),
            call("Cheescacke", ":", 380000)
        ]

        self.assertEqual(mock_print.call_args_list, expected_calls)


class TestAddItem(unittest.TestCase):

    def setUp(self):
        self.original_menu = cafe_manager.menu.copy()

    def tearDown(self):
        cafe_manager.menu.clear()
        cafe_manager.menu.update(self.original_menu)

    def test_add_item(self):
        with patch("builtins.input", side_effect=["Mocka", "350000"]):
            cafe_manager.add_item()

        self.assertEqual(cafe_manager.menu["Mocka"], 350000)

    def test_add_existing_item(self):
        with patch("builtins.input", return_value="Espresso"):
            with patch("builtins.print") as mock_print:
                cafe_manager.add_item()

        mock_print.assert_called_with("Item already exists.")
        self.assertEqual(cafe_manager.menu["Espresso"], 260000)

    def test_add_empty_name(self):
        with patch("builtins.input", side_effect=[
            "", "Mocka", "350000"
        ]):
            with patch("builtins.print") as mock_print:
                cafe_manager.add_item()

        mock_print.assert_any_call("please write a word")
        self.assertEqual(cafe_manager.menu["Mocka"], 350000)

    def test_add_invalid_price(self):
        with patch("builtins.input", side_effect=[
            "Mocka", "abc", "Mocka", "350000"
        ]):
            with patch("builtins.print") as mock_print:
                cafe_manager.add_item()

        mock_print.assert_any_call("Please type a number")
        self.assertEqual(cafe_manager.menu["Mocka"], 350000)


class TestRemoveItem(unittest.TestCase):

    def setUp(self):
        self.original_menu = cafe_manager.menu.copy()

    def tearDown(self):
        cafe_manager.menu.clear()
        cafe_manager.menu.update(self.original_menu)

    def test_remove_item(self):
        with patch("builtins.input", return_value="Espresso"):
            cafe_manager.remove_item()

        self.assertNotIn("Espresso", cafe_manager.menu)

    def test_remove_nonexistent_item(self):
        with patch("builtins.input", side_effect=[
            "Pizza", "Espresso"
        ]):
            with patch("builtins.print") as mock_print:
                cafe_manager.remove_item()

        mock_print.assert_any_call("Item not found")
        self.assertNotIn("Espresso", cafe_manager.menu)


class TestSearchItem(unittest.TestCase):

    def test_search_existing_item(self):
        with patch("builtins.input", return_value="Espresso"):
            with patch("builtins.print") as mock_print:
                cafe_manager.search_item()

        mock_print.assert_called_with(
            "Espresso", " price is: ", 260000
        )

    def test_search_nonexistent_item(self):
        with patch("builtins.input", side_effect=[
            "Pizza", "Latte"
        ]):
            with patch("builtins.print") as mock_print:
                cafe_manager.search_item()

        mock_print.assert_any_call("Item not found")
        mock_print.assert_any_call(
            "Latte", " price is: ", 300000
        )


class TestNewOrder(unittest.TestCase):

    def test_single_item_order(self):
        with patch("builtins.input", side_effect=[
            "Espresso", "2", "no"
        ]):
            with patch("builtins.print") as mock_print:
                cafe_manager.new_order()

        mock_print.assert_any_call("TOTAL:", 520000)
        mock_print.assert_any_call(" === RECEIPT===")

    def test_multiple_items_order(self):
        with patch("builtins.input", side_effect=[
            "Espresso", "2", "yes",
            "Latte", "1", "no"
        ]):
            with patch("builtins.print") as mock_print:
                cafe_manager.new_order()

        mock_print.assert_any_call("TOTAL:", 820000)
        mock_print.assert_any_call(" === RECEIPT===")

    def test_invalid_item(self):
        with patch("builtins.input", side_effect=[
            "Pizza",
            "Espresso", "1", "no"
        ]):
            with patch("builtins.print") as mock_print:
                cafe_manager.new_order()

        mock_print.assert_any_call("Item not found")
        mock_print.assert_any_call("TOTAL:", 260000)

    def test_invalid_quantity(self):
        with patch("builtins.input", side_effect=[
            "Espresso", "abc",
            "Espresso", "2", "no"
        ]):
            with patch("builtins.print") as mock_print:
                cafe_manager.new_order()

        mock_print.assert_any_call("Please enter an number:  ")
        mock_print.assert_any_call("TOTAL:", 520000)

    def test_invalid_continue_answer(self):
        with patch("builtins.input", side_effect=[
            "Espresso", "1",
            "maybe", "no"
        ]):
            with patch("builtins.print") as mock_print:
                cafe_manager.new_order()

        mock_print.assert_any_call("Please type yes ro no")
        mock_print.assert_any_call("TOTAL:", 260000)

    def test_receipt_details(self):
        with patch("builtins.input", side_effect=[
            "Espresso", "2", "no"
        ]):
            with patch("builtins.print") as mock_print:
                cafe_manager.new_order()

        mock_print.assert_any_call(
            "Espresso", " * ", 2,
            "\nprice:", 260000,
            "\nSubtotal: ", 520000,
            "\n-------------------"
        )

    def test_zero_quantity(self):
        with patch("builtins.input", side_effect=[
            "Espresso", "0", "no"
        ]):
            with patch("builtins.print") as mock_print:
                cafe_manager.new_order()

        mock_print.assert_any_call("TOTAL:", 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
