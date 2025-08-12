"""
Projects service for XRPL.Sale SDK
"""

from typing import Dict, Any, Optional, List
from ..models import Project, CreateProjectRequest, ListProjectsOptions, PaginatedResponse


class ProjectsService:
    """Service for managing projects"""
    
    def __init__(self, client):
        self.client = client
    
    async def create(self, project_data: CreateProjectRequest) -> Project:
        """Create a new project"""
        if isinstance(project_data, CreateProjectRequest):
            data = project_data.dict()
        else:
            data = project_data
        
        response = await self.client.post("/projects", data)
        return Project(**response)
    
    async def get(self, project_id: str) -> Project:
        """Get a project by ID"""
        response = await self.client.get(f"/projects/{project_id}")
        return Project(**response)
    
    async def list(self, options: Optional[ListProjectsOptions] = None) -> Dict[str, Any]:
        """List projects with optional filtering"""
        params = {}
        if options:
            if isinstance(options, ListProjectsOptions):
                params = options.dict(exclude_none=True)
            else:
                params = options
        
        response = await self.client.get("/projects", params=params)
        return {
            "data": [Project(**item) for item in response["data"]],
            "pagination": response["pagination"]
        }
    
    async def update(self, project_id: str, updates: Dict[str, Any]) -> Project:
        """Update a project"""
        response = await self.client.patch(f"/projects/{project_id}", updates)
        return Project(**response)
    
    async def launch(self, project_id: str) -> Project:
        """Launch a project (make it active for investments)"""
        response = await self.client.post(f"/projects/{project_id}/launch")
        return Project(**response)
    
    async def pause(self, project_id: str) -> Project:
        """Pause a project"""
        response = await self.client.post(f"/projects/{project_id}/pause")
        return Project(**response)
    
    async def resume(self, project_id: str) -> Project:
        """Resume a paused project"""
        response = await self.client.post(f"/projects/{project_id}/resume")
        return Project(**response)
    
    async def cancel(self, project_id: str) -> Project:
        """Cancel a project"""
        response = await self.client.post(f"/projects/{project_id}/cancel")
        return Project(**response)
    
    async def get_stats(self, project_id: str) -> Dict[str, Any]:
        """Get project statistics"""
        return await self.client.get(f"/projects/{project_id}/stats")
    
    async def get_active(self, **kwargs) -> Dict[str, Any]:
        """Get active projects (shorthand for list with status filter)"""
        options = ListProjectsOptions(status="active", **kwargs)
        return await self.list(options)