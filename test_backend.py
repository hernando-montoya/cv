#!/usr/bin/env python3
"""
Script para verificar que el backend esté funcionando correctamente
"""

import requests
import time
import sys

def test_backend_health(base_url="http://localhost:8007"):
    """Test que el backend responda correctamente"""
    
    print(f"🧪 Probando backend en {base_url}")
    
    # Test endpoints
    endpoints = [
        ("/health", "Health check endpoint"),
        ("/api/", "API root endpoint"),
        ("/api/import/status", "Import status endpoint")
    ]
    
    for endpoint, description in endpoints:
        url = f"{base_url}{endpoint}"
        try:
            print(f"\n📡 Probando: {description}")
            print(f"   URL: {url}")
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"   ✅ Status: {response.status_code}")
                try:
                    data = response.json()
                    print(f"   📄 Response: {data}")
                except:
                    print(f"   📄 Response: {response.text[:100]}...")
            else:
                print(f"   ⚠️  Status: {response.status_code}")
                print(f"   📄 Response: {response.text[:200]}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Error: No se puede conectar al backend")
        except requests.exceptions.Timeout:
            print(f"   ⏰ Error: Timeout al conectar")
        except Exception as e:
            print(f"   💥 Error: {e}")
    
    print(f"\n{'='*50}")
    print("🔍 DIAGNÓSTICO:")
    
    # Test básico de conectividad
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend está funcionando correctamente")
            return True
        else:
            print("⚠️  Backend responde pero con errores")
            return False
    except:
        print("❌ Backend no está accesible")
        return False

def wait_for_backend(base_url="http://localhost:8007", max_wait=120):
    """Espera a que el backend esté disponible"""
    
    print(f"⏳ Esperando que el backend esté disponible ({max_wait}s max)...")
    
    start_time = time.time()
    while time.time() - start_time < max_wait:
        try:
            response = requests.get(f"{base_url}/health", timeout=3)
            if response.status_code == 200:
                elapsed = int(time.time() - start_time)
                print(f"✅ Backend disponible después de {elapsed}s")
                return True
        except:
            pass
        
        print(".", end="", flush=True)
        time.sleep(5)
    
    print(f"\n❌ Backend no estuvo disponible en {max_wait}s")
    return False

def main():
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:8007"
    
    print("🚀 TEST DEL BACKEND CV")
    print(f"🔗 URL Base: {base_url}")
    print("="*50)
    
    # Primero esperar a que esté disponible
    if not wait_for_backend(base_url):
        print("\n💡 SUGERENCIAS:")
        print("1. Verifica que el contenedor esté corriendo: docker ps")
        print("2. Check logs del backend: docker logs cv_backend")
        print("3. Verifica el puerto: debe ser 8007 externamente")
        sys.exit(1)
    
    # Luego hacer test completo
    success = test_backend_health(base_url)
    
    if success:
        print("\n🎉 ¡Backend funcionando perfectamente!")
        print("👉 Puedes acceder al Admin Panel y usar la importación de datos")
    else:
        print("\n⚠️  Backend parcialmente funcional")
        print("👉 Revisa los logs para más detalles")

if __name__ == "__main__":
    main()