#!/usr/bin/env python3
"""
Test específico para la inicialización del CV
"""

import requests
import json
import sys

# Configuración
SERVER_IP = "192.168.1.18"
BACKEND_URL = f"http://{SERVER_IP}:8007"
FRONTEND_URL = f"http://{SERVER_IP}:8006"

# Credenciales por defecto
USERNAME = "admin"
PASSWORD = "password123"

def test_backend_endpoints():
    """Probar endpoints del backend"""
    print("🔗 PROBANDO BACKEND ENDPOINTS")
    print("=" * 40)
    
    endpoints = [
        ("/health", "Health Check"),
        ("/api/", "API Root"),
        ("/api/import/status", "Import Status")
    ]
    
    for endpoint, name in endpoints:
        url = f"{BACKEND_URL}{endpoint}"
        try:
            response = requests.get(url, timeout=5)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} {name}: {response.status_code}")
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   📄 {data}")
                except:
                    print(f"   📄 {response.text[:100]}")
        except Exception as e:
            print(f"❌ {name}: {e}")
        print()

def get_auth_token():
    """Obtener token de autenticación"""
    print("🔑 OBTENIENDO TOKEN DE AUTENTICACIÓN")
    print("=" * 40)
    
    login_url = f"{BACKEND_URL}/api/auth/login"
    login_data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    
    try:
        response = requests.post(
            login_url, 
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Login request to: {login_url}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            if token:
                print("✅ Token obtenido correctamente")
                print(f"   Token: {token[:50]}...")
                return token
            else:
                print("❌ Token no encontrado en respuesta")
                print(f"   Response: {data}")
        else:
            print(f"❌ Error en login: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error en login: {e}")
    
    return None

def test_quick_init(token):
    """Probar inicialización rápida"""
    print("\n🚀 PROBANDO INICIALIZACIÓN RÁPIDA")
    print("=" * 40)
    
    if not token:
        print("❌ No hay token, no se puede probar inicialización")
        return False
    
    init_url = f"{BACKEND_URL}/api/import/quick-init"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        print(f"POST to: {init_url}")
        response = requests.post(init_url, headers=headers, timeout=15)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Inicialización exitosa!")
            print(f"   Mensaje: {data.get('message', 'N/A')}")
            if 'records_count' in data:
                records = data['records_count']
                print(f"   Experiencias: {records.get('experiences', 0)}")
                print(f"   Educación: {records.get('education', 0)}")
                print(f"   Idiomas: {records.get('languages', 0)}")
            return True
        else:
            print(f"❌ Error en inicialización: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error en inicialización: {e}")
    
    return False

def check_frontend():
    """Verificar frontend"""
    print(f"\n🖥️  VERIFICANDO FRONTEND")
    print("=" * 40)
    
    frontend_urls = [
        (f"{FRONTEND_URL}", "Frontend Root"),
        (f"{FRONTEND_URL}/admin", "Admin Panel")
    ]
    
    for url, name in frontend_urls:
        try:
            response = requests.get(url, timeout=5)
            status = "✅" if response.status_code == 200 else "⚠️"
            print(f"{status} {name}: {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: {e}")

def main():
    print("🧪 TEST COMPLETO DE INICIALIZACIÓN")
    print(f"🔗 Backend: {BACKEND_URL}")
    print(f"🖥️  Frontend: {FRONTEND_URL}")
    print("=" * 50)
    
    # 1. Probar backend
    test_backend_endpoints()
    
    # 2. Verificar frontend
    check_frontend()
    
    # 3. Obtener token
    token = get_auth_token()
    
    # 4. Probar inicialización
    success = test_quick_init(token)
    
    print("\n" + "=" * 50)
    print("🎯 RESUMEN:")
    if success:
        print("✅ La inicialización funciona correctamente")
        print(f"👉 Ve a: {FRONTEND_URL}/admin")
        print("👉 Login: admin / password123")
        print("👉 Ve a pestaña Import para verificar datos")
    else:
        print("❌ Hay problemas con la inicialización")
        print("🔧 Posibles causas:")
        print("   - Problemas de autenticación")
        print("   - Base de datos no accesible")
        print("   - Frontend no tiene IP correcta")
        print(f"👉 Intenta rebuild del frontend con IP: {SERVER_IP}")

if __name__ == "__main__":
    main()