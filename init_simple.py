#!/usr/bin/env python3
"""
Inicializador simple para la base de datos CV
Usa pymongo (síncrono) en lugar de motor (asíncrono)
"""

try:
    from pymongo import MongoClient
    import sys
    
    # Configuración
    MONGO_URL = "mongodb://admin:securepassword123@localhost:27017/cv_database?authSource=admin"
    
    def init_cv_data():
        """Inicializar datos del CV en MongoDB"""
        
        print("🚀 Conectando a MongoDB...")
        
        try:
            # Conectar a MongoDB
            client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
            db = client["cv_database"]
            
            # Test connection
            client.admin.command('ping')
            print("✅ Conexión a MongoDB exitosa")
            
            # Verificar si ya existen datos
            if db.content.find_one():
                print("⚠️ Los datos del CV ya existen, saltando inicialización")
                return
                
            print("📝 Insertando datos del CV...")
            
            # Datos iniciales del CV
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
                            "en": ["Developed the Veepee/Privalia application", "Created new functionalities and integrated Jetpack Compose"],
                            "es": ["Desarrollé la aplicación Veepee/Privalia", "Creé nuevas funcionalidades e integré Jetpack Compose"],
                            "fr": ["Développé l'application Veepee/Privalia", "Créé de nouvelles fonctionnalités et intégré Jetpack Compose"]
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
                    "android": ["Gradle", "Firebase", "Jetpack Compose"],
                    "tools": ["Android Studio", "Git"],
                    "methodologies": ["MVVM", "Scrum"]
                },
                "languages": [
                    {"name": "English", "level": "B2", "proficiency": 75},
                    {"name": "Spanish", "level": "Native", "proficiency": 100},
                    {"name": "French", "level": "Bilingual", "proficiency": 95}
                ],
                "aboutDescription": {
                    "en": "Experienced Android developer with 13+ years in software development.",
                    "es": "Desarrollador Android experimentado con más de 13 años en desarrollo de software.",
                    "fr": "Développeur Android expérimenté avec plus de 13 ans en développement logiciel."
                }
            }
            
            # Insertar datos
            result = db.content.insert_one(cv_data)
            print(f"✅ Datos insertados correctamente con ID: {result.inserted_id}")
            print("🎉 ¡CV inicializado! Tu aplicación está lista para usar.")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("\n🔧 Soluciones:")
            print("1. Verifica que MongoDB esté running: docker ps")
            print("2. Verifica el puerto: docker port cv_mongodb")
            print("3. Espera unos segundos más y reintenta")
            sys.exit(1)
            
        finally:
            if 'client' in locals():
                client.close()
    
    if __name__ == "__main__":
        init_cv_data()
        
except ImportError:
    print("❌ PyMongo no está instalado")
    print("🔧 Instala con: pip install pymongo")
    print("📦 O usa el script init_manual.py con motor/asyncio")