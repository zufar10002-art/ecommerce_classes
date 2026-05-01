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
        """
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price

    @classmethod
    def new_product(cls, product_data: dict) -> 'Product':
        """
        Class method to create a new Product from a dictionary.
        """
        return cls(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            quantity=product_data['quantity']
        )

    def __str__(self) -> str:
        """
        String representation of the product.
        """
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: 'Product') -> float:
        """
        Sum of total costs of two products (price * quantity).
        """
        if type(self) is not type(other):
            raise TypeError(f"Нельзя складывать {type(self).__name__} и {type(other).__name__}")
        return (self.price * self.quantity) + (other.price * other.quantity)


class Smartphone(Product):
    """Class for smartphone products."""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: str, model: str, memory: int, color: str):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self) -> str:
        """String representation of smartphone."""
        base_str = super().__str__()
        return f"{base_str} (Смартфон: {self.model}, {self.memory}ГБ, {self.color})"


class LawnGrass(Product):
    """Class for lawn grass products."""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: str, color: str):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self) -> str:
        """String representation of lawn grass."""
        base_str = super().__str__()
        return f"{base_str} (Газонная трава: {self.country}, срок прорастания {self.germination_period})"


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
        """
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты Product или его наследников")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """
        Getter for products that returns formatted string.
        """
        result = ""
        for product in self.__products:
            result += str(product) + "\n"
        return result.strip()

    def __str__(self) -> str:
        """
        String representation of the category.
        """
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."


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

    smartphone = Smartphone(
        "Samsung Galaxy S23 Ultra",
        "Флагманский смартфон",
        180000.0,
        5,
        "8 ГГц",
        "SM-S918B",
        256,
        "черный"
    )
    category1.add_product(smartphone)
    print("\n" + category1.products)
    print(f"\nTotal categories: {Category.category_count}")
    print(f"Total products: {Category.product_count}")

    grass = LawnGrass(
        "Газон 'Изумруд'",
        "Газон для дачи",
        5000.0,
        10,
        "Россия",
        "7-14 дней",
        "зеленый"
    )
    category2 = Category(
        "Садовые товары",
        "Товары для сада",
        [grass]
    )
    print("\n" + category2.products)

    print("\n--- Testing __add__ with same types ---")
    total = product1 + product2
    print(f"Суммарная стоимость product1 + product2: {total} руб.")

    print("\n--- Testing __add__ with different types ---")
    try:
        result = product1 + grass
        print(f"Результат (не должно было случиться): {result}")
    except TypeError as e:
        print(f"Ошибка: {e}")
