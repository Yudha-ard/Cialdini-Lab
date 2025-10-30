#!/bin/bash

echo "🚀 Tegalsec Social Engineering Lab - Auto Installation"
echo "======================================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first:"
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first:"
    echo "   https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Stop and remove existing containers
echo "🧹 Cleaning up existing containers..."
docker-compose down -v

# Build and start services
echo "🏗️  Building and starting services..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 15

# Check if services are running
echo ""
echo "📊 Checking services status..."
docker-compose ps

echo ""
echo "✅ Installation Complete!"
echo ""
echo "📱 Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8001"
echo "   API Docs: http://localhost:8001/docs"
echo ""
echo "👤 Default accounts:"
echo "   Admin: username=admin, password=admin123"
echo "   User: username=user, password=user123"
echo ""
echo "🛠️  Useful commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop: docker-compose stop"
echo "   Restart: docker-compose restart"
echo "   Remove: docker-compose down -v"
echo ""
