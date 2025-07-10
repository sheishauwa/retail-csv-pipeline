CREATE OR REPLACE VIEW sales_summary AS
SELECT 
    region,
    product,
    date,
    SUM(quantity) AS total_quantity,
    SUM(price * quantity) AS total_sales
FROM 
    "retail_db"."sales_data"
GROUP BY 
    region, product, date;
