#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for CV Application
Tests all critical endpoints and functionality
"""

import requests
import json
import os
import sys
from datetime import datetime
import tempfile
import time

# Configuration
BACKEND_URL = "http://localhost:8001"  # Use internal URL since external routing has issues
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin2024"

class CVBackendTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.token = None
        self.test_results = []
        self.session = requests.Session()
        
    def log_test(self, test_name, success, message, details=None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if details and not success:
            print(f"   Details: {details}")
    
    def test_health_check(self):
        """Test health check endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                expected_fields = ["status", "message", "storage"]
                
                if all(field in data for field in expected_fields):
                    if data["status"] == "healthy" and data["storage"] in ["connected", "error"]:
                        self.log_test("Health Check", True, f"Health check passed - Storage: {data['storage']}")
                        return True
                    else:
                        self.log_test("Health Check", False, "Invalid health check response format", data)
                else:
                    self.log_test("Health Check", False, "Missing required fields in health response", data)
            else:
                self.log_test("Health Check", False, f"HTTP {response.status_code}", {"response": response.text})
                
        except Exception as e:
            self.log_test("Health Check", False, f"Request failed: {str(e)}")
        
        return False
    
    def test_authentication(self):
        """Test authentication system"""
        try:
            # Test login
            login_data = {
                "username": ADMIN_USERNAME,
                "password": ADMIN_PASSWORD
            }
            
            response = self.session.post(
                f"{self.base_url}/api/auth/login",
                json=login_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data and "token_type" in data:
                    self.token = data["access_token"]
                    self.log_test("Authentication Login", True, "Login successful")
                    
                    # Test token verification
                    headers = {"Authorization": f"Bearer {self.token}"}
                    verify_response = self.session.post(
                        f"{self.base_url}/api/auth/verify",
                        headers=headers,
                        timeout=10
                    )
                    
                    if verify_response.status_code == 200:
                        verify_data = verify_response.json()
                        if verify_data.get("valid") and verify_data.get("username") == ADMIN_USERNAME:
                            self.log_test("Authentication Verify", True, "Token verification successful")
                            return True
                        else:
                            self.log_test("Authentication Verify", False, "Invalid token verification response", verify_data)
                    else:
                        self.log_test("Authentication Verify", False, f"Token verification failed: HTTP {verify_response.status_code}")
                else:
                    self.log_test("Authentication Login", False, "Missing token in login response", data)
            else:
                self.log_test("Authentication Login", False, f"Login failed: HTTP {response.status_code}", {"response": response.text})
                
        except Exception as e:
            self.log_test("Authentication", False, f"Authentication test failed: {str(e)}")
        
        return False
    
    def test_content_api(self):
        """Test content API endpoints"""
        try:
            # Test GET content
            response = self.session.get(f"{self.base_url}/api/content/", timeout=10)
            
            if response.status_code == 200:
                content_data = response.json()
                required_fields = ["personalInfo", "experiences", "education", "skills", "languages", "aboutDescription"]
                
                if all(field in content_data for field in required_fields):
                    self.log_test("Content API GET", True, "Content retrieval successful")
                    
                    # Test PUT content (requires authentication)
                    if self.token:
                        headers = {"Authorization": f"Bearer {self.token}"}
                        
                        # Create a simple update
                        update_data = {
                            "personalInfo": {
                                "name": "Test Update Name",
                                "title": content_data["personalInfo"]["title"],
                                "phone": content_data["personalInfo"]["phone"],
                                "email": content_data["personalInfo"]["email"],
                                "website": content_data["personalInfo"]["website"],
                                "profileImage": content_data["personalInfo"]["profileImage"]
                            }
                        }
                        
                        put_response = self.session.put(
                            f"{self.base_url}/api/content/",
                            json=update_data,
                            headers=headers,
                            timeout=10
                        )
                        
                        if put_response.status_code == 200:
                            updated_data = put_response.json()
                            if updated_data["personalInfo"]["name"] == "Test Update Name":
                                self.log_test("Content API PUT", True, "Content update successful")
                                
                                # Restore original name
                                restore_data = {
                                    "personalInfo": content_data["personalInfo"]
                                }
                                self.session.put(
                                    f"{self.base_url}/api/content/",
                                    json=restore_data,
                                    headers=headers,
                                    timeout=10
                                )
                                return True
                            else:
                                self.log_test("Content API PUT", False, "Content update did not persist", updated_data)
                        else:
                            self.log_test("Content API PUT", False, f"Content update failed: HTTP {put_response.status_code}")
                    else:
                        self.log_test("Content API PUT", False, "No authentication token available for PUT test")
                else:
                    self.log_test("Content API GET", False, "Missing required fields in content", {"missing": [f for f in required_fields if f not in content_data]})
            else:
                self.log_test("Content API GET", False, f"Content retrieval failed: HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Content API", False, f"Content API test failed: {str(e)}")
        
        return False
    
    def test_import_export_system(self):
        """Test import/export system"""
        if not self.token:
            self.log_test("Import/Export System", False, "No authentication token available")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            
            # Test export
            export_response = self.session.get(
                f"{self.base_url}/api/import/export",
                headers=headers,
                timeout=10
            )
            
            if export_response.status_code == 200:
                export_data = export_response.json()
                if "success" in export_data and export_data["success"] and "data" in export_data:
                    self.log_test("Export System", True, "Export successful")
                    
                    # Test import with the exported data
                    test_data = export_data["data"].copy()
                    test_data["personalInfo"]["name"] = "Import Test Name"
                    
                    # Create a temporary JSON file
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                        json.dump(test_data, temp_file, indent=2)
                        temp_file_path = temp_file.name
                    
                    try:
                        # Test import
                        with open(temp_file_path, 'rb') as f:
                            files = {'file': ('test_import.json', f, 'application/json')}
                            import_response = self.session.post(
                                f"{self.base_url}/api/import/cv-data",
                                files=files,
                                headers=headers,
                                timeout=10
                            )
                        
                        if import_response.status_code == 200:
                            import_data = import_response.json()
                            if import_data.get("success"):
                                self.log_test("Import System", True, "Import successful")
                                
                                # Verify the import worked by checking content
                                verify_response = self.session.get(f"{self.base_url}/api/content/", timeout=10)
                                if verify_response.status_code == 200:
                                    verify_data = verify_response.json()
                                    if verify_data["personalInfo"]["name"] == "Import Test Name":
                                        self.log_test("Import Verification", True, "Import data verified successfully")
                                        
                                        # Restore original data
                                        original_data = export_data["data"]
                                        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as restore_file:
                                            json.dump(original_data, restore_file, indent=2)
                                            restore_file_path = restore_file.name
                                        
                                        with open(restore_file_path, 'rb') as f:
                                            files = {'file': ('restore.json', f, 'application/json')}
                                            self.session.post(
                                                f"{self.base_url}/api/import/cv-data",
                                                files=files,
                                                headers=headers,
                                                timeout=10
                                            )
                                        
                                        os.unlink(restore_file_path)
                                        return True
                                    else:
                                        self.log_test("Import Verification", False, "Import data not found in content")
                                else:
                                    self.log_test("Import Verification", False, "Could not verify import")
                            else:
                                self.log_test("Import System", False, "Import response indicates failure", import_data)
                        else:
                            self.log_test("Import System", False, f"Import failed: HTTP {import_response.status_code}")
                    
                    finally:
                        # Clean up temp file
                        if os.path.exists(temp_file_path):
                            os.unlink(temp_file_path)
                else:
                    self.log_test("Export System", False, "Invalid export response format", export_data)
            else:
                self.log_test("Export System", False, f"Export failed: HTTP {export_response.status_code}")
                
        except Exception as e:
            self.log_test("Import/Export System", False, f"Import/Export test failed: {str(e)}")
        
        return False
    
    def test_static_file_serving(self):
        """Test static file serving"""
        try:
            # Test root route
            root_response = self.session.get(f"{self.base_url}/", timeout=10)
            if root_response.status_code == 200:
                if "html" in root_response.headers.get("content-type", "").lower():
                    self.log_test("Static Files Root", True, "Root route serves HTML content")
                else:
                    self.log_test("Static Files Root", False, f"Root route content-type: {root_response.headers.get('content-type')}")
            else:
                self.log_test("Static Files Root", False, f"Root route failed: HTTP {root_response.status_code}")
            
            # Test admin route
            admin_response = self.session.get(f"{self.base_url}/admin", timeout=10)
            if admin_response.status_code == 200:
                if "html" in admin_response.headers.get("content-type", "").lower():
                    self.log_test("Static Files Admin", True, "Admin route serves HTML content")
                else:
                    self.log_test("Static Files Admin", False, f"Admin route content-type: {admin_response.headers.get('content-type')}")
            else:
                self.log_test("Static Files Admin", False, f"Admin route failed: HTTP {admin_response.status_code}")
            
            # Test fallback route
            fallback_response = self.session.get(f"{self.base_url}/some-random-route", timeout=10)
            if fallback_response.status_code == 200:
                if "html" in fallback_response.headers.get("content-type", "").lower():
                    self.log_test("Static Files Fallback", True, "Fallback route serves HTML content")
                    return True
                else:
                    self.log_test("Static Files Fallback", False, f"Fallback route content-type: {fallback_response.headers.get('content-type')}")
            else:
                self.log_test("Static Files Fallback", False, f"Fallback route failed: HTTP {fallback_response.status_code}")
                
        except Exception as e:
            self.log_test("Static File Serving", False, f"Static file test failed: {str(e)}")
        
        return False
    
    def test_cors_headers(self):
        """Test CORS headers"""
        try:
            # Test preflight request
            headers = {
                "Origin": "https://example.com",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type,Authorization"
            }
            
            response = self.session.options(f"{self.base_url}/api/content/", headers=headers, timeout=10)
            
            cors_headers = {
                "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin"),
                "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods"),
                "Access-Control-Allow-Headers": response.headers.get("Access-Control-Allow-Headers")
            }
            
            if any(cors_headers.values()):
                self.log_test("CORS Headers", True, "CORS headers present", cors_headers)
                return True
            else:
                self.log_test("CORS Headers", False, "No CORS headers found", {"response_headers": dict(response.headers)})
                
        except Exception as e:
            self.log_test("CORS Headers", False, f"CORS test failed: {str(e)}")
        
        return False
    
    def test_protected_routes(self):
        """Test that protected routes require authentication"""
        try:
            # Test import export without token (should be protected)
            export_response = self.session.get(f"{self.base_url}/api/import/export", timeout=10)
            
            if export_response.status_code in [401, 403]:
                self.log_test("Protected Routes", True, "Export route properly requires authentication")
                
                # Test import status without token (should be unprotected)
                status_response = self.session.get(f"{self.base_url}/api/import/status", timeout=10)
                if status_response.status_code == 200:
                    self.log_test("Public Routes", True, "Status route is properly public")
                    return True
                else:
                    self.log_test("Public Routes", False, f"Status route should be public: HTTP {status_response.status_code}")
            else:
                self.log_test("Protected Routes", False, f"Export route should require auth: HTTP {export_response.status_code}")
                
        except Exception as e:
            self.log_test("Protected Routes", False, f"Protected routes test failed: {str(e)}")
        
        return False
    
    def run_all_tests(self):
        """Run all tests"""
        print(f"\n🚀 Starting CV Backend API Tests")
        print(f"Backend URL: {self.base_url}")
        print(f"Test Time: {datetime.now().isoformat()}")
        print("=" * 60)
        
        # Run tests in order
        tests = [
            ("Health Check", self.test_health_check),
            ("Authentication", self.test_authentication),
            ("Content API", self.test_content_api),
            ("Import/Export System", self.test_import_export_system),
            ("Static File Serving", self.test_static_file_serving),
            ("CORS Headers", self.test_cors_headers),
            ("Protected Routes", self.test_protected_routes)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n📋 Running {test_name}...")
            if test_func():
                passed += 1
        
        # Summary
        print("\n" + "=" * 60)
        print(f"🏁 TEST SUMMARY")
        print(f"Passed: {passed}/{total}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED!")
        else:
            print("⚠️  Some tests failed. Check details above.")
        
        # Detailed results
        print(f"\n📊 DETAILED RESULTS:")
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test']}: {result['message']}")
        
        return passed == total

def main():
    """Main test runner"""
    print("CV Backend API Comprehensive Test Suite")
    print("=" * 50)
    
    tester = CVBackendTester()
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()