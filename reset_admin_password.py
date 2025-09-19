#!/usr/bin/env python3
"""
Reset admin password to something simple
"""

import hashlib
import secrets
from pathlib import Path

def hash_password(password: str) -> str:
    """Hash password with salt"""
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{salt}:{password_hash.hex()}"

# Generate new simple password hash
new_password = "admin"
new_hash = hash_password(new_password)

print(f"🔧 RESETTING ADMIN PASSWORD")
print(f"="*50)
print(f"New password: {new_password}")
print(f"New hash: {new_hash}")

# Update .env file
env_file = Path('/app/backend/.env')
if env_file.exists():
    with open(env_file, 'r') as f:
        content = f.read()
    
    # Replace the hash line
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('ADMIN_PASSWORD_HASH='):
            lines[i] = f'ADMIN_PASSWORD_HASH="{new_hash}"'
            break
    
    with open(env_file, 'w') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ Updated .env file")
    print(f"🔑 New login credentials:")
    print(f"   Username: admin")
    print(f"   Password: {new_password}")
    print(f"")
    print(f"⚠️  Please restart the backend service:")
    print(f"   sudo supervisorctl restart backend")
else:
    print(f"❌ .env file not found")