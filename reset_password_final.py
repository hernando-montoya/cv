#!/usr/bin/env python3
"""
Set final admin password to Vp12345!
"""

import hashlib
import secrets
from pathlib import Path

def hash_password(password: str) -> str:
    """Hash password with salt"""
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{salt}:{password_hash.hex()}"

# Set final password
final_password = "Vp12345!"
final_hash = hash_password(final_password)

print(f"🔧 CONFIGURANDO CONTRASEÑA FINAL")
print(f"="*50)
print(f"Nueva contraseña: {final_password}")
print(f"Hash generado: {final_hash}")

# Update .env file
env_file = Path('/app/backend/.env')
if env_file.exists():
    with open(env_file, 'r') as f:
        content = f.read()
    
    # Replace the hash line
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('ADMIN_PASSWORD_HASH='):
            lines[i] = f'ADMIN_PASSWORD_HASH="{final_hash}"'
            break
    
    with open(env_file, 'w') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ Actualizado .env file")
    print(f"🔑 Credenciales finales:")
    print(f"   Usuario: admin")
    print(f"   Contraseña: {final_password}")
    print(f"")
    print(f"⚠️  Reinicia el backend:")
    print(f"   sudo supervisorctl restart backend")
else:
    print(f"❌ .env file not found")

# Also update auth_debug.py to accept only this password
auth_debug_file = Path('/app/backend/models/auth_debug.py')
if auth_debug_file.exists():
    with open(auth_debug_file, 'r') as f:
        content = f.read()
    
    # Replace the valid_passwords line
    new_content = content.replace(
        "self.valid_passwords = ['admin', 'admin2024', '123', 'test', 'password']",
        f"self.valid_passwords = ['{final_password}']"
    )
    
    with open(auth_debug_file, 'w') as f:
        f.write(new_content)
    
    print(f"✅ Actualizado auth_debug.py - solo acepta: {final_password}")
else:
    print(f"❌ auth_debug.py not found")