#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

echo "Waiting for MySQL..."

# Try connecting until success
until nc -z db 3306; do
  sleep 1
done

echo "MySQL started, running migrations..."
python manage.py migrate

echo "Starting Django server..."
exec "$@"
