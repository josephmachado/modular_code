-- Create orders table
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    order_date DATE,
    product_id INTEGER,
    region_id INTEGER,
    sales_amount DECIMAL(10,2)
);

-- Create products table
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT
);

-- Create regions table
CREATE TABLE regions (
    region_id INTEGER PRIMARY KEY,
    region_name TEXT
);

-- Insert sample data into orders table
INSERT INTO orders (order_id, order_date, product_id, region_id, sales_amount) VALUES
(1, '2024-01-05', 101, 1, 500.00),
(2, '2024-01-10', 102, 2, 300.00),
(3, '2024-01-15', 103, 3, 700.00),
(4, '2024-02-05', 101, 1, 600.00),
(5, '2024-02-10', 102, 2, 400.00),
(6, '2024-02-15', 103, 3, 800.00);

-- Insert sample data into products table
INSERT INTO products (product_id, product_name, category) VALUES
(101, 'Product A', 'Category 1'),
(102, 'Product B', 'Category 2'),
(103, 'Product C', 'Category 3');

-- Insert sample data into regions table
INSERT INTO regions (region_id, region_name) VALUES
(1, 'North America'),
(2, 'Europe'),
(3, 'Asia');
