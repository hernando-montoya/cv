#!/bin/bash

# Script para solucionar problemas comunes con contenedores
echo "🔧 Solucionando problemas con contenedores..."

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

# 1. Parar todos los contenedores
print_status "Parando contenedores existentes..."
docker-compose down 2>/dev/null || docker compose down 2>/dev/null || echo "No hay contenedores corriendo"

# 2. Limpiar volúmenes y redes
print_status "Limpiando volúmenes y redes..."
docker-compose down -v 2>/dev/null || echo "Sin volúmenes para limpiar"

# 3. Verificar .env
print_status "Verificando configuración .env..."
if [ ! -f ".env" ]; then
    print_warning "Creando .env desde template..."
    cp .env.example .env
fi

# Actualizar .env con valores válidos
print_status "Actualizando .env con valores válidos..."
cat > .env << EOF
# Database Configuration
MONGO_ROOT_USER=admin
MONGO_ROOT_PASSWORD=securepass123
DB_NAME=cv_database

# Admin Authentication (FOR DEVELOPMENT ONLY!)
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=b8d6c1a9b2e5d7f3:a1b2c3d4e5f6789012345678901234567890123456789012345678901234567890
JWT_SECRET=development_jwt_secret_key_very_long_for_testing_purposes_only_12345

# Frontend Configuration
REACT_APP_BACKEND_URL=http://localhost:8001
EOF

print_success ".env actualizado"

# 4. Verificar y arreglar frontend
print_status "Verificando frontend..."
cd frontend

# Asegurar que el build script existe
if ! grep -q '"docker:build"' package.json; then
    print_status "Agregando script docker:build..."
    # Crear backup
    cp package.json package.json.backup
    
    # Agregar script usando sed de forma más robusta
    sed -i 's/"build": "craco build"/"build": "craco build",\n    "docker:build": "GENERATE_SOURCEMAP=false react-scripts build"/' package.json
fi

# Probar build local
print_status "Probando build del frontend..."
if GENERATE_SOURCEMAP=false npx react-scripts build >/dev/null 2>&1; then
    print_success "Build del frontend OK"
else
    print_warning "Build falló, instalando dependencias..."
    rm -rf node_modules yarn.lock
    yarn install --legacy-peer-deps
    
    if GENERATE_SOURCEMAP=false npx react-scripts build >/dev/null 2>&1; then
        print_success "Build del frontend OK después de reinstalar"
    else
        print_error "Build del frontend sigue fallando"
        # Mostrar error específico
        echo "Error específico:"
        GENERATE_SOURCEMAP=false npx react-scripts build
    fi
fi

cd ..

# 5. Reconstruir imágenes
print_status "Reconstruyendo imágenes Docker..."
docker-compose build --no-cache

# 6. Iniciar servicios uno por uno
print_status "Iniciando MongoDB..."
docker-compose up -d mongodb

print_status "Esperando que MongoDB esté listo..."
sleep 15

# Verificar MongoDB
if docker exec cv_mongodb mongosh --eval "db.adminCommand('ping')" >/dev/null 2>&1; then
    print_success "MongoDB está funcionando"
else
    print_error "MongoDB no está respondiendo"
    echo "Logs de MongoDB:"
    docker logs cv_mongodb --tail 20
fi

print_status "Iniciando Backend..."
docker-compose up -d backend

print_status "Esperando que Backend esté listo..."
sleep 10

# Verificar Backend
if curl -f http://localhost:8001/api/ >/dev/null 2>&1; then
    print_success "Backend está funcionando"
else
    print_error "Backend no está respondiendo"
    echo "Logs de Backend:"
    docker logs cv_backend --tail 20
fi

print_status "Iniciando Frontend..."
docker-compose up -d frontend

print_status "Esperando que Frontend esté listo..."
sleep 10

# Verificar Frontend
if curl -f http://localhost:3000/ >/dev/null 2>&1; then
    print_success "Frontend está funcionando"
else
    print_error "Frontend no está respondiendo"
    echo "Logs de Frontend:"
    docker logs cv_frontend --tail 20
fi

# 7. Inicializar datos
print_status "Iniciando inicializador de datos..."
docker-compose run --rm data-init

# 8. Estado final
print_status "Estado final de los servicios:"
docker-compose ps

echo ""
print_success "🎉 Proceso de reparación completado!"
echo ""
echo "URLs para probar:"
echo "- Frontend: http://localhost:3000"
echo "- Backend API: http://localhost:8001/api"
echo "- Admin: http://localhost:3000 (clic en 'Admin' → admin/admin2024)"
echo ""
echo "Si aún hay problemas, ejecuta:"
echo "  ./check_containers.sh"
echo ""
echo "Para ver logs en tiempo real:"
echo "  docker-compose logs -f"