from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from models.content import ContentData, ContentUpdate
import os
from typing import Optional

router = APIRouter(prefix="/api/content", tags=["content"])

# MongoDB connection
from server import db

@router.get("/", response_model=ContentData)
async def get_content():
    """Get current content data"""
    try:
        content = await db.content.find_one({}, sort=[("updated_at", -1)])
        if not content:
            # Return default content if none exists
            default_content = {
                "personalInfo": {
                    "name": "Hernando Montoya Oliveros",
                    "title": "Android Research & Development Engineer",
                    "phone": "06.23.70.58.66",
                    "email": "h.montoya2004@gmail.com",
                    "website": "hernandomontoya.net",
                    "profileImage": "https://customer-assets.emergentagent.com/job_responsive-vita/artifacts/x21fq5wh_profil.png"
                },
                "experiences": [],
                "education": [],
                "skills": {
                    "languages": ["Kotlin", "Java"],
                    "android": ["Gradle", "Firebase", "Dagger2", "Dagger Hilt", "RxJava", "Coroutines", "Jetpack Compose"],
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
            return ContentData(**default_content)
        
        # Remove MongoDB _id field
        content.pop('_id', None)
        return ContentData(**content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching content: {str(e)}")

@router.put("/", response_model=ContentData)
async def update_content(content_update: ContentUpdate):
    """Update content data"""
    try:
        # Get current content
        current_content = await db.content.find_one({}, sort=[("updated_at", -1)])
        
        if current_content:
            current_content.pop('_id', None)
            current_data = ContentData(**current_content)
        else:
            # Create default if none exists
            current_data = await get_content()
        
        # Update only provided fields
        update_data = current_data.dict()
        
        if content_update.personalInfo:
            update_data['personalInfo'] = content_update.personalInfo.dict()
        if content_update.experiences is not None:
            update_data['experiences'] = [exp.dict() for exp in content_update.experiences]
        if content_update.education is not None:
            update_data['education'] = [edu.dict() for edu in content_update.education]
        if content_update.skills:
            update_data['skills'] = content_update.skills
        if content_update.languages is not None:
            update_data['languages'] = [lang.dict() for lang in content_update.languages]
        if content_update.aboutDescription:
            update_data['aboutDescription'] = content_update.aboutDescription
        
        # Create new content entry
        new_content = ContentData(**update_data)
        
        # Save to database
        await db.content.insert_one(new_content.dict())
        
        return new_content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating content: {str(e)}")

@router.post("/experience", response_model=dict)
async def add_experience(experience: dict):
    """Add new experience item"""
    try:
        current_content = await get_content()
        current_content.experiences.append(experience)
        
        update_request = ContentUpdate(experiences=current_content.experiences)
        updated_content = await update_content(update_request)
        
        return {"message": "Experience added successfully", "id": experience.get("id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding experience: {str(e)}")

@router.post("/education", response_model=dict)
async def add_education(education: dict):
    """Add new education item"""
    try:
        current_content = await get_content()
        current_content.education.append(education)
        
        update_request = ContentUpdate(education=current_content.education)
        updated_content = await update_content(update_request)
        
        return {"message": "Education added successfully", "id": education.get("id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding education: {str(e)}")

@router.delete("/experience/{experience_id}")
async def delete_experience(experience_id: str):
    """Delete experience item"""
    try:
        current_content = await get_content()
        current_content.experiences = [exp for exp in current_content.experiences if exp.id != experience_id]
        
        update_request = ContentUpdate(experiences=current_content.experiences)
        await update_content(update_request)
        
        return {"message": "Experience deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting experience: {str(e)}")

@router.delete("/education/{education_id}")
async def delete_education(education_id: str):
    """Delete education item"""
    try:
        current_content = await get_content()
        current_content.education = [edu for edu in current_content.education if edu.id != education_id]
        
        update_request = ContentUpdate(education=current_content.education)
        await update_content(update_request)
        
        return {"message": "Education deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting education: {str(e)}")