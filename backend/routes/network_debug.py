from fastapi import APIRouter
import socket
import subprocess
import os

router = APIRouter(prefix="/api/network", tags=["Network Debug"])

@router.get("/debug")
async def network_debug():
    """Debug network connectivity"""
    
    debug_info = {
        "hostname_resolution": {},
        "network_info": {},
        "mongo_connection_tests": {}
    }
    
    # Test 1: Hostname resolution
    hostnames_to_test = ["mongodb", "cv_mongodb", "localhost"]
    for hostname in hostnames_to_test:
        try:
            ip_address = socket.gethostbyname(hostname)
            debug_info["hostname_resolution"][hostname] = {
                "status": "ok",
                "ip": ip_address
            }
        except Exception as e:
            debug_info["hostname_resolution"][hostname] = {
                "status": "error",
                "message": str(e)
            }
    
    # Test 2: Network information
    try:
        # Get container hostname
        container_hostname = socket.gethostname()
        debug_info["network_info"]["container_hostname"] = container_hostname
        
        # Get environment variables
        mongo_url = os.environ.get('MONGO_URL', 'Not set')
        debug_info["network_info"]["mongo_url"] = mongo_url
        
    except Exception as e:
        debug_info["network_info"]["error"] = str(e)
    
    # Test 3: MongoDB connection attempts
    mongo_urls_to_test = [
        "mongodb://admin:securepassword123@mongodb:27017/cv_database?authSource=admin",
        "mongodb://admin:securepassword123@cv_mongodb:27017/cv_database?authSource=admin",
        "mongodb://admin:securepassword123@localhost:27017/cv_database?authSource=admin"
    ]
    
    for mongo_url in mongo_urls_to_test:
        try:
            from motor.motor_asyncio import AsyncIOMotorClient
            test_client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=5000)
            
            # Try to ping
            result = await test_client.admin.command('ping')
            debug_info["mongo_connection_tests"][mongo_url] = {
                "status": "ok",
                "ping_result": result
            }
            test_client.close()
            
        except Exception as e:
            debug_info["mongo_connection_tests"][mongo_url] = {
                "status": "error", 
                "message": str(e)
            }
    
    return debug_info