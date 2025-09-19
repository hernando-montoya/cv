#!/usr/bin/env python3
"""
Debug completo de autenticación - encontrar la contraseña correcta
"""

import hashlib
import secrets
import os
import requests
import json
from pathlib import Path

def hash_password(password: str) -> str:
    """Hash password with salt"""
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{salt}:{password_hash.hex()}"

def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash"""
    try:
        salt, stored_hash = password_hash.split(':')
        password_hash_check = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return stored_hash == password_hash_check.hex()
    except:
        return False

def test_login_api(username, password, base_url="http://localhost:8001"):
    """Test login via API"""
    try:
        response = requests.post(
            f"{base_url}/api/auth/login",
            json={"username": username, "password": password},
            timeout=5
        )
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.text
    except Exception as e:
        return False, str(e)

def main():
    print("🔍 DEBUG COMPLETO DE AUTENTICACIÓN")
    print("="*60)
    
    # 1. Check current .env
    env_file = Path('/app/backend/.env')
    current_hash = None
    current_username = None
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('ADMIN_USERNAME='):
                    current_username = line.split('=', 1)[1].strip().strip('"')
                elif line.startswith('ADMIN_PASSWORD_HASH='):
                    current_hash = line.split('=', 1)[1].strip().strip('"')
        
        print(f"📁 Current .env:")
        print(f"   Username: {current_username}")
        print(f"   Hash: {current_hash[:50]}...")
    
    # 2. Test common passwords against current hash
    common_passwords = [
        'admin', 'admin2024', 'password', '123456', 'admin123', 
        'root', 'test', 'demo', 'cv', 'hernando'
    ]
    
    print(f"\n🧪 Testing passwords against current hash:")
    found_password = None
    
    for pwd in common_passwords:
        if current_hash and verify_password(pwd, current_hash):
            print(f"   ✅ FOUND: '{pwd}' matches current hash")
            found_password = pwd
            break
        else:
            print(f"   ❌ '{pwd}' - no match")
    
    # 3. Test API with different passwords
    print(f"\n🌐 Testing API login:")
    
    for pwd in common_passwords:
        success, result = test_login_api(current_username or 'admin', pwd)
        if success:
            print(f"   ✅ API SUCCESS: admin/{pwd}")
            found_password = pwd
            break
        else:
            print(f"   ❌ API FAIL: admin/{pwd} - {result[:100]}")
    
    # 4. Create multiple password options
    print(f"\n🔧 Creating multiple password options:")
    
    simple_passwords = ['admin', '123', 'test']
    
    for simple_pwd in simple_passwords:
        new_hash = hash_password(simple_pwd)
        print(f"\n   Password: '{simple_pwd}'")
        print(f"   Hash: {new_hash}")
        
        # Test this hash
        if verify_password(simple_pwd, new_hash):
            print(f"   ✅ Hash verification: OK")
        else:
            print(f"   ❌ Hash verification: FAILED")
    
    # 5. Recommendations
    print(f"\n📋 RECOMMENDATIONS:")
    print(f"="*40)
    
    if found_password:
        print(f"✅ Working password found: '{found_password}'")
        print(f"   Try logging in with: admin/{found_password}")
        
        # Test API one more time
        success, result = test_login_api('admin', found_password)
        if success:
            print(f"✅ API confirms this works!")
            token = result.get('access_token', '')
            print(f"   Token: {token[:50]}...")
        else:
            print(f"❌ API test failed: {result}")
    else:
        print(f"❌ No working password found in common list")
        print(f"🔧 SOLUTION: Reset to simple password")
        
        # Reset to very simple password
        simple_hash = hash_password('123')
        print(f"\n   Use this in .env:")
        print(f"   ADMIN_PASSWORD_HASH=\"{simple_hash}\"")
        print(f"   Then login with: admin/123")

if __name__ == "__main__":
    main()