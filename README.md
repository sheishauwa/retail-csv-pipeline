# Retail CSV to Parquet Pipeline

## Setup
1. Create Input / Output / AthenaResults bucket.
2. Add them to GitHub Secrets (`INPUT_BUCKET`, `OUTPUT_BUCKET`, `ATHENA_RESULTS_BUCKET`).
3. `aws configure` locally for testing.

## Workflow
- Push to `main`: Lambda zip uploaded, CF deployed
- Upload CSV to Input bucket → Lambda auto-triggers → Parquet written to Output bucket
- Run Athena SQL to create external table
- Build QuickSight Dashboard using Athena table

## Testing
Upload `sales_sample.csv` from `sample-data/` to Input bucket. Verify Parquet appears in Output.

## Athena
Run:
```bash
$ aws athena start-query-execution --... --query-string "$(cat athena/create_sales_view.sql)"

# Retail CSV to Parquet Pipeline

This project automates the process of:

- Ingesting CSV files uploaded to S3
- Cleaning and transforming the data
- Converting the data to Parquet format
- Storing results in an S3 output bucket
- Querying with AWS Athena
- Visualizing with Amazon QuickSight

## 🔄 Last Updated

Deployment triggered on: **$(date)**  <!-- Trigger deployment -->
