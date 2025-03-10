
import pytest
import polars as pl
from modular_code import (  # Replace 'your_script' with the actual script filename
    get_monthly_sales,
    get_regional_sales,
    get_ranked_regions,
    get_product_sales,
    get_final_result,
)
import datetime

@pytest.fixture
def sample_orders():
    return pl.DataFrame({
        "order_id": [1, 2, 3, 4, 5],
        "order_date": pl.Series(
            [datetime.date(2024, 1, 5), datetime.date(2024, 1, 10), 
             datetime.date(2024, 2, 15), datetime.date(2024, 2, 20), 
             datetime.date(2024, 3, 25)], dtype=pl.Date
        ),
        "product_id": [101, 102, 101, 103, 104],
        "region_id": [1, 1, 2, 2, 3],
        "sales_amount": [500.0, 300.0, 700.0, 600.0, 400.0]
    })

@pytest.fixture
def sample_products():
    return pl.DataFrame({
        "product_id": [101, 102, 103, 104],
        "product_name": ["Product A", "Product B", "Product C", "Product D"],
        "category": ["Category 1", "Category 2", "Category 1", "Category 3"]
    })

@pytest.fixture
def sample_regions():
    return pl.DataFrame({
        "region_id": [1, 2, 3],
        "region_name": ["North America", "Europe", "Asia"]
    })

def test_get_monthly_sales(sample_orders):
    result = get_monthly_sales(sample_orders)
    
    assert result.shape[0] > 0
    assert "month" in result.columns
    assert "total_sales" in result.columns
    assert "order_count" in result.columns

def test_get_regional_sales(sample_orders):
    monthly_sales = get_monthly_sales(sample_orders)
    result = get_regional_sales(monthly_sales)

    assert result.shape[0] > 0
    assert "regional_sales" in result.columns
    assert "regional_orders" in result.columns

def test_get_ranked_regions(sample_orders):
    monthly_sales = get_monthly_sales(sample_orders)
    regional_sales = get_regional_sales(monthly_sales)
    result = get_ranked_regions(regional_sales)

    assert result.shape[0] > 0
    assert "sales_rank" in result.columns
    assert result["sales_rank"].min() == 1  # Rank should start from 1

def test_get_product_sales(sample_orders, sample_products):
    monthly_sales = get_monthly_sales(sample_orders)
    result = get_product_sales(monthly_sales, sample_products)

    assert result.shape[0] > 0
    assert "product_sales" in result.columns
    assert "product_name" in result.columns

def test_get_final_result(sample_orders, sample_products, sample_regions):
    monthly_sales = get_monthly_sales(sample_orders)
    regional_sales = get_regional_sales(monthly_sales)
    ranked_regions = get_ranked_regions(regional_sales)
    product_sales = get_product_sales(monthly_sales, sample_products)
    result = get_final_result(product_sales, ranked_regions, sample_regions)

    assert result.shape[0] > 0
    assert "region_name" in result.columns
    assert "sales_rank" in result.columns
    assert result["sales_rank"].max() <= 5  # Ensuring top 5 ranks only
