"""
Investments service for XRPL.Sale SDK
"""

from typing import Dict, Any, Optional
from ..models import Investment, ListInvestmentsOptions


class InvestmentsService:
    """Service for managing investments"""
    
    def __init__(self, client):
        self.client = client
    
    async def get(self, investment_id: str) -> Investment:
        """Get an investment by ID"""
        response = await self.client.get(f"/investments/{investment_id}")
        return Investment(**response)
    
    async def list(self, options: Optional[ListInvestmentsOptions] = None) -> Dict[str, Any]:
        """List investments with optional filtering"""
        params = {}
        if options:
            if isinstance(options, ListInvestmentsOptions):
                params = options.dict(exclude_none=True)
            else:
                params = options
        
        response = await self.client.get("/investments", params=params)
        return {
            "data": [Investment(**item) for item in response["data"]],
            "pagination": response["pagination"]
        }
    
    async def get_by_project(self, project_id: str, **kwargs) -> Dict[str, Any]:
        """Get investments for a specific project"""
        options = ListInvestmentsOptions(project_id=project_id, **kwargs)
        return await self.list(options)
    
    async def get_by_investor(self, investor_account: str, **kwargs) -> Dict[str, Any]:
        """Get investments for a specific investor"""
        options = ListInvestmentsOptions(investor_account=investor_account, **kwargs)
        return await self.list(options)
    
    async def create(self, investment_data: Dict[str, Any]) -> Investment:
        """Create a new investment"""
        response = await self.client.post("/investments", investment_data)
        return Investment(**response)
    
    async def get_investor_summary(self, investor_account: str) -> Dict[str, Any]:
        """Get investment summary for an investor"""
        return await self.client.get(f"/investments/summary/{investor_account}")
    
    async def simulate(self, simulation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate an investment (check pricing, fees, etc.)"""
        return await self.client.post("/investments/simulate", simulation_data)
    
    async def get_confirmed(self, **kwargs) -> Dict[str, Any]:
        """Get confirmed investments only"""
        options = ListInvestmentsOptions(status="confirmed", **kwargs)
        return await self.list(options)
    
    async def get_pending(self, **kwargs) -> Dict[str, Any]:
        """Get pending investments only"""
        options = ListInvestmentsOptions(status="pending", **kwargs)
        return await self.list(options)