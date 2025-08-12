"""
Analytics service for XRPL.Sale SDK
"""

from typing import Dict, Any, Optional
from ..models import Analytics, ProjectAnalytics


class AnalyticsService:
    """Service for analytics and reporting"""
    
    def __init__(self, client):
        self.client = client
    
    async def get_platform_analytics(self) -> Analytics:
        """Get platform-wide analytics"""
        response = await self.client.get("/analytics/platform")
        return Analytics(**response)
    
    async def get_project_analytics(
        self, 
        project_id: str, 
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        granularity: Optional[str] = None
    ) -> ProjectAnalytics:
        """Get analytics for a specific project"""
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if granularity:
            params["granularity"] = granularity
        
        response = await self.client.get(f"/analytics/projects/{project_id}", params=params)
        return ProjectAnalytics(**response)
    
    async def get_investor_analytics(self, investor_account: str) -> Dict[str, Any]:
        """Get investor analytics"""
        return await self.client.get(f"/analytics/investors/{investor_account}")
    
    async def get_market_trends(self, period: str = "30d") -> Dict[str, Any]:
        """Get market trends and statistics"""
        return await self.client.get(f"/analytics/trends?period={period}")
    
    async def get_tier_analytics(self) -> Dict[str, Any]:
        """Get tier system analytics"""
        return await self.client.get("/analytics/tiers")
    
    async def export_data(self, options: Dict[str, Any]) -> Dict[str, Any]:
        """Export analytics data"""
        return await self.client.post("/analytics/export", options)