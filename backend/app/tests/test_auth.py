#!/usr/bin/env python3
"""
Test script for authentication endpoints.
"""

import asyncio
import os
import pytest
import aiohttp
from typing import Dict, Any

# Configuration
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_PREFIX = "/api/v1"
TEST_USER_CREDS = {"email": "admin1.a@example.com", "password": "password"}


@pytest.mark.asyncio
async def test_user_login_and_me_endpoint():
    """
    Tests that a user can log in and that the /auth/me endpoint
    returns the correct user information.
    """
    async with aiohttp.ClientSession() as session:
        # 1. Login to get the token
        login_url = f"{BASE_URL}{API_PREFIX}/auth/login"
        async with session.post(login_url, json=TEST_USER_CREDS) as response:
            assert response.status == 200, f"Login failed: {await response.text()}"
            login_data = await response.json()
            assert "access_token" in login_data
            assert login_data["role"] == "CompanyAdmin"
            access_token = login_data["access_token"]

        # 2. Test the protected /auth/me endpoint
        me_url = f"{BASE_URL}{API_PREFIX}/auth/me"
        headers = {"Authorization": f"Bearer {access_token}"}
        async with session.get(me_url, headers=headers) as response:
            assert response.status == 200, f"/auth/me endpoint failed: {await response.text()}"
            me_data = await response.json()
            assert me_data["email"] == TEST_USER_CREDS["email"]
            assert me_data["role"]["name"] == "CompanyAdmin"
            assert "company" in me_data
            print("✅ User login and /auth/me endpoint test passed!") 