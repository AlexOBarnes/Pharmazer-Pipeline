# Pubmed Database

## Setup
1. Create a .env containing the following:
    - `DB_HOST`
    - `DB_PORT`
    - `DB_USER`
    - `DB_PW`
    - `DB_NAME`

## Usage
Once the MySQL database has been setup run the following commands
```bash
bash makedb.sh
bash reset.sh
```
 
### How it works

#### reset.sh
Included within this repository are shell scripts that make managing the MySQL more easy.  
`reset.sh` reruns the schema to reset each table.

#### connect.sh
This script is used to more speedily connect to the database. To use run the following:
```bash
bash connect.sh
```
#### makedb.sh
This creates a database called `pubmed_db` in the MySQL database
Use the following to run this script:
```bash
bash makedb.sh
```
#### listtb.sh
This bash script lists all the tables present in the `pubmed_db` database
Use the following to run this script:
```bash
bash listtb.sh
```
#### viewstatic.sh
This bash script returns the number of rows in the static tables of the `pubmed_db` database
Use the following to run this script:
```bash
bash viewstatic.sh
```