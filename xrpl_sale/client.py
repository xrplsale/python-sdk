"""
Main XRPL.Sale client implementation
"""

import asyncio
import logging
from typing import Optional, Dict, Any, Union
from urllib.parse import urljoin

import aiohttp
from pydantic import BaseModel, Field

from .services import (
    ProjectsService,
    InvestmentsService,
    AnalyticsService,
    WebhooksService,
    AuthService,
)
from .exceptions import XRPLSaleError, AuthenticationError
from .models import Environment

logger = logging.getLogger(__name__)


class XRPLSaleConfig(BaseModel):
    """Configuration for XRPL.Sale client"""
    
    api_key: str = Field(..., description="API key for authentication")
    environment: Environment = Field(Environment.PRODUCTION, description="Environment to use")
    timeout: int = Field(30, description="Request timeout in seconds")
    debug: bool = Field(False, description="Enable debug logging")
    webhook_secret: Optional[str] = Field(None, description="Secret for webhook verification")
    max_retries: int = Field(3, description="Maximum number of retries for failed requests")
    retry_delay: float = Field(1.0, description="Delay between retries in seconds")


class XRPLSaleClient:
    """
    Main XRPL.Sale SDK client with async support
    
    Provides access to all XRPL.Sale platform services including project management,
    investment tracking, analytics, webhooks, and authentication.
    """
    
    def __init__(self, config: Union[XRPLSaleConfig, Dict[str, Any], str]):
        """
        Initialize the XRPL.Sale client
        
        Args:
            config: Configuration object, dict, or API key string
        """
        if isinstance(config, str):
            config = XRPLSaleConfig(api_key=config)
        elif isinstance(config, dict):
            config = XRPLSaleConfig(**config)
        
        self.config = config
        self.base_url = self._get_base_url(config.environment)
        self._session: Optional[aiohttp.ClientSession] = None
        
        # Initialize services
        self.projects = ProjectsService(self)
        self.investments = InvestmentsService(self)
        self.analytics = AnalyticsService(self)
        self.webhooks = WebhooksService(self)
        self.auth = AuthService(self)
        
        if config.debug:
            logging.basicConfig(level=logging.DEBUG)
    
    def _get_base_url(self, environment: Environment) -> str:
        """Get base URL for the specified environment"""
        if environment == Environment.PRODUCTION:
            return "https://xrpl.sale/api"
        elif environment == Environment.TESTNET:
            return "https://testnet.xrpl.sale/api"
        else:
            raise ValueError(f"Unknown environment: {environment}")
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self._ensure_session()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    async def _ensure_session(self):
        """Ensure aiohttp session is created"""
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            headers = {
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
                "User-Agent": f"xrpl-sale-python-sdk/1.0.0",
            }
            self._session = aiohttp.ClientSession(
                timeout=timeout,
                headers=headers,
                raise_for_status=False
            )
    
    async def close(self):
        """Close the HTTP session"""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make an HTTP request with retry logic
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request body data
            params: Query parameters
            **kwargs: Additional request arguments
            
        Returns:
            Response data as dictionary
            
        Raises:
            XRPLSaleError: On API errors
        """
        await self._ensure_session()
        
        url = urljoin(self.base_url, endpoint)
        
        for attempt in range(self.config.max_retries + 1):
            try:
                if self.config.debug:
                    logger.debug(f"Making {method} request to {url}")
                
                async with self._session.request(
                    method,
                    url,
                    json=data,
                    params=params,
                    **kwargs
                ) as response:
                    response_data = await response.json()
                    
                    if response.status >= 400:
                        error_message = response_data.get("message", f"HTTP {response.status}")
                        if response.status == 401:
                            raise AuthenticationError(error_message)
                        else:
                            raise XRPLSaleError(
                                error_message,
                                status_code=response.status,
                                details=response_data
                            )
                    
                    return response_data
                    
            except aiohttp.ClientError as e:
                if attempt == self.config.max_retries:
                    raise XRPLSaleError(f"Network error: {str(e)}")
                
                if self.config.debug:
                    logger.debug(f"Request failed (attempt {attempt + 1}), retrying...")
                
                await asyncio.sleep(self.config.retry_delay * (2 ** attempt))
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request"""
        return await self._request("GET", endpoint, params=params)
    
    async def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a POST request"""
        return await self._request("POST", endpoint, data=data)
    
    async def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a PATCH request"""
        return await self._request("PATCH", endpoint, data=data)
    
    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make a DELETE request"""
        return await self._request("DELETE", endpoint)
    
    async def ping(self) -> Dict[str, Any]:
        """Test the API connection"""
        return await self.get("/ping")
    
    async def get_status(self) -> Dict[str, Any]:
        """Get API status and health information"""
        return await self.get("/status")