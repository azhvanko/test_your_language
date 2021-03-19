#!/bin/sh
set -e

while ! nc -z "$DB_HOST" "$DB_PORT"; do
  echo "Postgres is unavailable - sleeping"
  sleep 0.5
done

echo "Postgres is up"

python manage.py migrate

exec "$@"