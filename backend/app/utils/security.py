from passlib.context import CryptContext
from datetime import timedelta, datetime
import jwt
import os
from typing import Dict, Any, Optional

# Password hashing configuration
PWD_CTX = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
# Use a proper environment variable with a more secure default
SECRET = os.getenv("JWT_SECRET", "6Qb6XHKz9TP2QzWm7C5sR8vN3pL4yE1xA7")
ALG = "HS256"

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: The raw password to hash
        
    Returns:
        Hashed password string
    """
    return PWD_CTX.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        plain_password: The raw password to verify
        hashed_password: The hashed password to compare against
        
    Returns:
        True if password matches, False otherwise
    """
    return PWD_CTX.verify(plain_password, hashed_password)

def create_token(sub: str, tenant: str, role: str, exp_min: int = 15, extra: Optional[Dict[str, Any]] = None) -> str:
    """
    Create a JWT token with claims.
    
    Args:
        sub: Subject (usually user_guid)
        tenant: Company GUID
        role: User role (SystemAdmin, CompanyAdmin, etc.)
        exp_min: Expiration time in minutes
        extra: Additional claims to include
        
    Returns:
        Encoded JWT token string
    """
    payload = {
        "sub": sub,
        "tenant": tenant,
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=exp_min)
    }
    
    if extra:
        payload.update(extra)
        
    return jwt.encode(payload, SECRET, ALG)

def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate a JWT token.
    
    Args:
        token: The JWT token to decode
        
    Returns:
        Dict of token claims
        
    Raises:
        jwt.PyJWTError: If token is invalid or expired
    """
    return jwt.decode(token, SECRET, algorithms=[ALG]) 