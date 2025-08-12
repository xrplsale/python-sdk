"""
Pydantic models for XRPL.Sale SDK
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, validator


class Environment(str, Enum):
    """Supported environments"""
    PRODUCTION = "production"
    TESTNET = "testnet"


class ProjectStatus(str, Enum):
    """Project status options"""
    DRAFT = "draft"
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class InvestmentStatus(str, Enum):
    """Investment status options"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"
    REFUNDED = "refunded"


class WebhookEventType(str, Enum):
    """Webhook event types"""
    PROJECT_CREATED = "project.created"
    PROJECT_UPDATED = "project.updated"
    PROJECT_LAUNCHED = "project.launched"
    PROJECT_COMPLETED = "project.completed"
    INVESTMENT_CREATED = "investment.created"
    INVESTMENT_CONFIRMED = "investment.confirmed"
    INVESTMENT_FAILED = "investment.failed"
    TIER_COMPLETED = "tier.completed"
    TOKENS_DISTRIBUTED = "tokens.distributed"


class PaginationInfo(BaseModel):
    """Pagination information"""
    page: int
    limit: int
    total: int
    total_pages: int
    has_next: bool
    has_prev: bool


class PaginatedResponse(BaseModel):
    """Generic paginated response"""
    pagination: PaginationInfo


class ProjectTier(BaseModel):
    """Project tier configuration"""
    tier: int
    price_per_token: str
    total_tokens: str
    tokens_remaining: str
    min_investment: Optional[str] = None
    max_investment: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class Project(BaseModel):
    """Project model"""
    id: str
    name: str
    description: str
    token_symbol: str
    total_supply: str
    sale_supply: str
    created_at: datetime
    updated_at: datetime
    status: ProjectStatus
    sale_start_date: datetime
    sale_end_date: datetime
    tiers: List[ProjectTier]
    current_tier: int
    total_raised: str
    investor_count: int
    is_active: bool


class CreateProjectRequest(BaseModel):
    """Request model for creating a project"""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=2000)
    token_symbol: str = Field(..., regex=r"^[A-Z][A-Z0-9]{2,9}$")
    total_supply: str = Field(..., regex=r"^[0-9]+$")
    tiers: List[Dict[str, Any]]
    sale_start_date: Union[datetime, str]
    sale_end_date: Union[datetime, str]
    metadata: Optional[Dict[str, Any]] = None

    @validator("tiers")
    def validate_tiers(cls, v):
        if not v:
            raise ValueError("At least one tier is required")
        return v


class Investment(BaseModel):
    """Investment model"""
    id: str
    project_id: str
    investor_account: str
    amount_xrp: str
    token_amount: str
    status: InvestmentStatus
    transaction_hash: str
    tier: int
    created_at: datetime
    confirmed_at: Optional[datetime] = None


class Analytics(BaseModel):
    """Platform analytics model"""
    total_raised_xrp: str
    total_projects: int
    active_projects: int
    total_investors: int
    average_investment: str
    top_projects: List[Project]
    recent_investments: List[Investment]


class ProjectAnalytics(BaseModel):
    """Project-specific analytics"""
    project_id: str
    total_raised_xrp: str
    investor_count: int
    current_tier: int
    completion_percentage: float
    tier_distribution: List[Dict[str, Union[int, str]]]
    daily_investments: List[Dict[str, Union[str, int]]]


class WebhookEvent(BaseModel):
    """Webhook event model"""
    id: str
    type: WebhookEventType
    data: Dict[str, Any]
    timestamp: datetime
    version: str


class AuthRequest(BaseModel):
    """Authentication request model"""
    wallet_address: str = Field(..., regex=r"^r[1-9A-HJ-NP-Za-km-z]{25,34}$")
    signature: str
    timestamp: int


class AuthResponse(BaseModel):
    """Authentication response model"""
    token: str
    expires_at: datetime
    user_tier: Dict[str, Union[str, int, bool]]


class UserTier(BaseModel):
    """User tier information"""
    tier: str
    multiplier: float
    early_access: int
    guaranteed: bool


class ListProjectsOptions(BaseModel):
    """Options for listing projects"""
    page: int = 1
    limit: int = 10
    status: Optional[ProjectStatus] = None
    sort_by: str = "created_at"
    sort_order: str = "desc"


class ListInvestmentsOptions(BaseModel):
    """Options for listing investments"""
    page: int = 1
    limit: int = 10
    project_id: Optional[str] = None
    investor_account: Optional[str] = None
    status: Optional[InvestmentStatus] = None
    sort_by: str = "created_at"
    sort_order: str = "desc"