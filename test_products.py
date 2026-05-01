# -*- coding: utf-8 -*-
"""
Tests for Product and Category classes.
"""
import pytest

from main import Category, LawnGrass, Product, Smartphone


class TestProduct:
    """Tests for Product class."""

    def test_product_initialization(self):
        """Test product creation."""
        product = Product("Test Product", "Test Description", 100.5, 10)

        assert product.name == "Test Product"
        assert product.description == "Test Description"
        assert product.price == 100.5
        assert product.quantity == 10

    def test_product_price_getter(self):
        """Test price getter returns correct value."""
        product = Product("Test", "Desc", 99.99, 5)
        assert product.price == 99.99

    def test_product_price_setter_positive(self):
        """Test price setter with positive value."""
        product = Product("Test", "Desc", 100.0, 5)
        product.price = 150.0
        assert product.price == 150.0

    def test_product_price_setter_zero(self, capsys):
        """Test price setter with zero value."""
        product = Product("Test", "Desc", 100.0, 5)
        product.price = 0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 100.0

    def test_product_price_setter_negative(self, capsys):
        """Test price setter with negative value."""
        product = Product("Test", "Desc", 100.0, 5)
        product.price = -50.0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 100.0

    def test_new_product_classmethod(self):
        """Test new_product class method creates product from dict."""
        product_data = {
            "name": "Classmethod Product",
            "description": "Created from dict",
            "price": 299.99,
            "quantity": 50
        }
        product = Product.new_product(product_data)

        assert product.name == "Classmethod Product"
        assert product.description == "Created from dict"
        assert product.price == 299.99
        assert product.quantity == 50

    def test_product_str(self):
        """Test __str__ method of Product."""
        product = Product("TestPhone", "Desc", 500.0, 3)
        expected = "TestPhone, 500.0 руб. Остаток: 3 шт."
        assert str(product) == expected

    def test_product_add_same_type(self):
        """Test __add__ method with same type products."""
        product1 = Product("Phone", "Desc", 100.0, 2)
        product2 = Product("Tablet", "Desc", 200.0, 3)
        total = product1 + product2
        assert total == 800.0

    def test_product_add_different_type_raises_error(self):
        """Test __add__ raises TypeError when adding different class types."""
        product = Product("Phone", "Desc", 100.0, 2)
        grass = LawnGrass("Grass", "Desc", 50.0, 10, "Russia", "7 days", "green")
        with pytest.raises(TypeError, match="Нельзя складывать Product и LawnGrass"):
            _ = product + grass


class TestSmartphone:
    """Tests for Smartphone class."""

    def test_smartphone_initialization(self):
        """Test smartphone creation with all attributes."""
        phone = Smartphone(
            "Samsung", "Flagship", 100000.0, 5,
            "8 ГГц", "SM-S918B", 256, "черный"
        )
        assert phone.name == "Samsung"
        assert phone.price == 100000.0
        assert phone.quantity == 5
        assert phone.efficiency == "8 ГГц"
        assert phone.model == "SM-S918B"
        assert phone.memory == 256
        assert phone.color == "черный"

    def test_smartphone_str(self):
        """Test __str__ method of Smartphone."""
        phone = Smartphone(
            "Samsung", "Flagship", 100000.0, 5,
            "8 ГГц", "SM-S918B", 256, "черный"
        )
        assert "Смартфон" in str(phone)
        assert "SM-S918B" in str(phone)
        assert "256" in str(phone)


class TestLawnGrass:
    """Tests for LawnGrass class."""

    def test_lawn_grass_initialization(self):
        """Test lawn grass creation with all attributes."""
        grass = LawnGrass(
            "Изумруд", "For garden", 5000.0, 10,
            "Россия", "7-14 дней", "зеленый"
        )
        assert grass.name == "Изумруд"
        assert grass.price == 5000.0
        assert grass.quantity == 10
        assert grass.country == "Россия"
        assert grass.germination_period == "7-14 дней"
        assert grass.color == "зеленый"

    def test_lawn_grass_str(self):
        """Test __str__ method of LawnGrass."""
        grass = LawnGrass(
            "Изумруд", "For garden", 5000.0, 10,
            "Россия", "7-14 дней", "зеленый"
        )
        assert "Газонная трава" in str(grass)
        assert "Россия" in str(grass)


