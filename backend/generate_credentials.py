#!/usr/bin/env python3
"""
Script para generar credenciales seguras de producción
Ejecuta: python generate_credentials.py
"""

import secrets
import hashlib
import getpass
import sys

def generate_secure_credentials():
    """Genera credenciales seguras para producción"""
    
    print("=" * 70)
    print("        GENERADOR DE CREDENCIALES SEGURAS DE PRODUCCIÓN")
    print("=" * 70)
    print()
    
    # Solicitar nuevo usuario
    while True:
        username = input("📝 Nuevo usuario admin (mínimo 4 caracteres): ").strip()
        if len(username) >= 4 and username != "admin":
            break
        print("❌ El usuario debe tener al menos 4 caracteres y no ser 'admin'")
    
    # Solicitar nueva contraseña
    while True:
        password = getpass.getpass("🔐 Nueva contraseña admin (mínimo 8 caracteres): ")
        if len(password) >= 8:
            password_confirm = getpass.getpass("🔐 Confirma la contraseña: ")
            if password == password_confirm:
                break
            else:
                print("❌ Las contraseñas no coinciden. Intenta de nuevo.")
        else:
            print("❌ La contraseña debe tener al menos 8 caracteres")
    
    # Generar JWT secret seguro
    jwt_secret = secrets.token_urlsafe(64)
    
    # Generar hash de contraseña
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    full_hash = f"{salt}:{password_hash.hex()}"
    
    print("\n" + "=" * 70)
    print("              VARIABLES DE ENTORNO PARA PRODUCCIÓN")
    print("=" * 70)
    print()
    print("Copia y pega estas variables en tu servidor de producción:")
    print()
    print("# Autenticación")
    print(f"ADMIN_USERNAME={username}")
    print(f"ADMIN_PASSWORD_HASH={full_hash}")
    print(f"JWT_SECRET={jwt_secret}")
    print()
    print("# Base de datos")
    print("MONGO_URL=mongodb://localhost:27017/cv_production")
    print("DB_NAME=cv_production")
    print()
    print("# Frontend")
    print("REACT_APP_BACKEND_URL=https://tu-dominio.com")
    print()
    print("=" * 70)
    print("⚠️  IMPORTANTE: Guarda estas variables de forma segura")
    print("⚠️  NO las compartas ni las subas a repositorios públicos")
    print("=" * 70)
    
    # Generar archivo .env ejemplo
    env_content = f"""# Variables de entorno para producción
# Copia este archivo a tu servidor y ajusta las URLs

# Autenticación
ADMIN_USERNAME={username}
ADMIN_PASSWORD_HASH={full_hash}
JWT_SECRET={jwt_secret}

# Base de datos
MONGO_URL=mongodb://localhost:27017/cv_production
DB_NAME=cv_production

# Frontend
REACT_APP_BACKEND_URL=https://tu-dominio.com
"""
    
    try:
        with open('production.env', 'w') as f:
            f.write(env_content)
        print(f"✅ Archivo 'production.env' creado con las variables")
        print("   Cópialo a tu servidor de producción")
    except Exception as e:
        print(f"⚠️  No se pudo crear el archivo: {e}")
    
    print()
    print("🎉 Credenciales generadas exitosamente!")
    print()
    print("Próximos pasos:")
    print("1. Configura estas variables en tu servidor")
    print("2. Reinicia el backend")
    print("3. Prueba el acceso con las nuevas credenciales")

if __name__ == "__main__":
    try:
        generate_secure_credentials()
    except KeyboardInterrupt:
        print("\n\n❌ Operación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)