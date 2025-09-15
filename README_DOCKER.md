# 🐳 Docker Deployment Guide

## 🚀 Quick Start

### Development Deployment
```bash
# 1. Clone/copy your application
cd /path/to/your/app

# 2. Copy environment file
cp .env.example .env

# 3. Deploy with script
./deploy.sh

# OR manually:
docker-compose up -d
```

### Production Deployment
```bash
# 1. Generate secure credentials
cd backend
python generate_credentials.py

# 2. Update .env with generated values
nano .env

# 3. Deploy in production mode
./deploy.sh --prod

# OR manually:
docker-compose -f docker-compose.prod.yml up -d
```

---

## 📁 Docker Files Structure

```
/app/
├── docker-compose.yml          # Development configuration
├── docker-compose.prod.yml     # Production configuration
├── .env.example               # Environment template
├── deploy.sh                  # Automated deploy script
├── init-mongo.js             # MongoDB initialization
├── backend/
│   ├── Dockerfile            # Backend container
│   └── .dockerignore
├── frontend/
│   ├── Dockerfile            # Frontend container
│   ├── nginx.conf           # Nginx configuration
│   └── .dockerignore
```

---

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Database
MONGO_ROOT_USER=admin
MONGO_ROOT_PASSWORD=your_secure_password
DB_NAME=cv_database

# Authentication (Generate with backend/generate_credentials.py)
ADMIN_USERNAME=your_admin_user
ADMIN_PASSWORD_HASH=generated_hash
JWT_SECRET=generated_jwt_secret

# URLs
REACT_APP_BACKEND_URL=http://localhost:8001  # Dev
# REACT_APP_BACKEND_URL=https://api.yourdomain.com  # Prod
```

---

## 🐳 Services

### MongoDB (Database)
- **Port**: 27017
- **Volume**: `mongodb_data`
- **Health Check**: Ping database
- **Security**: Root user authentication

### Backend (FastAPI)
- **Port**: 8001
- **Health Check**: GET /api/
- **Dependencies**: MongoDB
- **Features**: JWT auth, content management

### Frontend (React + Nginx)
- **Port**: 3000
- **Health Check**: GET /health
- **Features**: Optimized build, gzip compression
- **Dependencies**: Backend

### Data Initializer
- **Purpose**: Populate initial CV data
- **Runs**: Once on first deployment
- **Dependencies**: MongoDB

---

## 📋 Commands

### Basic Operations
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Restart specific service
docker-compose restart backend

# Rebuild and start
docker-compose up -d --build
```

### Production Operations
```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d

# Production logs
docker-compose -f docker-compose.prod.yml logs -f

# Scale services (production)
docker-compose -f docker-compose.prod.yml up -d --scale backend=2
```

### Maintenance
```bash
# Database backup
docker exec cv_mongodb mongodump --db cv_database --out /backup

# View container stats
docker stats

# Clean unused images
docker system prune -a

# Update specific service
docker-compose pull backend
docker-compose up -d backend
```

---

## 🔍 Monitoring & Health Checks

### Service Health
```bash
# Check all services
docker-compose ps

# Check specific service health
docker inspect cv_backend --format='{{.State.Health.Status}}'

# Manual health checks
curl http://localhost:8001/api/        # Backend
curl http://localhost:3000/health      # Frontend
```

### Logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend

# Follow logs in real-time
docker-compose logs -f --tail=100

# Error logs only
docker-compose logs backend | grep ERROR
```

---

## 🔒 Security Considerations

### Development
- Default credentials are acceptable
- HTTP is fine for local development
- Volumes are bind-mounted for hot reload

### Production
- **MUST** change all default passwords
- **MUST** use HTTPS with SSL certificates
- **MUST** restrict network access
- **SHOULD** use secrets management
- **SHOULD** implement log rotation
- **SHOULD** set up automated backups

---

## 🚨 Troubleshooting

### Common Issues

#### Services not starting
```bash
# Check logs
docker-compose logs

# Check disk space
df -h

# Check Docker daemon
sudo systemctl status docker
```

#### Database connection errors
```bash
# Verify MongoDB is running
docker-compose exec mongodb mongosh --eval "db.adminCommand('ping')"

# Check connection string
docker-compose exec backend env | grep MONGO_URL
```

#### Frontend not loading
```bash
# Check backend connectivity from frontend
docker-compose exec frontend wget -qO- http://backend:8001/api/

# Verify build
docker-compose logs frontend | grep "build"
```

#### Port conflicts
```bash
# Check what's using ports
sudo netstat -tulpn | grep ":3000\|:8001\|:27017"

# Change ports in docker-compose.yml if needed
```

### Performance Issues
```bash
# Monitor resource usage
docker stats

# Check container limits
docker inspect cv_backend | grep -i memory

# Database performance
docker-compose exec mongodb mongosh --eval "db.stats()"
```

---

## 📊 Production Deployment Checklist

### Pre-Deployment
- [ ] Generate secure credentials
- [ ] Configure SSL certificates
- [ ] Set up domain DNS
- [ ] Configure firewall rules
- [ ] Set up monitoring
- [ ] Plan backup strategy

### Deployment
- [ ] Update .env with production values
- [ ] Deploy with production compose file
- [ ] Verify all health checks pass
- [ ] Test admin authentication
- [ ] Test content editing
- [ ] Verify SSL/HTTPS works

### Post-Deployment
- [ ] Set up log rotation
- [ ] Configure automated backups
- [ ] Set up monitoring alerts
- [ ] Document recovery procedures
- [ ] Schedule security updates

---

## 🎯 URLs & Access

### Development
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001/api
- **MongoDB**: mongodb://localhost:27017
- **Admin Access**: Click "Admin" → use .env credentials

### Production
- **Frontend**: https://yourdomain.com
- **Backend API**: https://yourdomain.com/api
- **Admin Access**: https://yourdomain.com → "Admin" button

---

## 🔄 Updates & Maintenance

### Application Updates
```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose build --no-cache
docker-compose up -d

# Verify health
docker-compose ps
```

### Database Backups
```bash
# Create backup
docker exec cv_mongodb mongodump --db cv_database --archive=/backup/cv_backup_$(date +%Y%m%d).archive

# Restore backup
docker exec cv_mongodb mongorestore --db cv_database --archive=/backup/cv_backup_YYYYMMDD.archive
```

---

🎉 **Your CV application is now fully containerized and ready for deployment!**