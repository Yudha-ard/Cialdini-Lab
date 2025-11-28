#!/bin/bash

set -e  # Exit on error

# Warna untuk output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Tegalsec Social Engineering Lab - Quick Install${NC}"
echo "========================================================"
echo ""

# 1. Check Docker Installation
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed.${NC}"
    exit 1
fi

# 2. Check Docker Compose V2
if ! docker compose version &> /dev/null; then
    echo -e "${RED}❌ Docker Compose V2 is not detected.${NC}"
    exit 1
fi

# 3. Check Docker Daemon
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker daemon is not running.${NC}"
    exit 1
fi

# 4. Clean up old containers
echo -e "${YELLOW}🧹 Cleaning up...${NC}"
docker compose down -v 2>/dev/null || true

# 5. Build images
echo -e "${YELLOW}🏗️  Building images...${NC}"
if docker compose build --no-cache; then
    echo -e "${GREEN}✅ Build successful!${NC}"
else
    echo -e "${RED}❌ Build failed!${NC}"
    exit 1
fi

# 6. Start services
echo -e "${YELLOW}🚀 Starting services...${NC}"
if docker compose up -d; then
    echo -e "${GREEN}✅ Services started in background!${NC}"
else
    echo -e "${RED}❌ Failed to start services!${NC}"
    exit 1
fi

# 7. Check Ports & IP (NEW FEATURE)
echo ""
echo -e "${YELLOW}🔍 Checking Network & Ports...${NC}"

# Detect Local IP (Linux support mostly)
HOST_IP=$(hostname -I 2>/dev/null | awk '{print $1}')
if [ -z "$HOST_IP" ]; then
    HOST_IP="127.0.0.1"
fi
echo -e "   Detected Host IP: ${GREEN}$HOST_IP${NC}"

# Function to check port using bash tcp (no extra tools needed)
check_port() {
    local port=$1
    local name=$2
    # Mencoba koneksi TCP ke localhost pada port tertentu
    if (echo > /dev/tcp/127.0.0.1/$port) >/dev/null 2>&1; then
        echo -e "   $name ($port): ${GREEN}OPEN (Running)${NC}"
    else
        echo -e "   $name ($port): ${RED}CLOSED (Not accessible yet)${NC}"
    fi
}

check_port 3000 "Frontend"
check_port 8001 "Backend"

echo ""
echo "=========================================="
echo -e "${GREEN}✅ Installation Complete!${NC}"
echo "=========================================="
echo ""
echo "🌐 Access URLs:"
echo "   Frontend: http://localhost:3000"
echo "           : http://$HOST_IP:3000"
echo "   Backend:  http://localhost:8001"
echo ""
echo "👤 Credentials (Admin):"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo -e "${YELLOW}Note: Jika status port masih CLOSED, tunggu 1-2 menit agar database selesai seeding.${NC}"
echo ""