class TestCategory:
    """Tests for Category class."""

    def setup_method(self):
        """Reset class counters before each test."""
        Category.category_count = 0
        Category.product_count = 0

    def test_category_initialization(self):
        """Test category creation."""
        product1 = Product("Product 1", "Desc1", 10.0, 5)
        product2 = Product("Product 2", "Desc2", 20.0, 3)
        products = [product1, product2]

        category = Category("Test Category", "Test Description", products)

        assert category.name == "Test Category"
        assert category.description == "Test Description"

    def test_private_products_attribute(self):
        """Test that products attribute is private."""
        category = Category("Test", "Desc", [])
        with pytest.raises(AttributeError):
            _ = category.__products

    def test_add_product_valid(self):
        """Test add_product with valid Product object."""
        category = Category("Test", "Desc", [])
        product = Product("New", "Desc", 50.0, 10)
        category.add_product(product)
        assert "New" in category.products

    def test_add_product_invalid_raises_error(self):
        """Test add_product raises TypeError when adding non-Product."""
        category = Category("Test", "Desc", [])
        with pytest.raises(TypeError, match="Можно добавлять только объекты Product или его наследников"):
            category.add_product("not a product")

    def test_add_product_with_smartphone(self):
        """Test add_product with Smartphone object."""
        category = Category("Test", "Desc", [])
        phone = Smartphone(
            "Samsung", "Flagship", 100000.0, 5,
            "8 ГГц", "SM-S918B", 256, "черный"
        )
        category.add_product(phone)
        assert "Смартфон" in category.products

    def test_add_product_increments_product_count(self):
        """Test that add_product increments product_count."""
        Category.category_count = 0
        Category.product_count = 0

        Category("Test", "Desc", [])
        assert Category.product_count == 0

        product = Product("New", "Desc", 50.0, 10)
        category = Category("Test2", "Desc2", [])
        category.add_product(product)
        assert Category.product_count == 1

    def test_products_getter_format(self):
        """Test that products getter returns formatted string."""
        product = Product("TestPhone", "Desc", 500.0, 3)
        category = Category("Test", "Desc", [product])
        result = category.products
        assert "TestPhone" in result
        assert "500.0" in result
        assert "руб." in result
        assert "3" in result

    def test_category_count_increment(self):
        """Test that category_count increments correctly."""
        assert Category.category_count == 0

        Category("Cat1", "Desc1", [])
        assert Category.category_count == 1

        Category("Cat2", "Desc2", [])
        assert Category.category_count == 2

    def test_product_count_increment_on_init(self):
        """Test that product_count increments correctly on initialization."""
        assert Category.product_count == 0

        products1 = [Product("P1", "D1", 10.0, 1), Product("P2", "D2", 20.0, 2)]
        Category("Cat1", "Desc1", products1)
        assert Category.product_count == 2

        products2 = [Product("P3", "D3", 30.0, 3)]
        Category("Cat2", "Desc2", products2)
        assert Category.product_count == 3

    def test_empty_category(self):
        """Test category with no products."""
        category = Category("Empty Cat", "No products", [])
        assert category.products == ""
        assert Category.product_count == 0

    def test_products_getter_returns_string(self):
        """Test that products getter returns a string."""
        category = Category("Test", "Desc", [])
        assert isinstance(category.products, str)

    def test_category_str(self):
        """Test __str__ method of Category."""
        product1 = Product("Phone", "Desc", 100.0, 2)
        product2 = Product("Tablet", "Desc", 200.0, 3)
        category = Category("Electronics", "Devices", [product1, product2])
        expected = "Electronics, количество продуктов: 5 шт."
        assert str(category) == expected

    def test_category_str_empty(self):
        """Test __str__ method of Category with no products."""
        category = Category("Empty", "Nothing", [])
        expected = "Empty, количество продуктов: 0 шт."
        assert str(category) == expected
