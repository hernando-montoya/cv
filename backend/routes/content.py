from fastapi import APIRouter, HTTPException
from models.content import ContentData, ContentUpdate
from json_storage import storage
from typing import Optional
import uuid

router = APIRouter(prefix="/api/content", tags=["content"])

@router.get("/", response_model=ContentData)
async def get_content():
    """Get current content data"""
    try:
        content_data = storage.load_content()
        return ContentData(**content_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching content: {str(e)}")

@router.put("/", response_model=ContentData)
async def update_content(content_update: ContentUpdate):
    """Update content data"""
    try:
        # Prepare updates dict
        updates = {}
        
        if content_update.personalInfo:
            updates['personalInfo'] = content_update.personalInfo.dict()
        if content_update.experiences is not None:
            updates['experiences'] = [exp.dict() for exp in content_update.experiences]
        if content_update.education is not None:
            updates['education'] = [edu.dict() for edu in content_update.education]
        if content_update.skills:
            updates['skills'] = content_update.skills
        if content_update.languages is not None:
            updates['languages'] = [lang.dict() for lang in content_update.languages]
        if content_update.aboutDescription:
            updates['aboutDescription'] = content_update.aboutDescription
        
        # Update content
        updated_content = storage.update_content(updates)
        
        return ContentData(**updated_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating content: {str(e)}")

@router.post("/experience", response_model=dict)
async def add_experience(experience: dict):
    """Add new experience item"""
    try:
        # Ensure ID exists
        if "id" not in experience:
            experience["id"] = str(uuid.uuid4())
        
        current_content = storage.load_content()
        current_content["experiences"].append(experience)
        
        storage.update_content({"experiences": current_content["experiences"]})
        
        return {"message": "Experience added successfully", "id": experience["id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding experience: {str(e)}")

@router.post("/education", response_model=dict)
async def add_education(education: dict):
    """Add new education item"""
    try:
        # Ensure ID exists
        if "id" not in education:
            education["id"] = str(uuid.uuid4())
        
        current_content = storage.load_content()
        current_content["education"].append(education)
        
        storage.update_content({"education": current_content["education"]})
        
        return {"message": "Education added successfully", "id": education["id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding education: {str(e)}")

@router.delete("/experience/{experience_id}")
async def delete_experience(experience_id: str):
    """Delete experience item"""
    try:
        current_content = storage.load_content()
        current_content["experiences"] = [
            exp for exp in current_content["experiences"] 
            if exp.get("id") != experience_id
        ]
        
        storage.update_content({"experiences": current_content["experiences"]})
        
        return {"message": "Experience deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting experience: {str(e)}")

@router.delete("/education/{education_id}")
async def delete_education(education_id: str):
    """Delete education item"""
    try:
        current_content = storage.load_content()
        current_content["education"] = [
            edu for edu in current_content["education"] 
            if edu.get("id") != education_id
        ]
        
        storage.update_content({"education": current_content["education"]})
        
        return {"message": "Education deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting education: {str(e)}")