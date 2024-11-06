class Inventory:
    LOW_STOCK_THRESHOLD = 5

    def __init__(self, notification_service, database_service):
        self.notification_service = notification_service
        self.database_service = database_service
        self.products = {}

    def add_product(self, product):
        """
        Add a product to the inventory.
        If the product already exists, send a notification.
        """
        if self.database_service.product_exists(product.get_id()):
            self.notification_service.send_notification(
                f"Product {product.get_name()} already exists in inventory."
            )
            return

        self.products[product.get_id()] = product
        self.database_service.save_product(product)

    def update_quantity(self, product_id, new_quantity):
        """
        Update the quantity of a product.
        If the quantity is below the LOW_STOCK_THRESHOLD, send a notification.
        """
        product = self.products.get(product_id)
        if product:
            product.set_quantity(new_quantity)
            self.database_service.save_product(product)

            if new_quantity < self.LOW_STOCK_THRESHOLD:
                self.notification_service.send_notification(
                    f"Stock for product {product.get_name()} is low: {new_quantity}"
                )

    def get_product_by_id(self, product_id):
        """
        Get a product by its ID.
        """
        return self.products.get(product_id)
