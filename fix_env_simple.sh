#!/bin/bash

echo "🔧 CORRECTOR SIMPLE DE .ENV"
echo "=============================="

# Archivo .env del frontend
ENV_FILE="/app/frontend/.env"

echo "📂 Archivo a corregir: $ENV_FILE"

# Mostrar contenido actual
if [ -f "$ENV_FILE" ]; then
    echo "📋 Contenido actual:"
    cat "$ENV_FILE"
else
    echo "⚠️  Archivo no existe, se creará"
fi

echo ""
echo "🔧 Aplicando corrección..."

# Crear nuevo contenido
cat > "$ENV_FILE" << EOF
REACT_APP_BACKEND_URL=http://localhost:8007
WDS_SOCKET_PORT=443
EOF

echo "✅ Archivo actualizado"
echo ""
echo "📋 Nuevo contenido:"
cat "$ENV_FILE"

echo ""
echo "🎯 PRÓXIMOS PASOS:"
echo "1. Rebuild el frontend en Portainer (Update stack → Re-deploy)"
echo "2. Ve al Admin Panel → pestaña Debug"
echo "3. Verifica que la conexión funcione"
echo "4. Usa Import → Inicialización Rápida"