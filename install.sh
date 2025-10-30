#!/bin/bash

echo "🚀 Tegalsec Social Engineering Lab - Docker Installation"
echo "========================================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Stop and remove existing containers
echo "🧹 Cleaning up existing containers..."
docker-compose down -v 2>/dev/null || true

# Build and start services
echo ""
echo "🏗️  Building and starting services..."
echo "This may take a few minutes on first run..."
echo ""

docker-compose up --build -d

# Wait for services to be ready
echo ""
echo "⏳ Waiting for services to start..."
sleep 15

# Check if services are running
echo ""
echo "🔍 Checking service status..."
docker-compose ps

# Show logs
echo ""
echo "📋 Recent logs:"
echo ""
docker-compose logs --tail=20

echo ""
echo "=========================================="
echo "✅ Installation Complete!"
echo "=========================================="
echo ""
echo "🌐 Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8001"
echo "   API Docs: http://localhost:8001/docs"
echo ""
echo "👤 Default Admin Account:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "📝 Useful Commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop: docker-compose down"
echo "   Restart: docker-compose restart"
echo "   Fresh start: ./install.sh"
echo ""
echo "⚠️  If services are not ready, wait a few more seconds"
echo "    and check logs with: docker-compose logs -f"
echo ""
