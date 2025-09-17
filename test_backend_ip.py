#!/usr/bin/env python3
"""
Test rápido del backend con la IP real
"""

import requests
import sys

# IP y puerto del servidor
SERVER_IP = "192.168.1.18"
BACKEND_PORT = "8007"
BASE_URL = f"http://{SERVER_IP}:{BACKEND_PORT}"

def test_endpoint(endpoint, description):
    """Probar un endpoint específico"""
    url = f"{BASE_URL}{endpoint}"
    try:
        print(f"🧪 Probando {description}:")
        print(f"   URL: {url}")
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print(f"   ✅ SUCCESS - Status: {response.status_code}")
            try:
                data = response.json()
                print(f"   📄 Response: {data}")
            except:
                print(f"   📄 Response: {response.text[:100]}...")
        else:
            print(f"   ⚠️  ERROR - Status: {response.status_code}")
            print(f"   📄 Response: {response.text[:200]}")
            
        return response.status_code == 200
        
    except requests.exceptions.ConnectionError:
        print(f"   ❌ FAILED - Connection refused")
        return False
    except requests.exceptions.Timeout:
        print(f"   ⏰ FAILED - Timeout")
        return False
    except Exception as e:
        print(f"   💥 FAILED - Error: {e}")
        return False

def main():
    print("🚀 TEST BACKEND CON IP REAL")
    print(f"🔗 Servidor: {SERVER_IP}:{BACKEND_PORT}")
    print("=" * 50)
    
    # Endpoints a probar
    tests = [
        ("/health", "Health Check"),
        ("/api/", "API Root"),
        ("/api/import/status", "Import Status"),
        ("/", "Root (debería fallar con 404)")
    ]
    
    success_count = 0
    total_tests = len(tests) - 1  # Excluir el test que debe fallar
    
    for endpoint, description in tests:
        success = test_endpoint(endpoint, description)
        if endpoint != "/" and success:  # No contar el root que debe fallar
            success_count += 1
        print()
    
    print("=" * 50)
    print(f"📊 RESUMEN: {success_count}/{total_tests} tests exitosos")
    
    if success_count >= 2:
        print("✅ BACKEND FUNCIONANDO CORRECTAMENTE")
        print(f"🎯 Actualiza frontend para usar: {BASE_URL}")
        print()
        print("📝 PRÓXIMOS PASOS:")
        print("1. Re-deploy usando portainer-ip-fixed.yml")
        print("2. O rebuild solo el frontend con la IP correcta")
        print(f"3. Ve a: http://{SERVER_IP}:8006/admin")
        print("4. Prueba Import → Inicialización Rápida")
    else:
        print("❌ BACKEND CON PROBLEMAS")
        print("🔧 Verifica logs: docker logs cv_backend")
    
    return success_count >= 2

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)