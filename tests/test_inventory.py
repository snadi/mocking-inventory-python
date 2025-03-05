'''
Some useful info:
- A stub is used to provide predefined responses for method calls, but it does not verify how those methods were used. 
It only controls the output of a method.
- A mock tracks interactions with the method (e.g., whether a method was called, how many times, and with what arguments).

When we create a MagicMock object (or mock any class in other languages/libraries), the libraries set up a test double that allows us to both track
interactions or control predefined responses. 

To illustrate a bit further, we can actually create stubs ourselves without using a mocking library. However, creating mocks is more difficult.
For example, I can create a stub for the database and notification services like this (add it as helper code in my tests)

class DatabaseServiceStub(DatabaseService):
    def product_exists(self, product_id):
        # Stubbed behavior: always returns False, as if the product doesn't exist
        return False

or let's say there's a gradebook class where I want to return fixed grades

class GradeBookStub(GradeBook):
    def get_grades(self):
        # instead of communicating with DB, return fixed values
        return [1.0, 3.0, 2.7]
'''

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
    mock_database_service.product_exists.return_value = False # stubbing
    inventory.add_product(product)
    mock_database_service.save_product.assert_called_once_with(product) # mocking
    assert inventory.get_product_by_id(1) == product

def test_add_product_existing(inventory, mock_database_service, product, mock_notification_service):
    mock_database_service.product_exists.return_value = True # stubbing
    inventory.add_product(product)
    mock_database_service.save_product.assert_not_called() # mocking
    assert inventory.get_product_by_id(1) is None
    assert mock_notification_service.send_notification.called # mocking

def test_update_quantity_above(inventory, mock_database_service, product, mock_notification_service):
    mock_database_service.product_exists.return_value = False # stubbing
    inventory.add_product(product)
    inventory.update_quantity(1, 10)
    mock_database_service.save_product.assert_called_once # mocking
    mock_notification_service.send_notification.assert_not_called() # mocking
    assert product.get_quantity() == 10
    
def test_update_quantity_below(inventory, mock_database_service, product, mock_notification_service):
    mock_database_service.product_exists.return_value = False # stubbing
    inventory.add_product(product)
    inventory.update_quantity(1, 3)
    mock_database_service.save_product.assert_called_once # mocking
    mock_notification_service.send_notification.assert_called_once() # mocking
    assert product.get_quantity() == 3

def test_update_nonexisting(inventory, mock_database_service, product, mock_notification_service):
    inventory.update_quantity(1, 3)
    mock_database_service.save_product.assert_not_called()
    mock_notification_service.send_notification.assert_not_called()
    assert inventory.get_product_by_id(1) is None
