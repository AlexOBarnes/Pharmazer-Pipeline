# Pharmazer Pipeline

### Overview
This project implements an ETL data pipeline that uses the `boto3` library to extract XML files from pubmed from an S3 bucket.    
The `pandas`, `spaCy`, `rapidfuzz` and `re` libraries are used to process the textual data. Transformation processes included extracting emails, institution names and locations.  
This project also contains the files necessary to terraform an RDS instance running MySQL.  
The pipeline is modular and is contained across the `pipeline.py`, `extract.py`, `transform.py` and `load.py` files within the `pipeline/` folder.

### Installation
1. Clone the repository:
```bash
git clone https://github.com/AlexOBarnes/Pharmazer-Pipeline
```

2. This project requires a pre-prepared S3 bucket on AWS. This can be provisioned through the AWS UI

3. Move into each folder and follow the instructions within each in the following order:
    - Pipeline
    - Terraform
    - Database

### Contributions
Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure that your code adheres to the project's coding standards, I use pylint to format my code, and is well-documented. Code must score above an 8 in pylint and the unit tests included in the repository must pass. 
### License
This project is licensed under the MIT License - Please see the attached file.
