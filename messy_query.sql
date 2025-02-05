WITH
monthly_sales AS (
    SELECT
        DATE_TRUNC('month', order_date) AS month,
        product_id,
        region_id,
        SUM(sales_amount) AS total_sales,
        COUNT(*) AS order_count
    FROM orders
    GROUP BY 1, 2, 3
),

regional_sales AS (
    SELECT
        ms.month,
        ms.region_id,
        SUM(ms.total_sales) AS regional_sales,
        SUM(ms.order_count) AS regional_orders
    FROM monthly_sales ms
    GROUP BY 1, 2
),

ranked_regions AS (
    SELECT
        rs.month,
        rs.region_id,
        rs.regional_sales,
        RANK() OVER (
            PARTITION BY rs.month
            ORDER BY rs.regional_sales DESC
        ) AS sales_rank
    FROM regional_sales rs
),

product_sales AS (
    SELECT
        ms.month,
        p.product_id,
        p.product_name,
        p.category,
        ms.region_id,
        ms.total_sales AS product_sales
    FROM monthly_sales ms
    JOIN products p ON ms.product_id = p.product_id
)

SELECT
    ps.month,
    ps.product_name,
    ps.category,
    r.region_name,
    ps.product_sales,
    rr.regional_sales AS region_total_sales,
    rr.sales_rank
FROM product_sales ps
JOIN ranked_regions rr
    ON ps.month = rr.month
    AND ps.region_id = rr.region_id
JOIN regions r
    ON ps.region_id = r.region_id
WHERE rr.sales_rank <= 5  -- Only show top 5 regions per month
ORDER BY ps.month DESC, rr.sales_rank, ps.product_sales DESC;
