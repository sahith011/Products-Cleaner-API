"""
Utility functions for cleaning and parsing product data.
All functions are pure - no FastAPI dependencies.
"""

import re
from typing import Optional


# Common stopwords to filter out from tags
STOPWORDS = {
    "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "a", "an", "is", "it", "this", "that"
}


def clean_title(raw_title: str) -> str:
    """
    Clean a product title by stripping whitespace, collapsing multiple spaces,
    and converting to Title Case.
    
    Args:
        raw_title: The raw product title string
        
    Returns:
        Cleaned title in Title Case
        
    Examples:
        >>> clean_title("  eco   friendly bottle  ")
        'Eco Friendly Bottle'
    """
    if not raw_title:
        return ""
    
    # Strip leading/trailing whitespace
    title = raw_title.strip()
    
    # Collapse multiple spaces into one
    title = re.sub(r'\s+', ' ', title)
    
    # Convert to Title Case
    title = title.title()
    
    return title


def parse_price(price_str: str) -> Optional[float]:
    """
    Parse a price string to extract numeric value, ignoring currency symbols and text.
    
    Args:
        price_str: Price string which may contain currency symbols, commas, etc.
        
    Returns:
        Numeric price value as float, or None if parsing fails
        
    Examples:
        >>> parse_price("₹499")
        499.0
        >>> parse_price("1,299 INR")
        1299.0
        >>> parse_price("$12.50")
        12.5
    """
    if not price_str:
        return None
    
    try:
        # Remove currency symbols, commas, and text
        # Keep only digits and decimal point
        cleaned = re.sub(r'[^\d.]', '', price_str)
        
        if not cleaned:
            return None
            
        return float(cleaned)
    except (ValueError, AttributeError):
        return None


def parse_rating(rating_str: str) -> Optional[float]:
    """
    Parse a rating string to extract numeric value between 0 and 5.
    
    Args:
        rating_str: Rating string in various formats like "4.2 out of 5", "4/5", "4.2"
        
    Returns:
        Rating value as float between 0 and 5, or None if parsing fails
        
    Examples:
        >>> parse_rating("4.2 out of 5")
        4.2
        >>> parse_rating("4/5")
        4.0
        >>> parse_rating("4.2")
        4.2
    """
    if not rating_str:
        return None
    
    try:
        # Try to match "X out of Y" format
        match = re.search(r'([\d.]+)\s*out\s*of\s*[\d.]+', rating_str, re.IGNORECASE)
        if match:
            rating = float(match.group(1))
            return min(max(rating, 0.0), 5.0)  # Clamp between 0 and 5
        
        # Try to match "X/Y" format
        match = re.search(r'([\d.]+)\s*/\s*([\d.]+)', rating_str)
        if match:
            numerator = float(match.group(1))
            denominator = float(match.group(2))
            if denominator > 0:
                # Normalize to 5-point scale
                rating = (numerator / denominator) * 5.0
                return min(max(rating, 0.0), 5.0)
        
        # Try to extract just a number
        match = re.search(r'[\d.]+', rating_str)
        if match:
            rating = float(match.group())
            return min(max(rating, 0.0), 5.0)
        
        return None
    except (ValueError, AttributeError):
        return None


def make_slug(title: str) -> str:
    """
    Generate a URL-friendly slug from a title.
    Lowercase, hyphen-separated, only alphanumeric and hyphens.
    
    Args:
        title: Clean product title
        
    Returns:
        URL-friendly slug
        
    Examples:
        >>> make_slug("Eco Friendly Bottle")
        'eco-friendly-bottle'
    """
    if not title:
        return ""
    
    # Convert to lowercase
    slug = title.lower()
    
    # Replace spaces with hyphens
    slug = re.sub(r'\s+', '-', slug)
    
    # Keep only alphanumeric and hyphens
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    
    # Remove consecutive hyphens
    slug = re.sub(r'-+', '-', slug)
    
    # Strip leading/trailing hyphens
    slug = slug.strip('-')
    
    return slug


def extract_tags(title: str) -> list[str]:
    """
    Extract keyword tags from a title.
    Returns lowercase words, filtering out stopwords.
    
    Args:
        title: Product title
        
    Returns:
        List of keyword tags
        
    Examples:
        >>> extract_tags("Eco Friendly Bottle 500ml")
        ['eco', 'friendly', 'bottle', '500ml']
    """
    if not title:
        return []
    
    # Convert to lowercase and split into words
    words = title.lower().split()
    
    # Filter out stopwords and short words, keep only alphanumeric
    tags = []
    for word in words:
        # Remove non-alphanumeric characters
        clean_word = re.sub(r'[^a-z0-9]', '', word)
        
        # Keep if it's not a stopword and has content
        if clean_word and clean_word not in STOPWORDS:
            tags.append(clean_word)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_tags = []
    for tag in tags:
        if tag not in seen:
            seen.add(tag)
            unique_tags.append(tag)
    
    return unique_tags
