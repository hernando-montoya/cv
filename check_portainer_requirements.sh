#!/bin/bash

# Script para verificar requisitos antes del deploy en Portainer
echo "🔍 Verificando requisitos para Portainer..."

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

# 1. Verificar Docker
print_status "Verificando Docker..."
if docker --version >/dev/null 2>&1; then
    print_success "Docker instalado: $(docker --version)"
else
    print_error "Docker no está instalado"
    exit 1
fi

# 2. Verificar red npm_proxy
print_status "Verificando red npm_proxy..."
if docker network ls | grep -q npm_proxy; then
    print_success "Red npm_proxy existe"
else
    print_warning "Red npm_proxy no existe, creándola..."
    if docker network create npm_proxy; then
        print_success "Red npm_proxy creada"
    else
        print_error "No se pudo crear la red npm_proxy"
        exit 1
    fi
fi

# 3. Verificar espacio en disco
print_status "Verificando espacio en disco..."
DISK_SPACE=$(df -h . | awk 'NR==2{print $4}' | sed 's/[^0-9]*//g')
if [ "$DISK_SPACE" -gt 2000 ]; then
    print_success "Espacio suficiente en disco"
else
    print_warning "Poco espacio en disco: $(df -h . | awk 'NR==2{print $4}')"
fi

# 4. Verificar memoria
print_status "Verificando memoria disponible..."
MEM_AVAILABLE=$(free -m | awk 'NR==2{print $7}')
if [ "$MEM_AVAILABLE" -gt 1000 ]; then
    print_success "Memoria suficiente: ${MEM_AVAILABLE}MB disponible"
else
    print_warning "Poca memoria disponible: ${MEM_AVAILABLE}MB"
fi

# 5. Verificar archivos necesarios
print_status "Verificando archivos necesarios..."

required_files=(
    "backend/Dockerfile"
    "frontend/Dockerfile"
    "backend/server.py"
    "frontend/package.json"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        print_success "✅ $file"
    else
        print_error "❌ $file no encontrado"
        exit 1
    fi
done

# 6. Test rápido de MongoDB
print_status "Probando imagen de MongoDB..."
if docker run --rm mongo:5.0 mongosh --version >/dev/null 2>&1; then
    print_success "Imagen MongoDB funcional"
else
    print_warning "Problema con imagen MongoDB, descargando..."
    docker pull mongo:5.0
fi

# 7. Verificar puertos no estén en uso
print_status "Verificando puertos..."
for port in 3000 8001 27017; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_warning "Puerto $port está en uso"
    else
        print_success "Puerto $port disponible"
    fi
done

# 8. Generar credenciales si no existen
if [ -f "backend/generate_credentials.py" ]; then
    print_status "Script de credenciales disponible"
    print_warning "Recuerda ejecutar: python backend/generate_credentials.py"
else
    print_error "Script generate_credentials.py no encontrado"
fi

echo ""
print_success "🎯 Verificación completada"
echo ""
print_status "=== PRÓXIMOS PASOS ==="
echo "1. Ejecutar: python backend/generate_credentials.py"
echo "2. En Portainer, usar: portainer-stack-minimal.yml"
echo "3. Configurar variables de entorno con valores generados"
echo "4. Deploy the stack"
echo ""
print_success "✅ Sistema listo para deploy en Portainer"