#!/bin/bash

# Script para probar la aplicación de un solo contenedor
echo "🧪 PROBANDO APLICACIÓN DE UN SOLO CONTENEDOR"
echo "=============================================="

# Variables
IMAGE_NAME="cv-app-single"
CONTAINER_NAME="cv-app-test"
PORT="8000"

echo ""
echo "📦 1. CONSTRUYENDO IMAGEN..."
docker build -f Dockerfile.single -t $IMAGE_NAME . 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Imagen construida exitosamente"
else
    echo "❌ Error construyendo imagen"
    exit 1
fi

echo ""
echo "🚀 2. INICIANDO CONTENEDOR..."
docker rm -f $CONTAINER_NAME 2>/dev/null
docker run -d \
    --name $CONTAINER_NAME \
    -p $PORT:8000 \
    -e CORS_ORIGINS="*" \
    -e ADMIN_USERNAME="admin" \
    -e ADMIN_PASSWORD_HASH="b8d6c1a9b2e5d7f3:a1b2c3d4e5f6789012345678901234567890123456789012345678901234567890" \
    -e JWT_SECRET="test_secret" \
    $IMAGE_NAME

if [ $? -eq 0 ]; then
    echo "✅ Contenedor iniciado en puerto $PORT"
else
    echo "❌ Error iniciando contenedor"
    exit 1
fi

echo ""
echo "⏳ 3. ESPERANDO QUE LA APLICACIÓN INICIE..."
sleep 10

echo ""
echo "🔍 4. PROBANDO ENDPOINTS..."

# Test 1: Health check
echo "📋 Health Check:"
curl -s http://localhost:$PORT/health | jq . 2>/dev/null || echo "❌ Health check failed"

# Test 2: API Content
echo ""
echo "📋 API Content:"
curl -s http://localhost:$PORT/api/content/ | jq '.personalInfo.name' 2>/dev/null || echo "❌ Content API failed"

# Test 3: Frontend (HTML)
echo ""
echo "📋 Frontend:"
response=$(curl -s -w "%{http_code}" -o /dev/null http://localhost:$PORT/)
if [ "$response" = "200" ]; then
    echo "✅ Frontend serving correctly (HTTP 200)"
else
    echo "❌ Frontend not serving correctly (HTTP $response)"
fi

# Test 4: Admin page
echo ""
echo "📋 Admin Page:"
response=$(curl -s -w "%{http_code}" -o /dev/null http://localhost:$PORT/admin)
if [ "$response" = "200" ]; then
    echo "✅ Admin page accessible (HTTP 200)"
else
    echo "❌ Admin page not accessible (HTTP $response)"
fi

echo ""
echo "📊 5. ESTADO DEL CONTENEDOR:"
docker ps --filter name=$CONTAINER_NAME --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "📜 6. LOGS DEL CONTENEDOR (últimas 10 líneas):"
docker logs --tail 10 $CONTAINER_NAME

echo ""
echo "🎯 RESUMEN:"
echo "- Imagen: $IMAGE_NAME"
echo "- Contenedor: $CONTAINER_NAME"
echo "- Puerto: http://localhost:$PORT"
echo "- Admin: http://localhost:$PORT/admin"
echo "- Health: http://localhost:$PORT/health"

echo ""
echo "🧹 Para limpiar después de las pruebas:"
echo "docker rm -f $CONTAINER_NAME"
echo "docker rmi $IMAGE_NAME"