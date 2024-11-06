from abc import ABC, abstractmethod


class DatabaseService(ABC):
    @abstractmethod
    def save_product(self, product):
        """
        Save a product to the database.
        """
        pass

    @abstractmethod
    def get_product_by_id(self, product_id):
        """
        Retrieve a product from the database by its ID.
        """
        pass

    @abstractmethod
    def product_exists(self, product_id):
        """
        Check if a product exists in the database by its ID.
        """
        pass
