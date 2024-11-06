import unittest
from inventory_system.inventory import Inventory
from inventory_system.product import Product
from unittest.mock import Mock
from inventory_system.notification_service import NotificationService
from inventory_system.database_service import DatabaseService


class TestProduct(unittest.TestCase):
    def setUp(self):
        self.database_service_mock = Mock(DatabaseService)
        self.notification_service_mock = Mock(NotificationService)
        self.inventory = Inventory(
            self.notification_service_mock, self.database_service_mock
        )

    def test_add_product(self):
        self.database_service_mock.product_exists.return_value = False

        self.product = Product("1", "Test Product", 10)
        self.inventory.add_product(self.product)

        self.assertEqual(self.inventory.get_product_by_id("1"), self.product)
        self.database_service_mock.save_product.assert_called_once()
        self.database_service_mock.save_product.assert_called_with(self.product)

    def test_add_existing_product(self):
        self.database_service_mock.product_exists.return_value = True

        self.product = Product("1", "Test Product", 10)
        self.inventory.add_product(self.product)

        self.assertEqual(self.inventory.get_product_by_id("1"), None)
        self.notification_service_mock.send_notification.assert_called_once()
        self.notification_service_mock.send_notification.assert_called_with(
            "Product Test Product already exists in inventory."
        )

    def test_update_quantity_for_existing_prod(self):

        # add product to inventory
        self.database_service_mock.product_exists.return_value = False
        self.product = Product("1", "Test Product", 10)
        self.inventory.add_product(self.product)

        # update quantity
        self.inventory.update_quantity("1", 25)

        self.assertEqual(self.inventory.get_product_by_id("1").get_quantity(), 25)
        self.database_service_mock.save_product.assert_called_with(self.product)

    def test_update_quantity_for_nonexisting_prod(self):
        self.inventory.update_quantity("1", 25)

        self.assertEqual(self.inventory.get_product_by_id("1"), None)
        self.database_service_mock.save_product.assert_not_called()

    def test_low_stock_update(self):
        self.database_service_mock.product_exists.return_value = False
        self.product = Product("1", "Test Product", 10)
        self.inventory.add_product(self.product)

        self.inventory.update_quantity("1", 4)

        self.notification_service_mock.send_notification.assert_called_once()
        self.notification_service_mock.send_notification.assert_called_with(
            "Stock for product Test Product is low: 4"
        )
        self.database_service_mock.save_product.assert_called_with(self.product)
