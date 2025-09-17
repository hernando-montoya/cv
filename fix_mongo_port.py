#!/usr/bin/env python3
"""
Script para forzar que MongoDB mantenga el puerto expuesto
"""

import subprocess
import json
import time
import sys

def run_cmd(cmd, timeout=10):
    """Ejecutar comando con timeout"""
    try:
        result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", "Timeout", 1
    except Exception as e:
        return "", str(e), 1

def get_container_info():
    """Obtener información detallada del contenedor"""
    stdout, stderr, code = run_cmd("docker inspect cv_mongodb")
    if code != 0:
        return None
    
    try:
        data = json.loads(stdout)[0]
        return {
            "id": data["Id"][:12],
            "state": data["State"]["Status"],
            "restart_count": data["RestartCount"],
            "ports": data["NetworkSettings"]["Ports"],
            "port_bindings": data["HostConfig"]["PortBindings"]
        }
    except:
        return None

def check_port_binding():
    """Verificar si el puerto está correctamente vinculado"""
    info = get_container_info()
    if not info:
        return False, "Container not found"
    
    # Verificar PortBindings en HostConfig
    port_bindings = info.get("port_bindings", {})
    if "27017/tcp" not in port_bindings:
        return False, "Port 27017 not in PortBindings"
    
    # Verificar Ports en NetworkSettings
    ports = info.get("ports", {})
    if "27017/tcp" not in ports or not ports["27017/tcp"]:
        return False, "Port 27017 not exposed in NetworkSettings"
    
    return True, "Port correctly bound"

def force_port_exposure():
    """Forzar que el puerto se mantenga expuesto"""
    print("🔧 FORZANDO EXPOSICIÓN DEL PUERTO 27017")
    print("=" * 50)
    
    # 1. Verificar estado actual
    print("1️⃣ Verificando estado actual...")
    is_bound, msg = check_port_binding()
    print(f"   Estado: {msg}")
    
    if is_bound:
        print("✅ El puerto está correctamente configurado")
        return True
    
    # 2. Intentar restart del contenedor
    print("\n2️⃣ Reiniciando contenedor para forzar configuración...")
    stdout, stderr, code = run_cmd("docker restart cv_mongodb")
    if code != 0:
        print(f"❌ Error reiniciando: {stderr}")
        return False
    
    print("⏳ Esperando que el contenedor arranque...")
    time.sleep(15)
    
    # 3. Verificar de nuevo
    print("\n3️⃣ Verificando después del reinicio...")
    is_bound, msg = check_port_binding()
    print(f"   Estado: {msg}")
    
    if is_bound:
        print("✅ Puerto expuesto correctamente después del reinicio")
        return True
    
    # 4. Si sigue fallando, recrear el contenedor
    print("\n4️⃣ El reinicio no funcionó. Intentando recrear...")
    print("⚠️  Esto recreará el contenedor con la configuración correcta")
    
    response = input("¿Continuar? (y/N): ").lower()
    if response not in ['y', 'yes', 'sí', 's']:
        print("Operación cancelada")
        return False
    
    # Obtener información del stack
    print("📋 Obteniendo configuración del stack...")
    
    # Parar y remover el contenedor actual
    print("🛑 Parando contenedor actual...")
    run_cmd("docker stop cv_mongodb")
    run_cmd("docker rm cv_mongodb")
    
    print("❌ ATENCIÓN: El contenedor ha sido removido.")
    print("🔧 SOLUCIÓN: Re-deploy tu stack en Portainer usando portainer-fixed.yml")
    print("   Esto recreará el contenedor con la configuración correcta de puertos")
    
    return False

def create_port_monitor():
    """Crear un script de monitoreo permanente"""
    monitor_script = '''#!/bin/bash
# Monitor automático del puerto MongoDB
# Se ejecuta cada 30 segundos

while true; do
    if ! nc -z localhost 27017 2>/dev/null; then
        echo "[$(date)] Puerto 27017 no accesible, reiniciando MongoDB..."
        docker restart cv_mongodb
        sleep 30
    fi
    sleep 30
done
'''
    
    with open('/tmp/mongo_port_monitor.sh', 'w') as f:
        f.write(monitor_script)
    
    run_cmd("chmod +x /tmp/mongo_port_monitor.sh")
    print("📝 Monitor creado en /tmp/mongo_port_monitor.sh")
    print("🚀 Para ejecutar en background: nohup /tmp/mongo_port_monitor.sh &")

def main():
    print("🔧 SOLUCIONADOR DE PUERTO MONGODB")
    print("=" * 40)
    
    # Verificar si Docker está disponible
    stdout, stderr, code = run_cmd("docker --version")
    if code != 0:
        print("❌ Docker no está disponible")
        print("🔧 Ejecuta este script desde tu servidor con Docker")
        sys.exit(1)
    
    # Verificar si el contenedor existe
    stdout, stderr, code = run_cmd("docker ps -a --filter name=cv_mongodb")
    if "cv_mongodb" not in stdout:
        print("❌ Contenedor cv_mongodb no encontrado")
        print("🔧 Deploy el stack en Portainer primero")
        sys.exit(1)
    
    # Intentar forzar la exposición del puerto
    success = force_port_exposure()
    
    if not success:
        print("\n💡 RECOMENDACIONES:")
        print("1. Re-deploy el stack con portainer-fixed.yml")
        print("2. Verifica que el YML incluye:")
        print("   ports:")
        print("     - '27017:27017'")
        print("3. Considera usar el monitor automático")
        
        create_monitor = input("\n¿Crear monitor automático? (y/N): ").lower()
        if create_monitor in ['y', 'yes', 'sí', 's']:
            create_port_monitor()

if __name__ == "__main__":
    main()