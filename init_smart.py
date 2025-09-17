#!/usr/bin/env python3
"""
Inicializador inteligente que prueba múltiples formas de conectar a MongoDB
"""

try:
    from pymongo import MongoClient
    import subprocess
    import json
    import socket
    import sys
    
    def get_container_ip():
        """Obtener la IP del contenedor MongoDB"""
        try:
            result = subprocess.run(['docker', 'inspect', 'cv_mongodb'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return data[0]['NetworkSettings']['Networks']['cv_network']['IPAddress']
        except:
            pass
        return None
    
    def test_connection(mongo_url, timeout=3):
        """Probar conexión a MongoDB"""
        try:
            client = MongoClient(mongo_url, serverSelectionTimeoutMS=timeout * 1000)
            client.admin.command('ping')
            client.close()
            return True
        except:
            return False
    
    def init_cv_data(mongo_url):
        """Inicializar datos del CV"""
        print(f"📝 Inicializando datos con: {mongo_url}")
        
        client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
        db = client["cv_database"]
        
        # Verificar si ya existen datos
        if db.content.find_one():
            print("⚠️ Los datos del CV ya existen")
            client.close()
            return
        
        # Datos del CV (versión resumida para inicialización rápida)
        cv_data = {
            "personalInfo": {
                "name": "Hernando Montoya Oliveros",
                "title": "Android Research & Development Engineer", 
                "phone": "06.23.70.58.66",
                "email": "h.montoya2004@gmail.com",
                "website": "hernandomontoya.net",
                "profileImage": "https://customer-assets.emergentagent.com/job_responsive-vita/artifacts/x21fq5wh_profil.png"
            },
            "experiences": [
                {
                    "id": "1",
                    "title": "Développeur Android",
                    "company": "Veepee", 
                    "location": "Full Remote",
                    "period": "2022 – Present",
                    "description": {
                        "en": ["Developed the Veepee/Privalia application for European markets", "Integrated Jetpack Compose and modern Android development"],
                        "es": ["Desarrollé la aplicación Veepee/Privalia para mercados europeos", "Integré Jetpack Compose y desarrollo Android moderno"],
                        "fr": ["Développé l'application Veepee/Privalia pour les marchés européens", "Intégré Jetpack Compose et développement Android moderne"]
                    }
                }
            ],
            "education": [
                {
                    "id": "1",
                    "title": "M2 Technologies d'Internet",
                    "institution": "Paris Dauphine", 
                    "year": "2007",
                    "type": "degree"
                }
            ],
            "skills": {
                "languages": ["Kotlin", "Java"],
                "android": ["Gradle", "Firebase", "Jetpack Compose", "Room", "ViewModels"],
                "tools": ["Android Studio", "Git", "Bitrise"],
                "methodologies": ["MVVM", "Scrum"]
            },
            "languages": [
                {"name": "English", "level": "B2", "proficiency": 75},
                {"name": "Spanish", "level": "Native", "proficiency": 100}, 
                {"name": "French", "level": "Bilingual", "proficiency": 95}
            ],
            "aboutDescription": {
                "en": "Experienced Android developer with 13+ years in software development, specializing in modern Android development with Kotlin and Jetpack Compose.",
                "es": "Desarrollador Android experimentado con más de 13 años en desarrollo de software, especializado en desarrollo Android moderno con Kotlin y Jetpack Compose.",
                "fr": "Développeur Android expérimenté avec plus de 13 ans en développement logiciel, spécialisé dans le développement Android moderne avec Kotlin et Jetpack Compose."
            }
        }
        
        # Insertar datos
        result = db.content.insert_one(cv_data)
        print(f"✅ Datos insertados con ID: {result.inserted_id}")
        client.close()
    
    def main():
        print("🚀 INICIALIZADOR INTELIGENTE CV")
        print("=" * 40)
        
        # Lista de URLs a probar en orden de prioridad
        container_ip = get_container_ip()
        
        urls_to_try = [
            ("localhost:27017", "mongodb://admin:securepassword123@localhost:27017/cv_database?authSource=admin"),
            ("127.0.0.1:27017", "mongodb://admin:securepassword123@127.0.0.1:27017/cv_database?authSource=admin"),
        ]
        
        if container_ip:
            urls_to_try.insert(0, (f"Container IP {container_ip}:27017", 
                                  f"mongodb://admin:securepassword123@{container_ip}:27017/cv_database?authSource=admin"))
        
        # Probar cada URL
        for desc, url in urls_to_try:
            print(f"\n🧪 Probando conexión: {desc}")
            
            if test_connection(url):
                print(f"✅ Conexión exitosa con {desc}")
                try:
                    init_cv_data(url)
                    print("🎉 ¡Inicialización completa! Tu CV está listo.")
                    return
                except Exception as e:
                    print(f"❌ Error durante inicialización: {e}")
                    continue
            else:
                print(f"❌ No se pudo conectar a {desc}")
        
        # Si ninguna URL funcionó
        print("\n💥 No se pudo conectar a MongoDB con ninguna configuración")
        print("\n🔧 SOLUCIONES:")
        print("1. Verifica que el stack esté deployado: docker ps")
        print("2. Usa portainer-fixed.yml que expone el puerto 27017")
        print("3. Ejecuta desde dentro del contenedor:")
        print("   docker exec -it cv_backend python init_data.py")
        print("4. Ejecuta el diagnóstico: python3 diagnose.py")
        
        sys.exit(1)
    
    if __name__ == "__main__":
        main()
        
except ImportError:
    print("❌ PyMongo no está instalado")
    print("🔧 Instala con: pip install pymongo")
    sys.exit(1)