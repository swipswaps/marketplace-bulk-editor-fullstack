# PostgreSQL Setup Guide

## Issue: psycopg2-binary Installation Failed

If you see this error:
```
Error: pg_config executable not found.
```

This means PostgreSQL development headers are not installed.

---

## Solution 1: Use SQLite (Recommended for Development)

**Already configured!** The backend now uses SQLite by default.

No additional setup required. Just run:
```bash
./run.sh
```

---

## Solution 2: Install PostgreSQL (For Production)

### On Fedora/RHEL/CentOS

```bash
sudo dnf install postgresql-devel python3-devel gcc
```

### On Ubuntu/Debian

```bash
sudo apt-get install postgresql postgresql-contrib libpq-dev python3-dev gcc
```

### On macOS

```bash
brew install postgresql
```

### Then uncomment psycopg2 in requirements.txt

```bash
# Edit requirements.txt
# Uncomment line: psycopg2-binary==2.9.9

# Reinstall dependencies
pip install -r requirements.txt
```

---

## Solution 3: Use Docker (Best for Production)

```bash
# From project root
docker-compose up -d
```

This includes PostgreSQL, Redis, and all dependencies.

---

## Current Configuration

### Development (Default)
- **Database**: SQLite (`marketplace.db`)
- **No PostgreSQL required**
- **Perfect for local development**

### Production (Docker)
- **Database**: PostgreSQL 15
- **Redis**: For caching and rate limiting
- **All dependencies included**

---

## Switching Between SQLite and PostgreSQL

### Use SQLite (Default)

In `.env`:
```bash
DATABASE_URL=sqlite:///marketplace.db
```

### Use PostgreSQL

In `.env`:
```bash
# Local PostgreSQL
DATABASE_URL=postgresql://localhost:5432/marketplace_db

# Docker PostgreSQL
DATABASE_URL=postgresql://marketplace_user:marketplace_pass@postgres:5432/marketplace_db
```

---

## Summary

**Problem**: psycopg2-binary requires PostgreSQL development headers

**Solution**: 
- ✅ **Development**: Use SQLite (already configured, no setup needed)
- ✅ **Production**: Use Docker Compose (includes PostgreSQL)
- ⚠️ **Manual PostgreSQL**: Install `postgresql-devel` package

**Next Steps**:
```bash
./run.sh  # Should work now with SQLite!
```

