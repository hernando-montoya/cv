#!/usr/bin/env python3
"""
Test rápido de conectividad Backend → MongoDB
"""

import os
import sys
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import socket

async def test_mongodb_connection():
    """Probar conexión MongoDB usando las mismas credenciales del backend"""
    
    # Configuraciones a probar
    test_configs = [
        {
            "name": "Hostname mongodb (Docker)",
            "url": "mongodb://admin:securepassword123@mongodb:27017/cv_database?authSource=admin"
        },
        {
            "name": "Localhost (Host)",  
            "url": "mongodb://admin:securepassword123@localhost:27017/cv_database?authSource=admin"
        },
        {
            "name": "IP 192.168.1.18 (Servidor)",
            "url": "mongodb://admin:securepassword123@192.168.1.18:27017/cv_database?authSource=admin"
        }
    ]
    
    print("🧪 PROBANDO CONEXIONES MONGODB")
    print("=" * 50)
    
    for config in test_configs:
        print(f"\n📍 Testing: {config['name']}")
        print(f"🔗 URL: {config['url']}")
        
        try:
            # Crear cliente
            client = AsyncIOMotorClient(config['url'], serverSelectionTimeoutMS=5000)
            
            # Probar conexión
            await client.admin.command('ping')
            
            # Probar acceso a database
            db = client.cv_database
            collections = await db.list_collection_names()
            
            print(f"✅ CONECTA - Collections: {collections}")
            
            # Cerrar cliente
            client.close()
            
        except Exception as e:
            print(f"❌ FALLA: {e}")

def test_port_access():
    """Probar acceso básico a puertos"""
    print("\n🔌 PROBANDO ACCESO A PUERTOS")
    print("-" * 30)
    
    ports_to_test = [
        ("localhost", 27017, "MongoDB Local"),
        ("192.168.1.18", 27017, "MongoDB Servidor"),
        ("localhost", 8007, "Backend Local"),
        ("192.168.1.18", 8007, "Backend Servidor")
    ]
    
    for host, port, description in ports_to_test:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                print(f"✅ {description} ({host}:{port})")
            else:
                print(f"❌ {description} ({host}:{port})")
                
        except Exception as e:
            print(f"❌ {description} ({host}:{port}) - Error: {e}")

async def main():
    print("🔍 DIAGNÓSTICO BACKEND ↔ MONGODB")
    print("=" * 60)
    
    # Test básico de puertos
    test_port_access()
    
    # Test conexiones MongoDB
    await test_mongodb_connection()
    
    print(f"\n🎯 RESUMEN:")
    print("- Si 'Hostname mongodb' funciona → Stack Docker OK")
    print("- Si solo 'Localhost' funciona → Puerto no expuesto en Portainer")
    print("- Si ninguno funciona → MongoDB no está corriendo")

if __name__ == "__main__":
    asyncio.run(main())