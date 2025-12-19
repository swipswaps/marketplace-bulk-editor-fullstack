#!/bin/bash
set -e

echo "==========================================="
echo "Marketplace Bulk Editor - Backend"
echo "Docker Container Starting"
echo "==========================================="

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
while ! pg_isready -h marketplace-postgres -U marketplace_user > /dev/null 2>&1; do
    echo "PostgreSQL is unavailable - sleeping"
    sleep 1
done
echo "✓ PostgreSQL is ready"

# Wait for Redis to be ready
echo "Waiting for Redis..."
while ! redis-cli -h marketplace-redis ping > /dev/null 2>&1; do
    echo "Redis is unavailable - sleeping"
    sleep 1
done
echo "✓ Redis is ready"

# Initialize database if needed
echo "Initializing database..."
python init_db.py || echo "⚠ Database initialization failed (may already exist)"

# Run database migrations
echo "Running database migrations..."
flask db upgrade || echo "⚠ No migrations to run"

echo "==========================================="
echo "✓ Backend initialization complete"
echo "Starting Flask application..."
echo "==========================================="

# Execute the main command
exec "$@"

