from pydantic import BaseModel
from typing import Optional
import hashlib
import secrets
import os
from datetime import datetime, timedelta
import jwt

class AdminCredentials(BaseModel):
    username: str
    password: str

class AuthToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600  # 1 hour

class AuthManager:
    def __init__(self):
        # In production, these should be environment variables
        self.admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        self.admin_password_hash = os.environ.get('ADMIN_PASSWORD_HASH', self._hash_password('admin2024'))
        self.jwt_secret = os.environ.get('JWT_SECRET', secrets.token_urlsafe(32))
        
    def _hash_password(self, password: str) -> str:
        """Hash password with salt"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}:{password_hash.hex()}"
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        try:
            salt, stored_hash = password_hash.split(':')
            password_hash_check = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return stored_hash == password_hash_check.hex()
        except:
            return False
    
    def create_access_token(self, username: str) -> str:
        """Create JWT access token"""
        payload = {
            'username': username,
            'exp': datetime.utcnow() + timedelta(hours=1),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')
    
    def verify_token(self, token: str) -> Optional[str]:
        """Verify JWT token and return username"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            return payload.get('username')
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def authenticate(self, username: str, password: str) -> Optional[AuthToken]:
        """Authenticate user and return token"""
        if username == self.admin_username and self.verify_password(password, self.admin_password_hash):
            access_token = self.create_access_token(username)
            return AuthToken(access_token=access_token)
        return None

# Global auth manager instance
auth_manager = AuthManager()