import pandas as pd
import requests

# 1. Load CSV
df = pd.read_csv('us-shein-mens_clothes-1891.csv')

# 2. Map CSV columns to your JSON Schema
products = []
for _, row in df.head(50).iterrows(): # Testing with first 50 rows
    products.append({
        "title": str(row['goods-title-link']),
        "price": str(row['price']),
        "rating": "0", # CSV lacks ratings, providing default
        "category": str(row['rank-sub']) if pd.notna(row['rank-sub']) else "Men's Fashion"
    })

# 3. Send to API
response = requests.post(
    "https://products-cleaner-api.onrender.com/clean/bulk",
    json={"products": products}
)

# 4. Save the Cleaned JSON result
if response.status_code == 200:
    with open('cleaned_products.json', 'w') as f:
        f.write(response.text)

    print("Done! Check cleaned_products.json")
