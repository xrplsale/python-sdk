"""
Setup configuration for XRPL.Sale Python SDK
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="xrpl-sale",
    version="1.0.0",
    author="XRPL.Sale Development Team",
    author_email="developers@xrpl.sale",
    description="Official Python SDK for XRPL.Sale platform integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xrplsale/python-sdk",
    project_urls={
        "Documentation": "https://docs.xrpl.sale",
        "Bug Tracker": "https://github.com/xrplsale/python-sdk/issues",
        "Homepage": "https://xrpl.sale",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Office/Business :: Financial",
    ],
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "django": [
            "django>=3.2",
        ],
        "fastapi": [
            "fastapi>=0.95.0",
            "uvicorn>=0.20.0",
        ],
    },
    keywords="xrpl xrpl-sale launchpad blockchain token-sale sdk python asyncio",
    license="MIT",
    zip_safe=False,
    include_package_data=True,
    package_data={
        "xrpl_sale": ["py.typed"],
    },
)