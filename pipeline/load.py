'''Loads a pandas dataframe to a csv'''
# pylint: disable=import-error
from os import environ as ENV
from io import StringIO
from datetime import datetime as dt
from boto3 import client
import pandas as pd

def load_to_csv(data: pd.DataFrame) -> None:
    '''Loads a dataframe to a csv and uploads it to a given S3 bucket'''
    aws_client = client(service_name="s3",
                        aws_access_key_id=ENV["AWS_ACCESS_KEY"],
                        aws_secret_access_key=ENV["AWS_SECRET_ACCESS_KEY"])

    date = dt.now().strftime('%d-%m-%Y')
    csv_file = StringIO()
    data.to_csv(csv_file, index=False)
    encoded_csv= csv_file.getvalue().encode('UTF-8')

    aws_client.put_object(Bucket=ENV["OUTPUTBUCKET"],
                          Key=f'c13/alex/sjogren-data-{date}.csv', Body=encoded_csv)

if __name__ == '__main__':
    load_to_csv(pd.DataFrame())
