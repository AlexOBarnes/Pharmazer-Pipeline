'''Extracts data from a xml file from an S3 bucket'''
# pylint: disable=import-error
from os import environ as ENV
import logging
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from io import BytesIO
from boto3 import client
import pandas as pd

def format_file_date(filename: str) -> datetime:
    '''Formats the csv file names into the file creation dates'''
    file_date = filename.split('/')[-1].split('-')[0]
    return datetime.strptime(file_date, '%d_%m_%Y')

def extract_alias() -> dict:
    '''Extracts alias data from local csv'''
    return pd.read_csv('aliases.csv')

def find_xml_data(objects: list) -> list:
    '''Uses endwith to find all xml files in an S3 bucket'''
    today = datetime.now() - timedelta(days=1)
    xml_files =  [o for o in objects if o.endswith('.xml') and o.startswith('c13/alex')]
    return [file for file in xml_files if format_file_date(file) > today]

def list_all_objects(bucket_name: str, storage_client) -> list:
    '''Returns all object names from a given bucket'''
    return find_xml_data([objects.get("Key") for objects in
                            storage_client.list_objects(Bucket=bucket_name)["Contents"]])

def download_xml_data(files: list, storage_client) -> pd.DataFrame:
    '''Downloads the specified files and extracts the XML root'''
    xml_data = BytesIO()

    storage_client.download_fileobj(Bucket=ENV["INPUTBUCKET"], Key=files[0], Fileobj=xml_data)
    logging.info("%s downloaded successfully.", files[0].capitalize())

    xml_data.seek(0)
    root = ET.fromstring(xml_data.getvalue())

    return root

def extract_data():
    '''Extracts files from the specified bucket'''
    aws_client = client(service_name="s3",
                        aws_access_key_id=ENV["AWS_ACCESS_KEY"],
                        aws_secret_access_key=ENV["AWS_SECRET_ACCESS_KEY"])
    file_names = list_all_objects(ENV["INPUTBUCKET"], aws_client)
    if file_names:
        logging.info("File found")
    return download_xml_data(file_names, aws_client)

if __name__ == '__main__':
    extract_data()
    extract_alias()
