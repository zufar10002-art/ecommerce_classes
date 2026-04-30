# -*- coding: utf-8 -*-
"""
Module with Product and Category classes for online store.
"""


class Product:
    """Class for product representation."""

    def __init__(self, name: str, description: str,
                 price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Getter for price."""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """
        Setter for price with validation.

        Args:
            new_price: New price value
        """
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price

    @classmethod
    def new_product(cls, product_data: dict) -> 'Product':
        """
        Class method to create a new Product from a dictionary.

        Args:
            product_data: Dictionary with keys 'name', 'description', 'price', 'quantity'

        Returns:
            Product instance
        """
        return cls(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            quantity=product_data['quantity']
        )


class Category:
    """Class for category representation."""

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list = None):
        self.name = name
        self.description = description
        self.__products = products if products is not None else []

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product: Product) -> None:
        """
        Add a product to the category.

        Args:
            product: Product object to add
        """
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """
        Getter for products that returns formatted string.

        Returns:
            String with all products in format: "Product name, X rub. Stock: X pcs.\n"
        """
        result = ""
        for product in self.__products:
            result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return result.strip()


if __name__ == "__main__":
    product1 = Product(
        "Samsung Galaxy S23 Ultra",
        "256GB, Gray, 200MP camera",
        180000.0,
        5
    )
    product2 = Product(
        "Iphone 15",
        "512GB, Gray space",
        210000.0,
        8
    )
    product3 = Product(
        "Xiaomi Redmi Note 11",
        "1024GB, Blue",
        31000.0,
        14
    )

    category1 = Category(
        "Smartphones",
        "Smartphones for communication",
        [product1, product2, product3]
    )

    print(category1.products)
    print(f"\nTotal categories: {Category.category_count}")
    print(f"Total products: {Category.product_count}")

    product4 = Product(
        "55\" QLED 4K",
        "Backlight",
        123000.0,
        7
    )
    category1.add_product(product4)
    print("\n" + category1.products)
    print(f"\nTotal categories: {Category.category_count}")
    print(f"Total products: {Category.product_count}")

    # Тестируем класс-метод new_product
    print("\n--- Testing new_product classmethod ---")
    product_data = {
        "name": "Test Phone",
        "description": "Test description",
        "price": 999.99,
        "quantity": 100
    }
    test_product = Product.new_product(product_data)
    print(f"Created product: {test_product.name}, {test_product.price} руб.")

    # Тестируем сеттер цены
    print("\n--- Testing price setter ---")
    print(f"Current price: {test_product.price}")
    test_product.price = 500
    print(f"New price after setting 500: {test_product.price}")
    test_product.price = -100
    print(f"Price after trying to set -100: {test_product.price}")
    test_product.price = 0
    print(f"Price after trying to set 0: {test_product.price}")
