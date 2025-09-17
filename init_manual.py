import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import sys

# Conexión directa usando localhost (desde fuera de Docker)
MONGO_URL = "mongodb://admin:securepassword123@localhost:27017/cv_database?authSource=admin"

# Si no funciona localhost, intentar con la IP del contenedor
# MONGO_URL = "mongodb://admin:securepassword123@172.17.0.1:27017/cv_database?authSource=admin"

async def init_content_data():
    """Initialize content data in MongoDB"""
    
    try:
        client = AsyncIOMotorClient(MONGO_URL, serverSelectionTimeoutMS=5000)
        db = client["cv_database"]
        
        # Test connection
        await client.admin.command('ping')
        print("✅ Conexión a MongoDB exitosa")
        
        # Check if content already exists
        existing_content = await db.content.find_one()
        if existing_content:
            print("⚠️ Los datos ya existen, saltando inicialización")
            return
        
        # Initial content data
        initial_content = {
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
                    "period_es": "2022 – Presente",
                    "period_fr": "2022 – Présent",
                    "description": {
                        "en": [
                            "Developed the Veepee/Privalia application for a group present in several European countries",
                            "Created new functionalities and integrated Jetpack Compose",
                            "Corrected bugs and improved performance",
                            "Created unit and UI tests",
                            "Deployed the app to the Play Store and App Gallery",
                            "Monitored different releases"
                        ],
                        "es": [
                            "Desarrollé la aplicación Veepee/Privalia para un grupo presente en varios países europeos",
                            "Creé nuevas funcionalidades e integré Jetpack Compose",
                            "Corregí errores y mejoré el rendimiento",
                            "Creé pruebas unitarias y de UI",
                            "Desplegué la aplicación en Play Store y App Gallery",
                            "Monitoreé diferentes versiones"
                        ],
                        "fr": [
                            "Développé l'application Veepee/Privalia pour un groupe présent dans plusieurs pays européens",
                            "Créé de nouvelles fonctionnalités et intégré Jetpack Compose",
                            "Corrigé des bugs et amélioré les performances",
                            "Créé des tests unitaires et UI",
                            "Déployé l'application sur le Play Store et App Gallery",
                            "Surveillé différentes versions"
                        ]
                    }
                },
                {
                    "id": "2",
                    "title": "Développeur Android",
                    "company": "Betclic Group",
                    "location": "Bordeaux",
                    "period": "2017 – 2022",
                    "description": {
                        "en": [
                            "Developed the Betclic Sport application for French and Portuguese regulation",
                            "Created new functionalities and migrated Java to Kotlin",
                            "Integrated platforms like AppsFlyer, Emarsys, Google Places, Firebase ML, and CameraX",
                            "Corrected bugs and improved performance",
                            "Created unit and UI tests",
                            "Deployed the app to the Play Store and via FTP"
                        ],
                        "es": [
                            "Desarrollé la aplicación Betclic Sport para la regulación francesa y portuguesa",
                            "Creé nuevas funcionalidades y migré de Java a Kotlin",
                            "Integré plataformas como AppsFlyer, Emarsys, Google Places, Firebase ML y CameraX",
                            "Corregí errores y mejoré el rendimiento",
                            "Creé pruebas unitarias y de UI",
                            "Desplegué la aplicación en Play Store y vía FTP"
                        ],
                        "fr": [
                            "Développé l'application Betclic Sport pour la réglementation française et portugaise",
                            "Créé de nouvelles fonctionnalités et migré de Java vers Kotlin",
                            "Intégré des plateformes comme AppsFlyer, Emarsys, Google Places, Firebase ML et CameraX",
                            "Corrigé des bugs et amélioré les performances",
                            "Créé des tests unitaires et UI",
                            "Déployé l'application sur le Play Store et via FTP"
                        ]
                    }
                }
            ],
            "education": [
                {
                    "id": "1",
                    "title": "Kotlin for Android Developers",
                    "institution": "Antonio Leiva",
                    "year": "2017",
                    "type": "certification"
                },
                {
                    "id": "2",
                    "title": "M2 Technologies d'Internet pour les organisations",
                    "institution": "Paris Dauphine",
                    "year": "2007",
                    "type": "degree"
                },
                {
                    "id": "3",
                    "title": "Ingénieur de Systèmes",
                    "institution": "Université de Cundinamarca, Colombie",
                    "year": "2004",
                    "type": "degree"
                }
            ],
            "skills": {
                "languages": ["Kotlin", "Java"],
                "android": ["Gradle", "Firebase", "Dagger2", "Dagger Hilt", "RxJava", "RxAndroid", "Coroutines", "Navigation", "ViewBinding", "Room", "ViewModels", "Jetpack Compose"],
                "tools": ["Android Studio", "VS Code", "Git", "Bitrise"],
                "methodologies": ["MVVM", "UML", "Scrum"]
            },
            "languages": [
                {"name": "English", "level": "B2", "proficiency": 75},
                {"name": "Spanish", "level": "Native", "proficiency": 100},
                {"name": "French", "level": "Bilingual", "proficiency": 95}
            ],
            "aboutDescription": {
                "en": "Experienced Android developer with 13+ years in software development, specializing in modern Android development with Kotlin, Jetpack Compose, and cutting-edge mobile technologies.",
                "es": "Desarrollador Android experimentado con más de 13 años en desarrollo de software, especializado en desarrollo Android moderno con Kotlin, Jetpack Compose y tecnologías móviles de vanguardia.",
                "fr": "Développeur Android expérimenté avec plus de 13 ans en développement logiciel, spécialisé dans le développement Android moderne avec Kotlin, Jetpack Compose et les technologies mobiles de pointe."
            }
        }
        
        # Insert initial content
        result = await db.content.insert_one(initial_content)
        print(f"✅ Datos inicializados correctamente con ID: {result.inserted_id}")
        
    except Exception as e:
        print(f"❌ Error durante la inicialización: {e}")
        print("\n🔧 Soluciones posibles:")
        print("1. Verifica que MongoDB esté corriendo: docker ps")
        print("2. Verifica el puerto MongoDB: docker port cv_mongodb")
        print("3. Prueba con IP del servidor en lugar de localhost")
        sys.exit(1)
        
    finally:
        client.close()

async def main():
    """Main initialization function"""
    print("🚀 Iniciando configuración de datos del CV...")
    await init_content_data()
    print("✅ ¡Inicialización completa! Tu CV está listo.")

if __name__ == "__main__":
    asyncio.run(main())