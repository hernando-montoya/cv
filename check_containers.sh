#!/bin/bash

# Script para verificar el estado real de los contenedores
echo "🔍 Verificando estado real de los contenedores..."

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

# 1. Verificar si los contenedores están corriendo
print_status "Estado de los contenedores:"
if command -v docker-compose &> /dev/null; then
    docker-compose ps
elif docker compose version &> /dev/null; then
    docker compose ps
else
    docker ps --filter "name=cv_"
fi

echo ""

# 2. Verificar logs de cada servicio
print_status "Verificando logs de los servicios..."

echo ""
print_warning "=== LOGS DEL BACKEND ==="
if docker logs cv_backend 2>/dev/null | tail -10; then
    echo ""
else
    print_error "No se encontró el contenedor cv_backend"
fi

echo ""
print_warning "=== LOGS DEL FRONTEND ==="
if docker logs cv_frontend 2>/dev/null | tail -10; then
    echo ""
else
    print_error "No se encontró el contenedor cv_frontend"
fi

echo ""
print_warning "=== LOGS DE MONGODB ==="
if docker logs cv_mongodb 2>/dev/null | tail -10; then
    echo ""
else
    print_error "No se encontró el contenedor cv_mongodb"
fi

# 3. Verificar conectividad interna
print_status "Verificando conectividad interna..."

# Probar backend desde dentro del contenedor
if docker exec cv_backend curl -f http://localhost:8001/api/ 2>/dev/null; then
    print_success "Backend responde internamente"
else
    print_error "Backend NO responde internamente"
fi

# Probar frontend desde dentro del contenedor
if docker exec cv_frontend wget -qO- http://localhost:3000/ 2>/dev/null >/dev/null; then
    print_success "Frontend responde internamente"
else
    print_error "Frontend NO responde internamente"
fi

# 4. Verificar puertos expuestos
print_status "Verificando puertos expuestos:"
docker port cv_backend 2>/dev/null || echo "Backend: puertos no expuestos"
docker port cv_frontend 2>/dev/null || echo "Frontend: puertos no expuestos"
docker port cv_mongodb 2>/dev/null || echo "MongoDB: puertos no expuestos"

# 5. Verificar red de Docker
print_status "Verificando red de Docker:"
docker network ls | grep cv || echo "Red cv_network no encontrada"

# 6. Intentar conectar desde host
print_status "Probando conectividad desde host:"

# Backend
if curl -f http://localhost:8001/api/ 2>/dev/null; then
    print_success "Backend accesible desde host (http://localhost:8001/api/)"
else
    print_error "Backend NO accesible desde host"
fi

# Frontend
if curl -f http://localhost:3000/ 2>/dev/null; then
    print_success "Frontend accesible desde host (http://localhost:3000/)"
else
    print_error "Frontend NO accesible desde host"
fi

# 7. Información de diagnóstico adicional
print_status "Información adicional de diagnóstico:"

echo "Contenedores en ejecución:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "Uso de recursos:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# 8. Comandos útiles para debugging
echo ""
print_warning "=== COMANDOS ÚTILES PARA DEBUG ==="
echo "Ver logs en tiempo real:"
echo "  docker-compose logs -f"
echo ""
echo "Ver logs específicos:"
echo "  docker logs cv_backend -f"
echo "  docker logs cv_frontend -f"
echo "  docker logs cv_mongodb -f"
echo ""
echo "Reiniciar servicios:"
echo "  docker-compose restart"
echo "  docker-compose restart backend"
echo ""
echo "Reconstruir y reiniciar:"
echo "  docker-compose down"
echo "  docker-compose up -d --build"
echo ""
echo "Entrar a contenedor para debug:"
echo "  docker exec -it cv_backend /bin/bash"
echo "  docker exec -it cv_frontend /bin/sh"