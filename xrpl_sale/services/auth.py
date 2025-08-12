"""
Authentication service for XRPL.Sale SDK
"""

from typing import Dict, Any
from ..models import AuthRequest, AuthResponse


class AuthService:
    """Service for authentication and authorization"""
    
    def __init__(self, client):
        self.client = client
    
    async def authenticate(self, auth_data: AuthRequest) -> AuthResponse:
        """Authenticate with XRPL wallet signature"""
        if isinstance(auth_data, AuthRequest):
            data = auth_data.dict()
        else:
            data = auth_data
        
        response = await self.client.post("/auth/wallet", data)
        return AuthResponse(**response)
    
    async def refresh(self, refresh_token: str) -> AuthResponse:
        """Refresh authentication token"""
        response = await self.client.post("/auth/refresh", {"refresh_token": refresh_token})
        return AuthResponse(**response)
    
    async def logout(self) -> Dict[str, Any]:
        """Logout and invalidate token"""
        return await self.client.post("/auth/logout")
    
    async def get_profile(self) -> Dict[str, Any]:
        """Get current user profile"""
        return await self.client.get("/auth/profile")
    
    async def update_profile(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update user profile"""
        return await self.client.patch("/auth/profile", updates)
    
    async def generate_challenge(self, wallet_address: str) -> Dict[str, Any]:
        """Generate authentication challenge for wallet signing"""
        return await self.client.post("/auth/challenge", {"wallet_address": wallet_address})
    
    async def verify_wallet(self, verification_data: Dict[str, Any]) -> Dict[str, Any]:
        """Verify wallet ownership"""
        return await self.client.post("/auth/verify", verification_data)
    
    async def get_permissions(self) -> Dict[str, Any]:
        """Get user permissions"""
        return await self.client.get("/auth/permissions")