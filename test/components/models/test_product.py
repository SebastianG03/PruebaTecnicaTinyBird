import pytest
from app.entities.models.product import ProductPopularity


def test_product_popularity_creation():
    """Creacion con datos validos"""
    product = ProductPopularity(
        product_id="p_123", price=99.99, purchases=5, views=42, revenue=499.95
    )

    assert product.product_id == "p_123"
    assert product.price == 99.99
    assert product.purchases == 5
    assert product.views == 42
    assert product.revenue == 499.95


def test_invalid_data_product_popularity():
    with pytest.raises(ValueError) as exc_info:
        ProductPopularity(
            product_id="p_123", price=-99.99, purchases=5, views=42, revenue=499.95
        )
    assert len(str(exc_info.value)) > 0
