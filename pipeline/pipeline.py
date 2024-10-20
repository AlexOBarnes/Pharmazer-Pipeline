'''An ETL pipeline that takes data from XML and converts it to a pandas dataframe'''
#pylint: disable=import-error,E0001
from os import environ as ENV
from datetime import datetime as dt
import logging
import argparse
from dotenv import load_dotenv
from transform import transform,wrangle_data
from extract import extract_data
from load import load_to_csv
from message import send_email

def get_date() -> str:
    '''Returns the current date'''
    return dt.now().strftime('%d-%m-%Y_%H:%M:%S')

def config_log() -> None:
    '''Configures the log'''
    date = get_date()
    logging.basicConfig(filename=f'pipeline_{date}.log',
                        encoding='UTF-8', level=logging.WARNING)

def parse_arguments() -> None:
    '''Parses CL arguments'''
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", "-l", action='store_true')
    args = parser.parse_args()

    log = args.log
    if log:
        config_log()
    else:
        logging.basicConfig(level=logging.INFO)

def pipeline() -> None:
    '''Extracts and Transforms the data from an XML file into a pandas dataframe'''
    send_email(True,get_date())
    logging.info('Email update sent.')
    data = extract_data()
    if data:
        logging.info('Data extracted.')
        pubmed_df = transform(data)
    if not pubmed_df.empty:
        logging.info('Data transformation complete.')
        pubmed_df = wrangle_data(pubmed_df)
    if not pubmed_df.empty:
        logging.info('Data processing complete.')
    load_to_csv(pubmed_df)
    logging.info('File uploaded successfully')
    send_email(False,get_date())
    logging.info('Email update sent.')

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    parse_arguments()
    load_dotenv()
    pipeline()
