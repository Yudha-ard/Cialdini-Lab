# Docker Installation & Troubleshooting Guide

## Quick Start

```bash
# Clone repository
git clone <your-repo-url>
cd tegalsec-lab

# Make install script executable
chmod +x install.sh

# Run installation
./install.sh
```

## Manual Installation

If the install script fails, follow these steps:

### Step 1: Stop existing containers
```bash
docker-compose down -v
```

### Step 2: Build images
```bash
docker-compose build --no-cache
```

### Step 3: Start services
```bash
docker-compose up -d
```

### Step 4: Check logs
```bash
# View all logs
docker-compose logs -f

# View specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mongodb
```

## Common Issues & Solutions

### 1. Error: "yarn.lock: not found"
**Solution:** Ensure you're in the project root directory, not inside frontend/backend folders.

```bash
# Check your location
pwd  # Should show path ending in /tegalsec-lab or /Cialdini-Lab

# If in wrong directory
cd ..  # Go back to project root
```

### 2. MongoDB Connection Failed
**Solution:** Wait for MongoDB to initialize (takes 10-15 seconds)

```bash
# Check MongoDB health
docker-compose ps

# Restart if needed
docker-compose restart mongodb
docker-compose restart backend
```

### 3. Port Already in Use
**Solution:** Change ports or stop conflicting services

```bash
# Check what's using the port
sudo lsof -i :3000  # Frontend
sudo lsof -i :8001  # Backend
sudo lsof -i :27017 # MongoDB

# Kill process
sudo kill -9 <PID>

# Or change ports in docker-compose.yml
ports:
  - "3001:3000"  # Change left number
```

### 4. Frontend Not Loading
**Solution:** Clear browser cache and wait for build

```bash
# Check frontend build progress
docker-compose logs -f frontend

# Rebuild frontend
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

### 5. Backend Seed Data Failed
**Solution:** Manually run seed scripts

```bash
# Enter backend container
docker exec -it tegalsec-backend sh

# Run seed scripts
python seed_data.py
python seed_indonesia_challenges.py
python seed_massive_challenges.py
python seed_final_10.py
python seed_courses.py

# Exit container
exit
```

### 6. Permission Denied
**Solution:** Run with sudo or fix permissions

```bash
# Run with sudo
sudo docker-compose up -d

# Or fix Docker permissions (Linux)
sudo usermod -aG docker $USER
newgrp docker
```

### 7. "version is obsolete" Warning
**Solution:** This is just a warning, can be ignored. Docker Compose v2 doesn't require version field.

### 8. Services Keep Restarting
**Solution:** Check logs for errors

```bash
# View crash logs
docker-compose logs --tail=100 backend

# Common causes:
# - Missing dependencies (check requirements.txt)
# - MongoDB not ready (wait longer)
# - Port conflicts (change ports)
```

## Development Mode

For development with hot reload:

```bash
# Backend hot reload (already enabled)
docker-compose logs -f backend

# Frontend hot reload
docker-compose logs -f frontend
```

## Production Mode

For production deployment:

```bash
# Use production frontend Dockerfile
docker-compose -f docker-compose.prod.yml up -d

# Or manually
docker build -f Dockerfile.frontend.prod -t tegalsec-frontend:prod .
```

## Cleanup & Reset

### Soft Reset (keeps database)
```bash
docker-compose restart
```

### Hard Reset (removes everything)
```bash
docker-compose down -v
docker system prune -af
./install.sh
```

### Remove only containers
```bash
docker-compose down
docker-compose up -d
```

### Remove database
```bash
docker volume rm cialdini-lab_mongodb_data
# or
docker volume prune
```

## Useful Commands

```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f

# Enter container shell
docker exec -it tegalsec-backend sh
docker exec -it tegalsec-frontend sh
docker exec -it tegalsec-mongodb mongosh

# Stop services
docker-compose stop

# Start services
docker-compose start

# Rebuild specific service
docker-compose build backend
docker-compose up -d backend

# View resource usage
docker stats
```

## Environment Variables

Edit `docker-compose.yml` to customize:

```yaml
environment:
  - MONGO_URL=mongodb://mongodb:27017
  - DB_NAME=tegalsec_lab
  - JWT_SECRET_KEY=your-secret-key-here  # Change this!
  - REACT_APP_BACKEND_URL=http://localhost:8001
```

## Network Issues

If services can't communicate:

```bash
# Check network
docker network ls
docker network inspect cialdini-lab_tegalsec-network

# Recreate network
docker-compose down
docker network prune
docker-compose up -d
```

## Database Access

### Via Docker
```bash
docker exec -it tegalsec-mongodb mongosh
use tegalsec_lab
db.users.find()
db.challenges.countDocuments()
exit
```

### Via Localhost
```bash
# Install MongoDB client
mongosh mongodb://localhost:27017/tegalsec_lab
```

## Health Checks

```bash
# Check backend health
curl http://localhost:8001/docs

# Check frontend
curl http://localhost:3000

# Check MongoDB
docker exec tegalsec-mongodb mongosh --eval "db.adminCommand('ping')"
```

## Getting Help

1. Check logs: `docker-compose logs -f`
2. Check service status: `docker-compose ps`
3. Verify ports: `netstat -tulpn | grep -E '3000|8001|27017'`
4. Review this guide for common issues
5. Open an issue on GitHub with:
   - Your OS and Docker version
   - Full error logs
   - Steps to reproduce

---

**Need more help?** Join our Discord community or open a GitHub issue.
