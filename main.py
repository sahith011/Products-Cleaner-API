"""
FastAPI application for cleaning and standardizing ecommerce product data.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from app.schemas import (
    TitleCleanRequest,
    TitleCleanResponse,
    ProductInput,
    ProductCleaned,
    BulkCleanRequest,
    BulkCleanResponse,
)
from app.utils import (
    clean_title,
    parse_price,
    parse_rating,
    make_slug,
    extract_tags,
)


app = FastAPI(
    title="Product Cleaner API",
    description="Clean and standardize ecommerce product data",
    version="1.0.0",
)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Product Cleaner API",
        "version": "1.0.0",
        "endpoints": {
            "POST /clean/title": "Clean a single product title",
            "POST /clean/product": "Clean and standardize a complete product",
            "POST /clean/bulk": "Clean multiple products at once",
        },
    }


@app.post("/clean/title", response_model=TitleCleanResponse)
async def clean_product_title(request: TitleCleanRequest):
    """
    Clean a product title by removing extra whitespace and applying Title Case.
    
    Args:
        request: Contains raw_title string
        
    Returns:
        TitleCleanResponse with cleaned title
        
    Example:
        Input: {"raw_title": "  eco   friendly bottle  "}
        Output: {"clean_title": "Eco Friendly Bottle"}
    """
    cleaned = clean_title(request.raw_title)
    return TitleCleanResponse(clean_title=cleaned)


@app.post("/clean/product", response_model=ProductCleaned)
async def clean_product(product: ProductInput):
    """
    Clean and standardize a complete product record.
    
    Processes:
    - Title: cleaned and formatted in Title Case
    - Price: parsed to numeric value
    - Rating: parsed to 0-5 float
    - Slug: generated from cleaned title
    - Tags: extracted keywords from title
    
    Args:
        product: ProductInput with title, price, rating, category
        
    Returns:
        ProductCleaned with all processed fields
        
    Example:
        Input: {
            "title": " eco friendly bottle 500ml green",
            "price": "₹499",
            "rating": "4.2 out of 5",
            "category": "Kitchen"
        }
        Output: {
            "title_clean": "Eco Friendly Bottle 500ml Green",
            "price_value": 499.0,
            "rating_value": 4.2,
            "slug": "eco-friendly-bottle-500ml-green",
            "tags": ["eco", "friendly", "bottle", "500ml", "green"]
        }
    """
    # Clean the title
    title_cleaned = clean_title(product.title)
    
    # Parse price and rating
    price_val = parse_price(product.price)
    rating_val = parse_rating(product.rating)
    
    # Generate slug and tags from cleaned title
    slug = make_slug(title_cleaned)
    tags = extract_tags(title_cleaned)
    
    return ProductCleaned(
        title_clean=title_cleaned,
        price_value=price_val,
        rating_value=rating_val,
        slug=slug,
        tags=tags,
    )


@app.post("/clean/bulk", response_model=BulkCleanResponse)
async def clean_bulk_products(request: BulkCleanRequest):
    """
    Clean multiple products in a single request.
    
    Applies the same cleaning logic as /clean/product to each item in the list.
    
    Args:
        request: BulkCleanRequest containing list of products
        
    Returns:
        BulkCleanResponse with list of cleaned products
        
    Example:
        Input: {
            "products": [
                {"title": "widget a", "price": "$10", "rating": "5/5", "category": "Tools"},
                {"title": "widget b", "price": "$20", "rating": "4.5", "category": "Tools"}
            ]
        }
        Output: {
            "products": [
                {"title_clean": "Widget A", "price_value": 10.0, ...},
                {"title_clean": "Widget B", "price_value": 20.0, ...}
            ]
        }
    """
    cleaned_products = []
    
    for product in request.products:
        # Clean the title
        title_cleaned = clean_title(product.title)
        
        # Parse price and rating
        price_val = parse_price(product.price)
        rating_val = parse_rating(product.rating)
        
        # Generate slug and tags
        slug = make_slug(title_cleaned)
        tags = extract_tags(title_cleaned)
        
        cleaned_products.append(
            ProductCleaned(
                title_clean=title_cleaned,
                price_value=price_val,
                rating_value=rating_val,
                slug=slug,
                tags=tags,
            )
        )
    
    return BulkCleanResponse(products=cleaned_products)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error occurred"},
    )
