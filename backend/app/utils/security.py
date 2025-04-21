from datetime import datetime, timedelta
from typing import Optional, Any, Dict

from passlib.context import CryptContext
import jwt

from app.core.config import settings

# Password hashing context
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return PWD_CONTEXT.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return PWD_CONTEXT.verify(plain_password, hashed_password)

def create_token(
    subject: str, 
    tenant: str, 
    role: str, 
    expires_min: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    extra_data: Optional[Dict[str, Any]] = None
) -> str:
    """Create a JWT token with tenant and role claims."""
    expiry = datetime.utcnow() + timedelta(minutes=expires_min)
    
    # Base payload
    payload = {
        "sub": subject,
        "tenant": tenant,
        "role": role,
        "exp": expiry
    }
    
    # Add any extra data if provided
    if extra_data:
        payload.update(extra_data)
        
    # Encode with JWT
    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

def decode_token(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.PyJWTError as e:
        raise ValueError(f"Invalid token: {str(e)}") 