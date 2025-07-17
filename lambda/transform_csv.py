import boto3
import pandas as pd
import io
import pyarrow as pa
import pyarrow.parquet as pq

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key    = event['Records'][0]['s3']['object']['key']

    obj = s3.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(obj['Body'])

    # Clean missing values
    df.fillna(0, inplace=True)

    # Convert to Parquet
    table = pa.Table.from_pandas(df)
    buffer = io.BytesIO()
    pq.write_table(table, buffer)

    # Save transformed file
    s3.put_object(
        Bucket=bucket,
        Key=f'processed/{key.replace(".csv", ".parquet")}',
        Body=buffer.getvalue()
    )

    return {"status": "done", "file": key}

