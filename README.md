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
