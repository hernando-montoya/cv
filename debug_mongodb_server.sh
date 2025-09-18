#!/bin/bash

# Script para diagnosticar MongoDB crasheando en el servidor
# Ejecutar este script en tu servidor donde está Portainer

echo "🚨 DIAGNÓSTICO: MONGODB CONTAINER CRASHEANDO"
echo "============================================================"

echo ""
echo "🔍 ESTADO DE CONTENEDORES"
echo "----------------------------------------"
echo "✅ CONTENEDORES ACTIVOS:"
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'

echo ""
echo "📋 TODOS LOS CONTENEDORES (incluyendo detenidos):"
docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'

echo ""
echo "🔍 LOGS DEL CONTENEDOR MONGODB"
echo "----------------------------------------"

# Intentar obtener logs de diferentes nombres posibles
for container in cv_mongodb mongodb; do
    echo "📋 Probando contenedor: $container"
    if docker logs $container 2>/dev/null; then
        echo "✅ Logs obtenidos de $container"
        break
    else
        echo "❌ Contenedor $container no encontrado o sin logs"
    fi
done

echo ""
echo "🔍 EVENTOS DOCKER RECIENTES (últimos 30 minutos)"
echo "------------------------------------------------"
docker events --since 30m --until now | grep -i mongodb | tail -20

echo ""
echo "🔍 INSPECCIONAR CONTENEDOR MONGODB"
echo "-----------------------------------"
for container in cv_mongodb mongodb; do
    if docker inspect $container >/dev/null 2>&1; then
        echo "📊 ESTADO DE $container:"
        docker inspect $container | jq -r '.[0].State | "Status: \(.Status), Running: \(.Running), ExitCode: \(.ExitCode), Error: \(.Error // "None")"'
        
        echo "🔄 RESTART POLICY:"
        docker inspect $container | jq -r '.[0].RestartPolicy | "Name: \(.Name), MaxRetryCount: \(.MaximumRetryCount)"'
        
        echo "💾 VOLÚMENES:"
        docker inspect $container | jq -r '.[0].Mounts[] | "\(.Source) -> \(.Destination)"'
        break
    fi
done

echo ""
echo "🔍 RECURSOS DEL SISTEMA"
echo "------------------------"
echo "💾 ESPACIO EN DISCO:"
df -h

echo ""
echo "🧠 MEMORIA:"
free -h

echo ""
echo "🔍 VERIFICAR PERMISOS VOLÚMENES"
echo "--------------------------------"
echo "📂 Volúmenes Docker MongoDB:"
docker volume ls | grep -E "(mongodb|cv)"

echo ""
echo "🎯 POSIBLES SOLUCIONES:"
echo "========================"
echo "1. Si ExitCode = 125: Error de configuración o permisos"
echo "2. Si ExitCode = 1: Error de MongoDB (revisar logs)"
echo "3. Si ExitCode = 0: Contenedor se cerró normalmente (configuración)"
echo "4. Si 'no space left on device': Limpiar espacio en disco"
echo "5. Si 'permission denied': Problema de permisos en volúmenes"
echo ""
echo "📋 COMANDOS ÚTILES:"
echo "- Limpiar volúmenes: docker volume prune"
echo "- Reiniciar stack completo en Portainer"
echo "- Verificar logs en tiempo real: docker logs -f cv_mongodb"