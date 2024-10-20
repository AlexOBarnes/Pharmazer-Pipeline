# Pharmazer Terraform

## Overview
This terraform provisions ECS tasks and RDS instances that this ETL-pipeline runs on. In order to setup the cloud architecture contained within this folder one can modify the terraform script or provision the additional services through the AWS UI

## Setup
This setup assumes the use of AWS and that the user has setup a VPC and security groups for this project.

1. Create the docker images and push to the ECR repository

2. In order to run the script users must create a .tfvars file containing the following things.
- `AWS_ACCESS_KEY`
- `AWS_SECRET_ACCESS_KEY`
- `INPUTBUCKET`
- `OUTPUTBUCKET`
- `SUBNET_ID`
- `IMAGE_URI`
- `SECURITY_GROUP_ID`
- `FROM`
- `TO`
- `DB_PW`
- `DB_USER`

## Usage
Run the following command to provision the cloud services:
```bash
terraform init
terraform apply
```

### How it works
#### `main.tf`
- Contains the terraform config for ECS task and RDS instances described in the cloud architecture diagram.
#### `variables.tf`
- Details the private variables used in the config file.
