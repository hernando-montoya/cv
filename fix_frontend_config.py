#!/usr/bin/env python3
"""
Script para corregir automáticamente la configuración del frontend
Detecta el entorno y configura la URL correcta del backend
"""

import os
import sys
import requests
import time

def detect_environment():
    """Detectar si estamos en Docker o desarrollo local"""
    if os.path.exists('/.dockerenv'):
        return 'docker'
    elif os.environ.get('DOCKER_ENV'):
        return 'docker'
    else:
        return 'local'

def test_backend_url(url, timeout=5):
    """Probar si una URL del backend funciona"""
    try:
        response = requests.get(f"{url}/health", timeout=timeout)
        return response.status_code == 200
    except:
        return False

def find_working_backend_url():
    """Encontrar una URL del backend que funcione"""
    
    env = detect_environment()
    
    # URLs candidatas según el entorno
    if env == 'docker':
        candidates = [
            "http://backend:8001",
            "http://cv_backend:8001", 
            "http://localhost:8007",
            "http://127.0.0.1:8007"
        ]
    else:
        candidates = [
            "http://localhost:8007",
            "http://127.0.0.1:8007",
            "http://localhost:8001",
            "http://127.0.0.1:8001"
        ]
    
    print(f"🔍 Detectado entorno: {env}")
    print(f"🧪 Probando URLs candidatas...")
    
    for url in candidates:
        print(f"   Probando: {url}")
        if test_backend_url(url):
            print(f"   ✅ Funciona: {url}")
            return url
        else:
            print(f"   ❌ No funciona: {url}")
    
    return None

def update_frontend_env(backend_url):
    """Actualizar el archivo .env del frontend"""
    
    env_file = '/app/frontend/.env'
    
    if not os.path.exists(env_file):
        print(f"⚠️  Archivo {env_file} no existe, creándolo...")
    
    # Leer contenido actual
    content = ""
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            content = f.read()
    
    # Actualizar o agregar REACT_APP_BACKEND_URL
    lines = content.split('\n')
    updated = False
    
    for i, line in enumerate(lines):
        if line.startswith('REACT_APP_BACKEND_URL='):
            lines[i] = f'REACT_APP_BACKEND_URL={backend_url}'
            updated = True
            break
    
    if not updated:
        lines.append(f'REACT_APP_BACKEND_URL={backend_url}')
    
    # Escribir archivo actualizado
    new_content = '\n'.join(line for line in lines if line.strip())
    
    try:
        with open(env_file, 'w') as f:
            f.write(new_content + '\n')
        print(f"✅ Archivo {env_file} actualizado")
        return True
    except Exception as e:
        print(f"❌ Error escribiendo {env_file}: {e}")
        return False

def show_current_config():
    """Mostrar la configuración actual"""
    env_file = '/app/frontend/.env'
    
    print(f"\n📋 CONFIGURACIÓN ACTUAL:")
    print(f"Archivo: {env_file}")
    
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            content = f.read()
        print("Contenido:")
        for line in content.split('\n'):
            if line.strip():
                print(f"  {line}")
    else:
        print("  Archivo no existe")

def main():
    print("🔧 CORRECTOR DE CONFIGURACIÓN FRONTEND")
    print("=" * 50)
    
    # Mostrar configuración actual
    show_current_config()
    
    # Buscar URL que funcione
    working_url = find_working_backend_url()
    
    if not working_url:
        print("\n❌ No se encontró ninguna URL del backend que funcione")
        print("\n💡 VERIFICA:")
        print("1. Que el contenedor backend esté corriendo")
        print("2. Que el puerto 8007 esté mapeado")
        print("3. Que el backend responda en /health")
        sys.exit(1)
    
    print(f"\n✅ URL del backend encontrada: {working_url}")
    
    # Actualizar configuración
    if update_frontend_env(working_url):
        print(f"\n🎉 Configuración actualizada correctamente")
        print(f"URL del backend: {working_url}")
        
        print(f"\n📝 PRÓXIMOS PASOS:")
        print(f"1. Reinicia el frontend si es necesario")
        print(f"2. Ve al Admin Panel → pestaña 'Debug'")
        print(f"3. Verifica que la conexión funcione")
        print(f"4. Usa la pestaña 'Import' para cargar datos")
    else:
        print(f"\n❌ Error actualizando la configuración")
        sys.exit(1)

if __name__ == "__main__":
    main()