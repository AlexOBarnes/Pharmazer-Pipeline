'''Functions that connect to AWS and send an email via SES'''
from os import environ as ENV
from boto3 import client

def send_email(start: bool, date: str) -> None:
    '''Sends an email using SES to a specified email address'''
    ses = client("ses", aws_access_key_id=ENV["AWS_ACCESS_KEY"],
                 aws_secret_access_key=ENV["AWS_SECRET_ACCESS_KEY"],
                 region_name="eu-west-2")
    if start:
        text = "A file has been added to your S3 bucket. Data processing has begun"
        subject = f"Pipeline Run {date}"
    else:
        text = '''Data processing has been completed,
        the clean data has been uploaded to your output S3 bucket'''
        subject = f"Pipeline Complete {date}"


    ses.send_email(Source=ENV['FROM'],
        Destination={'ToAddresses': [ENV['TO']]},
        Message={'Subject': {'Data': subject},
            'Body': {'Text': {'Data': text}}})

if __name__ == '__main__':
    send_email(True,'10')
