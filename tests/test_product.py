import pytest
from inventory_system.product import Product

@pytest.fixture
def product():
    return Product(1, "Test Product", 10)

def test_get_id(product):
    assert product.get_id() == 1

def test_get_name(product):
    assert product.get_name() == "Test Product"

def test_get_quantity(product):
    assert product.get_quantity() == 10

def test_set_quantity(product):
    product.set_quantity(20)
    assert product.get_quantity() == 20