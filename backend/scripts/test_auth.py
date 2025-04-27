#!/usr/bin/env python3
"""
Test script for authentication against the real database.
This script allows you to test the authentication endpoints
without having to use the web interface.
"""

import argparse
import asyncio
import httpx
import json
import os
from typing import Dict, Any

async def test_auth(base_url: str, email: str, password: str) -> Dict[str, Any]:
    """
    Test authentication with the given credentials.
    
    Args:
        base_url: Base URL of the API
        email: Email address for login
        password: Password for login
        
    Returns:
        Response data from the API
    """
    auth_url = f"{base_url}/api/v1/auth/login"
    
    # Prepare the request data
    data = {
        "email": email,
        "password": password
    }
    
    # Make the request
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                auth_url,
                json=data,
                headers={"Content-Type": "application/json"}
            )
            
            # Parse the response
            response_data = response.json()
            
            if response.status_code == 200:
                print("Authentication successful!")
                print(f"Status code: {response.status_code}")
                
                # Print the token details but truncate them for security
                token_data = {
                    "access_token": response_data["access_token"][:20] + "..." if response_data.get("access_token") else None,
                    "refresh_token": response_data["refresh_token"][:20] + "..." if response_data.get("refresh_token") else None,
                    "role": response_data.get("role"),
                    "expires_in": response_data.get("expires_in")
                }
                print(json.dumps(token_data, indent=2))
                
                # Test the protected endpoint
                me_url = f"{base_url}/api/v1/auth/me"
                me_response = await client.get(
                    me_url,
                    headers={
                        "Authorization": f"Bearer {response_data['access_token']}",
                        "Content-Type": "application/json"
                    }
                )
                
                if me_response.status_code == 200:
                    print("\nUser info endpoint successful!")
                    print(json.dumps(me_response.json(), indent=2))
                else:
                    print("\nUser info endpoint failed:")
                    print(f"Status code: {me_response.status_code}")
                    print(json.dumps(me_response.json(), indent=2))
            else:
                print("Authentication failed!")
                print(f"Status code: {response.status_code}")
                print(json.dumps(response_data, indent=2))
                
            return response_data
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return {"error": str(e)}
        
async def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Test authentication with the real database")
    parser.add_argument("--email", help="Email address for login", required=True)
    parser.add_argument("--password", help="Password for login", required=True)
    parser.add_argument("--url", help="Base URL of the API", default="https://rafactory.raworkshop.bg")
    
    args = parser.parse_args()
    
    # Test authentication
    await test_auth(args.url, args.email, args.password)

if __name__ == "__main__":
    asyncio.run(main()) 