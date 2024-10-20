source .env
export MYSQL_PWD=$DB_PW
mysql -h $DB_HOST -P $DB_PORT -u $DB_USER $DB_NAME < schema.sql