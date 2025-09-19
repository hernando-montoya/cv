#!/usr/bin/env python3
"""
Script para verificar y generar contraseñas admin
"""

import hashlib
import secrets
import os
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

def check_current_env():
    """Check current .env password"""
    env_file = Path('/app/backend/.env')
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
            for line in content.split('\n'):
                if line.startswith('ADMIN_PASSWORD_HASH='):
                    hash_value = line.split('=', 1)[1].strip('"')
                    print(f"Current hash: {hash_value}")
                    
                    # Test common passwords
                    common_passwords = ['admin', 'admin2024', 'password', '123456', 'admin123']
                    
                    print("\nTesting common passwords:")
                    for pwd in common_passwords:
                        if verify_password(pwd, hash_value):
                            print(f"✅ FOUND: Password is '{pwd}'")
                            return pwd
                        else:
                            print(f"❌ Not: {pwd}")
                    
                    print(f"\n❌ Current hash doesn't match any common password")
                    return None
    return None

def generate_new_password():
    """Generate new admin2024 hash"""
    new_hash = hash_password('admin2024')
    print(f"\nNew hash for 'admin2024': {new_hash}")
    return new_hash

if __name__ == "__main__":
    print("🔍 CHECKING ADMIN PASSWORD")
    print("="*50)
    
    current_pwd = check_current_env()
    
    if not current_pwd:
        print("\n🔧 GENERATING NEW PASSWORD HASH")
        print("="*50)
        new_hash = generate_new_password()
        
        print(f"\n📝 To update .env file:")
        print(f'ADMIN_PASSWORD_HASH="{new_hash}"')
        
        print(f"\n🔑 Login credentials would be:")
        print(f"Username: admin")
        print(f"Password: admin2024")
    else:
        print(f"\n🔑 Current login credentials:")
        print(f"Username: admin")
        print(f"Password: {current_pwd}")