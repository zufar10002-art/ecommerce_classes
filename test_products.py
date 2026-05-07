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
        assert product.price == 100.5
        assert product.quantity == 10

    def test_product_zero_quantity_raises_error(self):
        """Test that creating product with quantity=0 raises ValueError."""
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            Product("Bad Product", "Description", 100.0, 0)

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
        assert product.price == 299.99

    def test_product_str(self):
        """Test __str__ method of Product."""
        product = Product("TestPhone", "Desc", 500.0, 3)
        assert "TestPhone" in str(product)
        assert "500.0" in str(product)

    def test_product_add_same_type(self):
        """Test __add__ with same type products."""
        p1 = Product("A", "", 100.0, 2)
        p2 = Product("B", "", 200.0, 3)
        assert p1 + p2 == 800.0

    def test_product_add_different_type_raises_error(self):
        """Test __add__ raises TypeError for different classes."""
        p = Product("Phone", "", 100.0, 2)
        g = LawnGrass("Grass", "", 50.0, 10, "RU", "7 days", "green")
        with pytest.raises(TypeError, match="Нельзя складывать Product и LawnGrass"):
            _ = p + g


class TestSmartphone:
    """Tests for Smartphone class."""

    def test_smartphone_initialization(self):
        """Test smartphone creation."""
        phone = Smartphone("Samsung", "", 100000.0, 5,
                           "8 GHz", "S23", 256, "black")
        assert phone.name == "Samsung"
        assert phone.efficiency == "8 GHz"
        assert phone.model == "S23"
        assert phone.memory == 256
        assert phone.color == "black"

    def test_smartphone_str(self):
        """Test __str__ method of Smartphone."""
        phone = Smartphone("Samsung", "", 100000.0, 5,
                           "8 GHz", "S23", 256, "black")
        assert "Смартфон" in str(phone)


class TestLawnGrass:
    """Tests for LawnGrass class."""

    def test_lawn_grass_initialization(self):
        """Test lawn grass creation."""
        grass = LawnGrass("Grass", "", 5000.0, 10,
                          "Russia", "7-14 days", "green")
        assert grass.name == "Grass"
        assert grass.country == "Russia"
        assert grass.germination_period == "7-14 days"
        assert grass.color == "green"

    def test_lawn_grass_str(self):
        """Test __str__ method of LawnGrass."""
        grass = LawnGrass("Grass", "", 5000.0, 10,
                          "Russia", "7-14 days", "green")
        assert "Газонная трава" in str(grass)


class TestCategory:
    """Tests for Category class."""

    def setup_method(self):
        """Reset class counters before each test."""
        Category.category_count = 0
        Category.product_count = 0

    def test_add_product_valid(self):
        """Test add_product with valid Product."""
        cat = Category("Test", "", [])
        prod = Product("P", "", 100.0, 5)
        cat.add_product(prod)
        assert "P" in cat.products

    def test_add_product_invalid_raises_error(self):
        """Test add_product raises TypeError for non-Product."""
        cat = Category("Test", "", [])
        with pytest.raises(TypeError, match="Можно добавлять только объекты Product"):
            cat.add_product("not a product")

    def test_middle_price_with_products(self):
        """Test middle_price returns correct average."""
        p1 = Product("A", "", 100.0, 2)
        p2 = Product("B", "", 200.0, 3)
        cat = Category("Test", "", [p1, p2])
        assert cat.middle_price() == 150.0

    def test_middle_price_empty_category(self):
        """Test middle_price returns 0 for empty category."""
        cat = Category("Empty", "", [])
        assert cat.middle_price() == 0

    def test_category_str(self):
        """Test __str__ method of Category."""
        p1 = Product("A", "", 100.0, 2)
        p2 = Product("B", "", 200.0, 3)
        cat = Category("Electronics", "", [p1, p2])
        assert "Electronics, количество продуктов: 5 шт." in str(cat)
