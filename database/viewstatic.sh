source .env
export MYSQL_PWD=$DB_PW
mysql -h $DB_HOST -P $DB_PORT -u $DB_USER -D $DB_NAME -e 'SELECT COUNT(*) FROM affiliation;SELECT COUNT(*) FROM keywords;'