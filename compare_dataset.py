
import duckdb
import polars as pl
import datacompy
from modular_code import (  # Replace 'your_script' with the actual script filename
    get_monthly_sales,
    get_regional_sales,
    get_ranked_regions,
    get_product_sales,
    get_final_result,
    read_base_tables
)

def run_duckdb_query(db_path: str = './database.db', query_file: str = './messy_query.sql') -> pl.DataFrame:
    """
    Executes a DuckDB query and returns the result as a Polars DataFrame.
    """
    con = duckdb.connect(db_path)
    with open(query_file, 'r') as f:
        query = f.read()
        
    result = con.sql(query).pl()  # Fetch result as Polars DataFrame
    con.close()
    return result

def compare_dataframes(df1: pl.DataFrame, df2: pl.DataFrame, join_columns: list):
    """
    Compares two Polars DataFrames using datacompy.
    Converts Polars DataFrames to Pandas before comparison.
    """
    df1_pd = df1.to_pandas()
    df2_pd = df2.to_pandas()

    comparison = datacompy.Compare(
        df1_pd, df2_pd, join_columns=join_columns, cast_column_names_lower=False
    )

    return comparison.report()

if __name__ == "__main__":
    # Run DuckDB query and load data into Polars
    df_duckdb = run_duckdb_query()

    db_path = "database.db"
    orders, products, regions = read_base_tables(db_path)
    
    monthly_sales = get_monthly_sales(orders)
    regional_sales = get_regional_sales(monthly_sales)
    ranked_regions = get_ranked_regions(regional_sales)
    product_sales = get_product_sales(monthly_sales, products)
    final_result = get_final_result(product_sales, ranked_regions, regions)
    df_other = final_result.select(pl.col("month"), pl.col("product_name"), pl.col("category"), pl.col("region_name"), pl.col("product_sales"), pl.col("regional_sales").alias("region_total_sales"), pl.col("sales_rank"))

    # Compare the two DataFrames
    report = compare_dataframes(df_duckdb, df_other, join_columns=["month", "product_name", "region_name"])
    
    print(report)
