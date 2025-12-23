# Product Cleaner API

A lightweight, robust tool for cleaning messy ecommerce product data. 

We all know the pain of getting supplier CSVs with titles like `"  SUMMER   drESS  2024 "` and mixed-up price formats. This API automates the cleanup process, giving you standardized, ready-to-use JSON data for your store. Designed to be simple to run locally or deploy to the cloud.

## Features

- **Title Cleaning**: Removes extra whitespace, normalizes formatting, applies Title Case
- **Price Parsing**: Extracts numeric values from prices with currency symbols (₹, $, etc.) and formatting
- **Rating Normalization**: Parses ratings in various formats ("4.2 out of 5", "4/5", etc.) to a 0-5 scale
- **Slug Generation**: Creates URL-friendly slugs from product titles
- **Tag Extraction**: Generates keyword tags from titles, filtering out common stopwords
- **Bulk Processing**: Handle multiple products in a single API call

## Tech Stack

- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Data Validation**: Pydantic
- **Server**: Uvicorn (for local development)
- **Testing**: Pytest with httpx

## Setup Locally

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd product-cleaner-api
```

### 2. Create a virtual environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the development server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

Interactive API docs (Swagger UI): `http://127.0.0.1:8000/docs`

## API Endpoints

### 1. POST `/clean/title`

Clean a single product title.

**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/clean/title" \
  -H "Content-Type: application/json" \
  -d '{"raw_title": "  eco   friendly bottle  "}'
```

**Response:**
```json
{
  "clean_title": "Eco Friendly Bottle"
}
```

---

### 2. POST `/clean/product`

Clean and standardize a complete product record.

**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/clean/product" \
  -H "Content-Type: application/json" \
  -d '{
    "title": " eco friendly bottle 500ml green",
    "price": "₹499",
    "rating": "4.2 out of 5",
    "category": "Kitchen"
  }'
```

**Response:**
```json
{
  "title_clean": "Eco Friendly Bottle 500ml Green",
  "price_value": 499.0,
  "rating_value": 4.2,
  "slug": "eco-friendly-bottle-500ml-green",
  "tags": ["eco", "friendly", "bottle", "500ml", "green"]
}
```

**Handles various price formats:**
- `"₹499"` → `499.0`
- `"$12.50"` → `12.5`
- `"1,299 INR"` → `1299.0`

**Handles various rating formats:**
- `"4.2 out of 5"` → `4.2`
- `"4/5"` → `4.0`
- `"4.2"` → `4.2`

---

### 3. POST `/clean/bulk`

Clean multiple products in a single request.

**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/clean/bulk" \
  -H "Content-Type: application/json" \
  -d '{
    "products": [
      {
        "title": "  premium wireless headphones  ",
        "price": "$89.99",
        "rating": "4.5 out of 5",
        "category": "Electronics"
      },
      {
        "title": "organic cotton tshirt",
        "price": "₹799",
        "rating": "4/5",
        "category": "Apparel"
      }
    ]
  }'
```

**Response:**
```json
{
  "products": [
    {
      "title_clean": "Premium Wireless Headphones",
      "price_value": 89.99,
      "rating_value": 4.5,
      "slug": "premium-wireless-headphones",
      "tags": ["premium", "wireless", "headphones"]
    },
    {
      "title_clean": "Organic Cotton Tshirt",
      "price_value": 799.0,
      "rating_value": 4.0,
      "slug": "organic-cotton-tshirt",
      "tags": ["organic", "cotton", "tshirt"]
    }
  ]
}
```

## Running Tests

Run the test suite:

```bash
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=app --cov-report=term-missing
```

## Project Structure

```
product-cleaner-api/
├── app/
│   ├── __init__.py           # Package initialization
│   ├── main.py               # FastAPI app and route definitions
│   ├── schemas.py            # Pydantic models for request/response
│   └── utils.py              # Data cleaning and parsing functions
├── tests/
│   └── test_endpoints.py     # API endpoint tests
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Freelance Use Case

This API is designed for **ecommerce store owners**, **virtual assistants**, and **data teams** who need to clean product data before uploading to platforms like:

- **Shopify / WooCommerce**: Standardize product titles and prices from supplier feeds
- **Amazon / eBay**: Generate SEO-friendly slugs and extract relevant tags for listings
- **Custom storefronts**: Normalize vendor data imports with inconsistent formatting

### Typical Workflow:

1. **Export** messy product data from supplier CSV/Excel
2. **Call** the `/clean/bulk` endpoint with your product list
3. **Receive** cleaned, structured JSON with normalized fields
4. **Import** directly into your ecommerce platform or database

By standardizing product data upfront, you reduce manual editing time, improve SEO, and maintain consistent catalog quality across your store.

## Development

To add new cleaning functions:

1. Add pure function to `app/utils.py`
2. Update Pydantic models in `app/schemas.py` if needed
3. Use the function in `app/main.py` endpoint logic
4. Add tests in `tests/test_endpoints.py`

## License

MIT
