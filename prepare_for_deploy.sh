#!/bin/bash

# Script para preparar la aplicación para deploy en Portainer
echo "🚀 PREPARANDO APLICACIÓN PARA DEPLOY"
echo "===================================="

# Verificar si estamos en el directorio correcto
if [ ! -f "package.json" ] && [ ! -d "frontend" ]; then
    echo "❌ Error: Ejecutar desde el directorio raíz del proyecto"
    exit 1
fi

echo ""
echo "📦 1. COMPILANDO FRONTEND..."
cd frontend

# Verificar si existe yarn.lock
if [ -f "yarn.lock" ]; then
    echo "✅ Usando Yarn..."
    yarn install --frozen-lockfile
    yarn build
else
    echo "✅ Usando NPM..."
    npm install
    npm run build
fi

# Verificar que el build fue exitoso
if [ -d "build" ] && [ -f "build/index.html" ]; then
    echo "✅ Frontend compilado exitosamente"
    ls -la build/ | head -5
else
    echo "❌ Error: No se pudo compilar el frontend"
    exit 1
fi

cd ..

echo ""
echo "🔧 2. VERIFICANDO BACKEND..."
cd backend

# Verificar archivos importantes
if [ -f "server.py" ] && [ -f "json_storage.py" ] && [ -f "requirements.txt" ]; then
    echo "✅ Archivos del backend encontrados"
else
    echo "❌ Error: Faltan archivos del backend"
    exit 1
fi

cd ..

echo ""
echo "📋 3. VERIFICANDO DOCKERFILES..."
if [ -f "Dockerfile.prebuilt" ]; then
    echo "✅ Dockerfile.prebuilt encontrado"
else
    echo "❌ Error: Dockerfile.prebuilt no encontrado"
    exit 1
fi

if [ -f "portainer-single-app.yml" ]; then
    echo "✅ portainer-single-app.yml encontrado"
else
    echo "❌ Error: portainer-single-app.yml no encontrado"
    exit 1
fi

echo ""
echo "🧪 4. PRUEBA RÁPIDA DEL BUILD..."
echo "Verificando que el Dockerfile puede leer los archivos..."

# Verificar estructura mínima
echo "Frontend build: $(ls -1 frontend/build/ | wc -l) archivos"
echo "Backend files: $(ls -1 backend/*.py | wc -l) archivos Python"

echo ""
echo "✅ 5. ¡PREPARACIÓN COMPLETA!"
echo "=========================="
echo ""
echo "📋 ARCHIVOS LISTOS PARA PORTAINER:"
echo "- ✅ Frontend compilado: frontend/build/"
echo "- ✅ Backend preparado: backend/"
echo "- ✅ Dockerfile: Dockerfile.prebuilt"
echo "- ✅ Stack: portainer-single-app.yml"
echo ""
echo "🚀 PRÓXIMOS PASOS:"
echo "1. Subir código a repositorio Git"
echo "2. En Portainer: Stacks → Add Stack"
echo "3. Repository URL: [tu-repo]"
echo "4. Compose file: portainer-single-app.yml"
echo "5. Deploy stack"
echo ""
echo "🌐 DESPUÉS DEL DEPLOY:"
echo "- App: http://tu-servidor:8000"
echo "- Admin: http://tu-servidor:8000/admin"
echo "- Health: http://tu-servidor:8000/health"
echo ""
echo "🔐 LOGIN ADMIN:"
echo "- Usuario: admin"
echo "- Password: password123"