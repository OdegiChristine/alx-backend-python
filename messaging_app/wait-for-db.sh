#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

echo "Waiting for MySQL..."

# Try connecting until success
while ! python -c "import socket; s=socket.socket(); s.connect(('db', 3306))" 2>/dev/null; do
  sleep 1
done

echo "MySQL started, running migrations..."
python manage.py migrate

echo "Starting Django server..."
exec "$@"
