#!/bin/bash

echo "🔧 Arreglando configuración de nginx..."

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
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

# 1. Verificar que la configuración esté corregida
print_status "Verificando nginx.conf..."
if grep -q "gzip_proxied expired no-cache no-store private auth" frontend/nginx.conf; then
    print_success "Configuración de nginx corregida"
else
    print_error "La configuración aún no está corregida"
    exit 1
fi

# 2. Parar el frontend
print_status "Parando frontend..."
docker-compose stop frontend 2>/dev/null
docker-compose rm -f frontend 2>/dev/null

# 3. Reconstruir imagen
print_status "Reconstruyendo imagen del frontend..."
docker-compose build --no-cache frontend

# 4. Iniciar frontend
print_status "Iniciando frontend..."
docker-compose up -d frontend

# 5. Verificar logs
print_status "Verificando logs iniciales..."
sleep 5
docker logs cv_frontend --tail 10

# 6. Esperar y probar
print_status "Esperando que nginx inicie correctamente..."
sleep 10

# 7. Probar conectividad múltiples veces
print_status "Probando conectividad..."
for i in {1..15}; do
    if curl -f http://localhost:3000/ >/dev/null 2>&1; then
        print_success "✅ Frontend funcionando: http://localhost:3000/"
        echo ""
        echo "🎉 ¡Aplicación completamente funcional!"
        echo ""
        echo "URLs de acceso:"
        echo "  Frontend: http://localhost:3000"
        echo "  Backend:  http://localhost:8001/api"
        echo "  Admin:    http://localhost:3000 → Clic 'Admin' → admin/admin2024"
        exit 0
    else
        echo -n "."
        sleep 2
    fi
done

echo ""
print_error "Frontend aún no responde después de 30 segundos"
echo ""
print_status "Logs del frontend:"
docker logs cv_frontend --tail 20

echo ""
print_status "Estado de contenedores:"
docker-compose ps