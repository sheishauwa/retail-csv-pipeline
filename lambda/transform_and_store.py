import boto3
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import io

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    # Get the uploaded file details
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    obj = s3.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(obj['Body'])

    # Basic cleaning
    df.dropna(inplace=True)  # remove rows with missing values
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])  # remove rows with invalid dates

    # Convert to Parquet
    table = pa.Table.from_pandas(df)
    out_buffer = io.BytesIO()
    pq.write_table(table, out_buffer)

    # Upload to processed bucket
    processed_key = key.replace('.csv', '.parquet')
    s3.put_object(
        Bucket='retail-parquet-data',
        Key=processed_key,
        Body=out_buffer.getvalue()
    )

    return {'statusCode': 200, 'body': 'Transformation complete'}
