from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List
import uuid
from datetime import datetime
from json_storage import storage


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app without a prefix
app = FastAPI(title="CV Backend API", description="Simple CV management system with JSON storage")

# Health check endpoint (sin prefijo para Docker health check)
@app.get("/health")
async def health_check():
    try:
        # Test JSON storage access
        content = storage.load_content()
        storage_status = "connected"
    except:
        storage_status = "error"
    
    return {
        "status": "healthy", 
        "message": "Backend is running",
        "storage": storage_status,
        "timestamp": datetime.utcnow().isoformat()
    }

# Test route
@app.get("/test")
async def test_route():
    return {"message": "Test route works"}

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "CV Backend API - JSON Storage", "version": "2.0"}

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import and include API routes FIRST
from routes.content import router as content_router
from routes.auth import router as auth_router
from routes.import_data import router as import_data_router

app.include_router(content_router)
app.include_router(auth_router)
app.include_router(import_data_router)

# Include the api router
app.include_router(api_router)

# Mount static files and frontend routes LAST
static_dir = Path("/app/frontend_build")
if static_dir.exists():
    logger.info(f"Frontend build directory found at {static_dir}")
    
    # Add special route for admin page
    @app.get("/admin")
    async def serve_admin():
        """Serve admin.html for admin routes"""
        admin_file = static_dir / "admin.html"
        if admin_file.exists():
            return FileResponse(str(admin_file))
        else:
            return {"detail": "Admin page not found"}
    
    # Add root route
    @app.get("/")
    async def serve_index():
        """Serve index.html for root route"""
        index_file = static_dir / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        else:
            return {"detail": "Frontend not built"}
    
    # Serve frontend for all other non-API routes
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve frontend for all routes that don't start with /api or /health"""
        if full_path.startswith("api/") or full_path == "health":
            # Let API routes handle themselves
            return {"detail": "API endpoint"}
        
        # For admin routes, serve admin.html
        if full_path == "admin" or full_path.startswith("admin/"):
            admin_file = static_dir / "admin.html"
            if admin_file.exists():
                return FileResponse(str(admin_file))
        
        # For all other routes, serve index.html (SPA behavior)
        index_file = static_dir / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        else:
            return {"detail": "Frontend not built"}
else:
    logger.warning("Frontend build directory not found at /app/frontend_build")
