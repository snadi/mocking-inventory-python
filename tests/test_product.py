import unittest
from inventory_system.product import Product


class TestProduct(unittest.TestCase):

    def setUp(self):
        self.product = Product(1, "Test Product", 10)

    def test_get_id(self):
        self.assertEqual(self.product.get_id(), 1)

    def test_get_name(self):
        self.assertEqual(self.product.get_name(), "Test Product")

    def test_get_quantity(self):
        self.assertEqual(self.product.get_quantity(), 10)

    def test_set_quantity(self):
        self.product.set_quantity(20)
        self.assertEqual(self.product.get_quantity(), 20)
