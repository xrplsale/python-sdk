# XRPL.Sale Python SDK

Official Python SDK for integrating with the XRPL.Sale platform - the native XRPL launchpad for token sales and project funding.

[![PyPI version](https://badge.fury.io/py/xrpl-sale.svg)](https://pypi.org/project/xrpl-sale/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🐍 **Pure Python** - Built with async/await support
- 🚀 **Async/Await Support** - Modern Python async programming
- 🔐 **XRPL Wallet Authentication** - Seamless wallet integration
- 📊 **Project Management** - Create, launch, and manage token sales
- 💰 **Investment Tracking** - Monitor investments and analytics
- 🔔 **Webhook Support** - Real-time event notifications with framework integration
- 📈 **Analytics & Reporting** - Comprehensive data insights
- 🛡️ **Robust Error Handling** - Comprehensive exception hierarchy
- 🔄 **Auto-retry Logic** - Resilient API calls with exponential backoff
- 🐧 **Framework Integration** - FastAPI, Django, Flask support

## Installation

```bash
pip install xrpl-sale
```

For development with additional tools:

```bash
pip install xrpl-sale[dev]
```

For Django integration:

```bash
pip install xrpl-sale[django]
```

For FastAPI integration:

```bash
pip install xrpl-sale[fastapi]
```

## Quick Start

```python
import asyncio
from xrpl_sale import XRPLSaleClient

async def main():
    # Initialize the client
    client = XRPLSaleClient({
        "api_key": "your-api-key",
        "environment": "production",  # or "testnet"
        "debug": True
    })
    
    async with client:
        # Create a new project
        project = await client.projects.create({
            "name": "My DeFi Protocol",
            "description": "Revolutionary DeFi protocol on XRPL",
            "token_symbol": "MDP",
            "total_supply": "100000000",
            "tiers": [
                {
                    "tier": 1,
                    "price_per_token": "0.001",
                    "total_tokens": "20000000"
                }
            ],
            "sale_start_date": "2025-02-01T00:00:00Z",
            "sale_end_date": "2025-03-01T00:00:00Z"
        })
        
        print(f"Project created: {project.id}")

# Run the async function
asyncio.run(main())
```

## Context Manager Usage

The SDK supports async context managers for automatic resource cleanup:

```python
async with XRPLSaleClient("your-api-key") as client:
    projects = await client.projects.list()
    print(f"Found {len(projects['data'])} projects")
# Session automatically closed
```

## Authentication

### XRPL Wallet Authentication

```python
async def authenticate_wallet():
    async with XRPLSaleClient("your-api-key") as client:
        # Generate challenge
        challenge = await client.auth.generate_challenge("rYourWalletAddress...")
        
        # Sign the challenge with your wallet
        # (implementation depends on your wallet library)
        signature = sign_message(challenge["challenge"])
        
        # Authenticate
        auth_result = await client.auth.authenticate({
            "wallet_address": "rYourWalletAddress...",
            "signature": signature,
            "timestamp": challenge["timestamp"]
        })
        
        print(f"Authentication successful: {auth_result.token}")
        return auth_result.token
```

## Core Services

### Projects Service

```python
async def manage_projects():
    async with XRPLSaleClient("your-api-key") as client:
        # List active projects
        projects = await client.projects.get_active(page=1, limit=10)
        
        # Get project details
        project = await client.projects.get("proj_abc123")
        
        # Launch a project
        await client.projects.launch("proj_abc123")
        
        # Get project statistics
        stats = await client.projects.get_stats("proj_abc123")
        print(f"Total raised: {stats['total_raised']} XRP")
```

### Investments Service

```python
async def track_investments():
    async with XRPLSaleClient("your-api-key") as client:
        # Create an investment
        investment = await client.investments.create({
            "project_id": "proj_abc123",
            "amount_xrp": "100",
            "investor_account": "rInvestorAddress..."
        })
        
        # List investments for a project
        investments = await client.investments.get_by_project("proj_abc123")
        
        # Get investor summary
        summary = await client.investments.get_investor_summary("rInvestorAddress...")
        
        # Simulate an investment
        simulation = await client.investments.simulate({
            "project_id": "proj_abc123",
            "amount_xrp": "100"
        })
        print(f"Expected tokens: {simulation['token_amount']}")
```

### Analytics Service

```python
async def get_analytics():
    async with XRPLSaleClient("your-api-key") as client:
        # Get platform analytics
        analytics = await client.analytics.get_platform_analytics()
        print(f"Total raised: {analytics.total_raised_xrp} XRP")
        
        # Get project-specific analytics
        project_analytics = await client.analytics.get_project_analytics(
            "proj_abc123",
            start_date="2025-01-01",
            end_date="2025-01-31"
        )
        
        # Get market trends
        trends = await client.analytics.get_market_trends("30d")
        
        # Export data
        export_data = await client.analytics.export_data({
            "type": "projects",
            "format": "csv",
            "start_date": "2025-01-01",
            "end_date": "2025-01-31"
        })
        print(f"Download URL: {export_data['download_url']}")
```

## Webhook Integration

### FastAPI Integration

```python
from fastapi import FastAPI, Depends
from xrpl_sale import XRPLSaleClient

app = FastAPI()
client = XRPLSaleClient("your-api-key")

@app.post("/webhooks")
async def handle_webhook(
    event = Depends(client.webhooks.fastapi_dependency())
):
    if event.type == "investment.created":
        await handle_new_investment(event.data)
    elif event.type == "project.launched":
        await handle_project_launched(event.data)
    
    return {"status": "success"}

async def handle_new_investment(data):
    print(f"New investment: {data['amount_xrp']} XRP")
    # Process the investment...
```

### Django Integration

```python
from django.http import HttpResponse
from xrpl_sale import XRPLSaleClient

client = XRPLSaleClient("your-api-key")

@client.webhooks.django_view(verify_signature=True)
def webhook_handler(event):
    if event.type == "investment.created":
        handle_new_investment(event.data)
    elif event.type == "project.launched":
        handle_project_launched(event.data)
    
    return "OK"

def handle_new_investment(data):
    print(f"New investment: {data['amount_xrp']} XRP")
    # Process the investment...

# urls.py
from django.urls import path
urlpatterns = [
    path("webhooks/", webhook_handler, name="webhooks"),
]
```

### Flask Integration

```python
from flask import Flask
from xrpl_sale import XRPLSaleClient

app = Flask(__name__)
client = XRPLSaleClient("your-api-key")

@app.route("/webhooks", methods=["POST"])
@client.webhooks.flask_decorator()
def handle_webhook(event):
    if event.type == "investment.created":
        handle_new_investment(event.data)
    elif event.type == "project.launched":
        handle_project_launched(event.data)
    
    return "OK"

def handle_new_investment(data):
    print(f"New investment: {data['amount_xrp']} XRP")
    # Process the investment...
```

### Manual Webhook Verification

```python
import hmac
import hashlib

async def verify_webhook_manually():
    client = XRPLSaleClient("your-api-key")
    
    # In your webhook endpoint
    payload = request.body  # Raw request body
    signature = request.headers.get("X-XRPL-Sale-Signature")
    
    if client.webhooks.verify_signature(payload, signature):
        event = client.webhooks.parse_webhook(payload)
        # Process event...
    else:
        return "Invalid signature", 401
```

## Error Handling

The SDK provides comprehensive error handling:

```python
from xrpl_sale import (
    XRPLSaleError,
    ValidationError,
    AuthenticationError,
    NotFoundError,
    RateLimitError
)

async def handle_errors():
    async with XRPLSaleClient("your-api-key") as client:
        try:
            project = await client.projects.get("invalid-id")
        except NotFoundError:
            print("Project not found")
        except AuthenticationError:
            print("Authentication failed")
        except ValidationError as e:
            print(f"Validation error: {e.details}")
        except RateLimitError:
            print("Rate limit exceeded")
        except XRPLSaleError as e:
            print(f"API error: {e.message} (Status: {e.status_code})")
```

## Configuration Options

```python
from xrpl_sale import XRPLSaleClient, Environment

# Full configuration
client = XRPLSaleClient({
    "api_key": "your-api-key",
    "environment": Environment.PRODUCTION,  # or Environment.TESTNET
    "timeout": 30,  # Request timeout in seconds
    "debug": True,  # Enable debug logging
    "webhook_secret": "your-webhook-secret",
    "max_retries": 3,  # Maximum retries for failed requests
    "retry_delay": 1.0  # Delay between retries in seconds
})

# Simple configuration
client = XRPLSaleClient("your-api-key")  # Uses defaults
```

## Pagination

Most list methods support pagination:

```python
async def paginate_results():
    async with XRPLSaleClient("your-api-key") as client:
        result = await client.projects.list({
            "page": 1,
            "limit": 50,
            "sort_by": "created_at",
            "sort_order": "desc"
        })
        
        projects = result["data"]
        pagination = result["pagination"]
        
        print(f"Page {pagination['page']} of {pagination['total_pages']}")
        print(f"Total projects: {pagination['total']}")
```

## Retry Logic

The SDK includes automatic retry logic with exponential backoff:

```python
# Automatic retries are built-in
async with XRPLSaleClient({
    "api_key": "your-api-key",
    "max_retries": 5,
    "retry_delay": 2.0
}) as client:
    # This will automatically retry on network errors
    projects = await client.projects.list()
```

## Logging

Enable debug logging to see detailed request/response information:

```python
import logging

# Enable SDK debug logging
logging.basicConfig(level=logging.DEBUG)

client = XRPLSaleClient({
    "api_key": "your-api-key",
    "debug": True
})
```

## Testing

Run the test suite:

```bash
# Install dev dependencies
pip install -e .[dev]

# Run tests
pytest

# Run tests with coverage
pytest --cov=xrpl_sale

# Run async tests specifically
pytest -v tests/test_async.py
```

## Type Hints

The SDK includes comprehensive type hints for better IDE support:

```python
from typing import Dict, Any
from xrpl_sale import XRPLSaleClient, Project, Investment

async def typed_example(client: XRPLSaleClient) -> Project:
    project: Project = await client.projects.get("proj_123")
    return project
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Install development dependencies (`pip install -e .[dev]`)
4. Make your changes
5. Run tests (`pytest`)
6. Run linting (`black . && isort . && flake8`)
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/xrplsale/python-sdk.git
cd python-sdk

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .[dev]

# Run tests
pytest

# Format code
black .
isort .
flake8 .

# Type checking
mypy xrpl_sale
```

## Support

- 📖 [Documentation](https://docs.xrpl.sale)
- 💬 [Discord Community](https://discord.gg/xrpl-sale)
- 🐛 [Issue Tracker](https://github.com/xrplsale/python-sdk/issues)
- 📧 [Email Support](mailto:developers@xrpl.sale)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- [XRPL.Sale Platform](https://xrpl.sale)
- [API Documentation](https://docs.xrpl.sale/api)
- [Other SDKs](https://docs.xrpl.sale/developers/sdk-downloads)
- [GitHub Organization](https://github.com/xrplsale)

---

Made with ❤️ by the XRPL.Sale team