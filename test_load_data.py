# -*- coding: utf-8 -*-
"""
Tests for loading data from JSON.
"""
import json
import os
import tempfile

from load_data import load_categories_from_json
from main import Category


class TestLoadData:
    """Tests for JSON loading function."""

    def test_load_categories_from_json(self):
        """Test loading categories from JSON file."""
        test_data = [
            {
                "name": "Test Category",
                "description": "Test Description",
                "products": [
                    {
                        "name": "Test Product",
                        "description": "Test Product Desc",
                        "price": 99.99,
                        "quantity": 10
                    }
                ]
            }
        ]

        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.json', delete=False, encoding='utf-8'
        ) as f:
            json.dump(test_data, f)
            temp_file = f.name

        try:
            categories = load_categories_from_json(temp_file)

            assert len(categories) == 1
            assert isinstance(categories[0], Category)
            assert categories[0].name == "Test Category"
            assert "Test Product" in categories[0].products
            assert "99.99" in categories[0].products
        finally:
            os.unlink(temp_file)

    def test_load_multiple_categories(self):
        """Test loading multiple categories."""
        test_data = [
            {
                "name": "Category 1",
                "description": "Desc 1",
                "products": []
            },
            {
                "name": "Category 2",
                "description": "Desc 2",
                "products": [
                    {
                        "name": "Product A",
                        "description": "Desc A",
                        "price": 10.0,
                        "quantity": 1
                    }
                ]
            }
        ]

        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.json', delete=False, encoding='utf-8'
        ) as f:
            json.dump(test_data, f)
            temp_file = f.name

        try:
            categories = load_categories_from_json(temp_file)

            assert len(categories) == 2
            assert categories[0].name == "Category 1"
            assert categories[0].products == ""
            assert categories[1].name == "Category 2"
            assert "Product A" in categories[1].products
        finally:
            os.unlink(temp_file)

    def test_load_empty_products(self):
        """Test loading category with empty products list."""
        test_data = [
            {
                "name": "Empty Category",
                "description": "No products",
                "products": []
            }
        ]

        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.json', delete=False, encoding='utf-8'
        ) as f:
            json.dump(test_data, f)
            temp_file = f.name

        try:
            categories = load_categories_from_json(temp_file)
            assert len(categories) == 1
            assert categories[0].name == "Empty Category"
            assert categories[0].products == ""
        finally:
            os.unlink(temp_file)
