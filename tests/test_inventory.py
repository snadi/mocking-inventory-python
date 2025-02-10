import pytest
from inventory_system.inventory import Inventory
from inventory_system.product import Product
from unittest.mock import MagicMock
from inventory_system.database_service import DatabaseService
from inventory_system.notification_service import NotificationService

@pytest.fixture
def mock_notification_service():
    """Fixture to provide a mocked notification service."""
    return MagicMock()

@pytest.fixture
def mock_database_service():
    """Fixture to provide a mocked database service."""
    return MagicMock()

@pytest.fixture
def inventory(mock_notification_service, mock_database_service):
    """Fixture to create an Inventory instance with mocked dependencies."""
    return Inventory(mock_notification_service, mock_database_service)

@pytest.fixture
def product():
    return Product(1, "Test Product", 10)

def test_add_product_notexisting(inventory, mock_database_service, product):
    mock_database_service.product_exists.return_value = False
    inventory.add_product(product)
    mock_database_service.save_product.assert_called_once_with(product)
    assert inventory.get_product_by_id(1) == product

def test_add_product_existing(inventory, mock_database_service, product, mock_notification_service):
    mock_database_service.product_exists.return_value = True
    inventory.add_product(product)
    mock_database_service.save_product.assert_not_called()
    assert inventory.get_product_by_id(1) is None
    assert mock_notification_service.send_notification.called

def test_update_quantity_above(inventory, mock_database_service, product, mock_notification_service):
    mock_database_service.product_exists.return_value = False
    inventory.add_product(product)
    inventory.update_quantity(1, 10)
    mock_database_service.save_product.assert_called_once
    mock_notification_service.send_notification.assert_not_called()
    assert product.get_quantity() == 10
    
def test_update_quantity_below(inventory, mock_database_service, product, mock_notification_service):
    mock_database_service.product_exists.return_value = False
    inventory.add_product(product)
    inventory.update_quantity(1, 3)
    mock_database_service.save_product.assert_called_once
    mock_notification_service.send_notification.assert_called_once()
    assert product.get_quantity() == 3