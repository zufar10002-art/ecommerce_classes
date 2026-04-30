"""
Module for loading data from JSON file.
"""
import json

from main import Category, Product


def load_categories_from_json(file_path: str) -> list:
    """
    Load categories and products from JSON file.

    Args:
        file_path: Path to JSON file

    Returns:
        List of Category objects
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    categories = []

    for category_data in data:
        products = []
        for product_data in category_data['products']:
            product = Product(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                quantity=product_data['quantity']
            )
            products.append(product)

        category = Category(
            name=category_data['name'],
            description=category_data['description'],
            products=products
        )
        categories.append(category)

    return categories


if __name__ == "__main__":
    categories = load_categories_from_json('products.json')
    for cat in categories:
        print(f"Category: {cat.name}")
        print(f"Description: {cat.description}")
        print(f"Products count: {len(cat.products)}")
        for product in cat.products:
            print(f"  - {product.name}: {product.price} rub, "
                  f"{product.quantity} pcs")
        print()
