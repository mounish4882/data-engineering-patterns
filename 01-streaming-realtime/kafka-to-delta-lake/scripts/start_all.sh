#!/bin/bash
# Quick start script for Kafka to Delta Lake streaming pipeline
# Usage: ./scripts/start_all.sh

set -e

echo "=========================================="
echo "Kafka to Delta Lake Pipeline - Quick Start"
echo "=========================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop and try again."
    exit 1
fi

echo "✓ Docker is running"
echo ""

# Step 1: Start infrastructure
echo "📦 Step 1/3: Starting Kafka, Zookeeper, and monitoring stack..."
docker-compose up -d

echo "⏳ Waiting for services to be ready..."
sleep 15

# Check if Kafka is ready
echo "Checking Kafka..."
until docker exec kafka kafka-broker-api-versions --bootstrap-server localhost:9092 > /dev/null 2>&1; do
    echo "Waiting for Kafka to be ready..."
    sleep 5
done
echo "✓ Kafka is ready"

# Step 2: Install Python dependencies
echo ""
echo "📦 Step 2/3: Installing Python dependencies..."
pip install -r requirements.txt --quiet

echo "✓ Dependencies installed"

# Step 3: Instructions
echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "📊 Access the services:"
echo "  • Kafka UI:    http://localhost:8080"
echo "  • Grafana:     http://localhost:3000 (admin/admin)"
echo "  • Prometheus:  http://localhost:9090"
echo ""
echo "🚀 Next steps:"
echo ""
echo "  1. Start the streaming pipeline:"
echo "     python src/run_pipeline.py"
echo ""
echo "  2. In another terminal, generate sample data:"
echo "     python src/data_generator.py --events-per-second 1000"
echo ""
echo "  3. View real-time data in Kafka UI:"
echo "     http://localhost:8080"
echo ""
echo "📝 To stop everything:"
echo "     docker-compose down"
echo ""
