from fastapi import APIRouter, HTTPException, File, UploadFile, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import json
import os
from typing import Dict, Any
import jwt
from datetime import datetime
from json_storage import storage

router = APIRouter(prefix="/api/import", tags=["Data Import"])

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

@router.get("/debug")
async def debug_import_system():
    """Debug endpoint to test system components"""
    import logging
    logger = logging.getLogger(__name__)
    
    debug_info = {
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {}
    }
    
    # Test 1: Basic Python imports
    try:
        import json
        import os
        import jwt
        debug_info["checks"]["imports"] = {"status": "ok", "message": "All imports successful"}
    except Exception as e:
        debug_info["checks"]["imports"] = {"status": "error", "message": str(e)}
    
    # Test 2: Environment variables
    try:
        jwt_secret = os.environ.get('JWT_SECRET')
        admin_user = os.environ.get('ADMIN_USERNAME')
        
        debug_info["checks"]["environment"] = {
            "status": "ok",
            "jwt_secret_exists": bool(jwt_secret),
            "admin_user": admin_user,
            "storage_type": "JSON file system"
        }
    except Exception as e:
        debug_info["checks"]["environment"] = {"status": "error", "message": str(e)}
    
    # Test 3: JSON Storage access
    try:
        content = storage.load_content()
        debug_info["checks"]["storage"] = {
            "status": "ok", 
            "content_loaded": bool(content),
            "storage_path": str(storage.content_file)
        }
    except Exception as e:
        debug_info["checks"]["storage"] = {"status": "error", "message": str(e)}
    
    # Test 4: Data structure validation
    try:
        content = storage.load_content()
        required_fields = ["personalInfo", "experiences", "education", "skills", "languages", "aboutDescription"]
        missing_fields = [field for field in required_fields if field not in content]
        
        debug_info["checks"]["data_structure"] = {
            "status": "ok" if not missing_fields else "warning",
            "missing_fields": missing_fields,
            "records_count": {
                "experiences": len(content.get("experiences", [])),
                "education": len(content.get("education", [])),
                "skills_categories": len(content.get("skills", {})),
                "languages": len(content.get("languages", []))
            }
        }
    except Exception as e:
        debug_info["checks"]["data_structure"] = {"status": "error", "message": str(e)}
    
    return debug_info

@router.post("/test-auth")
async def test_auth_system(current_user: dict = Depends(verify_jwt_token)):
    """Test JWT authentication system"""
    return {
        "status": "ok",
        "message": "Authentication successful",
        "user": current_user,
        "timestamp": datetime.utcnow().isoformat()
    }

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
        
        # Import using JSON storage
        logger.info("Importing data to JSON storage...")
        storage.import_content(cv_data)
        logger.info("Import successful!")
        
        response_data = {
            "success": True,
            "message": "CV data imported successfully",
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
    except ValueError as e:
        logger.error(f"Data validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during import: {e}")
        logger.exception("Full traceback:")
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")

@router.post("/quick-init")
async def quick_initialize_default_data(
    current_user: dict = Depends(verify_jwt_token)
):
    """Quick initialize with default CV data (no file upload needed)"""
    
    try:
        # Check if data already exists
        current_content = storage.load_content()
        if current_content.get("experiences") or current_content.get("education"):
            raise HTTPException(status_code=400, detail="CV data already exists. Use import to replace.")
        
        # Force creation of default content
        storage._create_default_content()
        content = storage.load_content()
        
        return {
            "success": True,
            "message": "Default CV data initialized successfully",
            "timestamp": datetime.utcnow().isoformat(),
            "records_count": {
                "experiences": len(content.get("experiences", [])),
                "education": len(content.get("education", [])),
                "skills_categories": len(content.get("skills", {})),
                "languages": len(content.get("languages", []))
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Initialization failed: {str(e)}")

@router.get("/export")
async def export_cv_data(
    current_user: dict = Depends(verify_jwt_token)
):
    """Export current CV data as JSON"""
    
    try:
        content = storage.export_content()
        
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
    """Clear all CV data and reset to default"""
    
    try:
        # Delete current data file
        if storage.content_file.exists():
            storage.content_file.unlink()
        
        # Create fresh default content
        storage._create_default_content()
        
        return {
            "success": True,
            "message": "CV data cleared and reset to default",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Clear operation failed: {str(e)}")

@router.get("/status")
async def get_import_status():
    """Get the current status of CV data"""
    
    try:
        content = storage.load_content()
        
        return {
            "initialized": True,
            "message": "CV data is available",
            "storage_type": "JSON file system",
            "last_updated": content.get("updated_at", "Unknown"),
            "data_file": str(storage.content_file),
            "backups_available": len(storage.get_backups()),
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

@router.get("/backups")
async def list_backups(
    current_user: dict = Depends(verify_jwt_token)
):
    """List available backups"""
    
    try:
        backups = storage.get_backups()
        return {
            "success": True,
            "backups": backups,
            "backup_dir": str(storage.backup_dir)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list backups: {str(e)}")

@router.post("/restore/{backup_name}")
async def restore_backup(
    backup_name: str,
    current_user: dict = Depends(verify_jwt_token)
):
    """Restore from backup"""
    
    try:
        content = storage.restore_backup(backup_name)
        return {
            "success": True,
            "message": f"Successfully restored from backup: {backup_name}",
            "timestamp": datetime.utcnow().isoformat(),
            "records_count": {
                "experiences": len(content.get("experiences", [])),
                "education": len(content.get("education", [])),
                "skills_categories": len(content.get("skills", {})),
                "languages": len(content.get("languages", []))
            }
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Backup not found: {backup_name}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Restore failed: {str(e)}")