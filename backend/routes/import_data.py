from fastapi import APIRouter, HTTPException, File, UploadFile, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from motor.motor_asyncio import AsyncIOMotorClient
import json
import os
from typing import Dict, Any
import jwt
from datetime import datetime

router = APIRouter(prefix="/api/import", tags=["Data Import"])

# MongoDB connection
from server import db

# JWT verification
security = HTTPBearer()

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token for admin access"""
    try:
        payload = jwt.decode(
            credentials.credentials, 
            os.environ.get("JWT_SECRET", "fallback_secret"), 
            algorithms=["HS256"]
        )
        if payload.get("username") != os.environ.get("ADMIN_USERNAME", "admin"):
            raise HTTPException(status_code=403, detail="Access denied")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/cv-data")
async def import_cv_data(
    file: UploadFile = File(...),
    current_user: dict = Depends(verify_jwt_token)
):
    """Import CV data from JSON file"""
    
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"Starting import for file: {file.filename}")
    logger.info(f"File content type: {file.content_type}")
    logger.info(f"User: {current_user.get('username', 'unknown')}")
    
    # Validate file type
    if not file.filename.endswith('.json'):
        logger.error(f"Invalid file type: {file.filename}")
        raise HTTPException(status_code=400, detail="Only JSON files are allowed")
    
    try:
        # Read and parse JSON file
        logger.info("Reading file contents...")
        contents = await file.read()
        logger.info(f"File size: {len(contents)} bytes")
        
        logger.info("Parsing JSON...")
        cv_data = json.loads(contents.decode('utf-8'))
        logger.info(f"JSON parsed successfully. Keys: {list(cv_data.keys())}")
        
        # Validate required fields
        required_fields = ["personalInfo", "experiences", "education", "skills", "languages", "aboutDescription"]
        missing_fields = [field for field in required_fields if field not in cv_data]
        
        if missing_fields:
            logger.error(f"Missing required fields: {missing_fields}")
            raise HTTPException(
                status_code=400, 
                detail=f"Missing required fields: {', '.join(missing_fields)}"
            )
        
        logger.info("Checking existing content in database...")
        # Check if data already exists
        existing_content = await db.content.find_one()
        
        if existing_content:
            logger.info("Updating existing content...")
            # Update existing data
            result = await db.content.replace_one(
                {"_id": existing_content["_id"]}, 
                cv_data
            )
            action = "updated"
            logger.info(f"Content updated. Matched: {result.matched_count}, Modified: {result.modified_count}")
        else:
            logger.info("Inserting new content...")
            # Insert new data
            result = await db.content.insert_one(cv_data)
            action = "created"
            logger.info(f"Content created with ID: {result.inserted_id}")
        
        response_data = {
            "success": True,
            "message": f"CV data {action} successfully",
            "filename": file.filename,
            "timestamp": datetime.utcnow().isoformat(),
            "records_count": {
                "experiences": len(cv_data.get("experiences", [])),
                "education": len(cv_data.get("education", [])),
                "skills_categories": len(cv_data.get("skills", {})),
                "languages": len(cv_data.get("languages", []))
            }
        }
        
        logger.info(f"Import successful: {response_data}")
        return response_data
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid JSON format: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during import: {e}")
        logger.exception("Full traceback:")
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")

@router.post("/quick-init")
async def quick_initialize_default_data(
    current_user: dict = Depends(verify_jwt_token)
):
    """Quick initialize with default CV data (no file upload needed)"""
    
    # Check if data already exists
    existing_content = await db.content.find_one()
    if existing_content:
        raise HTTPException(status_code=400, detail="CV data already exists. Use import to replace.")
    
    # Default CV data
    default_cv_data = {
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
                    "en": [
                        "Developed the Veepee/Privalia application for a group present in several European countries",
                        "Created new functionalities and integrated Jetpack Compose",
                        "Corrected bugs and improved performance"
                    ],
                    "es": [
                        "Desarrollé la aplicación Veepee/Privalia para un grupo presente en varios países europeos",
                        "Creé nuevas funcionalidades e integré Jetpack Compose",
                        "Corregí errores y mejoré el rendimiento"
                    ],
                    "fr": [
                        "Développé l'application Veepee/Privalia pour un groupe présent dans plusieurs pays européens",
                        "Créé de nouvelles fonctionnalités et intégré Jetpack Compose",
                        "Corrigé des bugs et amélioré les performances"
                    ]
                }
            }
        ],
        "education": [
            {
                "id": "1",
                "title": "M2 Technologies d'Internet pour les organisations",
                "institution": "Paris Dauphine",
                "year": "2007",
                "type": "degree"
            },
            {
                "id": "2",
                "title": "Ingénieur de Systèmes",
                "institution": "Université de Cundinamarca, Colombie",
                "year": "2004",
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
            "en": "Experienced Android developer with 13+ years in software development, specializing in modern Android development with Kotlin, Jetpack Compose, and cutting-edge mobile technologies.",
            "es": "Desarrollador Android experimentado con más de 13 años en desarrollo de software, especializado en desarrollo Android moderno con Kotlin, Jetpack Compose y tecnologías móviles de vanguardia.",
            "fr": "Développeur Android expérimenté avec plus de 13 ans en développement logiciel, spécialisé dans le développement Android moderne avec Kotlin, Jetpack Compose et les technologies mobiles de pointe."
        }
    }
    
    try:
        result = await db.content.insert_one(default_cv_data)
        return {
            "success": True,
            "message": "Default CV data initialized successfully",
            "timestamp": datetime.utcnow().isoformat(),
            "records_count": {
                "experiences": len(default_cv_data["experiences"]),
                "education": len(default_cv_data["education"]),
                "skills_categories": len(default_cv_data["skills"]),
                "languages": len(default_cv_data["languages"])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Initialization failed: {str(e)}")

@router.get("/export")
async def export_cv_data(
    current_user: dict = Depends(verify_jwt_token)
):
    """Export current CV data as JSON"""
    
    try:
        content = await db.content.find_one()
        if not content:
            raise HTTPException(status_code=404, detail="No CV data found to export")
        
        # Remove MongoDB _id field for clean export
        if "_id" in content:
            del content["_id"]
        
        return {
            "success": True,
            "data": content,
            "exported_at": datetime.utcnow().isoformat(),
            "records_count": {
                "experiences": len(content.get("experiences", [])),
                "education": len(content.get("education", [])),
                "skills_categories": len(content.get("skills", {})),
                "languages": len(content.get("languages", []))
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

@router.delete("/cv-data")
async def clear_cv_data(
    current_user: dict = Depends(verify_jwt_token)
):
    """Clear all CV data"""
    
    try:
        result = await db.content.delete_many({})
        return {
            "success": True,
            "message": f"Deleted {result.deleted_count} CV records",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Clear operation failed: {str(e)}")

@router.get("/status")
async def get_import_status():
    """Get the current status of CV data"""
    
    try:
        content = await db.content.find_one()
        
        if not content:
            return {
                "initialized": False,
                "message": "No CV data found. Use quick-init or import a JSON file."
            }
        
        return {
            "initialized": True,
            "message": "CV data is available",
            "last_updated": content.get("last_updated", "Unknown"),
            "records_count": {
                "experiences": len(content.get("experiences", [])),
                "education": len(content.get("education", [])),
                "skills_categories": len(content.get("skills", {})),
                "languages": len(content.get("languages", []))
            }
        }
        
    except Exception as e:
        return {
            "initialized": False,
            "error": str(e)
        }