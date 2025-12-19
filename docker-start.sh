#!/bin/bash
set -e

echo "==========================================="
echo "Marketplace Bulk Editor - Docker Setup"
echo "==========================================="

# Create network if it doesn't exist
docker network create marketplace-network 2>/dev/null || echo "Network already exists"

# Create volumes if they don't exist
docker volume create marketplace-bulk-editor_postgres_data 2>/dev/null || echo "postgres_data volume exists"
docker volume create marketplace-bulk-editor_redis_data 2>/dev/null || echo "redis_data volume exists"
docker volume create marketplace-bulk-editor_upload_data 2>/dev/null || echo "upload_data volume exists"

echo ""
echo "Starting PostgreSQL..."
docker run -d \
  --name marketplace-postgres \
  --network marketplace-network \
  -e POSTGRES_USER=marketplace_user \
  -e POSTGRES_PASSWORD=marketplace_pass \
  -e POSTGRES_DB=marketplace_db \
  -p 5432:5432 \
  -v marketplace-bulk-editor_postgres_data:/var/lib/postgresql/data \
  --health-cmd="pg_isready -U marketplace_user" \
  --health-interval=10s \
  --health-timeout=5s \
  --health-retries=5 \
  postgres:15-alpine 2>/dev/null || echo "PostgreSQL already running"

echo "Starting Redis..."
docker run -d \
  --name marketplace-redis \
  --network marketplace-network \
  -p 6379:6379 \
  -v marketplace-bulk-editor_redis_data:/data \
  --health-cmd="redis-cli ping" \
  --health-interval=10s \
  --health-timeout=5s \
  --health-retries=5 \
  redis:7-alpine 2>/dev/null || echo "Redis already running"

echo ""
echo "Waiting for PostgreSQL to be healthy..."
until [ "$(docker inspect -f {{.State.Health.Status}} marketplace-postgres 2>/dev/null)" == "healthy" ]; do
    echo -n "."
    sleep 2
done
echo " ✓ PostgreSQL is healthy"

echo "Waiting for Redis to be healthy..."
until [ "$(docker inspect -f {{.State.Health.Status}} marketplace-redis 2>/dev/null)" == "healthy" ]; do
    echo -n "."
    sleep 2
done
echo " ✓ Redis is healthy"

echo ""
echo "Starting Backend..."
docker run -d \
  --name marketplace-backend \
  --network marketplace-network \
  -e FLASK_ENV=development \
  -e FLASK_APP=app.py \
  -e DATABASE_URL=postgresql://marketplace_user:marketplace_pass@marketplace-postgres:5432/marketplace_db \
  -e REDIS_URL=redis://marketplace-redis:6379/0 \
  -e JWT_SECRET_KEY=dev-jwt-secret-change-in-production \
  -e JWT_REFRESH_SECRET=dev-jwt-refresh-secret-change-in-production \
  -e ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000,http://localhost:5000 \
  -e RATE_LIMIT_STORAGE=redis://marketplace-redis:6379/1 \
  -e SECRET_KEY=dev-secret-key-change-in-production \
  -p 5000:5000 \
  -v "$(pwd)/backend:/app" \
  -v marketplace-bulk-editor_upload_data:/tmp/uploads \
  marketplace-backend \
  flask run --host=0.0.0.0 --port=5000 --debug 2>/dev/null || echo "Backend already running"

echo "Starting Frontend..."
docker run -d \
  --name marketplace-frontend \
  --network marketplace-network \
  -e VITE_API_BASE_URL=http://localhost:5000 \
  -p 5173:5173 \
  -v "$(pwd)/src:/app/src" \
  -v "$(pwd)/public:/app/public" \
  -v "$(pwd)/index.html:/app/index.html" \
  -v "$(pwd)/vite.config.ts:/app/vite.config.ts" \
  -v "$(pwd)/tsconfig.json:/app/tsconfig.json" \
  -v "$(pwd)/tsconfig.app.json:/app/tsconfig.app.json" \
  -v "$(pwd)/tsconfig.node.json:/app/tsconfig.node.json" \
  -v "$(pwd)/tailwind.config.js:/app/tailwind.config.js" \
  -v "$(pwd)/postcss.config.js:/app/postcss.config.js" \
  marketplace-frontend 2>/dev/null || echo "Frontend already running"

echo ""
echo "==========================================="
echo "✓ All services started!"
echo "==========================================="
echo ""
echo "Services:"
echo "  Frontend:  http://localhost:5173"
echo "  Backend:   http://localhost:5000"
echo "  PostgreSQL: localhost:5432"
echo "  Redis:     localhost:6379"
echo ""
echo "View logs:"
echo "  docker logs -f marketplace-backend"
echo "  docker logs -f marketplace-frontend"
echo ""
echo "Stop all:"
echo "  ./docker-stop.sh"
echo ""

