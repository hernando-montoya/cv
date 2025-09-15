#!/bin/bash

# Deploy script for CV Application
set -e

echo "🚀 Starting CV Application Deployment"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Default values
ENVIRONMENT="development"
COMPOSE_FILE="docker-compose.yml"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -e|--env)
            ENVIRONMENT="$2"
            shift
            shift
            ;;
        -p|--prod)
            ENVIRONMENT="production"
            COMPOSE_FILE="docker-compose.prod.yml"
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  -e, --env ENVIRONMENT    Set environment (development|production)"
            echo "  -p, --prod              Use production configuration"
            echo "  -h, --help              Show this help message"
            exit 0
            ;;
        *)
            print_error "Unknown option $1"
            exit 1
            ;;
    esac
done

print_status "Deploying in $ENVIRONMENT mode using $COMPOSE_FILE"

# Check if .env file exists
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        print_warning ".env file not found. Copying from .env.example"
        cp .env.example .env
        print_warning "Please edit .env file with your configuration before continuing."
        
        if [ "$ENVIRONMENT" = "production" ]; then
            print_error "Production deployment requires proper .env configuration."
            print_status "Run the following to generate secure credentials:"
            print_status "cd backend && python generate_credentials.py"
            exit 1
        fi
    else
        print_error ".env file not found and .env.example doesn't exist"
        exit 1
    fi
fi

# Validate environment variables for production
if [ "$ENVIRONMENT" = "production" ]; then
    print_status "Validating production environment variables..."
    
    if grep -q "your_secure_mongo_password" .env; then
        print_error "Please update MONGO_ROOT_PASSWORD in .env file"
        exit 1
    fi
    
    if grep -q "admin2024" .env; then
        print_error "Please update admin credentials in .env file"
        print_status "Run: cd backend && python generate_credentials.py"
        exit 1
    fi
    
    print_success "Environment validation passed"
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p logs
mkdir -p data/mongodb
mkdir -p nginx/conf.d
mkdir -p nginx/ssl

# Stop existing containers
print_status "Stopping existing containers..."
docker-compose -f $COMPOSE_FILE down

# Remove old images (optional)
read -p "Do you want to rebuild images? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Removing old images..."
    docker-compose -f $COMPOSE_FILE build --no-cache
fi

# Start services
print_status "Starting services..."
docker-compose -f $COMPOSE_FILE up -d

# Wait for services to be healthy
print_status "Waiting for services to be ready..."
sleep 10

# Check service health
print_status "Checking service health..."

# Check MongoDB
if docker-compose -f $COMPOSE_FILE exec mongodb mongosh --eval "db.adminCommand('ping')" &> /dev/null; then
    print_success "MongoDB is healthy"
else
    print_error "MongoDB is not responding"
fi

# Check Backend
if curl -f http://localhost:8001/api/ &> /dev/null; then
    print_success "Backend is healthy"
else
    print_error "Backend is not responding"
fi

# Check Frontend
if curl -f http://localhost:3000/ &> /dev/null; then
    print_success "Frontend is healthy"
else
    print_error "Frontend is not responding"
fi

# Show running containers
print_status "Running containers:"
docker-compose -f $COMPOSE_FILE ps

# Show logs command
print_status "To view logs, run:"
echo "docker-compose -f $COMPOSE_FILE logs -f"

# Show application URLs
print_success "🎉 Deployment completed!"
echo ""
echo "Application URLs:"
echo "  Frontend: http://localhost:3000"
echo "  Backend API: http://localhost:8001/api"
echo "  MongoDB: mongodb://localhost:27017"
echo ""
echo "Admin Access:"
echo "  Click 'Admin' button on the website"
echo "  Use credentials from your .env file"
echo ""

if [ "$ENVIRONMENT" = "production" ]; then
    echo "Production Notes:"
    echo "  - Configure SSL certificates in nginx/ssl/"
    echo "  - Update DNS records to point to this server"
    echo "  - Set up monitoring and backups"
    echo "  - Review firewall settings"
fi

print_success "Deployment finished successfully! 🚀"