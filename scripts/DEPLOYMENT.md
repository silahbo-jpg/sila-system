# SILA System Deployment Guide

This document explains how to deploy the SILA System backend with Prisma and PostgreSQL using the automated deployment scripts.

## Prerequisites

- Python 3.8+
- Node.js and npm
- PostgreSQL database
- Prisma CLI installed globally (`npm install -g prisma`)
- curl (for health checks)

## Project Structure

The scripts correctly reference the backend directory structure:
- Main project directory: sila-system/
- Backend directory: sila-system/backend/
- Application code: sila-system/backend/app/
- Deployment scripts: sila-system/scripts/

## Deployment Scripts

The deployment process is automated through the following scripts:

### Pre-deployment Validation
- `scripts/pre_deploy_check.sh` (Linux/Mac)
- `scripts/pre_deploy_check.ps1` (Windows)

These scripts validate:
- Correct project directory structure
- No SQLite contamination in the codebase
- Presence of required environment files
- Database connectivity

### Main Deployment
- `scripts/deploy_backend.sh` (Linux/Mac)
- `scripts/deploy_backend.ps1` (Windows)

These scripts handle:
- Path validation for required directories
- Virtual environment setup
- Dependency installation
- Prisma schema validation and generation
- Database migrations
- Server startup
- Health checks
- Endpoint validation

## Deployment Commands

### Linux/Mac
```bash
make deploy
```

### Windows
```bash
make deploy_win
```

### Manual Execution

Linux/Mac:
```bash
chmod +x scripts/deploy_backend.sh
./scripts/deploy_backend.sh
```

Windows:
```powershell
powershell -ExecutionPolicy Bypass -File scripts/deploy_backend.ps1
```

## Validation

After deployment, you can validate the deployment with:
```bash
make validate_deployment
```

This checks:
- Health endpoint (`/health`)
- Protocols endpoint (`/api/protocols`)
- Auth login endpoint (`/api/auth/login`)

## Automated Recovery

The deployment scripts include automated recovery features:
- Exit on first error with detailed logging
- Automatic fallback for migration issues
- Comprehensive health checks before completion
- Timestamped logs for audit trails

## Validation Metrics

The deployment process validates:
- ✅ Zero SQLite references in codebase
- ✅ Database connection successful
- ✅ Prisma schema validates without errors
- ✅ All migrations applied successfully
- ✅ Server starts and responds to health checks
- ✅ Critical endpoints return expected responses

## Path Resolution

All scripts dynamically resolve paths to ensure they work regardless of the project location or directory structure changes:
- Base path is determined relative to the script location
- Backend directory is correctly identified as `sila-system/backend/`
- Application code is correctly identified as `sila-system/backend/app/`
- All required paths are validated before proceeding