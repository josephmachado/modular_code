
import duckdb
import polars as pl

def read_base_tables(db_path: str):
    con = duckdb.connect(db_path)
    
    orders = con.sql("SELECT * FROM orders").pl()
    products = con.sql("SELECT * FROM products").pl()
    regions = con.sql("SELECT * FROM regions").pl()
    
    con.close()
    return orders, products, regions

def get_monthly_sales(orders: pl.DataFrame) -> pl.DataFrame:
    return (
        orders
        .with_columns(pl.col("order_date").dt.truncate("1mo").alias("month"))
        .group_by(["month", "product_id", "region_id"])
        .agg([
            pl.col("sales_amount").sum().alias("total_sales"),
            pl.col("order_id").count().alias("order_count")
        ])
    )

def get_regional_sales(monthly_sales: pl.DataFrame) -> pl.DataFrame:
    return (
        monthly_sales
        .group_by(["month", "region_id"])
        .agg([
            pl.col("total_sales").sum().alias("regional_sales"),
            pl.col("order_count").sum().alias("regional_orders")
        ])
    )

def get_ranked_regions(regional_sales: pl.DataFrame) -> pl.DataFrame:
    return (
        regional_sales
        .with_columns(
            pl.col("regional_sales")
            .rank("dense", descending=True)
            .over("month")
            .alias("sales_rank")
        )
    )

def get_product_sales(monthly_sales: pl.DataFrame, products: pl.DataFrame) -> pl.DataFrame:
    return (
        monthly_sales
        .join(products, on="product_id", how="inner")
        .select(["month", "product_id", "product_name", "category", "region_id", "total_sales"])
        .rename({"total_sales": "product_sales"})
    )

def get_final_result(product_sales: pl.DataFrame, ranked_regions: pl.DataFrame, regions: pl.DataFrame) -> pl.DataFrame:
    return (
        product_sales
        .join(ranked_regions, on=["month", "region_id"], how="inner")
        .join(regions, on="region_id", how="inner")
        .filter(pl.col("sales_rank") <= 5)
        .sort(["month", "sales_rank", "product_sales"], descending=[True, False, True])
    )

if __name__ == "__main__":
    db_path = "database.db"
    orders, products, regions = read_base_tables(db_path)
    
    monthly_sales = get_monthly_sales(orders)
    regional_sales = get_regional_sales(monthly_sales)
    ranked_regions = get_ranked_regions(regional_sales)
    product_sales = get_product_sales(monthly_sales, products)
    final_result = get_final_result(product_sales, ranked_regions, regions)
    print(final_result.select(pl.col("month"), pl.col("product_name"), pl.col("category"), pl.col("region_name"), pl.col("product_sales"), pl.col("regional_sales").alias("region_total_sales"), pl.col("sales_rank")))
