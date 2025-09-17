#!/bin/bash

echo "🔍 Verificando estado de MongoDB..."

echo "📋 Contenedores activos:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "🔌 Puertos de MongoDB:"
docker port cv_mongodb 2>/dev/null || echo "❌ Contenedor cv_mongodb no encontrado"

echo ""
echo "📊 Estado específico de MongoDB:"
docker inspect cv_mongodb --format='{{.State.Status}}' 2>/dev/null || echo "❌ Contenedor cv_mongodb no encontrado"

echo ""
echo "📜 Últimas líneas del log de MongoDB:"
docker logs cv_mongodb --tail 10 2>/dev/null || echo "❌ No se pueden obtener logs de cv_mongodb"

echo ""
echo "🧪 Test de conexión a MongoDB:"
echo "Intentando conectar a localhost:27017..."

# Intentar conexión simple
if command -v mongosh >/dev/null 2>&1; then
    echo "Usando mongosh..."
    timeout 5 mongosh --host localhost:27017 --username admin --password securepassword123 --eval "db.adminCommand('ping')" 2>/dev/null && echo "✅ Conexión exitosa" || echo "❌ Conexión fallida"
else
    echo "mongosh no disponible, usando netcat..."
    timeout 3 bash -c "</dev/tcp/localhost/27017" 2>/dev/null && echo "✅ Puerto 27017 accesible" || echo "❌ Puerto 27017 no accesible"
fi