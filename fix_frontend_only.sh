#!/bin/bash

# Script para arreglar solo el frontend (backend y MongoDB están OK)
echo "🔧 Arreglando solo el frontend..."

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

# 1. Ver por qué falló el frontend
print_status "Verificando logs del frontend..."
if docker logs cv_frontend 2>/dev/null; then
    echo ""
else
    print_warning "El contenedor cv_frontend no existe o falló al crearse"
fi

# 2. Parar solo el frontend (mantener backend y MongoDB)
print_status "Deteniendo frontend..."
docker-compose stop frontend 2>/dev/null || echo "Frontend no estaba corriendo"
docker-compose rm -f frontend 2>/dev/null || echo "No hay contenedor frontend para remover"

# 3. Verificar build del frontend
print_status "Verificando build del frontend..."
cd frontend

# Limpiar build anterior
rm -rf build/

# Probar build local primero
print_status "Probando build local..."
if GENERATE_SOURCEMAP=false npm run build 2>/dev/null; then
    print_success "Build local exitoso"
elif GENERATE_SOURCEMAP=false npx react-scripts build 2>/dev/null; then
    print_success "Build con react-scripts exitoso"
else
    print_warning "Build local falló, limpiando dependencias..."
    rm -rf node_modules yarn.lock
    
    print_status "Reinstalando dependencias..."
    npm install --legacy-peer-deps
    
    print_status "Intentando build nuevamente..."
    if GENERATE_SOURCEMAP=false npx react-scripts build; then
        print_success "Build exitoso después de reinstalar"
    else
        print_error "Build sigue fallando"
        echo "Vamos a ver el error específico:"
        GENERATE_SOURCEMAP=false npx react-scripts build
        exit 1
    fi
fi

cd ..

# 4. Reconstruir solo la imagen del frontend
print_status "Reconstruyendo imagen del frontend..."
docker-compose build --no-cache frontend

# 5. Iniciar solo el frontend
print_status "Iniciando frontend..."
docker-compose up -d frontend

# 6. Esperar que inicie
print_status "Esperando que el frontend inicie..."
sleep 10

# 7. Verificar estado
print_status "Verificando estado final..."
docker-compose ps

# 8. Probar conectividad
print_status "Probando conectividad..."

# Backend (debería seguir funcionando)
if curl -f http://localhost:8001/api/ >/dev/null 2>&1; then
    print_success "✅ Backend funcionando: http://localhost:8001/api/"
else
    print_warning "⚠️  Backend no responde"
fi

# Frontend (debería funcionar ahora)
sleep 5
if curl -f http://localhost:3000/ >/dev/null 2>&1; then
    print_success "✅ Frontend funcionando: http://localhost:3000/"
else
    print_error "❌ Frontend aún no responde"
    echo ""
    print_status "Verificando logs del frontend:"
    docker logs cv_frontend --tail 20
    echo ""
    print_status "Verificando puertos del frontend:"
    docker port cv_frontend 2>/dev/null || echo "No hay puertos expuestos"
fi

echo ""
print_status "=== ESTADO FINAL ==="
docker-compose ps

echo ""
if curl -f http://localhost:3000/ >/dev/null 2>&1; then
    print_success "🎉 ¡Aplicación completamente funcional!"
    echo ""
    echo "URLs de acceso:"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend:  http://localhost:8001/api"
    echo "  Admin:    http://localhost:3000 → Clic 'Admin' → admin/admin2024"
else
    print_error "El frontend aún tiene problemas"
    echo ""
    echo "Para debugging:"
    echo "  docker logs cv_frontend -f"
    echo "  docker-compose logs frontend"
    echo ""
    echo "El backend está funcionando en: http://localhost:8001/api"
fi