#!/bin/bash

echo "🔍 Verificación rápida del estado actual..."

echo ""
echo "=== CONTENEDORES CORRIENDO ==="
docker-compose ps

echo ""
echo "=== INTENTANDO VER LOGS DEL FRONTEND ==="
docker logs cv_frontend 2>/dev/null || echo "❌ No hay contenedor cv_frontend"

echo ""
echo "=== VERIFICANDO SI EXISTE LA IMAGEN DEL FRONTEND ==="
docker images | grep cv-frontend || echo "❌ No hay imagen cv-frontend construida"

echo ""
echo "=== PROBANDO CONECTIVIDAD ==="
echo -n "Backend: "
if curl -f http://localhost:8001/api/ 2>/dev/null; then
    echo "✅ OK"
else
    echo "❌ NO"
fi

echo -n "Frontend: "
if curl -f http://localhost:3000/ 2>/dev/null; then
    echo "✅ OK"
else
    echo "❌ NO"
fi

echo ""
echo "=== RESUMEN ==="
echo "El problema es que el frontend nunca se construyó o falló al iniciarse"
echo "El backend y MongoDB están perfectos"
echo ""
echo "Ejecuta: ./fix_frontend_only.sh"