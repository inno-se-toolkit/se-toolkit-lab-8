#!/bin/bash
# Lab 8 Setup Script for VM
# Run this on the VM after cloning the repo

set -e

echo "=== Lab 8 Setup Script ==="

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "ERROR: Please run this script from ~/se-toolkit-lab-8"
    exit 1
fi

# Step 1: Create .env.docker.secret from template
echo "Creating .env.docker.secret..."
if [ -f ".env.docker.secret.template" ]; then
    cp .env.docker.secret.template .env.docker.secret
    echo ".env.docker.secret created from template"
else
    echo "ERROR: .env.docker.secret.template not found"
    exit 1
fi

# Step 2: Stop Lab 7 services
echo "Stopping Lab 7 services..."
cd ~/se-toolkit-lab-7 2>/dev/null && docker compose --env-file .env.docker.secret down || echo "Lab 7 not found or already stopped"
cd ~/se-toolkit-lab-8

# Step 3: Start Lab 8 services
echo "Starting Lab 8 services..."
docker compose --env-file .env.docker.secret up --build -d

# Step 4: Wait for services to be ready
echo "Waiting for services to start..."
sleep 10

# Step 5: Check service status
echo "Service status:"
docker compose --env-file .env.docker.secret ps --format "table {{.Service}}\t{{.Status}}"

# Step 6: Run ETL pipeline sync
echo "Running ETL pipeline sync..."
curl -s -X POST http://localhost:42002/pipeline/sync \
    -H "Authorization: Bearer my-secret-api-key" \
    -H "Content-Type: application/json" || echo "ETL sync failed - do it manually via Swagger"

echo ""
echo "=== Setup Complete ==="
echo "Open http://localhost:42002/docs to verify"
echo "Use LMS_API_KEY: my-secret-api-key"
