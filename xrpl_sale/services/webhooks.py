"""
Webhooks service for XRPL.Sale SDK
"""

import hmac
import hashlib
import json
from typing import Dict, Any, Optional, List, Union, Callable
from ..models import WebhookEvent
from ..exceptions import XRPLSaleError


class WebhooksService:
    """Service for webhook management and verification"""
    
    def __init__(self, client):
        self.client = client
        self.webhook_secret = getattr(client.config, 'webhook_secret', None)
    
    def verify_signature(
        self, 
        payload: Union[str, bytes], 
        signature: str, 
        secret: Optional[str] = None
    ) -> bool:
        """Verify webhook signature"""
        secret_to_use = secret or self.webhook_secret
        if not secret_to_use:
            raise XRPLSaleError("Webhook secret is required for signature verification")
        
        if isinstance(payload, str):
            payload = payload.encode('utf-8')
        
        expected_signature = hmac.new(
            secret_to_use.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        expected_signature = f"sha256={expected_signature}"
        
        # Use constant-time comparison to prevent timing attacks
        return hmac.compare_digest(expected_signature, signature)
    
    def parse_webhook(self, payload: Union[str, bytes]) -> WebhookEvent:
        """Parse webhook payload"""
        try:
            if isinstance(payload, bytes):
                payload = payload.decode('utf-8')
            
            data = json.loads(payload)
            return WebhookEvent(**data)
        except (json.JSONDecodeError, TypeError) as e:
            raise XRPLSaleError(f"Invalid webhook payload: {e}")
    
    def fastapi_dependency(
        self, 
        verify_signature: bool = True,
        secret: Optional[str] = None
    ):
        """FastAPI dependency for webhook handling"""
        from fastapi import Request, HTTPException, Depends
        
        async def webhook_handler(request: Request):
            try:
                body = await request.body()
                
                if verify_signature:
                    signature = request.headers.get("x-xrpl-sale-signature")
                    if not signature:
                        raise HTTPException(status_code=401, detail="Missing signature header")
                    
                    if not self.verify_signature(body, signature, secret):
                        raise HTTPException(status_code=401, detail="Invalid signature")
                
                event = self.parse_webhook(body)
                return event
                
            except XRPLSaleError as e:
                raise HTTPException(status_code=400, detail=str(e))
        
        return webhook_handler
    
    def flask_decorator(
        self, 
        verify_signature: bool = True,
        secret: Optional[str] = None
    ):
        """Flask decorator for webhook handling"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                from flask import request, abort
                
                try:
                    payload = request.get_data()
                    
                    if verify_signature:
                        signature = request.headers.get("X-XRPL-Sale-Signature")
                        if not signature:
                            abort(401, "Missing signature header")
                        
                        if not self.verify_signature(payload, signature, secret):
                            abort(401, "Invalid signature")
                    
                    event = self.parse_webhook(payload)
                    return func(event, *args, **kwargs)
                    
                except XRPLSaleError:
                    abort(400, "Invalid webhook payload")
            
            return wrapper
        return decorator
    
    def django_view(
        self, 
        handler_func: Callable,
        verify_signature: bool = True,
        secret: Optional[str] = None
    ):
        """Django view for webhook handling"""
        from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
        from django.views.decorators.csrf import csrf_exempt
        from django.views.decorators.http import require_http_methods
        
        @csrf_exempt
        @require_http_methods(["POST"])
        def webhook_view(request):
            try:
                payload = request.body
                
                if verify_signature:
                    signature = request.META.get("HTTP_X_XRPL_SALE_SIGNATURE")
                    if not signature:
                        return HttpResponseForbidden("Missing signature header")
                    
                    if not self.verify_signature(payload, signature, secret):
                        return HttpResponseForbidden("Invalid signature")
                
                event = self.parse_webhook(payload)
                result = handler_func(event)
                
                return HttpResponse("OK" if result is None else str(result))
                
            except XRPLSaleError:
                return HttpResponseBadRequest("Invalid webhook payload")
        
        return webhook_view
    
    async def register(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Register a webhook endpoint"""
        return await self.client.post("/webhooks", webhook_data)
    
    async def list(self) -> List[Dict[str, Any]]:
        """List registered webhooks"""
        response = await self.client.get("/webhooks")
        return response
    
    async def update(self, webhook_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update a webhook"""
        return await self.client.patch(f"/webhooks/{webhook_id}", updates)
    
    async def delete(self, webhook_id: str) -> Dict[str, Any]:
        """Delete a webhook"""
        return await self.client.delete(f"/webhooks/{webhook_id}")
    
    async def test(self, webhook_id: str) -> Dict[str, Any]:
        """Test webhook delivery"""
        return await self.client.post(f"/webhooks/{webhook_id}/test")
    
    async def get_deliveries(
        self, 
        webhook_id: str, 
        page: int = 1,
        limit: int = 10,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get webhook delivery logs"""
        params = {"page": page, "limit": limit}
        if status:
            params["status"] = status
        
        return await self.client.get(f"/webhooks/{webhook_id}/deliveries", params=params)