#!/bin/bash

echo "Stopping all Marketplace Bulk Editor containers..."

docker stop marketplace-frontend 2>/dev/null || echo "Frontend not running"
docker stop marketplace-backend 2>/dev/null || echo "Backend not running"
docker stop marketplace-redis 2>/dev/null || echo "Redis not running"
docker stop marketplace-postgres 2>/dev/null || echo "PostgreSQL not running"

docker rm marketplace-frontend 2>/dev/null || echo "Frontend container removed"
docker rm marketplace-backend 2>/dev/null || echo "Backend container removed"
docker rm marketplace-redis 2>/dev/null || echo "Redis container removed"
docker rm marketplace-postgres 2>/dev/null || echo "PostgreSQL container removed"

echo ""
echo "✓ All containers stopped and removed"
echo ""
echo "To remove volumes (WARNING: deletes all data):"
echo "  docker volume rm marketplace-bulk-editor_postgres_data"
echo "  docker volume rm marketplace-bulk-editor_redis_data"
echo "  docker volume rm marketplace-bulk-editor_upload_data"
echo ""

