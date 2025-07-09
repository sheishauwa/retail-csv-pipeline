import os
import boto3
import pandas as pd
import io

s3 = boto3.client('s3')
OUTPUT_BUCKET = os.getenv('OUTPUT_BUCKET')

def lambda_handler(event, context):
    for rec in event['Records']:
        bucket = rec['s3']['bucket']['name']
        key = rec['s3']['object']['key']

        resp = s3.get_object(Bucket=bucket, Key=key)
        df = pd.read_csv(io.BytesIO(resp['Body'].read()))

        # Simple cleaning:
        df = df.dropna(subset=['sale_id','date','region','product_id','quantity','price'])
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0).astype(int)
        df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0.0)

        # Add total
        df['total'] = df['quantity'] * df['price']

        # Convert to Parquet
        out_buffer = io.BytesIO()
        df.to_parquet(out_buffer, index=False)

        out_key = key.replace('.csv', '.parquet')
        s3.put_object(Bucket=OUTPUT_BUCKET, Key=out_key, Body=out_buffer.getvalue())

    return {'status': 'success'}
