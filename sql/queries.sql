-- 1. Total Revenue
SELECT 
    SUM(sales) as total_revenue 
FROM 
    sales;

-- 2. Orders per Month
SELECT 
    order_year_month, 
    COUNT(DISTINCT order_id) as total_orders 
FROM 
    sales 
GROUP BY 
    order_year_month 
ORDER BY 
    order_year_month;

-- 3. Top Customers (by total spend)
SELECT 
    customer_name, 
    SUM(sales) as total_spent 
FROM 
    sales 
GROUP BY 
    customer_name 
ORDER BY 
    total_spent DESC 
LIMIT 10;

-- 4. Top Selling Products (by quantity)
SELECT 
    category, 
    SUM(quantity) as total_items_sold 
FROM 
    sales 
WHERE 
    category != 'unknown'
GROUP BY 
    category 
ORDER BY 
    total_items_sold DESC 
LIMIT 10;

-- 5. Sales by Region
SELECT 
    region, 
    SUM(sales) as total_sales,
    COUNT(DISTINCT order_id) as total_orders
FROM 
    sales 
GROUP BY 
    region 
ORDER BY 
    total_sales DESC;
