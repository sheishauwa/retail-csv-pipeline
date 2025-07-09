CREATE DATABASE IF NOT EXISTS retail;

CREATE EXTERNAL TABLE IF NOT EXISTS retail.parquet_sales (
  sale_id string,
  date date,
  region string,
  product_id string,
  quantity int,
  price double,
  total double
)
STORED AS PARQUET
LOCATION 's3://<YourOutputBucket>/';

-- Optional: view for analysis
CREATE OR REPLACE VIEW retail.sales_summary AS
SELECT
  region,
  date,
  SUM(quantity) AS total_qty,
  SUM(total) AS total_sales
FROM retail.parquet_sales
GROUP BY region, date;

