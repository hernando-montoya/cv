#!/bin/bash

# Script de diagnóstico y solución para problemas de Docker
echo "🔍 Diagnosticando problemas de Docker..."

# Colores para output
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
if command -v docker &> /dev/null; then
    print_success "Docker está instalado: $(docker --version)"
else
    print_error "Docker no está instalado"
    echo "Instala Docker desde: https://docs.docker.com/get-docker/"
    exit 1
fi

# 2. Verificar Docker Compose
print_status "Verificando Docker Compose..."
if command -v docker-compose &> /dev/null; then
    print_success "Docker Compose está instalado: $(docker-compose --version)"
elif docker compose version &> /dev/null; then
    print_success "Docker Compose (plugin) está disponible"
    # Crear alias para compatibilidad
    alias docker-compose='docker compose'
else
    print_error "Docker Compose no está instalado"
    echo "Instala Docker Compose desde: https://docs.docker.com/compose/install/"
    exit 1
fi

# 3. Verificar archivos necesarios
print_status "Verificando archivos de configuración..."

if [ ! -f ".env" ]; then
    print_warning ".env no existe, copiando desde .env.example"
    cp .env.example .env
fi

if [ ! -f "docker-compose.yml" ]; then
    print_error "docker-compose.yml no existe"
    exit 1
fi

print_success "Archivos de configuración encontrados"

# 4. Verificar y arreglar frontend
print_status "Verificando configuración del frontend..."

cd frontend

# Verificar package.json
if grep -q '"react": "\^19' package.json; then
    print_warning "React 19 detectado, puede causar problemas"
    print_status "Actualizando a React 18 para mejor compatibilidad..."
    
    # Backup
    cp package.json package.json.backup
    
    # Actualizar React a versión 18
    sed -i 's/"react": "\^19[^"]*"/"react": "^18.2.0"/g' package.json
    sed -i 's/"react-dom": "\^19[^"]*"/"react-dom": "^18.2.0"/g' package.json
    
    # Limpiar y reinstalar
    rm -rf node_modules yarn.lock
    yarn install --legacy-peer-deps
fi

# Verificar scripts de build
if ! grep -q '"docker:build"' package.json; then
    print_status "Agregando script docker:build..."
    # Agregar script docker:build si no existe
    sed -i 's/"build": "craco build"/"build": "craco build",\n    "docker:build": "react-scripts build"/g' package.json
fi

cd ..

# 5. Probar build del frontend
print_status "Probando build del frontend..."
cd frontend

if yarn docker:build &> /dev/null; then
    print_success "Build del frontend exitoso"
else
    print_warning "Build con yarn falló, probando con npx..."
    if npx react-scripts build &> /dev/null; then
        print_success "Build con npx exitoso"
    else
        print_error "Build del frontend falló completamente"
        print_status "Intentando solución alternativa..."
        
        # Limpiar completamente
        rm -rf node_modules build yarn.lock
        
        # Reinstalar con versiones específicas
        yarn add react@18.2.0 react-dom@18.2.0 react-scripts@5.0.1
        yarn install --legacy-peer-deps
        
        # Intentar build nuevamente
        if npx react-scripts build; then
            print_success "Build exitoso después de reinstalación"
        else
            print_error "Build sigue fallando. Revisa los logs detallados."
            exit 1
        fi
    fi
fi

cd ..

# 6. Verificar puertos
print_status "Verificando puertos disponibles..."
for port in 3000 8001 27017; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_warning "Puerto $port está en uso"
        echo "Para liberar el puerto: sudo lsof -ti:$port | xargs kill -9"
    else
        print_success "Puerto $port está disponible"
    fi
done

# 7. Generar credenciales de desarrollo
print_status "Configurando credenciales de desarrollo..."
cd backend

if [ -f "generate_credentials.py" ]; then
    # Generar credenciales automáticamente para desarrollo
    python3 -c "
import secrets, hashlib
username = 'admin'
password = 'admin2024'
jwt_secret = secrets.token_urlsafe(64)
salt = secrets.token_hex(16)
password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
full_hash = f'{salt}:{password_hash.hex()}'
print(f'ADMIN_USERNAME={username}')
print(f'ADMIN_PASSWORD_HASH={full_hash}')
print(f'JWT_SECRET={jwt_secret}')
" > ../dev_credentials.env
    
    # Actualizar .env con credenciales generadas
    source ../dev_credentials.env
    cd ..
    
    # Actualizar .env
    sed -i "s/ADMIN_USERNAME=.*/ADMIN_USERNAME=$ADMIN_USERNAME/" .env
    sed -i "s/ADMIN_PASSWORD_HASH=.*/ADMIN_PASSWORD_HASH=$ADMIN_PASSWORD_HASH/" .env
    sed -i "s/JWT_SECRET=.*/JWT_SECRET=$JWT_SECRET/" .env
    
    print_success "Credenciales de desarrollo configuradas"
    rm -f dev_credentials.env
else
    print_warning "generate_credentials.py no encontrado, usando valores por defecto"
fi

cd ..

# 8. Instrucciones finales
print_success "🎉 Diagnóstico completado!"
echo ""
echo "Para deployar la aplicación:"
echo "1. ./deploy.sh"
echo "   O manualmente:"
echo "2. docker-compose up -d"
echo ""
echo "URLs de acceso:"
echo "- Frontend: http://localhost:3000"
echo "- Backend: http://localhost:8001/api"
echo "- Admin: Clic en 'Admin' → usuario: admin, contraseña: admin2024"
echo ""
echo "Para ver logs:"
echo "docker-compose logs -f"
echo ""
print_success "¡Todo listo para Docker! 🐳"