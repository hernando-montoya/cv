#!/usr/bin/env python3
"""
Script simple para probar conectividad MongoDB
"""

import socket
import subprocess
import json

def test_port_connectivity(host, port, timeout=5):
    """Probar conectividad a un puerto específico"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"❌ Error probando conexión: {e}")
        return False

def check_docker_containers():
    """Verificar estado de contenedores Docker"""
    try:
        result = subprocess.run(['docker', 'ps', '--format', 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("📋 CONTENEDORES ACTIVOS:")
            print(result.stdout)
        else:
            print("❌ Error obteniendo estado de contenedores")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🔍 DIAGNÓSTICO MONGODB - PUERTO Y CONECTIVIDAD")
    print("=" * 60)
    
    # 1. Verificar contenedores Docker
    check_docker_containers()
    print()
    
    # 2. Probar conectividad a diferentes configuraciones
    test_configs = [
        ("localhost", 27017, "MongoDB local"),
        ("192.168.1.18", 27017, "MongoDB en servidor"),
        ("127.0.0.1", 27017, "MongoDB loopback")
    ]
    
    print("🧪 PROBANDO CONECTIVIDAD:")
    print("-" * 40)
    
    for host, port, description in test_configs:
        print(f"Testing {description} ({host}:{port})... ", end="")
        if test_port_connectivity(host, port):
            print("✅ CONECTA")
        else:
            print("❌ NO CONECTA")
    
    print()
    print("🔧 PRÓXIMOS PASOS:")
    print("1. Si no conecta: el stack necesita re-deploy con puerto corregido")
    print("2. Si conecta: probar connection string completa de MongoDB")
    print("3. Stack corregido disponible: portainer-mongodb-fixed.yml")

if __name__ == "__main__":
    main()