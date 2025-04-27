#!/usr/bin/env python3
"""
Generate a password hash using the same hashing method as the application.
"""

import sys
from passlib.context import CryptContext

# Use the same password hashing configuration as in security.py
PWD_CTX = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

if __name__ == "__main__":
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("Usage: generate_hash.py <password> [<hash_to_verify>]")
        sys.exit(1)
    
    password = sys.argv[1]
    
    # Generate hash
    hash_value = hash_password(password)
    print(f"Password: {password}")
    print(f"Hash: {hash_value}")
    
    # Verify against existing hash if provided
    if len(sys.argv) == 3:
        existing_hash = sys.argv[2]
        is_match = verify_password(password, existing_hash)
        print(f"Verification against existing hash: {'Success' if is_match else 'Failed'}") 