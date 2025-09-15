import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def init_content_data():
    """Initialize content data in MongoDB"""
    
    # Check if content already exists
    existing_content = await db.content.find_one()
    if existing_content:
        print("Content data already exists, skipping initialization")
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
            },
            {
                "id": "3",
                "title": "Développeur .NET",
                "company": "Betclic",
                "location": "Paris",
                "period": "2011 – 2017",
                "description": {
                    "en": [
                        "Implemented a database archiving system",
                        "Created WCF services and developed trading platform (WPF/WCF)",
                        "Developed web components/functionalities (ASP.NET)",
                        "Built unit tests and performed TMA for BackOffice and FrontOffice",
                        "Integrated various betting offer providers",
                        "Implemented queuing system with RabbitMQ, Mass Transit, and Worker (microservices)"
                    ],
                    "es": [
                        "Implementé un sistema de archivo de base de datos",
                        "Creé servicios WCF y desarrollé plataforma de trading (WPF/WCF)",
                        "Desarrollé componentes/funcionalidades web (ASP.NET)",
                        "Construí pruebas unitarias y realicé TMA para BackOffice y FrontOffice",
                        "Integré varios proveedores de ofertas de apuestas",
                        "Implementé sistema de colas con RabbitMQ, Mass Transit y Worker (microservicios)"
                    ],
                    "fr": [
                        "Implémenté un système d'archivage de base de données",
                        "Créé des services WCF et développé une plateforme de trading (WPF/WCF)",
                        "Développé des composants/fonctionnalités web (ASP.NET)",
                        "Construit des tests unitaires et effectué TMA pour BackOffice et FrontOffice",
                        "Intégré diverses plateformes de fournisseurs d'offres de paris",
                        "Implémenté un système de file d'attente avec RabbitMQ, Mass Transit et Worker (microservices)"
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
                "title": "Angular JS",
                "institution": "SFEIR School",
                "year": "2014",
                "type": "certification"
            },
            {
                "id": "3",
                "title": "Développement WPF",
                "institution": "Microsoft Paris",
                "year": "2011",
                "type": "certification"
            },
            {
                "id": "4",
                "title": "ASP.NET Academy",
                "institution": "Formations SQLI, Paris",
                "year": "2008",
                "type": "certification"
            },
            {
                "id": "5",
                "title": "M2 Technologies d'Internet pour les organisations",
                "institution": "Paris Dauphine",
                "year": "2007",
                "type": "degree"
            },
            {
                "id": "6",
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
            "en": "Experienced Android developer with 13+ years in software development, specializing in modern Android development with Kotlin, Jetpack Compose, and cutting-edge mobile technologies. Passionate about creating innovative solutions that push the boundaries of mobile development.",
            "es": "Desarrollador Android experimentado con más de 13 años en desarrollo de software, especializado en desarrollo Android moderno con Kotlin, Jetpack Compose y tecnologías móviles de vanguardia. Apasionado por crear soluciones innovadoras que expanden los límites del desarrollo móvil.",
            "fr": "Développeur Android expérimenté avec plus de 13 ans en développement logiciel, spécialisé dans le développement Android moderne avec Kotlin, Jetpack Compose et les technologies mobiles de pointe. Passionné par la création de solutions innovantes qui repoussent les limites du développement mobile."
        }
    }
    
    # Insert initial content
    result = await db.content.insert_one(initial_content)
    print(f"Initialized content data with ID: {result.inserted_id}")

async def main():
    """Main initialization function"""
    try:
        await init_content_data()
        print("✅ Database initialization completed successfully")
    except Exception as e:
        print(f"❌ Error during initialization: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())