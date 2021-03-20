#!/bin/sh
set -e

psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
  CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
  ALTER ROLE $DB_USER SET client_encoding TO 'UTF8';
  ALTER ROLE $DB_USER SET default_transaction_isolation TO 'READ COMMITTED';
  ALTER ROLE $DB_USER SET TIMEZONE TO '$TZ';
  CREATE DATABASE $DB_NAME OWNER $DB_USER;
  GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
  ALTER ROLE $DB_USER CREATEDB;
EOSQL