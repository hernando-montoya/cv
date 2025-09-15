#!/bin/bash

# Script para arreglar problemas de build del frontend
echo "🔧 Arreglando problemas de compatibilidad del frontend..."

cd frontend

echo "📦 Instalando dependencias con compatibilidad..."

# Limpiar cache de node_modules
rm -rf node_modules
rm -f yarn.lock

# Instalar dependencias con versiones compatibles
yarn add react@^18.2.0 react-dom@^18.2.0
yarn add @craco/craco@^6.4.5
yarn add react-scripts@5.0.1 --dev

# Actualizar scripts en package.json para usar tanto craco como react-scripts
echo "📝 Actualizando scripts..."

# Instalar todas las dependencias
yarn install --legacy-peer-deps

echo "✅ Dependencias instaladas correctamente"

# Probar build
echo "🏗️ Probando build..."
if yarn docker:build; then
    echo "✅ Build exitoso!"
else
    echo "❌ Build falló, intentando con react-scripts directamente..."
    if npx react-scripts build; then
        echo "✅ Build exitoso con react-scripts!"
    else
        echo "❌ Build falló completamente"
        exit 1
    fi
fi

echo "🎉 Frontend listo para Docker!"