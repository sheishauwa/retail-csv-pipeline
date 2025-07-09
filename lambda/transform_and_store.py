import os
import boto3
import csv
import io
import json

s3 = boto3.client('s3')
OUTPUT_BUCKET = os.environ['OUTPUT_BUCKET']

def lambda_handler(event, context):
    for rec in event['Records']:
        bucket = rec['s3']['bucket']['name']
        key = rec['s3']['object']['key']

        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8').splitlines()
        reader = csv.DictReader(content)

        # Prepare cleaned data
        cleaned_rows = []
        for row in reader:
            if all(row.get(k) for k in ['sale_id','date','region','product_id','quantity','price']):
                try:
                    quantity = int(float(row['quantity']))
                    price = float(row['price'])
                    row['total'] = round(quantity * price, 2)
                    cleaned_rows.append(row)
                except:
                    continue

        # Convert to JSON and upload
        out_key = key.replace('.csv', '.json')
        json_data = json.dumps(cleaned_rows)

        s3.put_object(Bucket=OUTPUT_BUCKET, Key=out_key, Body=json_data)

    return {'status': 'success'}
