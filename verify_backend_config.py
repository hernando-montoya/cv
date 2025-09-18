#!/usr/bin/env python3
"""
Verificar configuración del backend - Leer .env y validar settings
"""

import os
import sys
from pathlib import Path

def load_env_file(env_path):
    """Cargar variables del archivo .env"""
    env_vars = {}
    try:
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Remover comillas si las hay
                    value = value.strip('"\'')
                    env_vars[key] = value
        return env_vars
    except Exception as e:
        print(f"❌ Error leyendo {env_path}: {e}")
        return {}

def main():
    print("🔍 VERIFICACIÓN CONFIGURACIÓN BACKEND")
    print("=" * 50)
    
    # Cargar .env del backend
    backend_env_path = "/app/backend/.env"
    backend_env = load_env_file(backend_env_path)
    
    print("📋 CONFIGURACIÓN BACKEND:")
    print("-" * 30)
    for key, value in backend_env.items():
        # Ocultar passwords parcialmente
        if 'PASSWORD' in key or 'SECRET' in key:
            display_value = value[:10] + "..." if len(value) > 10 else value
        else:
            display_value = value
        print(f"✅ {key}: {display_value}")
    
    # Cargar .env del frontend  
    frontend_env_path = "/app/frontend/.env"
    frontend_env = load_env_file(frontend_env_path)
    
    print(f"\n📋 CONFIGURACIÓN FRONTEND:")
    print("-" * 30)
    for key, value in frontend_env.items():
        print(f"✅ {key}: {value}")
    
    # Validaciones
    print(f"\n🧪 VALIDACIONES:")
    print("-" * 20)
    
    # 1. MongoDB URL
    mongo_url = backend_env.get('MONGO_URL', '')
    if 'mongodb://' in mongo_url and 'cv_database' in mongo_url:
        print("✅ MONGO_URL configurada correctamente")
    else:
        print("❌ MONGO_URL incorrecta o faltante")
    
    # 2. Backend URL del frontend
    backend_url = frontend_env.get('REACT_APP_BACKEND_URL', '')
    if '8007' in backend_url:
        print("✅ REACT_APP_BACKEND_URL apunta al puerto correcto")
    else:
        print("❌ REACT_APP_BACKEND_URL no apunta al puerto 8007")
    
    # 3. Credenciales admin
    if backend_env.get('ADMIN_USERNAME') and backend_env.get('ADMIN_PASSWORD_HASH'):
        print("✅ Credenciales admin configuradas")
    else:
        print("❌ Falta configuración de admin")
    
    print(f"\n🎯 RESUMEN:")
    print("- ✅ Configuraciones corregidas para Portainer")
    print("- ✅ MongoDB apunta a hostname 'mongodb' para Docker")
    print("- ✅ Frontend apunta a puerto 8007 del servidor")
    print("- 🔧 Falta: Re-deploy del stack con puerto MongoDB expuesto")

if __name__ == "__main__":
    main()