from unittest.mock import MagicMock
from inventory_system.inventory import Inventory
from inventory_system.product import Product
import pytest


@pytest.fixture
def database_service():
    db_service = MagicMock()
    return db_service


@pytest.fixture
def notification_service():
    notification_service = MagicMock()
    return notification_service


@pytest.fixture
def inventory(database_service, notification_service):
    return Inventory(notification_service, database_service)


def test_add_new_product(inventory, database_service, notification_service):
    database_service.product_exists.return_value = False
    product = Product(1, "Widget", 10)
    inventory.add_product(product)
    assert inventory.get_product_by_id(1) == product
    database_service.save_product.assert_called_once_with(product)
    notification_service.send_notification.assert_not_called()


def test_add_existing_product(inventory, database_service, notification_service):
    database_service.product_exists.return_value = True

    product = Product(1, "Widget", 10)
    inventory.add_product(product)

    notification_service.send_notification.assert_called_once_with(
        "Product Widget already exists in inventory."
    )
    database_service.save_product.assert_not_called()


def test_update_quantity_above_threshold(
    inventory, database_service, notification_service
):
    database_service.product_exists.return_value = False
    product = Product(1, "Widget", 10)
    inventory.add_product(product)

    inventory.update_quantity(1, 7)
    assert inventory.get_product_by_id(1).get_quantity() == 7

    database_service.save_product.assert_called_with(product)
    notification_service.send_notification.assert_not_called()


def test_update_quantity_below_threshold(
    inventory, database_service, notification_service
):
    database_service.product_exists.return_value = False
    product = Product(1, "Widget", 10)
    inventory.add_product(product)

    inventory.update_quantity(1, 3)
    database_service.save_product.assert_called_with(product)
    notification_service.send_notification.assert_called_once_with(
        "Stock for product Widget is low: 3"
    )


def test_update_nonexistent_product(inventory, database_service, notification_service):
    inventory.update_quantity(999, 10)  # Non-existent product ID
    database_service.save_product.assert_not_called()
    notification_service.send_notification.assert_not_called()
