#!/usr/bin/env python3
"""
Script de diagnóstico para problemas de conexión MongoDB
"""

import socket
import subprocess
import sys
import os

def check_port(host, port):
    """Verificar si un puerto está abierto"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def run_command(cmd):
    """Ejecutar comando y capturar output"""
    try:
        result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=10)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", "Timeout", 1
    except Exception as e:
        return "", str(e), 1

def main():
    print("🔍 DIAGNÓSTICO DE CONEXIÓN MONGODB")
    print("=" * 50)
    
    # 1. Verificar si Docker está disponible
    print("\n1️⃣ Verificando Docker...")
    stdout, stderr, code = run_command("docker --version")
    if code == 0:
        print(f"✅ Docker disponible: {stdout}")
    else:
        print(f"❌ Docker no disponible: {stderr}")
        print("🔧 Ejecuta este script desde tu servidor donde tienes Docker/Portainer")
        return
    
    # 2. Verificar contenedores
    print("\n2️⃣ Verificando contenedores...")
    stdout, stderr, code = run_command("docker ps")
    if code == 0:
        if "cv_mongodb" in stdout:
            print("✅ Contenedor cv_mongodb está corriendo")
            print("📋 Contenedores activos:")
            lines = stdout.split('\n')
            for line in lines:
                if 'cv_' in line:
                    print(f"   {line}")
        else:
            print("❌ Contenedor cv_mongodb NO encontrado")
            print("📋 Contenedores activos:")
            print(stdout)
    else:
        print(f"❌ Error verificando contenedores: {stderr}")
    
    # 3. Verificar puertos específicos de MongoDB
    print("\n3️⃣ Verificando puertos de MongoDB...")
    stdout, stderr, code = run_command("docker port cv_mongodb")
    if code == 0:
        print(f"✅ Puertos de cv_mongodb: {stdout}")
    else:
        print(f"❌ No se pueden obtener puertos de cv_mongodb: {stderr}")
    
    # 4. Test de conectividad
    print("\n4️⃣ Test de conectividad...")
    hosts_to_test = ["localhost", "127.0.0.1"]
    
    for host in hosts_to_test:
        print(f"🧪 Probando {host}:27017...")
        if check_port(host, 27017):
            print(f"✅ {host}:27017 accesible")
        else:
            print(f"❌ {host}:27017 NO accesible")
    
    # 5. Obtener IP del contenedor MongoDB
    print("\n5️⃣ Obteniendo IP del contenedor...")
    stdout, stderr, code = run_command("docker inspect cv_mongodb")
    if code == 0:
        try:
            import json
            data = json.loads(stdout)
            ip = data[0]['NetworkSettings']['Networks']['cv_network']['IPAddress']
            print(f"📍 IP del contenedor MongoDB: {ip}")
            
            # Test con IP del contenedor
            if check_port(ip, 27017):
                print(f"✅ {ip}:27017 accesible")
                print(f"🔧 Usa esta conexión: mongodb://admin:securepassword123@{ip}:27017/cv_database?authSource=admin")
            else:
                print(f"❌ {ip}:27017 NO accesible")
        except:
            print("❌ No se pudo parsear la información del contenedor")
    else:
        print(f"❌ Error obteniendo info del contenedor: {stderr}")
    
    # 6. Logs de MongoDB
    print("\n6️⃣ Últimos logs de MongoDB...")
    stdout, stderr, code = run_command("docker logs cv_mongodb --tail 5")
    if code == 0:
        print("📜 Logs recientes:")
        print(stdout)
    else:
        print(f"❌ Error obteniendo logs: {stderr}")
    
    print("\n" + "=" * 50)
    print("🔧 SOLUCIONES POSIBLES:")
    print("1. Si el contenedor no existe: redeploy el stack en Portainer")
    print("2. Si el puerto no está expuesto: usa portainer-fixed.yml")
    print("3. Si tienes la IP del contenedor: modifica init_simple.py con esa IP")
    print("4. Alternativamente: ejecuta desde dentro del contenedor")
    print("   docker exec -it cv_backend python init_data.py")

if __name__ == "__main__":
    main()