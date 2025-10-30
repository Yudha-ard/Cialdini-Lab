#!/bin/bash

set -e  # Exit on error

echo "🚀 Tegalsec Social Engineering Lab - Docker Installation"
echo "========================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}✅ Docker and Docker Compose are installed${NC}"

# Check Docker daemon
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker daemon is not running. Please start Docker first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker daemon is running${NC}"
echo ""

# Stop and remove existing containers
echo -e "${YELLOW}🧹 Cleaning up existing containers...${NC}"
docker-compose down -v 2>/dev/null || true
echo ""

# Build and start services
echo -e "${YELLOW}🏗️  Building Docker images...${NC}"
echo "This may take 5-10 minutes on first run..."
echo ""

if docker-compose build --no-cache; then
    echo -e "${GREEN}✅ Build successful!${NC}"
else
    echo -e "${RED}❌ Build failed! Check logs above.${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}🚀 Starting services...${NC}"
if docker-compose up -d; then
    echo -e "${GREEN}✅ Services started!${NC}"
else
    echo -e "${RED}❌ Failed to start services!${NC}"
    exit 1
fi

# Wait for services with progress indicator
echo ""
echo -e "${YELLOW}⏳ Waiting for services to initialize...${NC}"
for i in {1..30}; do
    echo -n "."
    sleep 1
    
    # Check if backend is healthy
    if curl -s http://localhost:8001/docs > /dev/null 2>&1; then
        echo ""
        echo -e "${GREEN}✅ Backend is ready!${NC}"
        break
    fi
    
    if [ $i -eq 30 ]; then
        echo ""
        echo -e "${YELLOW}⚠️  Services might still be starting. Check logs with: docker-compose logs -f${NC}"
    fi
done

# Check service status
echo ""
echo -e "${YELLOW}🔍 Checking service status...${NC}"
docker-compose ps

# Show recent logs
echo ""
echo -e "${YELLOW}📋 Recent logs:${NC}"
echo ""
docker-compose logs --tail=30 | tail -20

echo ""
echo "=========================================="
echo -e "${GREEN}✅ Installation Complete!${NC}"
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
echo "📖 Troubleshooting Guide: See DOCKER_GUIDE.md"
echo ""
echo -e "${YELLOW}⚠️  If services are not responding:${NC}"
echo "   1. Wait 1-2 more minutes for initialization"
echo "   2. Check logs: docker-compose logs -f"
echo "   3. Restart: docker-compose restart"
echo ""

