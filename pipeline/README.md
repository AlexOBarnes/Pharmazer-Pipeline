# Pharmazer pipeline
Contains the code for the ETL pipeline of this project.

## Installation
1. Install the required Python packages:

```bash
pip install -r requirements.txt
```
Requirements.txt file includes all dependencies including: `spaCy`, `pandas`, and `python-dotenv`.

2. To install the `spaCy` model further steps are required, different sizes of models are available. The medium model was used for this project
```bash
python -m spacy download en_core_web_md
```

3. If you wish to deploy this project to the cloud run the following commands:
```bash
docker build -t [example_name] . --platform "linux/amd64"
```
Create an ECR repository on AWS, this can be done through terraform or through the UI, then authenticate using AWS cli.
```bash
brew install awscli
aws ecr get-login-password --region [region-of-choice]| docker login --username AWS --password-stdin [ECR-URI]
```
Then tag your docker image and push to the ECR repository.
```bash
docker tag [example_name]:[ECR-URI]
docker push [ECR-URI]
```

## Setup
In order to run the script users must create a .env file containing the following things.
    - AWS_ACCESS_KEY - Key used to access AWS
    - AWS_SECRET_ACCESS_KEY - Secret key to access AWS
    - INPUTBUCKET - Bucket name for inputting XML files
    - OUTPUTBUCKET - Bucket name for outputting XML files
    - FROM - Email address that will send the notification emails
    - TO - Email address that will receive the notification emails

The *.py files use environment variables and the names of these can be changed easily to match your .env format.

## Usage
To run the pipeline:
```bash
python pipeline.py
```
Additional `-l` argument can be added to log to file.

## How it works

#### `pipeline.py`
- Calls all other functions in the ETL pipeline.
- Takes command line arguments in order to configure the logging of the pipeline.
#### `extract.py`
- Uses the `io` and `boto3` libraries to extract data from the S3 bucket.
- Returns an `xml` root ready for later transformation.
#### `transform.py`
- Uses `xml` library to extract and convert to a `pandas` dataframe
- Extracts emails using regex and the `re` library
- Uses `spaCy` library to identify geopolitical entities and organisations
- Uses `rapidfuzz` library to match aliases stored within `aliases.csv` to institution names
#### `load.py`
- Uses `boto3` to upload data to the output bucket
#### `message,py`
- Uses `boto3` to send notifications for the start and end of the notification process