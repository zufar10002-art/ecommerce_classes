"""
Module with Product and Category classes for online store.
"""


class Product:
    """Class for product representation."""

    def __init__(self, name: str, description: str,
                 price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Class for category representation."""

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.products = products

        Category.category_count += 1
        Category.product_count += len(products)


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

    print(f"Category: {category1.name}")
    print(f"Description: {category1.description}")
    print(f"Products count in category: {len(category1.products)}")
    print(f"Total categories: {Category.category_count}")
    print(f"Total products: {Category.product_count}")

    product4 = Product(
        "55\" QLED 4K",
        "Backlight",
        123000.0,
        7
    )
    category2 = Category(
        "TVs",
        "Modern televisions",
        [product4]
    )

    print(f"\nCategory: {category2.name}")
    print(f"Products count: {len(category2.products)}")
    print(f"Total categories: {Category.category_count}")
    print(f"Total products: {Category.product_count}")
