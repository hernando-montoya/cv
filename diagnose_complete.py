#!/usr/bin/env python3
"""
Diagnóstico completo del sistema CV
"""

import subprocess
import json
import requests
import sys
import time

def run_cmd(cmd, timeout=10):
    """Ejecutar comando con timeout"""
    try:
        result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", "Timeout", 1
    except Exception as e:
        return "", str(e), 1

def check_docker_containers():
    """Verificar contenedores Docker"""
    print("🐳 VERIFICANDO CONTENEDORES DOCKER")
    print("=" * 50)
    
    stdout, stderr, code = run_cmd("docker ps --format json")
    if code != 0:
        print(f"❌ Error verificando contenedores: {stderr}")
        return False
    
    if not stdout.strip():
        print("❌ No hay contenedores corriendo")
        return False
    
    containers = []
    for line in stdout.strip().split('\n'):
        try:
            container = json.loads(line)
            containers.append(container)
            
            name = container.get('Names', 'unknown')
            status = container.get('Status', 'unknown')
            ports = container.get('Ports', 'none')
            
            if 'cv_' in name:
                print(f"✅ {name}")
                print(f"   Estado: {status}")
                print(f"   Puertos: {ports}")
            else:
                print(f"ℹ️  {name} (no relacionado)")
        except json.JSONDecodeError:
            continue
    
    cv_containers = [c for c in containers if 'cv_' in c.get('Names', '')]
    print(f"\n📊 Total contenedores CV: {len(cv_containers)}")
    
    return len(cv_containers) > 0

def check_ports():
    """Verificar puertos específicos"""
    print("\n🔌 VERIFICANDO PUERTOS")
    print("=" * 50)
    
    ports_to_check = [
        (8006, "Frontend"),
        (8007, "Backend (externo)"),
        (8001, "Backend (interno)"),
        (27017, "MongoDB")
    ]
    
    for port, description in ports_to_check:
        stdout, stderr, code = run_cmd(f"netstat -tuln")
        if code == 0 and f":{port}" in stdout:
            print(f"✅ Puerto {port} ({description}) - ABIERTO")
        else:
            print(f"❌ Puerto {port} ({description}) - CERRADO")

def test_backend_endpoints():
    """Probar endpoints del backend"""
    print("\n🧪 PROBANDO ENDPOINTS DEL BACKEND")
    print("=" * 50)
    
    base_urls = [
        "http://localhost:8007",
        "http://127.0.0.1:8007", 
        "http://localhost:8001",
        "http://127.0.0.1:8001"
    ]
    
    endpoints = ["/health", "/api/", "/api/import/status"]
    
    for base_url in base_urls:
        print(f"\n🔗 Probando: {base_url}")
        
        for endpoint in endpoints:
            url = f"{base_url}{endpoint}"
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"   ✅ {endpoint} - OK ({response.status_code})")
                else:
                    print(f"   ⚠️  {endpoint} - Error {response.status_code}")
            except requests.exceptions.ConnectionError:
                print(f"   ❌ {endpoint} - Conexión rechazada")
            except requests.exceptions.Timeout:
                print(f"   ⏰ {endpoint} - Timeout")
            except Exception as e:
                print(f"   💥 {endpoint} - Error: {e}")

def check_docker_logs():
    """Verificar logs de contenedores"""
    print("\n📜 VERIFICANDO LOGS DE CONTENEDORES")
    print("=" * 50)
    
    containers = ["cv_backend", "cv_frontend", "cv_mongodb"]
    
    for container in containers:
        print(f"\n📋 Logs de {container}:")
        stdout, stderr, code = run_cmd(f"docker logs {container} --tail 10")
        
        if code == 0:
            if stdout:
                print("   Últimas líneas:")
                for line in stdout.split('\n')[-5:]:
                    if line.strip():
                        print(f"   {line}")
            else:
                print("   Sin logs recientes")
        else:
            print(f"   ❌ Error obteniendo logs: {stderr}")

def check_network_connectivity():
    """Verificar conectividad de red"""
    print("\n🌐 VERIFICANDO CONECTIVIDAD DE RED")
    print("=" * 50)
    
    # Verificar si Docker está corriendo
    stdout, stderr, code = run_cmd("docker --version")
    if code == 0:
        print(f"✅ Docker disponible: {stdout}")
    else:
        print(f"❌ Docker no disponible: {stderr}")
        return False
    
    # Verificar red de Docker
    stdout, stderr, code = run_cmd("docker network ls")
    if code == 0:
        if "cv_network" in stdout:
            print("✅ Red cv_network encontrada")
        else:
            print("⚠️  Red cv_network no encontrada")
    
    return True

def provide_recommendations():
    """Proporcionar recomendaciones"""
    print("\n💡 RECOMENDACIONES")
    print("=" * 50)
    
    print("1. 🔄 REINICIAR SERVICIOS:")
    print("   docker restart cv_backend cv_frontend")
    print("")
    
    print("2. 🔍 VERIFICAR STACK:")
    print("   - Ve a Portainer → Tu Stack")
    print("   - Verifica que todos los contenedores estén 'running'")
    print("   - Si alguno está 'unhealthy', reinícialo")
    print("")
    
    print("3. 📝 RE-DEPLOY COMPLETO:")
    print("   - Usa portainer-simple-fixed.yml")
    print("   - Update stack → Re-deploy")
    print("")
    
    print("4. 🛠️  SOLUCIÓN MANUAL:")
    print("   - bash fix_env_simple.sh")
    print("   - Rebuild solo el frontend")

def main():
    print("🔍 DIAGNÓSTICO COMPLETO DEL SISTEMA CV")
    print("=" * 60)
    
    # Verificar Docker y contenedores
    if not check_network_connectivity():
        print("❌ Docker no está disponible. Ejecuta desde el servidor con Docker.")
        sys.exit(1)
    
    # Verificar contenedores
    containers_ok = check_docker_containers()
    
    # Verificar puertos
    check_ports()
    
    # Probar endpoints
    test_backend_endpoints()
    
    # Verificar logs
    check_docker_logs()
    
    # Proporcionar recomendaciones
    provide_recommendations()
    
    print(f"\n{'='*60}")
    print("🎯 RESUMEN:")
    if containers_ok:
        print("✅ Contenedores Docker encontrados")
    else:
        print("❌ Problemas con contenedores Docker")
    
    print("📋 Revisa los resultados arriba para identificar el problema específico")

if __name__ == "__main__":
    main()