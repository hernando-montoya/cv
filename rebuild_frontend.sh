#!/bin/bash

echo "🔧 Reconstruyendo frontend después de arreglar nginx.conf..."

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

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 1. Parar frontend actual
print_status "Parando frontend actual..."
docker-compose stop frontend 2>/dev/null
docker-compose rm -f frontend 2>/dev/null

# 2. Verificar que nginx.conf existe
if [ -f "frontend/nginx.conf" ]; then
    print_success "nginx.conf encontrado"
else
    print_error "nginx.conf no encontrado"
    exit 1
fi

# 3. Limpiar imagen anterior
print_status "Limpiando imagen anterior..."
docker rmi cv-frontend 2>/dev/null || echo "No había imagen anterior"

# 4. Reconstruir imagen
print_status "Reconstruyendo imagen del frontend..."
if docker-compose build --no-cache frontend; then
    print_success "Imagen construida exitosamente"
else
    print_error "Error construyendo imagen"
    exit 1
fi

# 5. Iniciar frontend
print_status "Iniciando frontend..."
docker-compose up -d frontend

# 6. Esperar y verificar
print_status "Esperando que el frontend inicie..."
sleep 15

# 7. Verificar estado
print_status "Verificando estado..."
docker-compose ps

# 8. Probar conectividad
print_status "Probando conectividad..."

for i in {1..10}; do
    if curl -f http://localhost:3000/ >/dev/null 2>&1; then
        print_success "✅ Frontend funcionando: http://localhost:3000/"
        break
    else
        echo -n "."
        sleep 2
    fi
done

echo ""

# Verificación final
if curl -f http://localhost:3000/ >/dev/null 2>&1; then
    print_success "🎉 ¡Frontend completamente funcional!"
    echo ""
    echo "URLs de acceso:"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend:  http://localhost:8001/api"
    echo "  Admin:    http://localhost:3000 → Clic 'Admin' → admin/admin2024"
else
    print_error "Frontend aún no responde"
    echo ""
    echo "Logs del frontend:"
    docker logs cv_frontend --tail 20
fi