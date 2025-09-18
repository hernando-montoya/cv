#!/usr/bin/env python3
"""
Script para obtener la IP del contenedor MongoDB y crear un YML corregido
"""

import subprocess
import json
import sys

def get_container_ip(container_name):
    """Obtener la IP de un contenedor específico"""
    try:
        # Obtener información del contenedor
        result = subprocess.run([
            'docker', 'inspect', container_name
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode != 0:
            print(f"❌ Error: Contenedor {container_name} no encontrado")
            return None
        
        # Parsear JSON
        data = json.loads(result.stdout)[0]
        
        # Obtener IP de la red
        networks = data['NetworkSettings']['Networks']
        for network_name, network_info in networks.items():
            ip_address = network_info.get('IPAddress')
            if ip_address:
                print(f"✅ {container_name} en red {network_name}: {ip_address}")
                return ip_address
        
        print(f"❌ No se encontró IP para {container_name}")
        return None
        
    except Exception as e:
        print(f"❌ Error obteniendo IP: {e}")
        return None

def create_fixed_yml(mongodb_ip):
    """Crear YML con IP específica de MongoDB"""
    
    yml_content = f'''# Stack CV App - Con IP específica de MongoDB
# Solución para problema de resolución de hostnames

version: '3.8'

services:
  mongodb:
    image: mongo:5.0
    container_name: cv_mongodb
    restart: unless-stopped
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: securepassword123
      MONGO_INITDB_DATABASE: cv_database
    volumes:
      - mongodb_data:/data/db
      - mongodb_config:/data/configdb
    networks:
      - cv_network

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.no-healthcheck
    container_name: cv_backend
    restart: unless-stopped
    environment:
      # Usar IP específica en lugar de hostname
      MONGO_URL: mongodb://admin:securepassword123@{mongodb_ip}:27017/cv_database?authSource=admin
      DB_NAME: cv_database
      ADMIN_USERNAME: admin
      ADMIN_PASSWORD_HASH: b8d6c1a9b2e5d7f3:a1b2c3d4e5f6789012345678901234567890123456789012345678901234567890
      JWT_SECRET: production_jwt_secret_change_this
      CORS_ORIGINS: "*"
    ports:
      - "8007:8001"
    networks:
      - cv_network
    depends_on:
      - mongodb

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.portainer
      args:
        REACT_APP_BACKEND_URL: http://192.168.1.18:8007
    container_name: cv_frontend
    restart: unless-stopped
    environment:
      REACT_APP_BACKEND_URL: http://192.168.1.18:8007
    ports:
      - "8006:3000"
    networks:
      - cv_network
    depends_on:
      - backend

networks:
  cv_network:
    driver: bridge

volumes:
  mongodb_data:
    driver: local
  mongodb_config:
    driver: local

# 📋 CONFIGURACIÓN:
# MongoDB IP: {mongodb_ip}
# Frontend: http://192.168.1.18:8006
# Backend: http://192.168.1.18:8007
# Sin dependencia de resolución de hostnames'''

    with open('/app/portainer-ip-specific.yml', 'w') as f:
        f.write(yml_content)
    
    print(f"✅ YML creado: portainer-ip-specific.yml")
    print(f"📍 MongoDB IP configurada: {mongodb_ip}")

def main():
    print("🔍 OBTENIENDO IP DEL CONTENEDOR MONGODB")
    print("=" * 50)
    
    # Intentar obtener IP del contenedor MongoDB
    containers_to_try = ['cv_mongodb', 'mongodb']
    
    mongodb_ip = None
    for container in containers_to_try:
        print(f"🧪 Probando contenedor: {container}")
        ip = get_container_ip(container)
        if ip:
            mongodb_ip = ip
            break
    
    if not mongodb_ip:
        print("\n❌ No se pudo obtener la IP de MongoDB")
        print("🔧 Posibles soluciones:")
        print("1. Verificar que el contenedor MongoDB esté corriendo: docker ps")
        print("2. Re-deploy del stack para crear la red correctamente")
        print("3. Usar configuración con host networking")
        sys.exit(1)
    
    # Crear YML con IP específica
    create_fixed_yml(mongodb_ip)
    
    print(f"\n🎯 PRÓXIMOS PASOS:")
    print(f"1. Ve a Portainer → Stack → Editor")
    print(f"2. Reemplaza con el contenido de portainer-ip-specific.yml")
    print(f"3. Update stack → Re-deploy")
    print(f"4. La nueva configuración usará MongoDB IP: {mongodb_ip}")

if __name__ == "__main__":
    main()