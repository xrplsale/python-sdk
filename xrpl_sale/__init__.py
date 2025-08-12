"""
XRPL.Sale Python SDK

Official Python SDK for integrating with the XRPL.Sale platform.
"""

from .client import XRPLSaleClient
from .services import (
    ProjectsService,
    InvestmentsService,
    AnalyticsService,
    WebhooksService,
    AuthService,
)
from .models import *
from .exceptions import *
from .utils import *

__version__ = "1.0.0"
__author__ = "XRPL.Sale Development Team"
__email__ = "developers@xrpl.sale"

__all__ = [
    "XRPLSaleClient",
    "ProjectsService",
    "InvestmentsService", 
    "AnalyticsService",
    "WebhooksService",
    "AuthService",
]