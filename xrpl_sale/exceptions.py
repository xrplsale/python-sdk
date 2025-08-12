"""
Custom exceptions for XRPL.Sale SDK
"""

from typing import Any, Dict, Optional


class XRPLSaleError(Exception):
    """Base exception for XRPL.Sale SDK errors"""
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}
    
    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class ValidationError(XRPLSaleError):
    """Raised when request validation fails"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=400, details=details)


class AuthenticationError(XRPLSaleError):
    """Raised when authentication fails"""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)


class AuthorizationError(XRPLSaleError):
    """Raised when authorization fails"""
    
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, status_code=403)


class NotFoundError(XRPLSaleError):
    """Raised when a resource is not found"""
    
    def __init__(self, resource: str):
        super().__init__(f"{resource} not found", status_code=404)


class RateLimitError(XRPLSaleError):
    """Raised when rate limit is exceeded"""
    
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, status_code=429)


class ServerError(XRPLSaleError):
    """Raised when server error occurs"""
    
    def __init__(self, message: str = "Internal server error"):
        super().__init__(message, status_code=500)