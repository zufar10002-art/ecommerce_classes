"""
Tests for Product and Category classes.
"""
import pytest

from main import Category, Product


class TestProduct:
    """Tests for Product class."""
    
    def test_product_initialization(self):
        """Test product creation."""
        product = Product("Test Product", "Test Description", 100.5, 10)
        
        assert product.name == "Test Product"
        assert product.description == "Test Description"
        assert product.price == 100.5
        assert product.quantity == 10
    
    def test_product_with_zero_price(self):
        """Test product with zero price."""
        product = Product("Free Item", "Description", 0.0, 5)
        assert product.price == 0.0
    
    def test_product_with_zero_quantity(self):
        """Test product with zero quantity."""
        product = Product("Out of Stock", "Description", 100.0, 0)
        assert product.quantity == 0


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
        assert len(category.products) == 2
        assert category.products[0] == product1
        assert category.products[1] == product2
    
    def test_category_count_increment(self):
        """Test that category_count increments correctly."""
        assert Category.category_count == 0
        
        category1 = Category("Cat1", "Desc1", [])
        assert Category.category_count == 1
        
        category2 = Category("Cat2", "Desc2", [])
        assert Category.category_count == 2
    
    def test_product_count_increment(self):
        """Test that product_count increments correctly."""
        assert Category.product_count == 0
        
        products1 = [Product("P1", "D1", 10.0, 1), Product("P2", "D2", 20.0, 2)]
        category1 = Category("Cat1", "Desc1", products1)
        assert Category.product_count == 2
        
        products2 = [Product("P3", "D3", 30.0, 3)]
        category2 = Category("Cat2", "Desc2", products2)
        assert Category.product_count == 3
    
    def test_empty_category(self):
        """Test category with no products."""
        category = Category("Empty Cat", "No products", [])
        assert len(category.products) == 0
        assert Category.product_count == 0
