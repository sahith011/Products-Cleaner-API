"""
Pydantic models for request and response validation.
"""

from pydantic import BaseModel, Field
from typing import Optional


class TitleCleanRequest(BaseModel):
    """Request model for /clean/title endpoint."""
    raw_title: str = Field(..., description="Raw product title to clean")


class TitleCleanResponse(BaseModel):
    """Response model for /clean/title endpoint."""
    clean_title: str = Field(..., description="Cleaned product title in Title Case")


class ProductInput(BaseModel):
    """Input model for a single product."""
    title: str = Field(..., description="Raw product title")
    price: str = Field(..., description="Price string with currency symbols")
    rating: str = Field(..., description="Rating string in various formats")
    category: str = Field(..., description="Product category free text")


class ProductCleaned(BaseModel):
    """Cleaned product output model."""
    title_clean: str = Field(..., description="Cleaned product title")
    price_value: Optional[float] = Field(None, description="Parsed numeric price value")
    rating_value: Optional[float] = Field(None, description="Parsed rating value (0-5)")
    slug: str = Field(..., description="URL-friendly slug")
    tags: list[str] = Field(..., description="Keyword tags extracted from title")


class BulkCleanRequest(BaseModel):
    """Request model for /clean/bulk endpoint."""
    products: list[ProductInput] = Field(..., description="List of products to clean")


class BulkCleanResponse(BaseModel):
    """Response model for /clean/bulk endpoint."""
    products: list[ProductCleaned] = Field(..., description="List of cleaned products")
